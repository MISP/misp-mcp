"""Turn MISP connectivity and API errors into clear tool errors.

Without this, a request against an unreachable MISP instance or one
rejecting the API key surfaces as a raw requests/PyMISP exception,
which reads as connection-pool internals rather than something an
operator can act on.
"""

from functools import wraps

import requests
from mcp.server.fastmcp.exceptions import ToolError
from pymisp.exceptions import PyMISPError


def handle_misp_errors(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            raise ToolError(f"Could not reach MISP: {e}") from e
        except PyMISPError as e:
            raise ToolError(f"MISP request failed: {e}") from e

    return wrapper
