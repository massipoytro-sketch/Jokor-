# Jokor Backend

Flask API foundation for Jokor.

## Architecture

- `api/` — HTTP routes
- `services/` — application logic
- `adapters/freefire/` — external Free Fire data adapter
- `models/` — normalized Jokor data models (to be added)
- `cache/` — response caching (to be added)

The backend is designed to run as a Render Web Service. Secrets and service credentials must be provided through environment variables and must never be committed to Git.

Current scope is informational player/profile/stat data only. Account modification, credential capture, token theft, and authentication bypass are out of scope.
