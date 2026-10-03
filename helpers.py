def startup_context(startup: dict) -> str:
    return "\n".join(
        [
            f"Startup: {startup['startup_name']}",
            f"Idea: {startup['idea']}",
            f"Problem: {startup['problem']}",
            f"Customer: {startup['customer']}",
            f"Solution: {startup['solution']}",
            f"Business model: {startup['business_model']}",
            f"Location: {startup['location']}",
            f"Industry: {startup['industry']}",
            f"Stage: {startup['stage']}",
        ]
    )


def compact_result(name: str, result) -> dict:
    return {
        "agent": name,
        "score": result.score,
        "confidence": result.confidence,
        "summary": result.summary,
        "evidence": result.evidence,
        "unknowns": result.unknowns,
    }


def trim_text(text: str, limit: int) -> str:
    """Cut text to roughly `limit` characters at a word boundary."""
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + " ..."


def _pick(items, limit: int = 2) -> str:
    return "; ".join(str(item).strip() for item in (items or [])[:limit])


def brief(name: str, result) -> str:
    """Short one-paragraph version of an agent result (saves tokens)."""
    return (
        f"{name} [score {result.score}, {result.confidence}] {result.summary} "
        f"Strengths: {_pick(result.strengths)} | Risks: {_pick(result.risks)} "
        f"| Unknowns: {_pick(result.unknowns)}"
    )


def brief_red_team(result) -> str:
    return (
        f"RED TEAM [score {result.score}, {result.confidence}] {result.summary} "
        f"Challenges: {_pick(result.challenges, 3)} | "
        f"Critical assumptions: {_pick(result.critical_assumptions, 3)} | "
        f"Failure modes: {_pick(result.failure_modes, 2)}"
    )


def brief_validation(plan) -> str:
    experiments = " || ".join(
        f"{e.assumption} -> {e.experiment} (success: {e.success_criterion}; "
        f"{e.priority})"
        for e in plan.experiments
    )
    days = " | ".join(f"D{d.day}: {d.action}" for d in plan.seven_day_plan)
    return f"VALIDATION EXPERIMENTS: {experiments}\n7-DAY PLAN: {days}"
