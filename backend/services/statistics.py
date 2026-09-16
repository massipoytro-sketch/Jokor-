"""Pure calculations over statistics returned by a validated provider.

These functions never fetch data and never infer missing values as zero.
"""
from typing import Any


def ratio(numerator: Any, denominator: Any) -> float | None:
    try:
        n, d = float(numerator), float(denominator)
    except (TypeError, ValueError):
        return None
    if d <= 0:
        return None
    return round(n / d, 4)


def percentage(numerator: Any, denominator: Any) -> float | None:
    value = ratio(numerator, denominator)
    return round(value * 100, 2) if value is not None else None


def derive_metrics(stats: dict) -> dict:
    """Derive common rates only when source counters exist."""
    stats = stats if isinstance(stats, dict) else {}
    matches = stats.get("matches")
    wins = stats.get("wins")
    kills = stats.get("kills")
    deaths = stats.get("deaths")
    headshots = stats.get("headshots")
    return {
        "win_rate_pct": percentage(wins, matches),
        "kd_ratio": ratio(kills, deaths),
        "headshot_rate_pct": percentage(headshots, kills),
        "data_note": "Derived values are null when source counters are missing or denominator is zero.",
    }
