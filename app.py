#!/usr/bin/env python3
"""
Acclime EuroTrack AI - Backend Application
FastAPI Server providing:
- Full CRUD & query endpoints for 80 European Companies SQLite DB
- Natural Language "Just Ask" Query Engine (translates free-form prompts into SQL & AI insights)
- Dynamic Temporary Question Generator by Context
- Email Outreach Drafter
- Static Asset Serving
"""

import hashlib
import json
import os
import re
import sqlite3
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Auto-load .env file if present
env_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(env_file):
    with open(env_file, "r") as ef:
        for eline in ef:
            eline = eline.strip()
            if eline and not eline.startswith("#") and "=" in eline:
                ek, ev = eline.split("=", 1)
                os.environ.setdefault(ek.strip(), ev.strip())
DB_PATH = os.path.join(BASE_DIR, "euro_companies.db")
JSON_PATH = os.path.join(BASE_DIR, "euro_companies.json")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI(
    title="Acclime EuroTrack AI",
    description="80-Company European Engagement & Question Intelligence Dashboard",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ----------------- PYDANTIC MODELS -----------------

class NLQueryRequest(BaseModel):
    query: str

class UpdateStatusRequest(BaseModel):
    status: str

class AddQuestionRequest(BaseModel):
    question: str

class QuestionContextRequest(BaseModel):
    context: str  # "Post-Last-Year Re-engagement", "15-Min Check-in Call", "India Market Entry & Tax", "M&A / JV Exploration"

class EmailDraftRequest(BaseModel):
    company_id: str
    selected_questions: List[str]
    context: Optional[str] = "Post-Last-Year Re-engagement"
    analyst_name: Optional[str] = "Arjun Mehta"
    analyst_title: Optional[str] = "Director - European Inward Investment, Acclime India"

# ----------------- CORE DATA HELPERS -----------------

def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    d = dict(row)
    d["met_last_year"] = bool(d["met_last_year"])
    try:
        d["potential_temporary_questions"] = json.loads(d["potential_temporary_questions"])
    except Exception:
        d["potential_temporary_questions"] = []
    d["key_contact"] = {
        "name": d.pop("key_contact_name", ""),
        "role": d.pop("key_contact_role", ""),
        "email": d.pop("key_contact_email", "")
    }
    return d

# ----------------- NATURAL LANGUAGE QUERY ENGINE -----------------

def parse_and_execute_nl_query(query_text: str) -> Dict[str, Any]:
    """
    Parses natural language queries such as:
      - "Which companies did I meet last year?"
      - "Which German chemical companies did I meet last year?"
      - "Show me the companies I didn't meet last year with revenue over €100M"
      - "What are the potential temporary questions for the companies I met in Q4 last year?"
      - "Top unmet cleantech companies in Sweden or Denmark"
      - "Companies with urgent follow up due"
    Translates into SQL, executes safely, and generates analytical insights.
    """
    q_lower = query_text.lower().strip()
    
    where_clauses = []
    params = []
    insights = []
    
    # 1. Met Last Year detection
    if any(phrase in q_lower for phrase in ["did i meet", "did we meet", "companies i met", "met last year", "we met in", "already met", "met in 2025"]):
        if any(neg in q_lower for phrase in ["did i meet", "did we meet", "companies i met", "met last year"] for neg in ["didn't", "did not", "not meet", "never met", "haven't met", "unmet"]):
            where_clauses.append("met_last_year = 0")
            insights.append("Filtered for companies **NOT met last year**.")
        else:
            where_clauses.append("met_last_year = 1")
            insights.append("Filtered for companies **MET last year (2025)**.")
    elif any(phrase in q_lower for phrase in ["didn't meet", "did not meet", "unmet", "not met", "haven't met", "never met", "not yet met"]):
        where_clauses.append("met_last_year = 0")
        insights.append("Filtered for target companies **NOT met yet**.")
    
    # 2. Country detection
    country_map = {
        "germany": "Germany", "german": "Germany",
        "uk": "UK", "united kingdom": "UK", "british": "UK", "britain": "UK",
        "france": "France", "french": "France",
        "netherlands": "Netherlands", "dutch": "Netherlands", "holland": "Netherlands",
        "switzerland": "Switzerland", "swiss": "Switzerland",
        "sweden": "Sweden", "swedish": "Sweden",
        "italy": "Italy", "italian": "Italy",
        "spain": "Spain", "spanish": "Spain",
        "belgium": "Belgium", "belgian": "Belgium",
        "denmark": "Denmark", "danish": "Denmark"
    }
    
    detected_countries = set()
    for word, ctry in country_map.items():
        if re.search(r'\b' + re.escape(word) + r'\b', q_lower):
            detected_countries.add(ctry)
            
    if detected_countries:
        placeholders = ",".join("?" for _ in detected_countries)
        # Check country prefix
        where_clauses.append(f"({' OR '.join(['country LIKE ?' for _ in detected_countries])})")
        for c in detected_countries:
            params.append(f"{c}%")
        insights.append(f"Geographic focus: **{', '.join(sorted(detected_countries))}**.")

    # 3. Sector detection
    sector_map = {
        "chemical": "Specialty Chemicals",
        "chemicals": "Specialty Chemicals",
        "automotive": "Automotive",
        "auto": "Automotive",
        "car": "Automotive",
        "ev": "Automotive",
        "manufacturing": "Industrial Manufacturing",
        "industrial": "Industrial Manufacturing",
        "machining": "Industrial Manufacturing",
        "medtech": "MedTech",
        "medical": "MedTech",
        "health": "MedTech",
        "cleantech": "Cleantech",
        "clean": "Cleantech",
        "solar": "Cleantech",
        "wind": "Cleantech",
        "energy": "Cleantech",
        "saas": "SaaS",
        "software": "SaaS",
        "tech": "SaaS",
        "cloud": "SaaS"
    }
    
    detected_sectors = set()
    for kw, sec in sector_map.items():
        if re.search(r'\b' + re.escape(kw) + r'\b', q_lower):
            detected_sectors.add(sec)
            
    if detected_sectors:
        where_clauses.append(f"sector IN ({','.join(['?' for _ in detected_sectors])})")
        params.extend(list(detected_sectors))
        insights.append(f"Industry verticals: **{', '.join(sorted(detected_sectors))}**.")

    # 4. Status detection
    if "follow-up" in q_lower or "follow up" in q_lower or "urgent" in q_lower or "pending" in q_lower:
        where_clauses.append("current_status LIKE '%Follow-up Due%'")
        insights.append("Identified accounts with **Follow-up Due**.")
    elif "pipeline" in q_lower or "active" in q_lower:
        where_clauses.append("current_status LIKE '%Active Pipeline%'")
        insights.append("Focused on **Active Pipeline** accounts.")
    elif "paused" in q_lower or "pause" in q_lower:
        where_clauses.append("current_status LIKE '%Paused%'")
        insights.append("Filtered for accounts currently **Paused**.")
    elif "high priority" in q_lower or "top" in q_lower or "priority" in q_lower:
        if "met_last_year = 0" in " ".join(where_clauses):
            where_clauses.append("current_status LIKE '%High Priority%'")
            insights.append("Targeting **High Priority Unmet** companies.")
    elif "cold" in q_lower:
        where_clauses.append("current_status LIKE '%Cold%'")
        insights.append("Filtered for **Cold** target tier.")

    # 5. Revenue threshold detection
    rev_over = re.search(r'(?:over|above|greater than|>)\s*(?:€|eur)?\s*(\d+)', q_lower)
    rev_under = re.search(r'(?:under|below|less than|<)\s*(?:€|eur)?\s*(\d+)', q_lower)
    if rev_over:
        val = float(rev_over.group(1))
        where_clauses.append("revenue_eur_m >= ?")
        params.append(val)
        insights.append(f"Annual revenue **≥ €{int(val)}M**.")
    if rev_under:
        val = float(rev_under.group(1))
        where_clauses.append("revenue_eur_m <= ?")
        params.append(val)
        insights.append(f"Annual revenue **≤ €{int(val)}M**.")

    # 6. Meeting Quarter / Date detection
    if "q1" in q_lower:
        where_clauses.append("meeting_date_last_year BETWEEN '2025-01-01' AND '2025-03-31'")
        insights.append("Meetings held in **Q1 2025**.")
    elif "q2" in q_lower:
        where_clauses.append("meeting_date_last_year BETWEEN '2025-04-01' AND '2025-06-30'")
        insights.append("Meetings held in **Q2 2025**.")
    elif "q3" in q_lower:
        where_clauses.append("meeting_date_last_year BETWEEN '2025-07-01' AND '2025-09-30'")
        insights.append("Meetings held in **Q3 2025**.")
    elif "q4" in q_lower:
        where_clauses.append("meeting_date_last_year BETWEEN '2025-10-01' AND '2025-12-31'")
        insights.append("Meetings held in **Q4 2025**.")

    # 7. Check if user is asking for temporary questions specifically
    wants_questions = any(k in q_lower for k in ["question", "questions", "ask", "outreach", "talking points"])

    # Build SQL
    sql = "SELECT * FROM companies"
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    
    # Ordering
    if "top 5" in q_lower or "top five" in q_lower:
        sql += " ORDER BY revenue_eur_m DESC LIMIT 5"
        insights.append("Sorted by revenue, limited to **Top 5**.")
    elif "revenue" in q_lower and ("high" in q_lower or "largest" in q_lower or "biggest" in q_lower):
        sql += " ORDER BY revenue_eur_m DESC"
    else:
        sql += " ORDER BY met_last_year DESC, revenue_eur_m DESC"

    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    results = [row_to_dict(r) for r in rows]
    conn.close()

    # Formulate executive AI summary answer
    count = len(results)
    if count == 0:
        ai_summary = f"No companies matched the criteria in your query: '{query_text}'. Try broadening your search or clearing specific filters."
    else:
        met_in_res = sum(1 for r in results if r["met_last_year"])
        unmet_in_res = count - met_in_res
        total_rev = sum(r["revenue_eur_m"] for r in results)
        
        # Collect sample temporary questions if requested or helpful
        sample_questions = []
        for r in results[:3]:
            if r["potential_temporary_questions"]:
                sample_questions.append({
                    "company": r["company_name"],
                    "question": r["potential_temporary_questions"][0]
                })

        summary_parts = [
            f"**Found {count} European {'companies' if count != 1 else 'company'}** representing **€{int(total_rev):,}M** in combined annual turnover."
        ]
        
        if met_in_res > 0 and unmet_in_res > 0:
            summary_parts.append(f"Includes **{met_in_res} companies met last year** and **{unmet_in_res} target companies not yet met**.")
        elif met_in_res > 0:
            summary_parts.append(f"All **{met_in_res} companies were met in 2025**, with specific discussion history and tailored follow-up triggers.")
        else:
            summary_parts.append(f"All **{unmet_in_res} companies are unmet targets** with high-fit strategic rationales for Acclime India expansion.")

        if insights:
            summary_parts.append(" | ".join(insights))

        # Add strategic recommendation
        if any("Follow-up Due" in r["current_status"] for r in results):
            followup_due = sum(1 for r in results if "Follow-up Due" in r["current_status"])
            summary_parts.append(f"⚠️ **Action Required**: {followup_due} companies have urgent follow-up milestones pending from their 2025 meetings.")
        
        ai_summary = "\n\n".join(summary_parts)

    return {
        "query": query_text,
        "sql_executed": sql,
        "sql_params": params,
        "count": count,
        "ai_summary": ai_summary,
        "wants_questions": wants_questions,
        "companies": results
    }

# ----------------- DYNAMIC QUESTION GENERATOR -----------------

def generate_contextual_questions(company: Dict[str, Any], context: str) -> List[Dict[str, str]]:
    """
    Generates 4 time-sensitive, situational questions tailored to:
      1. Whether company was met last year or not
      2. The selected strategic context:
         - 'Post-Last-Year Re-engagement'
         - '15-Min Check-in Call'
         - 'India Market Entry & Tax'
         - 'M&A / JV Exploration'
    """
    met = company["met_last_year"]
    name = company["company_name"]
    sector = company["sector"]
    country = company["country"].split(" ")[0]
    date = company.get("meeting_date_last_year") or "last year"
    contact_name = company.get("key_contact", {}).get("name", "Executive")
    notes = company.get("last_year_discussion_summary", "")

    questions = []

    if context == "Post-Last-Year Re-engagement":
        if met:
            questions = [
                {
                    "question": f"When we sat down on {date}, you paused India entity setup due to EU capex tightening—how are 2026 corporate allocations progressing for APAC?",
                    "tag": "Timeline & Capex",
                    "reasoning": f"Directly links to the specific roadblock discussed during our {date} meeting."
                },
                {
                    "question": f"Have your technical and operations directors finalized the site evaluation between Gujarat and Maharashtra that we benchmarked?",
                    "tag": "Site Selection",
                    "reasoning": "Re-opens the location advisory thread Acclime provided last year."
                },
                {
                    "question": f"Given the ongoing European energy cost adjustments, has your board re-visited the cost arbitrage of an Indian manufacturing or technical hub?",
                    "tag": "Cost Arbitrage",
                    "reasoning": "Highlights current macroeconomic pressures driving European capex to India."
                },
                {
                    "question": f"Would you like Acclime India to refresh our regulatory roadmap and corporate incorporation timeline for an H1 2026 entity incorporation?",
                    "tag": "Acclime Next Steps",
                    "reasoning": "Actionable closing question offering immediate advisory assistance."
                }
            ]
        else:
            questions = [
                {
                    "question": f"Are rising European energy levies and CBAM compliance pressure accelerating {name}'s evaluation of an Indian manufacturing or sourcing base?",
                    "tag": "De-risking & CBAM",
                    "reasoning": "Taps into European regulatory pressure to open high-level strategic dialogue."
                },
                {
                    "question": f"How is {name} addressing the China+1 mandate for {sector.lower()} supplies across the Asia-Pacific corridor?",
                    "tag": "Supply Chain Diversification",
                    "reasoning": "Positions Acclime India as a solution to supply chain concentration risks."
                },
                {
                    "question": f"Have you evaluated the state-level capital subsidies and industrial corridors (e.g. Dahej, Chakan, Sriperumbudur) tailored for {sector}?",
                    "tag": "Incentives & Subsidies",
                    "reasoning": "Demonstrates specific sector knowledge and financial incentives."
                },
                {
                    "question": f"Could we arrange a concise 20-minute executive briefing on foreign direct investment (FDI) pathways into India with Acclime's leadership team?",
                    "tag": "Discovery Meeting",
                    "reasoning": "Low-friction call to action for the analyst to secure a first meeting."
                }
            ]

    elif context == "15-Min Check-in Call":
        if met:
            questions = [
                {
                    "question": f"Since our {date} meeting, what has changed internally regarding {name}'s international footprint and expansion priorities?",
                    "tag": "Executive Priority",
                    "reasoning": "Fast pulse check to uncover new board directives."
                },
                {
                    "question": f"Is the transfer pricing and corporate structure we reviewed last year still the preferred model, or has your tax team suggested revisions?",
                    "tag": "Tax & Structure",
                    "reasoning": "Follows up on the governance structure discussed in 2025."
                },
                {
                    "question": f"Are your European customers pushing for faster APAC turnaround times that a local Indian entity could immediately solve?",
                    "tag": "Commercial Demand",
                    "reasoning": "Connects client customer demand to India operational footprint."
                },
                {
                    "question": f"What is the single biggest hurdle preventing your board from approving the India market entry in the upcoming quarter?",
                    "tag": "Bottleneck Resolution",
                    "reasoning": "Direct question allowing Acclime to propose targeted solutions."
                }
            ]
        else:
            questions = [
                {
                    "question": f"In 15 minutes, could we share how comparable {country} companies in {sector} are structuring their Indian operating entities to save 30%+ in operating costs?",
                    "tag": "Peer Benchmarking",
                    "reasoning": "Powerful peer benchmarking angle that sparks executive curiosity."
                },
                {
                    "question": f"What is your current distribution or sales model for Indian clients, and are you losing margin to third-party intermediaries?",
                    "tag": "Margin Optimization",
                    "reasoning": "Uncovers pain points around local distributor margins and control."
                },
                {
                    "question": f"Are you aware of India's updated 2026 fast-track corporate incorporation channels that allow entity setup within 14 business days?",
                    "tag": "Speed to Market",
                    "reasoning": "Dispels legacy myths about bureaucratic delays in India."
                },
                {
                    "question": f"If we could provide a turnkey solution covering nominee directors, compliance, and payroll, would that make an India footprint viable for {name}?",
                    "tag": "Acclime Turnkey Value",
                    "reasoning": "Directly presents Acclime's core corporate services value proposition."
                }
            ]

    elif context == "India Market Entry & Tax":
        questions = [
            {
                "question": f"How is {name} planning to leverage India's concessional 15% corporate tax rate window for new manufacturing and technical entities?",
                "tag": "Section 115BAB Tax Window",
                "reasoning": "Highly relevant fiscal incentive for European CFOs and tax directors."
            },
            {
                "question": f"Have you structured your cross-border IP licensing and management fees to optimize withholding tax under the {country}-India DTAA treaty?",
                "tag": "DTAA & Withholding Tax",
                "reasoning": "Demonstrates sophisticated cross-border tax advisory capabilities."
            },
            {
                "question": f"Will your Indian entity be set up as a Wholly Owned Subsidiary (WOS), a branch office, or an Employer of Record (EOR) structure initially?",
                "tag": "Entity Architecture",
                "reasoning": "Core Acclime structuring choice that determines speed and legal liability."
            },
            {
                "question": f"Do you require Acclime to provide local resident directorship and registered office compliance to satisfy Ministry of Corporate Affairs rules?",
                "tag": "Statutory Governance",
                "reasoning": "Critical legal requirement for foreign entities entering India."
            }
        ]

    elif context == "M&A / JV Exploration":
        questions = [
            {
                "question": f"Would {name} prefer acquiring a majority stake in an existing Indian mid-market player or forging a strategic 51/49 joint venture?",
                "tag": "M&A vs Greenfield",
                "reasoning": "Explores inorganic growth pathways versus greenfield investment."
            },
            {
                "question": f"What specific deadlock resolution, drag-along, and IP reversion clauses does your legal counsel require in an Indian joint venture agreement?",
                "tag": "JV Legal Safeguards",
                "reasoning": "Addresses European investors' primary fear regarding IP loss in foreign JVs."
            },
            {
                "question": f"Can Acclime assist in conducting independent financial, tax, and environmental due diligence on prospective Indian acquisition targets?",
                "tag": "Target Due Diligence",
                "reasoning": "Introduces Acclime's transaction advisory and audit support."
            },
            {
                "question": f"How do you plan to satisfy Indian foreign exchange management regulations (FEMA) regarding pricing guidelines on cross-border share transfers?",
                "tag": "FEMA Regulatory Compliance",
                "reasoning": "Essential Reserve Bank of India valuation and capital control compliance."
            }
        ]

    return questions

# ----------------- API ROUTES -----------------

@app.get("/api/kpi")
def get_kpi_metrics():
    """Returns top KPI statistics for dashboard cards"""
    conn = get_db()
    cur = conn.cursor()
    
    total = cur.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
    met_last_year = cur.execute("SELECT COUNT(*) FROM companies WHERE met_last_year = 1").fetchone()[0]
    not_met = cur.execute("SELECT COUNT(*) FROM companies WHERE met_last_year = 0").fetchone()[0]
    followup_due = cur.execute("SELECT COUNT(*) FROM companies WHERE current_status = 'Met Last Year - Follow-up Due'").fetchone()[0]
    active_pipeline = cur.execute("SELECT COUNT(*) FROM companies WHERE current_status = 'Met Last Year - Active Pipeline'").fetchone()[0]
    paused = cur.execute("SELECT COUNT(*) FROM companies WHERE current_status = 'Met Last Year - Paused'").fetchone()[0]
    unmet_high = cur.execute("SELECT COUNT(*) FROM companies WHERE current_status = 'Not Met - High Priority'").fetchone()[0]
    unmet_cold = cur.execute("SELECT COUNT(*) FROM companies WHERE current_status = 'Not Met - Cold'").fetchone()[0]
    
    total_rev = cur.execute("SELECT SUM(revenue_eur_m) FROM companies").fetchone()[0]
    met_rev = cur.execute("SELECT SUM(revenue_eur_m) FROM companies WHERE met_last_year = 1").fetchone()[0]
    
    conn.close()
    
    return {
        "total_companies": total,
        "met_last_year": met_last_year,
        "not_met_yet": not_met,
        "followup_due": followup_due,
        "active_pipeline": active_pipeline,
        "paused": paused,
        "unmet_high_priority": unmet_high,
        "unmet_cold": unmet_cold,
        "total_revenue_eur_m": round(total_rev, 1),
        "met_revenue_eur_m": round(met_rev, 1)
    }

@app.get("/api/companies")
def get_companies(
    met_last_year: Optional[bool] = None,
    country: Optional[str] = None,
    sector: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "id",
    sort_order: Optional[str] = "asc"
):
    """Retrieve companies with optional filtering and sorting"""
    conn = get_db()
    cur = conn.cursor()
    
    where = []
    params = []
    
    if met_last_year is not None:
        where.append("met_last_year = ?")
        params.append(1 if met_last_year else 0)
        
    if country and country != "All":
        where.append("country LIKE ?")
        params.append(f"{country}%")
        
    if sector and sector != "All":
        where.append("sector = ?")
        params.append(sector)
        
    if status and status != "All":
        where.append("current_status = ?")
        params.append(status)
        
    if search:
        search_like = f"%{search.strip()}%"
        where.append("(company_name LIKE ? OR country LIKE ? OR sector LIKE ? OR last_year_discussion_summary LIKE ? OR key_contact_name LIKE ?)")
        params.extend([search_like, search_like, search_like, search_like, search_like])
        
    sql = "SELECT * FROM companies"
    if where:
        sql += " WHERE " + " AND ".join(where)
        
    allowed_sorts = {
        "id": "id",
        "company_name": "company_name",
        "revenue_eur_m": "revenue_eur_m",
        "meeting_date_last_year": "meeting_date_last_year",
        "country": "country",
        "sector": "sector"
    }
    sort_col = allowed_sorts.get(sort_by, "id")
    order = "DESC" if sort_order.lower() == "desc" else "ASC"
    
    if sort_col == "meeting_date_last_year":
        # Keep non-null dates on top if requested
        sql += f" ORDER BY {sort_col} IS NULL, {sort_col} {order}"
    else:
        sql += f" ORDER BY {sort_col} {order}"
        
    cur.execute(sql, params)
    rows = cur.fetchall()
    companies = [row_to_dict(r) for r in rows]
    conn.close()
    
    return {
        "count": len(companies),
        "companies": companies
    }

@app.get("/api/companies/{company_id}")
def get_company(company_id: str):
    """Get single company details"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies WHERE id = ? OR company_name LIKE ?", (company_id, f"%{company_id}%"))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Company not found")
        
    return row_to_dict(row)

@app.post("/api/companies/{company_id}/questions")
def get_questions_for_company(company_id: str, req: QuestionContextRequest):
    """Generates 4 temporary questions customized by strategic context"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies WHERE id = ?", (company_id,))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Company not found")
        
    company = row_to_dict(row)
    questions = generate_contextual_questions(company, req.context)
    
    return {
        "company_id": company["id"],
        "company_name": company["company_name"],
        "context": req.context,
        "questions": questions
    }

