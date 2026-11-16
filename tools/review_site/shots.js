// Screenshots: a picture of a game screen, and for each message on it a box around the text.
// Cards show a zoom on that box; the dialog uploads (paste, drop or pick), draws boxes, and
// walks through the other messages of the same screen. Uses the globals of app.js.
"use strict";

const shotUrl = id => "api.php?a=shot&id=" + id;

/** Links of a message, best first: this language, then English, then the others. */
function linksFor(key) {
  const rank = l => (IDX.shots.get(l.shot_id).lang === S.lang ? 0 : IDX.shots.get(l.shot_id).lang === "en" ? 1 : 2);
  return (IDX.links.get(key) || []).slice().sort((a, b) => rank(a) - rank(b) || b.shot_id - a.shot_id);
}

/** A box showing the link's rectangle with some room around it, at the image's real proportions. */
function zoomHtml(l, big = false) {
  const sh = IDX.shots.get(l.shot_id);
  const pad = Math.max(l.w, l.h * sh.height / sh.width) * 0.35 + 0.01;
  let x0 = Math.max(0, l.x - pad), x1 = Math.min(1, l.x + l.w + pad);
  const padY = pad * sh.width / sh.height;
  let y0 = Math.max(0, l.y - padY), y1 = Math.min(1, l.y + l.h + padY);
  const rw = x1 - x0, rh = y1 - y0;
  const ratio = (rw * sh.width) / (rh * sh.height);
  const posX = rw >= 1 ? 0 : x0 / (1 - rw) * 100, posY = rh >= 1 ? 0 : y0 / (1 - rh) * 100;
  const mark = `left:${(l.x - x0) / rw * 100}%;top:${(l.y - y0) / rh * 100}%;width:${l.w / rw * 100}%;height:${l.h / rh * 100}%`;
  const maxW = big ? 900 : 340, maxH = big ? 500 : 150;
  const zw = Math.round(Math.min(maxW, maxH * ratio)), zh = Math.round(zw / ratio);
  return `<span class="zoom ${big ? "big" : ""}" style="width:${zw}px;height:${zh}px;background-image:url('${shotUrl(sh.id)}');background-size:${100 / rw}% auto;background-position:${posX}% ${posY}%">
    <span class="zmark" style="${mark}"></span></span>`;
}

function shotsHtml(r) {
  const links = linksFor(r.key);
  const tiles = links.slice(0, 3).map(l => {
    const sh = IDX.shots.get(l.shot_id);
    return `<button class="ztile" data-act="shot-view" data-id="${sh.id}" title="Open the whole screenshot">${zoomHtml(l)}
      <span class="msg">${sh.screen ? `<b>${esc(sh.screen)}</b> · ` : ""}${esc(langName(sh.lang))} screenshot${sh.lang !== S.lang ? " (other language)" : ""}${(sh.caption || "").startsWith("auto:") ? ", taken automatically" : ""}</span></button>`;
  }).join("");
  return `<div class="shots">${tiles}
    <div class="act">${!links.length && isMail(r) ? `<span class="msg">Mail or news text: no screenshot needed.</span>` : ""}
    <button class="btn small" data-act="shot-add">${links.length ? "Add another screenshot" : "Add screenshot"}</button>
    ${links.length > 3 ? `<span class="msg">${links.length - 3} more</span>` : ""}</div></div>`;
}

// --- dialog --------------------------------------------------------------------------------

const SD = { key: null, shotId: null, file: null, blobUrl: null, rect: null, mode: "pick", q: "" };

