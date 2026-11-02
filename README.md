# Acclime EuroTrack AI — 80-Company European Engagement & Question Intelligence Dashboard

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139-green.svg)](https://fastapi.tiangolo.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite%203-lightgrey.svg)](https://sqlite.org)
[![MCP](https://img.shields.io/badge/Protocol-Model%20Context%20Protocol%20(MCP)-purple.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/License-Proprietary%20Acclime-navy.svg)](#)

A production-ready European Engagement & Question Intelligence Web Application and Model Context Protocol (MCP) Database built for **Acclime India's Strategy & International Business Team**.

EuroTrack AI manages a curated database of **exactly 80 European companies**, tracks meeting memories from last year (2025) versus unmet targets, provides an AI-powered **"Just Ask" Natural Language Command Bar** with instant SQL translation, visualizes geographic and sectoral breakdowns, and dynamically generates **potential temporary questions** (timely, situational follow-up and discovery questions) customized by strategic context.

---

## 🏛️ Executive Architecture & System Design

```
acclime-eurotrack/
├── euro_companies.db             # Primary SQLite database (80 European companies & indexes)
├── euro_companies.json           # JSON database export & fallback
├── generate_dataset.py           # Reproducible dataset generator with strict validation checks
├── app.py                        # FastAPI REST API, Natural Language Query Engine, & Static Server
├── mcp_server.py                 # Model Context Protocol server (FastMCP + JSON-RPC 2.0 stdio)
├── test_mcp.py                   # MCP protocol testing and verification suite
├── claude_desktop_config.json    # Ready-to-use configuration for Claude Desktop
├── cursor_mcp.json               # Ready-to-use configuration for Cursor IDE
├── static/
│   ├── index.html                # Responsive dashboard with Tailwind CSS, Chart.js & Lucide icons
│   ├── css/styles.css            # Acclime design system, glassy cards, pulsing badges
│   └── js/app.js                 # Frontend application logic, filters, drawer, email composer
└── README.md                     # Comprehensive documentation & deployment guide
```

---

## 📊 1. The 80 European Companies Database (`met_last_year` Core Logic)

EuroTrack AI contains **exactly 80 realistic European corporate records** spanning 10 countries and 6 strategic industry verticals:

| Metric | Target Count | Verified Count | Key Strategic Insight |
| :--- | :--- | :--- | :--- |
| **Total European Database** | `80` | **80** | Balanced across 10 European economies |
| **Companies I Met Last Year (2025)** | `35` | **35** | Exact 2025 meeting dates & detailed discussion notes |
| **Companies Not Met Yet** | `45` | **45** | China+1, energy crisis, and India FDI rationales |
| **Pending Follow-ups from Last Year** | `18` | **18** | Actionable follow-up milestones due |
| **Active Pipeline from Last Year** | `—` | **11** | Entity setup or JV negotiations in flight |
| **Paused from Last Year** | `—` | **6** | Capex or regulatory pauses needing re-activation |
| **Not Met — High Priority Targets** | `—` | **28** | Immediate first-touch outreach candidates |
| **Not Met — Cold Targets** | `—` | **17** | Secondary tier monitoring |

### Geographic Coverage (10 European Nations)
- 🇩🇪 **Germany**: 14 companies (Munich, Stuttgart, Düsseldorf, Frankfurt, Hamburg, Berlin, etc.)
- 🇬🇧 **United Kingdom**: 12 companies (Oxford, Birmingham, Cambridge, Bristol, London, Manchester, etc.)
- 🇫🇷 **France**: 10 companies (Lyon, Rouen, Lille, Toulouse, Paris, Strasbourg, Bordeaux, etc.)
- 🇳🇱 **Netherlands**: 8 companies (Rotterdam, Eindhoven, Delft, Amsterdam, Utrecht, etc.)
- 🇨🇭 **Switzerland**: 7 companies (Basel, Zurich, La Chaux-de-Fonds, Geneva, Lucerne, etc.)
- 🇸🇪 **Sweden**: 7 companies (Stockholm, Gothenburg, Malmö, Västerås, Uppsala, etc.)
- 🇮🇹 **Italy**: 8 companies (Milan, Bologna, Turin, Padua, Florence, Parma, Bergamo, etc.)
- 🇪🇸 **Spain**: 6 companies (Barcelona, Bilbao, Valencia, Madrid, Zaragoza)
- 🇧🇪 **Belgium**: 4 companies (Antwerp, Ghent, Leuven, Brussels)
- 🇩🇰 **Denmark**: 4 companies (Copenhagen, Aarhus, Odense, Aalborg)

### Sector Verticals (6 High-Value Sectors)
1. **Specialty Chemicals** (15 companies) — Agrochemicals, catalysts, fluoropolymers, fragrance synthesis, bio-resins.
2. **Industrial Manufacturing** (17 companies) — Precision robotics, CNC milling, semiconductor handling, hydraulics.
3. **MedTech** (13 companies) — Surgical robotics, point-of-care diagnostics, continuous glucose monitors, dialysis.
4. **Cleantech** (13 companies) — Hydrogen electrolyzers, solar tracking, flow batteries, agrivoltaics, carbon capture.
5. **SaaS** (11 companies) — Supply chain tracking, AML fraud detection, digital twin simulation, grid management.
6. **Automotive** (11 companies) — EV powertrains, battery thermal management, chassis systems, sensor fusion.

---

## ⚡ 2. Core Application Features

### Feature 1: "Just Ask" Natural Language Bar
Located at the top of the dashboard, analysts can query the database using free-form natural language:
- *"Which companies did I meet last year?"*
- *"Which German chemical companies did I meet last year?"*
- *"Show me the companies I didn't meet last year with revenue over €100M"*
- *"What are the potential temporary questions for the companies I met in Q4 last year?"*
- *"Chemical & Manufacturing Companies Met Last Year"*
- *"Generate Temporary Questions for Top 5 Unmet Targets"*

**Under the Hood:**
1. The backend NLP engine parses entities (countries, sectors, revenue limits, quarters, and status).
2. Converts criteria into safe, parameterized SQLite queries.
3. Live-updates the entire dashboard (KPIs, visual tables, and card views).
4. Generates a crisp **Acclime Executive Summary Brief** highlighting revenue impact, follow-up flags, and strategic themes.
5. Displays the exact SQL executed in a collapsible developer accordion.

### Feature 2: Visual Analytics Dashboard ("Which Company / Companies I Met")
- **4 Top KPI Cards:** Direct 1-click drill-downs into Total (80), Met Last Year (35), Not Met (45), and Pending Follow-ups (18).
- **Interactive Country Breakdown Bar Chart:** Stacked comparison of Met vs. Not Met across all 10 countries; clicking any country bar instantly filters the company list.
- **Interactive Sector Breakdown Bar Chart:** Visualizes distribution across all 6 industry verticals; clicking any sector bar filters the directory.
- **Table vs. Card Grid Switcher:** Full spreadsheet view with sortable columns or visual cards with key contact and question previews.

### Feature 3: "Potential Temporary Questions" & Company Drawer
Clicking on any company slides open a comprehensive intelligence drawer:
- **Section A — Meeting Memory:**
  - Met status badge (`✓ Met Last Year` with date, or `○ Unmet Target`).
  - Key contact avatar, name, executive title, and direct email link.
  - Full discussion notes from 2025 or strategic FDI rationale.
  - Live status dropdown (updates SQLite database in real time).
- **Section B — Potential Temporary Questions (Core Deliverable):**
  - Displays 4 time-sensitive, situational questions tailored to the company's status.
  - **Dynamic Context Selector:** Switch between 4 strategic contexts:
    1. `Post-Last-Year Re-engagement`
    2. `15-Min Check-in Call`
    3. `India Market Entry & Tax`
    4. `M&A / JV Exploration`
  - Re-generates tailored questions on the fly when the context changes.
  - Add custom situational questions directly into the database.
  - 1-click copy individual questions or all 4 questions at once.
- **Outreach Email Composer:**
  - One click opens a pre-drafted client email customized with the company's meeting notes and selected temporary questions.
  - Features Acclime India signature block, 1-click "Copy to Clipboard", and "Open in Mail App (`mailto:`)".

### Feature 4: Model Context Protocol (`mcp_server.py`)
EuroTrack AI exposes a compliant **Model Context Protocol (MCP)** server supporting both `FastMCP` and clean standard JSON-RPC 2.0 over `stdio`. AI agents in Claude Desktop, Cursor, and other IDEs can execute 3 specialized tools:
1. `ask_companies_met_last_year(country, sector, met_last_year)`
2. `get_company_details_and_notes(company_name)`
3. `get_potential_temporary_questions(company_name, context)`

---

## 🚀 Quickstart Guide

### 1. Run the Web Application
```bash
cd /Users/anushkadhiman/.gemini/antigravity/scratch/acclime-eurotrack
python3 -m uvicorn app:app --host 127.0.0.1 --port 8080
```
Open **[http://127.0.0.1:8080](http://127.0.0.1:8080)** in your browser.

### 2. Run the MCP Server Self-Test
```bash
python3 mcp_server.py --test
```

### 3. Verify MCP Protocol Handling (JSON-RPC stdio)
```bash
python3 test_mcp.py
```

### 4. Connect to Claude Desktop
Add the following configuration to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "acclime-eurotrack": {
      "command": "python3",
      "args": [
        "/Users/anushkadhiman/.gemini/antigravity/scratch/acclime-eurotrack/mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### 5. Connect to Cursor IDE
Add the snippet in `cursor_mcp.json` to your Cursor Settings > MCP Servers:
```json
{
  "mcpServers": {
    "acclime-eurotrack": {
      "command": "python3",
      "args": [
        "/Users/anushkadhiman/.gemini/antigravity/scratch/acclime-eurotrack/mcp_server.py"
      ]
    }
  }
}
```

---

## 🧪 Verification & Test Results

```
============================================================
ACCLIME EUROTRACK SYSTEM INTEGRITY VERIFICATION
============================================================
✓ Total Companies: 80
✓ Met Last Year (2025): 35 (100% verified)
✓ Not Met Yet: 45 (100% verified)
✓ Met Last Year — Follow-up Due: 18 (100% verified)
✓ Active Pipeline: 11
✓ Paused: 6
✓ Unmet High Priority: 28
✓ Unmet Cold: 17
✓ Countries: 10 (Germany, UK, France, Netherlands, Switzerland, Sweden, Italy, Spain, Belgium, Denmark)
✓ Sectors: 6 (Specialty Chemicals, Industrial Manufacturing, MedTech, Cleantech, SaaS, Automotive)
✓ Web API Endpoints: 15 active routes verified with TestClient
✓ MCP Protocol stdio test: Passed (Initialize, tools/list, tools/call)
============================================================
```

---
*Built with ❤️ for Acclime India Strategy & International Business Advisory.*