@app.patch("/api/companies/{company_id}/status")
def update_company_status(company_id: str, req: UpdateStatusRequest):
    """Update current engagement status"""
    allowed_statuses = [
        "Met Last Year - Follow-up Due",
        "Met Last Year - Active Pipeline",
        "Met Last Year - Paused",
        "Not Met - High Priority",
        "Not Met - Cold"
    ]
    if req.status not in allowed_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {allowed_statuses}")
        
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE companies SET current_status = ? WHERE id = ?", (req.status, company_id))
    conn.commit()
    conn.close()
    
    return {"success": True, "id": company_id, "new_status": req.status}

@app.post("/api/companies/{company_id}/custom-question")
def add_custom_question(company_id: str, req: AddQuestionRequest):
    """Add a temporary question to company's list"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT potential_temporary_questions FROM companies WHERE id = ?", (company_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")
        
    try:
        q_list = json.loads(row[0])
    except Exception:
        q_list = []
        
    q_list.append(req.question.strip())
    cur.execute("UPDATE companies SET potential_temporary_questions = ? WHERE id = ?", (json.dumps(q_list), company_id))
    conn.commit()
    conn.close()
    
    return {"success": True, "questions": q_list}

@app.post("/api/ask")
def natural_language_ask(req: NLQueryRequest):
    """Primary Natural Language 'Just Ask' query endpoint"""
    return parse_and_execute_nl_query(req.query)

@app.post("/api/draft-email")
def draft_email_outreach(req: EmailDraftRequest):
    """Generates an executive outreach email with questions embedded"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies WHERE id = ?", (req.company_id,))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Company not found")
        
    company = row_to_dict(row)
    contact = company["key_contact"]
    first_name = contact["name"].split(" ")[-1] if " " in contact["name"] else contact["name"]
    salutation = f"Dear {contact['name'].split(' ')[0]} {contact['name'].split(' ')[-1]}" if "Dr." in contact["name"] else f"Dear {contact['name'].split(' ')[0]}"
    
    if company["met_last_year"]:
        subject = f"Acclime India Strategic Briefing: Following up on our {company['meeting_date_last_year']} meeting — {company['company_name']}"
        opener = (
            f"I hope this message finds you well. It was a pleasure meeting you last year on {company['meeting_date_last_year']} "
            f"to discuss {company['company_name']}'s Asia-Pacific trajectory and India operational roadmap.\n\n"
            f"As we enter this quarter, European market dynamics and Indian industrial corridor developments have evolved significantly. "
            f"Following up on our discussion regarding {company['last_year_discussion_summary'].split('.')[1] if '.' in company['last_year_discussion_summary'] else 'your planned India presence'}, "
            f"I wanted to share a few timely considerations our strategy team has prepared for your board:"
        )
    else:
        subject = f"Acclime India Strategic Introduction: Market Entry & Sourcing Advisory for {company['company_name']}"
        opener = (
            f"I hope this note finds you well. I lead European Inward Investment at Acclime India. "
            f"We have been following {company['company_name']}'s impressive leadership in {company['sector']} across {company['country'].split(' ')[0]}.\n\n"
            f"With European energy pressures and supply chain diversification (China+1) driving renewed executive interest in India, "
            f"we identified a compelling strategic alignment with your expansion roadmap. Specifically, our advisory practice has put together "
            f"a few timely questions regarding your APAC positioning:"
        )

    formatted_questions = "\n".join([f"  {idx+1}. {q}" for idx, q in enumerate(req.selected_questions)])

    body = f"""{salutation},

{opener}

{formatted_questions}

Acclime India acts as a seamless operating partner for over 450 multinational corporations—handling turnkey company incorporation, regulatory clearances, Section 115BAB corporate tax structuring, and resident directorship.

Would you be open to a concise 15-minute briefing next week to explore these points?

Warm regards,

{req.analyst_name}
{req.analyst_title}
Acclime Corporate Services (India) Private Limited
Direct: +91 22 6828 9100 | Mobile: +91 98200 48210
arjun.mehta@acclime.com | www.acclime.com
"""

    return {
        "to_email": contact["email"],
        "to_name": contact["name"],
        "subject": subject,
        "body": body
    }

