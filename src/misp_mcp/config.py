"""Configuration for MISP MCP server."""

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
    timeout = os.environ.get("MISP_TIMEOUT", "30")
    try:
        parsed_timeout = int(timeout)
    except ValueError as exc:
        raise ValueError(
            "MISP_TIMEOUT must be a positive integer"
        ) from exc
    if parsed_timeout <= 0:
        raise ValueError(
            "MISP_TIMEOUT must be a positive integer"
        )
    return parsed_timeout
