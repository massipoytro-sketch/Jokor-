from adapters.freefire.normalizer import normalize_profile, normalize_stats
from providers.registry import ProviderRegistry, ProviderUnavailable


class EmptyProvider:
    name = "empty"

    def get_profile(self, region, uid):
        raise NotImplementedError

    def get_stats(self, region, uid, mode):
        raise NotImplementedError


def test_profile_normalizer_accepts_common_aliases():
    result = normalize_profile({
        "basicInfo": {
            "accountId": 123,
            "nickname": "Jokor",
            "accountLevel": 42,
            "liked": 900,
            "guildId": "77",
        }
    }, "EU", "fallback")
    assert result["uid"] == "123"
    assert result["nickname"] == "Jokor"
    assert result["level"] == 42
    assert result["likes"] == 900
    assert result["guild_id"] == "77"


def test_stats_normalizer_preserves_missing_values_as_null():
    result = normalize_stats({"stats": {"games": 10, "wins": 2, "kills": 30}})
    assert result["matches"] == 10
    assert result["wins"] == 2
    assert result["deaths"] is None


def test_registry_raises_clear_error_when_all_providers_fail():
    registry = ProviderRegistry([EmptyProvider()])
    try:
        registry.call("get_profile", "EU", "123")
    except ProviderUnavailable as exc:
        assert "No configured provider" in str(exc)
    else:
        raise AssertionError("ProviderUnavailable was not raised")
