class AnalyticsService:
    """Provider-agnostic player comparison calculations.

    The service only derives deltas from data returned by the configured
    provider. It never invents missing player statistics.
    """

    def __init__(self, stats_service):
        self.stats_service = stats_service

    @staticmethod
    def _number(section: dict, key: str):
        data = section.get("data") if section.get("success") else None
        if not isinstance(data, dict):
            return None
        value = data.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        return float(value)

    @classmethod
    def _mode_metrics(cls, a: dict, b: dict) -> dict:
        fields = ("matches", "wins", "kills", "deaths", "headshots", "rankingPoints")
        metrics = {}
        for field in fields:
            a_value = cls._number(a, field)
            b_value = cls._number(b, field)
            metrics[field] = {
                "a": a_value,
                "b": b_value,
                "delta_a_minus_b": (a_value - b_value) if a_value is not None and b_value is not None else None,
            }

        for field in ("win_rate", "headshot_rate"):
            a_value = cls._number(a, field)
            b_value = cls._number(b, field)
            if a_value is None:
                a_value = cls._derived_rate(a, field)
            if b_value is None:
                b_value = cls._derived_rate(b, field)
            metrics[field] = {
                "a": a_value,
                "b": b_value,
                "delta_a_minus_b": (a_value - b_value) if a_value is not None and b_value is not None else None,
            }
        return metrics

    @classmethod
    def _derived_rate(cls, section: dict, field: str):
        matches = cls._number(section, "matches")
        wins = cls._number(section, "wins")
        kills = cls._number(section, "kills")
        headshots = cls._number(section, "headshots")
        if field == "win_rate" and matches and wins is not None:
            return wins / matches * 100
        if field == "headshot_rate" and kills and headshots is not None:
            return headshots / kills * 100
        return None

    def compare(self, region: str, uid_a: str, uid_b: str) -> dict:
        br_a = self.stats_service.get_stats(region, uid_a, "br")
        br_b = self.stats_service.get_stats(region, uid_b, "br")
        cs_a = self.stats_service.get_stats(region, uid_a, "cs")
        cs_b = self.stats_service.get_stats(region, uid_b, "cs")
        success = all(section.get("success") for section in (br_a, br_b, cs_a, cs_b))
        return {
            "success": success,
            "players": {
                "a": {"uid": uid_a, "br": br_a, "cs": cs_a},
                "b": {"uid": uid_b, "br": br_b, "cs": cs_b},
            },
            "comparison": {
                "br": self._mode_metrics(br_a, br_b),
                "cs": self._mode_metrics(cs_a, cs_b),
            },
            "metadata": {
                "region": region,
                "comparison": "battle_royale_and_clash_squad",
                "players_compared": 2,
            },
        }
