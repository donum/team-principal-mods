// Team review site: every message of the game's German file, where it shows, and the team's review.
"use strict";

const BOOT = JSON.parse(document.getElementById("boot").textContent);
let CSRF = BOOT.csrf;
const $ = (sel, el = document) => el.querySelector(sel);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmt = n => Number(n).toLocaleString("en-US");
const PH = /\{[^{}\n]*\}|<[^>\n]+>|\[[A-Z_/]+\]|%[sd]/g;
const placeholders = s => (String(s).match(PH) || []).sort().join("\u0001");
const store = {
  get(k, d) { try { const v = localStorage.getItem("tpreview." + k); return v === null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem("tpreview." + k, JSON.stringify(v)); } catch { /* private window */ } },
};

// --- server calls ---------------------------------------------------------------

async function api(action, body, isForm = false) {
  const opts = { method: body === undefined ? "GET" : "POST", headers: { "X-CSRF": CSRF }, credentials: "same-origin" };
  if (body !== undefined) {
    if (isForm) opts.body = body;
    else { opts.headers["Content-Type"] = "application/json"; opts.body = JSON.stringify(body); }
  }
  let res;
  try { res = await fetch("api.php?a=" + encodeURIComponent(action) + "&l=" + encodeURIComponent(st.lang || ""), opts); }
  catch { throw new Error("No connection to the server. Check your internet and try again."); }
  let data = {};
  try { data = await res.json(); } catch { /* not json */ }
  if (res.status === 401 && BOOT.mode === "app") { location.reload(); throw new Error("Please log in."); }
  if (!res.ok || data.error) throw new Error(data.error || `The server answered ${res.status}.`);
  return data;
}

let toastTimer;
function toast(text, err = false) {
  let t = $(".toast");
  if (!t) { t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
  t.textContent = text; t.classList.toggle("err", err); t.hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => { t.hidden = true; }, err ? 6000 : 2500);
}

// --- login, setup, invite -----------------------------------------------------------

function authPage() {
  const m = BOOT.mode;
  const heading = { setup: "Set up the review site", invite: "Join the review", login: "Log in" }[m];
  const intro = {
    setup: "Nobody has an account yet. Create the admin account. You can invite the team afterwards.",
    invite: "Choose a password for your account. Your name was set by the admin.",
    login: "Use the name and password from your invite.",
  }[m];
  $("#app").innerHTML = `<div class="auth">
    <h1>${esc(BOOT.title)}</h1>
    <form class="box" id="auth">
      <h2>${heading}</h2><p class="sub">${intro}</p>
      ${m !== "invite" ? `<label>Name<input type="text" id="au-name" autocomplete="username" required maxlength="40"></label>` : ""}
      <label>Password<input type="password" id="au-pw" autocomplete="${m === "login" ? "current-password" : "new-password"}" required minlength="${m === "login" ? 1 : 10}"></label>
      ${m !== "login" ? `<label>Password again<input type="password" id="au-pw2" autocomplete="new-password" required></label>` : ""}
      <button class="btn primary" type="submit">${m === "login" ? "Log in" : "Save and start"}</button>
      <p class="msg err" id="au-msg" role="alert"></p>
    </form></div>`;
  $("#auth").addEventListener("submit", async e => {
    e.preventDefault();
    const pw = $("#au-pw").value;
    if (m !== "login" && pw !== $("#au-pw2").value) { $("#au-msg").textContent = "The two passwords are not the same."; return; }
    const body = { password: pw };
    if (m !== "invite") body.name = $("#au-name").value.trim();
    if (m === "invite") body.token = BOOT.invite;
    try { await api(m === "invite" ? "accept_invite" : m, body); location.href = location.pathname; }
    catch (err) { $("#au-msg").textContent = err.message; }
  });
}

// --- data -------------------------------------------------------------------------

const FLAGS = {
  missing: ["Missing in the German file", "bad"],
  english: ["Still English", "bad"],
  placeholder: ["Placeholders differ", "bad"],
  informal: ["Informal address (the rest is formal)", "bad"],
  caps: ["English is all caps, German not", "warn"],
  long: ["Much longer than English, may not fit", "warn"],
  leftover: ["English words kept", "warn"],
  terms: ["Term translated several ways", "warn"],
  spacing: ["Spaces or line breaks differ", "warn"],
};
const HOW = { code: "found in game code", pack: "season pack text", key: "from key name", guess: "approximate" };
const AREA_ORDER = ["Menus and setup", "Team and car", "Markets and contracts", "Money", "Race weekend", "Season and rules", "Mailbox and news", "Editors and Workshop", "Other"];
const areaRank = a => { const i = AREA_ORDER.indexOf(a.replace("Oval series: ", "")); return (a.startsWith("Oval") ? 100 : 0) + (i < 0 ? 50 : i); };
const STATUS = {
  "": "Any status",
  "mine-open": "Not reviewed by me",
  "none": "Not reviewed by anyone",
  "needs-decision": "Suggestions waiting for a decision",
  "discuss": "Marked for discussion",
  "approved": "Approved, not in a package yet",
  "packaged": "In a package, not sent yet",
  "sent": "Sent to the developers",
  "rejected": "Rejected suggestions",
  "glossary": "Breaks an agreed glossary term",
  "noshot": "No screenshot yet (not mails or news)",
  "shot": "Has a screenshot",
};
const SORTS = { flagged: "Flagged first", suggestions: "Most suggestions first", key: "By key" };

let D = null;        // the release data from tools/locale_review.py
let S = null;        // the team's state from the server
let P = [], ROWS = [], BYKEY = new Map();
const IDX = { links: new Map(), shots: new Map(), reviews: new Map(), votes: new Map(), comments: new Map(), decisions: new Map(), claims: new Map(), users: new Map(), glossary: [] };
const st = { lang: store.get("lang", ""), view: store.get("view", "messages"), area: "", screen: "", q: "", flag: "", status: "", sort: "flagged", keys: null, keysLabel: "", page: 0, openArea: "" };
const PAGE = 30;
const dirty = new Set();   // cards with unsaved typing

const me = () => S.me;
const batchOf = id => S.batches.find(b => b.id === id);
const batchSent = id => !!batchOf(id)?.sent_at;
const isLead = () => !!S.me.lead;
const langName = l => (S?.lang_names || {})[l] || (l === "en" ? "English" : l);
const isAdmin = () => S.me.role === "admin";
const uname = id => { const u = IDX.users.get(id); return u ? (u.role === "removed" ? u.name + " (former member)" : u.name) : "Someone"; };

function indexState() {
  for (const m of Object.values(IDX)) if (m instanceof Map) m.clear();
  for (const u of S.users) IDX.users.set(u.id, u);
  for (const r of S.reviews) { if (!IDX.reviews.has(r.msg_key)) IDX.reviews.set(r.msg_key, []); IDX.reviews.get(r.msg_key).push(r); }
  for (const v of S.votes) { if (!IDX.votes.has(v.review_id)) IDX.votes.set(v.review_id, new Set()); IDX.votes.get(v.review_id).add(v.user_id); }
  for (const c of S.comments) { if (!IDX.comments.has(c.msg_key)) IDX.comments.set(c.msg_key, []); IDX.comments.get(c.msg_key).push(c); }
  for (const d of S.decisions) IDX.decisions.set(d.msg_key, d);
  for (const c of S.claims) IDX.claims.set(c.area, c);
  for (const sh of S.shots) IDX.shots.set(sh.id, sh);
  for (const l of S.shot_links) { if (!IDX.shots.has(l.shot_id)) continue; if (!IDX.links.has(l.msg_key)) IDX.links.set(l.msg_key, []); IDX.links.get(l.msg_key).push(l); }
  IDX.glossary = S.glossary.filter(g => g.status === "agreed" && g.en_term).map(g => ({
    ...g, re: new RegExp("(^|[^A-Za-z])" + g.en_term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "($|[^A-Za-z])", "i"),
  }));
}

function glossaryHits(r) {
  const out = [];
  const de = (IDX.decisions.get(r.key)?.status === "approved" ? IDX.decisions.get(r.key).text : r.de).toLowerCase();
  for (const g of IDX.glossary) {
    if (!g.re.test(r.en)) continue;
    const ok = !g.de_term || de.includes(g.de_term.toLowerCase());
    out.push({ g, ok });
  }
  return out;
}

function msgState(r) {
  const d = IDX.decisions.get(r.key);
  if (d) return d.batch_id ? (batchSent(d.batch_id) ? "sent" : "packaged") : d.status;
  const revs = IDX.reviews.get(r.key) || [];
  if (revs.some(v => v.verdict === "fix")) return "needs-decision";
  return revs.length ? "reviewed" : "none";
}

