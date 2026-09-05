#!/usr/bin/env python3
"""L'INSTRUMENT ROUGE EN DIRECT, sur la forme terminale du vert.

Trois commandes le structurent : `cascade screen --live` (la grille palier x seuil
du releve public, cliquer une cellule lit rappel et fausses alertes avec n et
intervalle), `optimise --recall` (le curseur de rappel exige rejoue la selection
de l'outil a la borne BASSE de Wilson sur les 51 seuils, et nomme la cellule ou
dit qu'aucune ne tient), `verify --sealed` (a l'ouverture, la page reapplique la
regle de selection aux donnees embarquees et refuse de se croire si elle ne
retombe pas sur la cellule emise ; l'empreinte du scelle s'affiche).

D'OU VIENNENT LES CHIFFRES
De instrument-screening-donnees.json, emis par extraire-instrument-screening.mjs :
le releve public scelle de cascade-screening, verifie puis recompose cellule par
cellule temoin avec le rate() de l'outil avant d'avoir le droit d'exister. Les
paires sont ECRITES PAR LE DEPOT (60 match, 60 negatifs durs), la moitie
synthetique est declaree et tenue a part ; aucune donnee client n'existe ici.

CE QUE LA PAGE NE FAIT PAS
Rien n'entre, rien ne sort (connect-src 'none', aucune ressource tierce). Mesurer
l'historique d'alertes du lecteur, c'est l'outil, chez lui : le terminal du bas
donne les trois vraies commandes.
"""
import json
import pathlib
import subprocess
import sys

BASE = pathlib.Path(__file__).parent

r = subprocess.run(["node", str(BASE / "extraire-instrument-screening.mjs")],
                   capture_output=True, text=True)
if r.returncode != 0:
    sys.exit(f"extraire-instrument-screening a refuse :\n{r.stderr}")
print(" ", r.stdout.strip())
D = json.loads((BASE / "instrument-screening-donnees.json").read_text())

PALIERS = [p["id"] for p in D["paliers"]]
MONTRES = D["seuilsMontres"]
DEPOT_URL = "https://github.com/ArslaneSempai-ui/cascade-screening"


def pc(x):
    s = f"{x * 100:.0f}"
    return s


def table_html():
    """La grille palier x seuil des huit colonnes du releve, moitie etiquetee au depart.
    Les cellules ne portent AUCUN chiffre en dur : le JS les peint depuis D, et les
    repeint quand on bascule sur la moitie synthetique."""
    tetes = "".join(f"<th scope='col'>{s:.2f}</th>" for s in MONTRES)
    lignes = ""
    for p in PALIERS:
        cells = "".join(
            f'<td><button class="cell" data-p="{p}" data-s="{s:.2f}" aria-pressed="false">'
            f'<span class="c-rappel"></span><span class="c-fp"></span></button></td>'
            for s in MONTRES)
        lignes += f"<tr><th scope='row'>{p}</th>{cells}</tr>"
    absents = "".join(
        f"<tr class='absent'><th scope='row'>{a}</th>"
        f"<td colspan='{len(MONTRES)}'>not in tonight's registry: measured when it ships, absent rather than faked</td></tr>"
        for a in D["absents"])
    return f'''<div class="t-scroll"><table class="grille">
      <caption class="sr">Pick a cell: each shows recall on confirmed matches over false alerts on hard negatives, at that matcher and threshold</caption>
      <thead><tr><th scope="col">matcher \\ threshold</th>{tetes}</tr></thead>
      <tbody>{lignes}{absents}</tbody></table></div>'''


