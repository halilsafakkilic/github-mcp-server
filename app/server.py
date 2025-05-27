from lib.custom_fastmcp import CustomFastMCP

mcp_server = CustomFastMCP("github-explorer", debug=True, log_level="DEBUG")

import app.services  # noqa
import app.routes  # noqa
