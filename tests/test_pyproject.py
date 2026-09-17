"""Tests for the packaging metadata in pyproject.toml."""

import re
from pathlib import Path

from packaging.requirements import Requirement

PYPROJECT = (
    Path(__file__).resolve().parent.parent
    / "pyproject.toml"
)


def _mcp_requirement():
    """Return the declared mcp dependency."""
    text = PYPROJECT.read_text(encoding="utf-8")
    match = re.search(r'"(mcp\[[^"]*\][^"]*)"', text)
    assert match, "mcp dependency not found"
    return Requirement(match.group(1))


class TestMcpDependency:
    def test_allows_v1(self):
        specifier = _mcp_requirement().specifier
        assert specifier.contains("1.29.1")

    def test_excludes_v2(self):
        # mcp 2.x dropped mcp.server.fastmcp, which both
        # the server and the test fixtures import from.
        specifier = _mcp_requirement().specifier
        assert not specifier.contains("2.0.0")
