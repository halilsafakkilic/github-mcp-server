from app.server import mcp_server
from app.constants import SHTTP_PORT

mcp_server.settings.host = "0.0.0.0"
mcp_server.settings.port = SHTTP_PORT

uvicorn_config_params = {"timeout_graceful_shutdown": 5}

# DEPRECATION WARNING: streamable_http transport is deprecated and will be removed in future versions. Please use SSE or WebSocket transports instead.


def main():
    import asyncio

    asyncio.run(mcp_server.run_streamable_http_async(uvicorn_config_params=uvicorn_config_params))


if __name__ == "__main__":
    main()
