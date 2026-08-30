"""Deterministic local analysis service used behind the TrueForge agent."""

from pathlib import Path

from .database import connect, execute_read_only
from .forecast import forecast_linear
from .models import AnalysisResult, Evidence, ForecastResult, MetricContract


QUALIFIED_LEADS_QUERY = """
SELECT substr(created_at, 1, 7) AS month,
       COUNT(*) AS qualified_leads,
       ROUND(AVG(sales_response_hours), 1) AS avg_response_hours
FROM leads
WHERE lifecycle_stage = 'qualified'
GROUP BY month
ORDER BY month
"""


def run_local_analysis(question: str, database_path: str | Path) -> AnalysisResult:
    """Run the first supported demo analysis without requiring a model API."""
    connection = connect(database_path)
    try:
        rows = execute_read_only(connection, QUALIFIED_LEADS_QUERY)
    finally:
        connection.close()

    contract = MetricContract(
        metric_name="qualified leads",
        definition="Leads whose lifecycle stage is qualified",
        period="all available months",
        comparison_period="month-over-month",
        exclusions=["No synthetic test records are included"],
        limitations=["This local demo does not infer causality"],
    )
    evidence = Evidence(
        finding="Qualified leads and average response time are grouped by month for investigation.",
        query_id="qualified-leads-monthly-v1",
        supporting_rows=rows[-6:],
        confidence="high",
    )
    values = [float(row["qualified_leads"]) for row in rows]
    forecast = forecast_linear("qualified leads", values, horizon=4)
    return AnalysisResult(
        question=question,
        contract=contract,
        answer=(
            "The investigation is ready: monthly qualified-lead volume and sales response "
            "time were calculated from the read-only database query. TrueForge can now ask "
            "specialist agents to interpret the trend and forecast the next periods."
        ),
        evidence=[evidence],
        forecast=forecast,
        approval_required=True,
    )


def run_forecast(database_path: str | Path, horizon: int = 4) -> ForecastResult:
    """Build the demo forecast from monthly qualified-lead observations."""
    connection = connect(database_path)
    try:
        rows = execute_read_only(connection, QUALIFIED_LEADS_QUERY)
    finally:
        connection.close()
    return forecast_linear(
        "qualified leads",
        [float(row["qualified_leads"]) for row in rows],
        horizon=horizon,
    )
