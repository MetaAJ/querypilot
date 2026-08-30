# QueryPilot Quick Start

QueryPilot is a TrueForge analytics agent. Run the local API, the read-only analytics MCP server, and TrueForge in separate WSL terminals.

## 1. Install and prepare

From the repository directory:

```bash
uv sync
uv run python scripts/generate_dataset.py
```

Configure the model, Daytona sandbox, ForgeFlow Analytics Database connector, and `skills/analytics/SKILL.md` skill in TrueForge.

## 2. Start the services

Run each command in a separate WSL terminal:

```bash
uv run uvicorn querypilot.api:app --reload --host 0.0.0.0 --port 8000
```

```bash
uv run python scripts/run_mcp_server.py
```

```bash
npx @truefoundry/trueforge@latest
```

Open the companion UI at `http://localhost:8000` and the live agent UI at `http://localhost:8790`.

## 3. Run the agent

In TrueForge, open the saved `querypilot-analytics` agent and start a new chat. Ask it to investigate qualified leads, show the read-only SQL, create a four-period forecast using Daytona, and request approval before generating an HTML report.

The authoritative agent trace is shown in TrueForge. The QueryPilot page at port `8000` is a local companion dashboard.

## Safety

Do not commit `.env` files or API keys. The analytics MCP server accepts only read-only SQL, and report creation remains approval-gated in TrueForge.
