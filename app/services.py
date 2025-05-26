from lib.utils import log_write_to_file
from app.server import mcp_server
import requests


@mcp_server.resource("echo://static")
async def echo_resource():
    log_write_to_file("Echo resource accessed")

    return "Echo!"


@mcp_server.resource("greeting://{name}")
async def get_greeting(name):
    log_write_to_file(f"Greeting requested for: {name}")

    return f"Hello, {name}!"


@mcp_server.tool()
async def get_user_repos(username: str) -> str:
    """Get public repositories for a GitHub user.

    Args:
        username: GitHub username
    """
    log_write_to_file(f"Fetching repositories for user: {username}")

    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code != 200:
        log_write_to_file(f"Failed to fetch repositories for user: {username}, status code: {response.status_code}")

        return "Unable to fetch repositories or user does not exist."

    data = response.json()
    if not data:
        log_write_to_file(f"Failed to fetch repositories for user: {username}")

        return "Unable to fetch repositories or user does not exist."

    repos = [repo["name"] for repo in data]

    if not repos:
        log_write_to_file(f"No repositories found for user: {username}")

        return "No public repositories found for this user."

    output = "\n".join(repos)

    log_write_to_file(f"Repositories fetched for user {username}")

    return output
