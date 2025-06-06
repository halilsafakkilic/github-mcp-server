# GitHub Explorer MCP Server

This project is a server using the MCP (Model Context Protocol) standard to list GitHub user repositories. It can operate over different communication protocols (stdio, Streamable HTTP and SSE).

## Features

- GitHub user repository listing
- Support for stdio, Streamable HTTP and SSE (Server-Sent Events) protocols
- Customized FastMCP configuration
- Basic File logging system

## Installation

Requirements to run this project:

```bash
# Install dependencies using uv
uv sync
```

## Server Usage

You can start the server in two different modes:

### Stdio Mode

```bash
uv run server
```

### Streamable Http Mode

```bash
uv run server_shttp
```

### SSE (Server-Sent Events) Mode

```bash
uv run server_sse
```

## Example Query

You can query the server using MCP Inspector:

```
Can you give me the list of repos of user halilsafakkilic on GitHub?
```

## Inspector Usage

### Configuration Setup

Before using the Inspector or client examples, you need to create a proper configuration file:

1. Copy the configuration template file:
   ```bash
   cp mcp_configs.json.dist mcp_configs.json
   ```

2. Edit the `mcp_configs.json` file and update the path in the `server_stdio` section:
   ```json
   "server_stdio": {
     "command": "uv",
     "args": [
       "--directory",
       "/YOUR/ABSOLUTE/PROJECT/PATH",  # Replace with your actual project path
       "run",
       "server"
     ]
   }
   ```
   Replace `/YOUR/ABSOLUTE/PROJECT/PATH` with the absolute path to your project directory.


To test the server with MCP Inspector:

```shell
# Using stdio
npx -y @modelcontextprotocol/inspector uv run server

# Using stdio with config file
npx -y @modelcontextprotocol/inspector --config mcp_configs.json --server server_stdio

# Using Streamable HTTP
npx -y @modelcontextprotocol/inspector --config mcp_configs.json --server server_shttp

# Using SSE
npx -y @modelcontextprotocol/inspector --config mcp_configs.json --server server_sse
```

## SSE + Streamable HTTP Health Check
To check the health of the SSE or Streamable HTTP server, you can use the following command:

```bash
curl -X GET http://localhost:8080/health
```

## Client Usage

This project includes example clients for both stdio and SSE protocols.

### Stdio Client

The `client_stdio.py` demonstrates how to connect to the server using the **stdio** protocol:

```bash
uv run client_stdio.py
```

### Streamable HTTP Client

The `client_shttp.py` demonstrates how to connect to the server using **Streamable HTTP** protocol:

```bash
# Run the Streamable HTTP client (make sure server_shttp.py is running)
uv run client_shttp.py
```

### SSE Client

The `client_sse.py` demonstrates how to connect to the server using **SSE** protocol:

```bash
# Run the SSE client (make sure server_sse.py is running)
uv run client_sse.py
```


## Project Structure

- `server.py`: Main server for stdio protocol
- `server_sse.py`: Main server for SSE protocol
- `client_stdio.py`: Example client using stdio protocol
- `client_sse.py`: Example client using SSE protocol
- `app/`: Application logic and services
- `lib/`: Custom library files
- `logs/`: Logging directory
- `mcp_configs.json`: MCP configuration settings for Inspector and example usage

## API Tools

Currently, there is one API tool available:

### get_user_repos

A tool that lists the public repositories of a GitHub user.

Parameters:
- `username`: GitHub username

Example usage:
```
Action: get_user_repos
Parameter (username): halilsafakkilic
```

## License

This project is licensed under the MIT License.

