"""Helpers for interpreting benchmark output."""
from __future__ import annotations


def percent_change(a: float, b: float) -> float:
    """Return percent change from A to B; positive means B is larger/slower."""
    if a == 0:
        raise ValueError("baseline value must be non-zero")
    return ((b - a) / a) * 100.0


def standard_error(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    import statistics
    return statistics.stdev(values) / (len(values) ** 0.5)
