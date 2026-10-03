from config import RESEARCH_MAX_TOKENS, USE_BROWSER_SEARCH
from llm import text_completion


def research_startup(startup: dict) -> str:
    query = f"""
Research the following startup idea for a validation report.

Startup: {startup['startup_name']}
Idea: {startup['idea']}
Problem: {startup['problem']}
Customer: {startup['customer']}
Solution: {startup['solution']}
Business model: {startup['business_model']}
Location: {startup['location']}
Industry: {startup['industry']}

Research:
1. Relevant market size indicators and market trends.
2. Customer behavior or demand signals.
3. Direct competitors.
4. Indirect competitors and alternatives.
5. Existing solutions and status quo.
6. Relevant pricing or monetization patterns.
7. Geographic considerations.
8. Important risks or regulatory considerations where relevant.

Use current publicly available information. Prefer credible sources.
Clearly distinguish facts/evidence from interpretation.
Include source names or URLs when available.
Do not invent statistics.
Keep the whole answer under 400 words, as short bullet points.
"""

    if USE_BROWSER_SEARCH:
        system_prompt = (
            "You are the market research specialist for a startup validation "
            "system. Perform evidence-oriented web research. Be concise but "
            "useful. If reliable evidence is unavailable, say so explicitly."
        )
    else:
        system_prompt = (
            "You are the market research specialist for a startup validation "
            "system. You have NO live web access: write background notes "
            "from general knowledge and label them clearly as unverified "
            "model knowledge, not sourced evidence. Do not cite URLs or "
            "invent statistics. Say explicitly where evidence is unavailable."
        )

    return text_completion(
        system_prompt=system_prompt,
        user_prompt=query,
        max_tokens=RESEARCH_MAX_TOKENS,
        use_browser_search=USE_BROWSER_SEARCH,
    )
