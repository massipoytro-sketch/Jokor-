# Jokor Backend

Flask backend for the Jokor platform. The codebase is intentionally modular so data providers can change without rewriting the API.

## Service map

- `api/` — HTTP API and validation
- `core/` — configuration, regions, cache, request IDs and errors
- `services/player_service.py` — normalized player profiles + TTL cache
- `services/stats_service.py` — BR/CS statistics boundary
- `services/search_service.py` — player search boundary
- `services/guild_service.py` — guild data boundary
- `services/asset_service.py` — item/asset catalog boundary
- `services/analytics_service.py` — player comparison/derived analytics
- `adapters/freefire/` — provider boundary
- `tests/` — API smoke tests

## API surface

- `GET /api/health`
- `GET /api/ready`
- `GET /api/meta`
- `GET /api/regions`
- `GET /api/player/<region>/<uid>`
- `GET /api/player/<region>/<uid>/stats?mode=br|cs`
- `GET /api/player/<region>/<uid>/compare/<other_uid>`
- `GET /api/search/<region>/<keyword>`
- `GET /api/guild/<region>/<guild_id>`
- `GET /api/assets/<item_id>`

## Deployment

Render uses the root `render.yaml`. The backend listens on `$PORT` and is served with Gunicorn.

## Provider rule

The Free Fire adapter is currently a safe boundary. Provider-specific compatibility work must be independently tested and licensed before activation. Jokor must not contain password collection, token theft, authentication bypass, account binding/unbinding, inventory modification, or other account-manipulation functionality.

## Local test

```bash
cd backend
pip install -r requirements.txt
pytest -q
python app.py
```
