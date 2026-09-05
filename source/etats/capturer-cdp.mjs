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
const loaded = new Promise(r => {
  const t = setInterval(() => { if (events.includes("Page.loadEventFired")) { clearInterval(t); r(); } }, 50);
  setTimeout(() => { clearInterval(t); r(); }, 8000);
});
await send("Page.navigate", { url });
await loaded;
await new Promise(r => setTimeout(r, 600));
if (scrollJs && scrollJs !== "-") {
  await send("Runtime.enable");
  await send("Runtime.evaluate", { expression: `document.documentElement.style.scrollBehavior='auto';${scrollJs}`, awaitPromise: false });
  await new Promise(r => setTimeout(r, +(process.env.WAIT || 500)));
}
const shot = await send("Page.captureScreenshot", { format: "png" });
writeFileSync(out, Buffer.from(shot.data, "base64"));
const info = await send("Runtime.evaluate", { expression: "innerWidth+'x'+innerHeight+' y='+Math.round(scrollY)", returnByValue: true }).catch(() => null);
console.log(out, info?.result?.value ?? "");
ws.close();
await fetch(`http://127.0.0.1:${port}/json/close/${target.id}`);
