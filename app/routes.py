from starlette.responses import PlainTextResponse
from starlette.requests import Request
from starlette.routing import Route


async def health(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")


starlette_routes = [
    Route("/health", methods=["GET"], endpoint=health),
]
