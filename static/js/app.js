/**
 * Acclime EuroTrack — Frontend Logic (Vibrant Edition)
 */

let allCompanies      = [];
let filteredCompanies = [];
let selectedCompany   = null;
let currentQuestionContext = "Post-Last-Year Re-engagement";
let currentView       = "table";
let sortField         = "id";
let sortOrder         = "asc";

let filterMetStatus = "All";
let filterCountry   = "All";
let filterSector    = "All";
let filterStatus    = "All";
let filterSearch    = "";

let countryChart = null;
let sectorChart  = null;

document.addEventListener("DOMContentLoaded", () => {
  loadKPIs();
  loadCompanies().then(() => initCharts());
});

// ─── DATA LOADING ─────────────────────────────────────────────

async function loadKPIs() {
  try {
    const r = await fetch("/api/kpi");
    const d = await r.json();
    document.getElementById("kpiTotal").textContent    = d.total_companies;
    document.getElementById("kpiMet").textContent      = d.met_last_year;
    document.getElementById("kpiUnmet").textContent    = d.not_met_yet;
    document.getElementById("kpiFollowup").textContent = d.followup_due;
  } catch (e) { console.error(e); }
}

async function loadCompanies() {
  try {
    const r = await fetch("/api/companies");
    const d = await r.json();
    allCompanies      = d.companies;
    filteredCompanies = [...allCompanies];
    renderView();
  } catch (e) {
    console.error(e);
    showToast("Failed to load companies", "error");
  }
}

// ─── CHARTS ───────────────────────────────────────────────────

async function initCharts() {
  try {
    const r = await fetch("/api/chart-data");
    const d = await r.json();
    buildCountryChart(d.countries);
    buildSectorChart(d.sectors);
  } catch (e) { console.error(e); }
}

function chartBase() {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top",
        align: "end",
        labels: {
          boxWidth: 10,
          boxHeight: 10,
          font: { size: 11, family: "-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" },
          color: "#64748b"
        }
      },
      tooltip: {
        backgroundColor: "#0f172a",
        titleFont: { size: 11, weight: "700" },
        bodyFont: { size: 11 },
        padding: 10,
        cornerRadius: 6,
        borderColor: "#1e293b",
        borderWidth: 1
      }
    }
  };
}

function buildCountryChart(data) {
  const ctx = document.getElementById("countryChart").getContext("2d");
  if (countryChart) countryChart.destroy();
  const labels = data.map(d => d.country);
  countryChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        { label: "Met (2025)", data: data.map(d => d.met),   backgroundColor: "#2563eb", borderRadius: 4 },
        { label: "Not Met",    data: data.map(d => d.unmet), backgroundColor: "#e2e8f0", borderRadius: 4 }
      ]
    },
    options: {
      ...chartBase(),
      scales: {
        x: { stacked: true, grid: { display: false }, ticks: { font: { size: 10 }, color: "#94a3b8" } },
        y: { stacked: true, beginAtZero: true, grid: { color: "#f1f5f9" }, ticks: { font: { size: 10 }, color: "#94a3b8" } }
      },
      onClick: (_, els) => {
        if (!els.length) return;
        const c = labels[els[0].index];
        document.getElementById("countryFilter").value = c;
        filterCountry = c;
        applyFilters();
        showToast("Filtered: " + c);
      }
    }
  });
}

function buildSectorChart(data) {
  const ctx = document.getElementById("sectorChart").getContext("2d");
  if (sectorChart) sectorChart.destroy();
  const labels = data.map(d => d.sector);
  sectorChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        { label: "Met (2025)", data: data.map(d => d.met),   backgroundColor: "#7c3aed", borderRadius: 4 },
        { label: "Not Met",    data: data.map(d => d.unmet), backgroundColor: "#e2e8f0", borderRadius: 4 }
      ]
    },
    options: {
      ...chartBase(),
      scales: {
        x: { stacked: true, grid: { display: false }, ticks: { font: { size: 10 }, color: "#94a3b8" } },
        y: { stacked: true, beginAtZero: true, grid: { color: "#f1f5f9" }, ticks: { font: { size: 10 }, color: "#94a3b8" } }
      },
      onClick: (_, els) => {
        if (!els.length) return;
        const s = labels[els[0].index];
        document.getElementById("sectorFilter").value = s;
        filterSector = s;
        applyFilters();
        showToast("Filtered: " + s);
      }
    }
  });
}

