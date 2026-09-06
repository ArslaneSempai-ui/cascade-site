// Capture native d'une page à taille et scroll exacts, via CDP (Chrome headless).
// usage: node capture.mjs <url> <largeur> <hauteur> <js-de-scroll|-> <sortie.png>
// Chrome doit tourner avec --remote-debugging-port=9222.
import { writeFileSync } from "node:fs";

const [url, w, h, scrollJs, out] = process.argv.slice(2);
const port = 9222;

const target = await fetch(`http://127.0.0.1:${port}/json/new?${encodeURIComponent("about:blank")}`, { method: "PUT" }).then(r => r.json());
const ws = new WebSocket(target.webSocketDebuggerUrl);
let id = 0;
const pend = new Map();
const send = (method, params = {}) => new Promise((res, rej) => {
  const mid = ++id;
  pend.set(mid, { res, rej });
  ws.send(JSON.stringify({ id: mid, method, params }));
});
const events = [];
ws.onmessage = (m) => {
  const d = JSON.parse(m.data);
  if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); }
  else if (d.method) events.push(d.method);
};
await new Promise(r => { ws.onopen = r; });

await send("Page.enable");
// le profil headless persiste entre les lancements : sans ceci, une page
// rebâtie peut être servie depuis le cache disque et la capture ment
await send("Network.enable");
await send("Network.setCacheDisabled", { cacheDisabled: true });
await send("Emulation.setDeviceMetricsOverride", { width: +w, height: +h, deviceScaleFactor: 1, mobile: false });
// A page is loaded when it SAYS so (Page.loadEventFired), never after a fixed delay: a delay
// that elapses concludes on a page still building, and the capture lies without a word.
// Past the deadline the answer is "undetermined", said as such, not a screenshot.
const DEADLINE_MS = 20_000;
const attendreChargement = () => new Promise((res, rej) => {
  const debut = Date.now();
  const t = setInterval(() => {
    if (events.includes("Page.loadEventFired")) { clearInterval(t); res(); }
    else if (Date.now() - debut > DEADLINE_MS) { clearInterval(t); rej(new Error(`undetermined: ${url} never fired its load event within ${DEADLINE_MS} ms; nothing captured`)); }
  }, 50);
});
await send("Runtime.enable");
// Settled = three consecutive readings, at least one second apart, that agree on the page's
// height and scroll position. A deferred script can move the layout two seconds after
// everything looks still; sampling until it stops is the only way to know it has.
const attendreStabilite = async (quoi) => {
  const lire = async () => (await send("Runtime.evaluate", {
    expression: "document.readyState+':'+document.documentElement.scrollHeight+':'+Math.round(scrollY)", returnByValue: true })).result.value;
  let precedent = await lire(), identiques = 1;
  for (let tour = 0; tour < 15 && identiques < 3; tour++) {
    await new Promise(r => setTimeout(r, 1000));
    const courant = await lire();
    identiques = courant === precedent ? identiques + 1 : 1;
    precedent = courant;
  }
  if (identiques < 3) throw new Error(`undetermined: ${url} has not settled ${quoi} after 15 s (last reading ${precedent}); nothing captured`);
};
// Any refusal below closes the tab and exits 2, so the caller reads "undetermined", not a
// stack trace, and no half-open tab survives in the headless profile.
try {
const chargement = attendreChargement();
await send("Page.navigate", { url });
await chargement;
await attendreStabilite("after load");
if (scrollJs && scrollJs !== "-") {
  await send("Runtime.evaluate", { expression: `document.documentElement.style.scrollBehavior='auto';${scrollJs}`, awaitPromise: false });
  await attendreStabilite("after the scroll");
}
const shot = await send("Page.captureScreenshot", { format: "png" });
writeFileSync(out, Buffer.from(shot.data, "base64"));
const info = await send("Runtime.evaluate", { expression: "innerWidth+'x'+innerHeight+' y='+Math.round(scrollY)", returnByValue: true }).catch(() => null);
console.log(out, info?.result?.value ?? "");
ws.close();
await fetch(`http://127.0.0.1:${port}/json/close/${target.id}`);
} catch (e) {
  console.error(e instanceof Error ? e.message : String(e));
  try { ws.close(); await fetch(`http://127.0.0.1:${port}/json/close/${target.id}`); }
  catch (e2) { console.error(`(the tab could not be closed either: ${e2 instanceof Error ? e2.message : String(e2)})`); }
  process.exit(2);
}
