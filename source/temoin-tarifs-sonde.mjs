// La sonde CDP du témoin des tarifs (engagement.html refait, 11/09).
// usage: node temoin-tarifs-sonde.mjs <url>
// Chrome sur 9222 ; viewport forcé 1440×900 (le panneau caché rend 29 px).
//
// Quatre affirmations, exécutées :
//   1. le compte-à-l'arrivée retombe sur la valeur ÉCRITE : après chargement, chaque
//      .c-prix affiche exactement le texte du HTML source (lu via data du DOM statique
//      passé en argv — non : relu ici par une 2e passe sans script) ;
//   2. le curseur est UN clavier : focus + flèches changent aria-valuenow et
//      réécrivent #etat ;
//   3. l'arithmétique du grand état : chaque montant $ affiché par #etat appartient à
//      l'ensemble dérivé des constantes LUES DANS LE JS SERVI (LIC, PART, CAMP :
//      LIC·PART, LIC·(1−PART), LIC, CAMP, 0) — jamais retapées dans ce témoin ;
//   4. sans JavaScript : #curseur et #courir invisibles, les cartes .pap toutes
//      pleines (opacité 1), la page lisible.
const [url, statiquesArg] = process.argv.slice(2);   // les .c-prix du HTML brut, passés par le pilote (la CSP du site refuse fetch in-page, à raison)
const target = await fetch("http://127.0.0.1:9222/json/new?" + encodeURIComponent("about:blank"), { method: "PUT" }).then((r) => r.json());
const ws = new WebSocket(target.webSocketDebuggerUrl);
let id = 0;
const pend = new Map();
const events = [];
const send = (m, p = {}) => new Promise((res, rej) => {
  const i = ++id;
  pend.set(i, { res, rej });
  ws.send(JSON.stringify({ id: i, method: m, params: p }));
});
ws.onmessage = (m) => {
  const d = JSON.parse(m.data);
  if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); }
  else if (d.method) events.push(d.method);
};
await new Promise((r) => { ws.onopen = r; });
await send("Page.enable");
await send("Runtime.enable");
await send("Network.enable");
await send("Network.setCacheDisabled", { cacheDisabled: true });
await send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });

const naviguer = async () => {
  events.length = 0;
  await send("Page.navigate", { url });
  const debut = Date.now();
  while (!events.includes("Page.loadEventFired")) {
    if (Date.now() - debut > 20000) throw new Error("undetermined: la page n'a jamais signalé son chargement");
    await new Promise((r) => setTimeout(r, 100));
  }
};
const evaluer = async (expr) => {
  const r = await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error("page: " + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
};
const fautes = [];
const dire = (ok, quoi) => { console.log((ok ? "  ok  " : "  ROUGE ") + quoi); if (!ok) fautes.push(quoi); };

await naviguer();

/* les constantes, LUES du JS servi — jamais retapées */
const C = JSON.parse(await evaluer(`(() => {
  const src = [...document.scripts].map((s) => s.textContent).join("\\n");
  const m = src.match(/const LIC = (\\d+), PART = ([\\d.]+), CAMP = (\\d+)/);
  return JSON.stringify(m ? { LIC: +m[1], PART: +m[2], CAMP: +m[3] } : null);
})()`));
dire(C !== null, "les constantes LIC/PART/CAMP se lisent dans le JS servi");
if (C === null) process.exit(1);

/* 1. le compte-à-l'arrivée retombe sur la valeur écrite (les textes du HTML brut
   viennent du pilote : la CSP de la page — connect-src 'none' — refuse fetch, à raison) */
const statiques = JSON.parse(statiquesArg);
await evaluer(`new Promise((r) => setTimeout(r, 2500))`);   // le compte dure ~1-2 s
const vivants = JSON.parse(await evaluer(`JSON.stringify([...document.querySelectorAll(".c-prix")].map((e) => e.textContent.trim()))`));
dire(JSON.stringify(vivants) === JSON.stringify(statiques),
     `le compte retombe sur l'écrit : ${vivants.join(" · ")}`);

/* 2. le curseur au clavier */
const avant = JSON.parse(await evaluer(`(() => {
  const c = document.getElementById("curseur");
  c.focus();
  return JSON.stringify({ v: c.getAttribute("aria-valuenow"), e: document.getElementById("etat").textContent });
})()`));
for (let i = 0; i < 25; i++) await send("Input.dispatchKeyEvent", { type: "keyDown", key: "ArrowRight", code: "ArrowRight", windowsVirtualKeyCode: 39 });
await evaluer(`new Promise((r) => setTimeout(r, 300))`);
const apres = JSON.parse(await evaluer(`JSON.stringify({ v: document.getElementById("curseur").getAttribute("aria-valuenow"), e: document.getElementById("etat").textContent })`));
dire(apres.v !== avant.v, `les flèches déplacent le jour (aria-valuenow ${avant.v} → ${apres.v})`);
dire(apres.e !== avant.e, "le déplacement réécrit la phrase d'état");

/* 3. l'arithmétique : au MILIEU de l'année (jour ~72, campagne réglée + 30 % versés),
   là où l'état écrit ses montants — au jour 365, la phrase ne parle que du
   renouvellement et un « aucun montant » serait un faux rouge (vu au premier tir) */
for (let i = 0; i < 10; i++) await send("Input.dispatchKeyEvent", { type: "keyDown", key: "ArrowRight", code: "ArrowRight", windowsVirtualKeyCode: 39 });
await evaluer(`new Promise((r) => setTimeout(r, 300))`);
const etat = await evaluer(`document.getElementById("etat").textContent`);
const attendus = new Set([C.LIC, C.CAMP, Math.round(C.LIC * C.PART), Math.round(C.LIC * (1 - C.PART)), 0]
  .map((n) => n.toLocaleString("en-US")));
const montants = (etat.match(/\$\d{1,3}(?:,\d{3})*/g) || []).map((x) => x.slice(1));
const orphelins = montants.filter((m) => !attendus.has(m));
dire(montants.length > 0 && orphelins.length === 0,
     `chaque montant de l'état dérive des constantes servies (${montants.join(", ") || "aucun"}${orphelins.length ? " ; orphelins : " + orphelins.join(", ") : ""})`);

/* 4. sans JavaScript : curseur et bouton cachés, cartes pleines */
await send("Emulation.setScriptExecutionDisabled", { value: true });
await naviguer();
const sans = JSON.parse(await evaluer(`JSON.stringify({
  curseur: (() => { const e = document.getElementById("curseur"); const s = e && getComputedStyle(e); return e ? (s.display === "none" || s.visibility === "hidden" || e.offsetParent === null) : null; })(),
  courir: (() => { const e = document.getElementById("courir"); const s = e && getComputedStyle(e); return e ? (s.display === "none" || s.visibility === "hidden" || e.offsetParent === null) : null; })(),
  paps: [...document.querySelectorAll(".pap")].every((p) => +getComputedStyle(p).opacity >= 0.99),
  nPaps: document.querySelectorAll(".pap").length,
})`));
dire(sans.curseur === true, "sans script, le curseur est caché");
dire(sans.courir === true, "sans script, « run the year » est caché");
dire(sans.paps && sans.nPaps > 0, `sans script, les ${sans.nPaps} cartes sont pleines`);
await send("Emulation.setScriptExecutionDisabled", { value: false });

await send("Page.close").catch(() => {});
if (fautes.length) { console.log(`${fautes.length} ROUGE(S)`); process.exit(1); }
console.log("sonde des tarifs : tout vert, et elle a regardé");
process.exit(0);
