"""Integration checks for Felix upgrade-PR CI monitoring on this Python repo.

These tests exercise runtime dependencies Felix may upgrade. If an upgrade
breaks imports or basic APIs, CI fails and Dash can spawn remediate_pr_checks.
"""

from __future__ import annotations

import requests
import streamlit as st
import urllib3


def test_streamlit_runtime_api() -> None:
    """streamlit must remain importable after dependency upgrades."""
    assert hasattr(st, "header")
    assert hasattr(st, "write")
    assert hasattr(st, "number_input")
    assert isinstance(st.__version__, str)
    assert st.__version__


def test_requests_runtime_api() -> None:
    """Pinned requests must stay compatible with Session usage."""
    session = requests.Session()
    assert session.headers is not None
    prepared = requests.Request("GET", "https://example.com").prepare()
    assert prepared.method == "GET"
    assert prepared.url == "https://example.com/"


def test_urllib3_runtime_api() -> None:
    """Pinned urllib3 (direct + requests transitive) must remain usable."""
    assert urllib3.__version__
    pool = urllib3.PoolManager()
    assert pool is not None


def test_dependency_versions_are_reported() -> None:
    """Helpful failure output when remediation inspects CI logs."""
    versions = {
        "streamlit": getattr(st, "__version__", "unknown"),
        "requests": getattr(requests, "__version__", "unknown"),
        "urllib3": getattr(urllib3, "__version__", "unknown"),
    }
    for name, version in versions.items():
        assert version, f"{name} version missing"
    print(versions)
