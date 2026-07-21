def add(a: float, b: float) -> float:
    return a + b

def diff(a: float, b: float) -> float:
    return a - b


# Felix remediation QA marker.
# On felix/upgrade/* PRs, CI fails until remediation sets this to "ok".
# Normal PRs / main do not require it.
FELIX_REMEDIATION_MARKER = "ok"
