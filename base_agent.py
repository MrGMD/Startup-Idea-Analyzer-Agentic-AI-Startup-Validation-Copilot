from schemas import AnalysisResult
from llm import structured_completion
from helpers import startup_context


class BaseAgent:
    name = "Base Agent"
    objective = ""

    def run(self, startup: dict, context: str = "") -> AnalysisResult:
        system = f"""
You are the {self.name} in an agentic startup validation system.

Objective:
{self.objective}

Rules:
- Analyze the startup using the information provided.
- Do not claim the startup will succeed or fail.
- Separate evidence, assumptions, uncertainty, and AI reasoning.
- Never invent statistics, customers, competitors, or sources.
- Use the research dossier when supplied.
- Score the current strength of the relevant dimension from 0 to 100.
- Confidence must be one of: Low, Medium, High.
- Recommendations must be actionable.
- Keep the response concise enough for a hackathon application.
"""

        user = f"""
STARTUP INFORMATION
{startup_context(startup)}

RESEARCH / OTHER AGENT CONTEXT
{context or "No additional context."}

Return the requested structured analysis.
"""

        return structured_completion(system, user, AnalysisResult)
