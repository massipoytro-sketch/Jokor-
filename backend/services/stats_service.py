from providers.registry import ProviderUnavailable
from services.provider_service import provider_hub
from services.statistics import derive_metrics


class StatsService:
    def __init__(self, player_service=None, provider=None):
        self.player_service = player_service
        self.provider = provider or provider_hub

    def get_stats(self, region: str, uid: str, mode: str = "br") -> dict:
        if mode not in {"br", "cs"}:
            return {"success": False, "error": "INVALID_MODE", "message": "Mode must be br or cs."}
        try:
            data, provider_name = self.provider.call("get_stats", region, uid, mode)
            payload = dict(data) if isinstance(data, dict) else {"raw": data}
            counters = {key: payload.get(key) for key in ("matches", "wins", "kills", "deaths", "headshots")}
            payload["derived"] = derive_metrics(counters)
            return {
                "success": True,
                "data": payload,
                "metadata": {"region": region, "uid": uid, "mode": mode, "provider": provider_name},
            }
        except ProviderUnavailable as exc:
            return {"success": False, "error": "DATA_SOURCE_NOT_CONFIGURED", "message": str(exc)}
        except Exception:
            return {"success": False, "error": "STATS_LOOKUP_FAILED", "message": "The statistics data source is temporarily unavailable."}
