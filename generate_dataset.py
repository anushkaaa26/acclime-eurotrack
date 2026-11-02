#!/usr/bin/env python3
"""
Dataset Generator for Acclime EuroTrack AI
Generates exactly 80 European companies across 10 countries and 6 sectors.
Met Last Year: exactly 35 (18 Follow-up Due, 10 Active Pipeline, 7 Paused)
Not Met: exactly 45 (25 High Priority, 20 Cold)
Outputs:
  - euro_companies.db (SQLite)
  - euro_companies.json (JSON fallback)
"""

import json
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "euro_companies.db")
JSON_PATH = os.path.join(os.path.dirname(__file__), "euro_companies.json")

# 80 hand-crafted, highly realistic European companies
COMPANIES = [
    # --- GERMANY (14 companies: 6 met, 8 unmet) ---
    {
        "id": "EUR-001",
        "company_name": "Bavaria Katalys Chem AG",
        "country": "Germany (Munich)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 420,
        "met_last_year": True,
        "meeting_date_last_year": "2025-10-14",
        "last_year_discussion_summary": "Met CEO Dr. Stefan Weber in Munich. They wanted to set up an Indian subsidiary in Q2 2026 for green hydrogen catalyst production but paused due to European energy costs. Highly interested in the Gujarat PCPIR chemical cluster and seeking Acclime advice on factory lease & hazardous materials licensing.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Dr. Stefan Weber", "role": "Chief Executive Officer", "email": "s.weber@bavaria-katalys.de"},
        "potential_temporary_questions": [
            "When we met in October last year, you paused your India entity setup due to EU capex tightening—how are board approvals shaping up for H1 2026?",
            "Have you evaluated the state-level capital subsidies in Gujarat's PCPIR corridor that we highlighted during our Munich meeting?",
            "Given recent European energy pricing adjustments, is the green catalyst blending timeline accelerating toward an Indian wholly owned subsidiary (WOS)?",
            "Do you need updated tax advisory regarding India's Section 115BAB manufacturing corporate tax incentives before Q2 capex sign-off?"
        ]
    },
    {
        "id": "EUR-002",
        "company_name": "Stuttgart Motion Dynamics GmbH",
        "country": "Germany (Stuttgart)",
        "sector": "Automotive",
        "revenue_eur_m": 310,
        "met_last_year": True,
        "meeting_date_last_year": "2025-06-18",
        "last_year_discussion_summary": "Met VP International Ops Klaus Lindner in Stuttgart. Exploring tier-1 electric drive manufacturing hub in Pune or Chennai to support Tata Motors and Mahindra EV platforms. Required transfer pricing structuring from Acclime.",
        "current_status": "Met Last Year - Active Pipeline",
        "key_contact": {"name": "Klaus Lindner", "role": "VP International Operations", "email": "k.lindner@stuttgartmotion.de"},
        "potential_temporary_questions": [
            "Following our June discussion on Pune vs Chennai for EV drivetrain assembly, have your Tier-1 supply discussions with Indian OEMs progressed?",
            "Have your tax advisors reviewed the Acclime transfer pricing model for cross-border IP licensing from Baden-Württemberg?",
            "Are you targeting the next round of India's Auto PLI (Production Linked Incentive) scheme application window?",
            "Can we prepare a comparative cost-of-doing-business benchmark between Chakan (Pune) and Sriperumbudur (Tamil Nadu) for your March board deck?"
        ]
    },
    {
        "id": "EUR-003",
        "company_name": "Rheinland Precision Machining SE",
        "country": "Germany (Düsseldorf)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 185,
        "met_last_year": True,
        "meeting_date_last_year": "2025-11-05",
        "last_year_discussion_summary": "Met Managing Director Heinrich Völkel. Considering JV with an Indian precision toolmaker in Bengaluru. Concerns raised around majority equity ownership and dispute resolution mechanisms under Indian company law.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Heinrich Völkel", "role": "Managing Director", "email": "h.voelkel@rheinland-precision.de"},
        "potential_temporary_questions": [
            "In our November meeting, you flagged majority equity protection in an Indian JV—have you finalized terms with the Bengaluru partner?",
            "Would you prefer Acclime to conduct independent compliance and financial due diligence on the Indian joint venture partner before term sheet execution?",
            "Have you explored setting up a 100% Wholly Owned Subsidiary first as an alternative to mitigate IP sharing risks?",
            "What is your target go-live date for Indian machining lines to service German aerospace export orders?"
        ]
    },
    {
        "id": "EUR-004",
        "company_name": "BioSynthetica Hesse GmbH",
        "country": "Germany (Frankfurt)",
        "sector": "MedTech",
        "revenue_eur_m": 95,
        "met_last_year": True,
        "meeting_date_last_year": "2025-09-22",
        "last_year_discussion_summary": "Met Chief Medical Officer Dr. Maren Scholl. Evaluating clinical trials partner and Indian medical device distribution entity. Required CDSCO regulatory roadmap and local director services.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Dr. Maren Scholl", "role": "Chief Scientific Officer", "email": "m.scholl@biosynthetica-hesse.de"},
        "potential_temporary_questions": [
            "Following our September discussion on CDSCO device registrations, have you locked down the product dossier classifications for India?",
            "Do you require Acclime India to provide resident nominee directorship to expedite your registrar of companies (RoC) incorporation?",
            "How does your 2026 R&D budget allocate between European clinical trials and APAC trial validation?",
            "Are you ready to review the commercial draft for our medical device distributor compliance package?"
        ]
    },
    {
        "id": "EUR-005",
        "company_name": "NordSolar CleanTech AG",
        "country": "Germany (Hamburg)",
        "sector": "Cleantech",
        "revenue_eur_m": 240,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Solar inverter and balance-of-system manufacturer. Evaluating 50MW assembly footprint in Rajasthan or Gujarat to de-risk supply chains from China; high priority target for Acclime India FDI & manufacturing setup.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Frank Richter", "role": "Chief Financial Officer", "email": "f.richter@nordsolar-cleantech.de"},
        "potential_temporary_questions": [
            "Has your finance committee reviewed the updated 2026 Union Budget basic customs duty revisions on solar inverter sub-components?",
            "Are you assessing Rajasthan vs Gujarat for a 50MW assembly plant footprint to capture domestic utility-scale solar tenders?",
            "Has the European supply chain due diligence directive accelerated your intent to de-risk solar balance-of-system sourcing via India?",
            "Could Acclime present a duty-drawback and customs bonded warehouse (MOOWR) feasibility analysis for your leadership?"
        ]
    },
    {
        "id": "EUR-006",
        "company_name": "ApexCloud Software Systems SE",
        "country": "Germany (Berlin)",
        "sector": "SaaS",
        "revenue_eur_m": 120,
        "met_last_year": True,
        "meeting_date_last_year": "2025-08-30",
        "last_year_discussion_summary": "Met VP Engineering Tobias Brandt. Wants to establish a 120-engineer Global Capability Center (GCC) in Hyderabad to handle enterprise DevOps and AI integrations.",
        "current_status": "Met Last Year - Active Pipeline",
        "key_contact": {"name": "Tobias Brandt", "role": "VP Engineering & Talent", "email": "t.brandt@apexcloud.de"},
        "potential_temporary_questions": [
            "Following our August talent cost modeling for Hyderabad, has executive leadership approved the initial 40-seat hiring tranche?",
            "Do you want Acclime to execute the SEZ / STPI registration and payroll processing setup this quarter?",
            "Have you finalized your transfer pricing agreement regarding R&D cost-plus remuneration for the Indian tech team?",
            "Can we introduce our vetted commercial leasing partners in Hitec City, Hyderabad for your site visit?"
        ]
    },
    {
        "id": "EUR-007",
        "company_name": "Hanover Polymer Solutions GmbH",
        "country": "Germany (Hanover)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 290,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Major producer of high-performance technical polymers. Facing soaring European energy levies and CBAM compliance pressure; perfect candidate for greenfield chemical plant in Western India.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Dr. Ulrich Becker", "role": "Head of Global Expansion", "email": "u.becker@hanoverpolymer.de"},
        "potential_temporary_questions": [
            "Are rising EU energy surcharges and carbon border taxes prompting you to evaluate a dedicated polymer synthesis base in India this year?",
            "How is Hanover Polymer approaching the China+1 mandate for specialty resin supplies into the automotive and electronics corridors?",
            "Have you explored the chemical infrastructure advantages and state subsidies offered within Gujarat's Dahej PCPIR?",
            "Would you be open to an Acclime briefing on foreign direct investment structuring and environmental clearances for specialty chemicals in India?"
        ]
    },
    {
        "id": "EUR-008",
        "company_name": "Saxony Robotic Automation AG",
        "country": "Germany (Dresden)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 145,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Produces semiconductor handling robotics. India's multi-billion semiconductor fab investments in Dholera and Sanand create massive demand for local servicing and assembly.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Matthias Vogel", "role": "Chief Commercial Officer", "email": "m.vogel@saxonyrobotic.de"},
        "potential_temporary_questions": [
            "With Tata Electronics and Micron scaling semiconductor mega-fabs in Gujarat and Assam, are you establishing an India field engineering hub?",
            "How do you plan to service Indian semiconductor cleanrooms without an incorporated local entity and bonded spare parts depot?",
            "Have you evaluated the capital subsidies available under India's SPECS and Modified Semicon India schemes?",
            "Can Acclime assist in setting up a local technical liaison office or wholly-owned servicing subsidiary before major fab deliveries begin?"
        ]
    },
    {
        "id": "EUR-009",
        "company_name": "Bavarian BioSensors GmbH",
        "country": "Germany (Nuremberg)",
        "sector": "MedTech",
        "revenue_eur_m": 68,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Manufactures continuous glucose monitoring sensors. High growth demand in India's metropolitan healthcare networks.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Anke Weimann", "role": "VP Global Sales", "email": "a.weimann@bavarianbiosensors.de"},
        "potential_temporary_questions": [
            "With India being the global diabetes capital, what is your current strategy for direct-to-consumer and hospital distribution across tier-1 metros?",
            "Are import tariffs on assembled biosensors hindering your margins compared to local assembly under the Medical Device PLI?",
            "Who currently handles your CDSCO regulatory certifications and authorized agent responsibilities in New Delhi?",
            "Would a 20-minute consultation on regulatory registration and import licensing structures with Acclime India be helpful?"
        ]
    },
    {
        "id": "EUR-010",
        "company_name": "Ruhr HydroGen Systems SE",
        "country": "Germany (Essen)",
        "sector": "Cleantech",
        "revenue_eur_m": 380,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Electrolyzer component manufacturer. High relevance for India's National Green Hydrogen Mission tenders (SECI).",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Jürgen Brandt", "role": "Director Strategy & M&A", "email": "j.brandt@ruhrhydrogen.de"},
        "potential_temporary_questions": [
            "Are you tracking the SECI Green Hydrogen & Electrolyzer manufacturing tenders under India's Strategic Interventions for Green Hydrogen Transition (SIGHT)?",
            "Are you evaluating joint venture partnerships with Indian energy conglomerates like Reliance, Adani, or L&T?",
            "What legal protections and IP safeguarding frameworks are essential for your membrane electrode assembly technology in India?",
            "Can Acclime brief your strategy committee on bidding eligibility and Indian subsidiary incorporation prerequisites?"
        ]
    },
    {
        "id": "EUR-011",
        "company_name": "DataKranz Logistics SaaS GmbH",
        "country": "Germany (Cologne)",
        "sector": "SaaS",
        "revenue_eur_m": 52,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Enterprise freight audit and supply chain tracking platform. High interest in setting up technical back-office and APAC support in India.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Svenja Kort", "role": "Head of Operations", "email": "s.kort@datakranz.de"},
        "potential_temporary_questions": [
            "Is DataKranz considering establishing a 24/7 client operations and data engineering support desk in Bengaluru or Pune?",
            "How are you managing EU customer data transfers in accordance with India's Digital Personal Data Protection (DPDP) Act?",
            "What is your timeline for scaling customer support coverage across the Asia-Pacific time zones?",
            "Would you like a sample benchmark of developer and support engineer compensation bands in tier-1 Indian tech hubs?"
        ]
    },
    {
        "id": "EUR-012",
        "company_name": "Schwarzwald Sensors & Micro GmbH",
        "country": "Germany (Freiburg)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 88,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. High-precision optical sensors for automated manufacturing. Looking to tap India's booming electronics manufacturing sector (Foxconn, Dixon, Tata).",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Markus Zeller", "role": "International Business Lead", "email": "m.zeller@schwarzwald-sensors.de"},
        "potential_temporary_questions": [
            "As consumer electronics assembly surges across Tamil Nadu and Noida, how are you supplying precision inspection sensors to EMS giants?",
            "Have you explored setting up an Indian branch or sales subsidiary to invoice clients directly in INR?",
            "Are you facing long lead times or customs bottlenecks using third-party distributors in Mumbai?",
            "Could Acclime walk you through the zero-hassle entity registration process under the National Single Window System?"
        ]
    },
    {
        "id": "EUR-013",
        "company_name": "Elbe AutoComponents SE",
        "country": "Germany (Wolfsburg)",
        "sector": "Automotive",
        "revenue_eur_m": 510,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Tier-1 chassis and suspension components. European cost inflation driving urgent search for low-cost APAC manufacturing and engineering centers.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Dr. Florian Schmidt", "role": "VP Global Sourcing", "email": "f.schmidt@elbe-auto.de"},
        "potential_temporary_questions": [
            "Are you feeling pressure from European automotive OEMs to reduce component costs by sourcing from Indian manufacturing hubs?",
            "Have you mapped out supplier clusters in the Oragadam (Chennai) or Sanand (Gujarat) automotive corridors?",
            "What is your appetite for acquiring an existing mid-market auto ancillary company in India versus a greenfield plant?",
            "How can Acclime support your initial market feasibility study and target screening in the Indian automotive supply chain?"
        ]
    },
    {
        "id": "EUR-014",
        "company_name": "Weser Biocides & Coating GmbH",
        "country": "Germany (Bremen)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 130,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Marine coatings and anti-fouling solutions. Significant shipbuilding and dry-dock expansion in Gujarat and Cochin.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Gerd Hagemann", "role": "Managing Director", "email": "g.hagemann@weser-coatings.de"},
        "potential_temporary_questions": [
            "With Indian shipyards seeing historic commercial orders, are you considering direct technical blending operations in Western India?",
            "What are your current barriers with Indian PESO and environmental approvals for chemical storage?",
            "Are you satisfied with your third-party agency agreements for port-side distribution in Kandla and JNPT?",
            "Can Acclime provide a compliance overview for chemical warehousing and customs bonded storage in Indian maritime zones?"
        ]
    },

    # --- UNITED KINGDOM (12 companies: 5 met, 7 unmet) ---
    {
        "id": "EUR-015",
        "company_name": "Oxford NanoMaterials Ltd",
        "country": "UK (Oxford)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 85,
        "met_last_year": True,
        "meeting_date_last_year": "2025-05-19",
        "last_year_discussion_summary": "Met Chief Technology Officer Dr. Sarah Jenkins in London. Spin-out commercializing graphene composites for battery anodes. Needs toll manufacturing partner and IP protection in India.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Dr. Sarah Jenkins", "role": "Chief Technology Officer", "email": "s.jenkins@oxfordnanomaterials.co.uk"},
        "potential_temporary_questions": [
            "When we met in London last May, you were shortlisting toll manufacturing partners for graphene blending—have contract negotiations commenced?",
            "Have you reviewed the bespoke IP protection protocols and non-compete covenants we recommended for your Indian tolling agreement?",
            "Are you considering establishing a wholly owned Indian entity to own local trademarks and patent filings?",
            "How do your timelines align with Indian battery cell manufacturers ramping up production under the Advanced Chemistry Cell PLI?"
        ]
    },
    {
        "id": "EUR-016",
        "company_name": "Midlands Precision Power Ltd",
        "country": "UK (Birmingham)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 210,
        "met_last_year": True,
        "meeting_date_last_year": "2025-10-28",
        "last_year_discussion_summary": "Met CEO Alistair Campbell. High-voltage switchgear manufacturer. Preparing tender submissions for Power Grid Corporation of India; required Indian entity incorporation to meet domestic content rules.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Alistair Campbell", "role": "Chief Executive Officer", "email": "a.campbell@midlandspower.co.uk"},
        "potential_temporary_questions": [
            "Following our October advisory on Power Grid Corporation public procurement rules, have you finalized the charter capital for your Indian subsidiary?",
            "Are you ready for Acclime to initiate the incorporation filing with the Ministry of Corporate Affairs to ensure tender qualification?",
            "Have you identified your Indian resident director or do you require Acclime's corporate nominee directorship services?",
            "Do you need assistance with GST registration and opening an Indian corporate banking account with HSBC or Standard Chartered?"
        ]
    },
    {
        "id": "EUR-017",
        "company_name": "Cambridge Digital Therapeutics Ltd",
        "country": "UK (Cambridge)",
        "sector": "MedTech",
        "revenue_eur_m": 45,
        "met_last_year": True,
        "meeting_date_last_year": "2025-03-14",
        "last_year_discussion_summary": "Met Head of Regulatory Nigel Brooks. Digital cognitive therapy app and bio-feedback sensors. Looking to establish offshore software development and data annotation center in Gurugram.",
        "current_status": "Met Last Year - Active Pipeline",
        "key_contact": {"name": "Nigel Brooks", "role": "Head of Regulatory & Expansion", "email": "n.brooks@cambridgedtx.co.uk"},
        "potential_temporary_questions": [
            "Since our March consultation on healthcare data sovereignty under the Indian DPDP Act, has your compliance board cleared offshore clinical data processing?",
            "Are you ready to initiate our turnkey GCC setup package for your 30-member Gurugram engineering pod?",
            "Have you considered partnering with Apollo or Fortis Hospital networks for Indian clinical validation?",
            "Can Acclime assist in drafting inter-company master service agreements (MSA) to secure UK R&D tax credit continuity?"
        ]
    },
    {
        "id": "EUR-018",
        "company_name": "Bristol Wave Dynamics Ltd",
        "country": "UK (Bristol)",
        "sector": "Cleantech",
        "revenue_eur_m": 115,
        "met_last_year": True,
        "meeting_date_last_year": "2025-07-25",
        "last_year_discussion_summary": "Met Commercial Director Emma Watson. Offshore tidal and marine turbine developer. Evaluating fabrication of turbine jackets in coastal Gujarat. Paused project pending UK export finance clearance.",
        "current_status": "Met Last Year - Paused",
        "key_contact": {"name": "Emma Watson", "role": "Commercial Director", "email": "e.watson@bristolwave.co.uk"},
        "potential_temporary_questions": [
            "Has UK Export Finance (UKEF) issued their underwriting decision for the Indian coastal fabrication feasibility study we reviewed in July?",
            "Are Indian coastal infrastructure EPC partners still engaged in joint bidding for the Gulf of Kutch pilot?",
            "Would an updated briefing on maritime port concessions and Indian coastal customs clearances help revive internal discussion?",
            "Can Acclime provide guidance on foreign contractor permanent establishment (PE) risks for your marine installation engineers?"
        ]
    },
    {
        "id": "EUR-019",
        "company_name": "FinRegulate AI Ltd",
        "country": "UK (London)",
        "sector": "SaaS",
        "revenue_eur_m": 72,
        "met_last_year": True,
        "meeting_date_last_year": "2025-11-18",
        "last_year_discussion_summary": "Met Founder & CEO David Sterling in Mayfair. Automated AML and anti-fraud monitoring SaaS. Seeking RBI regulatory sandbox admission and sales partnerships with Indian private banks.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "David Sterling", "role": "Founder & CEO", "email": "d.sterling@finregulate.ai"},
        "potential_temporary_questions": [
            "When we met in London in November, you were preparing your fintech pitch deck for Indian private banks—have you scheduled pilot demos with HDFC or ICICI?",
            "Have you reviewed the Reserve Bank of India (RBI) local data storage requirements for banking SaaS vendors that we compiled?",
            "Would you like Acclime to assist in establishing a Mumbai liaison office to facilitate executive interactions with the RBI FinTech Department?",
            "Are you considering applying for the upcoming cohort of the IFSCA Regulatory Sandbox at GIFT City, Gujarat?"
        ]
    },
    {
        "id": "EUR-020",
        "company_name": "Coventry EV Propulsion Ltd",
        "country": "UK (Coventry)",
        "sector": "Automotive",
        "revenue_eur_m": 160,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Next-gen silicon carbide traction inverters for electric buses and commercial vehicles. Prime fit for India's PM-eBus Sewa initiative (10,000 electric buses).",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Peter Hawthorne", "role": "Managing Director", "email": "p.hawthorne@coventryev.co.uk"},
        "potential_temporary_questions": [
            "With the Indian government procuring over 10,000 electric buses under the PM-eBus Sewa scheme, have you engaged with Indian e-bus OEMs like Olectra and JBM?",
            "What is your plan for meeting the mandatory Phased Manufacturing Programme (PMP) localization requirements in India?",
            "Have you explored setting up an engineering testing lab in the Pune automotive tech belt?",
            "Would you welcome a briefing from Acclime India on commercial vehicle EV incentives and entity establishment roadmaps?"
        ]
    },
    {
        "id": "EUR-021",
        "company_name": "Manchester BioPolymers Ltd",
        "country": "UK (Manchester)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 64,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Biodegradable packaging polymers derived from agricultural waste. Huge market potential due to India's single-use plastic ban enforcement.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Rachel Thorne", "role": "VP Commercial Development", "email": "r.thorne@manchesterbiopolymers.co.uk"},
        "potential_temporary_questions": [
            "Given India's nationwide strict ban on single-use plastics, how is your biopolymer resin positioned for Indian FMCG packaging converters?",
            "Are you considering licensing your starch-based polymer extrusion tech to Indian packaging conglomerates?",
            "Have you evaluated the feedstock cost advantages of sourcing agricultural bagasse and corn starch directly in Maharashtra and Punjab?",
            "Can Acclime advise your team on Central Pollution Control Board (CPCB) certification for compostable packaging in India?"
        ]
    },
    {
        "id": "EUR-022",
        "company_name": "Leeds Industrial Robotics Ltd",
        "country": "UK (Leeds)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 128,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Heavy-payload robotic arms for warehouse automation and automotive assembly. India warehouse logistics modernization is driving rapid adoption.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Simon Bradshaw", "role": "Sales Director APAC", "email": "s.bradshaw@leedsrobotics.co.uk"},
        "potential_temporary_questions": [
            "How are you addressing the skyrocketing demand for robotic warehouse automation across Indian e-commerce fulfillment hubs?",
            "Do your current distributor agreements in India include SLAs for 24-hour on-site maintenance and emergency component replacement?",
            "Have you assessed the tax efficiency of setting up a local technical assembly unit versus importing fully built robotic arms?",
            "Would you like an overview of corporate establishment and customs valuation regulations for capital equipment in India?"
        ]
    },
    {
        "id": "EUR-023",
        "company_name": "Belfast MedSystems Ltd",
        "country": "UK (Belfast)",
        "sector": "MedTech",
        "revenue_eur_m": 58,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Portable point-of-care cardiac diagnostic devices. High synergy with India's Ayushman Bharat rural health infrastructure upgrade.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Dr. Patrick O'Donnell", "role": "Chief Operating Officer", "email": "p.odonnell@belfastmedsystems.co.uk"},
        "potential_temporary_questions": [
            "Are you targeting government tenders under India's Ayushman Bharat rural digital health mission for point-of-care diagnostics?",
            "Have you initiated local manufacturing feasibility to fulfill the 'Make in India' preference criteria in public procurement?",
            "What CDSCO medical device classification has been assigned to your ECG and cardiac biomarker hardware?",
            "Could Acclime provide guidance on distributor vetting and regulatory compliance for Indian healthcare tenders?"
        ]
    },
    {
        "id": "EUR-024",
        "company_name": "Thames CleanWater Technologies Ltd",
        "country": "UK (Reading)",
        "sector": "Cleantech",
        "revenue_eur_m": 92,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Industrial zero-liquid-discharge (ZLD) effluent treatment membranes. Extremely relevant for Indian textile and chemical dyeing clusters in Tamil Nadu and Gujarat.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Clare Higgins", "role": "Business Development Director", "email": "c.higgins@thamescleanwater.co.uk"},
        "potential_temporary_questions": [
            "With stringent Zero Liquid Discharge (ZLD) norms mandated for textile and tannery belts in Tirupur and Kanpur, is your membrane technology present in India?",
            "Are you partnering with local Indian water treatment EPC companies like Thermax or VA Tech Wabag?",
            "What is your strategy for navigating state pollution control board (SPCB) tender requirements for wastewater treatment?",
            "Can Acclime connect your executive team with leading industrial water concessionaires in India?"
        ]
    },
    {
        "id": "EUR-025",
        "company_name": "CyberThames Security Solutions Ltd",
        "country": "UK (London)",
        "sector": "SaaS",
        "revenue_eur_m": 105,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Critical infrastructure cybersecurity SaaS. Indian banking and power grids are mandated to replace legacy solutions with certified zero-trust architecture.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Julian Croft", "role": "Chief Revenue Officer", "email": "j.croft@cyberthames.co.uk"},
        "potential_temporary_questions": [
            "Are you compliant with CERT-In cybersecurity directives and RBI operational resilience guidelines for financial institutions?",
            "Have you explored opening an Indian security operations center (SOC) and engineering lab in Bengaluru?",
            "What is your current distribution approach for major Indian IT systems integrators (TCS, Wipro, Infosys)?",
            "Can Acclime advise on corporate tax withholding (TDS) and equalization levy applicability for your SaaS subscription contracts in India?"
        ]
    },
    {
        "id": "EUR-026",
        "company_name": "Surrey AutoSensor Analytics Ltd",
        "country": "UK (Guildford)",
        "sector": "Automotive",
        "revenue_eur_m": 48,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. ADAS sensor fusion algorithms and simulation software. Major potential client for Indian auto R&D centers in Bengaluru and Chennai.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Oliver Vance", "role": "VP Global Partnerships", "email": "o.vance@surreysensors.co.uk"},
        "potential_temporary_questions": [
            "Are you collaborating with Indian automotive Tier-1 suppliers like Tata AutoComp or Motherson Sumi on ADAS sensor calibration?",
            "Have you considered tapping India's vast pool of computer vision and automotive software engineers through a dedicated India tech center?",
            "What is your IP licensing structure for cross-border software royalties into the Indian market?",
            "Would you be interested in an Acclime comparative guide on setting up a Global Capability Center (GCC) in India?"
        ]
    },

    # --- FRANCE (10 companies: 5 met, 5 unmet) ---
    {
        "id": "EUR-027",
        "company_name": "Rhône Specialty Catalysts SAS",
        "country": "France (Lyon)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 340,
        "met_last_year": True,
        "meeting_date_last_year": "2025-09-18",
        "last_year_discussion_summary": "Met VP Strategy Jean-Luc Moreau in Paris. They want to set up an Indian subsidiary in Q2 2026 to supply specialty catalysts to refinery and bio-ethanol plants. Paused due to European capex reallocation. Interested in Maharashtra chemical zones.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Jean-Luc Moreau", "role": "VP Strategy & Corporate Dev", "email": "jl.moreau@rhonecatalysts.fr"},
        "potential_temporary_questions": [
            "When we met in September, your board paused the Dahej/Rohi plant investment pending European capex stabilization—is this back on the 2026 agenda?",
            "Have you evaluated the updated 20% ethanol blending mandate in India and its impact on catalyst demand for 2G bio-refineries?",
            "Would you like Acclime to update our comparative site selection assessment between MIDC (Maharashtra) and GIDC (Gujarat)?",
            "Can we prepare an executive memorandum on hazardous chemicals regulatory compliance and EIA clearance timelines for your Q2 board review?"
        ]
    },
    {
        "id": "EUR-028",
        "company_name": "Normandie Precision Aerospace SAS",
        "country": "France (Rouen)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 220,
        "met_last_year": True,
        "meeting_date_last_year": "2025-06-04",
        "last_year_discussion_summary": "Met CEO Bertrand Lefèvre. Precision turbine blades and titanium fasteners. Strong vendor interest from Hindustan Aeronautics Limited (HAL) and Safran India JV in Hyderabad. Needed advice on offset obligations.",
        "current_status": "Met Last Year - Active Pipeline",
        "key_contact": {"name": "Bertrand Lefèvre", "role": "Chief Executive Officer", "email": "b.lefevre@normandie-aero.fr"},
        "potential_temporary_questions": [
            "Following our June discussion on aerospace defense offsets, have your tier-1 supply negotiations with Safran India in Hyderabad progressed?",
            "Have you decided whether to enter India via an incorporated Wholly Owned Subsidiary (WOS) or an aerospace manufacturing joint venture?",
            "Do you require Acclime assistance with industrial licensing from the Department for Promotion of Industry and Internal Trade (DPIIT)?",
            "Are you planning a site inspection of the Aerospace SEZ at Devanahalli (Bengaluru) or Adibatla (Hyderabad) this spring?"
        ]
    },
    {
        "id": "EUR-029",
        "company_name": "Lille BioDiagnostics SA",
        "country": "France (Lille)",
        "sector": "MedTech",
        "revenue_eur_m": 78,
        "met_last_year": True,
        "meeting_date_last_year": "2025-11-20",
        "last_year_discussion_summary": "Met Chief Scientific Officer Dr. Cécile Dubois. In-vitro diagnostic reagents and infectious disease test kits. Ready to partner with pan-India diagnostic chains like Dr Lal PathLabs and Metropolis.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Dr. Cécile Dubois", "role": "Chief Scientific Officer", "email": "c.dubois@lillebiodiagnostics.fr"},
        "potential_temporary_questions": [
            "In our November meeting, you outlined partnerships with Indian diagnostic chains—have distribution commercial agreements been initiated?",
            "Have your regulatory specialists completed the CDSCO import license dossier filings for your primary diagnostic reagent lines?",
            "Do you require Acclime India to serve as your Authorized Indian Agent (AIA) under Medical Device Rules 2017?",
            "Would you like an updated overview of GST rates on medical diagnostic consumables and transfer pricing benchmarks?"
        ]
    },
    {
        "id": "EUR-030",
        "company_name": "Occitanie CleanSolar SAS",
        "country": "France (Toulouse)",
        "sector": "Cleantech",
        "revenue_eur_m": 165,
        "met_last_year": True,
        "meeting_date_last_year": "2025-04-29",
        "last_year_discussion_summary": "Met Investment Director Mathieu Caron. Agrivoltaics and dual-use solar canopy technology. Evaluating pilot projects with state governments in Karnataka and Maharashtra.",
        "current_status": "Met Last Year - Paused",
        "key_contact": {"name": "Mathieu Caron", "role": "Investment Director", "email": "m.caron@occitanie-cleansolar.fr"},
        "potential_temporary_questions": [
            "Following our April analysis on agricultural land conversion laws in Karnataka, has your legal team cleared the pilot agrivoltaics site?",
            "Are you tracking the latest PM-KUSUM scheme guidelines for decentralized solar installations on agricultural land?",
            "Could Acclime structure a joint development agreement (JDA) framework with your local Indian solar EPC partners?",
            "What financing prerequisites from Proparco or AFD French Development Agency are currently pending for this initiative?"
        ]
    },
    {
        "id": "EUR-031",
        "company_name": "Parisian CloudSec Analytics SAS",
        "country": "France (Paris)",
        "sector": "SaaS",
        "revenue_eur_m": 110,
        "met_last_year": True,
        "meeting_date_last_year": "2025-10-08",
        "last_year_discussion_summary": "Met Chief Revenue Officer Élodie Mercier. Enterprise governance, risk, and compliance (GRC) software. Looking to recruit a 40-person customer success and cloud DevOps team in Bengaluru.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Élodie Mercier", "role": "Chief Revenue Officer", "email": "e.mercier@cloudsec-paris.fr"},
        "potential_temporary_questions": [
            "When we met in Paris in October, you targeted a Q1 2026 launch for your Bengaluru customer success hub—have job descriptions been finalized?",
            "Are you ready for Acclime to initiate the company incorporation, shop & establishment registration, and provident fund (PF) setup?",
            "Have you reviewed the cost-plus 15% transfer pricing markup standard commonly applied to Indian tech subsidiary services?",
            "Can we schedule an introductory meeting with our Bengaluru corporate workspace advisory partners to review office options?"
        ]
    },
    {
        "id": "EUR-032",
        "company_name": "Alsace Precision Hydraulics SAS",
        "country": "France (Strasbourg)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 195,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. High-pressure hydraulic pumps and valves for earthmoving equipment. Major suppliers to JCB and Caterpillar plants in India.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Thierry Bernard", "role": "Industrial Operations Director", "email": "t.bernard@alsacehydraulics.fr"},
        "potential_temporary_questions": [
            "With Indian infrastructure capex at all-time highs driving heavy earthmoving demand, how are you supplying hydraulic valves to Indian OEMs?",
            "Are lead times from France impairing your competitiveness against Japanese and local hydraulic component suppliers?",
            "Have you considered establishing a localized assembly and testing facility in the Oragadam industrial cluster in Tamil Nadu?",
            "Would you appreciate an Acclime strategic briefing on customs bonded assembly (MOOWR) and FDI setup in India?"
        ]
    },
    {
        "id": "EUR-033",
        "company_name": "Bordeaux BioPharma Solutions SA",
        "country": "France (Bordeaux)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 140,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Chiral synthesis and high-potency active pharmaceutical ingredients (HPAPI). High synergy with Hyderabad's Genome Valley pharmaceutical giants.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Dr. Florence Garnier", "role": "Head of BD & Licensing", "email": "f.garnier@bordeaux-biopharma.fr"},
        "potential_temporary_questions": [
            "Are you actively exploring contract development and manufacturing partnerships (CDMO) with Hyderabad pharma majors like Dr. Reddy's or Aurobindo?",
            "How is Bordeaux BioPharma addressing supply chain concentration risks for raw precursor chemicals originating from China?",
            "Have you explored setting up an R&D collaboration laboratory within Genome Valley in Hyderabad?",
            "Can Acclime advise your corporate development team on intellectual property assignment and pharmaceutical regulatory clearances in India?"
        ]
    },
    {
        "id": "EUR-034",
        "company_name": "Grenoble MedRobotics SAS",
        "country": "France (Grenoble)",
        "sector": "MedTech",
        "revenue_eur_m": 82,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Minimally invasive surgical robotics for orthopedic and spinal procedures. India's private hospital groups are investing heavily in robotic surgery suites.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Gilles Vautier", "role": "Chief Commercial Officer", "email": "g.vautier@grenoble-medrobotics.fr"},
        "potential_temporary_questions": [
            "Have you engaged with tier-1 private healthcare chains in India (Max Healthcare, Apollo, Manipal) for surgical robotics trials?",
            "What is your plan for complying with CDSCO registration requirements for robotic class C/D surgical medical devices?",
            "How do you plan to handle equipment leasing and hospital pay-per-use commercial financing models under Indian tax law?",
            "Would you be open to an Acclime guidance call on structuring medical equipment leasing entities and local servicing subsidiaries?"
        ]
    },
    {
        "id": "EUR-035",
        "company_name": "Marseille Maritime CleanEnergy SAS",
        "country": "France (Marseille)",
        "sector": "Cleantech",
        "revenue_eur_m": 125,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Port shore-power electrification systems and battery-hybrid harbor tugs. Relevant to India's Harit Nauka (green boat) and Green Tug Transition Programme (GTTP).",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Stéphane Perrin", "role": "Managing Director", "email": "s.perrin@marseille-cleanenergy.fr"},
        "potential_temporary_questions": [
            "Are you tracking the Ministry of Ports and Shipping's Green Tug Transition Programme (GTTP) and port electrification mandates in India?",
            "Have you initiated dialogue with Cochin Shipyard or Mazagon Dock regarding hybrid tug propulsion systems?",
            "What is your approach to meeting local value addition norms under the 'Make in India' defense and maritime public procurement orders?",
            "Can Acclime provide intelligence on public-private partnership (PPP) port concession guidelines and corporate establishment?"
        ]
    },
    {
        "id": "EUR-036",
        "company_name": "Valence AutoBattery Tech SAS",
        "country": "France (Valence)",
        "sector": "Automotive",
        "revenue_eur_m": 270,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Advanced battery thermal management systems for commercial electric vehicles. Critical component for Indian 2-wheeler and 3-wheeler fire safety standards (AIS-156).",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Antoine Renard", "role": "VP Global OEM Sales", "email": "a.renard@valence-autobattery.fr"},
        "potential_temporary_questions": [
            "With Indian AIS-156 thermal safety regulations strictly enforced for electric vehicles, what is your OEM strategy for Indian battery pack makers?",
            "Are you supplying thermal interface materials and cooling plates to Indian EV giants like Ola Electric or Ather Energy?",
            "Have you evaluated the cost savings of establishing a thermal management assembly line in Pune or Chennai?",
            "Could Acclime present an overview of industrial subsidies, state EV policies, and corporate tax structuring in India?"
        ]
    },

    # --- NETHERLANDS (8 companies: 4 met, 4 unmet) ---
    {
        "id": "EUR-037",
        "company_name": "Rotterdam BioPolymer Systems BV",
        "country": "Netherlands (Rotterdam)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 310,
        "met_last_year": True,
        "meeting_date_last_year": "2025-10-21",
        "last_year_discussion_summary": "Met Chief Operating Officer Pieter van Dijk. Sustainable circular polymers and bio-resins. Discussed tolling agreement with an Indian partner in Dahej and transfer of clean polymer technology. Paused to evaluate Dutch environmental subsidies.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Pieter van Dijk", "role": "Chief Operating Officer", "email": "p.vandijk@rotterdambiopolymers.nl"},
        "potential_temporary_questions": [
            "When we met in October, you were weighing Dutch state circularity grants against direct Indian capex—has your executive board reached a verdict?",
            "Have you concluded the NDA and commercial evaluation with the prospective toll manufacturing partner in Gujarat's Dahej zone?",
            "Would you like Acclime to conduct legal and regulatory due diligence on the proposed Indian tolling partner's environmental permits?",
            "Are you ready to explore the 15% corporate tax window available to new Indian manufacturing companies?"
        ]
    },
    {
        "id": "EUR-038",
        "company_name": "Eindhoven Semiconductor Optics BV",
        "country": "Netherlands (Eindhoven)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 480,
        "met_last_year": True,
        "meeting_date_last_year": "2025-05-12",
        "last_year_discussion_summary": "Met VP Business Expansion Willem de Jong in Eindhoven. Lithography optical sub-assemblies and inspection equipment. Evaluating India tech center for precision calibration software.",
        "current_status": "Met Last Year - Active Pipeline",
        "key_contact": {"name": "Willem de Jong", "role": "VP Business Expansion", "email": "w.dejong@eindhoven-optics.nl"},
        "potential_temporary_questions": [
            "Following our May session on establishing a calibration software engineering center in Bengaluru, have headcount budgets been approved?",
            "Have you finalized the transfer pricing strategy for technical service fees between Eindhoven and your prospective Indian entity?",
            "Do you require Acclime assistance with STPI / SEZ registration and Indian patent office utility model filings?",
            "Can we assist in arranging commercial real estate site visits and local management recruitment across Bengaluru and Hyderabad?"
        ]
    },
    {
        "id": "EUR-039",
        "company_name": "Delft CleanHydrogen BV",
        "country": "Netherlands (Delft)",
        "sector": "Cleantech",
        "revenue_eur_m": 150,
        "met_last_year": True,
        "meeting_date_last_year": "2025-09-03",
        "last_year_discussion_summary": "Met CEO Anouk van der Meer. Anion exchange membrane (AEM) electrolyzers. Deeply interested in setting up JV with Indian solar developer to bid for green ammonia projects in Odisha.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Anouk van der Meer", "role": "Chief Executive Officer", "email": "a.vandermeer@delft-cleanhydrogen.nl"},
        "potential_temporary_questions": [
            "Following our September meeting, have your joint venture discussions with the Odisha green ammonia consortium progressed?",
            "Have your corporate attorneys reviewed the draft Joint Venture Agreement regarding IP licensing and deadlock resolution clauses?",
            "Would you like Acclime to evaluate the state renewable policy incentives in Odisha and Andhra Pradesh for your pilot installation?",
            "What regulatory milestones are required from the Petroleum and Explosives Safety Organization (PESO) for your high-pressure electrolyzers?"
        ]
    },
    {
        "id": "EUR-040",
        "company_name": "Amsterdam AgriTech AI BV",
        "country": "Netherlands (Amsterdam)",
        "sector": "SaaS",
        "revenue_eur_m": 62,
        "met_last_year": True,
        "meeting_date_last_year": "2025-07-16",
        "last_year_discussion_summary": "Met Head of Product Daan Visser. Satellite crop yield forecasting and carbon credit verification software. Partnering with Indian agribusinesses. Paused due to Indian carbon market regulatory delays.",
        "current_status": "Met Last Year - Paused",
        "key_contact": {"name": "Daan Visser", "role": "Head of Product & Markets", "email": "d.visser@amsterdam-agritech.nl"},
        "potential_temporary_questions": [
            "Since our July discussion, the Bureau of Energy Efficiency (BEE) has released updated Carbon Credit Trading Scheme (CCTS) rules—is your board re-evaluating India?",
            "Are your pilot data verification trials with Indian agribusiness conglomerates (ITC, Godrej Agrovet) moving forward?",
            "Do you need an updated legal assessment of drone imagery and geospatial data hosting regulations under the National Geospatial Policy?",
            "Can Acclime assist in drafting SaaS enterprise service contracts governed by Indian commercial court jurisdiction?"
        ]
    },
    {
        "id": "EUR-041",
        "company_name": "Utrecht MicroMed Devices BV",
        "country": "Netherlands (Utrecht)",
        "sector": "MedTech",
        "revenue_eur_m": 76,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Disposable micro-endoscopes and surgical visualization consumables. Indian single-use endoscope market growing at 28% CAGR.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Sanne Bakker", "role": "Chief Commercial Officer", "email": "s.bakker@utrecht-micromed.nl"},
        "potential_temporary_questions": [
            "How is Utrecht MicroMed positioning its single-use endoscopy consumables against traditional reusable scopes across Indian private hospitals?",
            "Are you seeking an Indian master importer and authorized representative to manage CDSCO regulatory clearances?",
            "Have you considered the customs duty differentials between importing finished endoscopes versus CKD (completely knocked down) kit assembly?",
            "Could Acclime provide a customized go-to-market advisory and healthcare regulatory roadmap for India?"
        ]
    },
    {
        "id": "EUR-042",
        "company_name": "Twente Advanced Materials BV",
        "country": "Netherlands (Enschede)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 190,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Nanofiber filtration media for high-efficiency HVAC and industrial air purification. Huge Indian demand driven by urban air quality standards and industrial cleanrooms.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Koen Meijer", "role": "Managing Director", "email": "k.meijer@twente-materials.nl"},
        "potential_temporary_questions": [
            "With stringent particulate emission regulations being enforced across industrial clusters in North India, what is your B2B supply plan?",
            "Are you evaluating contract manufacturing or toll spinning partnerships for nanofiber membranes in India?",
            "What is your strategy to protect your proprietary electrospinning IP when manufacturing in emerging Asian markets?",
            "Can Acclime prepare a regulatory overview on environmental clearances and factory establishment in Maharashtra or Tamil Nadu?"
        ]
    },
    {
        "id": "EUR-043",
        "company_name": "Brabant AutoElectronics BV",
        "country": "Netherlands (Tilburg)",
        "sector": "Automotive",
        "revenue_eur_m": 225,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Power distribution units and wiring harnesses for commercial heavy vehicles. Exploring low-cost Indian engineering hub.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Bas van Leeuwen", "role": "VP Global Operations", "email": "b.vanleeuwen@brabant-autotech.nl"},
        "potential_temporary_questions": [
            "Are you considering setting up an offshore engineering and harness design bureau in Chennai or Pune to support European programs?",
            "How are you managing engineering billing rates in the Netherlands compared to the competitive talent economics of Indian engineering GCCs?",
            "What compliance steps have you mapped out regarding the Indian Shop & Establishment Act and professional employment organization (PEO) models?",
            "Would you like an Acclime briefing on fast-track entity setup vs Employer of Record (EOR) options for your initial team?"
        ]
    },
    {
        "id": "EUR-044",
        "company_name": "Groningen SmartGrid SaaS BV",
        "country": "Netherlands (Groningen)",
        "sector": "SaaS",
        "revenue_eur_m": 54,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Virtual power plant and smart meter data analytics platform. India is deploying 250 million smart prepaid meters under the RDSS scheme.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Femke de Boer", "role": "Head of Strategic Growth", "email": "f.deboer@groningen-smartgrid.nl"},
        "potential_temporary_questions": [
            "With India rolling out 250 million smart meters under the Revamped Distribution Sector Scheme (RDSS), are you partnering with state DISCOMs?",
            "Are you teaming up with Indian AMI (Advanced Metering Infrastructure) service providers like IntelliSmart or Genus Power?",
            "Have you evaluated data localization mandates under Indian power sector cybersecurity guidelines?",
            "Can Acclime advise your management team on government tender eligibility, consortium bidding, and local subsidiary formation in New Delhi?"
        ]
    },

    # --- SWITZERLAND (7 companies: 3 met, 4 unmet) ---
    {
        "id": "EUR-045",
        "company_name": "Helvetia Specialty Synth AG",
        "country": "Switzerland (Basel)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 520,
        "met_last_year": True,
        "meeting_date_last_year": "2025-08-14",
        "last_year_discussion_summary": "Met CFO Beat Schläpfer in Basel. Flavor & fragrance aroma chemicals and high-purity pharma intermediates. Considering $40M greenfield facility in Gujarat. Needed Swiss-India tax treaty dividend withholding advisory.",
        "current_status": "Met Last Year - Active Pipeline",
        "key_contact": {"name": "Beat Schläpfer", "role": "Chief Financial Officer", "email": "b.schlaepfer@helvetia-synth.ch"},
        "potential_temporary_questions": [
            "Following our Basel meeting regarding the Swiss-India Double Taxation Avoidance Agreement (DTAA) MFN clause, has your tax committee signed off on the financing structure?",
            "Are you ready for Acclime to coordinate environmental impact assessment (EIA) submissions for the proposed Dahej chemical plot?",
            "Have you finalized whether parent equity will flow directly from Basel or via a Singapore holding company?",
            "Can we schedule an introductory session with our transfer pricing partners to model cross-border royalty streams for your fragrance patents?"
        ]
    },
    {
        "id": "EUR-046",
        "company_name": "Zurich MedTech Precision AG",
        "country": "Switzerland (Zurich)",
        "sector": "MedTech",
        "revenue_eur_m": 190,
        "met_last_year": True,
        "meeting_date_last_year": "2025-10-30",
        "last_year_discussion_summary": "Met VP International Markets Urs Zimmermann. Orthopedic titanium implants and spinal fixation systems. Seeking India distributor network and investigating medical device park incentives in Andhra Pradesh.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Urs Zimmermann", "role": "VP International Markets", "email": "u.zimmermann@zurichmedtech.ch"},
        "potential_temporary_questions": [
            "When we met in October, you were reviewing distributor compliance terms for your spinal implants in India—have tier-1 dealers been onboarded?",
            "Have you evaluated the capital subsidies and plug-and-play manufacturing infrastructure at Andhra Pradesh MedTech Zone (AMTZ)?",
            "What is your status on CDSCO Class C medical device registration dossiers for your orthopedic line?",
            "Do you need Acclime to provide independent vendor integrity audits on prospective Indian distributors before signing agreements?"
        ]
    },
    {
        "id": "EUR-047",
        "company_name": "Alpine MicroMachining SA",
        "country": "Switzerland (La Chaux-de-Fonds)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 110,
        "met_last_year": True,
        "meeting_date_last_year": "2025-11-28",
        "last_year_discussion_summary": "Met Managing Director Marcel Favre. Ultra-precision 5-axis CNC machining tools. High interest from Indian defense and watch manufacturing sectors. Needed customs bonded warehouse guidance.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Marcel Favre", "role": "Managing Director", "email": "m.favre@alpine-machining.ch"},
        "potential_temporary_questions": [
            "Following our November briefing on India's MOOWR scheme (Manufacture and Other Operations in Warehouse Regulations), are you ready to structure your spare parts hub?",
            "Have you selected your local application engineering and customer service partner in Bengaluru?",
            "How does your leadership view currency volatility between CHF and INR for capital machinery import contracts?",
            "Can Acclime assist in setting up an Indian branch office or technical liaison office to directly service watch and defense clients?"
        ]
    },
    {
        "id": "EUR-048",
        "company_name": "Geneva EnviroTech Solutions SA",
        "country": "Switzerland (Geneva)",
        "sector": "Cleantech",
        "revenue_eur_m": 135,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Industrial carbon capture and solvent recycling technologies for heavy industry. Relevant to Indian steel and cement decarbonization roadmaps.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Corinne Bovet", "role": "Director Global Partnerships", "email": "c.bovet@geneva-envirotech.ch"},
        "potential_temporary_questions": [
            "With Indian cement and steel majors (Tata Steel, UltraTech) mandated to meet aggressive decarbonization targets, what is your market entry roadmap?",
            "Have you considered technology licensing or JV partnerships with Indian heavy engineering conglomerates?",
            "Are you tracking Indian government incentives under the Carbon Capture, Utilization and Storage (CCUS) national framework?",
            "Would you be open to an Acclime executive advisory on navigating corporate incorporation and joint venture safeguards in India?"
        ]
    },
    {
        "id": "EUR-049",
        "company_name": "Lucerne Banking Cloud AG",
        "country": "Switzerland (Lucerne)",
        "sector": "SaaS",
        "revenue_eur_m": 88,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Core wealth management and private banking software. Indian wealth management sector is booming with HNWI growth.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Christoph Meier", "role": "Head of Strategic Growth", "email": "c.meier@lucernebankingcloud.ch"},
        "potential_temporary_questions": [
            "Given the rapid growth of Indian family offices and wealth management firms, are you considering expanding your private banking SaaS into Mumbai?",
            "How do you plan to satisfy SEBI and RBI data residency mandates requiring banking financial data to remain within sovereign Indian borders?",
            "Have you evaluated setting up a development and tier-2 client support team in Pune or Hyderabad?",
            "Can Acclime provide guidance on goods and services tax (GST) cross-border invoicing and entity structuring for Swiss SaaS vendors?"
        ]
    },
    {
        "id": "EUR-050",
        "company_name": "St. Gallen EV Systems AG",
        "country": "Switzerland (St. Gallen)",
        "sector": "Automotive",
        "revenue_eur_m": 160,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. High-efficiency power electronics and DC-DC converters for heavy electric trucks and mining machinery. Mining electrification is accelerating in India.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Lukas Egger", "role": "Chief Commercial Officer", "email": "l.egger@stgallen-ev.ch"},
        "potential_temporary_questions": [
            "As Indian mining giants like Coal India and Tata Steel mandate green electric haul trucks, have you engaged with Indian commercial vehicle OEMs?",
            "What is your plan for local assembly to qualify for preferential domestic public procurement quotas?",
            "Have you explored setting up an R&D and firmware validation pod in Bengaluru's automotive engineering corridor?",
            "Would you like an Acclime comparative report on setting up an Indian manufacturing entity versus an engineering liaison office?"
        ]
    },
    {
        "id": "EUR-051",
        "company_name": "Neuchâtel MicroSensors SA",
        "country": "Switzerland (Neuchâtel)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 72,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. MEMS pressure and temperature sensors for aerospace and harsh industrial environments. Target for Indian aerospace supply chains.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Didier Vuille", "role": "VP Global Sales", "email": "d.vuille@neuchatel-sensors.ch"},
        "potential_temporary_questions": [
            "Are you supplying MEMS sensors to Indian space agency (ISRO) vendors or commercial aerospace manufacturing programs?",
            "How are you managing customs clearances and high import duties on specialized electronic instrumentation entering India?",
            "Have you explored opening an Indian technical application center to provide real-time calibration support for defense contractors?",
            "Can Acclime brief your international team on export control alignment and corporate entity formation under Indian regulations?"
        ]
    },

    # --- SWEDEN (7 companies: 3 met, 4 unmet) ---
    {
        "id": "EUR-052",
        "company_name": "Nordic BioPolymers AB",
        "country": "Sweden (Stockholm)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 210,
        "met_last_year": True,
        "meeting_date_last_year": "2025-06-25",
        "last_year_discussion_summary": "Met CEO Dr. Arvid Lindqvist in Stockholm. Forestry-derived lignin specialty polymers and bio-binders. Interested in setting up an Indian JV with a paper packaging conglomerate in Tamil Nadu. Paused due to local effluent regulations.",
        "current_status": "Met Last Year - Paused",
        "key_contact": {"name": "Dr. Arvid Lindqvist", "role": "Chief Executive Officer", "email": "a.lindqvist@nordicbiopolymers.se"},
        "potential_temporary_questions": [
            "When we met in Stockholm in June, you had questions regarding Tamil Nadu Pollution Control Board effluent norms for lignin extraction—has your technical team reviewed our advisory memo?",
            "Are you still in discussions with packaging partners in Coimbatore for your bio-binder formulation line?",
            "Would you like Acclime to arrange a structured consultation with state industrial development officials in SIPCOT Tamil Nadu?",
            "How can we help restart your India entry evaluation as sustainable packaging demand surges in 2026?"
        ]
    },
    {
        "id": "EUR-053",
        "company_name": "Gothenburg Heavy Electrics AB",
        "country": "Sweden (Gothenburg)",
        "sector": "Automotive",
        "revenue_eur_m": 430,
        "met_last_year": True,
        "meeting_date_last_year": "2025-09-12",
        "last_year_discussion_summary": "Met VP Strategy Henrik Larsson. Heavy commercial vehicle charging pantographs and high-output DC fast chargers. Preparing pilot with Indian logistics corridors (Delhi-Mumbai expressway).",
        "current_status": "Met Last Year - Active Pipeline",
        "key_contact": {"name": "Henrik Larsson", "role": "VP Strategy & Expansion", "email": "h.larsson@gothenburg-electrics.se"},
        "potential_temporary_questions": [
            "Following our September meeting, has the National Highways Authority of India (NHAI) expressway fast-charging pilot moved into formal commercial contracting?",
            "Have you finalized your Indian entity structure for operating EV charging infrastructure concessions?",
            "Do you require Acclime assistance with central goods and services tax (GST) registrations across multiple Indian states?",
            "Are you planning to deploy Swedish personnel to India, and do you require business visa facilitation and employment permit support?"
        ]
    },
    {
        "id": "EUR-054",
        "company_name": "Stockholm MedDiagnostics AB",
        "country": "Sweden (Stockholm)",
        "sector": "MedTech",
        "revenue_eur_m": 94,
        "met_last_year": True,
        "meeting_date_last_year": "2025-11-12",
        "last_year_discussion_summary": "Met Chief Commercial Officer Malin Engström. AI-powered diagnostic ultrasound imaging software and handheld probes. Planning to establish an AI research and clinical validation lab in Bengaluru.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Malin Engström", "role": "Chief Commercial Officer", "email": "m.engstrom@stockholm-meddiagnostics.se"},
        "potential_temporary_questions": [
            "When we met in November, you intended to incorporate your Bengaluru AI software laboratory by Q1 2026—are we ready to submit the name approval with the MCA?",
            "Have you finalized the employment contracts and IP assignment deeds for your initial team of 15 Indian computer vision engineers?",
            "What is the status of your institutional review board (IRB) clinical trial clearances with partner medical colleges in Karnataka?",
            "Would you like Acclime to execute the complete company incorporation and statutory payroll onboarding for your Swedish-Indian entity?"
        ]
    },
    {
        "id": "EUR-055",
        "company_name": "Malmö Industrial Robotics AB",
        "country": "Sweden (Malmö)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 175,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Collaborative robots (cobots) for electronics and pharmaceutical cleanroom packaging. Indian pharma manufacturing hubs in Telangana and Gujarat represent enormous demand.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Björn Sundström", "role": "Director Global Sales", "email": "b.sundstrom@malmorobotics.se"},
        "potential_temporary_questions": [
            "With Indian pharmaceutical majors automating packaging lines under US FDA compliance pressure, how are your cleanroom cobots deployed in India?",
            "Have you considered establishing a demonstration and training academy in Hyderabad or Ahmedabad to showcase your robotic applications?",
            "What is your distributor commission and margins structure for the Indian sub-continent?",
            "Can Acclime provide guidance on setting up an Indian private limited subsidiary to bill clients locally in INR?"
        ]
    },
    {
        "id": "EUR-056",
        "company_name": "Västerås CleanGrid Solutions AB",
        "country": "Sweden (Västerås)",
        "sector": "Cleantech",
        "revenue_eur_m": 260,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Grid-scale battery energy storage systems (BESS) and energy management software. India has launched gigawatt-hour BESS tenders under the Ministry of Power.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Karin Lindholm", "role": "VP International Growth", "email": "k.lindholm@vasteras-cleangrid.se"},
        "potential_temporary_questions": [
            "Are you bidding on the Solar Energy Corporation of India (SECI) 1,200 MW standalone Battery Energy Storage Systems (BESS) tenders?",
            "Have you evaluated partnering with Indian EPC giants (L&T, Tata Power Solar) for localized containerized battery assembly?",
            "What legal protections do you need for your proprietary battery management system (BMS) firmware under Indian law?",
            "Could Acclime provide a strategic briefing on tender qualifying parameters and corporate establishment requirements for foreign clean energy bidders?"
        ]
    },
    {
        "id": "EUR-057",
        "company_name": "Uppsala BioProcess Software AB",
        "country": "Sweden (Uppsala)",
        "sector": "SaaS",
        "revenue_eur_m": 48,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Bioreactor process optimization SaaS utilizing digital twin simulation. High relevance for Serum Institute, Biocon, and Indian vaccine manufacturers.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Fredrik Eklund", "role": "Head of Strategic Accounts", "email": "f.eklund@uppsalabioprocess.se"},
        "potential_temporary_questions": [
            "Given that India produces over 60% of the world's vaccines, what is your engagement level with vaccine giants like Serum Institute, Bharat Biotech, and Biocon?",
            "Are you offering on-premise deployments or cloud SaaS, and how are you addressing Indian data sovereignty requirements for proprietary bioprocess data?",
            "Have you considered establishing an Indian consulting branch to provide specialized bio-informatics process engineering?",
            "Can Acclime walk your finance team through Indian cross-border royalty withholding tax and GST implications for your enterprise software licenses?"
        ]
    },
    {
        "id": "EUR-058",
        "company_name": "Scania Precision Fasteners AB",
        "country": "Sweden (Södertälje)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 120,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. High-tensile fasteners for heavy commercial trucks and railway bogies. India's Vande Bharat train expansion and dedicated freight corridors provide huge volume opportunities.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Magnus Nyström", "role": "Chief Operating Officer", "email": "m.nystrom@scaniafasteners.se"},
        "potential_temporary_questions": [
            "Are you supplying specialized vibration-resistant fasteners to Indian Railways for the Vande Bharat and freight locomotive rolling stock programs?",
            "Have you evaluated setting up a cold forging manufacturing plant in the Haryana or Maharashtra industrial corridors?",
            "What are your biggest hurdles in passing Indian Research Designs and Standards Organisation (RDSO) vendor registration?",
            "Would you appreciate an introductory consultation with Acclime India on manufacturing FDI regulations and railway vendor approvals?"
        ]
    },

    # --- ITALY (8 companies: 4 met, 4 unmet) ---
    {
        "id": "EUR-059",
        "company_name": "Lombardia Polimeri Speciali SpA",
        "country": "Italy (Milan)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 380,
        "met_last_year": True,
        "meeting_date_last_year": "2025-05-28",
        "last_year_discussion_summary": "Met Managing Director Matteo Rossi in Milan. Engineering fluoropolymers and high-performance sealing compounds. Exploring setting up a compounding plant in Maharashtra. Concerns regarding Indian chemical import duties and local director requirements.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Matteo Rossi", "role": "Managing Director", "email": "m.rossi@lombardiapolimeri.it"},
        "potential_temporary_questions": [
            "When we met in Milan last May, you were assessing whether to import raw resin or establish local compounding in MIDC Maharashtra—what is the board's decision for 2026?",
            "Have your corporate advisors resolved the resident Indian nominee director requirement, or would you like Acclime to provide our corporate director service?",
            "Are you tracking the changes in basic customs duties (BCD) on imported fluoropolymer raw materials in the latest Indian budget?",
            "Can we prepare a draft timeline and regulatory milestone roadmap for incorporating your Indian private limited company within 30 days?"
        ]
    },
    {
        "id": "EUR-060",
        "company_name": "Bologna Packaging Automation SpA",
        "country": "Italy (Bologna)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 290,
        "met_last_year": True,
        "meeting_date_last_year": "2025-10-17",
        "last_year_discussion_summary": "Met Commercial Director Gianluca Conti in Bologna. High-speed blister packaging and aseptic filling lines for pharmaceuticals. Intends to open an Indian technical service and assembly center in Hyderabad.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Gianluca Conti", "role": "Commercial Director", "email": "g.conti@bolognapackaging.it"},
        "potential_temporary_questions": [
            "Following our October meeting in Bologna, have you finalized the location for your Hyderabad technical service and spare parts center?",
            "Are you ready for Acclime to initiate company incorporation and tax registrations under the Telangana State Industrial Project Approval System (TS-iPASS)?",
            "What is your target headcount for Indian field service technicians for the initial 12 months?",
            "Do you require assistance in drafting employment contracts, employee handbook policies, and statutory provident fund (PF) enrollments?"
        ]
    },
    {
        "id": "EUR-061",
        "company_name": "Torino Powertrain Tech SpA",
        "country": "Italy (Turin)",
        "sector": "Automotive",
        "revenue_eur_m": 350,
        "met_last_year": True,
        "meeting_date_last_year": "2025-07-09",
        "last_year_discussion_summary": "Met CEO Alessandro Moretti. Transmission systems and hybrid gearboxes. Discussing technology transfer and licensing with Indian automotive Tier-1 supplier. Required transfer pricing structuring.",
        "current_status": "Met Last Year - Active Pipeline",
        "key_contact": {"name": "Alessandro Moretti", "role": "Chief Executive Officer", "email": "a.moretti@torinopowertrain.it"},
        "potential_temporary_questions": [
            "Following our July discussions on cross-border IP licensing royalties from Turin to India, has your finance committee approved the proposed transfer pricing structure?",
            "Have you signed the technical collaboration term sheet with the Pune-based automotive Tier-1 partner?",
            "Do you need Acclime to review the draft agreement for compliance with Indian foreign exchange regulations (FEMA) and withholding tax optimization?",
            "What is your planned launch date for pilot hybrid gearbox production lines in India?"
        ]
    },
    {
        "id": "EUR-062",
        "company_name": "Veneto BioMedica SpA",
        "country": "Italy (Padua)",
        "sector": "MedTech",
        "revenue_eur_m": 82,
        "met_last_year": True,
        "meeting_date_last_year": "2025-04-18",
        "last_year_discussion_summary": "Met VP International Sales Chiara Ferrari. Hemodialysis equipment and disposable dialyzers. Evaluating supply to India's Pradhan Mantri National Dialysis Programme. Paused due to tender pricing caps.",
        "current_status": "Met Last Year - Paused",
        "key_contact": {"name": "Chiara Ferrari", "role": "VP International Sales", "email": "c.ferrari@venetobiomedica.it"},
        "potential_temporary_questions": [
            "In our April meeting, you expressed concern regarding government tender price caps under the National Dialysis Programme—have your margin targets adapted?",
            "Are you considering setting up a local assembly unit in India to bring down landed costs and qualify for domestic bidder preference?",
            "Would you like an updated market report on private dialysis clinic chains (NephroPlus, Apex Kidney Care) expanding across tier-2 Indian cities?",
            "Can Acclime structure a low-risk liaison office or agency validation framework for your executive team?"
        ]
    },
    {
        "id": "EUR-063",
        "company_name": "Toscana CleanEnergy Solutions SpA",
        "country": "Italy (Florence)",
        "sector": "Cleantech",
        "revenue_eur_m": 140,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Geothermal turbomachinery and industrial heat recovery systems. Target for Indian heavy industry and oil & gas decarbonization projects.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Lorenzo Ricci", "role": "Director BD & Strategy", "email": "l.ricci@toscanacleanenergy.it"},
        "potential_temporary_questions": [
            "With Indian public sector energy majors (ONGC, IOCL) piloting geothermal exploration in Ladakh and Himachal Pradesh, are you tracking these bids?",
            "What is your strategy for supplying high-temperature waste heat recovery ORC turbines to Indian steel and cement plants?",
            "Have you evaluated partnering with Indian heavy engineering EPC contractors for local equipment skid fabrication?",
            "Can Acclime provide intelligence on public sector undertaking (PSU) vendor pre-qualification criteria in India?"
        ]
    },
    {
        "id": "EUR-064",
        "company_name": "Emilia Logistics AI SpA",
        "country": "Italy (Parma)",
        "sector": "SaaS",
        "revenue_eur_m": 58,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Automated cold chain temperature monitoring and pharmaceutical track-and-trace SaaS. India's pharma export cold chain is undergoing major regulatory modernization.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Paola De Luca", "role": "Head of Strategic Growth", "email": "p.deluca@emilialogistics.it"},
        "potential_temporary_questions": [
            "With India's export pharmaceutical supply chain implementing mandatory 2D barcoding and cold chain temperature logging, how are you approaching Indian pharma exporters?",
            "Are you considering integrating your IoT SaaS platform with Indian cold chain logistics operators (Snowman, Coldman)?",
            "What is your strategy for complying with Indian telecom (DoT) M2M SIM card regulations for your IoT sensor hardware?",
            "Could Acclime advise your team on cross-border recurring SaaS billing, GST reverse charge mechanisms, and local entity incorporation?"
        ]
    },
    {
        "id": "EUR-065",
        "company_name": "Bergamo Valve Technologies SpA",
        "country": "Italy (Bergamo)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 165,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Subsea valves and cryogenic LNG valves. Huge demand in India's expanding city gas distribution (CGD) networks and LNG import terminals.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Andrea Fontana", "role": "VP Global Sales", "email": "a.fontana@bergamovalves.it"},
        "potential_temporary_questions": [
            "As India expands city gas distribution (CGD) licenses to cover 98% of the population, are you supplying cryogenic ball valves to Indian gas utilities?",
            "Have you explored setting up an assembly and hydrostatic testing facility in the Dahej or Hazira LNG corridor?",
            "What are your requirements for obtaining PESO approvals and Indian Boiler Regulations (IBR) certification for your valve lineup?",
            "Would you welcome a guidance briefing from Acclime India on energy sector procurement norms and corporate subsidiary formation?"
        ]
    },
    {
        "id": "EUR-066",
        "company_name": "Modena Racing Composites SpA",
        "country": "Italy (Modena)",
        "sector": "Automotive",
        "revenue_eur_m": 92,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Carbon fiber structural components for high-performance sports cars and luxury electric vehicles. Potential design and tooling partnership for Indian premium EV initiatives.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Marco Benetti", "role": "Managing Director", "email": "m.benetti@modenacomposites.it"},
        "potential_temporary_questions": [
            "Are you exploring carbon composite engineering partnerships with Indian luxury EV concepts or motorsport engineering teams?",
            "Have you considered tapping India's composite tooling and precision autoclave facilities to lower production tooling costs?",
            "What is your IP licensing strategy when transferring proprietary resin infusion techniques overseas?",
            "Can Acclime assist in screening potential Indian composite manufacturing partners and drafting protective non-disclosure agreements?"
        ]
    },

    # --- SPAIN (6 companies: 3 met, 3 unmet) ---
    {
        "id": "EUR-067",
        "company_name": "Catalunya Química Fina SA",
        "country": "Spain (Barcelona)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 260,
        "met_last_year": True,
        "meeting_date_last_year": "2025-06-11",
        "last_year_discussion_summary": "Met Chief Operating Officer Carles Puig in Barcelona. Active pharmaceutical ingredients (APIs) and advanced intermediates. Looking to secure an Indian raw material manufacturing base to bypass Chinese supply vulnerabilities.",
        "current_status": "Met Last Year - Active Pipeline",
        "key_contact": {"name": "Carles Puig", "role": "Chief Operating Officer", "email": "c.puig@catalunyaquimica.es"},
        "potential_temporary_questions": [
            "Following our June discussion on de-risking your European API synthesis from Chinese precursor dependencies, have you finalized target acquisition targets in India?",
            "Have you evaluated the Bulk Drug Park incentive scheme in Gujarat and Andhra Pradesh for your planned greenfield chemical synthesis unit?",
            "Would you like Acclime to conduct legal and environmental due diligence on the shortlisted API manufacturing sites in Ankleshwar?",
            "Can we provide an updated memorandum on the 15% corporate tax rate applicability for your Indian manufacturing entity?"
        ]
    },
    {
        "id": "EUR-068",
        "company_name": "Bilbao Heavy Machining SA",
        "country": "Spain (Bilbao)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 210,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Heavy gantry milling machines and railway wheel lathes. Exploring market entry into India to supply Indian Railways modernization tenders; prime fit for Acclime JV advisory and entity setup.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Iñigo Ortiz", "role": "Managing Director", "email": "i.ortiz@bilbaomachining.es"},
        "potential_temporary_questions": [
            "Are you evaluating the 50% minimum local content (Class-I local supplier) threshold required for Indian Railways public procurement bids?",
            "What is your strategy for partnering with an established Indian machine tool builder in Pune or Coimbatore?",
            "Would you like Acclime to conduct preliminary partner vetting and draft a protective JV term sheet with deadlock safeguards?",
            "Can we prepare a strategic assessment on establishing a 100% owned Indian subsidiary versus a joint venture structure?"
        ]
    },
    {
        "id": "EUR-069",
        "company_name": "Valencia SolarTech Renovables SA",
        "country": "Spain (Valencia)",
        "sector": "Cleantech",
        "revenue_eur_m": 180,
        "met_last_year": True,
        "meeting_date_last_year": "2025-08-20",
        "last_year_discussion_summary": "Met Investment Director Lucía Morales. Single-axis solar tracking systems. Considering a 2GW tracker manufacturing plant in Rajasthan. Paused pending resolution of Indian steel price volatility.",
        "current_status": "Met Last Year - Paused",
        "key_contact": {"name": "Lucía Morales", "role": "Investment Director", "email": "l.morales@valenciasolartech.es"},
        "potential_temporary_questions": [
            "Since our August discussion regarding domestic steel sourcing for tracker torque tubes, has your procurement team reviewed current Indian domestic steel prices?",
            "Are you tracking the latest Ministry of New and Renewable Energy (MNRE) Approved List of Models and Manufacturers (ALMM) updates for solar components?",
            "Could Acclime present an updated bonded warehouse (MOOWR) feasibility analysis to mitigate import duties on tracker slew drives and motors?",
            "What timeline is your investment committee contemplating for re-evaluating the Rajasthan manufacturing hub in 2026?"
        ]
    },
    {
        "id": "EUR-070",
        "company_name": "Madrid MedDiagnostics SA",
        "country": "Spain (Madrid)",
        "sector": "MedTech",
        "revenue_eur_m": 65,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Rapid molecular diagnostics for hospital-acquired infections (HAIs). Tremendous demand across Indian private hospital networks seeking antimicrobial stewardship.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Dr. Fernando Ruiz", "role": "Chief Scientific Officer", "email": "f.ruiz@madridmeddiagnostics.es"},
        "potential_temporary_questions": [
            "With Indian hospital chains prioritizing antimicrobial resistance (AMR) control, what is your commercial roadmap for rapid diagnostic cartidges in India?",
            "Who currently acts as your Indian Authorized Representative (AR) for CDSCO medical device registration?",
            "Have you explored setting up an Indian distribution subsidiary to capture full distributor margins rather than using third-party importers?",
            "Can Acclime provide a clear briefing on CDSCO regulatory pathways and corporate tax optimization for European medical diagnostics firms?"
        ]
    },
    {
        "id": "EUR-071",
        "company_name": "Barcelona Mobility Cloud SL",
        "country": "Spain (Barcelona)",
        "sector": "SaaS",
        "revenue_eur_m": 42,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Smart urban transit ticketing and MaaS (Mobility as a Service) fleet software. India's National Common Mobility Card (NCMC) rollout across 30+ metro systems presents massive opportunities.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Jordi Serra", "role": "VP Global Expansion", "email": "j.serra@barcelonamobility.es"},
        "potential_temporary_questions": [
            "With over 30 Indian cities modernizing urban transit under the National Common Mobility Card (NCMC) initiative, are you partnering with Indian metro rail corporations?",
            "How do your API microservices comply with the Reserve Bank of India's transit payment gateway tokenization standards?",
            "Have you evaluated establishing an engineering development hub in Pune or Bengaluru to customize software for APAC transit authorities?",
            "Can Acclime advise on corporate structure, intellectual property licensing, and Indian corporate tax compliance for your software solutions?"
        ]
    },
    {
        "id": "EUR-072",
        "company_name": "Zaragoza AutoStamping SA",
        "country": "Spain (Zaragoza)",
        "sector": "Automotive",
        "revenue_eur_m": 240,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Hot-stamped ultra-high-strength steel structural auto components. High interest from Indian automotive OEMs aiming to meet higher Bharat NCAP crash safety ratings.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Manuel Navarro", "role": "Chief Operating Officer", "email": "m.navarro@zaragoza-autostamping.es"},
        "potential_temporary_questions": [
            "With the rollout of mandatory Bharat NCAP crash safety ratings pushing Indian automakers toward high-strength steel hot stamping, what is your Indian market entry plan?",
            "Are you supplying or in dialogue with Indian auto leaders like Tata Motors, Mahindra, or Maruti Suzuki?",
            "Have you evaluated acquiring an Indian automotive stamping facility or forming a technical joint venture in the Sanand or Chakan auto corridors?",
            "Would you appreciate an introductory Acclime consultation on auto component FDI, factory setup incentives, and environmental clearances?"
        ]
    },

    # --- BELGIUM (4 companies: 2 met, 2 unmet) ---
    {
        "id": "EUR-073",
        "company_name": "Antwerp Speciality Resins NV",
        "country": "Belgium (Antwerp)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 280,
        "met_last_year": True,
        "meeting_date_last_year": "2025-11-09",
        "last_year_discussion_summary": "Met Chief Executive Officer Jan De Smet in Antwerp. Epoxy curing agents and high-performance resins for wind turbine blades. Evaluating an Indian production facility in Gujarat or Tamil Nadu to supply wind turbine OEM factories. Needed factory licensing roadmap.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Jan De Smet", "role": "Chief Executive Officer", "email": "j.desmet@antwerpresins.be"},
        "potential_temporary_questions": [
            "When we met in Antwerp in November, you were comparing Gujarat vs Tamil Nadu for your wind blade epoxy plant—has your location committee chosen a site?",
            "Have your engineers reviewed the State Pollution Control Board Consent to Establish (CTE) checklist we assembled for chemical resin synthesis?",
            "Are you ready for Acclime to handle your company incorporation and state industrial land allotment application with GIDC or SIPCOT?",
            "How does your executive team plan to utilize India's 15% corporate tax rate for new manufacturing setups before the March statutory deadline?"
        ]
    },
    {
        "id": "EUR-074",
        "company_name": "Gent BioPharma Engineering NV",
        "country": "Belgium (Ghent)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 155,
        "met_last_year": True,
        "meeting_date_last_year": "2025-06-30",
        "last_year_discussion_summary": "Met Head of APAC Development Marc Claes. Cleanroom stainless steel modular skids and bioprocess purification columns. Supplying Indian biopharma leaders in Bengaluru and Hyderabad.",
        "current_status": "Met Last Year - Active Pipeline",
        "key_contact": {"name": "Marc Claes", "role": "Head of APAC Development", "email": "m.claes@gent-biopharma.be"},
        "potential_temporary_questions": [
            "Following our June discussion on servicing biopharma clients in Genome Valley Hyderabad, have you finalized the charter for your Indian engineering support team?",
            "Do you require Acclime assistance with STPI / SEZ registration and opening corporate banking facilities in Hyderabad?",
            "What is your timeline for deploying Belgian technical specialists to supervise skid installations in Indian vaccine manufacturing facilities?",
            "Can we prepare a comprehensive guide on expatriate taxation and Indian business visa compliance for your visiting engineering team?"
        ]
    },
    {
        "id": "EUR-075",
        "company_name": "Leuven NanoSensor Technologies NV",
        "country": "Belgium (Leuven)",
        "sector": "MedTech",
        "revenue_eur_m": 62,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Silicon-photonic biosensors for early cancer marker screening. IMEC spin-out seeking low-cost software and clinical validation partnerships in India.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Dr. Sophie Wouters", "role": "VP Strategic Innovation", "email": "s.wouters@leuven-nanosensor.be"},
        "potential_temporary_questions": [
            "Are you considering setting up an Indian software development and clinical data annotation pod in Bengaluru to support your photonics platform?",
            "Have you explored clinical trial collaborations with leading Indian oncology research institutes such as Tata Memorial Centre?",
            "How do you plan to protect your proprietary silicon photonics intellectual property during international clinical validations?",
            "Can Acclime advise your management team on structuring an Indian R&D wholly owned subsidiary and optimizing cross-border research funding?"
        ]
    },
    {
        "id": "EUR-076",
        "company_name": "Brussels EnergyStorage Systems NV",
        "country": "Belgium (Brussels)",
        "sector": "Cleantech",
        "revenue_eur_m": 110,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Flow batteries for long-duration industrial energy storage. Extremely suitable for round-the-clock (RTC) renewable energy projects in India.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Luc Van Acker", "role": "Chief Commercial Officer", "email": "l.vanacker@brussels-energystorage.be"},
        "potential_temporary_questions": [
            "With the Indian Ministry of Power mandating Round-The-Clock (RTC) renewable power tenders, how is your vanadium redox flow battery positioning against lithium-ion?",
            "Have you evaluated partnering with Indian renewable developers (ReNew, Greenko) for a grid-scale pilot demonstration?",
            "What are your requirements for setting up an electrolyte chemical blending facility in India to avoid shipping heavy liquid chemicals from Europe?",
            "Would you appreciate an Acclime strategic briefing on Indian clean energy policies, government tenders, and corporate establishment?"
        ]
    },

    # --- DENMARK (4 companies: 2 met, 2 unmet) ---
    {
        "id": "EUR-077",
        "company_name": "Copenhagen BioEnzyme Solutions A/S",
        "country": "Denmark (Copenhagen)",
        "sector": "Specialty Chemicals",
        "revenue_eur_m": 390,
        "met_last_year": True,
        "meeting_date_last_year": "2025-10-02",
        "last_year_discussion_summary": "Met Chief Scientific Officer Dr. Mette Holm in Copenhagen. Industrial bio-enzymes for bio-fuels, textiles, and detergent manufacturing. Expanding Indian technical application laboratory in Pune and planning a bio-fermentation pilot plant. Required factory safety permits roadmap.",
        "current_status": "Met Last Year - Follow-up Due",
        "key_contact": {"name": "Dr. Mette Holm", "role": "Chief Scientific Officer", "email": "m.holm@copenhagen-bioenzyme.dk"},
        "potential_temporary_questions": [
            "When we met in Copenhagen in October, you were reviewing land lease terms for an expanded fermentation pilot in MIDC Pune—has the board granted final capex approval?",
            "Have your technical directors reviewed the environmental clearance and pollution control consent checklist Acclime assembled for industrial fermentation?",
            "Are you ready for Acclime to coordinate factory license approvals, building plan sanctions, and state water allocation clearances?",
            "Do you require assistance in drafting employment contracts and transfer pricing agreements for your Danish expatriate scientists stationed in Pune?"
        ]
    },
    {
        "id": "EUR-078",
        "company_name": "Aarhus Marine Wind Systems A/S",
        "country": "Denmark (Aarhus)",
        "sector": "Cleantech",
        "revenue_eur_m": 460,
        "met_last_year": True,
        "meeting_date_last_year": "2025-05-15",
        "last_year_discussion_summary": "Met VP Commercial Operations Lars Rasmussen. Offshore wind turbine electrical subsystems and condition monitoring software. Bidding on India's offshore wind tenders off Tamil Nadu and Gujarat. Needed tender qualification advisory.",
        "current_status": "Met Last Year - Active Pipeline",
        "key_contact": {"name": "Lars Rasmussen", "role": "VP Commercial Operations", "email": "l.rasmussen@aarhus-wind.dk"},
        "potential_temporary_questions": [
            "Following our May advisory regarding the Ministry of New and Renewable Energy (MNRE) offshore wind tenders off Tamil Nadu, are your consortium arrangements locked in?",
            "Have you finalized the establishment of your Chennai project office to coordinate port logistics at V.O. Chidambaranar Port in Tuticorin?",
            "Do you require Acclime guidance on navigating Indian maritime cabotage regulations and foreign flag vessel clearances for offshore geotechnical surveys?",
            "Can we prepare an executive tax advisory memo on Permanent Establishment (PE) mitigation for your offshore engineering personnel?"
        ]
    },
    {
        "id": "EUR-079",
        "company_name": "Odense Robotic Automation A/S",
        "country": "Denmark (Odense)",
        "sector": "Industrial Manufacturing",
        "revenue_eur_m": 135,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Heavy industrial mobile robots and autonomous internal logistics vehicles. High potential in Indian automotive assembly and electronics megaplants.",
        "current_status": "Not Met - High Priority",
        "key_contact": {"name": "Søren Møller", "role": "Director Global BD", "email": "s.moller@odense-robotics.dk"},
        "potential_temporary_questions": [
            "With massive automotive and electronics plants scaling in Tamil Nadu and Gujarat, how are your autonomous mobile robots (AMRs) addressing factory intralogistics?",
            "Have you evaluated establishing an Indian training and demonstration robotics center in Pune or Bengaluru?",
            "What is your current strategy for providing SLA-backed 24/7 technical field support to Indian manufacturing clients?",
            "Can Acclime provide guidance on fast-track Indian entity incorporation, GST compliance, and local distributor vetting?"
        ]
    },
    {
        "id": "EUR-080",
        "company_name": "Nordic MedDevice Diagnostics A/S",
        "country": "Denmark (Aalborg)",
        "sector": "MedTech",
        "revenue_eur_m": 58,
        "met_last_year": False,
        "meeting_date_last_year": None,
        "last_year_discussion_summary": "Unmet target. Non-invasive point-of-care hemoglobin and bilirubin photometers for neonatal and maternal care. Perfect match for India's National Health Mission maternal health procurement.",
        "current_status": "Not Met - Cold",
        "key_contact": {"name": "Kirsten Nørgaard", "role": "Chief Commercial Officer", "email": "k.norgaard@nordicmeddevice.dk"},
        "potential_temporary_questions": [
            "Are you targeting Indian government maternal and child health procurement tenders under the National Health Mission (NHM)?",
            "What CDSCO medical device registration steps have you completed for your non-invasive photometers in India?",
            "Have you considered partnering with Indian medical device manufacturing concessionaires to meet public procurement domestic value addition quotas?",
            "Would you be open to an Acclime India consultation on regulatory registration, distributor screening, and healthcare market entry strategy?"
        ]
    }
]

