import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    version: str = os.getenv("JOKOR_VERSION", "1.1.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("JOKOR_DEBUG", "false").lower() == "true"
    cors_origins: list[str] = tuple(x.strip() for x in os.getenv("CORS_ORIGINS", "*").split(","))
    cache_ttl: int = int(os.getenv("CACHE_TTL", "300"))
    rate_limit: int = int(os.getenv("RATE_LIMIT", "60"))
    # Real public API implementation used by Jokor; no API key is required.
    freefire_provider_url: str = os.getenv(
        "FREEFIRE_PROVIDER_URL",
        "https://free-ff-api-src-5plp.onrender.com",
    )
    provider_timeout: float = float(os.getenv("PROVIDER_TIMEOUT", "8"))


settings = Settings()
