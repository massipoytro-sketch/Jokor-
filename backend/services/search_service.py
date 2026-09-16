from adapters.freefire.client import FreeFireClient


class SearchService:
    def __init__(self):
        self.client = FreeFireClient()

    def search(self, region: str, keyword: str) -> dict:
        try:
            data = self.client.search(region, keyword)
            return {"success": True, "data": data, "metadata": {"region": region, "keyword": keyword}}
        except NotImplementedError:
            return {"success": False, "error": "DATA_SOURCE_NOT_CONFIGURED", "message": "Search provider is not configured."}
