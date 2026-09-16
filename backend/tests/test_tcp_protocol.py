from providers.freefire_tcp.protocol import safe_hex, split_length_prefixed


def test_split_length_prefixed_frame():
    frame, rest = split_length_prefixed((3).to_bytes(4, "big") + b"abc" + b"tail")
    assert frame.payload == b"abc"
    assert frame.length == 3
    assert rest == b"tail"


def test_split_length_prefixed_rejects_incomplete():
    try:
        split_length_prefixed(b"\x00\x00\x00\x05abc")
    except ValueError as exc:
        assert "incomplete" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_safe_hex_is_bounded():
    assert safe_hex(b"abcdef", limit=2) == "6162"
