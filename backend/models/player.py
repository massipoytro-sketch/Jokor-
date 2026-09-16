from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class PlayerProfile:
    uid: str
    region: str
    nickname: str | None = None
    level: int | None = None
    likes: int | None = None
    guild_id: str | None = None
    guild_name: str | None = None
    raw: dict[str, Any] | None = None

    def to_dict(self) -> dict:
        return asdict(self)