/** Mails and news: full sentences that read fine without a picture, so no screenshot is asked for. */
const isMail = r => r.key.startsWith("mail.") || P[r.places[0]][0].endsWith("Mailbox and news");

function matches(r) {
  if (st.keys && !st.keys.has(r.key)) return false;
  if (st.area && !r.places.some(i => P[i][0] === st.area && (!st.screen || P[i][1] === st.screen))) return false;
  if (st.flag && !r.flags.some(x => x.split(":")[0] === st.flag)) return false;
  if (st.status) {
    const s = msgState(r), revs = IDX.reviews.get(r.key) || [];
    switch (st.status) {
      case "mine-open": if (revs.some(v => v.user_id === me().id)) return false; break;
      case "none": if (revs.length) return false; break;
      case "glossary": if (!glossaryHits(r).some(h => !h.ok)) return false; break;
      case "noshot": if (IDX.links.has(r.key) || isMail(r)) return false; break;
      case "shot": if (!IDX.links.has(r.key)) return false; break;
      default: if (s !== st.status) return false;
    }
  }
  if (st.q && !r.hay.includes(st.q)) return false;
  return true;
}

const SEVERITY = { missing: 5, english: 4, placeholder: 5, informal: 4, caps: 1, long: 1, leftover: 1, terms: 2, spacing: 1 };
function score(r) { let s = 0; for (const f of r.flags) s += SEVERITY[f.split(":")[0]] || 0; return s; }

function sortedList() {
  const list = ROWS.filter(matches);
  if (st.sort === "flagged") list.sort((a, b) => b.score - a.score || (a.key < b.key ? -1 : 1));
  else if (st.sort === "suggestions") {
    const n = r => (IDX.reviews.get(r.key) || []).filter(v => v.verdict === "fix").length;
    list.sort((a, b) => n(b) - n(a) || b.score - a.score);
  }
  return list;
}

// --- rendering helpers ------------------------------------------------------------------

function placeHtml(i) {
  const [a, s, p, mod, how] = P[i];
  return `<span class="a">${esc(a)}</span><span class="sep">›</span><span class="s">${esc(s)}</span>` +
    (p ? `<span class="sep">›</span><span class="p">${esc(p)}</span>` : "") + ` <span class="how" title="${esc(mod)}">${HOW[how] || how}</span>`;
}
function chipHtml(f) {
  const [name, extra] = f.split(":");
  const [label, tone] = FLAGS[name] || [name, ""];
  return `<span class="chip ${tone}">${esc(label)}${extra ? ": " + esc(extra.replaceAll(",", ", ")) : ""}</span>`;
}
function when(iso) { if (!iso) return ""; const d = new Date(iso); return isNaN(d) ? "" : d.toLocaleDateString("en-GB", { day: "numeric", month: "short" }); }

function decisionHtml(r) {
  const d = IDX.decisions.get(r.key);
  if (!d) return "";
  const b = d.batch_id ? batchOf(d.batch_id) : null;
  const label = { approved: "Approved", rejected: "Rejected", discuss: "To discuss" }[d.status];
  return `<div class="row">
    <span class="badge ${d.status}">${label}</span>${b ? (b.sent_at ? `<span class="badge sent">Sent in ${esc(b.name)}</span>` : `<span class="badge discuss">In package ${esc(b.name)}, not sent yet</span>`) : ""}
    <span class="msg">by ${esc(uname(d.decided_by))}, ${when(d.updated)}</span></div>
    ${d.status === "approved" ? `<div><div class="lbl">Approved text</div><div class="de sg">${esc(d.text)}</div></div>` : ""}
    ${d.note ? `<div class="msg">Lead note: ${esc(d.note)}</div>` : ""}`;
}

function reviewsHtml(r) {
  const revs = (IDX.reviews.get(r.key) || []).slice().sort((a, b) => (b.verdict === "fix") - (a.verdict === "fix") ||
    (IDX.votes.get(b.id)?.size || 0) - (IDX.votes.get(a.id)?.size || 0));
  if (!revs.length) return "";
  return `<div class="revs">${revs.map(v => {
    const mine = v.user_id === me().id;
    const votes = IDX.votes.get(v.id) || new Set();
    const iVoted = votes.has(me().id);
    if (v.verdict === "ok") return `<div class="rev ${mine ? "mine" : ""}"><div class="by"><b>${esc(uname(v.user_id))}</b> says it looks good · ${when(v.updated)}</div>
      ${v.reason ? `<div class="why">${esc(v.reason)}</div>` : ""}</div>`;
    return `<div class="rev ${mine ? "mine" : ""}">
      <div class="by"><b>${esc(uname(v.user_id))}</b> suggests · ${when(v.updated)}${votes.size ? ` · ${votes.size} agree${votes.size === 1 ? "s" : ""}` : ""}</div>
      <div class="sg">${esc(v.text)}</div>
      ${v.reason ? `<div class="why">${esc(v.reason)}</div>` : ""}
      <div class="act">
        ${!mine ? `<button class="btn small ${iVoted ? "on" : ""}" data-act="vote" data-id="${v.id}" data-on="${iVoted ? 0 : 1}">${iVoted ? "You agree" : "Agree"}</button>` : ""}
        ${isLead() ? `<button class="btn small" data-act="use" data-id="${v.id}">Use for decision</button>` : ""}
      </div></div>`;
  }).join("")}</div>`;
}

function myFormHtml(r) {
  const mine = (IDX.reviews.get(r.key) || []).find(v => v.user_id === me().id);
  const open = st.editing === r.key;
  const verdict = mine?.verdict;
  return `<div class="act">
      <button class="btn good" data-act="ok" aria-pressed="${verdict === "ok"}">Looks good</button>
      <button class="btn bad" data-act="edit" aria-pressed="${verdict === "fix" || open}">${verdict === "fix" ? "Edit my suggestion" : "Suggest a change"}</button>
      ${mine ? `<button class="btn" data-act="unreview">Remove my review</button>` : ""}
    </div>
    ${open ? `<div class="form">
      <label class="lbl" for="sg-${esc(r.key)}">Your ${esc(langName(S.lang))} text</label>
      <textarea id="sg-${esc(r.key)}" data-f="text">${esc(mine?.verdict === "fix" ? mine.text : r.de)}</textarea>
      <label class="lbl" for="rs-${esc(r.key)}">Why (helps the lead decide)</label>
      <input type="text" id="rs-${esc(r.key)}" data-f="reason" maxlength="2000" value="${esc(mine?.reason || "")}" placeholder="For example: laps are Runden everywhere else">
      <div class="act"><button class="btn primary" data-act="save">Save suggestion</button><button class="btn" data-act="cancel">Cancel</button>
      <span class="msg err" data-msg></span></div></div>` : ""}`;
}

function leadHtml(r) {
  if (!isLead()) return "";
  const d = IDX.decisions.get(r.key);
  const revs = (IDX.reviews.get(r.key) || []).filter(v => v.verdict === "fix");
  const best = revs.sort((a, b) => (IDX.votes.get(b.id)?.size || 0) - (IDX.votes.get(a.id)?.size || 0))[0];
  const pre = st.leadText.get(r.key) ?? (d?.status === "approved" ? d.text : best?.text ?? r.de);
  return `<details class="lead" ${st.leadOpen.has(r.key) ? "open" : ""} data-lead>
    <summary class="lbl">Lead decision</summary>
    <label class="lbl" for="ld-${esc(r.key)}">Text to send</label>
    <textarea id="ld-${esc(r.key)}" data-f="leadtext">${esc(pre)}</textarea>
    <input type="text" data-f="leadnote" maxlength="2000" placeholder="Note for the developers (optional)" value="${esc(st.leadNote.get(r.key) ?? d?.note ?? "")}" aria-label="Note">
    <div class="act">
      <button class="btn primary" data-act="decide" data-s="approved">Approve this text</button>
      <button class="btn" data-act="decide" data-s="rejected">Reject suggestions</button>
      <button class="btn" data-act="decide" data-s="discuss">Mark for discussion</button>
      ${d && !(d.batch_id && batchSent(d.batch_id)) ? `<button class="btn" data-act="undecide">Undo decision</button>` : ""}
      <span class="msg err" data-msg></span>
    </div></details>`;
}

