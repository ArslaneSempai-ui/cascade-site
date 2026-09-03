#!/usr/bin/env python3
"""L'INSTRUMENT EN DIRECT : composer un routage, ou laisser le budget décider.

CE QUE CETTE PAGE EST
Une table palier x champ où chaque cellule est un bouton : cliquer compose un
routage, le panneau lit son coût et sa justesse en direct. Un curseur de budget
rejoue l'énumération des 16 807 routages, avec le départage exact de l'outil
(justesse maximale, à égalité le coût moindre). Deux préréglages : le routage
publié, le routage visé fichier.

D'OÙ VIENNENT LES CHIFFRES
De instrument-donnees.json, émis par extraire-instrument.mjs : les briques sont
calculées par le code de l'outil lui-même (pricePerThousandExtractions aux
latences gelées du relevé de référence), jamais recopiées. L'extracteur refuse
d'émettre si la recomposition du routage publié ne reproduit pas le landing ;
et la page refait ce témoin À L'OUVERTURE, sous les yeux du visiteur.

CE QUE LA PAGE NE FAIT PAS
Elle ne touche pas aux documents du visiteur : rien n'entre, rien ne sort
(connect-src 'none', aucune ressource tierce). Mesurer SES fichiers, c'est
l'outil, chez lui : le bouton du bas y mène.
"""
import json
import pathlib
import subprocess
import sys

BASE = pathlib.Path(__file__).parent

# ── les briques, calculées par l'outil à l'instant de la bâtisse ─────────────
r = subprocess.run(["node", str(BASE / "extraire-instrument.mjs")],
                   capture_output=True, text=True)
if r.returncode != 0:
    sys.exit(f"extraire-instrument a refusé :\n{r.stderr}")
print(" ", r.stdout.strip())
D = json.loads((BASE / "instrument-donnees.json").read_text())

FIELDS, TIERS = D["fields"], D["tiers"]
SCEAU = "1151f5a1cfaae0c0"
DEPOT_URL = "https://github.com/ArslaneSempai-ui/cascade-routing"


def table_html():
    tetes = "".join(
        f"<th scope='col'>{t}{'*' if t == 'human' else ''}</th>" for t in TIERS)
    lignes = ""
    for f in FIELDS:
        cells = ""
        for t in TIERS:
            v = D["acc"][t][f]
            s = f"{v:.1f}".rstrip("0").rstrip(".")
            cells += (f'<td><button class="cell" data-f="{f}" data-t="{t}" '
                      f'aria-pressed="false"><span class="c-acc">{s}<small>%</small></span>'
                      f'<span class="c-prix">${D["price"][t][f]:.2f}</span></button></td>')
        lignes += f"<tr><th scope='row'>{f}</th>{cells}</tr>"
    return f'''<div class="t-scroll"><table class="routage">
      <caption class="sr">Pick one tier per field; each cell shows measured accuracy and the price of a thousand extractions</caption>
      <thead><tr><th scope="col">field</th>{tetes}</tr></thead><tbody>{lignes}</tbody></table></div>'''


