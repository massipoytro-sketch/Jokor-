# Jokor Backend

Flask API for the Jokor Free Fire player-information platform. The backend is modular: HTTP routes, business services, normalization, caching and provider selection are separated so a validated live data source can be added without redesigning the site.

## Architecture

- `api/` — HTTP routes, validation and response contracts
- `core/` — configuration, regions, cache, request IDs, rate limiting, health and metrics
- `models/` — stable data models
- `services/player_service.py` — profile lookup + TTL cache
- `services/stats_service.py` — BR/CS statistics + derived metrics
- `services/search_service.py` — player search boundary
- `services/guild_service.py` — guild lookup boundary
- `services/analytics_service.py` + `services/compare_engine.py` — comparison and deterministic analytics
- `services/game_info.py` — presentation-ready game/mode/rank/field catalog
- `services/provider_service.py` — centralized provider hub and normalization boundary
- `adapters/freefire/` — provider adapter and payload normalizer
- `providers/` — provider interface and fallback registry
- `tests/` — API, calculation and provider-layer tests

## API surface

### System

- `GET /api/health`
- `GET /api/ready`
- `GET /api/meta`
- `GET /api/system/metrics`
- `GET /api/system/health-detail`

### Game information

- `GET /api/game-info`
- `GET /api/game-info/modes/br`
- `GET /api/game-info/modes/cs`
- `GET /api/regions`
- `GET /api/regions/<region>`

### Player

- `GET /api/player/<region>/<uid>`
- `GET /api/player/<region>/<uid>/stats?mode=br|cs`
- `GET /api/player/<region>/<uid>/compare/<other_uid>`
- `GET /api/search/<region>/<keyword>`

### Guild / assets

- `GET /api/guild/<region>/<guild_id>`
- `GET /api/assets/<item_id>`

### Tools

- `POST /api/tools/derive-stats`

## Data model planned for the website

Jokor is designed to present a player page in sections: identity (UID, nickname, region, level), social (likes and guild), competitive data (rank and points), BR/CS counters, derived rates, profile completeness, and comparison tools. Missing provider fields remain `null`; Jokor never invents live values.

## Provider status

The provider boundary is now centralized and supports fallback ordering. The bundled Free Fire client remains a deliberately empty adapter until a compatible, tested and permitted public-data source is configured. The API therefore runs correctly even when live player data is unavailable and returns a clear `DATA_SOURCE_NOT_CONFIGURED` response.

## Render

The root `render.yaml` uses `backend` as `rootDir`, installs `backend/requirements.txt`, starts Gunicorn with `app:app`, and checks `/api/health`. See `backend/DEPLOY_RENDER.md` before deployment.

## Local test

```bash
cd backend
pip install -r requirements.txt
pytest -q
python app.py
```
