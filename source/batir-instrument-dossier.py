#!/usr/bin/env python3
"""L'INSTRUMENT ONYX EN DIRECT, sur la forme terminale de la maison.

L'onyx n'a ni grille palier x seuil ni curseur de rappel : son relevé public EST
le Dossier de la suite. Trois commandes structurent la page : `cascade dossier
--live` (les questions de la chaîne contre les cinq contrôles du contrat, cliquer
une cellule lit le verdict en toutes lettres), `cascade dossier --next` (par
question : l'état atteint, et ce que le contrôle suivant attend encore, dans les
mots du relevé), `verify --sealed` (à l'ouverture, la page refait l'état de chaque
question depuis ses propres verdicts par la règle sans-trou du contrat, recompte
la couverture, et refuse de se croire si elle ne retombe pas sur le relevé).

D'OÙ VIENNENT LES LIGNES
De instrument-dossier-donnees.json, émis par extraire-instrument-dossier.mjs : le
relevé public scellé de cascade-dossier, vérifié (scellé, contrôles du contrat)
puis recomposé question par question avant d'avoir le droit d'exister. Les relevés
lus sont les relevés PUBLICS de la suite ; aucune donnée client n'existe ici.

CE QUE LA PAGE NE FAIT PAS
Rien n'entre, rien ne sort (connect-src 'none', aucune ressource tierce). Assembler
le dossier des rapports du lecteur, c'est l'outil, chez lui : le terminal du bas
donne les trois vraies commandes.
"""
import json
import pathlib
import subprocess
import sys

BASE = pathlib.Path(__file__).parent

sys.path.insert(0, str(BASE))
from instrument_carte import CSS_NOIR, CSS_ONYX, CARTE_ONYX_HTML, PANNEAU_ONYX_HTML, JS_ONYX  # noqa: E402

r = subprocess.run(["node", str(BASE / "extraire-instrument-dossier.mjs")],
                   capture_output=True, text=True)
if r.returncode != 0:
    sys.exit(f"extraire-instrument-dossier a refuse :\n{r.stderr}")
print(" ", r.stdout.strip())
D = json.loads((BASE / "instrument-dossier-donnees.json").read_text())


