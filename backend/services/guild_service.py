from adapters.freefire.client import FreeFireClient


class GuildService:
    def __init__(self):
        self.client = FreeFireClient()

    def get_guild(self, region: str, guild_id: str) -> dict:
        try:
            data = self.client.get_guild(region, guild_id)
            return {"success": True, "data": data, "metadata": {"region": region, "guild_id": guild_id}}
        except NotImplementedError:
            return {"success": False, "error": "DATA_SOURCE_NOT_CONFIGURED", "message": "Guild provider is not configured."}
