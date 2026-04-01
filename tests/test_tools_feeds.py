"""Tests for feed tools."""

import pytest


SAMPLE_FEEDS = [
    {
        "Feed": {
            "id": "1",
            "name": "CIRCL OSINT",
            "url": "https://www.circl.lu/doc/misp/feed",
        }
    },
    {
        "Feed": {
            "id": "2",
            "name": "Botvrij",
            "url": "https://www.botvrij.eu/data/feed",
        }
    },
]


class TestSearchFeeds:
    @pytest.mark.asyncio
    async def test_search_with_value(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search_feeds.return_value = [
            SAMPLE_FEEDS[0]
        ]
        await mcp_server.call_tool(
            "search_feeds", {"value": "CIRCL"}
        )
        mock_pymisp.search_feeds.assert_called_once_with(
            value="CIRCL", pythonify=False
        )
        mock_pymisp.feeds.assert_not_called()

    @pytest.mark.asyncio
    async def test_list_all_when_no_value(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.feeds.return_value = SAMPLE_FEEDS
        await mcp_server.call_tool("search_feeds", {})
        mock_pymisp.feeds.assert_called_once_with(
            pythonify=False
        )
        mock_pymisp.search_feeds.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_single_result(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.feeds.return_value = SAMPLE_FEEDS[0]
        result = await mcp_server.call_tool(
            "search_feeds", {}
        )
        assert len(result) > 0