// ─── FILTERS ──────────────────────────────────────────────────

function applyFilters() {
  filteredCompanies = allCompanies.filter(c => {
    if (filterMetStatus === "met"   && !c.met_last_year) return false;
    if (filterMetStatus === "unmet" &&  c.met_last_year) return false;
    if (filterCountry !== "All" && !c.country.toLowerCase().startsWith(filterCountry.toLowerCase())) return false;
    if (filterSector  !== "All" && c.sector !== filterSector)          return false;
    if (filterStatus  !== "All" && c.current_status !== filterStatus)  return false;
    if (filterSearch.trim()) {
      const q = filterSearch.toLowerCase();
      const fields = [c.company_name, c.country, c.sector, c.id, c.key_contact.name, c.last_year_discussion_summary];
      if (!fields.some(f => f.toLowerCase().includes(q))) return false;
    }
    return true;
  });
  sortCompanies();
  renderView();
  renderFilterTags();
}

function filterByMetStatus(status) {
  filterMetStatus = status;
  ["tabAll", "tabMet", "tabUnmet"].forEach(id => {
    document.getElementById(id).classList.toggle("active", {
      tabAll: "All", tabMet: "met", tabUnmet: "unmet"
    }[id] === status);
  });
  applyFilters();
}

function filterByStatus(name) {
  document.getElementById("statusFilter").value = name;
  filterStatus = name;
  applyFilters();
}

function handleTableSearch() {
  filterSearch = document.getElementById("tableSearch").value;
  applyFilters();
}

function handleDropdownFilter() {
  filterCountry = document.getElementById("countryFilter").value;
  filterSector  = document.getElementById("sectorFilter").value;
  filterStatus  = document.getElementById("statusFilter").value;
  applyFilters();
}

function resetAllFilters() {
  filterMetStatus = "All"; filterCountry = "All";
  filterSector = "All"; filterStatus = "All"; filterSearch = "";
  document.getElementById("tableSearch").value   = "";
  document.getElementById("countryFilter").value = "All";
  document.getElementById("sectorFilter").value  = "All";
  document.getElementById("statusFilter").value  = "All";
  document.getElementById("nlQueryInput").value  = "";
  document.getElementById("clearNLBtn").style.display = "none";
  document.getElementById("aiSummaryBanner").classList.remove("visible");
  filterByMetStatus("All");
}

function renderFilterTags() {
  const wrap = document.getElementById("activeFilterTags");
  const list = document.getElementById("tagsList");
  list.innerHTML = "";

  const tags = [];
  if (filterMetStatus === "met")   tags.push(["Met last year",        "met"]);
  if (filterMetStatus === "unmet") tags.push(["Not met yet",          "unmet"]);
  if (filterCountry !== "All")     tags.push(["Country: " + filterCountry, "country"]);
  if (filterSector  !== "All")     tags.push(["Sector: "  + filterSector,  "sector"]);
  if (filterStatus  !== "All")     tags.push(["Stage: "   + filterStatus,   "status"]);
  if (filterSearch.trim())         tags.push(['"' + filterSearch + '"',      "search"]);

  wrap.classList.toggle("visible", tags.length > 0);
  tags.forEach(([label, key]) => {
    const chip = document.createElement("span");
    chip.className = "filter-chip";
    chip.innerHTML = `${label} <button class="filter-chip-x" onclick="removeTag('${key}')">×</button>`;
    list.appendChild(chip);
  });
}

function removeTag(key) {
  if (key === "met" || key === "unmet") filterByMetStatus("All");
  if (key === "country") { filterCountry = "All"; document.getElementById("countryFilter").value = "All"; }
  if (key === "sector")  { filterSector  = "All"; document.getElementById("sectorFilter").value  = "All"; }
  if (key === "status")  { filterStatus  = "All"; document.getElementById("statusFilter").value  = "All"; }
  if (key === "search")  { filterSearch  = "";    document.getElementById("tableSearch").value   = "";    }
  applyFilters();
}

// ─── SORT ─────────────────────────────────────────────────────

function sortTable(field) {
  sortOrder = (sortField === field && sortOrder === "asc") ? "desc" : "asc";
  sortField = field;
  sortCompanies();
  renderView();
}

