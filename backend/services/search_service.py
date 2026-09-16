from providers.registry import ProviderUnavailable
from services.provider_service import provider_hub


class SearchService:
    def __init__(self, provider=None):
        self.provider = provider or provider_hub

    def search(self, region: str, keyword: str) -> dict:
        try:
            data, provider_name = self.provider.call("search", region, keyword)
            return {
                "success": True,
                "data": data,
                "metadata": {"region": region, "keyword": keyword, "provider": provider_name},
            }
        except ProviderUnavailable as exc:
            return {"success": False, "error": "DATA_SOURCE_NOT_CONFIGURED", "message": str(exc)}
        except Exception:
            return {"success": False, "error": "SEARCH_FAILED", "message": "The search data source is temporarily unavailable."}
