from app.server import mcp_server
from app.constants import SSE_PORT

mcp_server.settings.host = "0.0.0.0"
mcp_server.settings.port = SSE_PORT

uvicorn_config_params = {"timeout_graceful_shutdown": 5}


def main():
    import asyncio

    asyncio.run(mcp_server.run_sse_async(uvicorn_config_params=uvicorn_config_params))


if __name__ == "__main__":
    main()