function openShots(key, shotId = null) {
  Object.assign(SD, { key, shotId, file: null, rect: null, q: "", mode: shotId ? "mark" : "pick" });
  if (SD.blobUrl) { URL.revokeObjectURL(SD.blobUrl); SD.blobUrl = null; }
  if (shotId) { const l = (IDX.links.get(key) || []).find(x => x.shot_id === shotId); SD.rect = l ? { x: l.x, y: l.y, w: l.w, h: l.h } : null; }
  let dlg = $("#shotdlg");
  if (!dlg) {
    dlg = document.createElement("div"); dlg.id = "shotdlg"; dlg.className = "modal"; dlg.setAttribute("role", "dialog"); dlg.setAttribute("aria-modal", "true");
    document.body.appendChild(dlg);
    dlg.addEventListener("click", shotClick);
    dlg.addEventListener("pointerdown", drawStart);
    dlg.addEventListener("input", e => { if (e.target.id === "sd-q") { SD.q = e.target.value.toLowerCase(); renderNext(); } });
    dlg.addEventListener("change", e => { if (e.target.id === "sd-file" && e.target.files[0]) takeFile(e.target.files[0]); });
    dlg.addEventListener("dragover", e => { e.preventDefault(); });
    dlg.addEventListener("drop", e => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) takeFile(f); });
  }
  dlg.hidden = false; document.body.classList.add("noscroll");
  renderShots();
}
function closeShots() {
  const dlg = $("#shotdlg"); if (dlg) dlg.hidden = true;
  document.body.classList.remove("noscroll");
  if (SD.blobUrl) { URL.revokeObjectURL(SD.blobUrl); SD.blobUrl = null; }
  if ($("#list")) { renderList(); renderTree(); }
}
document.addEventListener("paste", e => {
  if ($("#shotdlg")?.hidden !== false || SD.mode !== "pick") return;
  const item = [...(e.clipboardData?.items || [])].find(i => i.type.startsWith("image/"));
  if (item) { e.preventDefault(); takeFile(item.getAsFile()); }
});
document.addEventListener("keydown", e => { if (e.key === "Escape" && $("#shotdlg")?.hidden === false) closeShots(); });

function takeFile(f) {
  if (!/^image\/(png|jpeg|webp|gif)$/.test(f.type)) { toast("Use a PNG, JPEG or WebP image.", true); return; }
  if (f.size > 12 * 1024 * 1024) { toast("The image is larger than 12 MB.", true); return; }
  SD.file = f; SD.shotId = null; SD.rect = null; SD.mode = "mark";
  if (SD.blobUrl) URL.revokeObjectURL(SD.blobUrl);
  SD.blobUrl = URL.createObjectURL(f);
  renderShots();
}

const msgPlace = r => P[r.places[0]];

