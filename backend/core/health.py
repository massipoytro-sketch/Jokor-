from core.config import settings
from services.provider_service import provider_hub


def health_snapshot() -> dict:
    providers = provider_hub.names()
    return {
        "service": "jokor-api",
        "version": settings.version,
        "status": "healthy",
        "checks": {
            "application": "ok",
            "configuration": "ok",
            "provider_layer": "configured" if providers else "empty",
        },
        "providers": providers,
        "cache": {"type": "in-memory-ttl"},
        "rate_limit": {"requests_per_minute": settings.rate_limit},
    }
