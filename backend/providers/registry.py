"""Provider selection and fallback for informational Free Fire data."""
from __future__ import annotations

from typing import Any
from providers.base import PublicDataProvider


class ProviderUnavailable(RuntimeError):
    """Raised when no configured provider can serve a request."""


class ProviderRegistry:
    def __init__(self, providers: list[PublicDataProvider] | None = None):
        self._providers = list(providers or [])

    def register(self, provider: PublicDataProvider) -> None:
        if provider not in self._providers:
            self._providers.append(provider)

    def names(self) -> list[str]:
        return [str(getattr(provider, "name", "unknown")) for provider in self._providers]

    def call(self, method: str, *args: Any, **kwargs: Any) -> tuple[Any, str]:
        errors: list[str] = []
        for provider in self._providers:
            operation = getattr(provider, method, None)
            if not callable(operation):
                continue
            try:
                result = operation(*args, **kwargs)
                if result is not None:
                    return result, str(getattr(provider, "name", "unknown"))
                errors.append(f"{getattr(provider, 'name', 'unknown')}: empty result")
            except (NotImplementedError, TimeoutError, ConnectionError, ValueError) as exc:
                errors.append(f"{getattr(provider, 'name', 'unknown')}: {type(exc).__name__}")
        raise ProviderUnavailable("No configured provider returned data" + (f" ({'; '.join(errors)})" if errors else ""))