function commentsHtml(r) {
  const cs = IDX.comments.get(r.key) || [];
  return `<details class="comments" ${st.commentsOpen.has(r.key) ? "open" : ""} data-comments>
    <summary>Discussion${cs.length ? ` (${cs.length})` : ""}</summary>
    ${cs.map(c => `<div class="comment"><div class="by">${esc(uname(c.user_id))} · ${when(c.created)}
      ${c.user_id === me().id || isLead() ? ` · <button class="linkish" data-act="uncomment" data-id="${c.id}">delete</button>` : ""}</div>${esc(c.body)}</div>`).join("")}
    <div class="form" style="margin-top:6px"><textarea data-f="comment" placeholder="Ask or explain something about this message" aria-label="Comment"></textarea>
    <div class="act"><button class="btn small" data-act="comment">Post</button></div></div></details>`;
}

function cardHtml(r) {
  const s = msgState(r);
  const cls = { approved: "approved", sent: "approved", rejected: "rejected", discuss: "discuss", "needs-decision": "open-fix" }[s] || "";
  const first = r.places[0], rest = r.places.slice(1);
  const gl = glossaryHits(r);
  return `<article class="card ${cls}" data-k="${esc(r.key)}">
    <div class="where">${placeHtml(first)}</div>
    ${rest.length ? `<details class="more"><summary>Also shown in ${rest.length} more place${rest.length > 1 ? "s" : ""}</summary><ul>${rest.map(i => `<li class="where">${placeHtml(i)}</li>`).join("")}</ul></details>` : ""}
    <div class="texts">
      <div><div class="lbl">English</div><div class="en">${esc(r.en)}</div></div>
      <div><div class="lbl">${esc(langName(S.lang))} now</div><div class="de">${r.de ? esc(r.de) : "<em>(missing)</em>"}</div></div>
    </div>
    ${r.flags.length || gl.length ? `<div class="chips">${r.flags.map(chipHtml).join("")}${gl.map(h =>
      `<span class="chip ${h.ok ? "good" : "bad"}">Glossary: ${esc(h.g.en_term)} → ${esc(h.g.de_term || "(keep English)")}${h.ok ? "" : ", not used"}</span>`).join("")}</div>` : ""}
    ${shotsHtml(r)}
    ${decisionHtml(r)}
    ${reviewsHtml(r)}
    ${myFormHtml(r)}
    ${commentsHtml(r)}
    ${leadHtml(r)}
    <div class="key mono">${esc(r.key)}</div>
  </article>`;
}
st.editing = null; st.leadText = new Map(); st.leadNote = new Map(); st.leadOpen = new Set(); st.commentsOpen = new Set();

function rerenderCard(key) {
  const el = document.querySelector(`.card[data-k="${CSS.escape(key)}"]`);
  if (!el) return;
  const tmp = document.createElement("div"); tmp.innerHTML = cardHtml(BYKEY.get(key));
  el.replaceWith(tmp.firstElementChild);
}

// --- page frame -------------------------------------------------------------------------

const TABS = [["messages", "Messages"], ["glossary", "Glossary"], ["areas", "Areas"], ["batches", "To the developers"], ["followup", "Follow-up"], ["team", "Team"]];

function frame() {
  $("#app").innerHTML = `
    <header class="top">
      <div><h1>${esc(BOOT.title)}</h1>
      <p class="sub">${D ? `${fmt(ROWS.length)} messages of ${esc(D.file)}, with the place in the game that shows each one.` : ""}</p></div>
      <div class="who">
        ${[...new Set([...S.langs, S.lang])].length > 1 ? `<label class="row">Language <select id="langsel" aria-label="Language">${[...new Set([...S.langs, S.lang])].map(l => `<option value="${esc(l)}" ${l === S.lang ? "selected" : ""}>${esc(langName(l))}</option>`).join("")}</select></label>` : `<span>${esc(langName(S.lang))}</span>`}
        <span>${esc(me().name)} · ${esc(me().role)}${me().role === "lead" ? ` (${esc(me().langs || "all languages")})` : ""}</span>
        <button class="btn small" data-act="logout">Log out</button></div>
    </header>
    <div id="howto"></div>
    <div class="stats" id="stats"></div>
    <nav class="tabs" role="tablist">${TABS.map(([v, l]) => `<button class="tab" role="tab" data-view="${v}" aria-selected="${st.view === v}">${l}<span class="n" data-n="${v}"></span></button>`).join("")}</nav>
    <main id="view"></main>`;
}

function renderHowto() {
  const el = $("#howto");
  if (store.get("howtoHidden", false)) { el.innerHTML = `<button class="linkish" data-act="howto-show">How this works</button>`; return; }
  el.innerHTML = `<div class="howto"><h3>How this works</h3><ol>
    <li><b>Claim an area</b> in the Areas tab, so two people don't check the same screens.</li>
    <li>Read the <b>Glossary</b> first. Agreed terms (like laps = Runden) count everywhere, and messages that break them are marked.</li>
    <li>For each message, press <b>Looks good</b> or <b>Suggest a change</b> and say why. Press <b>Agree</b> on someone else's suggestion if you like it.</li>
    <li>Keep the game's placeholders, like <span class="mono">{driver}</span> or <span class="mono">{value}</span>, exactly as they are. The page refuses a text where they differ.</li>
    <li><b>Screenshots</b> show how a text looks in the game. Take one (Windows: Win+Shift+S), press <b>Add screenshot</b> on a message, paste it with Ctrl+V and draw a box around the text. Then mark the other texts of that screen on the same picture.</li>
    <li>The <b>leads</b> decide: approve a text, reject the suggestions, or mark the message for discussion.</li>
    <li>In <b>To the developers</b>, a lead puts the approved changes into a <b>package</b>, downloads its two files and sends them to the developers (Discord or mail). Nothing changes in the game or in anyone's files until the developers take it.</li>
    </ol><button class="btn small" data-act="howto-hide">Hide</button></div>`;
}

function renderStats() {
  const reviewed = ROWS.filter(r => IDX.reviews.has(r.key)).length;
  const mine = S.reviews.filter(v => v.user_id === me().id).length;
  const waiting = ROWS.filter(r => msgState(r) === "needs-decision").length;
  const discuss = S.decisions.filter(d => d.status === "discuss").length;
  const approved = S.decisions.filter(d => d.status === "approved" && !d.batch_id).length;
  const packaged = S.decisions.filter(d => d.batch_id && !batchSent(d.batch_id)).length;
  const sent = S.decisions.filter(d => d.batch_id && batchSent(d.batch_id)).length;
  const steps = [
    ["1", "Review", "Everyone", `${fmt(reviewed)} of ${fmt(ROWS.length)} messages reviewed, ${fmt(mine)} by you`, "mine-open", "Show messages you haven't reviewed"],
    ["2", "Decide", "Leads", `${fmt(waiting)} with suggestions waiting${discuss ? `, ${fmt(discuss)} to discuss` : ""}`, "needs-decision", "Show the suggestions waiting for a lead"],
    ["3", "Package", "Leads", `${fmt(approved)} approved, not in a package`, "approved", "Show the approved changes"],
    ["4", "Send", "Leads", `${fmt(packaged)} in packages not sent yet`, "@batches", "Open To the developers"],
    ["5", "Check", "After a game update", `${fmt(sent)} sent: did the developers take them?`, "@followup", "Open Follow-up"],
  ];
  $("#stats").innerHTML = `<ol class="flow">${steps.map(([n, t, who, txt, f, title]) =>
    `<li><button class="step" data-act="stat" data-f="${f}" title="${esc(title)}"><span class="sn">${n}</span><span class="st"><b>${t}</b> <span class="swho">${who}</span><span class="sx">${txt}</span></span></button></li>`).join("")}</ol>`;
  const n = { batches: approved + packaged ? fmt(approved + packaged) : "" };
  for (const el of document.querySelectorAll("[data-n]")) el.textContent = n[el.dataset.n] || "";
}

function setView(v) {
  st.view = v; store.set("view", v);
  for (const t of document.querySelectorAll(".tab")) t.setAttribute("aria-selected", String(t.dataset.view === v));
  renderView();
}

function renderView() {
  const v = $("#view");
  if (!D && st.view !== "team") { v.innerHTML = `<div class="empty">No game file is loaded yet. ${isAdmin() ? "Upload one in the Team tab." : "The admin needs to upload one."}</div>`; return; }
  ({ messages: viewMessages, glossary: viewGlossary, areas: viewAreas, batches: viewBatches, followup: viewFollowup, team: viewTeam }[st.view] || viewMessages)(v);
}

// --- Messages view ---------------------------------------------------------------------------

