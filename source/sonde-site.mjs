// Sonde de débord horizontal : pages × largeurs, via CDP natif (jamais une capture
// étroite : headless recadre sous ~500 px et fait mentir l'image ; le scrollWidth, lui,
// ne ment pas). Portée du scratchpad du chef (9/09) avec deux duretés :
//   - PAGES est OBLIGATOIRE (la liste vient de docs/, jamais recopiée d'un vieux script :
//     la liste codée en dur avait 17 pages quand le site en servait 29) ;
//   - un chargement jamais signalé est un DÉFAUT dit (« INDÉTERMINÉ »), pas une page
//     sondée en plein bâti qui rendrait un zéro sans valeur.
// usage: PAGES=a.html,b/index.html [PORT=8802] node sonde-site.mjs
// Chrome doit tourner avec --remote-debugging-port=9222.
if (!process.env.PAGES) {
  console.error("PAGES absent : le banc ne devine pas la liste des pages — la lire de docs/ "
    + "(find . -name '*.html'), une liste recopiée vieillit sans le dire.");
  process.exit(2);
}
const PAGES = process.env.PAGES.split(",");
const LARGEURS = [320, 375, 500, 641, 768, 900, 1024, 1081, 1150, 1280, 1440, 1680];
const PROBE = `JSON.stringify((()=>{const w=innerWidth,d=document.documentElement;
const o={ov:d.scrollWidth-w,bad:[]};
if(o.ov>1){for(const el of document.querySelectorAll('body *')){
  const r=el.getBoundingClientRect();
  if(r.width>2&&(r.right>w+1||r.left<-1)){
    let p=el.parentElement,c=false;
    while(p){const s=getComputedStyle(p);
      if(/(auto|scroll|hidden|clip)/.test(s.overflowX)){c=true;break}p=p.parentElement}
    if(!c){o.bad.push((el.className||el.tagName).toString().slice(0,30)
      +':'+Math.round(r.left)+'..'+Math.round(r.right));if(o.bad.length>4)break}}}}
return o})())`;

const target = await fetch("http://127.0.0.1:9222/json/new?about:blank", { method: "PUT" }).then((r) => r.json());
const ws = new WebSocket(target.webSocketDebuggerUrl);
let id = 0;
const pend = new Map();
const events = [];
const send = (method, params = {}) => new Promise((res, rej) => {
  const mid = ++id;
  pend.set(mid, { res, rej });
  ws.send(JSON.stringify({ id: mid, method, params }));
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

let defauts = 0;
for (const page of PAGES) {
  for (const larg of LARGEURS) {
    await send("Emulation.setDeviceMetricsOverride", { width: larg, height: 900, deviceScaleFactor: 1, mobile: false });
    events.length = 0;
    await send("Page.navigate", { url: `http://127.0.0.1:${process.env.PORT || 8802}/${page}` });
    const charge = await new Promise((r) => {
      const t = setInterval(() => { if (events.includes("Page.loadEventFired")) { clearInterval(t); r(true); } }, 30);
      setTimeout(() => { clearInterval(t); r(false); }, 6000);
    });
    if (!charge) {
      defauts++;
      console.log(`INDÉTERMINÉ ${page} @${larg} : chargement jamais signalé en 6 s — rien de sondé, dit`);
      continue;
    }
    await new Promise((r) => setTimeout(r, 250));
    const res = await send("Runtime.evaluate", { expression: PROBE, returnByValue: true });
    const o = JSON.parse(res.result.value);
    if (o.ov > 1) { defauts++; console.log(`DEBORD ${page} @${larg} : +${o.ov}px ${o.bad.join(" | ")}`); }
  }
  console.log(`ok ${page} (${LARGEURS.length} largeurs)`);
}
console.log(defauts ? `${defauts} DÉFAUTS` : `ZÉRO débord sur ${PAGES.length * LARGEURS.length} combos`);
ws.close();
await fetch(`http://127.0.0.1:9222/json/close/${target.id}`);
process.exit(defauts ? 1 : 0);
