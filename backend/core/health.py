from core.config import settings


def health_snapshot() -> dict:
    return {
        "service": "jokor-api",
        "version": settings.version,
        "status": "healthy",
        "checks": {
            "application": "ok",
            "configuration": "ok",
            "provider_layer": "isolated",
        },
    }
