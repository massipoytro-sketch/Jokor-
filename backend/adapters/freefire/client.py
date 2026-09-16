class FreeFireClient:
    """Safe boundary for public/informational Free Fire data.

    Provider-specific protocol work stays behind this class. No credentials,
    token capture, account modification, or authentication-bypass operations
    belong in Jokor.
    """

    def get_profile(self, region: str, uid: str) -> dict:
        raise NotImplementedError("Public profile provider is not configured yet.")

    def get_stats(self, region: str, uid: str, mode: str) -> dict:
        raise NotImplementedError("Public statistics provider is not configured yet.")

    def search(self, region: str, keyword: str) -> list:
        raise NotImplementedError("Public search provider is not configured yet.")

    def get_guild(self, region: str, guild_id: str) -> dict:
        raise NotImplementedError("Public guild provider is not configured yet.")
