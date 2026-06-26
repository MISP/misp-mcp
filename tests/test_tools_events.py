"""Tests for event, attribute, and object tools."""

import pytest


SAMPLE_EVENT = {
    "Event": {
        "id": "1",
        "info": "Test event",
        "threat_level_id": "2",
        "analysis": "1",
        "Attribute": [
            {
                "id": "10",
                "type": "ip-src",
                "value": "192.168.1.1",
            }
        ],
    }
}

SAMPLE_ATTRIBUTE = {
    "Attribute": {
        "id": "10",
        "type": "ip-src",
        "value": "192.168.1.1",
        "event_id": "1",
    }
}

SAMPLE_OBJECT = {
    "Object": {
        "id": "5",
        "name": "file",
        "Attribute": [
            {"type": "filename", "value": "malware.exe"},
            {"type": "md5", "value": "d41d8cd98f00b204"},
        ],
    }
}

SAMPLE_INDEX = [
    {
        "id": "1",
        "info": "Test event",
        "threat_level_id": "2",
    },
    {
        "id": "2",
        "info": "Another event",
        "threat_level_id": "1",
    },
]

SAMPLE_EVENT_REPORT = {
    "EventReport": {
        "id": "7",
        "event_id": "1",
        "name": "Analyst summary",
        "content": "Known-good report content",
    }
}

SAMPLE_ATTRIBUTE_TYPES = {
    "result": {
        "types": ["ip-src", "domain", "sha256"],
        "categories": ["Network activity"],
    }
}

SAMPLE_ATTRIBUTE_STATISTICS = {
    "ip-src": 12,
    "domain": 7,
}


