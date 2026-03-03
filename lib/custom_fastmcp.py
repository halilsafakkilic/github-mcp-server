from typing import Optional

from fastmcp import FastMCP


class CustomFastMCP(FastMCP):
    async def run_sse_async(
        self,
        host: str = "0.0.0.0",
        port: int = 8081,
        uvicorn_config_params: Optional[dict] = None,
    ) -> None:
        await self.run_http_async(
            transport="sse",
            host=host,
            port=port,
            uvicorn_config=uvicorn_config_params or {},
        )

    async def run_streamable_http_async(
        self,
        host: str = "0.0.0.0",
        port: int = 8080,
        uvicorn_config_params: Optional[dict] = None,
    ) -> None:
        await self.run_http_async(
            transport="streamable-http",
            host=host,
            port=port,
            uvicorn_config=uvicorn_config_params or {},
        )
