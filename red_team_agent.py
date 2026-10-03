from schemas import RedTeamResult
from llm import structured_completion
from helpers import startup_context


class RedTeamAgent:
    name = "Red Team Agent"

    def run(self, startup: dict, context: str) -> RedTeamResult:
        system = """
You are the Red Team Agent in a startup validation system.

Your job is to challenge the startup, not promote it.

Ask:
- Why might this idea fail?
- What if customers already use another solution?
- What if customers will not pay?
- What assumptions are unsupported?
- What could competitors copy?
- What operational, technical, regulatory or adoption issue could break the model?

Do not predict failure. Identify testable failure modes and uncertainties.
Use only supplied evidence. Never invent facts.
Be brief: summary max 2 sentences; every list max 3 short items.
"""

        user = f"""
STARTUP
{startup_context(startup)}

ANALYSIS CONTEXT
{context}

Return a structured red-team challenge.
"""

        return structured_completion(system, user, RedTeamResult)
