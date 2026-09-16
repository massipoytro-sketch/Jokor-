"""Safe Free Fire TCP protocol adapter package.

This package is intentionally transport/protocol oriented. It never accepts,
stores, extracts, or generates player passwords, session cookies, or bearer
credentials. Authentication-dependent operations must be supplied by an
approved provider outside this adapter.
"""

from .provider import FreeFireTCPProvider

__all__ = ["FreeFireTCPProvider"]
