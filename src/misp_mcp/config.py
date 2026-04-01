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
