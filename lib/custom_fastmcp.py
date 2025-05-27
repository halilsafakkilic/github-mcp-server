from typing import Optional

from mcp.server.fastmcp import FastMCP


class CustomFastMCP(FastMCP):
    async def run_sse_async(self, mount_path: str | None = None, uvicorn_config_params: Optional[dict] = None) -> None:
        starlette_app = self.sse_app(mount_path)

        await self._start_uvicorn(starlette_app, uvicorn_config_params)

    async def run_streamable_http_async(self, uvicorn_config_params: Optional[dict] = None) -> None:
        starlette_app = self.streamable_http_app()

        await self._start_uvicorn(starlette_app, uvicorn_config_params)

    def _get_uvicorn_config(self, uvicorn_config_params: Optional[dict] = None) -> dict:
        uvicorn_config_params = uvicorn_config_params or {}
        if "host" not in uvicorn_config_params:
            uvicorn_config_params["host"] = self.settings.host

        if "port" not in uvicorn_config_params:
            uvicorn_config_params["port"] = self.settings.port

        if "log_level" not in uvicorn_config_params:
            uvicorn_config_params["log_level"] = self.settings.log_level.lower()

        return uvicorn_config_params

    async def _start_uvicorn(self, starlette_app, uvicorn_config_params: [dict] = None):
        import uvicorn

        config = uvicorn.Config(starlette_app, **self._get_uvicorn_config(uvicorn_config_params))
        server = uvicorn.Server(config)

        await server.serve()