function sortCompanies() {
  filteredCompanies.sort((a, b) => {
    let va = a[sortField] ?? "";
    let vb = b[sortField] ?? "";
    if (sortField === "revenue_eur_m") return sortOrder === "asc" ? va - vb : vb - va;
    va = va.toString().toLowerCase();
    vb = vb.toString().toLowerCase();
    if (va < vb) return sortOrder === "asc" ? -1 : 1;
    if (va > vb) return sortOrder === "asc" ?  1 : -1;
    return 0;
  });
}

// ─── BADGE HELPERS ────────────────────────────────────────────

function stageBadge(status) {
  const map = {
    "Met Last Year - Follow-up Due":   ["badge badge-red",    "Follow-up Due"],
    "Met Last Year - Active Pipeline": ["badge badge-blue",   "Active Pipeline"],
    "Met Last Year - Paused":          ["badge badge-gray",   "Paused"],
    "Not Met - High Priority":         ["badge badge-amber",  "High Priority"],
    "Not Met - Cold":                  ["badge badge-purple", "Cold"]
  };
  const [cls, label] = map[status] || ["badge badge-gray", status];
  return `<span class="${cls}">${label}</span>`;
}

function metBadge(c) {
  if (c.met_last_year) {
    return `<span class="badge badge-green">✓ ${c.meeting_date_last_year}</span>`;
  }
  return `<span class="badge badge-gray">Not met</span>`;
}

// ─── RENDERING ────────────────────────────────────────────────

function switchView(view) {
  currentView = view;
  document.getElementById("viewTableBtn").classList.toggle("active", view === "table");
  document.getElementById("viewGridBtn").classList.toggle("active", view === "grid");
  document.getElementById("tableViewContainer").classList.toggle("hidden", view !== "table");
  document.getElementById("gridViewContainer").classList.toggle("hidden", view !== "grid");
  renderView();
}

function renderView() {
  document.getElementById("resultCountText").textContent =
    `${filteredCompanies.length} account${filteredCompanies.length !== 1 ? "s" : ""}`;
  currentView === "table" ? renderTable() : renderGrid();
}