function viewMessages(v) {
  v.innerHTML = `<div class="layout">
    <aside class="side" aria-label="Where in the game"><div class="h">Where in the game</div><div class="tree" id="tree"></div></aside>
    <div style="min-width:0">
      <div class="filters">
        <input type="search" id="q" placeholder="Search English, German or key" aria-label="Search" value="${esc(st.q)}">
        <select id="flag" aria-label="Check"><option value="">All checks</option>${Object.entries(FLAGS).map(([f, [l]]) => {
          const n = ROWS.filter(r => r.flags.some(x => x.split(":")[0] === f)).length;
          return n ? `<option value="${f}" ${st.flag === f ? "selected" : ""}>${esc(l)} (${fmt(n)})</option>` : ""; }).join("")}</select>
        <select id="status" aria-label="Review status">${Object.entries(STATUS).map(([k, l]) => `<option value="${k}" ${st.status === k ? "selected" : ""}>${esc(l)}</option>`).join("")}</select>
        <select id="sort" aria-label="Order">${Object.entries(SORTS).map(([k, l]) => `<option value="${k}" ${st.sort === k ? "selected" : ""}>${esc(l)}</option>`).join("")}</select>
      </div>
      <div class="crumb" id="crumb"></div>
      <div id="list"></div>
      <div class="pager" id="pager"></div>
    </div></div>`;
  renderTree(); renderList();
  let qt;
  $("#q").addEventListener("input", e => { clearTimeout(qt); qt = setTimeout(() => { st.q = e.target.value.trim().toLowerCase(); st.page = 0; renderList(); }, 200); });
  $("#flag").addEventListener("change", e => { st.flag = e.target.value; st.page = 0; renderList(); });
  $("#status").addEventListener("change", e => { st.status = e.target.value; st.page = 0; renderList(); });
  $("#sort").addEventListener("change", e => { st.sort = e.target.value; st.page = 0; renderList(); });
}

function areaTree() {
  const tree = new Map();
  for (const r of ROWS) {
    const [a, s] = P[r.places[0]];
    if (!tree.has(a)) tree.set(a, new Map());
    const m = tree.get(a);
    if (!m.has(s)) m.set(s, { n: 0, done: 0 });
    const c = m.get(s); c.n++; if (IDX.reviews.has(r.key) || IDX.decisions.has(r.key)) c.done++;
  }
  return tree;
}
const claimKey = (a, s) => s ? a + " › " + s : a;

function renderTree() {
  const el = $("#tree"); if (!el) return;
  const tree = areaTree();
  const areas = [...tree.keys()].sort((a, b) => areaRank(a) - areaRank(b));
  let h = `<button class="area ${!st.area ? "on" : ""}" data-a=""><span>All areas</span><span class="n">${fmt(ROWS.length)}</span></button>`;
  for (const a of areas) {
    const m = tree.get(a); let n = 0, done = 0; for (const c of m.values()) { n += c.n; done += c.done; }
    const cl = IDX.claims.get(a);
    h += `<button class="area ${st.area === a && !st.screen ? "on" : ""}" data-a="${esc(a)}"><span>${esc(a)}${cl ? `<span class="claim">${esc(uname(cl.user_id))}</span>` : ""}</span><span class="n">${fmt(done)}/${fmt(n)}</span></button>`;
    if (st.openArea === a) for (const [s, c] of [...m.entries()].sort((x, y) => y[1].n - x[1].n)) {
      const cs = IDX.claims.get(claimKey(a, s));
      h += `<button class="scr ${st.screen === s && st.area === a ? "on" : ""}" data-a="${esc(a)}" data-s="${esc(s)}"><span>${esc(s)}${cs ? `<span class="claim">${esc(uname(cs.user_id))}</span>` : ""}</span><span class="n">${fmt(c.done)}/${fmt(c.n)}</span></button>`;
    }
  }
  el.innerHTML = h;
}

function renderList() {
  const listEl = $("#list"); if (!listEl) return;
  const list = sortedList();
  const pages = Math.max(1, Math.ceil(list.length / PAGE));
  st.page = Math.min(st.page, pages - 1);
  const slice = list.slice(st.page * PAGE, st.page * PAGE + PAGE);
  const crumbs = [];
  if (st.keysLabel) crumbs.push(`<button data-clear="keys">${esc(st.keysLabel)} ✕</button>`);
  if (st.area) crumbs.push(`<button data-clear="area">${esc(st.screen ? st.area + " › " + st.screen : st.area)} ✕</button>`);
  $("#crumb").innerHTML = `<span>${fmt(list.length)} message${list.length === 1 ? "" : "s"}</span>${crumbs.join("")}`;
  listEl.innerHTML = slice.length ? slice.map(cardHtml).join("") : `<div class="empty">No messages match. Clear a filter or search for another word.</div>`;
  $("#pager").innerHTML = pages > 1 ? `<button class="btn" data-p="-1" ${st.page ? "" : "disabled"}>Previous</button>
    <span>Page ${st.page + 1} of ${fmt(pages)}</span><button class="btn" data-p="1" ${st.page < pages - 1 ? "" : "disabled"}>Next</button>` : "";
}

function showKeys(keys, label) {
  st.keys = new Set(keys); st.keysLabel = label; st.area = ""; st.screen = ""; st.status = ""; st.flag = ""; st.page = 0;
  setView("messages");
}

// --- Glossary view ----------------------------------------------------------------------------

function termRegex(en) {
  return new RegExp("(^|[^A-Za-z])" + en.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "($|[^A-Za-z])", "i");
}

