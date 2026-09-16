from providers.registry import ProviderUnavailable
from services.provider_service import provider_hub


class GuildService:
    def __init__(self, provider=None):
        self.provider = provider or provider_hub

    def get_guild(self, region: str, guild_id: str) -> dict:
        try:
            data, provider_name = self.provider.call("get_guild", region, guild_id)
            return {
                "success": True,
                "data": data,
                "metadata": {"region": region, "guild_id": guild_id, "provider": provider_name},
            }
        except ProviderUnavailable as exc:
            return {"success": False, "error": "DATA_SOURCE_NOT_CONFIGURED", "message": str(exc)}
        except Exception:
            return {"success": False, "error": "GUILD_LOOKUP_FAILED", "message": "The guild data source is temporarily unavailable."}
