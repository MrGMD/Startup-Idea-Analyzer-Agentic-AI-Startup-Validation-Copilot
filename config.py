import os

MODEL_NAME = "openai/gpt-oss-120b"
GROQ_API_KEY_ENV = "GROQ_API_KEY"

# GPT-OSS 120B supports long context and structured outputs on Groq.
# Moderate output limits help keep hackathon usage under control.
MAX_COMPLETION_TOKENS = 1800
TEMPERATURE = 0.2
REASONING_EFFORT = "medium"

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
