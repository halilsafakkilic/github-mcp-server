from lib.custom_fastmcp import CustomFastMCP

mcp_server = CustomFastMCP("github-explorer")

import app.services  # noqa
import app.routes  # noqa