def _sans_cadratin(x):
    """Les details du releve portent des cadratins (« — nothing to verify ») ; la
    typographie de la maison les refuse, et le blob JSON les ferait passer sous la
    garde de l'assembleur en \\u2014 : remplaces A LA SOURCE, avant l'embarquement."""
    if isinstance(x, str):
        return x.replace("—", "·")
    if isinstance(x, dict):
        return {k: _sans_cadratin(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_sans_cadratin(v) for v in x]
    return x


D = _sans_cadratin(D)

ORDRE = D["controles"]["presents"]
QUESTIONS = list(D["questions"])
DEPOT_URL = "https://github.com/ArslaneSempai-ui/cascade-dossier"


def table_html():
    """Les questions de la chaîne contre les contrôles du contrat. Les cellules ne
    portent AUCUN verdict en dur : le JS les peint depuis D, et marque l'état
    atteint ; une question sans relevé public est une ligne dite, pas devinée."""
    tetes = "".join(f"<th scope='col'>{c}</th>" for c in ORDRE)
    lignes = ""
    for q in QUESTIONS:
        if not D["questions"][q]["present"]:
            lignes += (f"<tr class='absent'><th scope='row'>{q}</th>"
                       f"<td colspan='{len(ORDRE)}'>no public record yet: nothing judged, and said rather than guessed</td></tr>")
            continue
        cells = "".join(
            f'<td><button class="cell" data-q="{q}" data-c="{c}" aria-pressed="false">'
            f'<span class="c-verdict"></span><span class="c-eti"></span></button></td>'
            for c in ORDRE)
        lignes += f"<tr><th scope='row'>{q}</th>{cells}</tr>"
    return f'''<div class="t-scroll"><table class="grille">
      <caption class="sr">Pick a cell: each question of the chain against each control of the contract, held or not, with the verdict in the record's own words</caption>
      <thead><tr><th scope="col">question \\ control</th>{tetes}</tr></thead>
      <tbody>{lignes}</tbody></table></div>'''


CSS = '''
  :root{--nuit-a:#121216;--nuit-b:#0c0c10;--nuit-c:#070709;
    --sur:#efede6;--sur-pale:#b8b6ad;
    --papier:#dbd7c5;--papier-haut:#e2ddcb;--encre:#1b1d18;--demi:#4a4739;--pale:#55523f;
    --filet-clair:#bab7a0;
    --accent-titre:#1c1c22;--accent-vif:#8a8a96;--accent-clair:#e8e6df;
    --texte:"Literata",Georgia,serif;--mono:"Roboto Mono",ui-monospace,Menlo,monospace;
    --montee:cubic-bezier(.16,.84,.32,1)}
  *{box-sizing:border-box;margin:0}
  html{scroll-behavior:smooth;caret-color:var(--accent-vif);
    scrollbar-color:var(--accent-vif) var(--nuit-c)}
  @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
  body{background:var(--nuit-b);color:var(--sur);font-family:var(--texte);line-height:1.55}
  img{max-width:100%;display:block}
  ::selection{background:var(--accent-vif);color:var(--nuit-c)}
  a{text-underline-offset:4px;color:inherit}
  .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
  :focus-visible{outline:3px solid var(--accent-vif);outline-offset:3px;border-radius:2px}
  .colonne{max-width:1240px;margin:0 auto;padding:0 48px}

  .barre{position:absolute;inset:0 0 auto 0;z-index:40;display:flex;align-items:center;gap:28px;
    padding:14px 32px}
  .marque{font-weight:700;font-size:19px;letter-spacing:.01em;text-decoration:none;color:var(--sur)}
  .marque small{font-weight:500;color:var(--accent-clair)}
  .barre nav{display:flex;gap:16px;margin-left:auto}
  .barre nav a{font-size:14.5px;text-decoration:none;color:var(--sur-pale);padding:13px 6px}
  .barre nav a:hover{color:var(--sur);text-decoration:underline;
    text-decoration-color:var(--accent-vif);text-decoration-thickness:1.5px}
  .barre nav a[aria-current]{color:var(--sur)}
  .sceau{font-family:var(--mono);font-size:11px;color:var(--sur-pale);letter-spacing:.04em}

  .tete{padding:192px 0 30px;
    background:radial-gradient(120% 100% at 50% -20%,#1a1a21,var(--nuit-b) 70%)}
  .h1{font-size:clamp(36px,4.6vw,62px);font-weight:600;letter-spacing:-.02em;line-height:1.05;
    text-wrap:balance;max-width:18ch}
  .lede{font-size:clamp(15px,1.25vw,18px);color:var(--sur-pale);max-width:52ch;
    line-height:1.6;margin-top:16px;text-wrap:balance}
  .lede b{color:var(--sur)}

  /* le poste : le robot onyx penche derriere le bord du terminal, coupe net */
  .poste{position:relative;padding:44px 0 64px}
  .dessus{position:relative;width:min(100%,1020px);margin:0 auto}
  .rb{position:absolute;right:30px;top:-312px;width:340px;height:auto;z-index:2;pointer-events:none;
    filter:drop-shadow(0 26px 44px rgba(0,0,0,.55))}
  .terminal{position:relative;z-index:3;
    background:linear-gradient(180deg,color-mix(in srgb,var(--nuit-b) 55%,#000),color-mix(in srgb,var(--nuit-c) 92%,#000) 120px);
    border:1px solid color-mix(in srgb,var(--accent-vif) 30%,transparent);border-radius:14px;
    box-shadow:0 60px 140px rgba(0,0,0,.7),0 0 0 1px rgba(0,0,0,.4),
      inset 0 1px 0 color-mix(in srgb,var(--accent-clair) 22%,transparent);overflow:hidden}
  .terminal::after{content:"";position:absolute;inset:0;pointer-events:none;border-radius:14px;
    background:repeating-linear-gradient(to bottom,rgba(232,230,223,.016) 0 1px,transparent 1px 3px)}
  .caret{display:inline-block;width:7px;height:14px;vertical-align:-2px;background:var(--accent-clair);
    margin-left:6px;animation:caret 1.1s steps(1) infinite}
  @keyframes caret{50%{opacity:0}}
  .t-page-halo{position:absolute;left:50%;top:52%;width:min(1100px,92vw);height:min(700px,70vw);
    transform:translate(-50%,-50%);pointer-events:none;
    background:radial-gradient(50% 50% at 50% 50%,color-mix(in srgb,var(--accent-vif) 12%,transparent),transparent 70%)}
  .tm-barre{display:flex;align-items:center;gap:8px;padding:11px 16px;
    background:linear-gradient(180deg,color-mix(in srgb,var(--nuit-a) 55%,#000),color-mix(in srgb,var(--nuit-b) 75%,#000));
    border-bottom:1px solid color-mix(in srgb,var(--sur-pale) 14%,transparent)}
  .tm-barre i{width:10px;height:10px;border-radius:50%;
    background:color-mix(in srgb,var(--sur-pale) 30%,transparent)}
  .tm-barre i:first-child{background:var(--accent-vif);
    box-shadow:0 0 8px color-mix(in srgb,var(--accent-vif) 70%,transparent)}
  .tm-barre span{margin-left:6px;font-family:var(--mono);font-size:12px;color:var(--sur-pale)}
  .tm-corps{padding:22px 26px 26px;font-family:var(--mono);font-size:13.5px}
  .tm-l{color:var(--sur-pale);margin:0 0 10px}
  .tm-l .ps{color:var(--accent-vif)}
  .tm-sortie{color:var(--sur);margin:2px 0 14px;line-height:1.7}
  .tm-sortie b{color:var(--accent-clair);font-weight:500}
  .tm-preuve{font-size:12.5px;color:var(--sur-pale);line-height:1.7}
  .tm-preuve .ok{color:var(--accent-clair)}
  .tm-preuve .ko{color:#ff7b6e;font-weight:700}

  .t-scroll{overflow-x:auto;margin:6px 0 16px}
  table.grille{border-collapse:collapse;font-family:var(--mono);font-size:12.5px;min-width:760px}
  .grille caption{text-align:left}
  .grille th{color:var(--sur-pale);font-weight:500;padding:7px 9px;text-align:left;white-space:nowrap}
  .grille td{padding:0;border:1px solid color-mix(in srgb,var(--sur-pale) 12%,transparent)}
  .grille tr.absent td{padding:10px 12px;color:var(--sur-pale);font-size:12px;font-style:italic}
  .cell{display:flex;flex-direction:column;gap:2px;width:100%;padding:8px 10px;background:transparent;
    border:0;cursor:pointer;font:inherit;color:var(--sur);text-align:left}
  .cell:hover{background:color-mix(in srgb,var(--accent-vif) 12%,transparent);
    box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent-vif) 55%,transparent)}
  .cell[aria-pressed="true"]{background:color-mix(in srgb,var(--accent-vif) 18%,transparent);
    color:var(--accent-clair);box-shadow:inset 0 0 0 1.5px var(--accent-vif)}
  .cell.etat{box-shadow:inset 0 0 0 1.5px color-mix(in srgb,var(--accent-clair) 65%,transparent)}
  .c-verdict{font-size:13px}
  .c-eti{font-size:11px;color:var(--sur-pale)}
  .cell[aria-pressed="true"] .c-eti{color:var(--accent-clair)}

  .suivant{margin:4px 0 8px;line-height:1.8}
  .suivant b{color:var(--accent-clair);font-weight:500}

  /* le bas de page : le PARCHEMIN de la maison, comme les autres instruments */
  .basse{background:var(--papier);color:var(--encre);padding:64px 0 70px}
  .basse h2{font-size:clamp(22px,2.4vw,32px);font-weight:600;letter-spacing:-.015em;
    margin:0 0 14px;color:var(--encre)}
  .basse h2+ul,.basse h2+p{margin-top:0}
  .basse ul+h2,.basse p+h2,.basse div+h2{margin-top:40px}
  .basse p{font-size:15px;color:var(--demi);max-width:76ch;line-height:1.65;margin:8px 0}
  .basse p b{color:var(--encre)}
  .basse ul{color:var(--demi);max-width:76ch;margin:8px 0;padding:0;list-style:none;font-size:15px;line-height:1.65}
  .basse li{margin:0 0 .5rem;padding-left:1.1rem;position:relative}
  .basse li::before{content:"";position:absolute;left:0;top:.72em;width:6px;height:1.5px;background:var(--accent-titre)}
  .basse li b{color:var(--encre)}
  .clone-t{font:500 10px/1.4 var(--mono);letter-spacing:.14em;text-transform:uppercase;
    color:var(--accent-titre);display:block;margin:22px 0 8px}
  .clone{max-width:62ch;background:linear-gradient(163deg,var(--nuit-a),var(--nuit-b));
    border:1px solid color-mix(in srgb,var(--accent-vif) 30%,transparent);border-radius:8px;
    padding:14px 18px 16px;font-family:var(--mono);font-size:12.5px;line-height:1.85;overflow-x:auto;
    color:var(--sur);box-shadow:0 6px 18px rgba(18,18,22,.22)}
  .clone .ps{color:var(--accent-vif);font-weight:600}
  .clone .note{color:var(--sur-pale);font-size:12px}
  .pied{background:var(--nuit-c);color:var(--sur);padding:52px 0}
  .pied .colonne{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:baseline}
  .pied-p{font-size:clamp(17px,1.8vw,23px);font-weight:600;margin:0}
  .pied-p em{font-style:italic;color:var(--accent-clair)}
  .pied .sceau{color:var(--sur-pale)}

  @media (max-width:1080px){
    .barre{padding:12px 18px;gap:14px}
    .barre nav{display:none}
  }
  @media (max-width:900px){
    .colonne{padding:0 20px}
    .rb{width:220px;top:-200px;right:8px}
    .tete{padding:150px 0 18px}
  }
  @media (max-width:700px){
    .rb{display:none}
  }
'''

JS = '''
  const $ = (s) => document.querySelector(s);
  const D = JSON.parse(document.getElementById("donnees").textContent);
  const ORDRE = D.controles.presents;

  const verdictDe = (q, c) => (D.questions[q].verdicts || []).find((v) => v.controle === c) || null;

  const cells = [...document.querySelectorAll(".cell")];
  for (const cel of cells) {
    const q = cel.dataset.q, c = cel.dataset.c;
    const v = verdictDe(q, c);
    if (v === null) {
      cel.querySelector(".c-verdict").textContent = "\\u00b7";
      cel.querySelector(".c-eti").textContent = "not judged";
    } else if (v.tenu) {
      cel.querySelector(".c-verdict").textContent = "\\u2713";
      cel.querySelector(".c-eti").textContent = "held";
    } else {
      cel.querySelector(".c-verdict").textContent = "\\u00d7";
      cel.querySelector(".c-eti").textContent = "not held";
    }
    if (D.questions[q].etat === c) cel.classList.add("etat");
  }
  function lire(cel) {
    cells.forEach((x) => x.setAttribute("aria-pressed", String(x === cel)));
    const q = cel.dataset.q, c = cel.dataset.c;
    const v = verdictDe(q, c);
    $("#g-lecture").innerHTML = v === null
      ? "<b>" + q + "</b> \\u00b7 <b>" + c + "</b>: not judged \\u00b7 the record carries no verdict for this cell, and says so"
      : "<b>" + q + "</b> \\u00b7 <b>" + c + "</b> (" + (v.tenu ? "held" : "NOT held") + "): " + v.detail;
    viseQ = q; dessinerO(); peindrePanneauO();
  }
  cells.forEach((cel) => cel.addEventListener("click", () => lire(cel)));

  /* cascade dossier --next : par question, l'etat atteint et ce que le suivant attend */
  (() => {
    const lignes = [];
    for (const [q, d] of Object.entries(D.questions)) {
      if (!d.present) { lignes.push("<b>" + q + "</b>: no public record yet \\u00b7 nothing judged"); continue; }
      const tenu = Object.fromEntries((d.verdicts || []).map((v) => [v.controle, v.tenu]));
      const suivant = ORDRE.find((c) => !(c in tenu) || !tenu[c]);
      const jours = typeof d.joursDepuis === "number" ? " \\u00b7 measured " + d.joursDepuis + " day(s) ago" : "";
      if (suivant === undefined) {
        lignes.push("<b>" + q + "</b>: every control held" + jours);
      } else {
        const v = verdictDe(q, suivant);
        lignes.push("<b>" + q + "</b>: state reached <b>" + d.etat + "</b>" + jours
          + " \\u00b7 next, <b>" + suivant + "</b>: " + (v ? v.detail : "not judged by the record"));
      }
    }
    $("#g-suivant").innerHTML = lignes.join("<br>");
  })();

  /* verify --sealed : la page refait chaque etat par la regle sans-trou et recompte la couverture */
  (() => {
    const el = $("#tm-preuve");
    let refaits = 0, desaccords = [];
    for (const [q, d] of Object.entries(D.questions)) {
      if (!d.present) continue;
      const tenu = Object.fromEntries((d.verdicts || []).map((v) => [v.controle, v.tenu]));
      let etat = "none";
      for (const c of ORDRE) { if (!(c in tenu) || !tenu[c]) break; etat = c; }
      if (etat !== d.etat) desaccords.push(q + ": " + d.etat + " shipped, " + etat + " recomposed");
      refaits++;
    }
    const n = Object.values(D.questions).filter((d) => d.present).length;
    if (n !== D.couverture.n || Object.keys(D.questions).length !== D.couverture.sur) {
      desaccords.push("coverage: " + D.couverture.n + "/" + D.couverture.sur + " shipped, "
        + n + "/" + Object.keys(D.questions).length + " recounted");
    }
    if (desaccords.length === 0 && refaits > 0) {
      el.innerHTML = 'self-check <span class="ok">passed</span>: this page recomposed the state of all '
        + refaits + " judged questions from their own verdicts by the contract\\u2019s no-gap rule, and recounted the coverage \\u00b7 record "
        + D.provenance.empreinte + ", " + D.provenance.date + " (commit " + D.provenance.commit + ")";
    } else {
      el.innerHTML = 'self-check <span class="ko">FAILED</span>: this page no longer reproduces the sealed dossier ('
        + (desaccords.join(" \\u00b7 ") || "nothing was recomposed") + "); do not trust its lines";
    }
  })();
''' + JS_ONYX + '''
'''

CV, RG = D["couverture"], D["reglages"]

PAGE = f'''<!doctype html><html lang="en">
<meta charset="utf-8"><title>Cascade Dossier &#183; live instrument</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta property="og:type" content="website">
<meta property="og:title" content="Cascade Dossier: the live instrument">
<meta property="og:description" content="The four questions of the chain against the contract's five controls, states and verdicts live from the sealed public dossier, and what the next control still needs.">
<meta property="og:url" content="https://cascade-routing.com/dossier/instrument.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="description" content="The four questions of the chain against the contract's five controls, states and verdicts live from the sealed public dossier, and what the next control still needs.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M0 0h16L0 16z' fill='%23070709'/%3E%3Cpath d='M16 0v16H0z' fill='%231c1c22'/%3E%3C/svg%3E">
<link rel="stylesheet" href="../fontes/literata.css">
<link rel="stylesheet" href="../fontes/roboto-mono.css">
<script>document.documentElement.classList.add("js")</script>
<style>{CSS}{CSS_NOIR}{CSS_ONYX}</style>
<header class="barre">
  <a class="marque" href="../ACCUEIL.html">CASCADE</a>
  <nav aria-label="Site">
    <a href="INSTRUMENT-DOSSIER.html" aria-current="page">Instrument</a>
    <a href="../ENGAGEMENT.html">Pricing</a>
    <a href="ANNEXE-DOSSIER-METHODE.html">Method</a>
    <a href="ANNEXE-DOSSIER-SECURITE.html">Security</a>
    <a href="../CONTACT.html">Contact</a>
  </nav>
  <span class="sceau">seal {D["provenance"]["empreinte"]} &#183; measured, then frozen</span>
</header>

<section class="tete">
  <div class="colonne">
    <h1 class="h1">The whole chain, one table. Live.</h1>
    <p class="lede">Every line on this page comes from the <b>sealed public dossier</b> of
      cascade-dossier: the suite&#8217;s own public records, read and judged by its five controls.
      No client data exists here, nothing enters and nothing leaves,
      and the page checks its own arithmetic before your eyes.</p>
  </div>
</section>

<section class="poste">
  <div class="colonne">
    <div class="dessus">
      <div class="t-page-halo" aria-hidden="true"></div>
      <div class="poste-grille">
      <div class="fen-robot">
      <div class="terminal">
        <div class="tm-barre"><i></i><i></i><i></i><span>cascade dossier &#183; the public dossier, live</span></div>
        <div class="tm-corps">
          <p class="tm-l"><span class="ps">$</span> cascade dossier --live<span class="caret" aria-hidden="true"></span></p>
          <p class="tm-sortie">coverage <b>{CV["n"]} / {CV["sur"]}</b> questions with a sealed public record &#183;
            declared rhythm <b>{RG["rythmeJours"]} days</b> &#183; as of <b>{RG["auJour"]}</b></p>
          {CARTE_ONYX_HTML}
          {table_html()}
          <p class="tm-sortie" id="g-lecture">pick a cell: the verdict in the record&#8217;s own words &#183; the outlined cell of a row is the state reached with no gap</p>

          <p class="tm-l"><span class="ps">$</span> cascade dossier --next</p>
          <p class="tm-sortie suivant" id="g-suivant"></p>

          <p class="tm-l" style="margin-top:14px"><span class="ps">$</span> cascade verify --sealed</p>
          <p class="tm-preuve" id="tm-preuve">checking&#8230;</p>
        </div>
      </div>
      </div>
      <div class="pan-col">
      <img class="rb" src="../rendus/robot-onyx-regarde.webp" alt="">
      {PANNEAU_ONYX_HTML}
      </div>
      </div>
    </div>
  </div>
</section>

<section class="basse">
  <div class="colonne basse-grille">
    <div class="plis">
      <details class="pli"><summary>What this rests on</summary>
    <ul>
      <li><b>The sealed public dossier.</b> releve-public.json in the repository, fingerprint
        <b>{D["provenance"]["empreinte"]}</b>, measured at commit <b>{D["provenance"]["commit"]}</b>
        on {D["provenance"]["date"]}. The extractor that feeds this page verifies the seal,
        then recomposes every question&#8217;s state from its own verdicts with the contract&#8217;s
        no-gap rule, and refuses to emit if a single line disagrees.</li>
      <li><b>The suite&#8217;s own public records.</b> The reports judged here are the public
        records of Cascade&#8217;s tools (the reader, the matcher, the scenario, the factor):
        published, sealed, verifiable by anyone. A question without one is a named row,
        never a guessed column.</li>
      <li><b>Five controls, one order.</b> present, sealed, signed, fresh, consistent: the
        state reached is the highest control held <b>without a gap</b> in that order. A held
        control above a hole counts for nothing, and the table shows why.</li>
      <li><b>Freshness against a declared rhythm.</b> Each measurement&#8217;s age is judged
        against the rhythm written in the dossier itself ({RG["rythmeJours"]} days), never
        against an unstated habit.</li>
    </ul>
      </details>
      <details class="pli"><summary>What this refuses</summary>
    <ul>
      <li><b>Your data.</b> This page cannot read it: no network requests leave it
        (connect-src &#8216;none&#8217;), no third-party resource is loaded, and there is no input
        field to paste a report into.</li>
      <li><b>A verdict without its sentence.</b> Every cell opens into the record&#8217;s own
        words: what was checked, on which file, and what the next control still needs.</li>
    </ul>
      </details>
    </div>
    <aside class="clone-col">
    <h2>Assemble the dossier of your own reports</h2>
    <p>The instrument shows our dossier, over our public records. Yours is assembled at home,
      by the tool, from the sealed reports the suite&#8217;s tools left at your desk, and nothing
      about them leaves your machine.</p>
    <span class="clone-t">The three commands, exactly as they run</span>
    <div class="clone" role="group" aria-label="The three commands that assemble the dossier of your own reports">
      <div><span class="ps">$</span> git clone {DEPOT_URL}.git</div>
      <div><span class="ps">$</span> npm ci --ignore-scripts</div>
      <div><span class="ps">$</span> npm run dossier -- --reports=a-measured.json,b-measured.json</div>
      <div class="note">the dossier is written next to your reports, and nowhere else</div>
    </div>
    </aside>
  </div>
</section>

<footer class="pied">
  <div class="colonne">
    <p class="pied-p">On your records, on your machine. <em>Nothing of yours goes up.</em></p>
    <span class="sceau">seal {D["provenance"]["empreinte"]} &#183; measured, then frozen &#183; <a href="{DEPOT_URL}">repository</a></span>
  </div>
</footer>

<script type="application/json" id="donnees">{json.dumps(D)}</script>
<script>{JS}</script>
'''

# le cadratin est interdit sur le site : la garde de l'assembleur le refuse, on se
# l'applique avant lui (les details du releve peuvent en porter : remplaces)
PAGE = PAGE.replace("—", "·").replace("&#8212;", "&#183;")
if "—" in PAGE:
    sys.exit("un cadratin s'est glisse dans la page : la garde du site le refusera.")

(BASE / "INSTRUMENT-DOSSIER.html").write_text(PAGE, encoding="utf-8")
print(f"INSTRUMENT-DOSSIER.html {len(PAGE) / 1e3:.0f} ko")
