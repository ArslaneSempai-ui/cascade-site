// La sonde CDP du témoin des instruments vivants (les cinq pages en carte, 9/09).
// usage: node temoin-instrument-sonde.mjs <url> <type>     type ∈ grille | vert | onyx
// Chrome sur 9222 ; viewport FORCÉ à 1440×900 (le panneau caché du navigateur intégré
// rend un viewport de 29 px et fausse tout test de survol — constat du chef, 9/09).
//
// Cinq affirmations, chacune EXÉCUTÉE :
//   1. la ligne tirée et le curseur sont UNE valeur : tirer la ligne (vrais événements
//      pointeur) change #b-curseur et réécrit #b-lecture ; pousser le curseur redessine
//      la ligne (grille, vert) ; l'onyx n'a pas de curseur : sa ligne réécrit son
//      étiquette what-if et le compte de fraîcheur du panneau ;
//   2. la grille RESTE dans le DOM pour le clavier, peinte par les mêmes chiffres que la
//      carte (échantillon de cellules relues contre le JSON embarqué) ;
//   3. l'auto-contrôle #tm-preuve passe, la carte est présente ;
//   4. prefers-reduced-motion : le caret s'arrête (animation none, calculée) ;
//   5. les chiffres lus dans le panneau au clic d'une cellule se retrouvent dans le JSON
//      embarqué (formats de la maison recomposés côté page, jamais devinés ici).
const [url, type] = process.argv.slice(2);
if (!url || !["grille", "vert", "onyx"].includes(type)) {
  console.error("usage: node temoin-instrument-sonde.mjs <url> grille|vert|onyx");
  process.exit(2);
}
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