@app.get("/api/chart-data")
def get_chart_breakdowns():
    """Returns analytics datasets for Chart.js / ApexCharts"""
    conn = get_db()
    cur = conn.cursor()
    
    # By Country
    cur.execute("""
    SELECT 
        substr(country, 1, instr(country, ' (') - 1) AS cty,
        SUM(CASE WHEN met_last_year = 1 THEN 1 ELSE 0 END) AS met,
        SUM(CASE WHEN met_last_year = 0 THEN 1 ELSE 0 END) AS unmet,
        COUNT(*) AS total
    FROM companies
    GROUP BY cty
    ORDER BY total DESC
    """)
    country_rows = cur.fetchall()
    
    # By Sector
    cur.execute("""
    SELECT 
        sector,
        SUM(CASE WHEN met_last_year = 1 THEN 1 ELSE 0 END) AS met,
        SUM(CASE WHEN met_last_year = 0 THEN 1 ELSE 0 END) AS unmet,
        COUNT(*) AS total
    FROM companies
    GROUP BY sector
    ORDER BY total DESC
    """)
    sector_rows = cur.fetchall()
    
    # By Current Status
    cur.execute("""
    SELECT current_status, COUNT(*) AS count
    FROM companies
    GROUP BY current_status
    ORDER BY count DESC
    """)
    status_rows = cur.fetchall()

    conn.close()
    
    return {
        "countries": [
            {"country": r["cty"], "met": r["met"], "unmet": r["unmet"], "total": r["total"]}
            for r in country_rows
        ],
        "sectors": [
            {"sector": r["sector"], "met": r["met"], "unmet": r["unmet"], "total": r["total"]}
            for r in sector_rows
        ],
        "statuses": [
            {"status": r["current_status"], "count": r["count"]}
            for r in status_rows
        ]
    }