CSS = '''
  :root{--nuit-a:#33191f;--nuit-b:#241217;--nuit-c:#180b0f;
    --sur:#efe0e2;--sur-pale:#c0a6ab;
    --accent-titre:#7a1f2e;--accent-vif:#d64a5c;--accent-clair:#ffc2c9;
    --texte:"Literata",Georgia,serif;--mono:"Roboto Mono",ui-monospace,Menlo,monospace;
    --montee:cubic-bezier(.16,.84,.32,1)}
  *{box-sizing:border-box;margin:0}
  html{scroll-behavior:smooth;caret-color:var(--accent-vif);
    scrollbar-color:var(--accent-titre) var(--nuit-c)}
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
    background:radial-gradient(120% 100% at 50% -20%,#26101a,var(--nuit-b) 70%)}
  .h1{font-size:clamp(36px,4.6vw,62px);font-weight:600;letter-spacing:-.02em;line-height:1.05;
    text-wrap:balance;max-width:18ch}
  .lede{font-size:clamp(15px,1.25vw,18px);color:var(--sur-pale);max-width:52ch;
    line-height:1.6;margin-top:16px;text-wrap:balance}
  .lede b{color:var(--sur)}

  /* le poste : le robot rubis penche derriere le bord du terminal, coupe net */
  .poste{position:relative;padding:44px 0 64px}
  .dessus{position:relative;width:min(100%,1020px);margin:0 auto}
  .rb{position:absolute;right:30px;top:-312px;width:340px;z-index:2;pointer-events:none;
    filter:drop-shadow(0 26px 44px rgba(0,0,0,.55))}
  .terminal{position:relative;z-index:3;
    background:linear-gradient(180deg,color-mix(in srgb,var(--nuit-b) 55%,#000),color-mix(in srgb,var(--nuit-c) 92%,#000) 120px);
    border:1px solid color-mix(in srgb,var(--accent-vif) 30%,transparent);border-radius:14px;
    box-shadow:0 60px 140px rgba(0,0,0,.7),0 0 0 1px rgba(0,0,0,.4),
      inset 0 1px 0 color-mix(in srgb,var(--accent-clair) 22%,transparent);overflow:hidden}
  .terminal::after{content:"";position:absolute;inset:0;pointer-events:none;border-radius:14px;
    background:repeating-linear-gradient(to bottom,rgba(255,194,201,.016) 0 1px,transparent 1px 3px)}
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
  .tm-preuve .ok{color:var(--accent-vif)}
  .tm-preuve .ko{color:#ff7b6e;font-weight:700}
  .regl{font-family:var(--mono);font-size:12.5px;background:transparent;
    border:1px solid color-mix(in srgb,var(--accent-vif) 40%,transparent);
    border-radius:8px;padding:8px 13px;cursor:pointer;color:var(--accent-clair)}
  .regl:hover{border-color:var(--accent-vif)}
  .regl.actif{background:var(--accent-vif);color:var(--nuit-c);border-color:var(--accent-vif)}
  .regls{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 14px}

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
  .c-rappel{font-size:13px}
  .c-fp{font-size:11px;color:var(--sur-pale)}
  .cell[aria-pressed="true"] .c-fp{color:var(--accent-clair)}

  .b-curseur{flex:1;min-width:280px}
  input[type=range]{width:100%;accent-color:var(--accent-vif)}
  .b-ligne{display:flex;gap:18px;align-items:center;flex-wrap:wrap;margin:4px 0 8px}
  .b-val{font-family:var(--mono);font-size:13px;color:var(--accent-clair);min-width:64px}
  .b-lecture{min-height:44px}
  .b-rout{display:block;margin-top:6px;font-size:12px;color:var(--sur-pale)}

  .basse{padding:26px 0 90px}
  .basse h2{font-size:clamp(22px,2.4vw,30px);font-weight:600;letter-spacing:-.01em;margin:38px 0 10px}
  .basse p{color:var(--sur-pale);max-width:64ch;margin:8px 0}
  .basse p b{color:var(--sur)}
  .basse ul{color:var(--sur-pale);max-width:64ch;margin:8px 0 8px 20px;padding:0}
  .basse li{margin:6px 0}
  .basse li b{color:var(--sur)}
  .clone{margin-top:18px;background:color-mix(in srgb,var(--nuit-c) 92%,#000);
    border:1px solid color-mix(in srgb,var(--accent-vif) 25%,transparent);border-radius:12px;
    padding:18px 22px;font-family:var(--mono);font-size:13px;line-height:1.9;overflow-x:auto}
  .clone .ps{color:var(--accent-vif)}
  .clone .note{color:var(--sur-pale);font-size:12px}
  .pied{padding:26px 0 60px;border-top:1px solid color-mix(in srgb,var(--sur-pale) 14%,transparent);
    color:var(--sur-pale);font-size:13px}
  .pied a{color:inherit}

  /* la barre se replie comme celle du vert : sous 1080 la nav disparaît, le sceau
     garde sa place ; mesuré au banc des tailles : nav et sceau débordaient à 320-500 */
  @media (max-width:1080px){
    .barre{padding:12px 18px;gap:14px}
    .barre nav{display:none}
  }
  @media (max-width:900px){
    .colonne{padding:0 20px}
    .rb{width:220px;top:-200px;right:8px}
    .tete{padding:150px 0 18px}
  }
  /* Sous 700px le robot s'asseyait SUR la lede et cachait des mots, relu sur la capture
     375 : la lisibilite passe avant la mascotte, il se retire du telephone. */
  @media (max-width:700px){
    .rb{display:none}
  }
'''