function viewGlossary(v) {
  const L = S.lang, Lname = langName(L);
  const terms = (S.terms || []).map(t => ({ ...t, mine: t.langs[L] || null, re: termRegex(t.en_term) }));
  const uses = t => { if (t._uses === undefined) t._uses = ROWS.filter(r => t.re.test(r.en)).length; return t._uses; };
  const textOf = r => (IDX.decisions.get(r.key)?.status === "approved" ? IDX.decisions.get(r.key).text : r.de).toLowerCase();
  const breaks = t => t.mine && t.mine.status === "agreed" && t.mine.term
    ? ROWS.filter(r => t.re.test(r.en) && !textOf(r).includes(t.mine.term.toLowerCase())).map(r => r.key) : [];
  const filter = st.glFilter || "all";
  const shown = terms.filter(t => filter === "all" || (filter === "missing" && !t.mine) || (filter === "proposed" && t.mine && t.mine.status !== "agreed"));
  const counts = { all: terms.length, missing: terms.filter(t => !t.mine).length, proposed: terms.filter(t => t.mine && t.mine.status !== "agreed").length };
  const others = t => Object.entries(t.langs).filter(([l]) => l !== L).map(([l, x]) =>
    `<span class="chip ${x.status === "agreed" ? "good" : ""}" title="${esc(langName(l))}${x.note ? ": " + esc(x.note) : ""}">${esc(l)}: ${x.term ? esc(x.term) : "<em>English kept</em>"}</span>`).join(" ");
  const rowHtml = t => {
    const m = t.mine, b = breaks(t);
    const canEdit = m && (isLead() || (m.user_id === me().id && m.status !== "agreed"));
    const mineHtml = m
      ? `${m.term ? `<b>${esc(m.term)}</b>` : "<em>keep the English word</em>"} <span class="chip ${m.status === "agreed" ? "good" : "warn"}">${m.status === "agreed" ? "agreed" : "proposed"}</span>
         ${m.note ? `<div class="msg">${esc(m.note)}</div>` : ""}<div class="msg">${esc(uname(m.user_id))}, ${when(m.updated)}</div>`
      : `<span class="chip warn">no ${esc(Lname)} term yet</span>`;
    return `<tr>
      <td><b>${esc(t.en_term)}</b>${t.note ? `<div class="msg">${esc(t.note)}</div>` : ""}</td>
      <td>${mineHtml}</td>
      <td>${others(t) || '<span class="msg">no other language yet</span>'}</td>
      <td class="num"><button class="linkish" data-act="gl-uses" data-id="${t.id}">${fmt(uses(t))}</button>${b.length ? `<div><button class="linkish" data-act="gl-show" data-id="${t.id}" style="color:var(--bad)">${fmt(b.length)} break it</button></div>` : ""}</td>
      <td><div class="act">
        ${!m ? `<button class="btn small primary" data-act="gl-edit" data-id="${t.id}">Add ${esc(Lname)}</button>` : ""}
        ${m && isLead() && m.status !== "agreed" ? `<button class="btn small" data-act="gl-agree" data-id="${t.id}">Agree</button>` : ""}
        ${canEdit || (!m && isLead()) ? `<button class="btn small" data-act="gl-edit" data-id="${t.id}">Edit</button>` : ""}
        ${canEdit ? `<button class="btn small" data-act="gl-del" data-id="${t.id}">Remove ${esc(L)}</button>` : ""}
      </div></td></tr>`;
  };
  const words = new Map();
  for (const r of ROWS) for (const f of r.flags) if (f.startsWith("leftover:")) for (const w of f.slice(9).split(",")) { const k = w.toLowerCase(); if (!words.has(k)) words.set(k, []); words.get(k).push(r.key); }
  const wl = [...words.entries()].sort((a, b) => b[1].length - a[1].length).slice(0, 150);
  st.wordList = wl;
  const editing = st.glEdit ? terms.find(t => t.id === st.glEdit) : null;
  v.innerHTML = `
    <div class="box"><h2>${editing ? `${editing.mine ? "Change" : "Add the " + esc(Lname)} term for "${esc(editing.en_term)}"` : "Add a term"}</h2>
      <p class="sub">A term is one English word or phrase with its <b>meaning</b>, shared by every language, and one translation per language.
      A term another team started shows up here too, so all languages use the same list. ${isLead() ? "As a lead you can agree your language's term right away." : "A lead of your language agrees it."}</p>
      <form id="glform" class="form" style="max-width:820px">
        <div class="row">
          <input type="text" id="gl-en" placeholder="English, for example driver" required maxlength="200" aria-label="English term" style="flex:1 1 200px">
          <input type="text" id="gl-meaning" placeholder="Meaning, for all languages: the racing driver, never a software driver" maxlength="2000" aria-label="Meaning" style="flex:3 1 320px">
        </div>
        <div class="row">
          <input type="text" id="gl-de" placeholder="${esc(Lname)}, for example ${L === "de" ? "Fahrer" : "…"}" maxlength="200" aria-label="${esc(Lname)} term" style="flex:1 1 200px">
          <label class="row"><input type="checkbox" id="gl-keep"> keep the English word</label>
          <input type="text" id="gl-note" placeholder="Note for ${esc(Lname)} (optional)" maxlength="2000" aria-label="Note" style="flex:2 1 220px">
          ${isLead() ? `<label class="row"><input type="checkbox" id="gl-agreed"> agreed</label>` : ""}
        </div>
        <div class="act"><button class="btn primary" type="submit">Save</button>
        ${editing ? `<button class="btn" type="button" data-act="gl-cancel">Cancel</button>` : ""}</div>
      </form></div>
    <div class="row" style="justify-content:space-between;margin-bottom:8px">
      <h2 style="margin:0">Terms in all languages</h2>
      <div class="act">${[["all", "All"], ["missing", `No ${Lname} term yet`], ["proposed", "Proposed"]].map(([k, l]) =>
        `<button class="btn small ${filter === k ? "on" : ""}" data-act="gl-filter" data-f="${k}">${esc(l)} (${counts[k]})</button>`).join("")}</div>
    </div>
    ${shown.length ? `<div class="tbl"><table><thead><tr><th>English and meaning</th><th>${esc(Lname)}</th><th>Other languages</th><th class="num">Messages</th><th></th></tr></thead>
      <tbody>${shown.map(rowHtml).join("")}</tbody></table></div>`
      : `<div class="empty">${terms.length ? "No term in this list." : "No terms yet. Start with the most common ones in the lists below."}</div>`}
    <div class="grid2" style="margin-top:18px">
      <div><h2>Same term, several translations</h2><p class="sub">Short English terms the ${esc(Lname)} file translates in more than one way. Click a variant to see its messages.</p>
      <div class="tbl"><table><thead><tr><th>English</th><th>${esc(Lname)} variants (messages)</th><th></th></tr></thead><tbody>${D.terms.map((t, ti) => `<tr><td><b>${esc(t.en)}</b></td>
        <td>${t.variants.map((x, vi) => `<button class="linkish" data-act="term-show" data-t="${ti}" data-v="${vi}">${esc(x[0])}</button> <span class="msg">(${x[1].length})</span>`).join(" · ")}</td>
        <td><button class="btn small" data-act="term-add" data-t="${ti}">Make a term</button></td></tr>`).join("")}</tbody></table></div></div>
      <div><h2>English words kept</h2><p class="sub">English words that also appear in the ${esc(Lname)} text. Some are fine (Grand Prix), others are leftovers.</p>
      <div class="tbl"><table><thead><tr><th>Word</th><th class="num">Messages</th><th></th></tr></thead><tbody>${wl.map(([w, ks], i) => `<tr><td><button class="linkish" data-act="word-show" data-i="${i}">${esc(w)}</button></td><td class="num">${ks.length}</td>
        <td><button class="btn small" data-act="word-add" data-i="${i}">Make a term</button></td></tr>`).join("")}</tbody></table></div></div>
    </div>`;
  if (editing) {
    $("#gl-en").value = editing.en_term; $("#gl-meaning").value = editing.note || "";
    if (editing.mine) {
      $("#gl-de").value = editing.mine.term || ""; $("#gl-keep").checked = !editing.mine.term; $("#gl-note").value = editing.mine.note || "";
      if ($("#gl-agreed")) $("#gl-agreed").checked = editing.mine.status === "agreed";
    }
    (editing.mine ? $("#gl-de") : $("#gl-de")).focus();
  }
  if (st.glPrefill) {
    $("#gl-en").value = st.glPrefill.en; $("#gl-de").value = st.glPrefill.de || "";
    const known = terms.find(t => t.en_term.toLowerCase() === st.glPrefill.en.toLowerCase());
    if (known) $("#gl-meaning").value = known.note || "";
    st.glPrefill = null; $("#gl-de").focus();
  }
  $("#glform").addEventListener("submit", async e => {
    e.preventDefault();
    const term = $("#gl-de").value.trim(), keep = $("#gl-keep").checked;
    const body = { id: st.glEdit || 0, en_term: $("#gl-en").value, meaning: $("#gl-meaning").value, de_term: keep ? "" : term,
      keep_english: keep ? 1 : 0, note: $("#gl-note").value,
      status: $("#gl-agreed")?.checked ? "agreed" : "proposed" };
    try {
      await api("glossary", body);
      st.glEdit = null;
      toast(term || keep ? "Saved" : `Saved the English term. Add the ${Lname} word when you know it.`);
      await refresh(true);
    } catch (err) { toast(err.message, true); }
  });
}

// --- Areas view --------------------------------------------------------------------------------

function viewAreas(v) {
  const tree = areaTree();
  const areas = [...tree.keys()].sort((a, b) => areaRank(a) - areaRank(b));
  const row = (a, s, n, done, sub) => {
    const k = claimKey(a, s), cl = IDX.claims.get(k), mine = cl && cl.user_id === me().id;
    const pct = n ? Math.round(done / n * 100) : 0;
    return `<tr><td style="${sub ? "padding-left:28px" : "font-weight:600"}"><button class="linkish" data-act="area-show" data-a="${esc(a)}" data-s="${esc(s || "")}">${esc(s || a)}</button></td>
      <td class="num">${fmt(done)} / ${fmt(n)}</td><td><div class="bar" title="${pct}%"><i style="width:${pct}%"></i></div></td>
      <td>${cl ? esc(uname(cl.user_id)) : "<span class='msg'>free</span>"}</td>
      <td>${cl ? (mine || isLead() ? `<button class="btn small" data-act="unclaim" data-k="${esc(k)}">Release</button>` : "") : `<button class="btn small" data-act="claim" data-k="${esc(k)}">Claim</button>`}</td></tr>`;
  };
  let body = "";
  for (const a of areas) {
    const m = tree.get(a); let n = 0, done = 0; for (const c of m.values()) { n += c.n; done += c.done; }
    body += row(a, "", n, done, false);
    if (st.areasOpen?.has(a)) for (const [s, c] of [...m.entries()].sort((x, y) => y[1].n - x[1].n)) body += row(a, s, c.n, c.done, true);
    body += `<tr><td colspan="5" style="padding-top:0"><button class="linkish msg" data-act="area-toggle" data-a="${esc(a)}">${st.areasOpen?.has(a) ? "Hide screens" : `Show its ${m.size} screens`}</button></td></tr>`;
  }
  const people = S.users.filter(u => u.role !== "removed").map(u => {
    const n = S.reviews.filter(r => r.user_id === u.id).length;
    const cl = S.claims.filter(c => c.user_id === u.id).map(c => c.area);
    return `<tr><td>${esc(u.name)}</td><td class="num">${fmt(n)}</td><td>${cl.map(esc).join(", ") || "<span class='msg'>nothing claimed</span>"}</td></tr>`;
  }).join("");
  v.innerHTML = `<p class="sub">Claim a whole area, or open it and claim single screens. "Reviewed" counts messages with at least one review or a decision.</p>
    <div class="tbl"><table><thead><tr><th>Area or screen</th><th class="num">Reviewed</th><th></th><th>Claimed by</th><th></th></tr></thead><tbody>${body}</tbody></table></div>
    <h2 style="margin-top:18px">Who does what</h2>
    <div class="tbl"><table><thead><tr><th>Name</th><th class="num">Reviews</th><th>Claimed</th></tr></thead><tbody>${people}</tbody></table></div>`;
}

