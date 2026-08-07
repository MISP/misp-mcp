"""Tests for the MISP error-handling decorator."""

import pytest
import requests
from mcp.server.fastmcp.exceptions import ToolError
from pymisp.exceptions import PyMISPError

from misp_mcp.errors import handle_misp_errors


class TestHandleMispErrors:
    def test_returns_value_on_success(self):
        @handle_misp_errors
        def ok():
            return {"result": "data"}

        assert ok() == {"result": "data"}

    def test_wraps_request_exception(self):
        @handle_misp_errors
        def unreachable():
            raise requests.exceptions.ConnectionError("refused")

        with pytest.raises(ToolError, match="Could not reach MISP"):
            unreachable()

    def test_wraps_pymisp_error(self):
        @handle_misp_errors
        def bad_response():
            raise PyMISPError("unexpected response")

        with pytest.raises(ToolError, match="MISP request failed"):
            bad_response()

    def test_passes_through_arguments(self):
        @handle_misp_errors
        def add(a, b):
            return a + b

        assert add(1, b=2) == 3
