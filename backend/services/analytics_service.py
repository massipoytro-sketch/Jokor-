class AnalyticsService:
    def __init__(self, stats_service):
        self.stats_service = stats_service

    def compare(self, region: str, uid_a: str, uid_b: str) -> dict:
        a = self.stats_service.get_stats(region, uid_a, "br")
        b = self.stats_service.get_stats(region, uid_b, "br")
        return {
            "success": a.get("success") and b.get("success"),
            "players": {"a": a, "b": b},
            "metadata": {"region": region, "comparison": "battle_royale"},
        }
