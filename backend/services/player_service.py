from core.cache import TTLCache
from core.config import settings
from providers.registry import ProviderUnavailable
from services.provider_service import provider_hub


class PlayerService:
    def __init__(self, provider=None):
        self.provider = provider or provider_hub
        self.cache = TTLCache()

    def get_profile(self, region: str, uid: str) -> dict:
        key = f"profile:{region}:{uid}"
        cached = self.cache.get(key)
        if cached is not None:
            return {**cached, "metadata": {**cached.get("metadata", {}), "cache": "hit"}}
        try:
            data, provider_name = self.provider.call("get_profile", region, uid)
            result = {
                "success": True,
                "data": data,
                "metadata": {"region": region, "uid": uid, "cache": "miss", "provider": provider_name},
            }
            self.cache.set(key, result, settings.cache_ttl)
            return result
        except ProviderUnavailable as exc:
            return {"success": False, "error": "DATA_SOURCE_NOT_CONFIGURED", "message": str(exc)}
        except Exception:
            return {"success": False, "error": "PLAYER_LOOKUP_FAILED", "message": "The player data source is temporarily unavailable."}
