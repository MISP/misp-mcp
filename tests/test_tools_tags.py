"""Tests for tag and taxonomy tools."""

import pytest


SAMPLE_TAGS = {
    "Tag": [
        {"id": "1", "name": "tlp:white"},
        {"id": "2", "name": "tlp:green"},
    ]
}

SAMPLE_TAG_LIST = [
    {"id": "1", "name": "tlp:white"},
    {"id": "2", "name": "tlp:green"},
]

SAMPLE_TAG = {"Tag": {"id": "1", "name": "tlp:white"}}

SAMPLE_TAXONOMIES = [
    {"Taxonomy": {"id": "1", "namespace": "tlp"}},
    {
        "Taxonomy": {
            "id": "2",
            "namespace": "admiralty-scale",
        }
    },
]

SAMPLE_TAXONOMY = {
    "Taxonomy": {
        "id": "1",
        "namespace": "tlp",
        "description": "Traffic Light Protocol",
        "entries": [
            {"tag": "tlp:white", "expanded": "White"},
            {"tag": "tlp:green", "expanded": "Green"},
        ],
    }
}


class TestSearchTags:
    @pytest.mark.asyncio
    async def test_search_by_name(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search_tags.return_value = SAMPLE_TAGS
        await mcp_server.call_tool(
            "search_tags", {"tagname": "tlp"}
        )
        mock_pymisp.search_tags.assert_called_once_with(
            tagname="tlp",
            strict_tagname=False,
            pythonify=False,
        )

    @pytest.mark.asyncio
    async def test_strict_search(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search_tags.return_value = SAMPLE_TAGS
        await mcp_server.call_tool(
            "search_tags",
            {"tagname": "tlp:white", "strict": True},
        )
        call_kwargs = (
            mock_pymisp.search_tags.call_args[1]
        )
        assert call_kwargs["strict_tagname"] is True


class TestListTags:
    @pytest.mark.asyncio
    async def test_returns_list(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.tags.return_value = SAMPLE_TAG_LIST
        await mcp_server.call_tool("list_tags", {})
        mock_pymisp.tags.assert_called_once_with(
            pythonify=False,
            limit=100,
            page=1,
        )

    @pytest.mark.asyncio
    async def test_uses_pagination(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.tags.return_value = SAMPLE_TAG_LIST
        await mcp_server.call_tool(
            "list_tags", {"limit": 10, "page": 2}
        )
        mock_pymisp.tags.assert_called_once_with(
            pythonify=False,
            limit=10,
            page=2,
        )


class TestGetTag:
    @pytest.mark.asyncio
    async def test_get_by_id(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.get_tag.return_value = SAMPLE_TAG
        await mcp_server.call_tool(
            "get_tag", {"tag_id": 1}
        )
        mock_pymisp.get_tag.assert_called_once_with(
            1, pythonify=False
        )


class TestListTaxonomies:
    @pytest.mark.asyncio
    async def test_returns_list(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.taxonomies.return_value = (
            SAMPLE_TAXONOMIES
        )
        result = await mcp_server.call_tool(
            "list_taxonomies", {}
        )
        mock_pymisp.taxonomies.assert_called_once_with(
            pythonify=False
        )

    @pytest.mark.asyncio
    async def test_wraps_single_result(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.taxonomies.return_value = (
            SAMPLE_TAXONOMIES[0]
        )
        result = await mcp_server.call_tool(
            "list_taxonomies", {}
        )
        assert len(result) > 0


class TestGetTaxonomy:
    @pytest.mark.asyncio
    async def test_get_by_id(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.get_taxonomy.return_value = (
            SAMPLE_TAXONOMY
        )
        await mcp_server.call_tool(
            "get_taxonomy", {"taxonomy_id": 1}
        )
        mock_pymisp.get_taxonomy.assert_called_once_with(
            1, pythonify=False
        )
