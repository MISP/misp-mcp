"""Tests for configuration module."""

import logging
import os
import pytest
from unittest.mock import patch

from misp_mcp.config import (
    get_misp_url,
    get_misp_api_key,
    get_misp_verifycert,
    get_misp_timeout,
    get_misp_retries,
    get_misp_retry_delay,
    get_misp_log_level,
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


class TestGetMispTimeout:
    def test_returns_value_from_env(self):
        with patch.dict(os.environ, {"MISP_TIMEOUT": "60"}):
            assert get_misp_timeout() == 60

    def test_defaults_to_30(self):
        with patch.dict(os.environ, {}, clear=True):
            assert get_misp_timeout() == 30

    def test_invalid_value_falls_back_to_default(self):
        with patch.dict(os.environ, {"MISP_TIMEOUT": "abc"}):
            assert get_misp_timeout() == 30


class TestGetMispRetries:
    def test_returns_value_from_env(self):
        with patch.dict(os.environ, {"MISP_RETRIES": "5"}):
            assert get_misp_retries() == 5

    def test_defaults_to_3(self):
        with patch.dict(os.environ, {}, clear=True):
            assert get_misp_retries() == 3

    def test_invalid_value_falls_back_to_default(self):
        with patch.dict(os.environ, {"MISP_RETRIES": "xyz"}):
            assert get_misp_retries() == 3


class TestGetMispRetryDelay:
    def test_returns_value_from_env(self):
        with patch.dict(os.environ, {"MISP_RETRY_DELAY": "0.5"}):
            assert get_misp_retry_delay() == 0.5

    def test_defaults_to_1(self):
        with patch.dict(os.environ, {}, clear=True):
            assert get_misp_retry_delay() == 1.0

    def test_invalid_value_falls_back_to_default(self):
        with patch.dict(os.environ, {"MISP_RETRY_DELAY": "oops"}):
            assert get_misp_retry_delay() == 1.0


class TestGetMispLogLevel:
    def test_returns_value_from_env(self):
        with patch.dict(os.environ, {"MISP_LOG_LEVEL": "DEBUG"}):
            assert get_misp_log_level() == logging.DEBUG

    def test_defaults_to_warning(self):
        with patch.dict(os.environ, {}, clear=True):
            assert get_misp_log_level() == logging.WARNING

    def test_invalid_value_falls_back_to_warning(self):
        with patch.dict(os.environ, {"MISP_LOG_LEVEL": "NOPE"}):
            assert get_misp_log_level() == logging.WARNING
