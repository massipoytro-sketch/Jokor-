# Jokor

Advanced Free Fire public-information platform.

Jokor is designed as a modular service rather than a single script. The repository separates the HTTP API, data adapters, normalization, caching, rate limiting, analytics, health monitoring and future frontend integration.

## Current scope

- Public player/profile information
- Player statistics and derived metrics
- Region discovery and validation
- Search abstraction
- Guild/profile data abstraction
- Item/asset lookup abstraction
- Comparison and analytics layer
- Response caching and rate limiting
- Health/readiness/status endpoints
- Structured errors and request IDs
- Render-ready Python backend

## Architecture

```text
Client / Frontend
       |
       v
Jokor HTTP API
       |
       +--> validation / request-id / rate-limit
       |
       +--> services
       |      +--> player
       |      +--> stats
       |      +--> search
       |      +--> guild
       |      +--> assets
       |      +--> analytics
       |
       +--> adapters
              +--> Free Fire public-data adapter
              +--> future providers

cache / observability / configuration sit underneath the service layer.
```

## Safety and source policy

Jokor is limited to legitimate public/informational data. It must not implement password collection, token theft, authentication bypass, account binding/unbinding, inventory modification, or other account-manipulation features.

Public repositories may be used as architectural references, but code is only reused when its license permits it. External protocols and schemas are isolated behind adapters so the rest of Jokor does not depend on one provider.

## Backend

The backend lives in `backend/` and is intended for Render. See `backend/README.md` for the service map and deployment notes.
