"""Free Fire public-data provider used by Jokor.

Jokor uses the public Free Fire API implementation documented by the
0xMe/free-ff-api project. It exposes account, player-stats and guildInfo
endpoints without requiring an API key in Jokor.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from core.config import settings
from core.regions import SUPPORTED_REGIONS


class FreeFireClient:
    """Client for Jokor's real public Free Fire data source."""

    def __init__(self, base_url=None, timeout=None):
        self.base_url = (base_url or settings.freefire_provider_url).rstrip("/")
        self.timeout = timeout or settings.provider_timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json", "User-Agent": "Jokor/2.3"})

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
        # The public upstream playerstats endpoint exposes its BR-style
        # aggregate in one response; it does not document a gamemode query.
        # Keep the Jokor mode argument for API compatibility, but never send
        # an unsupported parameter upstream.
        return self._get("/api/v1/playerstats", {"region": region, "uid": uid})

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
        """Automatically discover the player's actual supported region."""
        regions = sorted(SUPPORTED_REGIONS)
        successful_responses = 0
        errors = []

        with ThreadPoolExecutor(max_workers=min(8, len(regions))) as pool:
            futures = {
                pool.submit(self.get_profile, region, uid): region
                for region in regions
            }
            for future in as_completed(futures):
                region = futures[future]
                try:
                    payload = future.result()
                    successful_responses += 1
                    if self._payload_matches_uid(payload, uid):
                        basic = payload.get("basicInfo") or payload.get("basic_info") or payload
                        detected = str(
                            (basic.get("region") if isinstance(basic, dict) else None) or region
                        ).upper()
                        return detected, payload
                except requests.RequestException as exc:
                    errors.append(f"{region}:{type(exc).__name__}")
                except (ValueError, KeyError, TypeError) as exc:
                    errors.append(f"{region}:{type(exc).__name__}")

        if successful_responses == 0:
            detail = ", ".join(errors[:4])
            raise RuntimeError(
                "The Free Fire public data provider is unavailable"
                + (f" ({detail})" if detail else "")
            )
        raise LookupError("Player was not found in the supported regions.")

    def search(self, region: str, keyword: str) -> list:
        payload = self._get("/api/v1/account", {"region": region, "uid": keyword})
        return payload.get("infos") or payload.get("results") or [payload]

    def get_guild(self, region: str, guild_id: str) -> dict:
        return self._get(
            "/api/v1/guildInfo",
            {"region": region, "guildID": guild_id},
        )
