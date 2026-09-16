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

    def detect_profile(self, uid: str) -> tuple[str, dict]:
        """Find a UID's region without asking the user to choose a server."""
        regions = sorted(SUPPORTED_REGIONS)
        errors = []
        with ThreadPoolExecutor(max_workers=min(8, len(regions))) as pool:
            futures = {pool.submit(self.get_profile, region, uid): region for region in regions}
            for future in as_completed(futures):
                region = futures[future]
                try:
                    payload = future.result()
                    basic = payload.get("basicInfo") or payload.get("basic_info") or payload
                    if isinstance(basic, dict) and str(basic.get("accountId", uid)) == str(uid):
                        detected = str(basic.get("region") or region).upper()
                        return detected, payload
                except Exception as exc:
                    errors.append(f"{region}:{type(exc).__name__}")
        raise LookupError("Player was not found in the supported regions.")

    def search(self, region: str, keyword: str) -> list:
        payload = self._get("/api/v1/account", {"region": region, "uid": keyword})
        return payload.get("infos") or payload.get("results") or [payload]

    def get_guild(self, region: str, guild_id: str) -> dict:
        return self._get("/api/v1/guild", {"region": region, "guildID": guild_id})
