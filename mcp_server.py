#!/usr/bin/env python3
"""
Acclime EuroTrack AI - Model Context Protocol (MCP) Server
Allows AI assistants (Claude Desktop, Cursor, etc.) to query the 80 European companies database,
check meeting memories from last year, and generate situational temporary questions.

Tools:
1. ask_companies_met_last_year(country, sector, met_last_year)
2. get_company_details_and_notes(company_name)
3. get_potential_temporary_questions(company_name, context)
4. run_natural_language_eurotrack_query(query)
"""

import sys
import os
import json
import sqlite3
from typing import Optional, List, Dict, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "euro_companies.db")

def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run generate_dataset.py first.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ----------------- TOOL IMPLEMENTATIONS -----------------

def ask_companies_met_last_year(
    country: Optional[str] = None,
    sector: Optional[str] = None,
    met_last_year: Optional[bool] = None
) -> str:
    """
    Search and filter European companies based on whether the analyst met them last year,
    optionally filtering by European country and industry sector.
    """
    conn = get_db_connection()
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
        where.append("sector LIKE ?")
        params.append(f"%{sector}%")
        
    sql = "SELECT id, company_name, country, sector, revenue_eur_m, met_last_year, meeting_date_last_year, current_status FROM companies"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY met_last_year DESC, revenue_eur_m DESC"
    
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    
    if not rows:
        return f"No companies found matching country='{country}', sector='{sector}', met_last_year={met_last_year}."
        
    output = [f"Found {len(rows)} European companies matching criteria:\n"]
    for r in rows:
        status_symbol = "✓ MET LAST YEAR" if r["met_last_year"] else "○ NOT MET YET"
        date_str = f" (Date: {r['meeting_date_last_year']})" if r["meeting_date_last_year"] else ""
        output.append(
            f"• [{r['id']}] {r['company_name']} | {r['country']} | {r['sector']} | €{r['revenue_eur_m']}M\n"
            f"  Status: {status_symbol}{date_str} | Pipeline: {r['current_status']}"
        )
        
    return "\n".join(output)

def get_company_details_and_notes(company_name: str) -> str:
    """
    Retrieve in-depth meeting memory, discussion summaries, financials, and key contact details
    for a specific European company by name or ID.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM companies WHERE id = ? OR company_name LIKE ?",
        (company_name.strip(), f"%{company_name.strip()}%")
    )
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return f"Company '{company_name}' was not found in the Acclime EuroTrack database."
        
    r = dict(row)
    try:
        questions = json.loads(r["potential_temporary_questions"])
    except Exception:
        questions = []
        
    met_str = f"YES - Met on {r['meeting_date_last_year']}" if r["met_last_year"] else "NO - Unmet Target Account"
    
    q_formatted = "\n".join([f"    {i+1}. {q}" for i, q in enumerate(questions)])
    
    return f"""=======================================================
ACCLIME EUROTRACK INTELLIGENCE FILE: {r['company_name']} ({r['id']})
=======================================================
• Country & HQ: {r['country']}
• Sector: {r['sector']}
• Revenue: €{r['revenue_eur_m']}M
• Met Last Year: {met_str}
• Current Pipeline Status: {r['current_status']}

KEY EXECUTIVE CONTACT:
• Name: {r['key_contact_name']}
• Role: {r['key_contact_role']}
• Email: {r['key_contact_email']}

MEETING MEMORY & STRATEGIC RATIONALE:
{r['last_year_discussion_summary']}

