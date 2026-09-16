from adapters.freefire.client import FreeFireClient
from core.cache import TTLCache
from core.config import settings


class PlayerService:
    def __init__(self):
        self.client = FreeFireClient()
        self.cache = TTLCache()

    def get_profile(self, region: str, uid: str) -> dict:
        key = f"profile:{region}:{uid}"
        cached = self.cache.get(key)
        if cached is not None:
            return {**cached, "metadata": {**cached.get("metadata", {}), "cache": "hit"}}
        try:
            data = self.client.get_profile(region, uid)
            result = {"success": True, "data": data, "metadata": {"region": region, "uid": uid, "cache": "miss"}}
            self.cache.set(key, result, settings.cache_ttl)
            return result
        except NotImplementedError as exc:
            return {"success": False, "error": "DATA_SOURCE_NOT_CONFIGURED", "message": str(exc)}
        except Exception:
            return {"success": False, "error": "PLAYER_LOOKUP_FAILED", "message": "The player data source is temporarily unavailable."}
