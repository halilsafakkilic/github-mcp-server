from starlette.responses import PlainTextResponse
from app.server import mcp_server


@mcp_server.custom_route("/health", methods=["GET"])
async def health_check() -> PlainTextResponse:
    return PlainTextResponse("OK")