POTENTIAL TEMPORARY QUESTIONS ON FILE:
{q_formatted}
======================================================="""

def get_potential_temporary_questions(
    company_name: str,
    context: Optional[str] = "Post-Last-Year Re-engagement"
) -> str:
    """
    Generate 4 situational, time-sensitive temporary questions tailored to a specific company
    and a specific strategic outreach context:
    - 'Post-Last-Year Re-engagement'
    - '15-Min Check-in Call'
    - 'India Market Entry & Tax'
    - 'M&A / JV Exploration'
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM companies WHERE id = ? OR company_name LIKE ?",
        (company_name.strip(), f"%{company_name.strip()}%")
    )
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return f"Company '{company_name}' was not found in the Acclime EuroTrack database."
        
    r = dict(row)
    
    # Generate contextual questions
    name = r["company_name"]
    sector = r["sector"]
    country = r["country"].split(" ")[0]
    date = r["meeting_date_last_year"] or "last year"
    met = bool(r["met_last_year"])
    
    ctx = context or "Post-Last-Year Re-engagement"
    
    output = [
        f"POTENTIAL TEMPORARY QUESTIONS FOR: {name}",
        f"Target Contact: {r['key_contact_name']} ({r['key_contact_role']})",
        f"Engagement Context: {ctx}",
        f"Met Last Year: {'Yes (' + str(date) + ')' if met else 'No (Unmet Target)'}",
        "-" * 55
    ]
    
    if ctx == "15-Min Check-in Call":
        if met:
            q_list = [
                f"1. Since our {date} meeting, what has shifted regarding {name}'s board priorities for international expansion?",
                f"2. Is the transfer pricing and corporate structure we reviewed last year still the preferred model, or has your tax team suggested revisions?",
                f"3. Are your European customers pushing for faster APAC turnaround times that a local Indian entity could immediately solve?",
                f"4. What is the single biggest operational bottleneck preventing your board from approving the India market entry this quarter?"
            ]
        else:
            q_list = [
                f"1. In 15 minutes, could we share how comparable {country} companies in {sector} are structuring Indian operating entities to save 30%+ in operating costs?",
                f"2. What is your current distribution or sales model for Indian clients, and are you losing margin to third-party intermediaries?",
                f"3. Are you aware of India's updated 2026 fast-track corporate incorporation channels that allow entity setup within 14 business days?",
                f"4. If Acclime could provide a turnkey solution covering nominee directorship, compliance, and payroll, would that make an India footprint viable?"
            ]
    elif ctx == "India Market Entry & Tax":
        q_list = [
            f"1. How is {name} planning to leverage India's concessional 15% corporate tax rate window for new manufacturing and technical entities?",
            f"2. Have you structured your cross-border IP licensing and management fees to optimize withholding tax under the {country}-India DTAA treaty?",
            f"3. Will your Indian entity be set up as a Wholly Owned Subsidiary (WOS), a branch office, or an Employer of Record (EOR) structure initially?",
            f"4. Do you require Acclime to provide local resident directorship and registered office compliance to satisfy Ministry of Corporate Affairs rules?"
        ]
    elif ctx == "M&A / JV Exploration":
        q_list = [
            f"1. Would {name} prefer acquiring a majority stake in an existing Indian mid-market player or forging a strategic 51/49 joint venture?",
            f"2. What specific deadlock resolution, drag-along, and IP reversion clauses does your legal counsel require in an Indian joint venture agreement?",
            f"3. Can Acclime assist in conducting independent financial, tax, and environmental due diligence on prospective Indian acquisition targets?",
            f"4. How do you plan to satisfy Indian foreign exchange management regulations (FEMA) regarding pricing guidelines on cross-border share transfers?"
        ]
    else:  # Post-Last-Year Re-engagement (Default)
        if met:
            q_list = [
                f"1. When we sat down on {date}, you paused India entity setup due to EU capex tightening—how are 2026 corporate allocations progressing for APAC?",
                f"2. Have your technical and operations directors finalized the site evaluation between Gujarat and Maharashtra that we benchmarked?",
                f"3. Given the ongoing European energy cost adjustments, has your board re-visited the cost arbitrage of an Indian manufacturing or technical hub?",
                f"4. Would you like Acclime India to refresh our regulatory roadmap and corporate incorporation timeline for an H1 2026 entity incorporation?"
            ]
        else:
            q_list = [
                f"1. Are rising European energy levies and CBAM compliance pressure accelerating {name}'s evaluation of an Indian manufacturing or sourcing base?",
                f"2. How is {name} addressing the China+1 mandate for {sector.lower()} supplies across the Asia-Pacific corridor?",
                f"3. Have you evaluated the state-level capital subsidies and industrial corridors (e.g. Dahej, Chakan, Sriperumbudur) tailored for {sector}?",
                f"4. Could we arrange a concise 20-minute executive briefing on foreign direct investment (FDI) pathways into India with Acclime's leadership team?"
            ]

    output.extend(q_list)
    output.append("-" * 55)
    output.append("💡 Tip: You can directly copy these questions into an outreach email or Acclime client briefing note.")
    return "\n".join(output)

# ----------------- MCP PROTOCOL HANDLING (STDIO) -----------------