# ----------------- REALISTIC TTS ENGINE -----------------

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "alloy"  # alloy, echo, fable, onyx, nova, shimmer
    api_key: Optional[str] = None

@app.post("/api/tts")
def generate_tts(req: TTSRequest):
    """
    Generates human-quality MP3 voice narration via OpenAI TTS API.
    Caches generated MP3 files locally to avoid redundant charges.
    """
    api_key = req.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return JSONResponse(
            status_code=400,
            content={
                "error": "OPENAI_API_KEY_REQUIRED",
                "message": "OpenAI API Key required (starts with 'sk-'). You can set OPENAI_API_KEY in environment or pass in request."
            }
        )
    
    # Cache audio locally by hash of text + voice
    text_hash = hashlib.md5(f"{req.voice}:{req.text}".encode()).hexdigest()
    cache_dir = os.path.join(BASE_DIR, "audio_cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"{text_hash}.mp3")
    
    if os.path.isfile(cache_path):
        return FileResponse(cache_path, media_type="audio/mpeg")
    
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "model": "tts-1",
        "input": req.text,
        "voice": req.voice or "alloy"
    }).encode("utf-8")
    
    try:
        request = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(request, timeout=30) as response:
            audio_bytes = response.read()
            with open(cache_path, "wb") as f:
                f.write(audio_bytes)
        return FileResponse(cache_path, media_type="audio/mpeg")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        return JSONResponse(status_code=e.code, content={"error": "OPENAI_API_ERROR", "details": err_body})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ----------------- STATIC ASSET SERVING -----------------

if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/favicon.ico")
def serve_favicon():
    favicon_file = os.path.join(STATIC_DIR, "favicon.svg")
    if os.path.isfile(favicon_file):
        return FileResponse(favicon_file, media_type="image/svg+xml")
    return JSONResponse(status_code=204, content={})

@app.get("/")
def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.isfile(index_file):
        return FileResponse(index_file)
    return HTMLResponse("<h1>Acclime EuroTrack AI Server Running</h1><p>Static index.html not found yet.</p>")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
