# ForgeFlow synthetic data

ForgeFlow is a fictional developer-tools SaaS company. The database is generated
locally and contains no real customer information. Run the generator from the
repository root:

```bash
uv run python scripts/generate_dataset.py
```

The generator is deterministic so demo results and tests remain reproducible.

The database is exposed to TrueForge through the read-only MCP server:

```bash
uv run python scripts/run_mcp_server.py
```

The Streamable HTTP endpoint is `http://localhost:8001/mcp`.
