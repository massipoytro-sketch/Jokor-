"""Free Fire public-data provider boundary used by Jokor.

When FREEFIRE_COMMUNITY_API_KEY is configured, profile/stats/auto-detection
use the documented Free Fire Community API. The older Render provider remains
only as a compatibility fallback when no primary key is configured.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from adapters.freefire.community import FreeFireCommunityClient
from core.config import settings
from core.regions import SUPPORTED_REGIONS


class FreeFireClient:
    """Provider boundary for public/informational Free Fire data."""

    def __init__(self, base_url=None, timeout=None):
        self.base_url = (base_url or settings.freefire_provider_url).rstrip("/")
        self.timeout = timeout or settings.provider_timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json", "User-Agent": "Jokor/2.3"})
        self.community = FreeFireCommunityClient(timeout=self.timeout)

    @property
    def primary_enabled(self) -> bool:
        return self.community.enabled

    def _get(self, path, params):
        response = self.session.get(f"{self.base_url}{path}", params=params, timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("Provider returned a non-object payload")
        return payload

    def get_profile(self, region: str, uid: str) -> dict:
        if self.primary_enabled:
            return self.community.get_profile(region, uid)
        return self._get("/api/v1/account", {"region": region, "uid": uid})

    def get_stats(self, region: str, uid: str, mode: str) -> dict:
        if self.primary_enabled:
            return self.community.get_stats(region, uid, mode)
        return self._get("/api/v1/playerstats", {"region": region, "uid": uid, "gamemode": mode})

    @staticmethod
    def _payload_matches_uid(payload: dict, uid: str) -> bool:
        basic = payload.get("basicInfo") or payload.get("basic_info") or payload.get("data") or payload
        if not isinstance(basic, dict):
            return False
        for key in ("accountId", "uid", "account_id", "playerId", "player_id"):
            value = basic.get(key)
            if value is not None:
                return str(value) == str(uid)
        return False

    def detect_profile(self, uid: str) -> tuple[str, dict]:
        """Find a UID's region using the primary provider or legacy fallback."""
        if self.primary_enabled:
            return self.community.detect_profile(uid)

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
            raise RuntimeError("The Free Fire public data provider did not respond successfully. Configure the primary provider or try again later.")
        raise LookupError("Player was not found in the supported regions.")

    def search(self, region: str, keyword: str) -> list:
        payload = self._get("/api/v1/account", {"region": region, "uid": keyword})
        return payload.get("infos") or payload.get("results") or [payload]

    def get_guild(self, region: str, guild_id: str) -> dict:
        payload = self._get("/api/v1/guild", {"region": region, "guildID": guild_id})
        return payload
