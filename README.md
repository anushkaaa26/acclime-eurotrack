<div align="center">

# 🌍 Acclime EuroTrack AI
### 80-Company European Engagement & Question Intelligence Platform

[![Render Deployment](https://img.shields.io/badge/Render-Live%20Deployed-00E599?logo=render&logoColor=white&style=for-the-badge)](https://acclime-eurotrack.onrender.com)
[![Video Tour](https://img.shields.io/badge/Video%20Tour-Interactive%20Walkthrough-FF0000?logo=youtube&logoColor=white&style=for-the-badge)](https://acclime-eurotrack.onrender.com/tour)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github&logoColor=white&style=for-the-badge)](https://github.com/anushkaaa26/acclime-eurotrack)

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLite3](https://img.shields.io/badge/Database-SQLite%203-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![MCP](https://img.shields.io/badge/Protocol-Model%20Context%20Protocol%20(MCP)-7C3AED)](https://modelcontextprotocol.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![Voice](https://img.shields.io/badge/AI%20Voice-Jenny%20Neural%20HD-0284C7)](https://acclime-eurotrack.onrender.com/tour)

<p align="center">
  <b>A bespoke, production-ready Client Intelligence & Strategic Advisory Web Platform engineered for Acclime India’s Strategy & International Business Practice.</b>
</p>

[🌐 Live Cloud App](https://acclime-eurotrack.onrender.com) • [🎬 Watch Video Tour](https://acclime-eurotrack.onrender.com/tour) • [📦 GitHub Repository](https://github.com/anushkaaa26/acclime-eurotrack) • [🛠️ MCP Setup](#-model-context-protocol-mcp-server)

---

</div>

## 🎬 Interactive Video Tour & Product Walkthrough

EuroTrack AI features a **cinematic, keynote-style interactive video walkthrough** with **Microsoft Jenny Neural HD** studio voice narration.

> 📺 **Watch the Full Interactive Walkthrough Live:**  
> 👉 **[https://acclime-eurotrack.onrender.com/tour](https://acclime-eurotrack.onrender.com/tour)**  
> *(Zero configuration needed — pre-rendered neural voice audio plays with 0ms latency)*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  🔴 🟡 🟢  https://eurotrack.acclime.com/tour                           [Studio Voice] │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   [ SCENE 1 / 8 ]  Executive Portfolio Overview                                        │
│   ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐ ┌────────────────┐ │
│   │ TOTAL PORTFOLIO   │ │ MET IN 2025       │ │ NOT MET YET       │ │ FOLLOW-UP DUE  │ │
│   │ 80 Companies      │ │ 35 Accounts       │ │ 45 Targets        │ │ 18 Urgent ⚡    │ │
│   │ 10 Nations · €14B │ │ Notes on file     │ │ High Priority     │ │ Action Req     │ │
│   └───────────────────┘ └───────────────────┘ └───────────────────┘ └────────────────┘ │
│                                                                                        │
│   🎙️ Voiceover: "Welcome to Acclime EuroTrack AI. At the top of your dashboard are     │
│   four KPI metric cards tracking all eighty European companies..."                     │
│   [ ılılıll AI SPEAKING ]                                  [ ⏮ Prev ] [ ▶ Play ] [ Next ⏭ ] │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Video Tour Chapters:

| # | Chapter Title | Timeline | Voice Narration Topic |
|---|---|---|---|
| **01** | **Executive Portfolio Overview** | `00:00 - 00:20` | High-level portfolio metrics: 80 companies, 35 met in 2025, 45 unmet, 18 urgent follow-ups. |
| **02** | **"Just Ask" AI Command Bar** | `00:20 - 00:40` | English-to-SQL translation in real-time, live SQL query inspection, and 5 quick filter presets. |
| **03** | **Coverage Distribution Analytics** | `00:40 - 01:00` | Stacked country (10 nations) & sector (6 verticals) charts with click-to-filter drilldown. |
| **04** | **Corporate Directory & Views** | `01:00 - 01:20` | Dense Table View vs. Visual Card Grid View, column sorting, search, and status badges. |
| **05** | **Account Dossier & Meeting Memory**| `01:20 - 01:40` | Solves engagement amnesia: verbatim 2025 meeting notes, executive contacts, and live stage updating. |
| **06** | **Potential Temporary Questions** | `01:40 - 02:00` | 4 situation-specific questions dynamically generated across 4 strategic advisory angles. |
| **07** | **1-Click Outreach Email Composer** | `02:00 - 02:20` | Auto-drafts personalized advisory emails pre-populated with questions and `mailto:` launch. |
| **08** | **Model Context Protocol (MCP)** | `02:20 - 02:40` | Connects Claude Desktop and Cursor directly to the SQLite database via JSON-RPC stdio. |

---

## 🏛️ Executive Summary & Strategic Rationale

Acclime India’s Strategy & International Business Practice advises European multinationals on **Inward Foreign Direct Investment (FDI)**, wholly-owned Indian subsidiary setup, regulatory compliance, transfer pricing, and "China+1" supply chain diversification into Indian industrial corridors (Gujarat chemicals, Tamil Nadu electronics, Pune automotive).

Senior advisory teams meet dozens of European executive delegations annually. **EuroTrack AI solves three critical institutional problems:**

1. **The Engagement Amnesia Problem**: Post-meeting momentum is historically lost. If an analyst met a CEO in October 2025 who paused India entry due to European energy costs, following up in 2026 requires instant recall of that exact strategic context.
2. **The Cold Target Discovery Problem**: Unmet targets receive generic outreach. EuroTrack generates tailored, timely questions referencing rising EU capex constraints and Indian cluster readiness.
3. **The Natural Language Querying Need**: Business leaders want to ask plain English questions like *"Which German chemical companies did I meet last year?"* or *"Top 5 unmet cleantech companies above €100M"* without writing SQL.

---

## 📊 The 80-Company European Database

The database is built on a validated relational SQLite engine ([`euro_companies.db`](euro_companies.db)) paired with a JSON fallback ([`euro_companies.json`](euro_companies.json)):

```
Total Portfolio: 80 Companies (€14.3 Billion Combined Turnover)
├── Met in 2025 (35 Companies)
│   ├── Follow-up Due (18)  ──> Action required from 2025 meetings
│   ├── Active Pipeline (11) ──> Subsidiary setup / JV in progress
│   └── Paused (6)           ──> Paused on energy/capex, ready for re-activation
└── Not Met Yet (45 Companies)
    ├── High Priority (28)   ──> Immediate first-touch outreach candidates
    └── Cold (17)            ──> Secondary tier monitoring
```

### 10 European Nations Covered:
- 🇩🇪 **Germany** (14): Munich, Stuttgart, Düsseldorf, Frankfurt, Hamburg, Berlin
- 🇬🇧 **United Kingdom** (11): Oxford, Cambridge, Birmingham, Bristol, London, Manchester
- 🇫🇷 **France** (10): Lyon, Toulouse, Lille, Paris, Rouen, Strasbourg
- 🇳🇱 **Netherlands** (8): Rotterdam, Eindhoven, Delft, Amsterdam, Utrecht
- 🇮🇹 **Italy** (8): Milan, Bologna, Turin, Padua, Florence, Parma
- 🇨🇭 **Switzerland** (7): Basel, Zurich, Geneva, Lucerne, La Chaux-de-Fonds
- 🇸🇪 **Sweden** (7): Stockholm, Gothenburg, Malmö, Västerås, Uppsala
- 🇪🇸 **Spain** (6): Barcelona, Bilbao, Valencia, Madrid, Zaragoza
- 🇧🇪 **Belgium** (4): Antwerp, Ghent, Leuven, Brussels
- 🇩🇰 **Denmark** (4): Copenhagen, Aarhus, Odense, Aalborg

### 6 High-Growth Sectors:
1. **Specialty Chemicals** (18 companies) — Agrochemicals, industrial catalysts, fluoropolymers, fragrance synthesis.
2. **Industrial Manufacturing** (16 companies) — Precision robotics, CNC tooling, semiconductor handling equipment.
3. **Cleantech & Solar** (13 companies) — Hydrogen electrolyzers, solar tracking, flow batteries, carbon capture.
4. **MedTech** (12 companies) — Surgical robotics, point-of-care diagnostics, continuous monitoring devices.
5. **SaaS & Enterprise Tech** (11 companies) — Supply chain visibility, AML fraud detection, digital twin simulation.
6. **Automotive & EV** (10 companies) — EV powertrains, battery thermal management, chassis electronics.

---

## ⚡ Core Application Architecture

```
                               ┌──────────────────────────────────────────────┐
                               │                 Client Layer                 │
                               │  (Browser Web UI / Claude Desktop / Cursor)  │
                               └──────────────────────┬───────────────────────┘
                                                      │
                              ┌───────────────────────┴───────────────────────┐
                              │                                               │
                              ▼                                               ▼
                  ┌───────────────────────┐                       ┌───────────────────────┐
                  │  FastAPI HTTP Server  │                       │   FastMCP / StdIO     │
                  │       (app.py)        │                       │    (mcp_server.py)    │
                  └───────────┬───────────┘                       └───────────┬───────────┘
                              │                                               │
                              ├───────────────────────┬───────────────────────┤
                              ▼                       ▼                       ▼
                  ┌───────────────────────┐ ┌───────────────────┐ ┌───────────────────────┐
                  │ NL Query Regex Engine │ │ Static Files CDN  │ │ SQLite Storage Engine │
                  │  (Entities -> SQL)    │ │  (HTML/CSS/JS)    │ │  (euro_companies.db)  │
                  └───────────────────────┘ └───────────────────┘ └───────────────────────┘
```

---

## 🚀 Key Feature Breakdown

### 1. "Just Ask" Natural Language Command Bar
- Type questions like:
  - *"Which companies did I meet last year?"*
  - *"German chemical companies met last year"*
  - *"Unmet cleantech companies above €100M"*
  - *"Follow-up due Q4 accounts"*
- An entity-extraction parser tokenizes country, sector, revenue constraints, and meeting status.
- Converts to safe, parameterized SQLite queries, updates the entire UI live, and renders an **AI Executive Summary Banner** with executed SQL code.

### 2. Dual-View Corporate Directory
- **Dense Table View:** Instant column sorting by ID, Company Name, Country, Turnover (€M), Meeting Date, and Stage.
- **Card Grid View:** Card-based UI showing key contacts, turnover, and discussion previews.
- **Multi-Filter Bar:** Real-time search by company name, executive contact, or notes, combined with dropdown filters for Country, Sector, and Stage.

### 3. Account Dossier Drawer & Engagement Memory
- **Section 1: Engagement Memory:** Displays exact meeting dates, executive contact name, role, verified email, and detailed verbatim notes from 2025.
- **Live Stage Updating:** Change the pipeline stage directly in the drawer dropdown — updates the SQLite database in real time.

### 4. Potential Temporary Questions Engine
- Automatically generates 4 time-sensitive, situational questions.
- **Dynamic Context Selector:**
  1. *Post-Meeting Re-engagement* (bridges gap from 2025 meeting notes)
  2. *15-Min Check-in Call* (low-friction check-in touchpoint)
  3. *India Market Entry & Tax* (FDI structuring, transfer pricing, entity setup)
  4. *M&A / JV Pathways* (local joint ventures, acquisition targets)
- Custom question input field to append account-specific notes directly to the database.

### 5. 1-Click Outreach Email Composer
- Pre-populates recipient name, email, advisory subject line, and formatted email body containing the situational questions.
- Includes 1-click **"Copy Text"** and **"Open in Mail"** (`mailto:`) for instant client outreach.

---

## 🛠️ Model Context Protocol (MCP) Server

EuroTrack AI ships with a compliant **Model Context Protocol (MCP)** server ([`mcp_server.py`](mcp_server.py)) running over standard I/O (JSON-RPC 2.0).

### Available Tools:

| Tool | Parameters | Description |
|---|---|---|
| `ask_companies_met_last_year` | `country`, `sector`, `met_last_year` | Query the 80 European companies by meeting status, country, or sector. |
| `get_company_details_and_notes` | `company_name` | Retrieve executive contacts, financial turnover, and 2025 meeting notes. |
| `get_potential_temporary_questions`| `company_name`, `context` | Generate 4 situational outreach questions tailored to a specific strategic context. |

### Connect to Claude Desktop:
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "acclime-eurotrack": {
      "command": "python3",
      "args": [
        "/path/to/acclime-eurotrack/mcp_server.py"
      ]
    }
  }
}
```

### Connect to Cursor IDE:
Add to Cursor Settings > **MCP Servers**:
```json
{
  "mcpServers": {
    "acclime-eurotrack": {
      "command": "python3",
      "args": [
        "/path/to/acclime-eurotrack/mcp_server.py"
      ]
    }
  }
}
```

---

## 🏃 Local Quickstart & Development

### 1. Clone & Setup
```bash
git clone https://github.com/anushkaaa26/acclime-eurotrack.git
cd acclime-eurotrack
pip install -r requirements.txt
```

### 2. Verify Database Integrity
```bash
python generate_dataset.py
```
*(Confirms exactly 80 companies, 35 met, 45 unmet, 18 follow-up due)*

### 3. Run Web Server
```bash
uvicorn app:app --host 127.0.0.1 --port 8080 --reload
```
Open **[http://127.0.0.1:8080](http://127.0.0.1:8080)** in your browser.  
Open **[http://127.0.0.1:8080/tour](http://127.0.0.1:8080/tour)** for the cinematic video walkthrough.

### 4. Run with Docker
```bash
docker compose up -d --build
```

---

## 🌐 Cloud Deployment (Render Blueprint)

This repository includes a [`render.yaml`](render.yaml) blueprint:
1. Connect your GitHub fork to [Render Dashboard](https://dashboard.render.com).
2. Select **New Web Service** → Choose `acclime-eurotrack`.
3. Render reads `render.yaml` automatically:
   - **Build Command:** `pip install -r requirements.txt && python generate_dataset.py`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. The service will be live with full SSL in 2 minutes!

---

## 🧪 Verification & Test Suite

Run the full system test suite:
```bash
# Verify MCP protocol stdio
python test_mcp.py

# Verify MCP server self-test
python mcp_server.py --test
```

```
============================================================
ACCLIME EUROTRACK SYSTEM INTEGRITY VERIFICATION
============================================================
✓ Total Companies: 80
✓ Met Last Year (2025): 35 (100% verified)
✓ Not Met Yet: 45 (100% verified)
✓ Met Last Year — Follow-up Due: 18 (100% verified)
✓ Total Portfolio Coverage: €14.3 Billion
✓ Countries: 10 European Nations
✓ Sectors: 6 Priority Verticals
✓ Web API Endpoints: 16 active routes verified (including /tour and /api/tts)
✓ Neural Voice Audio: 8 Studio MP3 Scenes Rendered (Jenny Neural HD)
✓ MCP Protocol stdio test: Passed (Initialize, tools/list, tools/call)
============================================================
```

---

<div align="center">
  <b>Built with ❤️ for Acclime India’s Strategy & International Business Practice</b><br>
  <sub>Designed & Developed by Anushka Dhiman</sub>
</div>
