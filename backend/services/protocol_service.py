"""Safe protocol diagnostics inspired by the FreeFire-TCP-BOT research surface.

This module deliberately stops at transport/frame inspection. It does not accept
credentials, session tokens, or implement account/game-state mutations.
"""
from __future__ import annotations

import base64
import binascii

from providers.freefire_tcp.protocol import safe_hex, split_length_prefixed


def inspect_frame(encoded_payload: str, *, width: int = 4) -> dict:
    """Inspect one base64-encoded length-prefixed frame without executing it."""
    if not isinstance(encoded_payload, str) or not encoded_payload.strip():
        raise ValueError("payload must be a non-empty base64 string")
    try:
        raw = base64.b64decode(encoded_payload, validate=True)
    except (ValueError, binascii.Error) as exc:
        raise ValueError("payload must be valid base64") from exc
    if len(raw) > 65536:
        raise ValueError("payload exceeds the 64 KiB diagnostic limit")
    frame, remaining = split_length_prefixed(raw, width=width)
    return {
        "frame_length": frame.length,
        "remaining_bytes": len(remaining),
        "payload_hex": safe_hex(frame.payload),
        "payload_size": len(frame.payload),
        "truncated_hex": len(frame.payload) > 128,
    }


def protocol_capabilities() -> dict:
    return {
        "transport": ["tcp_probe"],
        "diagnostics": ["length_prefixed_frame_inspection", "bounded_hex_preview"],
        "catalog_ready": ["emote_metadata", "protocol_metadata"],
        "disabled": ["credential_handling", "session_token_storage", "account_mutation", "automation_spam"],
    }
