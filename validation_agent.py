from schemas import ValidationPlan
from llm import structured_completion
from helpers import startup_context


class ValidationAgent:
    name = "Validation Agent"

    def run(self, startup: dict, context: str) -> ValidationPlan:
        system = """
You are the Validation Agent.

Convert the highest-impact and highest-uncertainty assumptions into practical
experiments.

For every experiment provide:
- the assumption,
- a concrete experiment,
- a measurable success criterion,
- priority.

Also produce a realistic 7-day validation roadmap.

Be brief: at most 4 experiments, one short sentence per field, and one
short sentence per day in the 7-day plan.

Do not recommend vague actions such as "do market research."
Prefer interviews, pricing tests, landing-page tests, prototype tests,
pre-orders, pilot signups, or other measurable experiments.
"""

        user = f"""
STARTUP
{startup_context(startup)}

ANALYSIS CONTEXT
{context}

Create the validation experiments and 7-day plan.
"""

        return structured_completion(system, user, ValidationPlan)
