"""Central provider hub used by Jokor services."""
from adapters.freefire.client import FreeFireClient
from adapters.freefire.normalizer import normalize_profile, normalize_stats
from providers.registry import ProviderRegistry


class FreeFireClientProvider:
    name = "freefire-public"

    def __init__(self, client=None):
        self.client = client or FreeFireClient()

    def get_profile(self, region: str, uid: str) -> dict:
        return normalize_profile(self.client.get_profile(region, uid), region, uid)

    def get_stats(self, region: str, uid: str, mode: str) -> dict:
        return normalize_stats(self.client.get_stats(region, uid, mode), mode)

    def detect_profile(self, uid: str) -> tuple[str, dict]:
        region, payload = self.client.detect_profile(uid)
        return region, normalize_profile(payload, region, uid)

    def search(self, region: str, keyword: str) -> list:
        return self.client.search(region, keyword)

    def get_guild(self, region: str, guild_id: str) -> dict:
        return self.client.get_guild(region, guild_id)


class ProviderHub:
    def __init__(self, providers=None):
        self.registry = ProviderRegistry(providers or [FreeFireClientProvider()])

    def call(self, method: str, *args, **kwargs):
        return self.registry.call(method, *args, **kwargs)

    def detect_profile(self, uid: str):
        for provider in self.registry.providers:
            method = getattr(provider, "detect_profile", None)
            if method is None:
                continue
            return method(uid), provider.name
        raise RuntimeError("No provider supports automatic region detection")

    def names(self):
        return self.registry.names()


provider_hub = ProviderHub()
