# QueryPilot

QueryPilot is an evidence-first analytics and forecasting copilot built for the TrueForge Agent Harness Hackathon. It helps revenue teams investigate business questions, generate safe SQL, forecast future trends, and understand the evidence behind each conclusion.

The fictional company behind the demo is ForgeFlow, a developer-tools SaaS company. The repository contains a deterministic synthetic dataset and a read-only SQLite MCP server. TrueForge is the agent runtime that coordinates the model, skill, tools, subagents, sandbox, session, and human approval checkpoint.

## Architecture

```text
TrueForge Chat UI / agent session
  ├── OpenAI model
  ├── QueryPilot analytics skill
  ├── ForgeFlow Analytics Database MCP server
  ├── Metric, SQL, and forecast subagents
  ├── Daytona sandbox for generated Python
  └── Approval gate before report export

QueryPilot application
  ├── FastAPI API and local companion UI
  ├── Read-only SQL safety layer
  ├── Forecasting and evidence models
  └── Synthetic ForgeFlow SQLite dataset
```

## What the agent does

For a question such as “Why did qualified leads change, and what should we expect next?”, QueryPilot:

1. Creates a metric contract.
2. Inspects the real database schema through MCP.
3. Delegates metric, SQL, and forecasting work to specialist agents.
4. Executes only read-only SQL.
5. Runs generated Python analysis inside Daytona.
6. Compares a forecast with a last-value baseline.
7. Reports evidence, uncertainty, and limitations.
8. Pauses for explicit approval before creating an export.

## Run locally

The commands below are intended for Ubuntu/WSL. The Windows virtual environment must not be reused inside WSL.

```bash
cd "/mnt/c/Users/Akshaj Manchanda/Documents/ChatGPT/Agent Harness Hackathon"
uv venv
source .venv/bin/activate
uv sync
export PYTHONPATH=src
python scripts/generate_dataset.py
```

### QueryPilot companion app

In one terminal:

```bash
export PYTHONPATH=src
uv run uvicorn querypilot.api:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000`. The custom UI is the QueryPilot product shell and local companion view. It is intentionally separate from the TrueForge runtime.

### ForgeFlow MCP server

In a second terminal:

```bash
export PYTHONPATH=src
uv run python scripts/run_mcp_server.py
```

The read-only Streamable HTTP MCP endpoint is `http://localhost:8001/mcp`.
It exposes `inspect_schema`, `run_read_only_query`, and `get_metric_samples`.

### TrueForge

In a third Ubuntu/WSL terminal:

```bash
npx @truefoundry/trueforge@latest
```

Open `http://localhost:8790`, then configure an OpenAI-compatible model, the ForgeFlow MCP connector at `http://localhost:8001/mcp`, the `skills/analytics/SKILL.md` skill from the `master` branch, and Daytona as the sandbox provider.

The actual agent should be run from the saved QueryPilot agent in the TrueForge UI. The MCP server and QueryPilot API must remain running while the agent is tested.

## Demo prompts

```text
Investigate why qualified leads changed over time.

Use the QueryPilot analytics skill. First create a metric contract. Inspect the ForgeFlow database schema. Compare monthly qualified leads by campaign channel. Show the read-only SQL before executing it. Use the ForgeFlow Analytics Database connector. Do not export or modify anything.
```

```text
Create a four-period qualified-leads forecast.
Use the Daytona sandbox to execute Python.
Show the generated Python code, model forecast, last-value baseline, uncertainty range, and limitations. Do not export anything.
```

```text
Create an HTML report containing the metric contract, monthly results, forecast, baseline comparison, uncertainty ranges, and limitations. Before creating or saving the file, pause and ask me for approval. Do not create the file until I explicitly approve.
```

## Safety

- Database access is read-only by default.
- SQL accepts only one `SELECT` or `WITH` statement.
- Generated Python runs in a disposable Daytona sandbox.
- Forecasts are labeled as projections and include limitations.
- Exports and other persistent actions require human approval.
- No credentials or real customer data are stored in this repository.

## Project layout

```text
src/querypilot/       Python domain logic, API, MCP server, and forecasting
scripts/              Dataset and MCP server launch scripts
data/                 Synthetic ForgeFlow dataset documentation
skills/analytics/     TrueForge git-backed skill
frontend/             QueryPilot companion UI
tests/                Core, dataset, API, and event-contract tests
```

## Qodo Code Review Evidence

Qodo reviewed the representative TrueForge integration pull request before merge. The review reported zero material bugs, rule violations, and requirement gaps.

Review PR: https://github.com/MetaAJ/querypilot/pull/1

## Submission checklist

- [x] Public GitHub repository.
- [x] TrueForge agent using a real MCP connector.
- [x] Skill loaded from the repository.
- [x] Python forecast executed in Daytona.
- [x] Human approval shown before HTML export.
- [x] Qodo-reviewed and merged pull request.
- [ ] Three-minute demo video.
- [ ] Final hackathon write-up and submission form.
