# Startup Idea Analyzer — Agentic AI

A hackathon-sized startup validation copilot based on the provided PRD.

## Architecture

Streamlit → Orchestrator → Specialized Agents → Research → Red Team →
Validation → Synthesis → Dashboard

## Model

- Groq
- `openai/gpt-oss-120b`
- Python 3.12
- Streamlit

GPT-OSS 120B is used for structured agent outputs. The research step uses
Groq's built-in browser search separately because Groq documents that
browser_search is not compatible with structured outputs.

## Project Structure

```text
startup-idea-analyzer/
├── app.py
├── orchestrator.py
├── config.py
├── llm.py
├── schemas.py
├── requirements.txt
├── README.md
├── base_agent.py
├── idea_agent.py
├── problem_agent.py
├── customer_agent.py
├── market_agent.py
├── competitor_agent.py
├── business_agent.py
├── feasibility_agent.py
├── risk_agent.py
├── red_team_agent.py
├── validation_agent.py
├── synthesis_agent.py
├── research_tool.py
├── scoring.py
└── helpers.py
```

## Streamlit Cloud

1. Push the project to GitHub.
2. Create a Streamlit Cloud app from the repository.
3. Set the main file to `app.py`.
4. Add this secret:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

Do not commit your API key to GitHub.

## Important

This MVP intentionally does not include:
- database
- authentication
- payments
- mobile app
- user accounts
- complex background workers

Those are outside the core hackathon MVP in the PRD.

## Run

Python 3.12:

```bash
pip install -r requirements.txt
streamlit run app.py
```