// --- To the developers (packages) -----------------------------------------------------------------

function viewBatches(v) {
  const waiting = S.decisions.filter(d => d.status === "approved" && !d.batch_id);
  const open = S.batches.filter(b => !b.sent_at), sent = S.batches.filter(b => b.sent_at);
  const files = b => `<a href="api.php?a=batch_export&amp;id=${b.id}&amp;fmt=json&amp;l=${esc(S.lang)}">JSON file</a> · <a href="api.php?a=batch_export&amp;id=${b.id}&amp;fmt=tsv&amp;l=${esc(S.lang)}">Table</a>`;
  const row = b => `<tr>
      <td><button class="linkish" data-act="batch-show" data-id="${b.id}">${esc(b.name)}</button><div class="msg">made ${when(b.created)} by ${esc(uname(b.created_by))}</div></td>
      <td class="num">${fmt(b.item_count)}</td>
      <td>${files(b)}</td>
      <td>${b.sent_at ? `Sent ${when(b.sent_at)} by ${esc(uname(b.sent_by))}${b.sent_note ? `<div class="msg">${esc(b.sent_note)}</div>` : ""}` : `<span class="chip warn">not sent yet</span>`}</td>
      <td>${isLead() ? `<div class="act">${b.sent_at
        ? `<button class="btn small" data-act="batch-unsend" data-id="${b.id}">Mark as not sent</button>`
        : `<input type="text" class="sentnote" data-id="${b.id}" placeholder="Where sent, e.g. Discord #translations" maxlength="500" aria-label="Where it was sent" style="width:210px">
           <button class="btn small primary" data-act="batch-send" data-id="${b.id}">Mark as sent</button>
           <button class="btn small" data-act="batch-delete" data-id="${b.id}">Delete package</button>`}</div>` : ""}</td></tr>`;
  const table = list => `<div class="tbl"><table><thead><tr><th>Package</th><th class="num">Changes</th><th>Files</th><th>Status</th><th></th></tr></thead><tbody>${list.map(row).join("")}</tbody></table></div>`;
  v.innerHTML = `
    <div class="box"><h2>How changes reach the developers</h2>
      <ol class="explain">
        <li><b>Package.</b> A package is a list of approved changes that go to the developers together, for example one area or one week. Making one sends nothing yet.</li>
        <li><b>Send.</b> Download the package's two files: the <b>JSON file</b> (same format as ${esc(S.lang)}.json, the developers can merge it) and the <b>Table</b> (English, old text, new text, reason). Send both to the developers yourself, then press <b>Mark as sent</b>.</li>
        <li><b>Check.</b> When a game update arrives, the admin loads the new game file. <b>Follow-up</b> then shows which sent changes the developers took.</li>
      </ol>
      <p class="msg">Until a package is marked as sent, a lead can delete it: its changes go back to "approved" and can go into another package. A change that is decided again leaves its unsent package by itself.</p>
    </div>
    <div class="box"><h2>1. Approved, waiting for a package: ${fmt(waiting.length)}</h2>
      ${waiting.length ? `<p><button class="linkish" data-act="batch-preview">Show these changes</button></p>` : `<p class="msg">Nothing waiting. Leads approve changes on the messages.</p>`}
      ${isLead() ? `<form id="bform" class="row"><input type="text" id="b-name" placeholder="Package name, for example Race weekend" maxlength="80" aria-label="Package name">
        <button class="btn primary" type="submit" ${waiting.length ? "" : "disabled"}>Put ${fmt(waiting.length)} change${waiting.length === 1 ? "" : "s"} into a package</button></form>` : `<p class="msg">A lead makes the packages.</p>`}
    </div>
    <h2>2. Packages to send: ${fmt(open.length)}</h2>
    ${open.length ? table(open) : `<div class="empty">No package waiting to be sent.</div>`}
    <h2 style="margin-top:18px">3. Sent: ${fmt(sent.length)}</h2>
    ${sent.length ? table(sent) : `<div class="empty">Nothing sent yet.</div>`}`;
  $("#bform")?.addEventListener("submit", async e => {
    e.preventDefault();
    try { const r = await api("batch_create", { name: $("#b-name").value }); toast(`Package made with ${r.count} change${r.count === 1 ? "" : "s"}. Download its files and send them.`); await refresh(true); }
    catch (err) { toast(err.message, true); }
  });
}

// --- Follow-up view ---------------------------------------------------------------------------------

const FU = {
  taken: ["Taken", "The game now has your text.", "good"],
  changed_differently: ["Changed differently", "The developers wrote something else. Check whether it's fine.", "warn"],
  still_old: ["Still old", "Not in the game yet. Send it again with the next batch.", "bad"],
  english_changed: ["English changed", "The English text (and so often the key) changed. Review the new message again.", "warn"],
};
async function viewFollowup(v) {
  v.innerHTML = `<p class="sub">Loading…</p>`;
  let data;
  try { data = await api("followup"); } catch (err) { v.innerHTML = `<div class="empty">${esc(err.message)}</div>`; return; }
  if (st.view !== "followup") return;   // the user moved on while it loaded
  const by = {}; for (const k of Object.keys(FU)) by[k] = data.items.filter(i => i.state === k);
  const sel = st.fuState || Object.keys(FU).find(k => by[k].length) || "taken";
  v.innerHTML = `<p class="sub">Every change in a package marked as sent, compared with the game file loaded now (${esc(data.release || "none")}).
    After a game update, the admin builds a new data file with tools/locale_review.py and uploads it in the Team tab. This page then shows what the developers took.</p>
    <div class="stats">${Object.entries(FU).map(([k, [l, , tone]]) => `<button class="stat" data-act="fu" data-s="${k}" ${k === sel ? 'style="border-color:var(--accent)"' : ""}><b>${fmt(by[k].length)}</b><span class="chip ${tone}">${l}</span></button>`).join("")}</div>
    <p class="sub">${FU[sel][1]}</p>
    ${by[sel].length ? `<div class="tbl"><table><thead><tr><th>Message</th><th>We sent</th><th>Game now</th><th>Batch</th></tr></thead><tbody>${by[sel].map(i => {
      const r = BYKEY.get(i.key);
      return `<tr><td><div class="mono key">${esc(i.key)}</div><div class="msg">${esc(i.en_then)}</div>${i.en_now !== null && i.en_now !== i.en_then ? `<div class="msg">Now: ${esc(i.en_now)}</div>` : ""}
        ${r ? `<button class="btn small" data-act="fu-open" data-k="${esc(i.key)}">Open message</button>` : `<button class="btn small" data-act="fu-search" data-q="${esc(i.en_then.slice(0, 40))}">Find the new message</button>`}</td>
        <td class="sg">${esc(i.sent)}</td><td class="sg">${i.de_now === null ? "<em>key gone</em>" : esc(i.de_now)}</td><td>${esc(i.batch)}</td></tr>`; }).join("")}</tbody></table></div>`
      : `<div class="empty">Nothing here.</div>`}`;
}

// --- Team view ------------------------------------------------------------------------------------------

