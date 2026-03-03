# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MCP (Model Context Protocol) server POC built with FastMCP v3. Demonstrates GitHub repository exploration through three transport protocols (stdio, SSE, streamable HTTP) with MCP features: Tools, Resources, Prompts, Context, and Sampling.

## Commands

```bash
# Run tests
uv run pytest tests/ -v

# Run a single test file
uv run pytest tests/test_get_user_repos.py -v

# Run a single test
uv run pytest tests/test_get_user_repos.py::TestGetUserRepos::test_success_returns_repos -v

# Start servers
uv run server            # stdio transport
uv run server_sse        # SSE on port 8081
uv run server_shttp      # Streamable HTTP on port 8080

# MCP Inspector (stdio)
npx @modelcontextprotocol/inspector uv run server

# Lint
ruff check .
ruff format .

# Install with sampling support
uv add anthropic
```

## Architecture

### Server Initialization Chain

`app/server.py` creates the global `mcp_server` (CustomFastMCP instance), then imports `app/services.py` and `app/routes.py` to register decorators. Entry points (`server.py`, `server_sse.py`, `server_shttp.py`) import this shared instance and run it with the appropriate transport.

### Key Pattern: Decorator Registration

All MCP features are registered via decorators on `mcp_server` in `app/services.py`:
- `@mcp_server.tool()` — Tools receive `ctx: Context` which FastMCP auto-injects (do not pass manually)
- `@mcp_server.resource("uri://pattern")` — Resources return JSON strings
- `@mcp_server.prompt()` — Prompts return `PromptMessage` objects
- `@mcp_server.custom_route("/path", ["GET"])` — Custom HTTP routes (in `app/routes.py`)

### CustomFastMCP (`lib/custom_fastmcp.py`)

Extends `fastmcp.FastMCP` with convenience async methods (`run_sse_async`, `run_streamable_http_async`) that wrap `run_http_async()` with pre-configured transport types and optional uvicorn config.

### Response Pattern

All tool/resource responses use `lib/response.py:ApiResponse` which standardizes output as `{"success": bool, "data": {...}}` or `{"success": false, "error": "...", "error_code": "..."}`.

### Sampling (LLM Integration)

`analyze_user_repos` uses `ctx.sample()` to send data to an LLM via the client's sampling handler. Clients use `lib/sampling.py:build_sampling_handler()` which returns `AnthropicSamplingHandler` if `ANTHROPIC_API_KEY` is set, or `None` otherwise.

### Dual Logging

Tools use both `log_write_to_file()` (writes to `logs/server.log`) and `ctx.info()`/`ctx.error()` (sent to MCP client). Both are kept intentionally to demonstrate the difference.

## Configuration

Environment variables loaded via python-dotenv from `.env` (see `.env.dist` for template). FastMCP v3 settings (`FASTMCP_DEBUG`, `FASTMCP_LOG_LEVEL`) are set as env vars, not constructor args.

## Testing

Tests use `pytest-asyncio` with `mode=strict`. Fixtures in `tests/conftest.py` provide mock Context (AsyncMock), mock HTTP responses, and sample repo data. All tool functions are imported directly from `app.services` — FastMCP v3 decorators return original functions (no `.fn` unwrapping needed).

## Code Style

Ruff with 120-char line length, double quotes, 4-space indent. Rules: `E4, E7, E9, F, I` (ignoring `I001, E402, F403, E711`).