function renderShots() {
  const dlg = $("#shotdlg"), r = BYKEY.get(SD.key);
  const head = `<div class="mhead"><div style="min-width:0"><div class="lbl">Screenshot for</div><div class="en"><b>${esc(r.en)}</b></div>
      <div class="where">${placeHtml(r.places[0])}</div></div><button class="btn" data-act="sd-close">Close</button></div>`;
  if (SD.mode === "pick") {
    const [a, s] = msgPlace(r);
    const all = [...IDX.shots.values()];
    const same = all.filter(x => x.area === a && x.screen === s), other = all.filter(x => !(x.area === a && x.screen === s));
    const thumbs = list => list.slice().reverse().map(x => `<button class="thumb" data-act="sd-use" data-id="${x.id}"><img src="${shotUrl(x.id)}" alt="" loading="lazy" width="${x.width}" height="${x.height}">
      <span class="msg">${esc(x.screen || "unsorted")} · ${esc(langName(x.lang))}</span></button>`).join("");
    dlg.innerHTML = `<div class="mbox">${head}
      <div class="drop" tabindex="0"><b>Paste a screenshot here (Ctrl+V)</b><br><span class="msg">or drop an image file, or</span>
        <label class="btn small" style="display:inline-block;margin-top:6px">Choose a file<input type="file" id="sd-file" accept="image/png,image/jpeg,image/webp" hidden></label>
        <p class="msg" style="margin-top:8px">On Windows, Win+Shift+S copies part of the screen. Full game screens work best, one picture per screen.</p></div>
      <div class="row" style="margin:8px 0"><label class="row">Game language in the picture
        <select id="sd-lang">${[...new Set([S.lang, ...S.langs, "en"])].map(l => `<option value="${esc(l)}">${esc(langName(l))}</option>`).join("")}</select></label></div>
      ${same.length ? `<h3>Screenshots of ${esc(s)}</h3><div class="thumbs">${thumbs(same)}</div>` : ""}
      ${other.length ? `<details ${same.length ? "" : "open"}><summary class="lbl">Other screenshots (${other.length})</summary><div class="thumbs">${thumbs(other)}</div></details>` : ""}
    </div>`;
    dlg.querySelector(".drop").focus();
    return;
  }
  const sh = SD.shotId ? IDX.shots.get(SD.shotId) : null;
  const src = sh ? shotUrl(sh.id) : SD.blobUrl;
  const others = sh ? S.shot_links.filter(l => l.shot_id === sh.id && l.msg_key !== SD.key) : [];
  const mine = sh && (IDX.links.get(SD.key) || []).find(l => l.shot_id === sh.id);
  const linked = !!mine;
  if (mine && !SD.rect) SD.rect = { x: mine.x, y: mine.y, w: mine.w, h: mine.h };
  const canDelete = sh && (sh.user_id === me().id || isLead());
  dlg.innerHTML = `<div class="mbox wide">${head}
    <p class="msg">${SD.rect ? "Drag again to redraw the yellow box." : "Drag a box around this text on the picture."} Dashed boxes are texts already marked.${sh ? ` Picture by ${esc(uname(sh.user_id))}, ${esc(langName(sh.lang))}.` : ""}</p>
    <div class="stage" id="stage"><img src="${src}" alt="Game screenshot" draggable="false" id="sd-img">
      ${others.map(l => `<span class="obox" style="${boxStyle(l)}" title="${esc(BYKEY.get(l.msg_key)?.en || l.msg_key)}"><span class="olabel">${esc((BYKEY.get(l.msg_key)?.en || l.msg_key).slice(0, 30))}</span></span>`).join("")}
      <span class="nbox" id="nbox" style="${SD.rect ? boxStyle(SD.rect) : "display:none"}"></span></div>
    <div class="act" style="margin-top:8px">
      <button class="btn primary" data-act="sd-save" ${SD.rect ? "" : "disabled"}>${linked ? "Save the box" : "Save"}</button>
      ${linked ? `<button class="btn" data-act="sd-unlink">Remove from this message</button>` : ""}
      ${canDelete ? `<button class="btn" data-act="sd-delete">Delete the screenshot</button>` : ""}
      <button class="btn" data-act="sd-back">Other screenshot</button>
      <span class="msg err" id="sd-msg"></span>
    </div>
    ${sh ? `<div id="sd-next"></div>` : ""}
  </div>`;
  if (sh) renderNext();
}

function boxStyle(b) { return `left:${b.x * 100}%;top:${b.y * 100}%;width:${b.w * 100}%;height:${b.h * 100}%`; }

/** The other messages of this screen, to mark on the same picture one after another. */
function renderNext() {
  const el = $("#sd-next"), sh = IDX.shots.get(SD.shotId); if (!el || !sh) return;
  const done = new Set(S.shot_links.filter(l => l.shot_id === sh.id).map(l => l.msg_key));
  const pool = ROWS.filter(r => r.places.some(i => P[i][0] === sh.area && P[i][1] === sh.screen));
  const todo = pool.filter(r => !done.has(r.key) && (!SD.q || r.hay.includes(SD.q)));
  el.innerHTML = `<h3 style="margin-top:12px">More texts on ${esc(sh.screen || "this screen")}: ${fmt(done.size)} of ${fmt(pool.length)} marked</h3>
    <input type="search" id="sd-q" placeholder="Search the texts of this screen" value="${esc(SD.q)}" aria-label="Search" style="width:100%;margin-bottom:6px">
    <div class="nextlist">${todo.slice(0, 60).map(r => `<button class="linkish" data-act="sd-next" data-k="${esc(r.key)}">${esc(r.en.slice(0, 90))}</button>`).join("") || `<span class="msg">All texts of this screen are marked.</span>`}</div>`;
  const q = $("#sd-q"); if (q && SD.q) { q.focus(); q.setSelectionRange(q.value.length, q.value.length); }
}

