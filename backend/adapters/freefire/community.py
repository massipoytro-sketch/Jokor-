"""Free Fire Community API adapter.

This is a server-side adapter for the documented Free Fire Community API.
The API key is read only from the backend environment and is never exposed
through the browser.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import requests

from core.config import settings


class FreeFireCommunityClient:
    name = "freefire-community"
    _region_map = {
        "IND": "ind",
        "BR": "br",
        "SAC": "br",
        "US": "br",
        "NA": "br",
        "SG": "sg",
        "ID": "sg",
        "TH": "sg",
        "TW": "sg",
        "VN": "sg",
        "ME": "sg",
        "PK": "sg",
        "BD": "sg",
        "CIS": "sg",
        "RU": "sg",
        "EU": "sg",
    }

    def __init__(self, base_url: str | None = None, api_key: str | None = None, timeout: float | None = None):
        self.base_url = (base_url or settings.freefire_community_url).rstrip("/")
        self.api_key = (api_key or settings.freefire_community_api_key).strip()
        self.timeout = timeout or settings.provider_timeout
        self.enabled = bool(self.api_key)
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "Jokor/2.3 (+https://jokor.vercel.app)",
            "x-api-key": self.api_key,
        })

    def _get(self, path: str, params: dict[str, Any]) -> dict:
        if not self.enabled:
            raise RuntimeError("Free Fire Community API key is not configured")
        response = self.session.get(f"{self.base_url}{path}", params=params, timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("Free Fire Community API returned a non-object payload")
        return payload

    @staticmethod
    def _data(payload: dict) -> dict:
        data = payload.get("data")
        if not isinstance(data, dict):
            raise ValueError("Free Fire Community API returned an invalid data object")
        return data

    @classmethod
    def provider_region(cls, region: str) -> str:
        try:
            return cls._region_map[region.upper()]
        except KeyError as exc:
            raise ValueError(f"Unsupported Jokor region: {region}") from exc

    def get_profile(self, region: str, uid: str) -> dict:
        requested = self.provider_region(region)
        payload = self._get("/info", {"region": requested, "uid": uid})
        data = self._data(payload)
        data.setdefault("uid", uid)
        return {"basicInfo": data, "community": payload}

    def get_stats(self, region: str, uid: str, mode: str) -> dict:
        requested = self.provider_region(region)
        payload = self._get("/stats", {"region": requested, "uid": uid})
        data = self._data(payload)
        return {"data": data, "community": payload, "mode": mode}

    def detect_profile(self, uid: str) -> tuple[str, dict]:
        if not self.enabled:
            raise RuntimeError("Free Fire Community API key is not configured")

        # The documented API exposes three region groups, so automatic
        # detection needs only three real upstream requests instead of Jokor's
        # old 16-region fan-out.
        groups = ("sg", "ind", "br")
        errors: list[str] = []
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = {
                pool.submit(self._get, "/info", {"region": group, "uid": uid}): group
                for group in groups
            }
            for future in as_completed(futures):
                group = futures[future]
                try:
                    payload = future.result()
                    data = self._data(payload)
                    returned_uid = str(data.get("uid") or data.get("accountId") or uid)
                    if returned_uid != str(uid):
                        continue
                    detected = str(data.get("region") or group).upper()
                    wrapped = {"basicInfo": {**data, "uid": uid, "region": detected}, "community": payload}
                    return detected, wrapped
                except requests.HTTPError as exc:
                    errors.append(f"{group}:HTTP_{exc.response.status_code if exc.response is not None else 'ERROR'}")
                except Exception as exc:
                    errors.append(f"{group}:{type(exc).__name__}")

        if errors:
            raise RuntimeError("Free Fire Community API lookup failed: " + ", ".join(errors))
        raise LookupError("Player was not found in the supported Free Fire Community API regions.")