CSS = '''
  :root{--papier:#dbd7c5;--papier-haut:#e2ddcb;--papier-bas:#cdccb9;--encre:#1b1d18;
    --demi:#4a4739;--pale:#55523f;--filet:#9d9a83;
    --nuit-a:#1b3229;--nuit-b:#14251e;--nuit-c:#0e1a15;--sur-vert:#e4ecdf;--sur-vert-pale:#a9bdaf;
    --vert-titre:#23543f;--vert-vif:#57b184;--vert-clair:#a5f7cb;
    --texte:"Literata",Georgia,serif;--mono:"Roboto Mono",ui-monospace,Menlo,monospace;
    --sans:ui-sans-serif,-apple-system,"Helvetica Neue",sans-serif;
    --montee:cubic-bezier(.16,.84,.32,1)}
  *{box-sizing:border-box;margin:0}
  html{scroll-behavior:smooth;caret-color:var(--vert-vif);
    scrollbar-color:var(--vert-titre) var(--nuit-c)}
  @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
  body{background:var(--nuit-b);color:var(--sur-vert);font-family:var(--texte);line-height:1.55}
  ::selection{background:var(--vert-vif);color:var(--nuit-c)}
  a{text-underline-offset:4px;color:inherit}
  .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
  :focus-visible{outline:3px solid var(--vert-vif);outline-offset:3px;border-radius:2px}
  .colonne{max-width:1180px;margin:0 auto;padding:0 48px}

  .barre{position:absolute;inset:0 0 auto 0;z-index:40;display:flex;align-items:center;gap:28px;
    padding:14px 32px}
  .marque{font-weight:700;font-size:19px;letter-spacing:.01em;text-decoration:none;color:var(--sur-vert)}
  .barre nav{display:flex;gap:16px;margin-left:auto}
  .barre nav a{font-size:14.5px;text-decoration:none;color:var(--sur-vert-pale);padding:13px 6px}
  .barre nav a:hover{color:var(--sur-vert);text-decoration:underline;
    text-decoration-color:var(--vert-vif);text-decoration-thickness:1.5px}
  .sceau{font-family:var(--mono);font-size:11px;color:var(--sur-vert-pale);letter-spacing:.04em}

  /* ── l'en-tête de l'instrument ── */
  .tete{padding:150px 0 40px;
    background:radial-gradient(120% 100% at 50% -20%,var(--nuit-a),var(--nuit-b) 60%)}
  .h1{font-size:clamp(36px,4.6vw,62px);font-weight:600;letter-spacing:-.02em;line-height:1.05;
    text-wrap:balance}
  .lede{font-size:clamp(15px,1.25vw,18px);color:var(--sur-vert-pale);max-width:72ch;
    line-height:1.6;margin-top:18px;text-wrap:balance}
  .lede b{color:var(--sur-vert)}

  /* ── l'instrument : la table à gauche, le pupitre de lecture à droite ── */
  .instrument{padding:34px 0 40px}
  .poste{display:flex;gap:28px;align-items:flex-start}
  .table-zone{flex:1;min-width:0}
  .t-scroll{overflow-x:auto;border-radius:14px;box-shadow:0 30px 80px rgba(0,0,0,.5);
    border:1px solid color-mix(in srgb,var(--vert-vif) 26%,transparent)}
  .routage{width:100%;border-collapse:collapse;background:color-mix(in srgb,var(--nuit-a) 72%,var(--nuit-b));
    color:var(--sur-vert);font-family:var(--mono);font-size:13px;min-width:640px}
  .routage th{padding:12px 10px;text-align:center;font-size:11px;letter-spacing:.1em;
    text-transform:uppercase;color:var(--sur-vert-pale);
    border:1px solid color-mix(in srgb,var(--sur-vert-pale) 14%,transparent)}
  .routage tbody th{text-align:left;padding-left:14px}
  .routage td{padding:0;border:1px solid color-mix(in srgb,var(--sur-vert-pale) 14%,transparent)}
  .cell{display:flex;flex-direction:column;gap:2px;align-items:center;justify-content:center;
    width:100%;min-height:56px;padding:8px 10px;background:none;border:0;cursor:pointer;
    font-family:var(--mono);color:var(--sur-vert);
    transition:background .16s,box-shadow .16s}
  .cell:hover{background:color-mix(in srgb,var(--vert-vif) 12%,transparent);
    box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--vert-vif) 55%,transparent)}
  .cell[aria-pressed="true"]{background:color-mix(in srgb,var(--vert-vif) 18%,transparent);
    color:var(--vert-clair);box-shadow:inset 0 0 0 1.5px var(--vert-vif)}
  .c-acc{font-size:13px}
  .c-acc small{font-size:.7em;color:var(--sur-vert-pale)}
  .c-prix{font-size:10px;color:color-mix(in srgb,var(--sur-vert-pale) 80%,transparent);
    letter-spacing:.04em}
  .cell[aria-pressed="true"] .c-prix{color:var(--vert-clair)}

  /* le pupitre de lecture */
  .pupitre{width:280px;flex:none;position:sticky;top:24px;display:flex;flex-direction:column;gap:0;
    background:linear-gradient(180deg,color-mix(in srgb,var(--nuit-b) 96%,transparent),
      color-mix(in srgb,var(--nuit-a) 92%,transparent));
    border:1px solid color-mix(in srgb,var(--vert-vif) 42%,transparent);border-radius:12px;
    padding:16px 22px 18px;box-shadow:0 18px 50px rgba(14,26,21,.32)}
  .p-t{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
    color:var(--sur-vert-pale);border-bottom:1px solid color-mix(in srgb,var(--sur-vert-pale) 25%,transparent);
    padding-bottom:8px;margin-bottom:14px}
  .p-chiffre{font-weight:600;font-size:clamp(30px,3vw,44px);letter-spacing:-.01em;
    font-variant-numeric:lining-nums tabular-nums;color:var(--vert-clair);
    text-shadow:0 0 18px color-mix(in srgb,var(--vert-vif) 45%,transparent)}
  .p-chiffre small{font-size:.5em;font-weight:400;color:var(--sur-vert-pale);white-space:nowrap}
  .p-leg{font-size:12.5px;color:var(--sur-vert-pale);line-height:1.5;margin:2px 0 14px}
  .p-just{font-weight:600;font-size:clamp(24px,2.2vw,32px);color:var(--sur-vert);
    font-variant-numeric:lining-nums tabular-nums}
  .p-delta{font-family:var(--mono);font-size:11.5px;letter-spacing:.06em;margin-top:12px;
    color:var(--sur-vert-pale)}
  .p-delta b{color:var(--vert-clair);font-weight:500;white-space:nowrap}
  .p-regl{display:flex;gap:8px;margin-top:16px;flex-wrap:wrap}
  .regl{font-family:var(--texte);font-size:13px;font-weight:600;color:var(--sur-vert);
    background:none;border:1px solid color-mix(in srgb,var(--vert-vif) 40%,transparent);
    border-radius:8px;padding:8px 12px;cursor:pointer;
    transition:background .2s,color .2s,border-color .2s}
  .regl:hover{border-color:var(--vert-vif)}
  .regl.actif{background:var(--vert-vif);color:var(--nuit-c);border-color:var(--vert-vif)}

  /* ── le curseur de budget ── */
  .budget{padding:40px 0 30px}
  .b-carte{background:color-mix(in srgb,var(--nuit-a) 55%,transparent);
    border:1px solid color-mix(in srgb,var(--vert-vif) 26%,transparent);border-radius:14px;
    padding:26px 30px}
  .b-t{font-size:clamp(20px,2vw,27px);font-weight:600;letter-spacing:-.01em;margin-bottom:4px}
  .b-note{font-size:13.5px;color:var(--sur-vert-pale);margin-bottom:20px}
  .b-ligne{display:flex;gap:24px;align-items:center;flex-wrap:wrap}
  .b-curseur{flex:1;min-width:260px}
  input[type=range]{width:100%;accent-color:var(--vert-vif);height:32px}
  .b-grad{display:flex;justify-content:space-between;font-family:var(--mono);font-size:10.5px;
    color:var(--sur-vert-pale);letter-spacing:.04em;margin-top:2px}
  .b-lecture{font-family:var(--mono);font-size:12.5px;color:var(--sur-vert-pale);min-width:270px}
  .b-lecture b{color:var(--vert-clair);font-weight:500;font-size:15px}
  .b-lecture .b-rout{display:block;margin-top:6px;line-height:1.6}

  /* ── l'auto-preuve ── */
  .preuve{font-family:var(--mono);font-size:11px;letter-spacing:.05em;color:var(--sur-vert-pale);
    padding:8px 0 46px}
  .preuve .ok{color:var(--vert-vif)}
  .preuve .ko{color:#d96b4a}

  /* ── les réserves, sur papier ── */
  .reserves{background:var(--papier);color:var(--encre);padding:64px 0 70px}
  .reserves h2{font-size:clamp(22px,2.4vw,32px);font-weight:600;letter-spacing:-.015em;
    margin-bottom:14px}
  .reserves p{font-size:15px;color:var(--demi);line-height:1.65;max-width:76ch;margin-bottom:10px}
  .reserves b{color:var(--encre)}
  .ouvrir-ligne{display:flex;justify-content:flex-end;margin-top:26px}
  .ouvrir{display:inline-flex;align-items:baseline;gap:12px;background:transparent;
    color:var(--vert-titre);text-decoration:none;font-family:var(--texte);font-size:17px;font-weight:600;
    padding:14px 26px;border-radius:10px;border:1px solid color-mix(in srgb,var(--vert-titre) 55%,transparent);
    transition:background .2s,color .2s,border-color .2s}
  .ouvrir .fl{font-family:var(--sans);transition:transform .2s var(--montee)}
  .ouvrir:hover{background:var(--vert-titre);color:var(--sur-vert);border-color:var(--vert-titre)}
  .ouvrir:hover .fl{transform:translateX(4px)}

  .pied{background:var(--nuit-c);color:var(--sur-vert);padding:52px 0}
  .pied .colonne{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:baseline}
  .pied-p{font-size:clamp(17px,1.8vw,23px);font-weight:600}
  .pied-p em{font-style:italic;color:var(--vert-clair)}
  .pied .sceau{color:var(--sur-vert-pale)}

  @media (max-width:1080px){
    .colonne{padding:0 22px}
    .barre{padding:12px 18px;gap:14px}
    .barre nav{display:none}
    .poste{flex-direction:column}
    .pupitre{position:static;width:100%}
    .tete{padding-top:110px}
  }
  html:not(.js) .cell{cursor:default}
  html:not(.js) .pupitre,html:not(.js) .budget,html:not(.js) .preuve{display:none}
  @media (prefers-reduced-motion:reduce){
    *{transition-duration:.01ms!important;animation-duration:.01ms!important}}
'''

