import asyncio

from app.constants import GITHUB_API_TIMEOUT
from lib.response import ApiResponse
from lib.utils import log_write_to_file, get_request
from app.server import mcp_server
from fastmcp.prompts.prompt import PromptMessage, TextContent


@mcp_server.resource("echo://static", mime_type="application/json")
async def echo_resource() -> str:
    """Static echo resource."""
    log_write_to_file("Echo resource accessed")

    response = ApiResponse(success=True, data={"message": "Echo!"})

    return response.to_json()


@mcp_server.resource("greeting://{name}", mime_type="application/json")
async def get_greeting(name: str) -> str:
    """Get a greeting for the given name.

    Args:
        name: The name to greet
    """
    log_write_to_file(f"Greeting requested for: {name}")

    response = ApiResponse(success=True, data={"greeting": f"Hello, {name}!"})

    return response.to_json()


@mcp_server.prompt()
def summarize_github_repos(tool_output: str) -> PromptMessage:
    """Summarizes GitHub repositories for presentation."""

    return PromptMessage(
        role="user",
        content=TextContent(
            type="text",
            text=f"""Summarize the GitHub repositories of a user.

INPUT:
{tool_output}

RULES:
- Select at most 5 repositories
- Sort by star count (descending)
- For each repository include:
  - name
  - primary language
  - star count
  - one-line description
- Do not invent missing data
- If the list is empty, say: "No public repositories found."
""",
        ),
    )


@mcp_server.tool()
async def get_user_repos(username: str) -> dict:
    """Get public repositories for a GitHub user.

    Args:
        username: GitHub username to fetch repositories for

    Returns:
        JSON response containing list of repositories or error details
    """
    log_write_to_file(f"Fetching repositories for user: {username}")

    # Input validation
    if not username or not isinstance(username, str) or len(username.strip()) == 0:
        error_response = ApiResponse(success=False, error="Username cannot be empty", error_code="INVALID_INPUT")
        log_write_to_file(f"Invalid username provided: {username}")

        return error_response.to_dict()

    url = f"https://api.github.com/users/{username}/repos"

    try:
        headers = {
            "User-Agent": "github-explorer/1.0",
            "Accept": "application/vnd.github+json",
        }

        response = await asyncio.to_thread(get_request, url, timeout=GITHUB_API_TIMEOUT, headers=headers)

        if response.status_code == 404:
            error_response = ApiResponse(
                success=False, error=f"User '{username}' not found on GitHub", error_code="USER_NOT_FOUND"
            )
            log_write_to_file(f"User not found: {username}")

            return error_response.to_dict()

        if response.status_code != 200:
            error_response = ApiResponse(
                success=False, error=f"GitHub API error: {response.status_code}", error_code="API_ERROR"
            )
            log_write_to_file(f"GitHub API error for user {username}: {response.status_code} | {response.text}")

            return error_response.to_dict()

        data = response.json()
        if len(data) == 0:
            success_response = ApiResponse(success=True, data={"repositories": [], "count": 0})
            log_write_to_file(f"No repositories found for user: {username}")

            return success_response.to_dict()

        success_response = ApiResponse(
            success=True, data={"username": username, "repositories": data, "count": len(data)}
        )
        log_write_to_file(f"Successfully fetched {len(data)} repositories for user {username}")

        return success_response.to_dict()

    except Exception as e:
        error_response = ApiResponse(
            success=False, error="An unexpected error occurred while fetching repositories", error_code="INTERNAL_ERROR"
        )
        log_write_to_file(f"Unexpected error fetching repositories for user {username}: {e}")

        return error_response.to_dict()
