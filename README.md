# QueryPilot

QueryPilot is an evidence-first analytics and forecasting copilot for the TrueForge
Agent Harness Hackathon. It helps revenue teams investigate business questions,
generate safe SQL, forecast future trends, and understand the evidence behind each
conclusion.

## Product flow

```text
Question → metric contract → schema inspection → specialist subagents
→ read-only SQL → sandboxed forecast → evidence-backed answer → approval-gated export
```

TrueForge orchestrates the model, MCP tools, skills, subagents, sandbox execution,
sessions, and human approvals. QueryPilot provides the domain logic, synthetic
ForgeFlow revenue dataset, safety policies, API, and user interface.

## Development

```bash
uv sync
uv run uvicorn querypilot.api:app --reload
```

Open `http://localhost:8000` for the QueryPilot workspace. The API health check is
available at `http://localhost:8000/health`.

## Safety principles

- Database access is read-only by default.
- Generated SQL is validated before execution.
- Generated Python analysis runs in a TrueForge sandbox.
- Forecasts include uncertainty and limitations.
- Exports and other persistent actions require human approval.
- Secrets and real customer data stay outside the repository.

## Qodo Code Review Evidence

This section will link to the representative merged pull request and summarize the
Qodo findings addressed before final submission.
