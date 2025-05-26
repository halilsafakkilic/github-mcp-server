import asyncio

from mcp.client.sse import sse_client
from mcp import ClientSession
from mcp.types import CallToolResult
from pydantic import AnyUrl

server_params = {
    "url": "http://localhost:8080/sse",
}


async def main():
    async with sse_client(**server_params) as (sse, write):
        async with ClientSession(sse, write) as session:
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
