SUPPORTED_REGIONS = {
    "BD", "BR", "CIS", "EU", "ID", "IND", "ME", "NA", "PK",
    "RU", "SAC", "SG", "TH", "TW", "US", "VN"
}

REGION_GROUPS = {
    "IND": "IND", "BD": "GLOBAL", "PK": "GLOBAL", "ME": "GLOBAL",
    "BR": "LATAM", "SAC": "LATAM", "NA": "NORTH_AMERICA", "US": "NORTH_AMERICA",
    "EU": "EUROPE", "CIS": "CIS", "RU": "CIS", "ID": "SEA", "SG": "SEA",
    "TH": "SEA", "TW": "SEA", "VN": "SEA",
}


def normalize_region(region: str) -> str:
    return region.strip().upper()


def region_group(region: str) -> str:
    return REGION_GROUPS.get(normalize_region(region), "UNKNOWN")