JS = '''
  const $ = (s) => document.querySelector(s);
  const D = JSON.parse(document.getElementById("donnees").textContent);
  const MONTRES = D.seuilsMontres.map((s) => s.toFixed(2));
  let moitie = "authored";

  const pc = (x) => (x * 100).toFixed(0) + "%";
  const pc1 = (x) => (x * 100).toFixed(1) + "%";
  const iv = (c) => "[" + (c.bas * 100).toFixed(0) + "\\u2013" + (c.haut * 100).toFixed(0) + "]";

  const cells = [...document.querySelectorAll(".cell")];
  function peindreGrille() {
    const g = D[moitie].grille;
    for (const c of cells) {
      const cel = g[c.dataset.p][c.dataset.s];
      c.querySelector(".c-rappel").textContent = pc(cel.rappel.taux);
      c.querySelector(".c-fp").textContent = pc(cel.fauxPositifs.taux) + " fa";
    }
    $("#g-quoi").innerHTML = moitie === "authored"
      ? "authored pairs: <b>" + D.authored.nMatch + " match</b>, <b>" + D.authored.nDifferent + " hard negatives</b>"
      : "synthetic variants, declared and kept apart: <b>" + D.synthetic.nMatch + " match</b>, <b>" + D.synthetic.nDifferent + " different</b>";
  }
  function lire(c) {
    cells.forEach((x) => x.setAttribute("aria-pressed", String(x === c)));
    const cel = D[moitie].grille[c.dataset.p][c.dataset.s];
    $("#g-lecture").innerHTML = "<b>" + c.dataset.p + "</b> at threshold <b>" + c.dataset.s + "</b>: "
      + "recall on confirmed matches <b>" + pc1(cel.rappel.taux) + "</b> " + iv(cel.rappel) + ", n=" + cel.rappel.n
      + " \\u00b7 false alerts <b>" + pc1(cel.fauxPositifs.taux) + "</b> " + iv(cel.fauxPositifs) + ", n=" + cel.fauxPositifs.n;
  }
  cells.forEach((c) => c.addEventListener("click", () => lire(c)));
  $("#m-auth").addEventListener("click", () => { moitie = "authored"; basculer(); });
  $("#m-synth").addEventListener("click", () => { moitie = "synthetic"; basculer(); });
  function basculer() {
    $("#m-auth").classList.toggle("actif", moitie === "authored");
    $("#m-synth").classList.toggle("actif", moitie === "synthetic");
    peindreGrille();
    const presse = cells.find((x) => x.getAttribute("aria-pressed") === "true");
    if (presse) lire(presse);
  }

  /* LA MEME REGLE QUE L'OUTIL, reappliquee ici : borne basse du rappel au plancher,
     puis le moins de fausses alertes, puis le palier le moins cher, puis le seuil haut. */
  const rangs = Object.fromEntries(D.paliers.map((p) => [p.id, p.rang]));
  function retenir(plancher) {
    let best = null;
    for (const [palier, grille] of Object.entries(D.authored.grille)) {
      for (const [seuil, cel] of Object.entries(grille)) {
        if (cel.rappel.bas < plancher) continue;
        const cand = { palier, seuil: Number(seuil), rang: rangs[palier], rappel: cel.rappel, fauxPositifs: cel.fauxPositifs };
        if (best === null
          || cand.fauxPositifs.taux < best.fauxPositifs.taux
          || (cand.fauxPositifs.taux === best.fauxPositifs.taux && (cand.rang < best.rang
          || (cand.rang === best.rang && cand.seuil > best.seuil)))) best = cand;
      }
    }
    return best;
  }
  const curseur = $("#b-curseur");
  function rejouer() {
    const plancher = parseFloat(curseur.value);
    $("#b-val").textContent = plancher.toFixed(2);
    const c = retenir(plancher);
    const sortie = $("#b-lecture");
    if (!c) {
      sortie.innerHTML = "no cell holds a recall LOWER BOUND of <b>" + plancher.toFixed(2)
        + "</b> on the public record \\u00b7 the tool would say the same, and name the strongest bound available";
      return;
    }
    sortie.innerHTML = "under a recall floor of <b>" + plancher.toFixed(2) + "</b> (lower bound, the tool's rule): "
      + "<b>" + c.palier + "</b> at threshold <b>" + c.seuil.toFixed(2) + "</b>"
      + '<span class="b-rout">recall ' + pc1(c.rappel.taux) + " " + iv(c.rappel) + ", n=" + c.rappel.n
      + " \\u00b7 false alerts " + pc1(c.fauxPositifs.taux) + " " + iv(c.fauxPositifs) + ", n=" + c.fauxPositifs.n + "</span>";
  }
  curseur.addEventListener("input", rejouer);

  /* verify --sealed : la page reapplique la regle et doit retomber sur la cellule emise */
  (() => {
    const relu = retenir(D.recommandee.plancher);
    const el = $("#tm-preuve");
    const ok = relu !== null && relu.palier === D.recommandee.palier && relu.seuil === D.recommandee.seuil;
    if (ok) {
      el.innerHTML = 'self-check <span class="ok">passed</span>: this page reapplies the tool\\u2019s selection rule to the shipped grid and lands on the same cell the extractor sealed \\u00b7 record '
        + D.provenance.empreinte + ", " + D.provenance.date + " (commit " + D.provenance.commit + ")";
    } else {
      el.innerHTML = 'self-check <span class="ko">FAILED</span>: this page no longer reproduces the sealed selection; do not trust its figures';
    }
  })();

  peindreGrille();
  curseur.value = D.recommandee.plancher;
  rejouer();
'''

