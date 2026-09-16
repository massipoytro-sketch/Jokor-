"""Safe account-link diagnostics.

This module intentionally never accepts game passwords, access tokens, cookies,
or performs unlink operations itself. It exposes a provider-neutral schema that
can be backed by an official OAuth/account-management integration later.
"""
from __future__ import annotations

from typing import Any


LINK_TYPES = [
    {"id": "google", "name": "Google", "category": "social_login"},
    {"id": "facebook", "name": "Facebook", "category": "social_login"},
    {"id": "vk", "name": "VK", "category": "social_login"},
    {"id": "apple", "name": "Apple", "category": "social_login"},
    {"id": "game_center", "name": "Game Center", "category": "platform"},
    {"id": "garena", "name": "Garena", "category": "publisher_account"},
]


def supported_link_types() -> list[dict[str, str]]:
    return list(LINK_TYPES)


def diagnostic_schema(uid: str, region: str) -> dict[str, Any]:
    return {
        "uid": uid,
        "region": region,
        "status": "provider-required",
        "privacy": {
            "credentials_required": False,
            "tokens_collected": False,
            "cookies_collected": False,
        },
        "links": [
            {
                **item,
                "state": "unknown",
                "can_unlink": False,
                "unlink_method": "official_provider_only",
            }
            for item in LINK_TYPES
        ],
        "message": "Link state requires an official account-management provider. Jokor never asks for game passwords or session tokens.",
    }
