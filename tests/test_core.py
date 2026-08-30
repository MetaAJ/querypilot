import sqlite3

import pytest

from querypilot.database import execute_read_only, schema_summary
from querypilot.forecast import forecast_linear
from querypilot.safety import UnsafeQueryError, validate_read_only_sql


def test_read_only_database_access() -> None:
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE leads (lead_id INTEGER, score INTEGER)")
    connection.execute("INSERT INTO leads VALUES (1, 80)")
    assert execute_read_only(connection, "SELECT * FROM leads") == [{"lead_id": 1, "score": 80}]
    assert schema_summary(connection) == {"leads": ["lead_id", "score"]}


@pytest.mark.parametrize("query", ["DELETE FROM leads", "SELECT 1; SELECT 2", "PRAGMA user_version"])
def test_rejects_unsafe_sql(query: str) -> None:
    with pytest.raises(UnsafeQueryError):
        validate_read_only_sql(query)


def test_forecast_has_baseline_and_uncertainty() -> None:
    result = forecast_linear("qualified leads", [10, 12, 14, 16], horizon=2)
    assert result.prediction[0] > result.baseline[0]
    assert result.lower_bound[0] <= result.prediction[0] <= result.upper_bound[0]
