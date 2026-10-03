import json
import os
import re
import time
from collections import deque
from typing import Optional, Type

import streamlit as st
from groq import Groq
from pydantic import BaseModel

from config import (
    MODEL_NAME,
    FINAL_MODEL_NAME,
    MAX_COMPLETION_TOKENS,
    MAX_RETRY_TOKENS,
    TEMPERATURE,
    REASONING_EFFORT,
    THROTTLE_FREE_TIER,
    TOKENS_PER_MINUTE_BUDGET,
)


def get_api_key() -> str:
    try:
        key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        key = None

    key = key or os.getenv("GROQ_API_KEY")

    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to Streamlit Cloud Secrets."
        )
    return key


_client = None


def get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=get_api_key())
    return _client


_UNSUPPORTED_KEYS = {"title", "minimum", "maximum", "default"}


def _strictify(node, defs):
    """Make a Pydantic JSON schema acceptable to Groq strict mode.

    - inlines $ref/$defs
    - sets additionalProperties: false on every object
    - marks every property as required
    - removes keywords strict mode does not support
    """
    if isinstance(node, list):
        return [_strictify(item, defs) for item in node]

    if not isinstance(node, dict):
        return node

    if "$ref" in node:
        name = node["$ref"].split("/")[-1]
        return _strictify(defs[name], defs)

    result = {}
    for key, value in node.items():
        if key in _UNSUPPORTED_KEYS and not isinstance(value, dict):
            continue
        if key == "$defs":
            continue
        if key == "properties":
            result[key] = {k: _strictify(v, defs) for k, v in value.items()}
        else:
            result[key] = _strictify(value, defs)

    if result.get("type") == "object" or "properties" in result:
        result["additionalProperties"] = False
        result["required"] = list(result.get("properties", {}).keys())

    return result


def _schema_for(model: Type[BaseModel]) -> dict:
    schema = model.model_json_schema()
    return _strictify(schema, schema.get("$defs", {}))


_usage = {}        # model -> deque of (timestamp, tokens)
_exhausted = {}    # model -> time its daily limit was hit
EXHAUSTED_COOLDOWN = 1800


def _is_rate_limit(exc: Exception) -> bool:
    text = str(exc).lower()
    return "429" in text or "rate_limit" in text or "rate limit" in text


def _is_schema_failure(exc: Exception) -> bool:
    """Model produced JSON that does not match the schema (a random glitch,
    most common on the smaller model). Retrying usually fixes it."""
    text = str(exc).lower()
    return "json_validate_failed" in text or "does not match the expected schema" in text


def _retry_seconds(text: str) -> float:
    """Read 'try again in 7m51.7s' / '2.5s' / '820ms' from a Groq error."""
    ms = re.search(r"try again in\s+(\d+(?:\.\d+)?)ms", text)
    if ms:
        return float(ms.group(1)) / 1000
    m = re.search(r"try again in\s+(?:(\d+)m)?(?:(\d+(?:\.\d+)?)s)?", text)
    if not m or not (m.group(1) or m.group(2)):
        return 5.0
    return int(m.group(1) or 0) * 60 + float(m.group(2) or 0)


def _estimate_tokens(messages, max_tokens: int) -> int:
    chars = sum(len(m["content"]) for m in messages)
    return chars // 4 + max_tokens


def _wait_for_capacity(model: str, needed: int) -> None:
    """Pause so we stay under the per-minute token limit of the free plan."""
    if not THROTTLE_FREE_TIER:
        return

    window = _usage.setdefault(model, deque())
    while True:
        now = time.time()
        while window and now - window[0][0] >= 60:
            window.popleft()
        used = sum(tokens for _, tokens in window)
        if not window or used + needed <= TOKENS_PER_MINUTE_BUDGET:
            return
        time.sleep(max(1.0, 60 - (now - window[0][0]) + 0.5))


def _record_usage(model: str, response) -> None:
    usage = getattr(response, "usage", None)
    tokens = getattr(usage, "total_tokens", None) if usage else None
    if tokens:
        _usage.setdefault(model, deque()).append((time.time(), tokens))


def _create(client: Groq, model: str, messages, max_tokens: int, **kwargs):
    """Call Groq on `model`. Waits out per-minute limits; if a model's daily
    limit is exhausted, tries the other configured model instead."""
    candidates = [model] + [
        m for m in (MODEL_NAME, FINAL_MODEL_NAME) if m != model
    ]
    last_exc = None

    for candidate in candidates:
        if time.time() - _exhausted.get(candidate, 0) < EXHAUSTED_COOLDOWN:
            continue

        for attempt in range(3):
            _wait_for_capacity(candidate, _estimate_tokens(messages, max_tokens))
            try:
                response = client.chat.completions.create(
                    model=candidate,
                    messages=messages,
                    max_completion_tokens=max_tokens,
                    **kwargs,
                )
            except Exception as exc:
                if _is_schema_failure(exc):
                    last_exc = exc
                    if attempt >= 1:
                        break  # give up on this model, try the other one
                    continue
                if not _is_rate_limit(exc):
                    raise
                last_exc = exc
                text = str(exc)
                if "(TPD)" in text or "per day" in text.lower():
                    _exhausted[candidate] = time.time()
                    break
                wait = _retry_seconds(text)
                if wait > 90:
                    break
                time.sleep(wait + 1)
                continue

            _record_usage(candidate, response)
            return response

    raise last_exc or RuntimeError(
        "Rate limit (429): daily token limit reached on all configured models."
    )


def structured_completion(
    system_prompt: str,
    user_prompt: str,
    output_model: Type[BaseModel],
    model: Optional[str] = None,
    max_tokens: Optional[int] = None,
) -> BaseModel:
    client = get_client()

    model = model or MODEL_NAME
    max_tokens = max_tokens or MAX_COMPLETION_TOKENS
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    content = None

    # Reasoning tokens count against max_completion_tokens, so a small limit
    # can leave no room for the JSON answer. Retry with a larger budget.
    for _ in range(3):
        response = _create(
            client,
            model,
            messages,
            max_tokens,
            temperature=TEMPERATURE,
            reasoning_effort=REASONING_EFFORT,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": output_model.__name__.lower(),
                    "strict": True,
                    "schema": _schema_for(output_model),
                },
            },
        )

        choice = response.choices[0]
        content = choice.message.content
        if content and choice.finish_reason != "length":
            break

        content = None
        max_tokens = min(int(max_tokens * 1.5), MAX_RETRY_TOKENS)

    if not content:
        raise RuntimeError("Groq returned an empty response.")

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Groq returned invalid JSON.") from exc

    return output_model.model_validate(data)


def text_completion(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 900,
    use_browser_search: bool = False,
    model: Optional[str] = None,
) -> str:
    client = get_client()

    model = model or MODEL_NAME
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    kwargs = {"temperature": 0.2, "reasoning_effort": "low"}

    if use_browser_search:
        # Browser search is kept separate from structured outputs because
        # Groq documents that browser_search is not compatible with them.
        kwargs["tools"] = [{"type": "browser_search"}]

    content = None
    for _ in range(3):
        response = _create(client, model, messages, max_tokens, **kwargs)
        content = response.choices[0].message.content
        if content:
            break
        max_tokens = min(int(max_tokens * 1.5), MAX_RETRY_TOKENS)

    if not content:
        raise RuntimeError("Groq returned an empty response.")

    return content
