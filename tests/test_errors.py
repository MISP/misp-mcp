"""Tests for error handling and retry decorator."""

import os
import pytest
import requests
from unittest.mock import patch
from pymisp.exceptions import PyMISPError

from misp_mcp.errors import handle_misp_errors


class TestHandleMispErrors:
    def test_returns_result_on_success(self):
        calls = []

        @handle_misp_errors(max_retries=3, base_delay=0)
        def ok():
            calls.append(1)
            return {"data": "ok"}

        assert ok() == {"data": "ok"}
        assert calls == [1]

    def test_retries_and_succeeds(self):
        calls = []

        @handle_misp_errors(max_retries=3, base_delay=0)
        def flaky():
            calls.append(1)
            if len(calls) < 3:
                raise requests.exceptions.ConnectionError("boom")
            return {"data": "recovered"}

        assert flaky() == {"data": "recovered"}
        assert len(calls) == 3

    def test_returns_error_dict_when_exhausted(self):
        @handle_misp_errors(max_retries=2, base_delay=0)
        def always_fails():
            raise PyMISPError("server exploded")

        result = always_fails()
        assert result["retries_exhausted"] is True
        assert "server exploded" in result["error"]
        assert result["tool"] == "always_fails"

    def test_retries_timeout_errors(self):
        calls = []

        @handle_misp_errors(max_retries=1, base_delay=0)
        def times_out():
            calls.append(1)
            raise requests.exceptions.Timeout("timed out")

        result = times_out()
        assert result["retries_exhausted"] is True
        assert len(calls) == 2  # 1 initial attempt + 1 retry

    def test_non_retryable_exception_propagates(self):
        @handle_misp_errors(max_retries=3, base_delay=0)
        def config_error():
            raise ValueError("MISP_URL missing")

        with pytest.raises(ValueError, match="MISP_URL missing"):
            config_error()

    def test_preserves_function_signature(self):
        import inspect

        @handle_misp_errors()
        def sample(value: str, limit: int = 25) -> dict:
            return {"value": value, "limit": limit}

        params = inspect.signature(sample).parameters
        assert list(params.keys()) == ["value", "limit"]
        assert params["limit"].default == 25


class TestToolErrorIntegration:
    @pytest.mark.asyncio
    async def test_search_events_returns_error_dict(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search.side_effect = PyMISPError(
            "connection refused"
        )
        with patch.dict(
            os.environ, {"MISP_RETRIES": "0", "MISP_RETRY_DELAY": "0"}
        ):
            result = await mcp_server.call_tool(
                "search_events", {"value": "1.2.3.4"}
            )

        # Structured tools return (unstructured, structured).
        structured = result[1] if isinstance(result, tuple) else result
        assert "connection refused" in str(structured)

    @pytest.mark.asyncio
    async def test_search_events_passes_through_on_success(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search.return_value = [{"Event": {"id": "1"}}]
        with patch.dict(
            os.environ, {"MISP_RETRIES": "0", "MISP_RETRY_DELAY": "0"}
        ):
            result = await mcp_server.call_tool(
                "search_events", {"value": "1.2.3.4"}
            )

        assert result is not None
        assert mock_pymisp.search.call_count == 1