JS = '''
  const D = DONNEES;
  const F = D.fields, T = D.tiers;
  const cells = new Map();
  document.querySelectorAll(".cell").forEach((c) => cells.set(c.dataset.f + "/" + c.dataset.t, c));
  const $ = (s) => document.querySelector(s);
  const fmtC = (c) => { const v = c * 100;
    return v >= 995 ? "$" + Math.round(v).toLocaleString("en-US")
         : v >= 99.5 ? "$" + v.toFixed(0) : "$" + v.toFixed(1); };

  let routage = { ...D.publie.routage };
  function lire(r) {
    const cout = F.reduce((s, f) => s + D.price[r[f]][f], 0);
    const just = F.reduce((s, f) => s + D.acc[r[f]][f], 0) / F.length;
    return { cout, just };
  }
  function peindre() {
    for (const [cle, c] of cells) {
      const [f, t] = cle.split("/");
      c.setAttribute("aria-pressed", routage[f] === t ? "true" : "false");
    }
    const { cout, just } = lire(routage);
    $("#p-cout").innerHTML = fmtC(cout) + "<small> /100k docs</small>";
    $("#p-just").textContent = just.toFixed(1) + "%";
    const { cout: cp, just: jp } = lire(D.publie.routage);
    const dc = (cout - cp) * 100, dj = just - jp;
    $("#p-delta").innerHTML = "vs published: <b>" + (dc >= 0 ? "+" : "&#8722;") + "$"
      + Math.abs(dc).toFixed(dc && Math.abs(dc) < 99.5 ? 1 : 0) + "</b> &#183; <b>"
      + (dj >= 0 ? "+" : "&#8722;") + Math.abs(dj).toFixed(1) + "&nbsp;pt</b>";
    const memePub = F.every((f) => routage[f] === D.publie.routage[f]);
    const memeVise = F.every((f) => routage[f] === D.vise.routage[f]);
    $("#r-pub").classList.toggle("actif", memePub);
    $("#r-vise").classList.toggle("actif", memeVise);
  }
  cells.forEach((c) => c.addEventListener("click", () => {
    routage[c.dataset.f] = c.dataset.t; peindre();
  }));
  $("#r-pub").addEventListener("click", () => { routage = { ...D.publie.routage }; peindre(); });
  $("#r-vise").addEventListener("click", () => { routage = { ...D.vise.routage }; peindre(); });

  /* l'espace entier des routages, comme l'outil : justesse d'abord, le coût départage */
  const frontiere = (() => {
    const pts = [];
    const marche = (i, r, cout, just) => {
      if (i === F.length) { pts.push({ r: { ...r }, cout, just: just / F.length }); return; }
      for (const t of T) { r[F[i]] = t;
        marche(i + 1, r, cout + D.price[t][F[i]], just + D.acc[t][F[i]]); }
    };
    marche(0, {}, 0, 0);
    pts.sort((a, b) => a.cout - b.cout || b.just - a.just);
    const front = [];
    let meilleure = -1;
    for (const p of pts) if (p.just > meilleure) { front.push(p); meilleure = p.just; }
    return front;
  })();
  $("#b-compte").textContent = frontiere.length;
  const curseur = $("#b-curseur");
  function sousBudget() {
    const budget = Math.pow(10, parseFloat(curseur.value)) / 100;  /* $/100k -> /1000 docs */
    let best = null;
    for (const p of frontiere) { if (p.cout <= budget) best = p; else break; }
    if (!best) {
      $("#b-lecture").innerHTML = "under <b>" + fmtC(budget) + "</b>: no routing fits &#183; even rules-only costs more";
      return;
    }
    $("#b-lecture").innerHTML = "under <b>" + fmtC(budget) + "</b>: best routing reads <b>"
      + best.just.toFixed(1) + "%</b> for <b>" + fmtC(best.cout) + "</b>"
      + '<span class="b-rout">' + F.map((f) => f + " &#8594; " + best.r[f]).join(" &#183; ") + "</span>";
    routage = { ...best.r }; peindre();
  }
  curseur.addEventListener("input", sousBudget);

  /* l'auto-preuve : la page refait le témoin de l'extracteur, sous les yeux du visiteur */
  (() => {
    const { cout, just } = lire(D.publie.routage);
    const okC = Math.abs(cout - D.publie.cout) <= 1e-4;
    const okJ = Math.abs(just - D.publie.justesse) <= 0.05;
    const el = $("#preuve");
    if (okC && okJ) {
      el.innerHTML = 'self-check at load <span class="ok">passed</span>: these bricks recompose the published routing at '
        + fmtC(cout) + " /100k and " + just.toFixed(1) + "%, as sealed on " + D.provenance.landingMeasuredAt.slice(0, 10)
        + " (commit " + D.provenance.commit + ")";
    } else {
      el.innerHTML = 'self-check <span class="ko">FAILED</span>: this page no longer reproduces the sealed routing; do not trust its figures';
    }
  })();
  peindre();
'''

