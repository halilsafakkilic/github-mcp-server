import asyncio

from fastmcp import Client
from fastmcp.client.transports import StdioTransport

from lib.sampling import build_sampling_handler

transport = StdioTransport(command="uv", args=["run", "server"])


async def main():
    async with Client(transport, sampling_handler=build_sampling_handler()) as client:
        resources = await client.list_resources()
        print("listResources", resources)

        greeting = await client.read_resource("greeting://HSK")
        print("readResource", greeting)

        prompts = await client.list_prompts()
        print("listPrompts", prompts)

        tools = await client.list_tools()
        print("listTools", tools)

        result = await client.call_tool("get_user_repos", {"username": "halilsafakkilic"})
        print("get_user_repos", result)

        try:
            analysis = await client.call_tool("analyze_user_repos", {"username": "halilsafakkilic"})
            print("analyze_user_repos", analysis)
        except Exception as e:
            print("Error calling analyze_user_repos:", e)


if __name__ == "__main__":
    asyncio.run(main())