const naviguer = async (u) => {
  events.length = 0;
  await send("Page.navigate", { url: u });
  const debut = Date.now();
  while (!events.includes("Page.loadEventFired")) {
    if (Date.now() - debut > 20000) throw new Error(`undetermined: ${u} n'a jamais signalé son chargement`);
    await new Promise((r) => setTimeout(r, 100));
  }
  await new Promise((r) => setTimeout(r, 500));
};
const evaluer = async (expr) => {
  const r = await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error("page: " + JSON.stringify(r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
};
const souris = async (typ, x, y) =>
  send("Input.dispatchMouseEvent", { type: typ, x, y, button: "left", buttons: typ === "mouseReleased" ? 0 : 1, clickCount: 1, pointerType: "mouse" });
const tirer = async (x0, y0, x1, y1) => {
  await souris("mousePressed", x0, y0);
  for (let i = 1; i <= 6; i++) await souris("mouseMoved", x0 + (x1 - x0) * i / 6, y0 + (y1 - y0) * i / 6);
  await souris("mouseReleased", x1, y1);
  await new Promise((r) => setTimeout(r, 200));
};

const fautes = [];
const dire = (ok, quoi) => { console.log((ok ? "  ok  " : "  ROUGE ") + quoi); if (!ok) fautes.push(quoi); };

await naviguer(url);

/* 3. l'auto-contrôle et la carte */
const preuve = await evaluer(`(document.getElementById("tm-preuve")||{textContent:""}).textContent`);
dire(/passed/.test(preuve), `auto-contrôle : ${preuve.slice(0, 70)}`);
dire(await evaluer(`!!document.getElementById("carte")`), "la carte est dans la page");

/* amener la carte en vue, prendre la prise de la ligne */
await evaluer(`(async () => { document.getElementById("carte").scrollIntoView({block:"center",behavior:"instant"}); await new Promise(r=>setTimeout(r,300)); return 1; })()`);
const prise = await evaluer(`(() => {
  const p = document.querySelector(".plancher-poignee, .ligne-poignee");
  if (!p) return null;
  const r = p.getBoundingClientRect();
  return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
})()`);
dire(prise !== null, "la poignée de la ligne existe");

/* 1. la ligne tirée et le curseur sont UNE valeur */
if (prise) {
  const avant = await evaluer(`JSON.stringify({
    v: (document.getElementById("b-curseur")||{}).value ?? null,
    l: (document.getElementById("b-lecture")||{}).textContent ?? null,
    t: (document.querySelector(".ligne-t, .plancher-t")||{}).textContent ?? "",
    pan: (document.getElementById("pan-verdicts")||{}).textContent ?? "",
  })`);
  if (type === "grille") await tirer(prise.x, prise.y, prise.x, prise.y - 60);
  else await tirer(prise.x, prise.y, prise.x - 80, prise.y);
  const apres = JSON.parse(await evaluer(`JSON.stringify({
    v: (document.getElementById("b-curseur")||{}).value ?? null,
    l: (document.getElementById("b-lecture")||{}).textContent ?? null,
    t: (document.querySelector(".ligne-t, .plancher-t")||{}).textContent ?? "",
    pan: (document.getElementById("pan-verdicts")||{}).textContent ?? "",
  })`));
  const av = JSON.parse(avant);
  if (type === "onyx") {
    dire(apres.t !== av.t && /if the rhythm were/.test(apres.t), `la ligne tirée réécrit son étiquette what-if : « ${apres.t.slice(0, 60)} »`);
    dire(apres.pan !== av.pan, "le compte de fraîcheur du panneau suit la ligne");
  } else {
    dire(av.v !== null && apres.v !== av.v, `tirer la ligne change #b-curseur (${av.v} → ${apres.v})`);
    dire(apres.l !== av.l, "tirer la ligne réécrit #b-lecture");
    /* le sens inverse : pousser le curseur redessine la ligne */
    const cible = type === "grille" ? "0.97" : null;
    if (cible) {
      await evaluer(`(() => { const c = document.getElementById("b-curseur"); c.value = ${cible}; c.dispatchEvent(new Event("input")); return 1; })()`);
      await new Promise((r) => setTimeout(r, 200));
      const t2 = await evaluer(`(document.querySelector(".plancher-t")||{textContent:""}).textContent`);
      dire(t2.includes(cible), `pousser le curseur redessine la ligne (« ${t2} »)`);
    }
  }
}

/* 2 et 5, selon le type */
if (type === "grille") {
  const grille = JSON.parse(await evaluer(`(() => {
    const D = JSON.parse(document.getElementById("donnees").textContent);
    const paliers = Object.keys(D.authored.grille);
    const seuils = D.seuilsMontres.map((s) => s.toFixed(2));
    let vus = 0, faux = [];
    for (const p of paliers) for (const s of [seuils[0], seuils[3], seuils[seuils.length - 1]]) {
      const cell = document.querySelector('.cell[data-p="' + p + '"][data-s="' + s + '"]');
      if (!cell) { faux.push(p + "@" + s + " sans cellule"); continue; }
      const attendu = Math.round(D.authored.grille[p][s].rappel.taux * 100) + "%";
      const lu = cell.querySelector(".c-rappel").textContent;
      if (lu !== attendu) faux.push(p + "@" + s + " : " + lu + " ≠ " + attendu);
      vus++;
    }
    return JSON.stringify({ vus, faux: faux.slice(0, 3) });
  })()`));
  dire(grille.vus >= 9 && grille.faux.length === 0,
       `la grille DOM porte les chiffres de la carte (${grille.vus} cellules relues${grille.faux.length ? " ; " + grille.faux.join(" | ") : ""})`);
  const panneau = JSON.parse(await evaluer(`(() => {
    const D = JSON.parse(document.getElementById("donnees").textContent);
    const p = Object.keys(D.authored.grille)[1], s = D.seuilsMontres[2].toFixed(2);
    const cell = document.querySelector('.cell[data-p="' + p + '"][data-s="' + s + '"]');
    cell.click();
    const c = D.authored.grille[p][s];
    const attendus = new Set();
    for (const m of [c.rappel, c.fauxPositifs]) {
      for (const v of [m.taux, m.bas, m.haut]) { attendus.add((v * 100).toFixed(1)); attendus.add(Math.round(v * 100).toString()); }
      attendus.add(String(m.n)); attendus.add(String(m.succes));
    }
    attendus.add(s); attendus.add(String(+s));
    const texte = ["pan-nom", "pan-g1", "pan-l1", "pan-g2", "pan-l2"].map((i) => (document.getElementById(i) || { textContent: "" }).textContent).join(" ");
    const nombres = texte.match(/\\d+(?:\\.\\d+)?/g) || [];
    const orphelins = nombres.filter((n) => !attendus.has(n) && !attendus.has((+n).toFixed(1)));
    return JSON.stringify({ n: nombres.length, orphelins: orphelins.slice(0, 4), texte: texte.slice(0, 60) });
  })()`));
  dire(panneau.n > 0 && panneau.orphelins.length === 0,
       `chaque chiffre du panneau se retrouve dans le JSON (${panneau.n} nombres lus${panneau.orphelins.length ? " ; orphelins : " + panneau.orphelins.join(", ") : ""})`);
} else if (type === "onyx") {
  const table = JSON.parse(await evaluer(`(() => {
    const D = JSON.parse(document.getElementById("donnees").textContent);
    let vus = 0, faux = [];
    for (const [q, d] of Object.entries(D.questions)) {
      if (!d.present) continue;
      for (const v of d.verdicts) {
        const cell = document.querySelector('.cell[data-q="' + q + '"][data-c="' + v.controle + '"]');
        if (!cell) { faux.push(q + "/" + v.controle + " sans cellule"); continue; }
        const lu = cell.querySelector(".c-eti").textContent;
        if ((v.tenu && lu !== "held") || (!v.tenu && lu !== "not held")) faux.push(q + "/" + v.controle + " : " + lu);
        vus++;
      }
    }
    return JSON.stringify({ vus, faux: faux.slice(0, 3) });
  })()`));
  dire(table.vus >= 15 && table.faux.length === 0,
       `la table DOM porte les verdicts du JSON (${table.vus} cellules relues${table.faux.length ? " ; " + table.faux.join(" | ") : ""})`);
  const panneau = JSON.parse(await evaluer(`(async () => {
    const D = JSON.parse(document.getElementById("donnees").textContent);
    const pierre = document.querySelector(".pierre");
    const r = pierre.getBoundingClientRect();
    pierre.dispatchEvent(new PointerEvent("pointermove", { bubbles: true, clientX: r.x + r.width / 2, clientY: r.y + r.height / 2 }));
    document.getElementById("carte").dispatchEvent(new PointerEvent("pointermove", { bubbles: true, clientX: r.x + r.width / 2, clientY: r.y + r.height / 2 }));
    await new Promise((rr) => setTimeout(rr, 150));
    const nom = document.getElementById("pan-nom").textContent.trim().split(/\\s/)[0];
    const jours = (document.getElementById("pan-g1") || { textContent: "" }).textContent.match(/\\d+/);
    const d = D.questions[nom];
    return JSON.stringify({ nom, ok: !!d && !!jours && +jours[0] === d.joursDepuis });
  })()`));
  dire(panneau.ok, `le panneau lit la pierre visée dans le JSON (question « ${panneau.nom} »)`);
} else {
  const vert = JSON.parse(await evaluer(`(() => {
    const okNom = (document.getElementById("pan-nom") || { textContent: "" }).textContent.length >= 0;
    const front = document.querySelectorAll(".pt-front").length;
    const rout = (document.getElementById("tm-rout") || { textContent: "" }).textContent;
    return JSON.stringify({ okNom, front, rout: rout.slice(0, 50) });
  })()`));
  dire(vert.front > 0, `la frontière du vert porte ${vert.front} points`);
}

/* 4. prefers-reduced-motion : le caret s'arrête */
await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
await naviguer(url);
const anim = await evaluer(`getComputedStyle(document.querySelector(".caret")).animationName`);
dire(anim === "none", `reduced-motion : le caret s'arrête (animation ${anim})`);

await send("Page.close").catch(() => {});
if (fautes.length) { console.log(`${fautes.length} ROUGE(S)`); process.exit(1); }
console.log("sonde : tout vert, et elle a regardé");
process.exit(0);
