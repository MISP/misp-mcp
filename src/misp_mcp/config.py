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


def get_misp_verifycert() -> bool | str:
    value = os.environ.get("MISP_VERIFYCERT", "true")
    lowered = value.lower()
    if lowered in ("true", "1", "yes"):
        return True
    if lowered in ("false", "0", "no"):
        return False
    # Not a recognised boolean: treat it as a path to a CA bundle and
    # hand it straight to PyMISP, which accepts bool | str for `ssl`.
    return value
