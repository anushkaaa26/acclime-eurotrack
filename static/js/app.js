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
