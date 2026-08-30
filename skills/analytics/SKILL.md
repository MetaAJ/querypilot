---
name: querypilot-analytics
description: Evidence-first revenue analytics and forecasting workflow for QueryPilot.
---

# QueryPilot analytics workflow

Use this skill when a user asks a question about ForgeFlow revenue, leads, pipeline,
subscriptions, support, or product usage.

## Required workflow

1. Restate the question and create a metric contract before querying.
2. Inspect the database schema; do not invent tables or columns.
3. Delegate metric definition, SQL planning, and forecasting to specialist subagents.
4. Generate only read-only `SELECT` or `WITH` SQL.
5. Run SQL through the QueryPilot safety validator before execution.
6. Execute generated Python analysis only inside the configured sandbox.
7. Separate observed facts, model predictions, assumptions, and recommendations.
8. Include supporting query results and confidence for each material finding.
9. Show uncertainty and limitations for every forecast.
10. Ask for human approval before exporting, saving, sending, or mutating anything.

## Safety rules

- Never execute `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, or multiple statements.
- Never expose credentials or private data in an answer, log, or artifact.
- If subagents disagree, show the disagreement and run a validation query.
- Treat forecasts as projections, never as causal proof.
