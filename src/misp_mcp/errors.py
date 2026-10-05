"""Error handling and retry helpers for MISP MCP tools."""

import functools
import logging
import time

import requests
from pymisp.exceptions import PyMISPError

from misp_mcp.config import get_misp_retries, get_misp_retry_delay

logger = logging.getLogger(__name__)

# Exceptions considered transient: worth retrying with backoff.
RETRYABLE_EXCEPTIONS = (
    requests.exceptions.ConnectionError,
    requests.exceptions.Timeout,
    requests.exceptions.HTTPError,
    PyMISPError,
)


def handle_misp_errors(max_retries=None, base_delay=None, backoff=2.0):
    """Decorate an MCP tool to retry transient failures and return a
    structured error instead of raising.

    Transient failures (network errors, timeouts, 5xx server errors) are
    retried with exponential backoff. Once the retries are exhausted, a
    structured error dict is returned so the calling agent receives a useful
    message rather than an uncaught exception propagating through the MCP
    protocol.

    Args:
        max_retries: Maximum number of retries. Defaults to ``MISP_RETRIES``.
        base_delay: Initial delay between retries in seconds. Defaults to
            ``MISP_RETRY_DELAY``.
        backoff: Exponential backoff multiplier applied per attempt.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = (
                max_retries
                if max_retries is not None
                else get_misp_retries()
            )
            delay = (
                base_delay
                if base_delay is not None
                else get_misp_retry_delay()
            )

            last_exc = None
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except RETRYABLE_EXCEPTIONS as exc:
                    last_exc = exc
                    if attempt >= retries:
                        break
                    wait = delay * (backoff ** attempt)
                    logger.warning(
                        "%s failed (attempt %d/%d): %s - "
                        "retrying in %.2fs",
                        func.__name__,
                        attempt + 1,
                        retries + 1,
                        exc,
                        wait,
                    )
                    time.sleep(wait)

            logger.error(
                "%s failed after %d attempt(s): %s",
                func.__name__,
                retries + 1,
                last_exc,
            )
            return {
                "error": str(last_exc),
                "tool": func.__name__,
                "retries_exhausted": True,
            }

        return wrapper

    return decorator
