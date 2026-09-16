"""High-level player intelligence aggregation for Jokor.

The service composes provider-backed profile and BR/CS statistics into one
stable response. Missing upstream data is never invented.
"""
from __future__ import annotations

from typing import Any


class IntelligenceService:
    def __init__(self, player_service, stats_service):
        self.player_service = player_service
        self.stats_service = stats_service

    @staticmethod
    def _number(data: dict[str, Any], *keys: str) -> float | None:
        for key in keys:
            value = data.get(key)
            if isinstance(value, bool):
                continue
            if isinstance(value, (int, float)):
                return float(value)
        return None

    @classmethod
    def _section_metrics(cls, section: dict[str, Any]) -> dict[str, Any]:
        data = section.get("data") if section.get("success") else None
        if not isinstance(data, dict):
            return {"available": False}
        matches = cls._number(data, "matches", "gamesPlayed")
        wins = cls._number(data, "wins")
        kills = cls._number(data, "kills")
        headshots = cls._number(data, "headshots")
        return {
            "available": True,
            "matches": matches,
            "wins": wins,
            "kills": kills,
            "headshots": headshots,
            "win_rate": (wins / matches * 100) if matches and wins is not None else None,
            "headshot_rate": (headshots / kills * 100) if kills and headshots is not None else None,
        }

    def scan(self, region: str, uid: str) -> dict[str, Any]:
        profile = self.player_service.get_profile(region, uid)
        br = self.stats_service.get_stats(region, uid, "br")
        cs = self.stats_service.get_stats(region, uid, "cs")
        sections = {"profile": profile, "br": br, "cs": cs}
        available = [name for name, value in sections.items() if value.get("success")]
        completeness = round(len(available) / len(sections) * 100)
        metrics = {"br": self._section_metrics(br), "cs": self._section_metrics(cs)}
        insights: list[str] = []
        for mode, values in metrics.items():
            if values["headshot_rate"] is not None:
                insights.append(f"{mode.upper()} headshot rate is {values['headshot_rate']:.1f}%.")
            if values["win_rate"] is not None:
                insights.append(f"{mode.upper()} win rate is {values['win_rate']:.1f}%.")
        return {
            "success": bool(available),
            "data": {
                "uid": uid,
                "region": region,
                "profile": profile,
                "br": br,
                "cs": cs,
                "metrics": metrics,
                "profile_completeness": completeness,
                "available_sections": available,
                "insights": insights,
            },
            "metadata": {
                "region": region,
                "uid": uid,
                "service": "player-intelligence",
                "sections_requested": len(sections),
                "sections_available": len(available),
            },
        }