function inviteUrl(tok) { return location.origin + location.pathname + "?invite=" + encodeURIComponent(tok); }
function viewTeam(v) {
  const users = S.users.filter(u => u.role !== "removed");
  v.innerHTML = `
    ${st.invite ? `<div class="box"><h3>Invite link for ${esc(st.invite.name)}</h3><p class="sub">Send this link to ${esc(st.invite.name)} by mail or chat. It works once, for 14 days.</p>
      <div class="row"><input type="text" readonly class="out" id="inv" value="${esc(inviteUrl(st.invite.token))}" aria-label="Invite link" style="flex:1 1 300px"><button class="btn" data-act="copy-invite">Copy</button></div></div>` : ""}
    <h2>Team</h2>
    <div class="tbl"><table><thead><tr><th>Name</th><th>Role</th><th>Last seen</th><th></th></tr></thead><tbody>${users.map(u => `<tr>
      <td>${esc(u.name)}${u.invited ? ` <span class="chip warn">invite not used yet</span>` : ""}</td>
      <td>${isAdmin() && u.id !== me().id ? `<div class="row"><select data-act="role" data-id="${u.id}" aria-label="Role">${["reviewer", "lead", "admin"].map(r => `<option ${u.role === r ? "selected" : ""}>${r}</option>`).join("")}</select>
        ${u.role === "lead" ? `<input type="text" data-act="langs" data-id="${u.id}" value="${esc(u.langs || "")}" placeholder="all languages" aria-label="Lead for languages" style="width:130px">` : ""}</div>` : esc(u.role) + (u.role === "lead" ? ` (${esc(u.langs || "all languages")})` : "")}</td>
      <td>${u.last_seen ? when(u.last_seen) : "never"}</td>
      <td>${isAdmin() && u.id !== me().id ? `<div class="act"><button class="btn small" data-act="reinvite" data-id="${u.id}" data-name="${esc(u.name)}">New invite link</button><button class="btn small" data-act="remove" data-id="${u.id}" data-name="${esc(u.name)}">Remove</button></div>` : ""}</td></tr>`).join("")}</tbody></table></div>
    <p class="msg" style="margin-top:6px">Reviewers review and discuss, in every language. Leads also decide, agree glossary terms and create batches, for the languages listed (empty means all). The admin also invites people and loads game files.</p>
    ${isAdmin() ? `<div class="grid2" style="margin-top:14px">
      <div class="box"><h3>Invite someone</h3><form id="uform" class="row">
        <input type="text" id="u-name" placeholder="Name" required maxlength="40" aria-label="Name">
        <select id="u-role" aria-label="Role"><option>reviewer</option><option>lead</option></select>
        <input type="text" id="u-langs" placeholder="Lead for (de, fr; empty = all)" maxlength="100" aria-label="Lead for languages" style="width:210px">
        <button class="btn primary" type="submit">Create invite link</button></form></div>
      <div class="box"><h3>Load a game file</h3>
        <p class="sub">Run <span class="mono">python tools/locale_review.py</span> and upload the <span class="mono">.json</span> it writes to private/locale_review/. Reviews and decisions stay.</p>
        <form id="iform" class="row"><input type="file" id="i-file" accept=".json,application/json" required aria-label="Data file"><button class="btn primary" type="submit">Upload</button></form>
        ${S.releases.length ? `<div class="tbl" style="margin-top:8px"><table><thead><tr><th>File</th><th>Loaded</th><th class="num">Messages</th></tr></thead><tbody>${S.releases.map(r => `<tr><td>${esc(r.release_id)}${r.is_current ? ` <span class="chip good">current</span>` : ""}</td><td>${when(r.imported_at)}</td><td class="num">${fmt(r.messages || 0)}</td></tr>`).join("")}</tbody></table></div>` : ""}
      </div></div>` : ""}
    <div class="box" style="margin-top:14px;max-width:520px"><h3>Change your password</h3><form id="pform" class="form">
      <input type="password" id="p-old" placeholder="Current password" autocomplete="current-password" required aria-label="Current password">
      <input type="password" id="p-new" placeholder="New password (10 characters or more)" autocomplete="new-password" required minlength="10" aria-label="New password">
      <div><button class="btn" type="submit">Change password</button></div></form></div>`;
  $("#uform")?.addEventListener("submit", async e => {
    e.preventDefault();
    const name = $("#u-name").value.trim();
    try { const r = await api("user_create", { name, role: $("#u-role").value, langs: $("#u-langs").value }); st.invite = { name, token: r.token }; await refresh(true); }
    catch (err) { toast(err.message, true); }
  });
  $("#iform")?.addEventListener("submit", async e => {
    e.preventDefault();
    const fd = new FormData(); fd.append("file", $("#i-file").files[0]);
    try { const r = await api("import", fd, true); toast(`Loaded ${r.release} (${fmt(r.messages)} messages)`); await loadData(true); }
    catch (err) { toast(err.message, true); }
  });
  $("#pform").addEventListener("submit", async e => {
    e.preventDefault();
    try { await api("password", { old: $("#p-old").value, new: $("#p-new").value }); toast("Password changed"); e.target.reset(); }
    catch (err) { toast(err.message, true); }
  });
}

// --- actions ------------------------------------------------------------------------------------------

function cardVal(card, f) { return card.querySelector(`[data-f="${f}"]`)?.value ?? ""; }
function cardMsg(card, text) { const m = card.querySelector("[data-msg]"); if (m) m.textContent = text; else toast(text, true); }