def init_db():
    print(f"Total companies in dataset: {len(COMPANIES)}")
    
    # Validation checks
    met_count = sum(1 for c in COMPANIES if c["met_last_year"])
    unmet_count = sum(1 for c in COMPANIES if not c["met_last_year"])
    followup_count = sum(1 for c in COMPANIES if c["current_status"] == "Met Last Year - Follow-up Due")
    
    print(f"Validation: Met Last Year: {met_count} (Expected: 35)")
    print(f"Validation: Not Met: {unmet_count} (Expected: 45)")
    print(f"Validation: Met Last Year - Follow-up Due: {followup_count} (Expected: 18)")
    
    assert len(COMPANIES) == 80, f"Expected 80 companies, got {len(COMPANIES)}"
    assert met_count == 35, f"Expected 35 met companies, got {met_count}"
    assert unmet_count == 45, f"Expected 45 unmet companies, got {unmet_count}"
    assert followup_count == 18, f"Expected 18 follow-up due companies, got {followup_count}"
    
    # Save JSON fallback
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(COMPANIES, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON database to {JSON_PATH}")

    # Save SQLite database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("DROP TABLE IF EXISTS companies")
    cur.execute("""
    CREATE TABLE companies (
        id TEXT PRIMARY KEY,
        company_name TEXT NOT NULL,
        country TEXT NOT NULL,
        sector TEXT NOT NULL,
        revenue_eur_m REAL NOT NULL,
        met_last_year INTEGER NOT NULL,
        meeting_date_last_year TEXT,
        last_year_discussion_summary TEXT NOT NULL,
        current_status TEXT NOT NULL,
        key_contact_name TEXT NOT NULL,
        key_contact_role TEXT NOT NULL,
        key_contact_email TEXT NOT NULL,
        potential_temporary_questions TEXT NOT NULL
    )
    """)
    
    for c in COMPANIES:
        cur.execute("""
        INSERT INTO companies (
            id, company_name, country, sector, revenue_eur_m,
            met_last_year, meeting_date_last_year, last_year_discussion_summary,
            current_status, key_contact_name, key_contact_role, key_contact_email,
            potential_temporary_questions
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["id"],
            c["company_name"],
            c["country"],
            c["sector"],
            c["revenue_eur_m"],
            1 if c["met_last_year"] else 0,
            c["meeting_date_last_year"],
            c["last_year_discussion_summary"],
            c["current_status"],
            c["key_contact"]["name"],
            c["key_contact"]["role"],
            c["key_contact"]["email"],
            json.dumps(c["potential_temporary_questions"])
        ))
        
    # Create useful indexes for fast search and query
    cur.execute("CREATE INDEX idx_met ON companies(met_last_year)")
    cur.execute("CREATE INDEX idx_sector ON companies(sector)")
    cur.execute("CREATE INDEX idx_country ON companies(country)")
    cur.execute("CREATE INDEX idx_status ON companies(current_status)")
    cur.execute("CREATE INDEX idx_revenue ON companies(revenue_eur_m)")
    
    conn.commit()
    conn.close()
    print(f"Saved SQLite database with {len(COMPANIES)} rows to {DB_PATH}")

if __name__ == "__main__":
    init_db()
