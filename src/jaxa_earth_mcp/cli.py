"""CLI entry point for jaxa-earth-mcp."""

import argparse

from jaxa_earth_mcp.server import mcp


def main():
    parser = argparse.ArgumentParser(description="JAXA Earth MCP Server CLI")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio", help="MCP transport protocol (default: stdio)")  # noqa
    parser.add_argument("--host", default="127.0.0.1", help="Host for SSE transport")  # noqa
    parser.add_argument("--port", type=int, default=8000, help="Port for SSE transport")  # noqa

    args, unknown = parser.parse_known_args()

    if args.transport == "sse":
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