document.addEventListener("click", async e => {
  const t = e.target.closest("[data-act], [data-view], [data-clear], [data-p], .tree button");
  if (!t) return;
  if (t.dataset.view) return setView(t.dataset.view);
  if (t.matches(".tree button")) { st.area = t.dataset.a; st.screen = t.dataset.s || ""; st.openArea = st.area; st.page = 0; renderTree(); renderList(); return; }
  if (t.dataset.clear) { if (t.dataset.clear === "keys") { st.keys = null; st.keysLabel = ""; } else { st.area = ""; st.screen = ""; renderTree(); } st.page = 0; renderList(); return; }
  if (t.dataset.p) { st.page += Number(t.dataset.p); renderList(); $("#view").scrollIntoView({ block: "start" }); return; }
  const act = t.dataset.act, card = t.closest(".card"), key = card?.dataset.k, r = key ? BYKEY.get(key) : null;
  const run = async (fn, okText) => { try { await fn(); if (okText) toast(okText); await refresh(false, key); } catch (err) { card ? cardMsg(card, err.message) : toast(err.message, true); } };
  switch (act) {
    case "logout": try { await api("logout", {}); } finally { location.href = location.pathname; } return;
    case "shot-add": return openShots(key);
    case "shot-view": return openShots(key, Number(t.dataset.id));
    case "howto-hide": store.set("howtoHidden", true); renderHowto(); return;
    case "howto-show": store.set("howtoHidden", false); renderHowto(); return;
    case "stat":
      if (t.dataset.f.startsWith("@")) return setView(t.dataset.f.slice(1));
      st.status = t.dataset.f; st.keys = null; st.keysLabel = ""; st.area = ""; st.screen = ""; st.page = 0; setView("messages"); return;
    case "ok": st.editing = null; dirty.delete(key); return run(() => api("review", { key, verdict: "ok" }), "Saved");
    case "edit": st.editing = key; rerenderCard(key); document.getElementById("sg-" + key)?.focus(); return;
    case "cancel": st.editing = null; dirty.delete(key); rerenderCard(key); return;
    case "save": {
      const text = cardVal(card, "text").trim();
      if (placeholders(text) !== placeholders(r.en)) return cardMsg(card, "Keep the placeholders of the English text, like {driver}, exactly as they are.");
      if (text === r.de) return cardMsg(card, "That is the current text. Press Looks good instead, or change it.");
      st.editing = null; dirty.delete(key);
      return run(() => api("review", { key, verdict: "fix", text, reason: cardVal(card, "reason") }), "Suggestion saved");
    }
    case "unreview": st.editing = null; return run(() => api("unreview", { key }), "Review removed");
    case "vote": return run(() => api("vote", { review_id: Number(t.dataset.id), on: t.dataset.on === "1" }));
    case "use": { const v = S.reviews.find(x => x.id === Number(t.dataset.id)); st.leadText.set(key, v.text); st.leadOpen.add(key); st.useReview = st.useReview || new Map(); st.useReview.set(key, v.id); rerenderCard(key); return; }
    case "decide": {
      const status = t.dataset.s, text = cardVal(card, "leadtext").trim();
      if (status === "approved") {
        if (placeholders(text) !== placeholders(r.en)) return cardMsg(card, "The placeholders must match the English text.");
        if (text === r.de) return cardMsg(card, "This is the current German text, so there is nothing to send.");
      }
      const used = st.useReview?.get(key) || (S.reviews.find(v => v.msg_key === key && v.verdict === "fix" && v.text === text)?.id ?? 0);
      return run(async () => {
        const res = await api("decide", { key, status, text, note: cardVal(card, "leadnote"), review_id: used });
        st.leadText.delete(key); st.leadNote.delete(key); st.leadOpen.delete(key); dirty.delete(key);
        if (res.was_sent) toast("This change was sent already. The new decision goes out with the next package.");
      }, { approved: "Approved", rejected: "Rejected", discuss: "Marked for discussion" }[status]);
    }
    case "undecide": return run(() => api("undecide", { key }), "Decision removed");
    case "comment": { const body = cardVal(card, "comment").trim(); if (!body) return; st.commentsOpen.add(key); dirty.delete(key); return run(() => api("comment", { key, body })); }
    case "uncomment": return run(() => api("uncomment", { id: Number(t.dataset.id) }));
    case "claim": return run(() => api("claim", { area: t.dataset.k }), "Claimed");
    case "unclaim": return run(() => api("claim", { area: t.dataset.k, release: 1 }), "Released");
    case "area-show": st.area = t.dataset.a; st.screen = t.dataset.s; st.openArea = st.area; st.keys = null; st.keysLabel = ""; st.page = 0; setView("messages"); return;
    case "area-toggle": st.areasOpen = st.areasOpen || new Set(); st.areasOpen.has(t.dataset.a) ? st.areasOpen.delete(t.dataset.a) : st.areasOpen.add(t.dataset.a); renderView(); return;
    case "gl-agree": { const tm = S.terms.find(x => x.id === Number(t.dataset.id)), m = tm.langs[S.lang];
      return run(() => api("glossary", { id: tm.id, en_term: tm.en_term, de_term: m.term, keep_english: m.term ? 0 : 1, note: m.note, status: "agreed" }), "Agreed"); }
    case "gl-filter": st.glFilter = t.dataset.f; renderView(); return;
    case "gl-uses": { const tm = S.terms.find(x => x.id === Number(t.dataset.id)), re = termRegex(tm.en_term);
      return showKeys(ROWS.filter(r => re.test(r.en)).map(r => r.key), `Messages with "${tm.en_term}"`); }
    case "gl-edit": st.glEdit = Number(t.dataset.id); renderView(); window.scrollTo(0, 0); return;
    case "gl-cancel": st.glEdit = null; renderView(); return;
    case "gl-del": return run(() => api("unglossary", { id: Number(t.dataset.id) }), "Deleted");
    case "gl-show": { const g = S.glossary.find(x => x.id === Number(t.dataset.id)); const e2 = IDX.glossary.find(x => x.id === g.id);
      const ks = ROWS.filter(r2 => e2.re.test(r2.en) && !(IDX.decisions.get(r2.key)?.status === "approved" ? IDX.decisions.get(r2.key).text : r2.de).toLowerCase().includes(g.de_term.toLowerCase())).map(r2 => r2.key);
      return showKeys(ks, `Breaks "${g.en_term} → ${g.de_term}"`); }
    case "term-show": { const tm = D.terms[t.dataset.t], vv = tm.variants[t.dataset.v]; return showKeys(vv[1], `"${tm.en}" as "${vv[0]}"`); }
    case "term-add": { const tm = D.terms[t.dataset.t]; st.glPrefill = { en: tm.en, de: tm.variants[0][0] }; st.glEdit = null; renderView(); window.scrollTo(0, 0); return; }
    case "word-show": { const [w, ks] = st.wordList[t.dataset.i]; return showKeys(ks, `English word "${w}"`); }
    case "word-add": { const [w] = st.wordList[t.dataset.i]; st.glPrefill = { en: w, de: "" }; st.glEdit = null; renderView(); window.scrollTo(0, 0); return; }
    case "batch-preview": return showKeys(S.decisions.filter(d => d.status === "approved" && !d.batch_id).map(d => d.msg_key), "Approved, not in a package");
    case "batch-send": { const id = Number(t.dataset.id), note = document.querySelector(`.sentnote[data-id="${id}"]`)?.value || "";
      try { await api("batch_sent", { id, sent: 1, note }); toast("Marked as sent"); await refresh(true); } catch (err) { toast(err.message, true); } return; }
    case "batch-unsend": try { await api("batch_sent", { id: Number(t.dataset.id), sent: 0 }); toast("Marked as not sent"); await refresh(true); } catch (err) { toast(err.message, true); } return;
    case "batch-delete":
      if (t.dataset.confirm !== "1") { t.dataset.confirm = "1"; t.textContent = "Really delete? Its changes stay approved"; return; }
      try { await api("batch_delete", { id: Number(t.dataset.id) }); toast("Package deleted. Its changes are approved again."); await refresh(true); } catch (err) { toast(err.message, true); } return;
    case "batch-show": { const id = Number(t.dataset.id); const b = S.batches.find(x => x.id === id);
      return showKeys(S.decisions.filter(d => d.batch_id === id).map(d => d.msg_key), `Package ${b.name}`); }
    case "fu": st.fuState = t.dataset.s; renderView(); return;
    case "fu-open": return showKeys([t.dataset.k], "Follow-up");
    case "fu-search": st.keys = null; st.keysLabel = ""; st.q = t.dataset.q.toLowerCase(); setView("messages"); return;
    case "copy-invite": try { await navigator.clipboard.writeText($("#inv").value); toast("Copied"); } catch { $("#inv").select(); toast("Selected. Press Ctrl+C."); } return;
    case "reinvite": try { const res = await api("user_reinvite", { id: Number(t.dataset.id) }); st.invite = { name: t.dataset.name, token: res.token }; await refresh(true); } catch (err) { toast(err.message, true); } return;
    case "remove":
      if (t.dataset.confirm !== "1") { t.dataset.confirm = "1"; t.textContent = `Really remove ${t.dataset.name}?`; return; }
      try { await api("user_remove", { id: Number(t.dataset.id) }); toast("Removed. Their reviews stay."); await refresh(true); } catch (err) { toast(err.message, true); } return;
  }
});

document.addEventListener("change", async e => {
  const t = e.target;
  if (t.dataset.act === "role" || t.dataset.act === "langs") {
    const row = t.closest("tr"), role = row.querySelector('[data-act="role"]').value, langs = row.querySelector('[data-act="langs"]')?.value || "";
    try { await api("user_role", { id: Number(t.dataset.id), role, langs }); toast("Saved"); await refresh(true); } catch (err) { toast(err.message, true); }
  }
  if (t.id === "langsel") {
    st.lang = t.value; store.set("lang", st.lang);
    Object.assign(st, { area: "", screen: "", keys: null, keysLabel: "", page: 0, status: "", flag: "" });
    try { S = await api("state"); indexState(); await loadData(false); frame(); renderHowto(); renderStats(); setView(st.view); } catch (err) { toast(err.message, true); }
  }
});
document.addEventListener("input", e => {
  const card = e.target.closest(".card"); if (!card) return;
  const key = card.dataset.k; dirty.add(key);
  if (e.target.dataset.f === "leadtext") st.leadText.set(key, e.target.value);
  if (e.target.dataset.f === "leadnote") st.leadNote.set(key, e.target.value);
});
document.addEventListener("toggle", e => {
  const card = e.target.closest?.(".card"); if (!card) return;
  const set = e.target.matches("[data-lead]") ? st.leadOpen : e.target.matches("[data-comments]") ? st.commentsOpen : null;
  if (set) e.target.open ? set.add(card.dataset.k) : set.delete(card.dataset.k);
}, true);

// --- loading and refresh ------------------------------------------------------------------------------

async function loadData(rerender) {
  const res = await fetch("api.php?a=data&l=" + encodeURIComponent(st.lang), { credentials: "same-origin" });
  const data = await res.json();
  if (data.error) throw new Error(data.error);
  if (data.empty) { D = null; ROWS = []; P = []; BYKEY = new Map(); }
  else {
    D = data; P = D.places;
    ROWS = D.rows.map(r => ({ key: r[0], en: r[1], de: r[2], places: r[3], flags: r[4], hay: (r[0] + "\n" + r[1] + "\n" + r[2]).toLowerCase() }));
    for (const r of ROWS) r.score = score(r);
    BYKEY = new Map(ROWS.map(r => [r.key, r]));
  }
  if (rerender) { await refresh(true); }
}

async function refresh(full, key) {
  S = await api("state");
  CSRF = S.csrf || CSRF; st.lang = S.lang;
  indexState();
  renderStats();
  if (full || st.view !== "messages") {
    if (st.view === "messages" && !full) return;
    if (!$("#view")) frame();
    renderView(); return;
  }
  if (key) { rerenderCard(key); renderTree(); return; }
  // background refresh: redraw only cards nobody is typing in
  renderTree();
  for (const el of document.querySelectorAll(".card")) {
    const k = el.dataset.k;
    if (!dirty.has(k) && st.editing !== k && !el.contains(document.activeElement)) rerenderCard(k);
  }
}

async function start() {
  if (BOOT.mode !== "app") return authPage();
  try {
    S = await api("state"); st.lang = S.lang; store.set("lang", st.lang); indexState();
    await loadData(false);
  } catch (err) { $("#app").innerHTML = `<div class="empty">${esc(err.message)}</div>`; return; }
  frame(); renderHowto(); renderStats();
  if (!TABS.some(([v]) => v === st.view)) st.view = "messages";
  setView(st.view);
  setInterval(() => { if (document.visibilityState === "visible") refresh(false).catch(() => {}); }, 60000);
}
start();
