from typing import List
from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    score: int = Field(ge=0, le=100)
    confidence: str
    summary: str
    strengths: List[str]
    findings: List[str]
    risks: List[str]
    assumptions: List[str]
    unknowns: List[str]
    evidence: List[str]
    recommendations: List[str]


class ValidationExperiment(BaseModel):
    assumption: str
    experiment: str
    success_criterion: str
    priority: str


class DayPlan(BaseModel):
    day: int
    action: str


class ValidationPlan(BaseModel):
    experiments: List[ValidationExperiment]
    seven_day_plan: List[DayPlan]


class RedTeamResult(BaseModel):
    score: int = Field(ge=0, le=100)
    confidence: str
    summary: str
    challenges: List[str]
    critical_assumptions: List[str]
    failure_modes: List[str]
    evidence: List[str]
    recommendations: List[str]


class FinalReport(BaseModel):
    overall: int = Field(ge=0, le=100)
    evidence_strength: str
    biggest_strength: str
    biggest_unknown: str
    biggest_risk: str
    next_action: str
    decision_focus: str

    executive_summary: str
    problem_analysis: str
    customer_analysis: str
    market_analysis: str
    competitor_landscape: str
    differentiation: str
    business_model: str
    feasibility: str
    risk_analysis: str
    assumption_map: str
    red_team_findings: str
    validation_experiments: str
    seven_day_plan: str
    recommendations: str
