// La sonde CDP du témoin du scrub (lot P-C1) : charge la page bâtie sur le manifeste
// factice, scrolle à quatre positions SANS lissage, et rend l'activation observée.
// usage: node temoin-scrub-sonde.mjs <url>
// Chrome doit tourner avec --remote-debugging-port=9222 (le banc du chef le tient) ;
// sans lui, temoin-scrub.py le DIT au lieu de se taire.
//
// Les quatre positions, contre le contrat (mouvement = 0.66 du manifeste factice) :
//   p=0.05 → k=0, q=0.25 < mouvement : AUCUNE scène active, le canevas seul ;
//   p=0.14 → k=0, q=0.70 ≥ mouvement : la scène 0 active ;
//   p=0.55 → k=2, q=0.75 ≥ mouvement : la scène 2 active ;
//   p=0.46 → k=2, q=0.30 < mouvement : aucune active (le retour aussi).
const url = process.argv[2];
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
await send("Network.enable");
await send("Network.setCacheDisabled", { cacheDisabled: true });
await send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
await send("Page.navigate", { url });
const debut = Date.now();
while (!events.includes("Page.loadEventFired")) {
  if (Date.now() - debut > 20000) throw new Error("undetermined: la page n'a jamais signalé son chargement en 20 s");
  await new Promise((r) => setTimeout(r, 100));
}
const sonde = `(async () => {
  const seq = document.querySelector(".sequence");
  const H = seq.offsetHeight - innerHeight;
  const lire = async (p) => {
    scrollTo({ top: seq.offsetTop + p * H, behavior: "instant" });
    await new Promise((r) => setTimeout(r, 250));
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
    return {
      p,
      actif: [...document.querySelectorAll(".scene")].findIndex((s) => s.classList.contains("actif")),
      film: document.querySelector(".colle").classList.contains("film"),
    };
  };
  await new Promise((r) => setTimeout(r, 1500));
  return JSON.stringify({
    canevas: !!document.querySelector("canvas.film"),
    mouvement: await lire(0.05),
    arret0: await lire(0.14),
    arret2: await lire(0.55),
    retour: await lire(0.46),
  });
})()`;
const r = await send("Runtime.evaluate", { expression: sonde, awaitPromise: true, returnByValue: true });
console.log(r.result.value);
await send("Page.close").catch(() => {});
process.exit(0);
