"""Provider facade for the optional Free Fire TCP protocol adapter."""
from __future__ import annotations

import os

from providers.base import PublicDataProvider
from providers.freefire_tcp.client import FreeFireTCPClient, TCPConfig


class FreeFireTCPProvider(PublicDataProvider):
    name = "freefire-tcp"

    def __init__(self):
        host = os.getenv("JOKOR_TCP_PROVIDER_HOST")
        port = os.getenv("JOKOR_TCP_PROVIDER_PORT")
        self.enabled = bool(host and port)
        self.client = None
        if self.enabled:
            self.client = FreeFireTCPClient(TCPConfig(host=host, port=int(port)))

    def health(self) -> dict:
        if not self.enabled or self.client is None:
            return {"name": self.name, "status": "disabled", "reason": "endpoint_not_configured"}
        try:
            return {"name": self.name, "status": "reachable", **self.client.probe()}
        except (OSError, TimeoutError) as exc:
            return {"name": self.name, "status": "unreachable", "error": type(exc).__name__}

    def get_profile(self, region: str, uid: str) -> dict:
        raise NotImplementedError("TCP profile lookup requires an approved authenticated provider")

    def get_stats(self, region: str, uid: str, mode: str) -> dict:
        raise NotImplementedError("TCP stats lookup requires an approved authenticated provider")
