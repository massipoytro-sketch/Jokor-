from adapters.freefire.client import FreeFireClient


class PlayerService:
    def __init__(self):
        self.client = FreeFireClient()

    def get_profile(self, region: str, uid: str) -> dict:
        """Return a normalized public player profile.

        The adapter is intentionally separated from the HTTP layer so the
        data source can be changed without rewriting Jokor's API.
        """
        try:
            data = self.client.get_profile(region, uid)
            return {
                "success": True,
                "data": data,
                "metadata": {"region": region, "uid": uid},
                "http_status": 200,
            }
        except NotImplementedError as exc:
            return {
                "success": False,
                "error": "DATA_SOURCE_NOT_CONFIGURED",
                "message": str(exc),
                "http_status": 503,
            }
        except Exception:
            return {
                "success": False,
                "error": "PLAYER_LOOKUP_FAILED",
                "message": "The player data source is temporarily unavailable.",
                "http_status": 502,
            }
