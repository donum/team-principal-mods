/* Season picker: one <select> with a group per series and an option per year, newest choice remembered.
 * Shared by our local review pages. Canonical copy: team-principal-mods/tools/web/season-picker.js.
 * Edit it there and run tools/web/sync_season_picker.py; the copies are overwritten.
 *
 *   const seasons = SeasonPicker.list(["dtm-2012", {id: "dtm-2013", note: "10 rounds"}]);
 *   const id = SeasonPicker.initial(seasons, {key: "my-page-season", fallback: "newest"});
 *   SeasonPicker.mount(selectEl, seasons, {value: id, key: "my-page-season", all: "All seasons",
 *                                          onChange: (id) => render()});
 *
 * A season is {id, series, year, label, note}. list() fills the gaps from the id ("dtm-2013",
 * "dtm/2013" or "DTM 2013" all give series "DTM", year "2013"). The "all" entry has the value "".
 * initial(): the hash parameter (opts.param, e.g. "season" for #season=dtm-2013), else the stored
 * choice (opts.key in localStorage), else opts.fallback: "newest", "oldest", "" (all) or an id.
 */
(function () {
  "use strict";
  // series id -> display name; anything missing is upper-cased
  const SERIES = { dtm: "DTM", f1: "F1", btcc: "BTCC", wtcc: "WTCC", wec: "WEC", indycar: "IndyCar", nascar: "NASCAR", gt: "GT" };
  const store = {
    get(k) { try { return k ? localStorage.getItem(k) : null; } catch (e) { return null; } },
    set(k, v) { try { if (k) localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  };
  const seriesName = (s) => SERIES[String(s).toLowerCase()] || String(s).toUpperCase();

  function split(id) {
    const m = /^(.+?)[-/ _]?(\d{4})$/.exec(String(id).trim());
    return m ? { series: m[1].replace(/[-/ _]+$/, ""), year: m[2] } : { series: String(id), year: "" };
  }
  function idOf(series, year) { return String(series).toLowerCase().replace(/\s+/g, "-") + "-" + year; }

  function list(items) {
    const seen = new Set(), out = [];
    for (const raw of items || []) {
      const x = typeof raw === "object" && raw ? { ...raw } : { id: String(raw) };
      const p = split(x.id || idOf(x.series || "", x.year || ""));
      x.series = x.series ? String(x.series) : seriesName(p.series);
      x.year = String(x.year || p.year);
      x.id = x.id || idOf(x.series, x.year);
      x.label = x.label || (x.series + " " + x.year).trim();
      if (!seen.has(x.id)) { seen.add(x.id); out.push(x); }
    }
    return out;
  }

  const byYear = (a, b) => String(a.year).localeCompare(String(b.year)) || a.id.localeCompare(b.id);

  function hashParam(name) {
    if (!name) return null;
    const h = location.hash.replace(/^#\/?/, "");
    return new URLSearchParams(h.includes("?") ? h.split("?")[1] : h).get(name);
  }

  function initial(seasons, opts) {
    opts = opts || {};
    const ok = (id) => id === "" ? opts.fallback === "" || opts.all : seasons.some((s) => s.id === id);
    for (const id of [hashParam(opts.param), store.get(opts.key)]) if (id !== null && ok(id)) return id;
    const sorted = [...seasons].sort(byYear);
    const f = opts.fallback === undefined ? "newest" : opts.fallback;
    if (f === "newest") return sorted.length ? sorted[sorted.length - 1].id : "";
    if (f === "oldest") return sorted.length ? sorted[0].id : "";
    return ok(f) ? f : "";
  }

  function mount(sel, seasons, opts) {
    opts = opts || {};
    const groups = {};
    seasons.forEach((s) => (groups[s.series] = groups[s.series] || []).push(s));
    sel.replaceChildren();
    const opt = (value, text) => { const o = document.createElement("option"); o.value = value; o.textContent = text; return o; };
    if (opts.all) sel.append(opt("", opts.all));
    for (const g of Object.keys(groups).sort()) {
      const og = document.createElement("optgroup");
      og.label = g;
      groups[g].sort(byYear).forEach((s) => og.append(opt(s.id, s.label + (s.note ? " · " + s.note : ""))));
      sel.append(og);
    }
    if (!sel.getAttribute("aria-label")) sel.setAttribute("aria-label", "Season");
    sel.value = opts.value !== undefined ? opts.value : initial(seasons, opts);
    sel.onchange = () => {
      store.set(opts.key, sel.value);
      if (opts.onChange) opts.onChange(sel.value, seasons.find((s) => s.id === sel.value) || null);
    };
    store.set(opts.key, sel.value);
    return sel;
  }

  window.SeasonPicker = { list, initial, mount, split, idOf, seriesName, SERIES };
})();
