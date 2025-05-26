import asyncio

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from mcp.types import CallToolResult
from pydantic import AnyUrl

server_params = StdioServerParameters(
    command="uv",
    args=["run", "server"],
    # env=None
)


async def main():
    async with stdio_client(server_params) as (stdio, write):
        async with ClientSession(stdio, write) as session:
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
