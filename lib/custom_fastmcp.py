from typing import Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
import uvicorn


class CustomFastMCP(FastMCP):
    async def run_sse_async(
        self,
        starlette_params: Optional[dict] = None,
        starlette_routes: Optional[list] = None,
        uvicorn_config_params: Optional[dict] = None,
    ) -> None:
        # Starlette configuration
        from starlette.applications import Starlette

        starlette_params = starlette_params or {}
        starlette_routes = starlette_routes or []

        if "debug" not in starlette_params:
            starlette_params["debug"] = self.settings.debug

        if "routes" not in starlette_params:
            sse = SseServerTransport("/messages/")

            async def handle_sse(request):
                async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
                    await self._mcp_server.run(
                        streams[0],
                        streams[1],
                        self._mcp_server.create_initialization_options(),
                    )

            from starlette.routing import Mount, Route

            starlette_params["routes"] = [
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ]

        # Route merging
        if starlette_routes:
            if "routes" in starlette_params:
                starlette_params["routes"].extend(starlette_routes)
            else:
                starlette_params["routes"] = starlette_routes

        starlette_app = Starlette(**starlette_params)

        # Uvicorn configuration
        uvicorn_config_params = uvicorn_config_params or {}
        if "host" not in uvicorn_config_params:
            uvicorn_config_params["host"] = self.settings.host

        if "port" not in uvicorn_config_params:
            uvicorn_config_params["port"] = self.settings.port

        if "log_level" not in uvicorn_config_params:
            uvicorn_config_params["log_level"] = self.settings.log_level.lower()

        config = uvicorn.Config(starlette_app, **uvicorn_config_params)

        server = uvicorn.Server(config)

        await server.serve()
