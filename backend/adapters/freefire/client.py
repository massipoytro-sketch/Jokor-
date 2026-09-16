"""Safe public-data adapter for Free Fire profile/stat lookups.

Jokor never accepts player passwords, access tokens, session tokens, or other
account credentials. The adapter talks only to a public informational API.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from core.config import settings
from core.regions import SUPPORTED_REGIONS


class FreeFireClient:
    """Provider boundary for public/informational Free Fire data."""

    def __init__(self, base_url=None, timeout=None):
        self.base_url = (base_url or settings.freefire_provider_url).rstrip("/")
        self.timeout = timeout or settings.provider_timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json", "User-Agent": "Jokor/1.1"})

    def _get(self, path, params):
        response = self.session.get(f"{self.base_url}{path}", params=params, timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("Provider returned a non-object payload")
        return payload

    def get_profile(self, region: str, uid: str) -> dict:
        return self._get("/api/v1/account", {"region": region, "uid": uid})

    def get_stats(self, region: str, uid: str, mode: str) -> dict:
        return self._get("/api/v1/playerstats", {"region": region, "uid": uid, "gamemode": mode})

    @staticmethod
    def _payload_matches_uid(payload: dict, uid: str) -> bool:
        """Accept the common public-provider response shapes.

        Some provider responses omit accountId and put the identity directly
        in the top-level object, so requiring accountId caused false 404s.
        """
        basic = payload.get("basicInfo") or payload.get("basic_info") or payload
        if not isinstance(basic, dict):
            return False
        for key in ("accountId", "uid", "account_id", "playerId", "player_id"):
            value = basic.get(key)
            if value is not None:
                return str(value) == str(uid)
        # A response containing recognizable profile fields is still a valid
        # profile response when this provider does not echo the UID.
        return any(basic.get(key) is not None for key in ("nickname", "name", "accountName", "level", "liked", "likes"))

    def detect_profile(self, uid: str) -> tuple[str, dict]:
        """Find a UID's region without asking the user to choose a server."""
        regions = sorted(SUPPORTED_REGIONS)
        errors = []
        successful_responses = 0
        with ThreadPoolExecutor(max_workers=min(8, len(regions))) as pool:
            futures = {pool.submit(self.get_profile, region, uid): region for region in regions}
            for future in as_completed(futures):
                region = futures[future]
                try:
                    payload = future.result()
                    successful_responses += 1
                    if self._payload_matches_uid(payload, uid):
                        basic = payload.get("basicInfo") or payload.get("basic_info") or payload
                        detected = str((basic.get("region") if isinstance(basic, dict) else None) or region).upper()
                        return detected, payload
                except Exception as exc:
                    errors.append(f"{region}:{type(exc).__name__}")
        if successful_responses == 0:
            raise RuntimeError("The Free Fire public data provider did not respond successfully. Please try again in a moment.")
        raise LookupError("Player was not found in the supported regions.")

    def search(self, region: str, keyword: str) -> list:
        payload = self._get("/api/v1/account", {"region": region, "uid": keyword})
        return payload.get("infos") or payload.get("results") or [payload]

    def get_guild(self, region: str, guild_id: str) -> dict:
        return self._get("/api/v1/guild", {"region": region, "guildID": guild_id})
