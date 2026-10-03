import os

# Analysis agents use the smaller model (separate daily quota on Groq).
MODEL_NAME = "openai/gpt-oss-20b"
# Only the final report uses the larger model.
FINAL_MODEL_NAME = "openai/gpt-oss-120b"
GROQ_API_KEY_ENV = "GROQ_API_KEY"

# Token budget (reasoning tokens count against these limits).
MAX_COMPLETION_TOKENS = 1800
FINAL_MAX_COMPLETION_TOKENS = 3500
MAX_RETRY_TOKENS = 5000
TEMPERATURE = 0.2
REASONING_EFFORT = "low"

# Live web research is the most token-hungry step. Keep it off on the free
# plan; set to True after upgrading (or if you have spare quota).
USE_BROWSER_SEARCH = False
RESEARCH_MAX_TOKENS = 900

# How much research text is passed on to the agents (characters).
RESEARCH_CHARS_FOR_AGENTS = 2500
RESEARCH_CHARS_FOR_LATER_STAGES = 1200

# Free-plan pacing: Groq's free plan allows ~8,000 tokens per minute per model.
# Set THROTTLE_FREE_TIER = False after upgrading to the Developer tier.
THROTTLE_FREE_TIER = True
TOKENS_PER_MINUTE_BUDGET = 7000

SCORING_WEIGHTS = {
    "Problem Strength": 0.15,
    "Customer Clarity": 0.10,
    "Market Opportunity": 0.15,
    "Competition": 0.10,
    "Differentiation": 0.15,
    "Business Model": 0.15,
    "Technical Feasibility": 0.10,
    "Operational Feasibility": 0.05,
    "Risk": 0.05,
}