let drawing = null;
function drawStart(e) {
  const stage = e.target.closest?.("#stage"); if (!stage || e.button !== 0) return;
  e.preventDefault();
  const box = $("#sd-img").getBoundingClientRect();
  const pt = ev => ({ x: Math.min(1, Math.max(0, (ev.clientX - box.left) / box.width)), y: Math.min(1, Math.max(0, (ev.clientY - box.top) / box.height)) });
  const a = pt(e), nbox = $("#nbox");
  drawing = { a };
  stage.setPointerCapture(e.pointerId);
  const move = ev => {
    const b = pt(ev);
    SD.rect = { x: Math.min(a.x, b.x), y: Math.min(a.y, b.y), w: Math.abs(b.x - a.x), h: Math.abs(b.y - a.y) };
    nbox.style.cssText = boxStyle(SD.rect);
  };
  const up = () => {
    stage.removeEventListener("pointermove", move); stage.removeEventListener("pointerup", up); drawing = null;
    if (SD.rect && (SD.rect.w < 0.003 || SD.rect.h < 0.003)) { SD.rect = null; nbox.style.display = "none"; }
    $('[data-act="sd-save"]').disabled = !SD.rect;
  };
  stage.addEventListener("pointermove", move); stage.addEventListener("pointerup", up);
}

async function shotClick(e) {
  if (e.target.id === "shotdlg") return closeShots();
  const t = e.target.closest("[data-act]"); if (!t) return;
  const msg = text => { const m = $("#sd-msg"); m ? m.textContent = text : toast(text, true); };
  try {
    switch (t.dataset.act) {
      case "sd-close": return closeShots();
      case "sd-back": SD.mode = "pick"; SD.shotId = null; SD.rect = null; return renderShots();
      case "sd-use": SD.shotId = Number(t.dataset.id); SD.rect = null; SD.mode = "mark"; return renderShots();
      case "sd-next": SD.key = t.dataset.k; SD.rect = null; SD.q = ""; return renderShots();
      case "sd-save": {
        if (!SD.rect) return msg("Drag a box around the text first.");
        t.disabled = true;
        if (!SD.shotId) {
          const r = BYKEY.get(SD.key), [a, s] = msgPlace(r);
          const fd = new FormData();
          fd.append("file", SD.file, SD.file.name || "screenshot.png");
          fd.append("area", a); fd.append("screen", s); fd.append("shot_lang", $("#sd-lang")?.value || SD.lang || S.lang);
          const up = await api("shot_upload", fd, true);
          SD.shotId = up.id; SD.file = null;
        }
        await api("shot_link", { shot_id: SD.shotId, key: SD.key, ...SD.rect });
        S = await api("state"); indexState();
        toast("Saved. Pick the next text of this screen, or close.");
        SD.rect = null;
        return renderShots();
      }
      case "sd-unlink":
        await api("shot_unlink", { shot_id: SD.shotId, key: SD.key });
        S = await api("state"); indexState(); toast("Removed"); return closeShots();
      case "sd-delete":
        if (t.dataset.confirm !== "1") { t.dataset.confirm = "1"; t.textContent = "Really delete it for all messages?"; return; }
        await api("shot_delete", { id: SD.shotId });
        S = await api("state"); indexState(); toast("Screenshot deleted"); return closeShots();
    }
  } catch (err) { t.disabled = false; msg(err.message); }
}

// Remember the language chosen in the pick screen while the dialog moves on to drawing.
document.addEventListener("change", e => { if (e.target.id === "sd-lang") SD.lang = e.target.value; });
