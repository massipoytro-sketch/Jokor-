from abc import ABC, abstractmethod
from typing import Any


class PublicDataProvider(ABC):
    name = "unknown"

    @abstractmethod
    def get_profile(self, region: str, uid: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_stats(self, region: str, uid: str, mode: str) -> dict[str, Any]:
        raise NotImplementedError

    def search(self, region: str, keyword: str) -> list[dict[str, Any]]:
        raise NotImplementedError

    def get_guild(self, region: str, guild_id: str) -> dict[str, Any]:
        raise NotImplementedError
