"""Central provider hub used by Jokor services.

Services depend on this small boundary rather than knowing how providers are selected.
A future validated provider can be registered without changing the HTTP API.
"""
from adapters.freefire.client import FreeFireClient
from adapters.freefire.normalizer import normalize_profile, normalize_stats
from providers.registry import ProviderRegistry


class FreeFireClientProvider:
    name = "freefire-adapter"

    def __init__(self, client=None):
        self.client = client or FreeFireClient()

    def get_profile(self, region: str, uid: str) -> dict:
        return normalize_profile(self.client.get_profile(region, uid), region, uid)

    def get_stats(self, region: str, uid: str, mode: str) -> dict:
        return normalize_stats(self.client.get_stats(region, uid, mode))

    def search(self, region: str, keyword: str) -> list:
        return self.client.search(region, keyword)

    def get_guild(self, region: str, guild_id: str) -> dict:
        return self.client.get_guild(region, guild_id)


class ProviderHub:
    def __init__(self, providers=None):
        self.registry = ProviderRegistry(providers or [FreeFireClientProvider()])

    def call(self, method: str, *args, **kwargs):
        return self.registry.call(method, *args, **kwargs)

    def names(self):
        return self.registry.names()


provider_hub = ProviderHub()
