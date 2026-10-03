from idea_agent import IdeaAgent
from problem_agent import ProblemAgent
from customer_agent import CustomerAgent
from market_agent import MarketAgent
from competitor_agent import CompetitorIntelligenceAgent
from business_agent import BusinessModelAgent
from feasibility_agent import FeasibilityAgent
from risk_agent import RiskAgent
from red_team_agent import RedTeamAgent
from validation_agent import ValidationAgent
from synthesis_agent import SynthesisAgent

from schemas import AnalysisResult
from research_tool import research_startup
from config import RESEARCH_CHARS_FOR_AGENTS, RESEARCH_CHARS_FOR_LATER_STAGES
from helpers import (
    brief,
    brief_red_team,
    brief_validation,
    compact_result,
    trim_text,
)
from scoring import calculate_scores


class StartupAnalyzer:
    def _status(self, callback, message, percent):
        if callback:
            callback(message, percent)

    def run(self, startup: dict, status_callback=None) -> dict:
        results = {}

        self._status(status_callback, "Understanding startup idea...", 5)
        idea = IdeaAgent().run(startup)
        results["idea"] = idea

        self._status(status_callback, "Researching market and competitors...", 15)
        full_research = research_startup(startup)
        research = trim_text(full_research, RESEARCH_CHARS_FOR_AGENTS)
        short_research = trim_text(full_research, RESEARCH_CHARS_FOR_LATER_STAGES)

        self._status(status_callback, "Analyzing the customer problem...", 28)
        results["problem"] = ProblemAgent().run(startup, research)

        self._status(status_callback, "Analyzing customers and buyers...", 38)
        results["customer"] = CustomerAgent().run(startup, research)

        self._status(status_callback, "Evaluating market opportunity...", 48)
        results["market"] = MarketAgent().run(startup, research)

        self._status(status_callback, "Investigating competitors and alternatives...", 58)
        results["competitor"] = CompetitorIntelligenceAgent().run(
            startup, research
        )

        self._status(status_callback, "Evaluating business model...", 66)
        results["business"] = BusinessModelAgent().run(
            startup,
            research,
        )

        self._status(status_callback, "Checking technical and operational feasibility...", 74)
        results["feasibility"] = FeasibilityAgent().run(
            startup,
            research,
        )

        self._status(status_callback, "Identifying major risks...", 80)
        results["risk"] = RiskAgent().run(
            startup,
            research,
        )

        # Compact context for later stages (saves tokens).
        agent_context = "\n".join(
            brief(key.upper(), value) for key, value in results.items()
        )

        self._status(status_callback, "Running red-team challenge...", 86)
        red_team = RedTeamAgent().run(
            startup,
            f"RESEARCH:\n{short_research}\n\nAGENT OUTPUTS:\n{agent_context}",
        )

        self._status(status_callback, "Designing validation experiments...", 91)
        validation = ValidationAgent().run(
            startup,
            f"AGENT OUTPUTS:\n{agent_context}\n\n{brief_red_team(red_team)}",
        )

        scores = calculate_scores(results)

        synthesis_context = f"""
RESEARCH:
{short_research}

CATEGORY SCORES:
{scores}

AGENT OUTPUTS:
{agent_context}

{brief_red_team(red_team)}

{brief_validation(validation)}
"""

        self._status(status_callback, "Building final evidence-aware report...", 96)
        report = SynthesisAgent().run(startup, synthesis_context)

        return {
            "research": full_research,
            "scores": scores,
            "report": report.model_dump(),
            "red_team": red_team.model_dump(),
            "validation": validation.model_dump(),
            "agent_results": [
                compact_result("Idea", results["idea"]),
                compact_result("Problem", results["problem"]),
                compact_result("Customer", results["customer"]),
                compact_result("Market", results["market"]),
                compact_result("Competitor", results["competitor"]),
                compact_result("Business Model", results["business"]),
                compact_result("Feasibility", results["feasibility"]),
                compact_result("Risk", results["risk"]),
            ],
        }
