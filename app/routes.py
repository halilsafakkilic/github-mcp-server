from starlette.responses import PlainTextResponse
from starlette.requests import Request
from app.server import mcp_server


@mcp_server.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")
