<div align="center">

# <font color="#39FF78">🟢 J O K O R</font>

<h2><font color="#9D4EDD">FREE FIRE PLAYER INTELLIGENCE // API // TCP // ANALYTICS</font></h2>

<img src="assets/jokor-neon-loop.svg" alt="Jokor animated neon intelligence banner" width="100%" />

<h3><font color="#39FF78">SCAN • ANALYZE • COMPARE • DISCOVER</font></h3>

<p><font color="#D8B4FE">A modular Free Fire intelligence platform built around providers, analytics, protocol diagnostics and a neon console.</font></p>

<p>
<font color="#39FF78">🟢 PLAYER INTELLIGENCE</font>　<font color="#9D4EDD">🟣 TCP PROTOCOL</font>　<font color="#39FF78">🟢 ANALYTICS</font>　<font color="#9D4EDD">🟣 GAME DATA</font>
</p>

[![JOKOR](https://img.shields.io/badge/JOKOR-39FF78?style=for-the-badge&labelColor=050805)](https://github.com/massipoytro-sketch/Jokor-)
[![TCP](https://img.shields.io/badge/TCP-PROTOCOL-9D4EDD?style=for-the-badge&labelColor=050805)](https://github.com/massipoytro-sketch/Jokor-)
[![Flask](https://img.shields.io/badge/BACKEND-FLASK-39FF78?style=for-the-badge&labelColor=050805)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/FRONTEND-REACT-9D4EDD?style=for-the-badge&labelColor=050805)](https://react.dev/)

</div>

<hr>

<h2><font color="#39FF78">🟢 WHAT IS JOKOR?</font></h2>
<p><font color="#D8B4FE">Jokor is not a one-file API. It is a modular intelligence platform for legitimate player information, statistics, comparisons, guild intelligence, game data and provider-backed services.</font></p>

<pre><font color="#39FF78">                         ┌─────────────────────────┐
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
                         PROVIDERS / TCP / CACHE / API</font></pre>

<h2><font color="#9D4EDD">⚡ JOKOR SERVICE GRID</font></h2>

<h3><font color="#39FF78">PLAYER INTELLIGENCE</font></h3>
<ul>
<li><font color="#39FF78">👤 Full player profile</font></li>
<li><font color="#D8B4FE">⚔️ BR statistics</font></li>
<li><font color="#39FF78">🎯 CS statistics</font></li>
<li><font color="#D8B4FE">📊 Derived K/D, win-rate and headshot metrics</font></li>
<li><font color="#39FF78">🧠 Player Intelligence Scan</font></li>
<li><font color="#D8B4FE">📈 Performance / combat indicators</font></li>
<li><font color="#39FF78">🔎 UID and nickname search architecture</font></li>
<li><font color="#D8B4FE">⚖️ Player vs Player comparison</font></li>
<li><font color="#39FF78">🧩 Profile completeness</font></li>
<li><font color="#D8B4FE">🏆 Rank / level / likes fields when supplied by the provider</font></li>
<li><font color="#39FF78">📜 History architecture for rank and activity data</font></li>
</ul>

<h3><font color="#9D4EDD">🏰 GUILD INTELLIGENCE</font></h3>
<ul>
<li><font color="#39FF78">Guild profile</font></li>
<li><font color="#D8B4FE">Guild members</font></li>
<li><font color="#39FF78">Member statistics</font></li>
<li><font color="#D8B4FE">Guild statistics</font></li>
<li><font color="#39FF78">Guild comparison foundation</font></li>
<li><font color="#D8B4FE">Provider-backed guild expansion</font></li>
</ul>

<h3><font color="#39FF78">🧬 GAME DATA</font></h3>
<ul>
<li><font color="#39FF78">Regions</font></li><li><font color="#D8B4FE">Modes</font></li><li><font color="#39FF78">Ranks</font></li><li><font color="#D8B4FE">Seasons</font></li><li><font color="#39FF78">Weapons</font></li><li><font color="#D8B4FE">Characters</font></li><li><font color="#39FF78">Pets</font></li><li><font color="#D8B4FE">Cosmetics</font></li><li><font color="#39FF78">Vehicles</font></li><li><font color="#D8B4FE">Assets / item lookup</font></li>
</ul>

<h3><font color="#9D4EDD">🧠 ANALYTICS ENGINE</font></h3>
<ul>
<li><font color="#39FF78">Win-rate calculations</font></li><li><font color="#D8B4FE">K/D calculations</font></li><li><font color="#39FF78">Headshot percentage</font></li><li><font color="#D8B4FE">Match-volume analysis</font></li><li><font color="#39FF78">Comparison deltas</font></li><li><font color="#D8B4FE">Performance indicators</font></li><li><font color="#39FF78">Profile completeness</font></li><li><font color="#D8B4FE">Future trend/history calculations when real history is available</font></li>
</ul>

<h2><font color="#39FF78">🟢 TCP / PROTOCOL LAYER</font></h2>
<p><font color="#D8B4FE">Jokor contains a separate protocol layer inspired by research of the public <code>Freefire-TCP-BOT</code> project. That project describes TCP communication, custom headers, emote automation and session caching.</font></p>
<p><font color="#39FF78">Jokor does not copy its credential/session automation. Instead, the safe protocol layer provides:</font></p>

<table>
<tr><th><font color="#39FF78">Service</font></th><th><font color="#9D4EDD">Status</font></th></tr>
<tr><td><font color="#D8B4FE">TCP transport probe</font></td><td><font color="#39FF78">🟢 Ready</font></td></tr>
<tr><td><font color="#D8B4FE">Length-prefixed frame inspection</font></td><td><font color="#39FF78">🟢 Ready</font></td></tr>
<tr><td><font color="#D8B4FE">Bounded hexadecimal payload preview</font></td><td><font color="#39FF78">🟢 Ready</font></td></tr>
<tr><td><font color="#D8B4FE">Protocol capability discovery</font></td><td><font color="#39FF78">🟢 Ready</font></td></tr>
<tr><td><font color="#D8B4FE">Emote metadata architecture</font></td><td><font color="#9D4EDD">🟣 Provider-ready</font></td></tr>
<tr><td><font color="#D8B4FE">Protocol metadata architecture</font></td><td><font color="#9D4EDD">🟣 Provider-ready</font></td></tr>
<tr><td><font color="#D8B4FE">Live protocol data</font></td><td><font color="#D8B4FE">🟡 Provider-dependent</font></td></tr>
</table>

<h3><font color="#9D4EDD">TCP API</font></h3>
<pre><font color="#39FF78">GET  /api/protocol/tcp/capabilities
POST /api/protocol/tcp/inspect</font></pre>
<p><font color="#D8B4FE">The inspector accepts a bounded Base64 frame and returns only diagnostic information such as frame length, remaining bytes and a bounded hexadecimal preview.</font></p>
<p><font color="#39FF78">It intentionally does not accept passwords, session tokens, cookies or account credentials, and it does not implement account mutations or spam automation.</font></p>

<h2><font color="#9D4EDD">🌌 SERVICES FROM THE JOKOR ECOSYSTEM</font></h2>
<pre><font color="#D8B4FE">PLAYER
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
 └─ Metrics</font></pre>

<h2><font color="#39FF78">🔌 PROVIDER ARCHITECTURE</font></h2>
<pre><font color="#39FF78">                         JOKOR API
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
                           CACHE</font></pre>
<p><font color="#D8B4FE">This makes Jokor extensible: a new real provider can be connected without rebuilding the entire API.</font></p>

<h2><font color="#39FF78">🚀 API SURFACE</font></h2>
<h3><font color="#9D4EDD">CORE</font></h3>
<pre><font color="#D8B4FE">GET  /api/meta
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
POST /api/tools/derive-stats</font></pre>

<h3><font color="#39FF78">CATALOG</font></h3>
<pre><font color="#9D4EDD">GET /api/catalog
GET /api/catalog/regions
GET /api/catalog/modes
GET /api/catalog/ranks
GET /api/catalog/categories
GET /api/catalog/seasons
GET /api/weapons
GET /api/characters
GET /api/pets
GET /api/cosmetics
GET /api/vehicles</font></pre>

<h3><font color="#9D4EDD">PLATFORM / PROTOCOL</font></h3>
<pre><font color="#39FF78">GET  /api/services
GET  /api/services/{service_id}
GET  /api/service-status
GET  /api/capabilities
GET  /api/account-links/types
GET  /api/account-links/{region}/{uid}
GET  /api/protocol/tcp/capabilities
POST /api/protocol/tcp/inspect
GET  /api/system/metrics
GET  /api/system/health-detail</font></pre>
<p><font color="#D8B4FE">Live endpoints depend on a configured provider. Jokor keeps provider-dependent capabilities explicit instead of pretending static data is live.</font></p>

<h2><font color="#9D4EDD">🧪 REFERENCE PROJECTS &amp; DIFFERENCE</font></h2>
<p><font color="#D8B4FE">The public <code>siambhau/FreeFireApi</code> currently advertises 34 endpoints across 19 groups, including player info, JWT, ban check, guild tools, friends, wallet, login history, wishlist and more.</font></p>
<p><font color="#39FF78">The public <code>Freefire-TCP-BOT</code> describes TCP communication, custom headers, emote automation and session caching.</font></p>
<p><font color="#D8B4FE"><strong>Jokor's approach is different:</strong> it combines useful architectural ideas into a provider-based platform with analytics, normalization, service discovery, protocol diagnostics, frontend console architecture and explicit capability states.</font></p>

<h2><font color="#39FF78">🛡️ SECURITY BOUNDARY</font></h2>
<pre><font color="#39FF78">ALLOWED / SAFE
├─ Public player information
├─ Statistics and analytics
├─ Comparisons
├─ Game catalog metadata
├─ Provider health / diagnostics
├─ Generic TCP frame inspection
└─ Official/provider-backed integrations

<font color="#9D4EDD">NOT IMPLEMENTED
├─ Password collection
├─ Credential theft
├─ Session-token theft
├─ Authentication bypass
├─ Account takeover
├─ Unauthorized account binding/unbinding
├─ Inventory/account mutation
└─ Spam / abusive automation</font></font></pre>

<h2><font color="#9D4EDD">📁 PROJECT STRUCTURE</font></h2>
<pre><font color="#D8B4FE">Jokor-/
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
└── README.md</font></pre>

<h2><font color="#39FF78">📊 DEVELOPMENT STATUS</font></h2>
<table>
<tr><th><font color="#39FF78">Component</font></th><th><font color="#9D4EDD">State</font></th></tr>
<tr><td><font color="#D8B4FE">Core API</font></td><td><font color="#39FF78">🟢 Active</font></td></tr>
<tr><td><font color="#D8B4FE">Player intelligence</font></td><td><font color="#39FF78">🟢 Active</font></td></tr>
<tr><td><font color="#D8B4FE">Stats / analytics</font></td><td><font color="#39FF78">🟢 Active</font></td></tr>
<tr><td><font color="#D8B4FE">Search / guild</font></td><td><font color="#39FF78">🟢 Active</font></td></tr>
<tr><td><font color="#D8B4FE">Catalog</font></td><td><font color="#39FF78">🟢 Active</font></td></tr>
<tr><td><font color="#D8B4FE">Provider registry</font></td><td><font color="#39FF78">🟢 Active</font></td></tr>
<tr><td><font color="#D8B4FE">Cache / rate limit</font></td><td><font color="#39FF78">🟢 Active</font></td></tr>
<tr><td><font color="#D8B4FE">TCP diagnostics</font></td><td><font color="#39FF78">🟢 Active</font></td></tr>
<tr><td><font color="#D8B4FE">Frontend console</font></td><td><font color="#D8B4FE">🟡 Expanding</font></td></tr>
<tr><td><font color="#D8B4FE">Live provider coverage</font></td><td><font color="#D8B4FE">🟡 Provider-dependent</font></td></tr>
<tr><td><font color="#D8B4FE">Rank/activity history</font></td><td><font color="#9D4EDD">🟣 Provider-dependent</font></td></tr>
<tr><td><font color="#D8B4FE">Live leaderboards</font></td><td><font color="#9D4EDD">🟣 Provider-dependent</font></td></tr>
<tr><td><font color="#D8B4FE">OpenAPI explorer</font></td><td><font color="#9D4EDD">🟣 Planned</font></td></tr>
</table>

<h2><font color="#9D4EDD">🗺️ ROADMAP</font></h2>
<h3><font color="#39FF78">PHASE 1 — CORE</font></h3>
<ul><li><font color="#39FF78">[x] Modular Flask backend</font></li><li><font color="#D8B4FE">[x] Player service</font></li><li><font color="#39FF78">[x] BR / CS statistics</font></li><li><font color="#D8B4FE">[x] Search abstraction</font></li><li><font color="#39FF78">[x] Guild abstraction</font></li><li><font color="#D8B4FE">[x] Analytics engine</font></li><li><font color="#39FF78">[x] Cache / rate limit</font></li><li><font color="#D8B4FE">[x] Health / readiness</font></li></ul>

<h3><font color="#9D4EDD">PHASE 2 — INTELLIGENCE</font></h3>
<ul><li><font color="#39FF78">[x] Player Intelligence Scan</font></li><li><font color="#D8B4FE">[x] Player comparison</font></li><li><font color="#39FF78">[x] Service registry</font></li><li><font color="#D8B4FE">[x] Catalog foundation</font></li><li><font color="#9D4EDD">[ ] Advanced history</font></li><li><font color="#9D4EDD">[ ] Rank history</font></li><li><font color="#9D4EDD">[ ] Trend engine</font></li><li><font color="#9D4EDD">[ ] Advanced guild analytics</font></li></ul>

<h3><font color="#39FF78">PHASE 3 — TCP / PROVIDERS</font></h3>
<ul><li><font color="#39FF78">[x] TCP transport architecture</font></li><li><font color="#D8B4FE">[x] Safe frame inspection</font></li><li><font color="#39FF78">[x] Protocol capability discovery</font></li><li><font color="#9D4EDD">[ ] Real provider-backed protocol data</font></li><li><font color="#9D4EDD">[ ] Emote metadata provider</font></li><li><font color="#9D4EDD">[ ] Multiple live providers</font></li><li><font color="#9D4EDD">[ ] Automatic provider fallback expansion</font></li></ul>

<h3><font color="#9D4EDD">PHASE 4 — JOKOR CONSOLE</font></h3>
<ul><li><font color="#9D4EDD">[ ] Full player scanner</font></li><li><font color="#9D4EDD">[ ] Intelligence dashboard</font></li><li><font color="#9D4EDD">[ ] Compare workspace</font></li><li><font color="#9D4EDD">[ ] Guild intelligence dashboard</font></li><li><font color="#9D4EDD">[ ] Game-data browser</font></li><li><font color="#9D4EDD">[ ] API explorer</font></li><li><font color="#9D4EDD">[ ] System monitoring console</font></li><li><font color="#9D4EDD">[ ] Advanced visual analytics</font></li></ul>

<h2><font color="#39FF78">💚🟣 DESIGN</font></h2>
<p><font color="#D8B4FE">Jokor uses a black + ion green + electric purple identity.</font></p>
<pre><font color="#39FF78">ION GREEN       #39FF78</font>
<font color="#9D4EDD">ELECTRIC PURPLE #9D4EDD</font>
<font color="#39FF78">DEEP BLACK      #050805</font>
<font color="#D8B4FE">PURPLE LIGHT    #D8B4FE</font></pre>
<ul><li><font color="#39FF78">🟢 Neon green intelligence panels</font></li><li><font color="#9D4EDD">🟣 Purple accent systems</font></li><li><font color="#39FF78">⚡ Animated neon banner</font></li><li><font color="#9D4EDD">🌐 Grid / scanline atmosphere</font></li><li><font color="#39FF78">🃏 Jokor identity</font></li><li><font color="#9D4EDD">📡 Protocol-console styling</font></li><li><font color="#39FF78">📊 Dense analytics dashboards</font></li><li><font color="#9D4EDD">📱 Responsive interface</font></li></ul>

<h2><font color="#9D4EDD">☠️ JOKOR TERMINAL</font></h2>
<pre><font color="#39FF78">&gt; INITIALIZING JOKOR CORE...
&gt; PROVIDER REGISTRY ............. ONLINE
&gt; PLAYER INTELLIGENCE ........... ONLINE
&gt; ANALYTICS ENGINE .............. ONLINE
&gt; TCP DIAGNOSTICS ............... ONLINE
&gt; CATALOG SYSTEM ................ ONLINE
&gt; CACHE LAYER ................... ONLINE
&gt; RATE LIMITER .................. ONLINE
&gt; HEALTH MONITOR ................ ONLINE
&gt;
&gt; STATUS: READY
&gt; MODE: INTELLIGENCE
&gt; COLOR: GREEN // PURPLE</font></pre>

<h2><font color="#39FF78">🚀 DEPLOYMENT</font></h2>
<p><font color="#D8B4FE">The backend is prepared for deployment on <strong>Render</strong> after repository verification and CI completion.</font></p>
<pre><font color="#9D4EDD">GitHub
  ↓
Jokor backend + frontend
  ↓
CI verification
  ↓
Render
  ↓
Jokor API + Console</font></pre>
<p><font color="#39FF78">📘 backend/README.md</font><br><font color="#9D4EDD">📘 backend/DEPLOY_RENDER.md</font></p>

<hr>
<div align="center">
<img src="assets/jokor-neon-loop.svg" alt="Jokor animated neon footer" width="90%" />
<h1><font color="#39FF78">🃏 JOKOR</font></h1>
<h3><font color="#9D4EDD">GREEN // PURPLE // INTELLIGENCE // TCP // API</font></h3>
<p><font color="#D8B4FE">Built as a modular Free Fire intelligence platform.</font></p>
</div>