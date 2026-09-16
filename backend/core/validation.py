"""Reusable input validation for Jokor's public-information API."""
import re

UID_RE = re.compile(r"^[0-9]{1,15}$")
REGION_RE = re.compile(r"^[A-Z]{2,5}$")


def validate_uid(value: str) -> bool:
    return bool(UID_RE.fullmatch(str(value or ""))) and int(value) > 0


def validate_region(value: str, supported: set[str]) -> bool:
    normalized = str(value or "").strip().upper()
    return bool(REGION_RE.fullmatch(normalized)) and normalized in supported


def validate_keyword(value: str, minimum: int = 2, maximum: int = 64) -> bool:
    value = str(value or "").strip()
    return minimum <= len(value) <= maximum and not any(ord(c) < 32 for c in value)
