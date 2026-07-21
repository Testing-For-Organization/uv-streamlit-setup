"""HTTP helpers used by the app — depends on requests.

Uses ``HTTPResponse`` from ``urllib3.response`` (re-exported from
``requests.adapters`` in requests 2.28, removed in 2.32+).
"""

from __future__ import annotations

from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.response import HTTPResponse


def build_session() -> requests.Session:
    session = requests.Session()
    session.mount("https://", HTTPAdapter())
    session.mount("http://", HTTPAdapter())
    return session


def prepare_example_request() -> requests.PreparedRequest:
    return build_session().prepare_request(
        requests.Request("GET", "https://example.com", headers={"Accept": "text/html"})
    )


def response_type_name() -> str:
    """Return the name of the HTTPResponse class (from urllib3.response)."""
    return HTTPResponse.__name__


def session_meta() -> dict[str, Any]:
    return {
        "requests_version": requests.__version__,
        "response_type": response_type_name(),
        "has_session": isinstance(build_session(), requests.Session),
    }
