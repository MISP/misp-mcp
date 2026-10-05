"""Tests for server setup and tool registration."""

import pytest
from unittest.mock import patch, MagicMock


EXPECTED_TOOLS = [
    "search_events",
    "search_attributes",
    "search_objects",
    "search_event_index",
    "get_event",
    "get_attribute",
    "get_object",
    "search_tags",
    "list_taxonomies",
    "get_taxonomy",
    "search_galaxies",
    "get_galaxy",
    "search_galaxy_clusters",
    "search_feeds",
]


class TestServerSetup:
    def test_all_tools_registered(self, mcp_server):
        tools = list(
            mcp_server._tool_manager._tools.keys()
        )
        for tool_name in EXPECTED_TOOLS:
            assert tool_name in tools, (
                f"Tool {tool_name} not registered"
            )

    def test_no_unexpected_tools(self, mcp_server):
        tools = list(
            mcp_server._tool_manager._tools.keys()
        )
        for tool_name in tools:
            assert tool_name in EXPECTED_TOOLS, (
                f"Unexpected tool {tool_name} registered"
            )

    def test_tool_count(self, mcp_server):
        tools = list(
            mcp_server._tool_manager._tools.keys()
        )
        assert len(tools) == len(EXPECTED_TOOLS)


class TestClientInitialisation:
    @patch("misp_mcp.server.PyMISP")
    @patch("misp_mcp.server.get_misp_timeout")
    @patch("misp_mcp.server.get_misp_verifycert")
    @patch("misp_mcp.server.get_misp_api_key")
    @patch("misp_mcp.server.get_misp_url")
    def test_lazy_client_creation(
        self,
        mock_url,
        mock_key,
        mock_verify,
        mock_timeout,
        mock_pymisp_cls,
    ):
        import misp_mcp.server as srv

        srv._client = None
        mock_url.return_value = "https://misp.test"
        mock_key.return_value = "test-key"
        mock_verify.return_value = False
        mock_timeout.return_value = 30

        client = srv.get_client()

        mock_pymisp_cls.assert_called_once_with(
            url="https://misp.test",
            key="test-key",
            ssl=False,
            timeout=30,
        )
        assert client == mock_pymisp_cls.return_value
        srv._client = None

    @patch("misp_mcp.server.PyMISP")
    @patch("misp_mcp.server.get_misp_verifycert")
    @patch("misp_mcp.server.get_misp_api_key")
    @patch("misp_mcp.server.get_misp_url")
    def test_client_reuse(
        self,
        mock_url,
        mock_key,
        mock_verify,
        mock_pymisp_cls,
    ):
        import misp_mcp.server as srv

        srv._client = None
        mock_url.return_value = "https://misp.test"
        mock_key.return_value = "test-key"
        mock_verify.return_value = True

        client1 = srv.get_client()
        client2 = srv.get_client()

        assert client1 is client2
        assert mock_pymisp_cls.call_count == 1
        srv._client = None
