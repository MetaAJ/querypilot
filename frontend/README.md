# QueryPilot frontend

The frontend will consume the backend contract rather than call the database or
model directly. The first screen should show the question, agent activity, metric
contract, SQL/evidence, forecast chart, and approval request in that order.

Planned endpoints:

- `GET /health`
- `POST /api/analysis`
- `GET /api/forecast?horizon=4`
