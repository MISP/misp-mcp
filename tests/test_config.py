"""Tests for configuration module."""

import os
import pytest
from unittest.mock import patch

from misp_mcp.config import (
    get_misp_url,
    get_misp_api_key,
    get_misp_verifycert,
)


class TestGetMispUrl:
    def test_returns_url_from_env(self):
        with patch.dict(
            os.environ, {"MISP_URL": "https://misp.test"}
        ):
            assert get_misp_url() == "https://misp.test"

    def test_strips_trailing_slash(self):
        with patch.dict(
            os.environ, {"MISP_URL": "https://misp.test/"}
        ):
            assert get_misp_url() == "https://misp.test"

    def test_raises_when_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="MISP_URL"):
                get_misp_url()

    def test_raises_when_empty(self):
        with patch.dict(os.environ, {"MISP_URL": ""}):
            with pytest.raises(ValueError, match="MISP_URL"):
                get_misp_url()


class TestGetMispApiKey:
    def test_returns_key_from_env(self):
        with patch.dict(
            os.environ, {"MISP_API_KEY": "abc123"}
        ):
            assert get_misp_api_key() == "abc123"

    def test_raises_when_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(
                ValueError, match="MISP_API_KEY"
            ):
                get_misp_api_key()


class TestGetMispVerifycert:
    @pytest.mark.parametrize(
        "value,expected",
        [
            ("true", True),
            ("True", True),
            ("1", True),
            ("yes", True),
            ("false", False),
            ("0", False),
            ("no", False),
        ],
    )
    def test_parses_values(self, value, expected):
        with patch.dict(
            os.environ, {"MISP_VERIFYCERT": value}
        ):
            assert get_misp_verifycert() is expected

    def test_defaults_to_true(self):
        with patch.dict(os.environ, {}, clear=True):
            assert get_misp_verifycert() is True

    def test_returns_path_for_ca_bundle(self):
        with patch.dict(
            os.environ,
            {"MISP_VERIFYCERT": "/etc/ssl/certs/internal-ca.pem"},
        ):
            assert (
                get_misp_verifycert()
                == "/etc/ssl/certs/internal-ca.pem"
            )
