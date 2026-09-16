<div align="center">

# 🃏 JOKOR

### FREE FIRE PLAYER INTELLIGENCE PLATFORM

**Scan. Analyze. Compare. Understand.**

[![Jokor API](https://img.shields.io/badge/JOKOR-ION%20GREEN-39ff78?style=for-the-badge&labelColor=050805)](https://github.com/massipoytro-sketch/Jokor-)
[![Backend](https://img.shields.io/badge/BACKEND-Flask-111111?style=for-the-badge&logo=flask)](https://github.com/massipoytro-sketch/Jokor-)
[![Python](https://img.shields.io/badge/PYTHON-3.x-111111?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/LICENSE-SEE%20REPO-111111?style=for-the-badge)](LICENSE)

> **Jokor is an intelligence-style platform for legitimate Free Fire public information, player analytics, comparisons, game data and provider-backed services.**

</div>

---

<div align="center">

```text
       ███████╗ ██████╗ ██╗  ██╗ ██████╗ ██████╗
       ╚══███╔╝██╔═══██╗██║ ██╔╝██╔═══██╗██╔══██╗
          ███╔╝ ██║   ██║█████╔╝ ██║   ██║██████╔╝
         ███╔╝  ██║   ██║██╔═██╗ ██║   ██║██╔══██╗
        ███████╗╚██████╔╝██║  ██╗╚██████╔╝██║  ██║
        ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
```

**JOKOR // PLAYER INTELLIGENCE // API // ANALYTICS // DATA**

</div>

## 🟢 What is Jokor?

Jokor is being built as a **large modular Free Fire intelligence platform**, not a single API script.

The goal is to bring player lookup, statistics, comparison, guild intelligence, game catalogs, analytics, provider integrations and operational monitoring into one organized system.

```text
                    ┌─────────────────────┐
                    │       JOKOR         │
                    │  PLAYER INTEL CORE  │
                    └──────────┬──────────┘
                               │
       ┌───────────────────────┼────────────────────────┐
       │                       │                        │
   PLAYER INTEL           GAME DATA                ANALYTICS
       │                       │                        │
   Profiles                 Weapons                 K/D
   BR / CS Stats            Characters              Win Rate
   Search                   Pets                    Headshots
   Guilds                   Cosmetics               Comparisons
   Compare                  Vehicles                Trends
       │                       │                        │
       └───────────────────────┼────────────────────────┘
                               │
                    PROVIDERS / CACHE / API
```

## ☠️ Service Map

### PLAYER INTELLIGENCE

- 👤 Full player profile
- ⚔️ Battle Royale statistics
- 🎯 Clash Squad statistics
- 📈 Derived performance metrics
- 💀 K/D analysis
- 🎯 Headshot-rate analysis
- 🏆 Rank and level information
- ❤️ Likes / social profile fields when provided
- 🧩 Profile completeness
- 🔍 Player search
- ⚖️ Player vs Player comparison

### 🏰 GUILD INTELLIGENCE

- Guild profile
- Guild members
- Guild statistics
- Member statistics
- Guild search abstraction
- Guild comparison foundation

### 🧠 ANALYTICS ENGINE

- Win-rate calculations
- K/D calculations
- Headshot percentage
- Match-volume analysis
- Performance indicators
- Comparison deltas
- Profile completeness
- Future trend/history analysis when real history data is available

### 🗃️ GAME DATA CATALOG

- Regions
- Modes
- Ranks
- Seasons
- Weapons
- Characters
- Pets
- Cosmetics
- Vehicles
- Assets / item lookup

### 🌐 API & INFRASTRUCTURE

- Modular Flask API
- Provider registry
- Provider fallback architecture
- Response cache
- Rate limiting
- Request IDs
- Input validation
- Structured errors
- Health checks
- Readiness checks
- Metrics
- Service capabilities
- Versioned API foundation

### 🔌 PROVIDER-DEPENDENT SERVICES

The architecture reserves dedicated service slots for capabilities such as:

- Ban status
- Friends
- Login history
- Wishlist
- Wallet information
- Dynamic Duo
- Live leaderboards
- Inventory
- Player history

These are exposed only when a real provider can supply the data. **Jokor never pretends static data is live data.**

---

## 🧪 Current API Surface

Core endpoints include:

```text
GET  /api/meta
GET  /api/health
GET  /api/ready
GET  /api/regions
GET  /api/game-info
GET  /api/player/{region}/{uid}
GET  /api/player/{region}/{uid}/stats
GET  /api/player/{region}/{uid}/compare/{other_uid}
GET  /api/search/{region}/{keyword}
GET  /api/guild/{region}/{guild_id}
GET  /api/assets/{item_id}
POST /api/tools/derive-stats
```

Catalog and platform endpoints:

```text
GET /api/catalog
GET /api/catalog/regions
GET /api/catalog/modes
GET /api/catalog/ranks
GET /api/catalog/categories
GET /api/catalog/seasons
GET /api/weapons
GET /api/characters
GET /api/pets
GET /api/cosmetics
GET /api/vehicles
GET /api/service-status
GET /api/capabilities
```

> Endpoint availability depends on the configured provider. Static catalog endpoints are intentionally separated from live player data.

---

## 🧬 Architecture

```text
                         CLIENT / FRONTEND
                                │
                                ▼
                         ┌─────────────┐
                         │ JOKOR API   │
                         └──────┬──────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
        VALIDATION          SERVICES           METRICS
        REQUEST ID          PLAYER             HEALTH
        RATE LIMIT          STATS              READY
              │             SEARCH             CACHE
              │             GUILD
              │             ANALYTICS
              │             CATALOG
              │
              └────────────────┬────────────────┘
                               ▼
                       PROVIDER REGISTRY
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
              Provider A    Provider B    Provider C
                 │             │             │
                 └─────────────┼─────────────┘
                               ▼
                         NORMALIZATION
                               │
                               ▼
                             CACHE
```

This separation lets Jokor add providers without rewriting the whole API.

---

## 🟩 Project Structure

```text
Jokor-/
├── backend/
│   ├── api/
│   │   ├── routes.py
│   │   └── extended_routes.py
│   ├── services/
│   │   ├── player_service.py
│   │   ├── stats_service.py
│   │   ├── search_service.py
│   │   ├── guild_service.py
│   │   ├── asset_service.py
│   │   ├── analytics_service.py
│   │   ├── statistics.py
│   │   ├── game_info.py
│   │   ├── provider_service.py
│   │   └── catalog_service.py
│   ├── adapters/
│   │   └── freefire/
│   ├── providers/
│   ├── models/
│   ├── core/
│   ├── tests/
│   └── app.py
│
├── frontend/
│   └── React / Vite interface
│
└── README.md
```

---

## 🃏 Design Language

Jokor uses an **ion-green + black intelligence-console aesthetic**:

- `#39ff78` ion green
- Deep black surfaces
- Neon borders and glow
- Scanline / grid atmosphere
- Tactical dashboards
- Cyberpunk-inspired status panels
- Clear data visualization
- Responsive mobile interface

The visual direction is inspired by the **Jokor identity**, while the software architecture is built independently.

---

## ⚡ Development Status

| Area | Status |
|---|---|
| Core API | 🟢 Active |
| Player service | 🟢 Active |
| Stats & analytics | 🟢 Active |
| Search | 🟢 Active |
| Guild abstraction | 🟢 Active |
| Catalog foundation | 🟢 Active |
| Provider architecture | 🟢 Active |
| Cache / rate limit | 🟢 Active |
| Frontend | 🟡 Expanding |
| Live provider coverage | 🟡 Provider-dependent |
| Advanced history | 🟡 Planned |
| Live leaderboards | 🟡 Provider-dependent |

Jokor is an evolving platform. Features are marked according to whether they are implemented, being expanded, or require a real external provider.

---

## 🛡️ Data & Safety Policy

Jokor is intended for legitimate informational and analytical use.

The project does **not** implement:

- Password collection
- Credential theft
- Token theft
- Authentication bypass
- Account takeover
- Unauthorized account binding/unbinding
- Inventory modification
- Other account-manipulation operations

Public repositories may be used as architectural references. Code is reused only where licensing permits it, and external provider protocols are isolated behind adapters.

---

## 🚀 Roadmap

### Phase 1 — Core

- [x] Modular backend
- [x] Player service
- [x] Statistics
- [x] Search abstraction
- [x] Guild abstraction
- [x] Analytics
- [x] Cache / rate limit
- [x] Health / readiness

### Phase 2 — Intelligence Expansion

- [x] Catalog foundation
- [x] Player comparison
- [x] Service capability registry
- [ ] Advanced player history
- [ ] Rank history
- [ ] Trend engine
- [ ] Advanced guild analytics

### Phase 3 — Provider Expansion

- [ ] Multiple live providers
- [ ] Automatic provider fallback
- [ ] Ban-status provider
- [ ] Friends provider
- [ ] Login-history provider
- [ ] Wishlist provider
- [ ] Inventory provider
- [ ] Live leaderboard provider

### Phase 4 — JOKOR Console

- [ ] Full player scanner
- [ ] Player intelligence dashboard
- [ ] Compare workspace
- [ ] Guild intelligence dashboard
- [ ] Game-data browser
- [ ] API explorer
- [ ] System monitoring console
- [ ] Advanced visual analytics

---

## 🔧 Backend

The backend lives in `backend/` and is designed for deployment on Render.

See [`backend/README.md`](backend/README.md) and [`backend/DEPLOY_RENDER.md`](backend/DEPLOY_RENDER.md) for backend details.

---

## ⭐ Why Jokor?

```text
NOT JUST AN API.

A modular intelligence layer.
A growing service ecosystem.
A provider-independent architecture.
A serious Free Fire data console.

JOKOR IS BUILT TO SCALE.
```

<div align="center">

### 🃏 JOKOR
**ION GREEN // BLACK // INTELLIGENCE**

</div>
