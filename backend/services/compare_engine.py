"""Deterministic comparison helpers for provider-sourced player statistics."""
from services.statistics import derive_metrics


COUNTER_FIELDS = ("matches", "wins", "kills", "deaths", "headshots")


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value if value >= 0 else None


def compare_stats(stats_a: dict, stats_b: dict) -> dict:
    """Compare only counters actually supplied; never invent missing data."""
    a = stats_a if isinstance(stats_a, dict) else {}
    b = stats_b if isinstance(stats_b, dict) else {}
    counters = {}
    for field in COUNTER_FIELDS:
        av, bv = _number(a.get(field)), _number(b.get(field))
        counters[field] = {"a": av, "b": bv, "delta_b_minus_a": round(bv-av, 4) if av is not None and bv is not None else None}
    return {
        "counters": counters,
        "derived": {"a": derive_metrics(a), "b": derive_metrics(b)},
        "metadata": {"comparison": "same_mode_counters", "missing_values": "null"},
    }
