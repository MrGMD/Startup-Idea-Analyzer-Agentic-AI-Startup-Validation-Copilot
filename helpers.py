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
