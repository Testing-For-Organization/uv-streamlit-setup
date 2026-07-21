"""Genuine integration checks for Felix upgrade-PR CI / remediation.

App code uses urllib3 1.26's Retry(method_whitelist=...). That kwarg is removed
in urllib3 2.x. When Felix upgrades urllib3, these tests fail for real and
remediation must update http_util to allowed_methods (or equivalent).
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


def test_urllib3_retry_method_whitelist_api() -> None:
    """Fails for real after urllib3 2.x upgrade until http_util is remediated."""
    retry = http_util.build_retry()
    assert retry.total == 2
    # 1.26 exposes method_whitelist; 2.x removed it (use allowed_methods).
    assert hasattr(retry, "method_whitelist") or hasattr(retry, "allowed_methods")


def test_urllib3_pool_manager_with_retries() -> None:
    meta = http_util.pool_request_meta()
    assert meta["urllib3_version"] == urllib3.__version__
    assert meta["pool_type"] == "PoolManager"
    assert meta["has_request"] is True
    assert meta["retry_total"] == 2


def test_requests_urllib3_versions_are_compatible() -> None:
    assert requests.__version__
    assert urllib3.__version__
    assert http_util.build_session().headers is not None
