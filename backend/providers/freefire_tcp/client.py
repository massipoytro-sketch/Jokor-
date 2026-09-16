"""Optional TCP transport for an explicitly configured protocol endpoint."""
from __future__ import annotations

import socket
from dataclasses import dataclass


@dataclass(frozen=True)
class TCPConfig:
    host: str
    port: int
    timeout: float = 5.0


class FreeFireTCPClient:
    """Minimal TCP transport with no authentication or account mutation logic."""

    def __init__(self, config: TCPConfig):
        self.config = config

    def probe(self) -> dict:
        """Check whether the configured endpoint accepts a TCP connection."""
        with socket.create_connection((self.config.host, self.config.port), timeout=self.config.timeout):
            return {"reachable": True, "host": self.config.host, "port": self.config.port}