class TestSearchEvents:
    @pytest.mark.asyncio
    async def test_basic_search(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search.return_value = [SAMPLE_EVENT]
        result = await mcp_server.call_tool(
            "search_events", {"value": "192.168.1.1"}
        )
        mock_pymisp.search.assert_called_once()
        call_kwargs = mock_pymisp.search.call_args[1]
        assert call_kwargs["controller"] == "events"
        assert call_kwargs["value"] == "192.168.1.1"

    @pytest.mark.asyncio
    async def test_search_with_filters(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search.return_value = []
        await mcp_server.call_tool(
            "search_events",
            {
                "type_attribute": "ip-src",
                "tags": ["tlp:white"],
                "date_from": "2024-01-01",
                "limit": 10,
            },
        )
        call_kwargs = mock_pymisp.search.call_args[1]
        assert call_kwargs["type_attribute"] == "ip-src"
        assert call_kwargs["tags"] == ["tlp:white"]
        assert call_kwargs["date_from"] == "2024-01-01"
        assert call_kwargs["limit"] == 10

    @pytest.mark.asyncio
    async def test_search_returns_dict_passthrough(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search.return_value = {
            "response": [SAMPLE_EVENT]
        }
        result = await mcp_server.call_tool(
            "search_events", {}
        )
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_default_pagination(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search.return_value = []
        await mcp_server.call_tool("search_events", {})
        call_kwargs = mock_pymisp.search.call_args[1]
        assert call_kwargs["limit"] == 25
        assert call_kwargs["page"] == 1


class TestSearchAttributes:
    @pytest.mark.asyncio
    async def test_basic_search(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search.return_value = [
            SAMPLE_ATTRIBUTE
        ]
        result = await mcp_server.call_tool(
            "search_attributes",
            {
                "value": "192.168.1.1",
                "type_attribute": "ip-src",
            },
        )
        call_kwargs = mock_pymisp.search.call_args[1]
        assert call_kwargs["controller"] == "attributes"
        assert call_kwargs["value"] == "192.168.1.1"
        assert call_kwargs["type_attribute"] == "ip-src"

    @pytest.mark.asyncio
    async def test_default_includes_event_uuid(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search.return_value = []
        await mcp_server.call_tool(
            "search_attributes", {}
        )
        call_kwargs = mock_pymisp.search.call_args[1]
        assert call_kwargs["include_event_uuid"] is True

    @pytest.mark.asyncio
    async def test_default_limit(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search.return_value = []
        await mcp_server.call_tool(
            "search_attributes", {}
        )
        call_kwargs = mock_pymisp.search.call_args[1]
        assert call_kwargs["limit"] == 50


class TestSearchObjects:
    @pytest.mark.asyncio
    async def test_search_by_object_name(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search.return_value = [SAMPLE_OBJECT]
        await mcp_server.call_tool(
            "search_objects", {"object_name": "file"}
        )
        call_kwargs = mock_pymisp.search.call_args[1]
        assert call_kwargs["controller"] == "objects"
        assert call_kwargs["object_name"] == "file"


class TestSearchEventIndex:
    @pytest.mark.asyncio
    async def test_basic_index_search(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search_index.return_value = (
            SAMPLE_INDEX
        )
        result = await mcp_server.call_tool(
            "search_event_index",
            {"eventinfo": "Test"},
        )
        mock_pymisp.search_index.assert_called_once()
        call_kwargs = (
            mock_pymisp.search_index.call_args[1]
        )
        assert call_kwargs["eventinfo"] == "Test"

    @pytest.mark.asyncio
    async def test_threat_level_filter(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search_index.return_value = []
        await mcp_server.call_tool(
            "search_event_index", {"threatlevel": 1}
        )
        call_kwargs = (
            mock_pymisp.search_index.call_args[1]
        )
        assert call_kwargs["threatlevel"] == 1


class TestGetEvent:
    @pytest.mark.asyncio
    async def test_get_by_id(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.get_event.return_value = SAMPLE_EVENT
        result = await mcp_server.call_tool(
            "get_event", {"event_id": 1}
        )
        mock_pymisp.get_event.assert_called_once_with(
            1, pythonify=False
        )

    @pytest.mark.asyncio
    async def test_get_with_correlations_uses_search(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search.return_value = [SAMPLE_EVENT]
        await mcp_server.call_tool(
            "get_event",
            {
                "event_id": 1,
                "include_correlations": True,
            },
        )
        mock_pymisp.search.assert_called_once()
        mock_pymisp.get_event.assert_not_called()


class TestGetAttribute:
    @pytest.mark.asyncio
    async def test_get_by_id(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.get_attribute.return_value = (
            SAMPLE_ATTRIBUTE
        )
        await mcp_server.call_tool(
            "get_attribute", {"attribute_id": 10}
        )
        mock_pymisp.get_attribute.assert_called_once_with(
            10, pythonify=False
        )


class TestGetObject:
    @pytest.mark.asyncio
    async def test_get_by_id(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.get_object.return_value = (
            SAMPLE_OBJECT
        )
        await mcp_server.call_tool(
            "get_object", {"object_id": 5}
        )
        mock_pymisp.get_object.assert_called_once_with(
            5, pythonify=False
        )


class TestEventReports:
    @pytest.mark.asyncio
    async def test_list_event_reports(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.get_event_reports.return_value = [
            SAMPLE_EVENT_REPORT
        ]
        await mcp_server.call_tool(
            "list_event_reports", {"event_id": 1}
        )
        mock_pymisp.get_event_reports.assert_called_once_with(
            1, pythonify=False
        )

    @pytest.mark.asyncio
    async def test_get_event_report(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.get_event_report.return_value = (
            SAMPLE_EVENT_REPORT
        )
        await mcp_server.call_tool(
            "get_event_report", {"event_report_id": 7}
        )
        mock_pymisp.get_event_report.assert_called_once_with(
            7, pythonify=False
        )


class TestAttributeMetadata:
    @pytest.mark.asyncio
    async def test_describe_attribute_types(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.direct_call.return_value = (
            SAMPLE_ATTRIBUTE_TYPES
        )
        await mcp_server.call_tool(
            "describe_attribute_types", {}
        )
        mock_pymisp.direct_call.assert_called_once_with(
            "attributes/describeTypes"
        )

    @pytest.mark.asyncio
    async def test_get_attribute_statistics(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.attributes_statistics.return_value = (
            SAMPLE_ATTRIBUTE_STATISTICS
        )
        await mcp_server.call_tool(
            "get_attribute_statistics",
            {"context": "category", "percentage": True},
        )
        mock_pymisp.attributes_statistics.assert_called_once_with(
            context="category",
            percentage=True,
        )

    @pytest.mark.asyncio
    async def test_attribute_exists(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.attribute_exists.return_value = True
        result = await mcp_server.call_tool(
            "attribute_exists", {"attribute_id": 10}
        )
        mock_pymisp.attribute_exists.assert_called_once_with(
            10
        )
        assert result[0][0].text == "true"
        assert result[1] == {"result": True}

    @pytest.mark.asyncio
    async def test_get_attribute_by_base64_value(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.direct_call.return_value = (
            SAMPLE_ATTRIBUTE
        )
        await mcp_server.call_tool(
            "get_attribute_by_base64_value",
            {"base64_value": "ZXhhbXBsZS5jb20="},
        )
        mock_pymisp.direct_call.assert_called_once_with(
            "attributes/getAttributeByB64Value/"
            "ZXhhbXBsZS5jb20%3D"
        )
