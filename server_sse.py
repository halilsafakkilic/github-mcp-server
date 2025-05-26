from app.server import mcp_server

timeout_graceful_shutdown = 5

mcp_server.settings.host = "0.0.0.0"
mcp_server.settings.port = 8080


def main():
    import asyncio

    asyncio.run(
        mcp_server.run_sse_async(uvicorn_config_params={"timeout_graceful_shutdown": timeout_graceful_shutdown})
    )


if __name__ == "__main__":
    main()
