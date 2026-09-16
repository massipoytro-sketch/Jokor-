class StatsService:
    def __init__(self, player_service):
        self.player_service = player_service

    def get_stats(self, region: str, uid: str, mode: str = "br") -> dict:
        if mode not in {"br", "cs"}:
            return {"success": False, "error": "INVALID_MODE", "message": "Mode must be br or cs."}
        try:
            data = self.player_service.client.get_stats(region, uid, mode)
            return {"success": True, "data": data, "metadata": {"region": region, "uid": uid, "mode": mode}}
        except NotImplementedError:
            return {"success": False, "error": "DATA_SOURCE_NOT_CONFIGURED", "message": "Statistics provider is not configured."}
