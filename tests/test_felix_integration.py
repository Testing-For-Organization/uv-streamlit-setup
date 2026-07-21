"""Integration tests — fail for real when requests is upgraded past 2.28.

Dash issue lists: requests 2.28.0 → 2.33.0.
App now imports HTTPResponse from urllib3.response (removed from requests.adapters).
"""

from __future__ import annotations

import requests
import streamlit as st

from myproject.pkg1 import simple_fn
from myproject.pkg2 import complex_fn, http_util


def test_streamlit_runtime_api() -> None:
    assert hasattr(st, "header")
    assert hasattr(st, "write")
    assert hasattr(st, "number_input")
    assert st.__version__


def test_app_math_still_works_with_streamlit_entry_contract() -> None:
    assert complex_fn.square_of_diff(5, 2) == 9
    assert complex_fn.square_of_sum(2, 3) == 25
    assert simple_fn.add(1, 2) == 3


def test_requests_session_and_prepare() -> None:
    prepared = http_util.prepare_example_request()
    assert prepared.method == "GET"
    assert prepared.url == "https://example.com/"
    assert isinstance(http_util.build_session(), requests.Session)


def test_requests_adapters_httpresponse_export() -> None:
    """Genuine break on requests 2.32+ (ImportError / failed import of http_util)."""
    meta = http_util.session_meta()
    assert meta["requests_version"] == requests.__version__
    assert meta["response_type"] == "HTTPResponse"
    assert meta["has_session"] is True
