from querypilot.dataset import create_dataset
from querypilot.service import run_forecast, run_local_analysis


def test_local_analysis_returns_evidence(tmp_path) -> None:
    database_path = create_dataset(tmp_path / "querypilot.db")
    result = run_local_analysis("Why did qualified leads change?", database_path)
    assert result.contract.metric_name == "qualified leads"
    assert result.evidence[0].query_id == "qualified-leads-monthly-v1"
    assert len(result.evidence[0].supporting_rows) == 6
    assert result.approval_required is True
    assert result.forecast is not None
    assert len(result.forecast.prediction) == 4


def test_forecast_horizon_is_respected(tmp_path) -> None:
    database_path = create_dataset(tmp_path / "querypilot.db")
    result = run_forecast(database_path, horizon=3)
    assert len(result.prediction) == 3
    assert len(result.lower_bound) == 3
