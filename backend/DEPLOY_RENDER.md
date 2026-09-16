# Jokor Backend — Render Deployment Guide

This document describes the Flask backend deployment path and what must be verified before treating the API as production-ready.

## Current scope

Jokor is structured as a public Free Fire information and analysis API. Its intended modules include player profiles, ranked statistics, search, guild information, asset metadata, derived statistics, caching, request IDs, rate limiting, health checks, and provider abstraction.

**Important:** profile/statistics endpoints require a working, permitted upstream data provider. The built-in FreeFire client is a boundary/placeholder; a successful Render deployment alone does not mean live player data is available. Do not publish fabricated player records as real results.

## Render setup

Create a **Web Service** connected to `massipoytro-sketch/Jokor-` and select the `main` branch.

- Root Directory: `backend`
- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
- Health Check Path: `/health` (confirm this path in `app.py`; use the exact implemented route if it differs)

Use the free instance if available for the account/region. Free instances may sleep when idle, so the first request can be slow.

## Environment variables

Set only values actually supported by `backend/core/config.py` and `backend/.env.example`. Never commit provider credentials or private tokens. If no live provider is configured, leave provider configuration unset and expect data endpoints to report a clear unavailable/not-configured response.

## Deploy checklist

1. Confirm the repository root contains `backend/app.py` and `backend/requirements.txt`.
2. Confirm `gunicorn` is included in `requirements.txt`.
3. Confirm the app binds to the Render-provided `PORT`.
4. Confirm the configured health path returns HTTP 200 without requiring an upstream provider.
5. Run the test suite from `backend` with `python -m pytest` before deployment.
6. After deployment, check the Render logs and call the health endpoint.
7. Test one invalid UID/region and one data lookup; verify errors are structured and do not leak secrets.

## API discovery

Use the routes actually registered in `backend/api/routes.py` as the source of truth. Expected areas include player lookup, derived-stat tools, service health, readiness, supported regions, and metrics where enabled. Do not assume an endpoint exists based only on this guide.

## Frontend integration

Configure the website's backend base URL as the deployed Render service URL. Keep the URL in frontend environment configuration (for example, a Vite `VITE_API_BASE_URL` variable), not hard-coded across components. The frontend should display distinct states for loading, invalid input, no public data, provider unavailable, and server error.

## Readiness status

This guide is documentation, not a deployment or test report. Verify the repository's current imports, tests, health route, and provider configuration before using the backend for a public launch.