ABSENTS = ", ".join(D["absents"]) if D["absents"] else ""

PAGE = f'''<!doctype html><html lang="en">
<meta charset="utf-8"><title>Cascade Screening &#183; live instrument</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta property="og:type" content="website">
<meta property="og:title" content="Cascade Screening: the live instrument">
<meta property="og:description" content="Every matcher at every threshold on the sealed public record: recall against false alerts, intervals everywhere, the tool's own selection rule under your recall floor.">
<meta property="og:url" content="https://cascade-routing.com/screening/instrument.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="description" content="Every matcher at every threshold on the sealed public record: recall against false alerts, intervals everywhere, the tool's own selection rule under your recall floor.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M0 0h16L0 16z' fill='%23180b0f'/%3E%3Cpath d='M16 0v16H0z' fill='%237a1f2e'/%3E%3C/svg%3E">
<link rel="stylesheet" href="../fontes/literata.css">
<link rel="stylesheet" href="../fontes/roboto-mono.css">
<script>document.documentElement.classList.add("js")</script>
<style>{CSS}</style>
<header class="barre">
  <a class="marque" href="../HERO.html">CASCADE <small>&#183; Screening</small></a>
  <nav aria-label="Site">
    <a href="INSTRUMENT-SCREENING.html" aria-current="page">Instrument</a>
    <a href="../ENGAGEMENT.html">Pricing</a>
    <a href="{DEPOT_URL}">Repository</a>
  </nav>
  <span class="sceau">sealed {D["provenance"]["empreinte"]}</span>
</header>

<section class="tete">
  <div class="colonne">
    <h1 class="h1">Which matcher, at which threshold. Live.</h1>
    <p class="lede">Every figure on this page comes from the <b>sealed public record</b> of
      cascade-screening: pairs the repository wrote itself, hard negatives included, measured
      by its own matchers. No client data exists here, nothing enters and nothing leaves,
      and the page checks its own arithmetic before your eyes.</p>
  </div>
</section>

<section class="poste">
  <div class="colonne">
    <div class="dessus">
      <div class="t-page-halo" aria-hidden="true"></div>
      <img class="rb" src="../rendus/robot-rubis-penche.webp" alt="" width="680" height="765">
      <div class="terminal">
        <div class="tm-barre"><i></i><i></i><i></i><span>cascade screening &#183; the public record, live</span></div>
        <div class="tm-corps">
          <p class="tm-l"><span class="ps">$</span> cascade screen --live<span class="caret" aria-hidden="true"></span></p>
          <div class="regls" role="group" aria-label="Which half of the record">
            <button class="regl actif" id="m-auth">labelled pairs (authored)</button>
            <button class="regl" id="m-synth">synthetic variants (declared)</button>
          </div>
          <p class="tm-sortie" id="g-quoi"></p>
          {table_html()}
          <p class="tm-sortie" id="g-lecture">pick a cell: recall over false alerts, with n and its 95&nbsp;% interval</p>

          <p class="tm-l"><span class="ps">$</span> cascade optimise --recall</p>
          <div class="b-ligne">
            <span class="b-val" id="b-val"></span>
            <div class="b-curseur"><input type="range" id="b-curseur" min="0.50" max="1.00" step="0.01"
              aria-label="Required recall floor, held at the Wilson lower bound"></div>
          </div>
          <p class="tm-sortie b-lecture" id="b-lecture"></p>

          <p class="tm-l" style="margin-top:14px"><span class="ps">$</span> cascade verify --sealed</p>
          <p class="tm-preuve" id="tm-preuve">checking&#8230;</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="basse">
  <div class="colonne">
    <h2>What this rests on</h2>
    <ul>
      <li><b>The sealed public record.</b> releve-public.json in the repository, fingerprint
        <b>{D["provenance"]["empreinte"]}</b>, measured at commit <b>{D["provenance"]["commit"]}</b>
        on {D["provenance"]["date"]}. The extractor that feeds this page verifies the seal,
        then recomposes witness cells with the tool&#8217;s own interval code, and refuses to emit
        if a single figure disagrees.</li>
      <li><b>Pairs the repository wrote.</b> The labelled half is authored: true correspondences
        (transliterations, token order, initials, typos, particles) and hard negatives
        (siblings, partial homonyms, near-strings that are not the same person). The labels
        ship with the pairs, debatable ones with their reasons.</li>
      <li><b>Synthetic variants, kept apart.</b> Generated from list-entry names, nature by
        nature, and never merged with the authored half: the toggle above switches the whole
        grid, it never blends.</li>
      <li><b>The tool&#8217;s selection rule.</b> The slider holds your recall floor at the Wilson
        <b>lower bound</b>, exactly as <span style="font-family:var(--mono)">npm run optimise</span>
        does: a point estimate never clears a floor here.</li>
    </ul>
    <h2>What this refuses</h2>
    <ul>
      <li><b>Your data.</b> This page cannot read it: no network requests leave it
        (connect-src &#8216;none&#8217;), no third-party resource is loaded, and there is no input
        field to paste a name into.</li>
      <li><b>Bare rates.</b> Every cell carries its n and its 95&nbsp;% interval; a matcher absent
        from tonight&#8217;s registry ({ABSENTS}) is a named row, never a guessed column.</li>
    </ul>
    <h2>Measure your own alert history</h2>
    <p>The instrument shows our record. Yours is measured at home, by the tool, and nothing
      about your file leaves your machine:</p>
    <div class="clone">
      <div><span class="ps">$</span> git clone {DEPOT_URL}.git</div>
      <div><span class="ps">$</span> npm ci --ignore-scripts</div>
      <div><span class="ps">$</span> npm run measure:yours -- --alerts=your-alerts.csv</div>
      <div class="note">the report and the sealed record are written next to your file, and nowhere else</div>
    </div>
  </div>
</section>

<footer class="pied">
  <div class="colonne">
    Cascade &#183; Screening &#8212; every figure above is read from the sealed public record,
    never typed. <a href="{DEPOT_URL}">Repository</a>.
  </div>
</footer>

<script type="application/json" id="donnees">{json.dumps(D)}</script>
<script>{JS}</script>
'''

# le cadratin est interdit sur le site : la garde de l'assembleur le refuse, on se
# l'applique avant lui (l'entite &#8212; du pied est volontairement REMPLACEE ici)
PAGE = PAGE.replace("&#8212;", "&#183;")
if "—" in PAGE:
    sys.exit("un cadratin s'est glisse dans la page : la garde du site le refusera.")

(BASE / "INSTRUMENT-SCREENING.html").write_text(PAGE, encoding="utf-8")
print(f"INSTRUMENT-SCREENING.html {len(PAGE) / 1e3:.0f} ko")
