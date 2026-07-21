"""Integration checks for Felix upgrade-PR CI monitoring.

These tests exercise real app + dependency APIs (streamlit, requests, urllib3).
If an upgrade breaks imports or calling conventions, CI fails and Dash can
spawn remediate_pr_checks against real application/test failures.
"""

from __future__ import annotations

import requests
import streamlit as st
import urllib3

from myproject.pkg1 import simple_fn
from myproject.pkg2 import complex_fn, http_util


def test_streamlit_runtime_api() -> None:
    assert hasattr(st, "header")
    assert hasattr(st, "write")
    assert hasattr(st, "number_input")
    assert isinstance(st.__version__, str) and st.__version__


def test_app_math_still_works_with_streamlit_entry_contract() -> None:
    """hello.py uses complex_fn.square_of_diff with streamlit inputs — keep that path green."""
    assert complex_fn.square_of_diff(5, 2) == 9
    assert complex_fn.square_of_sum(2, 3) == 25
    assert simple_fn.add(1, 2) == 3


def test_requests_session_and_prepare() -> None:
    prepared = http_util.prepare_example_request()
    assert prepared.method == "GET"
    assert prepared.url == "https://example.com/"
    assert prepared.headers.get("Accept") == "text/html"

    session = http_util.build_session()
    assert isinstance(session, requests.Session)
    assert "https://" in session.adapters


def test_urllib3_pool_manager_api() -> None:
    meta = http_util.pool_request_meta()
    assert meta["urllib3_version"] == urllib3.__version__
    assert meta["pool_type"] == "PoolManager"
    assert meta["has_request"] is True

    # Retry helper must remain importable/constructible across urllib3 minors.
    retry = urllib3.Retry(total=1)
    assert retry.total == 1


def test_requests_urllib3_versions_are_compatible() -> None:
    """requests is built on urllib3 — both must import and report versions."""
    assert requests.__version__
    assert urllib3.__version__
    # Session uses urllib3 under the hood; constructing one catches wiring breaks.
    assert http_util.build_session().headers is not None
