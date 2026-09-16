"""Canonical service registry for Jokor.

The registry is descriptive: a service is marked live only when a configured
provider can actually supply the requested data.
"""

SERVICES = [
    {"id": "player-profile", "name": "Player Profile", "group": "player", "status": "live"},
    {"id": "player-stats", "name": "Player Statistics", "group": "player", "status": "live"},
    {"id": "player-compare", "name": "Player Comparison", "group": "analytics", "status": "live"},
    {"id": "player-search", "name": "Player Search", "group": "search", "status": "live"},
    {"id": "guild", "name": "Guild Intelligence", "group": "guild", "status": "live"},
    {"id": "derived-analytics", "name": "Derived Analytics", "group": "analytics", "status": "live"},
    {"id": "catalog", "name": "Game Catalog", "group": "game-data", "status": "live"},
    {"id": "weapons", "name": "Weapons Catalog", "group": "game-data", "status": "live"},
    {"id": "characters", "name": "Characters Catalog", "group": "game-data", "status": "live"},
    {"id": "pets", "name": "Pets Catalog", "group": "game-data", "status": "live"},
    {"id": "cosmetics", "name": "Cosmetics Catalog", "group": "game-data", "status": "live"},
    {"id": "vehicles", "name": "Vehicles Catalog", "group": "game-data", "status": "live"},
    {"id": "rank-history", "name": "Rank History", "group": "history", "status": "provider-dependent"},
    {"id": "activity-history", "name": "Activity History", "group": "history", "status": "provider-dependent"},
    {"id": "leaderboards", "name": "Leaderboards", "group": "competitive", "status": "provider-dependent"},
    {"id": "ban-status", "name": "Ban Status", "group": "player", "status": "provider-dependent"},
    {"id": "friends", "name": "Friends", "group": "social", "status": "provider-dependent"},
    {"id": "inventory", "name": "Inventory", "group": "player", "status": "provider-dependent"},
    {"id": "wishlist", "name": "Wishlist", "group": "player", "status": "provider-dependent"},
    {"id": "wallet", "name": "Wallet Info", "group": "player", "status": "provider-dependent"},
    {"id": "dynamic-duo", "name": "Dynamic Duo", "group": "social", "status": "provider-dependent"},
    {"id": "api-docs", "name": "OpenAPI Schema", "group": "infrastructure", "status": "planned"},
]


def all_services():
    return SERVICES


def get_service(service_id):
    return next((item for item in SERVICES if item["id"] == service_id), None)
