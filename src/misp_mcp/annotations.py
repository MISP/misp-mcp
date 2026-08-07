"""Shared MCP tool annotations.

Every tool in this server only reads from MISP; none of them create,
modify, or delete data (see server.py's `instructions` and the README).
"""

from mcp.types import ToolAnnotations

READ_ONLY = ToolAnnotations(readOnlyHint=True)
