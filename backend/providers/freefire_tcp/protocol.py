"""Small, dependency-free helpers for inspecting framed TCP payloads.

The upstream Free Fire TCP bot repository contains a much larger automation
stack. Jokor only keeps generic framing/inspection primitives here. They are
useful for provider development and tests without implementing account
automation or credential handling.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Frame:
    payload: bytes
    length: int


def split_length_prefixed(data: bytes, *, width: int = 4, byteorder: str = "big") -> tuple[Frame, bytes]:
    """Decode one length-prefixed frame and return the remaining bytes.

    Raises ValueError for malformed/incomplete frames. No interpretation of
    the payload is performed.
    """
    if width not in (1, 2, 4, 8):
        raise ValueError("width must be one of 1, 2, 4 or 8")
    if len(data) < width:
        raise ValueError("incomplete frame header")
    length = int.from_bytes(data[:width], byteorder=byteorder, signed=False)
    end = width + length
    if len(data) < end:
        raise ValueError("incomplete frame payload")
    return Frame(data[width:end], length), data[end:]


def safe_hex(data: bytes, limit: int = 128) -> str:
    """Return a bounded hexadecimal representation for diagnostics."""
    return bytes(data[:limit]).hex()
