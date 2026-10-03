from schemas import FinalReport
from llm import structured_completion
from helpers import startup_context


class SynthesisAgent:
    name = "Synthesis / CEO Agent"

    def run(self, startup: dict, context: str) -> FinalReport:
        system = """
You are the final Synthesis Agent / CEO AI of a startup validation system.

Create an evidence-aware final report from the supplied agent outputs.

Important:
- Do NOT claim the startup will succeed.
- Do NOT present the overall score as probability of success.
- The score represents current strength of the startup case based on available
  information.
- Clearly distinguish evidence, AI analysis, assumptions and unknowns.
- The most useful outcome is the next thing the founder should validate.
- Keep all conclusions grounded in the supplied information.
- If evidence is weak, say so.
- Do not invent sources or statistics.

The report must be practical for an early-stage founder.
"""

        user = f"""
STARTUP
{startup_context(startup)}

FULL AGENT CONTEXT
{context}

Produce the final structured validation report.
"""

        return structured_completion(system, user, FinalReport)
