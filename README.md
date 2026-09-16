<div align="center">

# 🟢🟣 J O K O R

## <font color="#39ff78">FREE FIRE PLAYER INTELLIGENCE // API // TCP // ANALYTICS</font>

<img src="assets/jokor-neon-loop.svg" alt="Jokor animated neon intelligence banner" width="100%" />

### <font color="#39ff78">SCAN • ANALYZE • COMPARE • DISCOVER</font>

<font color="#d8b4fe">A modular Free Fire intelligence platform built around providers, analytics, protocol diagnostics and a neon console.</font>

<br/>

[![JOKOR](https://img.shields.io/badge/JOKOR-39FF78?style=for-the-badge&labelColor=050805)](https://github.com/massipoytro-sketch/Jokor-)
[![TCP](https://img.shields.io/badge/TCP-PROTOCOL-9D4EDD?style=for-the-badge&labelColor=050805)](https://github.com/massipoytro-sketch/Jokor-)
[![Flask](https://img.shields.io/badge/BACKEND-FLASK-39FF78?style=for-the-badge&labelColor=050805)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/FRONTEND-REACT-9D4EDD?style=for-the-badge&labelColor=050805)](https://react.dev/)

</div>

---

## <font color="#39ff78">🟢 WHAT IS JOKOR?</font>

<font color="#d8b4fe">Jokor is not a one-file API. It is a modular intelligence platform for legitimate player information, statistics, comparisons, guild intelligence, game data and provider-backed services.</font>

```text
                         ┌─────────────────────────┐
                         │          JOKOR           │
                         │   PLAYER INTELLIGENCE    │
                         └────────────┬────────────┘
                                      │
          ┌───────────────────────────┼──────────────────────────┐
          ▼                           ▼                          ▼
   PLAYER INTEL                 GAME DATA                 ANALYTICS
   Profile / Stats              Ranks / Seasons           K/D / Win Rate
   Search / Guild               Weapons / Characters     Headshots
   Compare / History            Pets / Cosmetics         Trends / Deltas
          │                           │                          │
          └───────────────────────────┼──────────────────────────┘
                                      ▼
                         PROVIDERS / TCP / CACHE / API
```

---

## <font color="#9d4edd">⚡ JOKOR SERVICE GRID</font>

### <font color="#39ff78">PLAYER INTELLIGENCE</font>

- 👤 Full player profile
- ⚔️ BR statistics
- 🎯 CS statistics
- 📊 Derived K/D, win-rate and headshot metrics
- 🧠 Player Intelligence Scan
- 📈 Performance / combat indicators
- 🔎 UID and nickname search architecture
- ⚖️ Player vs Player comparison
- 🧩 Profile completeness
- 🏆 Rank / level / likes fields when supplied by the provider
- 📜 History architecture for rank and activity data

### <font color="#39ff78">🏰 GUILD INTELLIGENCE</font>

- Guild profile
- Guild members
- Member statistics
- Guild statistics
- Guild comparison foundation
- Provider-backed guild expansion

### <font color="#39ff78">🧬 GAME DATA</font>

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

### <font color="#9d4edd">🧠 ANALYTICS ENGINE</font>

- Win-rate calculations
- K/D calculations
- Headshot percentage
- Match-volume analysis
- Comparison deltas
- Performance indicators
- Profile completeness
- Future trend/history calculations when real history is available

---

## <font color="#39ff78">🟢 TCP / PROTOCOL LAYER</font>

Jokor now contains a **separate protocol layer inspired by research of the public `Freefire-TCP-BOT` project**. That project describes TCP communication, custom headers, emote automation and session caching. citeturn0search1

Jokor does **not** copy its credential/session automation. Instead, the safe protocol layer provides:

| Service | Status |
|---|---|
| TCP transport probe | 🟢 Ready |
| Length-prefixed frame inspection | 🟢 Ready |
| Bounded hexadecimal payload preview | 🟢 Ready |
| Protocol capability discovery | 🟢 Ready |
| Emote metadata architecture | 🟣 Provider-ready |
| Protocol metadata architecture | 🟣 Provider-ready |
| Live protocol data | 🟡 Provider-dependent |

### <font color="#9d4edd">TCP API</font>

```text
GET  /api/protocol/tcp/capabilities
POST /api/protocol/tcp/inspect
```

The inspector accepts a bounded Base64 frame and returns only diagnostic information such as frame length, remaining bytes and a bounded hexadecimal preview.

<font color="#d8b4fe">It intentionally does not accept passwords, session tokens, cookies or account credentials, and it does not implement account mutations or spam automation.</font>

---

## <font color="#9d4edd">🌌 SERVICES FROM THE JOKOR ECOSYSTEM</font>

```text
PLAYER
 ├─ Profile
 ├─ BR Stats
 ├─ CS Stats
 ├─ Intelligence Scan
 ├─ Compare
 └─ Search

GUILD
 ├─ Profile
 ├─ Members
 ├─ Statistics
 └─ Intelligence

GAME DATA
 ├─ Regions
 ├─ Ranks
 ├─ Seasons
 ├─ Weapons
 ├─ Characters
 ├─ Pets
 ├─ Cosmetics
 └─ Vehicles

PROTOCOL
 ├─ TCP Probe
 ├─ Frame Inspector
 ├─ Protocol Capabilities
 ├─ Emote Metadata
 └─ Protocol Metadata

INFRASTRUCTURE
 ├─ Provider Registry
 ├─ Fallback
 ├─ Cache
 ├─ Rate Limit
 ├─ Request IDs
 ├─ Health
 ├─ Readiness
 └─ Metrics
```

---

## <font color="#39ff78">🔌 PROVIDER ARCHITECTURE</font>

```text
                         JOKOR API
                             │
                   ┌─────────┴─────────┐
                   │   SERVICE LAYER   │
                   └─────────┬─────────┘
                             │
                    PROVIDER REGISTRY
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
      Provider A         Provider B        TCP Provider
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ▼
                        NORMALIZATION
                             ▼
                           CACHE
```

This makes Jokor extensible: a new real provider can be connected without rebuilding the entire API.

---

## <font color="#39ff78">🚀 API SURFACE</font>

### Core

```text
GET  /api/meta
GET  /api/health
GET  /api/ready
GET  /api/regions
GET  /api/game-info
GET  /api/player/{region}/{uid}
GET  /api/player/{region}/{uid}/stats
GET  /api/player/{region}/{uid}/compare/{other_uid}
GET  /api/player/{region}/{uid}/intelligence
GET  /api/search/{region}/{keyword}
GET  /api/guild/{region}/{guild_id}
GET  /api/assets/{item_id}
POST /api/tools/derive-stats
```

### Catalog

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
```

### Platform / Protocol

```text
GET  /api/services
GET  /api/services/{service_id}
GET  /api/service-status
GET  /api/capabilities
GET  /api/account-links/types
GET  /api/account-links/{region}/{uid}
GET  /api/protocol/tcp/capabilities
POST /api/protocol/tcp/inspect
GET  /api/system/metrics
GET  /api/system/health-detail
```

<font color="#d8b4fe">Live endpoints depend on a configured provider. Jokor keeps provider-dependent capabilities explicit instead of pretending static data is live.</font>

---

## <font color="#9d4edd">🧪 REFERENCE PROJECTS & DIFFERENCE</font>

The public `siambhau/FreeFireApi` currently advertises 34 endpoints across 19 groups, including player info, JWT, ban check, guild tools, friends, wallet, login history, wishlist and more. citeturn0search0

The public `Freefire-TCP-BOT` describes TCP communication, custom headers, emote automation and session caching. citeturn0search1

**Jokor's approach is different:** it combines the useful architectural ideas into a provider-based platform with analytics, normalization, service discovery, protocol diagnostics, frontend console architecture and explicit capability states.

---

## <font color="#39ff78">🛡️ SECURITY BOUNDARY</font>

Jokor is designed for legitimate informational and analytical use.

```text
ALLOWED / SAFE
├─ Public player information
├─ Statistics and analytics
├─ Comparisons
├─ Game catalog metadata
├─ Provider health / diagnostics
├─ Generic TCP frame inspection
└─ Official/provider-backed integrations

NOT IMPLEMENTED
├─ Password collection
├─ Credential theft
├─ Session-token theft
├─ Authentication bypass
├─ Account takeover
├─ Unauthorized account binding/unbinding
├─ Inventory/account mutation
└─ Spam / abusive automation
```

---

## <font color="#9d4edd">📁 PROJECT STRUCTURE</font>

```text
Jokor-/
├── assets/
│   ├── jokor-banner.svg
│   └── jokor-neon-loop.svg
│
├── backend/
│   ├── api/
│   │   ├── routes.py
│   │   └── extended_routes.py
│   ├── services/
│   │   ├── player_service.py
│   │   ├── stats_service.py
│   │   ├── search_service.py
│   │   ├── guild_service.py
│   │   ├── analytics_service.py
│   │   ├── intelligence_service.py
│   │   ├── catalog_service.py
│   │   ├── protocol_service.py
│   │   └── service_registry.py
│   ├── providers/
│   │   └── freefire_tcp/
│   │       ├── client.py
│   │       └── protocol.py
│   ├── adapters/
│   ├── models/
│   ├── core/
│   └── tests/
│
├── frontend/
│   └── React / Vite console
│
└── README.md
```

---

## <font color="#39ff78">📊 DEVELOPMENT STATUS</font>

| Component | State |
|---|---|
| Core API | 🟢 Active |
| Player intelligence | 🟢 Active |
| Stats / analytics | 🟢 Active |
| Search / guild | 🟢 Active |
| Catalog | 🟢 Active |
| Provider registry | 🟢 Active |
| Cache / rate limit | 🟢 Active |
| TCP diagnostics | 🟢 Active |
| Frontend console | 🟡 Expanding |
| Live provider coverage | 🟡 Provider-dependent |
| Rank/activity history | 🟣 Provider-dependent |
| Live leaderboards | 🟣 Provider-dependent |
| OpenAPI explorer | 🟣 Planned |

---

## <font color="#9d4edd">🗺️ ROADMAP</font>

### PHASE 1 — CORE

- [x] Modular Flask backend
- [x] Player service
- [x] BR / CS statistics
- [x] Search abstraction
- [x] Guild abstraction
- [x] Analytics engine
- [x] Cache / rate limit
- [x] Health / readiness

### PHASE 2 — INTELLIGENCE

- [x] Player Intelligence Scan
- [x] Player comparison
- [x] Service registry
- [x] Catalog foundation
- [ ] Advanced history
- [ ] Rank history
- [ ] Trend engine
- [ ] Advanced guild analytics

### PHASE 3 — TCP / PROVIDERS

- [x] TCP transport architecture
- [x] Safe frame inspection
- [x] Protocol capability discovery
- [ ] Real provider-backed protocol data
- [ ] Emote metadata provider
- [ ] Multiple live providers
- [ ] Automatic provider fallback expansion

### PHASE 4 — JOKOR CONSOLE

- [ ] Full player scanner
- [ ] Intelligence dashboard
- [ ] Compare workspace
- [ ] Guild intelligence dashboard
- [ ] Game-data browser
- [ ] API explorer
- [ ] System monitoring console
- [ ] Advanced visual analytics

---

## <font color="#39ff78">💚🟣 DESIGN</font>

Jokor uses a **black + ion green + electric purple** identity:

```text
ION GREEN     #39FF78
ELECTRIC PURPLE #9D4EDD
DEEP BLACK    #050805
PURPLE LIGHT  #D8B4FE
```

Visual language:

- 🟢 Neon green intelligence panels
- 🟣 Purple accent systems
- ⚡ Animated neon banner
- 🌐 Grid / scanline atmosphere
- 🃏 Jokor identity
- 📡 Protocol-console styling
- 📊 Dense analytics dashboards
- 📱 Responsive interface

---

## <font color="#9d4edd">☠️ JOKOR TERMINAL</font>

```text
> INITIALIZING JOKOR CORE...
> PROVIDER REGISTRY ............. ONLINE
> PLAYER INTELLIGENCE ........... ONLINE
> ANALYTICS ENGINE .............. ONLINE
> TCP DIAGNOSTICS ............... ONLINE
> CATALOG SYSTEM ................ ONLINE
> CACHE LAYER ................... ONLINE
> RATE LIMITER .................. ONLINE
> HEALTH MONITOR ................ ONLINE
>
> STATUS: READY
> MODE: INTELLIGENCE
> COLOR: GREEN // PURPLE
```

---

## <font color="#39ff78">🚀 DEPLOYMENT</font>

The backend is prepared for deployment on **Render** after repository verification and CI completion.

```text
GitHub
  ↓
Jokor backend + frontend
  ↓
CI verification
  ↓
Render
  ↓
Jokor API + Console
```

See:

- [`backend/README.md`](backend/README.md)
- [`backend/DEPLOY_RENDER.md`](backend/DEPLOY_RENDER.md)

---

<div align="center">

<img src="assets/jokor-neon-loop.svg" alt="Jokor animated neon footer" width="90%" />

# <font color="#39ff78">🃏 JOKOR</font>

### <font color="#9d4edd">GREEN // PURPLE // INTELLIGENCE // TCP // API</font>

<font color="#d8b4fe">Built as a modular Free Fire intelligence platform.</font>

</div>
