"""MISP MCP Server - read-only threat intelligence access."""

from mcp.server.fastmcp import FastMCP
from pymisp import PyMISP

from misp_mcp.config import (
    get_misp_api_key,
    get_misp_timeout,
    get_misp_url,
    get_misp_verifycert,
)
from misp_mcp.tools import events, feeds, galaxies, tags

mcp = FastMCP(
    "MISP",
    instructions=(
        "MISP is a threat intelligence sharing platform. "
        "Use these tools to search and retrieve threat "
        "intelligence data including events, attributes "
        "(indicators of compromise), objects, tags, "
        "taxonomies, galaxies (threat actors, malware, "
        "ATT&CK techniques), and feeds. "
        "All access is read-only."
    ),
)

_client: PyMISP | None = None


def get_client() -> PyMISP:
    """Get or create the PyMISP client."""
    global _client
    if _client is None:
        _client = PyMISP(
            url=get_misp_url(),
            key=get_misp_api_key(),
            ssl=get_misp_verifycert(),
            timeout=get_misp_timeout(),
        )
    return _client


events.register(mcp, get_client)
tags.register(mcp, get_client)
galaxies.register(mcp, get_client)
feeds.register(mcp, get_client)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