function renderTable() {
  const tbody = document.getElementById("companyTableBody");
  tbody.innerHTML = "";

  if (!filteredCompanies.length) {
    tbody.innerHTML = `<tr class="empty-row"><td colspan="8">No accounts match the current filters. <button onclick="resetAllFilters()" style="color:#2563eb; text-decoration:underline; background:none; border:none; cursor:pointer; font-family:inherit; font-size:12px; font-weight:600;">Reset filters</button></td></tr>`;
    return;
  }

  filteredCompanies.forEach(c => {
    const tr = document.createElement("tr");
    tr.onclick = e => { if (!e.target.closest("button") && !e.target.closest("a")) openDrawer(c.id); };

    const q0 = c.potential_temporary_questions?.[0] ?? "–";

    tr.innerHTML = `
      <td class="col-id">${c.id}</td>
      <td>
        <div class="col-company">${c.company_name}</div>
        <div class="col-sector">${c.sector}</div>
      </td>
      <td style="font-size:12px; color:#475569; white-space:nowrap; font-weight:500;">${c.country}</td>
      <td class="col-revenue">€${c.revenue_eur_m}M</td>
      <td>${metBadge(c)}</td>
      <td>${stageBadge(c.current_status)}</td>
      <td class="col-preview" title="${esc(q0)}">${q0}</td>
      <td class="col-action">
        <button class="btn btn-default" style="font-size:11px;" onclick="openDrawer('${c.id}')">Open →</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function renderGrid() {
  const wrap = document.getElementById("gridViewContainer");
  wrap.innerHTML = "";

  if (!filteredCompanies.length) {
    wrap.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:40px; font-size:13px; color:#94a3b8;">No accounts match the current filters. <button onclick="resetAllFilters()" style="color:#2563eb; text-decoration:underline; background:none; border:none; cursor:pointer; font-family:inherit; font-size:13px; font-weight:600;">Reset</button></div>`;
    return;
  }

  filteredCompanies.forEach(c => {
    const card = document.createElement("div");
    card.className = "grid-card";
    card.onclick = () => openDrawer(c.id);

    const q0 = c.potential_temporary_questions?.[0] ?? "–";

    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
        <span class="grid-card-id">${c.id}</span>
        ${metBadge(c)}
      </div>
      <div class="grid-card-name">${c.company_name}</div>
      <div class="grid-card-meta">
        <span>${c.country}</span>
        <span class="text-mono" style="color:#0f172a; font-weight:700;">€${c.revenue_eur_m}M</span>
      </div>
      <div class="grid-card-preview">${q0}</div>
      <div class="grid-card-footer">
        ${stageBadge(c.current_status)}
        <span style="font-size:11px; color:#94a3b8; font-weight:600;">Open →</span>
      </div>
    `;
    wrap.appendChild(card);
  });
}

// ─── NL QUERY ─────────────────────────────────────────────────

async function handleNLQuery() {
  const q = document.getElementById("nlQueryInput").value.trim();
  if (!q) return;
  document.getElementById("clearNLBtn").style.display = "";
  try {
    const r = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: q })
    });
    const d = await r.json();

    document.getElementById("aiResultBadge").textContent = d.count + " accounts returned";
    document.getElementById("aiSummaryText").innerHTML   = d.ai_summary
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n\n/g, "<br><br>");
    document.getElementById("aiSqlBox").textContent = d.sql_executed + "\n-- params: " + JSON.stringify(d.sql_params);
    document.getElementById("aiSummaryBanner").classList.add("visible");

    filteredCompanies = d.companies;
    renderView();
  } catch (e) {
    console.error(e);
    showToast("Query failed", "error");
  }
}

function quickAsk(text) {
  document.getElementById("nlQueryInput").value = text;
  handleNLQuery();
}

function clearNLQuery() {
  document.getElementById("nlQueryInput").value = "";
  document.getElementById("clearNLBtn").style.display = "none";
  document.getElementById("aiSummaryBanner").classList.remove("visible");
  resetAllFilters();
}

function toggleSQL() {
  document.getElementById("aiSqlBox").classList.toggle("visible");
}

// ─── DRAWER ───────────────────────────────────────────────────

async function openDrawer(id) {
  try {
    const r = await fetch(`/api/companies/${id}`);
    if (!r.ok) throw new Error();
    selectedCompany = await r.json();
    const c = selectedCompany;

    document.getElementById("drawerId").textContent          = c.id;
    document.getElementById("drawerCompanyName").textContent = c.company_name;
    document.getElementById("drawerCountry").textContent     = c.country;
    document.getElementById("drawerSector").textContent      = c.sector;
    document.getElementById("drawerRevenue").textContent     = `€${c.revenue_eur_m}M`;

    // Contact
    document.getElementById("drawerContactName").textContent  = c.key_contact.name;
    document.getElementById("drawerContactRole").textContent  = c.key_contact.role;
    document.getElementById("drawerContactEmail").textContent = c.key_contact.email;
    document.getElementById("drawerContactEmailLink").href    = "mailto:" + c.key_contact.email;

    // Avatar initials
    const parts    = c.key_contact.name.split(" ");
    const initials = parts.filter(p => /[A-Z]/.test(p[0])).map(p => p[0]).slice(0, 2).join("");
    document.getElementById("drawerContactInitials").textContent = initials || "??";

    // Met status
    const metLine = document.getElementById("drawerMetLine");
    const metText = document.getElementById("drawerMetText");
    if (c.met_last_year) {
      metLine.className   = "met-pill is-met";
      metLine.innerHTML   = `<span class="met-dot green"></span><span>Met on ${c.meeting_date_last_year}</span>`;
      document.getElementById("drawerNotesLabel").textContent = "Meeting notes (2025):";
    } else {
      metLine.className   = "met-pill is-unmet";
      metLine.innerHTML   = `<span class="met-dot gray"></span><span>Not met — target account</span>`;
      document.getElementById("drawerNotesLabel").textContent = "Target rationale:";
    }

    document.getElementById("drawerStatusSelect").value   = c.current_status;
    document.getElementById("drawerNotesText").textContent = c.last_year_discussion_summary;

    currentQuestionContext = document.getElementById("questionContextSelect").value;
    await loadAndRenderQuestions();

    document.getElementById("drawerOverlay").classList.add("open");
    document.getElementById("companyDrawer").classList.add("open");
  } catch (e) {
    console.error(e);
    showToast("Could not load account", "error");
  }
}

function closeDrawer() {
  document.getElementById("drawerOverlay").classList.remove("open");
  document.getElementById("companyDrawer").classList.remove("open");
}

async function changeQuestionContext() {
  currentQuestionContext = document.getElementById("questionContextSelect").value;
  await loadAndRenderQuestions();
}

async function loadAndRenderQuestions() {
  const wrap = document.getElementById("drawerQuestionsContainer");
  wrap.innerHTML = `<div style="font-size:12px; color:#94a3b8; padding:8px 0;">Loading...</div>`;
  try {
    const r = await fetch(`/api/companies/${selectedCompany.id}/questions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ context: currentQuestionContext })
    });
    const d = await r.json();
    wrap.innerHTML = "";
    d.questions.forEach((q, i) => {
      const div = document.createElement("div");
      div.className = "q-item";
      div.innerHTML = `
        <div class="q-num">${i + 1} · ${q.tag || "Strategic"}</div>
        <div class="q-text">${q.question}</div>
        ${q.reasoning ? `<div class="q-why">${q.reasoning}</div>` : ""}
        <button class="q-copy-btn" onclick="copyQ('${esc(q.question)}')">copy</button>
      `;
      wrap.appendChild(div);
    });
  } catch (e) {
    wrap.innerHTML = `<div style="font-size:12px; color:#dc2626;">Failed to load questions.</div>`;
  }
}

