"""Read-only MCP tools for the ForgeFlow analytics database."""

import json
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .database import connect, execute_read_only, schema_summary


server = FastMCP(
    "ForgeFlow Analytics Database",
    port=8001,
    instructions=(
        "This database is read-only. Use inspect_schema before writing SQL. "
        "Only SELECT and WITH queries are accepted."
    ),
)


def _database_path() -> Path:
    return Path(os.environ.get("QUERYPILOT_DATABASE", "data/querypilot.db"))


@server.tool()
def inspect_schema() -> str:
    """List the available ForgeFlow tables and columns."""
    with connect(_database_path()) as connection:
        return json.dumps(schema_summary(connection), indent=2)


@server.tool()
def run_read_only_query(sql: str) -> str:
    """Execute one validated SELECT/WITH query and return JSON rows."""
    with connect(_database_path()) as connection:
        rows = execute_read_only(connection, sql)
    return json.dumps({"row_count": len(rows), "rows": rows}, default=str)


@server.tool()
def get_metric_samples(metric: str = "qualified_leads") -> str:
    """Return monthly sample data for supported demo metrics."""
    queries = {
        "qualified_leads": """
            SELECT substr(created_at, 1, 7) AS month, COUNT(*) AS qualified_leads
            FROM leads WHERE lifecycle_stage = 'qualified'
            GROUP BY month ORDER BY month
        """,
        "opportunities_won": """
            SELECT substr(created_at, 1, 7) AS month, SUM(won) AS opportunities_won
            FROM opportunities GROUP BY month ORDER BY month
        """,
    }
    if metric not in queries:
        raise ValueError(f"Unsupported metric: {metric}")
    with connect(_database_path()) as connection:
        rows = execute_read_only(connection, queries[metric])
    return json.dumps({"metric": metric, "rows": rows}, default=str)


if __name__ == "__main__":
    server.run(transport="streamable-http")
