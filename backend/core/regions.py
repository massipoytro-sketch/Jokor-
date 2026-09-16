"""Regions actually supported by Jokor's public data provider.

Do not advertise regions that the upstream endpoint does not document.
"""

SUPPORTED_REGIONS = {
    "BD", "BR", "CIS", "ID", "IND", "ME", "PK",
    "RU", "SG", "TH", "TW", "US", "VN"
}

REGION_GROUPS = {
    "IND": "IND", "BD": "GLOBAL", "PK": "GLOBAL", "ME": "GLOBAL",
    "BR": "LATAM", "US": "NORTH_AMERICA", "CIS": "CIS", "RU": "CIS",
    "ID": "SEA", "SG": "SEA", "TH": "SEA", "TW": "SEA", "VN": "SEA",
}


def normalize_region(region: str) -> str:
    return region.strip().upper()


def region_group(region: str) -> str:
    return REGION_GROUPS.get(normalize_region(region), "UNKNOWN")