async function addCustomQuestion() {
  const inp  = document.getElementById("customQuestionInput");
  const text = inp.value.trim();
  if (!text || !selectedCompany) return;
  try {
    const r = await fetch(`/api/companies/${selectedCompany.id}/custom-question`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: text })
    });
    if (r.ok) { inp.value = ""; await loadAndRenderQuestions(); showToast("Question added"); }
  } catch (e) { showToast("Failed to add question", "error"); }
}

async function updateDrawerStatus() {
  if (!selectedCompany) return;
  const status = document.getElementById("drawerStatusSelect").value;
  try {
    await fetch(`/api/companies/${selectedCompany.id}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status })
    });
    selectedCompany.current_status = status;
    const t = allCompanies.find(x => x.id === selectedCompany.id);
    if (t) t.current_status = status;
    applyFilters();
    loadKPIs();
    initCharts();
    showToast("Stage updated");
  } catch (e) { showToast("Failed to update", "error"); }
}

function copyQ(text) {
  navigator.clipboard.writeText(text);
  showToast("Copied to clipboard");
}

function copyAllQuestions() {
  const items = document.querySelectorAll("#drawerQuestionsContainer .q-text");
  const text  = Array.from(items).map((el, i) => `${i + 1}. ${el.textContent}`).join("\n\n");
  navigator.clipboard.writeText(text);
  showToast("All questions copied");
}

// ─── EMAIL MODAL ──────────────────────────────────────────────

async function openEmailModal() {
  if (!selectedCompany) return;
  const questions = Array.from(document.querySelectorAll("#drawerQuestionsContainer .q-text"))
    .map(el => el.textContent);
  try {
    const r = await fetch("/api/draft-email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ company_id: selectedCompany.id, selected_questions: questions, context: currentQuestionContext })
    });
    const d = await r.json();
    document.getElementById("emailToInput").value      = `${d.to_name} <${d.to_email}>`;
    document.getElementById("emailSubjectInput").value = d.subject;
    document.getElementById("emailBodyTextarea").value = d.body;
    const mailto = `mailto:${d.to_email}?subject=${encodeURIComponent(d.subject)}&body=${encodeURIComponent(d.body)}`;
    document.getElementById("emailMailtoBtn").href = mailto;
    document.getElementById("emailModal").classList.add("open");
  } catch (e) { showToast("Failed to generate email", "error"); }
}

function closeEmailModal() { document.getElementById("emailModal").classList.remove("open"); }

function copyEmailBody() {
  navigator.clipboard.writeText(document.getElementById("emailBodyTextarea").value);
  showToast("Email text copied");
}

// ─── TOUR WALKTHROUGH ─────────────────────────────────────────

const tourSteps = [
  {
    step: "STEP 1/6",
    title: "Executive Portfolio & KPI Cards",
    subtitle: "At-a-Glance European Coverage",
    audioSrc: "/static/audio/scene1.mp3",
    graphic: `
      <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:8px; text-align:center;">
        <div style="background:#0f172a; padding:8px; border-radius:6px; border:1px solid #334155;">
          <div style="font-size:10px; color:#94a3b8; font-weight:700;">TOTAL</div>
          <div style="font-size:20px; font-weight:800; color:#fff;">80</div>
        </div>
        <div style="background:#0f172a; padding:8px; border-radius:6px; border:1px solid #16a34a;">
          <div style="font-size:10px; color:#4ade80; font-weight:700;">MET 2025</div>
          <div style="font-size:20px; font-weight:800; color:#4ade80;">35</div>
        </div>
        <div style="background:#0f172a; padding:8px; border-radius:6px; border:1px solid #334155;">
          <div style="font-size:10px; color:#94a3b8; font-weight:700;">UNMET</div>
          <div style="font-size:20px; font-weight:800; color:#cbd5e1;">45</div>
        </div>
        <div style="background:#450a0a; padding:8px; border-radius:6px; border:1px solid #dc2626;">
          <div style="font-size:10px; color:#f87171; font-weight:700;">FOLLOW-UP</div>
          <div style="font-size:20px; font-weight:800; color:#f87171;">18</div>
        </div>
      </div>
    `,
    explanation: "<strong>Where it is:</strong> Top row of the dashboard.<br><strong>What it does:</strong> Displays live counts of Acclime India's European accounts. Exactly 35 were met in 2025, 45 are prospective unmet targets, and 18 have urgent follow-ups due. <em>Tip: Click any card to filter the directory instantly!</em>"
  },
  {
    step: "STEP 2/6",
    title: "'Just Ask' Natural Language Command Bar",
    subtitle: "Ask Any Question in Plain English",
    audioSrc: "/static/audio/scene2.mp3",
    graphic: `
      <div style="background:#0f172a; border:1px solid #3b82f6; border-radius:8px; padding:10px;">
        <div style="font-size:10px; color:#60a5fa; font-weight:700; margin-bottom:4px;">QUERY DATABASE IN NATURAL LANGUAGE</div>
        <div style="background:#1e293b; padding:8px 12px; border-radius:6px; font-size:12px; color:#e2e8f0; font-family:monospace;">
          🔍 "German chemical companies met last year"
        </div>
        <div style="margin-top:6px; font-size:10px; color:#94a3b8;">Presets: Met Last Year (35) · Not Met Yet (45) · Follow-up Due (18)</div>
      </div>
    `,
    explanation: "<strong>Where it is:</strong> The dark navy bar right beneath the KPI cards.<br><strong>What it does:</strong> Uses an entity-extraction engine to turn conversational English questions into parameterized SQL queries in real time. It displays an AI summary banner and filters the companies automatically."
  },
  {
    step: "STEP 3/6",
    title: "Geographic & Industry Analytics",
    subtitle: "Interactive Country & Sector Breakdown",
    audioSrc: "/static/audio/scene3.mp3",
    graphic: `
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:11px;">
        <div style="background:#0f172a; padding:10px; border-radius:6px; border:1px solid #334155;">
          <div style="font-weight:700; color:#cbd5e1; margin-bottom:4px;">Country Coverage</div>
          <div style="color:#94a3b8;">Germany (14) · UK (11) · France (10)...</div>
          <div style="height:6px; background:#2563eb; border-radius:3px; margin-top:6px; width:80%;"></div>
        </div>
        <div style="background:#0f172a; padding:10px; border-radius:6px; border:1px solid #334155;">
          <div style="font-weight:700; color:#cbd5e1; margin-bottom:4px;">Sector Coverage</div>
          <div style="color:#94a3b8;">Chemicals · Mfg · Cleantech · MedTech...</div>
          <div style="height:6px; background:#7c3aed; border-radius:3px; margin-top:6px; width:70%;"></div>
        </div>
      </div>
    `,
    explanation: "<strong>Where it is:</strong> Below the search bar.<br><strong>What it does:</strong> Two stacked bar charts compare companies met in 2025 vs. unmet targets across 10 countries and 6 sectors. <em>Click any bar on either chart to filter the company directory below!</em>"
  },
  {
    step: "STEP 4/6",
    title: "Corporate Directory & Table Controls",
    subtitle: "Search, Multi-Filter, and View Switching",
    audioSrc: "/static/audio/scene4.mp3",
    graphic: `
      <div style="background:#0f172a; border:1px solid #334155; border-radius:6px; padding:10px; font-size:11px;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #334155; padding-bottom:6px; margin-bottom:6px;">
          <span style="font-weight:700; color:#fff;">All (80) · Met (35) · Not Met (45)</span>
          <span style="color:#94a3b8;">Table / Grid Toggle</span>
        </div>
        <div style="display:flex; justify-content:space-between; color:#cbd5e1;">
          <span>EUR-001 Bavaria Katalys Chem AG</span>
          <span style="color:#4ade80; font-weight:700;">✓ Met 2025-09-18</span>
        </div>
      </div>
    `,
    explanation: "<strong>Where it is:</strong> The main directory card.<br><strong>What it does:</strong> Displays each company with ID, location, annual revenue in €M, 2025 meeting status, pipeline stage badge, and talking point preview. You can toggle between <em>Dense Table View</em> and <em>Card Grid View</em>."
  },
  {
    step: "STEP 5/6",
    title: "Account Dossier Drawer & Meeting Memory",
    subtitle: "Deep Account Memory & Discussion Notes",
    audioSrc: "/static/audio/scene5.mp3",
    graphic: `
      <div style="background:#0f172a; border-left:4px solid #2563eb; border-radius:6px; padding:10px; font-size:11px;">
        <div style="font-weight:800; color:#fff; font-size:12px;">Bavaria Katalys Chem AG · €420M</div>
        <div style="color:#4ade80; font-weight:700; margin:4px 0;">✓ Met on 2025-09-18 · Dr. Stefan Weber (CEO)</div>
        <div style="background:#1e293b; padding:6px; border-radius:4px; color:#cbd5e1; font-style:italic;">
          "Met CEO in Oct 2025. Paused India subsidiary due to EU capex tightening. Interested in Gujarat chemical cluster."
        </div>
      </div>
    `,
    explanation: "<strong>Where it is:</strong> Click anywhere on a company row or 'Open' button to slide it open from the right.<br><strong>What it does:</strong> Displays executive contacts, verified email, and detailed 2025 meeting memory. You can update the pipeline stage directly, saving changes back to SQLite."
  },
  {
    step: "STEP 6/6",
    title: "Temporary Questions & Email Drafting",
    subtitle: "Contextual Outreach Ready in Seconds",
    audioSrc: "/static/audio/scene6.mp3",
    graphic: `
      <div style="background:#0f172a; border:1px solid #334155; border-radius:6px; padding:10px; font-size:11px;">
        <div style="color:#60a5fa; font-weight:700;">Angle: Post-Meeting Re-engagement</div>
        <div style="background:#1e293b; padding:6px; border-radius:4px; margin:6px 0; color:#e2e8f0;">
          1. "When we met in October last year, you paused your India entity setup due to EU capex tightening—how are timelines looking for this quarter?"
        </div>
        <div style="display:flex; gap:6px;">
          <span style="background:#2563eb; color:#fff; padding:3px 8px; border-radius:4px; font-weight:700;">Draft Outreach Email</span>
          <span style="background:#334155; color:#cbd5e1; padding:3px 8px; border-radius:4px;">Copy Questions</span>
        </div>
      </div>
    `,
    explanation: "<strong>Where it is:</strong> Section 2 inside the Dossier Drawer.<br><strong>What it does:</strong> Generates 4 tailored talking points. Switch angles (Post-Meeting, 15-Min Check-in, India Entry & Tax, or M&A) to generate new questions. Click <strong>'Draft Outreach Email'</strong> to generate an email with one-click send!"
  }
];

let currentTourIndex = 0;
let isTourVoiceOn = true;
let currentTourAudio = null;

function toggleModalVoice() {
  isTourVoiceOn = !isTourVoiceOn;
  const btn = document.getElementById("modalVoiceBtn");
  if (isTourVoiceOn) {
    btn.textContent = "🔊 Voice: ON";
    btn.style.color = "#60a5fa";
    speakTourStep();
  } else {
    btn.textContent = "🔇 Voice: MUTED";
    btn.style.color = "#94a3b8";
    if (currentTourAudio) currentTourAudio.pause();
    if (window.speechSynthesis) window.speechSynthesis.cancel();
  }
}

function speakTourStep() {
  if (currentTourAudio) {
    currentTourAudio.pause();
    currentTourAudio.currentTime = 0;
  }
  if (!isTourVoiceOn) return;

  const s = tourSteps[currentTourIndex];
  if (s.audioSrc) {
    currentTourAudio = new Audio(s.audioSrc);
    currentTourAudio.play().catch(e => {
      // Fallback to speech synthesis if audio blocked
      if (window.speechSynthesis) {
        const cleanText = (s.title + ". " + s.explanation).replace(/<[^>]*>/g, "").replace(/&[^;]+;/g, " ");
        const utter = new SpeechSynthesisUtterance(cleanText);
        window.speechSynthesis.speak(utter);
      }
    });
  }
}

function openTourModal() {
  currentTourIndex = 0;
  renderTourStep();
  document.getElementById("tourModal").classList.add("open");
  speakTourStep();
}

function closeTourModal() {
  document.getElementById("tourModal").classList.remove("open");
  if (currentTourAudio) currentTourAudio.pause();
  if (window.speechSynthesis) window.speechSynthesis.cancel();
}

function renderTourStep() {
  const s = tourSteps[currentTourIndex];
  document.getElementById("tourStepBadge").textContent = s.step;
  document.getElementById("tourTitle").textContent = s.title;
  document.getElementById("tourSubtitle").textContent = s.subtitle;
  document.getElementById("tourGraphic").innerHTML = s.graphic;
  document.getElementById("tourExplanation").innerHTML = s.explanation;

  document.getElementById("tourPrevBtn").style.visibility = currentTourIndex === 0 ? "hidden" : "visible";
  document.getElementById("tourNextBtn").textContent = currentTourIndex === tourSteps.length - 1 ? "Got it! Close Tour" : "Next →";

  // Dots
  const dotsContainer = document.getElementById("tourDots");
  dotsContainer.innerHTML = tourSteps.map((_, i) => `
    <span style="display:inline-block; width:${i === currentTourIndex ? '18px' : '6px'}; height:6px; border-radius:3px; background:${i === currentTourIndex ? '#2563eb' : '#cbd5e1'}; transition:all 0.2s;"></span>
  `).join("");

  speakTourStep();
}

function nextTourStep() {
  if (currentTourIndex < tourSteps.length - 1) {
    currentTourIndex++;
    renderTourStep();
  } else {
    closeTourModal();
  }
}

function prevTourStep() {
  if (currentTourIndex > 0) {
    currentTourIndex--;
    renderTourStep();
  }
}

// ─── MCP MODAL ────────────────────────────────────────────────

function openMCPModal()  { document.getElementById("mcpModal").classList.add("open");    }
function closeMCPModal() { document.getElementById("mcpModal").classList.remove("open"); }

// ─── EXPORT ───────────────────────────────────────────────────

function exportData() {
  const headers = ["ID","Company Name","Country","Sector","Revenue (EUR M)","Met Last Year","Meeting Date","Current Status","Contact Name","Contact Email","Discussion Summary"];
  const rows = filteredCompanies.map(c => [
    `"${c.id}"`, `"${c.company_name.replace(/"/g,'""')}"`, `"${c.country}"`, `"${c.sector}"`,
    c.revenue_eur_m, c.met_last_year ? "TRUE" : "FALSE",
    c.meeting_date_last_year ? `"${c.meeting_date_last_year}"` : '""',
    `"${c.current_status}"`, `"${c.key_contact.name}"`, `"${c.key_contact.email}"`,
    `"${c.last_year_discussion_summary.replace(/"/g,'""')}"`
  ]);
  const csv = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(r => r.join(","))].join("\n");
  const a   = document.createElement("a");
  a.href    = encodeURI(csv);
  a.download = `EuroTrack_${new Date().toISOString().slice(0,10)}.csv`;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  showToast("CSV downloaded");
}

// ─── TOAST ────────────────────────────────────────────────────

function showToast(msg, type = "info") {
  const c = document.getElementById("toast-container");
  const t = document.createElement("div");
  t.className = "toast" + (type === "error" ? " error" : "");
  t.textContent = msg;
  c.appendChild(t);
  requestAnimationFrame(() => t.classList.add("show"));
  setTimeout(() => { t.classList.remove("show"); setTimeout(() => t.remove(), 200); }, 2500);
}

// ─── UTIL ─────────────────────────────────────────────────────

function esc(s) {
  return String(s).replace(/'/g, "\\'").replace(/"/g, "&quot;");
}