PAGE = f'''<!doctype html><html lang="en">
<meta charset="utf-8"><title>Cascade, the live instrument</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta property="og:type" content="website">
<meta property="og:title" content="Cascade: the live instrument">
<meta property="og:description" content="Compose a routing cell by cell, or let the budget decide: the same bricks the tool bills, frozen and self-checked in your browser.">
<meta property="og:url" content="https://cascade-routing.com/instrument.html">
<meta property="og:image" content="https://cascade-routing.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="description" content="Compose a routing cell by cell, or let the budget decide: the same bricks the tool bills, frozen and self-checked in your browser.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M0 0h16L0 16z' fill='%2314251e'/%3E%3Cpath d='M16 0v16H0z' fill='%2323543f'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<link rel="stylesheet" href="fontes/roboto-mono.css">
<script>document.documentElement.classList.add("js")</script>
<style>{CSS}</style>
<header class="barre">
  <a class="marque" href="HERO.html">CASCADE</a>
  <nav aria-label="Site">
    <a href="ANNEXE-METHODE.html">Method</a>
    <a href="ANNEXE-SECURITE.html">Security</a>
    <a href="ANNEXE-QUESTIONS.html">Questions</a>
    <a href="CONTACT.html">Contact</a>
  </nav>
  <span class="sceau">seal {SCEAU} &#183; measured, then frozen</span>
</header>

<main>
<section class="tete"><div class="colonne">
  <h1 class="h1">Take the instrument. It answers live.</h1>
  <p class="lede">One tier per field: click any cell and read what your routing would cost, and how much
    it would get right. Or slide the budget and let the enumeration decide, the way the tool does:
    <b>highest accuracy first, cheaper on a tie</b>. Every brick below is the tool's own arithmetic
    at the frozen latencies, and the page re-proves it on load.</p>
</div></section>

<section class="instrument"><div class="colonne">
  <div class="poste">
    <div class="table-zone">{table_html()}
      <p class="preuve" id="preuve">self-check requires JavaScript; the figures above are still the sealed readings.</p>
    </div>
    <aside class="pupitre" aria-label="Your routing, read live">
      <p class="p-t">your routing</p>
      <span class="p-chiffre" id="p-cout">$191<small> /100k docs</small></span>
      <p class="p-leg">what it costs to run, on the assumed prices</p>
      <span class="p-just" id="p-just">94.4%</span>
      <p class="p-leg">per-field mean accuracy; fields are measured on separate samples, so this mean carries no interval</p>
      <p class="p-delta" id="p-delta">vs published: +$0 &#183; +0.0 pt</p>
      <div class="p-regl">
        <button class="regl actif" id="r-pub">published &#183; $191</button>
        <button class="regl" id="r-vise">file-aimed &#183; $54</button>
      </div>
    </aside>
  </div>
</div></section>

<section class="budget"><div class="colonne">
  <div class="b-carte">
    <p class="b-t">Or let the budget decide.</p>
    <p class="b-note">All 16,807 assignments of seven readers over five fields, enumerated in your
      browser; <span id="b-compte">&#8230;</span> of them sit on the frontier where no cheaper routing
      reads better.</p>
    <div class="b-ligne">
      <div class="b-curseur">
        <label class="sr" for="b-curseur">Budget, dollars per hundred thousand documents, logarithmic</label>
        <input type="range" id="b-curseur" min="0" max="5" step="0.01" value="2.3">
        <div class="b-grad" aria-hidden="true"><span>$1</span><span>$10</span><span>$100</span><span>$1k</span><span>$10k</span><span>$100k</span></div>
      </div>
      <p class="b-lecture" id="b-lecture">slide to read the best routing under your budget</p>
    </div>
  </div>
</div></section>
</main>

<section class="reserves"><div class="colonne">
  <h2>What this instrument rests on, and what it refuses.</h2>
  <p><b>The prices are assumed, and say so:</b> the small and large tiers are billed at assumed
    per-call rates, the generative tiers at their frozen measured latency times an assumed machine
    cost, the human tier at an assumed pace and salary. Change the assumptions and the dollars move;
    the accuracies do not.</p>
  <p><b>The human column is an assumption, never a measurement:</b> {D["humanAccuracy"]:.0f}% on every
    field, declared in the tool's own source. It is the only displayed figure that was not measured.</p>
  <p><b>Your documents never touch this page:</b> nothing is uploaded, nothing is fetched, and the
    page's security policy refuses every network call. These are our sealed readings; your records may
    disagree, and there is one honest way to find out.</p>
  <div class="ouvrir-ligne"><a class="ouvrir" href="{DEPOT_URL}">Run it on your records <span class="fl" aria-hidden="true">&#8594;</span></a></div>
</div></section>

<footer class="pied"><div class="colonne">
  <p class="pied-p">On your records, on your machine. <em>Nothing leaves the network.</em></p>
  <span class="sceau">seal {SCEAU} &#183; measured, then frozen</span>
</div></footer>

<script>
const DONNEES = {json.dumps({k: D[k] for k in ("fields", "tiers", "price", "acc", "publie", "vise", "provenance")})};
{JS}</script>
'''

assert "—" not in PAGE, "un cadratin s'est glissé dans la page"
(BASE / "INSTRUMENT.html").write_text(PAGE, encoding="utf-8")
print(f"INSTRUMENT.html {len(PAGE) / 1e3:.0f} ko")
