"""Shared fixtures for misp-mcp tests."""

import pytest
from unittest.mock import MagicMock, patch

from mcp.server.fastmcp import FastMCP


@pytest.fixture
def mock_pymisp():
    """Create a mock PyMISP client."""
    client = MagicMock()
    client.search.return_value = []
    client.search_index.return_value = []
    client.get_event.return_value = {}
    client.get_attribute.return_value = {}
    client.get_object.return_value = {}
    client.get_event_report.return_value = {}
    client.get_event_reports.return_value = []
    client.attributes_statistics.return_value = {}
    client.attribute_exists.return_value = False
    client.direct_call.return_value = {}
    client.search_tags.return_value = {}
    client.tags.return_value = []
    client.get_tag.return_value = {}
    client.taxonomies.return_value = []
    client.get_taxonomy.return_value = {}
    client.search_galaxy.return_value = {}
    client.get_galaxy.return_value = {}
    client.search_galaxy_clusters.return_value = {}
    client.get_galaxy_cluster.return_value = {}
    client.feeds.return_value = []
    client.search_feeds.return_value = []
    return client


@pytest.fixture
def mcp_server(mock_pymisp):
    """Create a fresh MCP server with mocked PyMISP."""
    from misp_mcp.tools import events, tags, galaxies, feeds

    server = FastMCP("MISP-Test")
    get_client = lambda: mock_pymisp
    events.register(server, get_client)
    tags.register(server, get_client)
    galaxies.register(server, get_client)
    feeds.register(server, get_client)
    return server
