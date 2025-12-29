import asyncio

from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from mcp.types import CallToolResult
from pydantic import AnyUrl

from app.constants import SHTTP_PORT

server_params = {
    "url": f"http://localhost:{SHTTP_PORT}/mcp/",
}

# DEPRECATION WARNING: streamable_http transport is deprecated and will be removed in future versions. Please use SSE or WebSocket transports instead.


async def main():
    async with streamablehttp_client(**server_params) as (shttp, write, _):
        async with ClientSession(shttp, write) as session:
            await session.initialize()

            response = await session.list_resources()
            print("listResources", response)

            response = await session.read_resource(AnyUrl("greeting://HSK"))
            print("readResource", response)

            response = await session.list_prompts()
            print("listPrompts", response)

            response = await session.list_tools()
            print("listTools", response)

            response: CallToolResult = await session.call_tool("get_user_repos", {"username": "halilsafakkilic"})
            print("response", response)


if __name__ == "__main__":
    asyncio.run(main())