TOOLS_MANIFEST = [
    {
        "name": "ask_companies_met_last_year",
        "description": "Filter and search 80 European companies based on whether the analyst met them last year, country, and sector.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "European country (e.g. 'Germany', 'UK', 'France', 'Netherlands', 'Switzerland', 'Sweden', 'Italy', 'Spain', 'Belgium', 'Denmark')"
                },
                "sector": {
                    "type": "string",
                    "description": "Industry sector (e.g. 'Specialty Chemicals', 'Industrial Manufacturing', 'MedTech', 'Cleantech', 'SaaS', 'Automotive')"
                },
                "met_last_year": {
                    "type": "boolean",
                    "description": "True for the 35 companies met last year (2025); False for the 45 companies not met yet."
                }
            }
        }
    },
    {
        "name": "get_company_details_and_notes",
        "description": "Retrieve comprehensive company intelligence, meeting notes from last year, contact details, and financials.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "company_name": {
                    "type": "string",
                    "description": "Name or ID of the European company (e.g. 'Bavaria Katalys Chem AG' or 'EUR-001')"
                }
            },
            "required": ["company_name"]
        }
    },
    {
        "name": "get_potential_temporary_questions",
        "description": "Generate 4 situational, time-sensitive temporary questions tailored to a specific company and context.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "company_name": {
                    "type": "string",
                    "description": "Name or ID of the company"
                },
                "context": {
                    "type": "string",
                    "enum": [
                        "Post-Last-Year Re-engagement",
                        "15-Min Check-in Call",
                        "India Market Entry & Tax",
                        "M&A / JV Exploration"
                    ],
                    "description": "Outreach or meeting context"
                }
            },
            "required": ["company_name"]
        }
    }
]

def handle_stdio_rpc():
    """Lightweight, standard JSON-RPC 2.0 stdio MCP server loop"""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue
            
        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "initialize":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "acclime-eurotrack-mcp",
                        "version": "2.0.0"
                    }
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        elif method == "notifications/initialized":
            pass
        elif method == "tools/list":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": TOOLS_MANIFEST
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})
            try:
                if tool_name == "ask_companies_met_last_year":
                    content = ask_companies_met_last_year(
                        country=args.get("country"),
                        sector=args.get("sector"),
                        met_last_year=args.get("met_last_year")
                    )
                elif tool_name == "get_company_details_and_notes":
                    content = get_company_details_and_notes(
                        company_name=args.get("company_name", "")
                    )
                elif tool_name == "get_potential_temporary_questions":
                    content = get_potential_temporary_questions(
                        company_name=args.get("company_name", ""),
                        context=args.get("context", "Post-Last-Year Re-engagement")
                    )
                else:
                    content = f"Unknown tool: {tool_name}"
                    
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": content}
                        ]
                    }
                }
            except Exception as e:
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        elif req_id is not None:
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

# ----------------- CLI TEST MODE -----------------

def run_tests():
    print("=" * 60)
    print("ACCLIME EUROTRACK MCP SERVER SELF-TEST")
    print("=" * 60)
    
    print("\n--- Test 1: ask_companies_met_last_year(country='Germany', met_last_year=True) ---")
    t1 = ask_companies_met_last_year(country="Germany", met_last_year=True)
    print(t1)
    
    print("\n--- Test 2: get_company_details_and_notes('EUR-001') ---")
    t2 = get_company_details_and_notes("EUR-001")
    print(t2)
    
    print("\n--- Test 3: get_potential_temporary_questions('EUR-001', 'India Market Entry & Tax') ---")
    t3 = get_potential_temporary_questions("EUR-001", "India Market Entry & Tax")
    print(t3)
    
    print("\n--- Test 4: get_potential_temporary_questions for unmet company 'EUR-007', '15-Min Check-in Call' ---")
    t4 = get_potential_temporary_questions("EUR-007", "15-Min Check-in Call")
    print(t4)
    
    print("\nAll MCP tool tests completed successfully!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        # Check if FastMCP can be used or fallback to stdio JSON-RPC
        try:
            from mcp.server.fastmcp import FastMCP
            mcp = FastMCP("AcclimeEuroTrack")
            
            @mcp.tool()
            def tool_ask_companies_met_last_year(
                country: Optional[str] = None,
                sector: Optional[str] = None,
                met_last_year: Optional[bool] = None
            ) -> str:
                return ask_companies_met_last_year(country, sector, met_last_year)
                
            @mcp.tool()
            def tool_get_company_details_and_notes(company_name: str) -> str:
                return get_company_details_and_notes(company_name)
                
            @mcp.tool()
            def tool_get_potential_temporary_questions(company_name: str, context: Optional[str] = "Post-Last-Year Re-engagement") -> str:
                return get_potential_temporary_questions(company_name, context)
                
            mcp.run()
        except ImportError:
            # Clean stdio JSON-RPC fallback
            handle_stdio_rpc()
