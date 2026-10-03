from config import SCORING_WEIGHTS


def calculate_scores(results: dict) -> dict:
    values = {
        "Problem Strength": results["problem"].score,
        "Customer Clarity": results["customer"].score,
        "Market Opportunity": results["market"].score,
        "Competition": results["competitor"].score,
        "Differentiation": results["business"].score,
        "Business Model": results["business"].score,
        "Technical Feasibility": results["feasibility"].score,
        "Operational Feasibility": results["feasibility"].score,
        "Risk": results["risk"].score,
    }

    overall = round(
        sum(values[name] * weight for name, weight in SCORING_WEIGHTS.items())
    )

    return {
        "overall": overall,
        "categories": values,
    }
