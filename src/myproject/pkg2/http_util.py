"""HTTP helpers used by the app — depends on requests + urllib3."""

from __future__ import annotations

from typing import Any

import requests
import urllib3


def build_session() -> requests.Session:
    """Create a Session with explicit urllib3 retry/adapter wiring."""
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        max_retries=urllib3.Retry(total=2, connect=2, read=2, backoff_factor=0.1)
    )
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def prepare_example_request() -> requests.PreparedRequest:
    """Prepare a GET the same way upgrade-sensitive client code typically does."""
    return build_session().prepare_request(
        requests.Request("GET", "https://example.com", headers={"Accept": "text/html"})
    )


def pool_request_meta() -> dict[str, Any]:
    """Exercise urllib3 PoolManager surface area Felix may touch during upgrades."""
    http = urllib3.PoolManager()
    return {
        "urllib3_version": urllib3.__version__,
        "pool_type": type(http).__name__,
        "has_request": callable(getattr(http, "request", None)),
    }
