import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    version: str = os.getenv("JOKOR_VERSION", "1.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("JOKOR_DEBUG", "false").lower() == "true"
    cors_origins: list[str] = tuple(x.strip() for x in os.getenv("CORS_ORIGINS", "*").split(","))
    cache_ttl: int = int(os.getenv("CACHE_TTL", "300"))
    rate_limit: int = int(os.getenv("RATE_LIMIT", "60"))


settings = Settings()
