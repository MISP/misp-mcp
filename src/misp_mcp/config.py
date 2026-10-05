"""Configuration for MISP MCP server."""

import logging
import os


def get_misp_url() -> str:
    url = os.environ.get("MISP_URL", "")
    if not url:
        raise ValueError(
            "MISP_URL environment variable is required"
        )
    return url.rstrip("/")


def get_misp_api_key() -> str:
    key = os.environ.get("MISP_API_KEY", "")
    if not key:
        raise ValueError(
            "MISP_API_KEY environment variable is required"
        )
    return key


def get_misp_verifycert() -> bool:
    return os.environ.get(
        "MISP_VERIFYCERT", "true"
    ).lower() in ("true", "1", "yes")


def get_misp_timeout() -> int:
    """Get the HTTP request timeout in seconds (default 30)."""
    raw = os.environ.get("MISP_TIMEOUT", "30")
    try:
        return int(raw)
    except ValueError:
        return 30


def get_misp_retries() -> int:
    """Get the number of retries for transient failures (default 3)."""
    raw = os.environ.get("MISP_RETRIES", "3")
    try:
        return int(raw)
    except ValueError:
        return 3


def get_misp_retry_delay() -> float:
    """Get the base delay between retries in seconds (default 1.0)."""
    raw = os.environ.get("MISP_RETRY_DELAY", "1.0")
    try:
        return float(raw)
    except ValueError:
        return 1.0


def get_misp_log_level() -> int:
    """Get the logging level (default WARNING)."""
    raw = os.environ.get("MISP_LOG_LEVEL", "WARNING").upper()
    return getattr(logging, raw, logging.WARNING)
