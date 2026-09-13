// LE TÉMOIN DU PLI : on ATTERRIT sur le rideau (#tools) ; ses cinq boutons « Open » doivent être dans
// l'écran à 1440x900 (le portable le plus courant) et à 1440x700. Le 13/09 (nuit), des questions
// plus longues ont poussé les boutons à 1005 px sur 900 sans qu'aucune garde ne le dise : le banc
// mesure le débord horizontal et le hors-section, pas le pli.
// usage: node temoin-rideau.mjs <url-avec-#tools>   (Chrome sur 9222) ; code 1 si un bouton passe sous le pli.
const [url] = process.argv.slice(2);
const mesure = async (w, h) => {
  const t = await fetch("http://127.0.0.1:9222/json/new?about:blank", {method: "PUT"}).then(r => r.json());
  const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const pend = new Map(); let charge = false;
  const send = (m, p = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, {res, rej}); ws.send(JSON.stringify({id: i, method: m, params: p})); });
  ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); } else if (d.method === "Page.loadEventFired") charge = true; };
  await new Promise(r => ws.onopen = r);
  await send("Page.enable"); await send("Runtime.enable"); await send("Network.enable"); await send("Network.setCacheDisabled", {cacheDisabled: true});
  await send("Emulation.setDeviceMetricsOverride", {width: w, height: h, deviceScaleFactor: 1, mobile: false});
  await send("Page.navigate", {url});
  for (let i = 0; i < 200 && !charge; i++) await new Promise(r => setTimeout(r, 100));
  await new Promise(r => setTimeout(r, 1500));
  const r = await send("Runtime.evaluate", {returnByValue: true, expression: `(()=>{const pans=[...document.querySelectorAll('.pan')];if(!pans.length)return null;return pans.map(p=>{const o=p.querySelector('.p-ouvrir');return {bas:Math.round(o.getBoundingClientRect().bottom),ih:innerHeight}})})()`});
  ws.close(); await fetch(`http://127.0.0.1:9222/json/close/${t.id}`);
  return r.result.value;
};
let fautes = 0;
// TEMOIN_HAUTEURS=500 : la preuve que le témoin sait refuser (aucun rideau ne tient dans 500 px)
const hauteurs = (process.env.TEMOIN_HAUTEURS || "900,700").split(",").map(Number);
for (const [w, h] of hauteurs.map(h => [1440, h])) {
  const pans = await mesure(w, h);
  if (!pans) { console.log(`INDÉTERMINÉ : aucun pan sur ${url}`); process.exit(2); }
  const pire = Math.max(...pans.map(p => p.bas));
  const ok = pire <= h;
  if (!ok) fautes++;
  console.log(`  rideau ${w}x${h} : ${pans.length} boutons, le plus bas à ${pire} px pour ${h} d'écran ${ok ? "✓" : "✗ SOUS LE PLI"}`);
}
process.exit(fautes ? 1 : 0);
