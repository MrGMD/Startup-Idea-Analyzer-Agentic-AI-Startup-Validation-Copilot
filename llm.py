import json
import os
from typing import Type

import streamlit as st
from groq import Groq
from pydantic import BaseModel

from config import (
    MODEL_NAME,
    MAX_COMPLETION_TOKENS,
    TEMPERATURE,
    REASONING_EFFORT,
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


def _schema_for(model: Type[BaseModel]) -> dict:
    return model.model_json_schema()


def structured_completion(
    system_prompt: str,
    user_prompt: str,
    output_model: Type[BaseModel],
) -> BaseModel:
    client = get_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=TEMPERATURE,
        max_completion_tokens=MAX_COMPLETION_TOKENS,
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

    content = response.choices[0].message.content
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
    max_tokens: int = 2200,
    use_browser_search: bool = False,
) -> str:
    client = get_client()

    kwargs = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_completion_tokens": max_tokens,
        "reasoning_effort": "medium",
    }

    if use_browser_search:
        # Browser search is intentionally kept separate from structured
        # outputs because Groq documents that browser_search is not
        # compatible with structured outputs.
        kwargs["tools"] = [{"type": "browser_search"}]

    response = client.chat.completions.create(**kwargs)
    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("Groq returned an empty response.")

    return content
