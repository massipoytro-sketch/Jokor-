class FreeFireClient:
    """Boundary for Jokor's Free Fire data source.

    This layer deliberately contains no account credentials, token capture,
    account modification, or authentication-bypass logic. Only public,
    informational player data should be normalized here.
    """

    def get_profile(self, region: str, uid: str) -> dict:
        raise NotImplementedError(
            "Free Fire public-data adapter is not configured yet. "
            "Complete source/protobuf compatibility testing before enabling it."
        )
