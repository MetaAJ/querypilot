"""Typed domain objects exchanged by the agent and frontend."""

from pydantic import BaseModel, Field


class MetricContract(BaseModel):
    metric_name: str
    definition: str
    period: str
    comparison_period: str | None = None
    exclusions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class Evidence(BaseModel):
    finding: str
    query_id: str
    supporting_rows: list[dict[str, object]] = Field(default_factory=list)
    confidence: str = "medium"


class ForecastResult(BaseModel):
    metric_name: str
    horizon: str
    baseline: list[float]
    prediction: list[float]
    lower_bound: list[float]
    upper_bound: list[float]
    limitations: list[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    question: str
    contract: MetricContract
    answer: str
    evidence: list[Evidence] = Field(default_factory=list)
    forecast: ForecastResult | None = None
    approval_required: bool = False
