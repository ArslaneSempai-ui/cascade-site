#!/usr/bin/env python3
"""Six directions pour le même écran d'accueil, écrites d'un coup.

POURQUOI UN GÉNÉRATEUR ET PAS SIX FICHIERS À LA MAIN
Six fichiers écrits l'un après l'autre dérivent : la palette bouge, l'en-tête change de
demi-pixel, et on finit par comparer des feuilles de style au lieu de comparer des idées.
Ici l'identité — palette, en-tête, bouton, échelle typographique — est écrite UNE fois ;
ce qui diffère d'une direction à l'autre est la COMPOSITION et l'argument, c'est-à-dire
la seule chose qu'on veut juger.

CE QUI DIFFÈRE, ET POURQUOI ÇA VAUT LA PEINE
Six styles ne sont pas six directions. Chacune ci-dessous répond autrement à « comment
prouver l'écart en trois secondes », et chacune a une valeur ajoutée qu'aucune autre n'a :
  2 · l'objet annoté   — l'argument vit DANS la photographie ; aucun diagramme.
  3 · le calcul        — montre POURQUOI les deux chiffres diffèrent, pas seulement qu'ils
                         diffèrent : cinq taux moyennés d'un côté, cent vingt dossiers
                         comptés de l'autre. C'est la seule qui explique.
  4 · la couverture    — impact maximal, chiffres au second plan. La moins informative.
  5 · le livrable      — ce n'est pas un site, c'est la première page du rapport qu'ils
                         recevront. Vend l'artefact plutôt que la promesse.
  6 · les 120 dossiers — rend les 28 dossiers cassés COMPTABLES au lieu d'un pourcentage.
                         La plus directe pour qui traite les dossiers.
La direction 1, l'instrument à l'échelle, existe déjà : A3-hero.html.
"""
import pathlib

BASE = pathlib.Path(__file__).parent

TETE = ('<div class="tete"><b>CASCADE</b><span>routing audit — KYC extraction</span>'
        '<span class="d">report 64bdacf · measured once · frozen</span></div>')
TITRE = "Your dashboard says 94%. Your case files go out at 77%."
THESE = ("Both figures are true, and they measure different things. Only one counts a file "
         "as right when <b>all five fields are right together</b> — and that is the one "
         "whose errors reach your review team.")
CTA = '<a class="bouton" href="#">Have your routing measured</a>'
APPUI = ("On your records, on your machine. Nothing leaves the network. If nothing comes "
         "out cheaper without breaking a file, the report says so.")
ALT = ("The measurement in relief: six rows of chip stacks on a plate, one stack per reader "
       "and per field, each chip worth ten points of measured accuracy. The seventh row has "
       "no tiles at all — the human operator was never sampled field by field.")

COMMUN = """
  :root{
    --papier:#e3ddcc; --relief:#efeade; --creux:#d5cdb8;
    --encre:#16181c; --demi:#4f4a41; --pale:#6c6656;
    --filet:#b7ae96; --fin:#cdc4ae;
    --vert:#2f8a60; --rouge:#a8462f;
    --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
    --sans:ui-sans-serif,-apple-system,"Helvetica Neue",sans-serif;
    --mono:ui-monospace,"SF Mono",Menlo,monospace;
  }
  *{box-sizing:border-box}
  /* Le fond va sur <html> ET sur <body> : sans celui de <html>, celui de <body> est propagé
     au canevas, et un élément en mélange n'aurait plus de toile de fond. */
  html{background:#ded7c4}
  body{margin:0;color:var(--encre);font:400 16px/1.55 var(--serif);
       -webkit-font-smoothing:antialiased;
       background:
         radial-gradient(58% 54% at 71% 30%, rgba(248,244,235,.55) 0%, rgba(248,244,235,0) 72%),
         linear-gradient(172deg, #e9e3d3 0%, #e1dac8 52%, #d5cdb6 100%);
       background-attachment:fixed}
  .ecran{min-height:100vh;display:flex;flex-direction:column;max-width:94rem;margin:0 auto;
         padding:1.3rem clamp(1.2rem,3.6vw,3.2rem) 1.2rem}
  .tete{display:flex;gap:1.1rem;align-items:baseline;flex-wrap:wrap;
        border-bottom:1.5px solid var(--encre);padding-bottom:.5rem}
  .tete b{font:600 13px/1 var(--sans);letter-spacing:.22em}
  .tete span{font-size:14.5px;color:var(--demi)}
  .tete .d{margin-left:auto;font:600 10px/1 var(--sans);letter-spacing:.14em;
           text-transform:uppercase;color:var(--pale)}
  .oeil{font:600 10px/1.4 var(--sans);letter-spacing:.16em;text-transform:uppercase;
        color:var(--pale);display:block;margin-bottom:.75rem}
  h1{font:600 clamp(1.9rem,3.5vw,3rem)/1.07 var(--serif);letter-spacing:-.023em;
     margin:0 0 .8rem;max-width:18ch;text-wrap:balance}
  .these{color:var(--demi);margin:0 0 1.4rem;max-width:42ch;font-size:16.5px}
  .these b{color:var(--encre);font-weight:600}
  .agir{display:flex;gap:1.1rem;align-items:center;flex-wrap:wrap}
  .bouton{background:var(--encre);color:var(--relief);text-decoration:none;
          font:600 15px/1 var(--sans);padding:.95rem 1.5rem;border:1px solid var(--encre)}
  .bouton:hover{background:transparent;color:var(--encre)}
  .bouton:focus-visible{outline:2px solid var(--vert);outline-offset:3px}
  .agir p{margin:0;font:400 13.5px/1.45 var(--sans);color:var(--demi);max-width:34ch}
  .n{font-family:var(--mono);font-variant-numeric:tabular-nums}
  .prise{all:unset;cursor:pointer;display:block}
  .prise:focus-visible{outline:2px solid var(--vert);outline-offset:2px}
"""

def page(nom, titre, extra_css, corps, script=""):
    (BASE / nom).write_text(f"""<!doctype html>
<meta charset="utf-8"><title>{titre}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%23e3ddcc'/%3E%3C/svg%3E">
<style>{COMMUN}{extra_css}</style>
{corps}
{script}
""")
    print("  écrit :", nom)


# ── 2 · L'OBJET ANNOTÉ ────────────────────────────────────────────────────────
# L'argument vit dans la photographie : deux repères posés SUR l'objet, tirés vers les
# chiffres. Aucun diagramme, aucune deuxième figure — l'objet fait le travail des deux.
page("D2-objet-annote.html", "Cascade — annotated", """
  .scene{flex:1;position:relative;display:grid;
         grid-template-columns:minmax(0,.86fr) minmax(0,1.14fr);
         gap:clamp(1rem,3vw,2.6rem);align-items:center;padding:1.4rem 0 .6rem}
  @media(max-width:960px){.scene{grid-template-columns:1fr}}
  .plaque{position:relative;margin:0}
  .plaque img{width:100%;max-width:760px;max-height:66vh;object-fit:contain;display:block;
              margin-left:auto}
  /* Les repères sont posés en pour-cent de la figure : ils suivent l'image quand elle se
     redimensionne, au lieu de glisser à côté de ce qu'ils désignent. */
  .rep{position:absolute;font:600 10px/1.4 var(--sans);letter-spacing:.12em;
       text-transform:uppercase;color:var(--pale);white-space:nowrap}
  .rep b{display:block;font:600 30px/1 var(--mono);letter-spacing:-.02em;margin-top:.15rem}
  .rep i{display:block;font:400 12px/1.4 var(--sans);font-style:normal;max-width:23ch;
         white-space:normal;margin-top:.2rem}
  .rep.efface{opacity:.3}
  .rep{transition:opacity .2s ease}
  .rep.haut{color:var(--pale)}
  .rep.bas b{color:var(--encre)}
  .fil{position:absolute;border-left:1px solid var(--filet)}
  .fil.h{border-left:none;border-top:1px solid var(--filet)}
  .socle{display:flex;gap:1.4rem;align-items:baseline;flex-wrap:wrap;
         border-top:1px solid var(--filet);padding-top:.7rem;
         font:400 13.5px/1.5 var(--sans);color:var(--demi)}
""", f"""<div class="ecran">
  {TETE}
  <div class="scene">
    <div>
      <span class="oeil">Finding — two rates over the same 120 files</span>
      <h1>{TITRE}</h1>
      <p class="these">{THESE}</p>
      <div class="agir">{CTA}<p>{APPUI}</p></div>
    </div>
    <figure class="plaque">
      <img src="rendus/plaque-hero.png" alt="{ALT}">
      <span class="fil" style="left:31%;top:6%;height:13%"></span>
      <button class="rep haut prise" type="button" data-rep="A" style="left:16%;top:0">Green tiles — the routing in production
        <b>94.4%</b><i>the mean of its five field rates, one field at a time</i></button>
      <span class="fil h" style="left:62%;top:84%;width:22%"></span>
      <button class="rep bas prise" type="button" data-rep="B" style="left:62%;top:86%">All five together, one file
        <b>76.7%</b><i>92 of 120 · Wilson 95% [68.3 – 83.3]</i></button>
    </figure>
  </div>
  <div class="socle"><span class="n" style="color:var(--encre);font-weight:600">17.7 points</span>
    <span>separate what the dashboard reports from what the review desk receives.
      The plate holds one stack per reader and per field; the empty channel is the human
      operator, who was never sampled field by field.</span></div>
</div>""", """<script>
/* Un repère à la fois : les deux allumés, la photographie porte deux affirmations que rien
   ne sépare, et c'est exactement la confusion que la page dénonce. */
const reps = [...document.querySelectorAll(".rep")];
let vu = null;
for (const r of reps) r.addEventListener("click", () => {
  vu = vu === r.dataset.rep ? null : r.dataset.rep;
  for (const x of reps) x.classList.toggle("efface", vu !== null && x.dataset.rep !== vu);
});
</script>""")


# ── 3 · LE CALCUL ─────────────────────────────────────────────────────────────
# La seule direction qui explique POURQUOI les deux chiffres diffèrent : à gauche cinq taux
# qu'on moyenne, à droite cent vingt dossiers qu'on compte. Deux opérations, deux unités.
page("D3-le-calcul.html", "Cascade — two arithmetics", """
  .haut{padding:1.3rem 0 .4rem}
  .deux{flex:1;display:grid;grid-template-columns:1fr 1px 1fr;gap:clamp(1.2rem,3.4vw,3rem);
        align-items:start;padding-bottom:.8rem}
  @media(max-width:960px){.deux{grid-template-columns:1fr}.sep{display:none}}
  .sep{background:var(--filet)}
  .col h2{font:600 11px/1.4 var(--sans);letter-spacing:.14em;text-transform:uppercase;
          color:var(--pale);margin:0 0 .1rem}
  .col .op{font:400 14px/1.5 var(--sans);color:var(--demi);margin:0 0 1rem;max-width:38ch}
  .champ{display:grid;grid-template-columns:9.5rem 3.6rem minmax(0,1fr);gap:.7rem;
         align-items:center;padding:.3rem 0;width:100%;text-align:left;
         transition:opacity .2s ease}
  .col.choisi .champ:not(.vu){opacity:.34}
  .champ.vu .b i{background:var(--encre)}
  .champ.vu .q,.champ.vu .v{font-weight:600;color:var(--encre)}
  .champ .q{font:400 14.5px/1.3 var(--serif)}
  .champ .v{font:500 13.5px/1 var(--mono);font-variant-numeric:tabular-nums;text-align:right}
  .champ .b{height:9px;background:var(--creux)}
  .champ .b i{display:block;height:100%;background:var(--pale)}
  .somme{display:grid;grid-template-columns:9.5rem 3.6rem minmax(0,1fr);gap:.7rem;
         align-items:center;border-top:1.5px solid var(--encre);margin-top:.5rem;
         padding-top:.5rem}
  .somme .q{font:600 15.5px/1.3 var(--serif)}
  .somme .v{font:600 19px/1 var(--mono);text-align:right}
  .somme .r{font:400 12.5px/1.4 var(--sans);color:var(--pale)}
  /* Cent vingt dossiers, comptés. Le pourcentage n'apparaît qu'après le compte, jamais avant. */
  .grille{display:grid;grid-template-columns:repeat(20,1fr);gap:3px;margin:.2rem 0 .8rem}
  .grille i{display:block;aspect-ratio:1;background:var(--encre)}
  .grille i.casse{background:transparent;box-shadow:inset 0 0 0 1px var(--rouge)}
  .cpt{display:flex;gap:1.3rem;flex-wrap:wrap;font:400 13.5px/1.5 var(--sans);color:var(--demi)}
  .cpt b{color:var(--encre)}
  .cpt .k{color:var(--rouge)}
  .bas{display:flex;gap:1.3rem;align-items:center;flex-wrap:wrap;
       border-top:1px solid var(--filet);padding-top:.9rem}
""", f"""<div class="ecran">
  {TETE}
  <div class="haut">
    <span class="oeil">Two arithmetics over the same 120 files</span>
    <h1>{TITRE}</h1>
  </div>
  <div class="deux">
    <div class="col">
      <h2>What the dashboard averages</h2>
      <p class="op">Five field rates, measured one field at a time, then divided by five.
        A mean of five rates is not a proportion, so it carries no interval.</p>
      <button class="champ prise" type="button"><span class="q">Name</span><span class="v">96.6</span>
        <span class="b"><i style="width:96.6%"></i></span></button>
      <button class="champ prise" type="button"><span class="q">Date of birth</span><span class="v">100</span>
        <span class="b"><i style="width:100%"></i></span></button>
      <button class="champ prise" type="button"><span class="q">Document no.</span><span class="v">79.7</span>
        <span class="b"><i style="width:79.7%"></i></span></button>
      <button class="champ prise" type="button"><span class="q">Country</span><span class="v">100</span>
        <span class="b"><i style="width:100%"></i></span></button>
      <button class="champ prise" type="button"><span class="q">Address</span><span class="v">95.8</span>
        <span class="b"><i style="width:95.8%"></i></span></button>
      <div class="somme"><span class="q">Mean</span><span class="v">94.4%</span>
        <span class="r">472.1 ÷ 5 — no confidence interval</span></div>
    </div>
    <div class="sep"></div>
    <div class="col">
      <h2>What the review desk counts</h2>
      <p class="op">One mark per case file. A file counts only when all five fields are
        right together — which is the unit that leaves the desk.</p>
      <div class="grille" id="grille"></div>
      <div class="cpt"><span><b>92</b> complete</span>
        <span class="k"><b class="k">28</b> with at least one field wrong</span>
        <span>120 files in the retained corpus</span></div>
      <div class="somme"><span class="q">Per-file rate</span><span class="v">76.7%</span>
        <span class="r">92 ÷ 120 — Wilson 95% [68.3 – 83.3]</span></div>
    </div>
  </div>
  <div class="bas">{CTA}<p style="margin:0;font:400 13.5px/1.45 var(--sans);color:var(--demi);max-width:52ch">{APPUI}</p></div>
</div>""", """<script>
/* La grille se dessine depuis les comptes, pas à la main : cent vingt cases écrites en dur
   se désaccordent du chiffre dès qu'un dossier change de camp, et c'est la figure qui ment. */
const COMPLETS = 92, TOTAL = 120;
const g = document.getElementById("grille");
for (let k = 0; k < TOTAL; k++) {
  const i = document.createElement("i");
  if (k >= COMPLETS) i.className = "casse";
  g.appendChild(i);
}

/* Un champ retenu à la fois : c'est ce qui laisse voir lequel des cinq tire la moyenne
   vers le bas, ce qu'une colonne de cinq barres également noires ne montre pas. */
const col = document.querySelector(".col");
col.addEventListener("click", (e) => {
  const b = e.target.closest("button.champ"); if (!b) return;
  const deja = b.classList.contains("vu");
  col.querySelectorAll(".vu").forEach((x) => x.classList.remove("vu"));
  if (!deja) b.classList.add("vu");
  col.classList.toggle("choisi", !deja);
});
</script>""")


# ── 4 · LA COUVERTURE ─────────────────────────────────────────────────────────
# Impact d'abord : l'objet à pleine page, le texte en pied comme la légende d'une couverture.
# La moins informative des six, et c'est assumé — elle est là pour tenir trois secondes.
page("D4-couverture.html", "Cascade — cover", """
  .ecran{padding-bottom:0}
  .plein{flex:1;position:relative;display:flex;align-items:center;justify-content:center;
         margin:0 calc(-1 * clamp(1.2rem,3.6vw,3.2rem));overflow:hidden}
  .plein img{width:104%;max-width:none;object-fit:contain;max-height:74vh;display:block;
             transform:translateY(-2%)}
  .legende{position:absolute;left:clamp(1.2rem,3.6vw,3.2rem);bottom:2%;max-width:34rem;
           padding-right:1rem}
  .legende h1{font-size:clamp(2rem,4.2vw,3.5rem);max-width:16ch;margin-bottom:.6rem}
  .legende p{margin:0 0 1.2rem;color:var(--demi);font-size:17px;max-width:34ch}
  .pied{display:flex;gap:1.6rem;align-items:baseline;flex-wrap:wrap;
        border-top:1.5px solid var(--encre);padding:.7rem 0 1.1rem;
        font:400 13.5px/1.5 var(--sans);color:var(--demi)}
  .pied b{font:600 15px/1 var(--mono);color:var(--encre)}
  .pied .prise{white-space:nowrap;border-bottom:1px dotted var(--filet);padding-bottom:1px}
  .pied .prise[aria-expanded="true"]{border-bottom-color:var(--encre)}
  .pied dfn{display:none;font-style:normal;color:var(--pale);white-space:normal;
            font-size:12.5px;margin-left:.5rem}
  .pied .prise[aria-expanded="true"] dfn{display:inline}
""", f"""<div class="ecran">
  {TETE}
  <div class="plein">
    <img src="rendus/plaque-hero.png" alt="{ALT}">
    <div class="legende">
      <span class="oeil">Finding — two rates over the same 120 files</span>
      <h1>{TITRE}</h1>
      <p>Both are true. Only one counts a file as right when all five fields are right
        together.</p>
      <div class="agir">{CTA}</div>
    </div>
  </div>
  <div class="pied">
    <button class="prise" type="button" aria-expanded="false"><b>94.4%</b> mean of five field rates<dfn>— five fields measured one at a time, then divided by five. Not a proportion, so no interval.</dfn></button>
    <button class="prise" type="button" aria-expanded="false"><b>76.7%</b> per file · 92 of 120<dfn>— a file counts only when all five fields are right together. Wilson 95% [68.3 – 83.3].</dfn></button>
    <button class="prise" type="button" aria-expanded="false"><b>17.7</b> points apart<dfn>— the distance between the two, over the same 120 files.</dfn></button>
    <span style="white-space:normal">On your records, on your machine. Nothing leaves the network.</span>
  </div>
</div>""", """<script>
/* Une définition à la fois, et repliée par défaut : une couverture qui déplie tout n'est
   plus une couverture. */
const pied = document.querySelector(".pied");
pied.addEventListener("click", (e) => {
  const b = e.target.closest("button.prise"); if (!b) return;
  const ouvert = b.getAttribute("aria-expanded") === "true";
  pied.querySelectorAll('[aria-expanded="true"]').forEach((x) =>
    x.setAttribute("aria-expanded", "false"));
  b.setAttribute("aria-expanded", ouvert ? "false" : "true");
});
</script>""")


# ── 5 · LE LIVRABLE ───────────────────────────────────────────────────────────
# Ce n'est pas une page de vente : c'est la première page du rapport qu'ils recevront,
# composée comme telle. Elle vend l'artefact au lieu de la promesse.
page("D5-livrable.html", "Cascade — Finding 01", """
  .ecran{max-width:82rem}
  .cartouche{display:grid;grid-template-columns:auto 1fr auto;gap:1.2rem;align-items:end;
             border-bottom:2px solid var(--encre);padding-bottom:.5rem;margin-bottom:1.1rem}
  .cartouche .no{font:600 42px/1 var(--mono);letter-spacing:-.03em}
  .cartouche .ti{font:600 12px/1.5 var(--sans);letter-spacing:.14em;text-transform:uppercase;
                 color:var(--pale)}
  .cartouche .ti em{display:block;font:400 19px/1.3 var(--serif);font-style:normal;
                    letter-spacing:0;text-transform:none;color:var(--encre)}
  .cartouche .ref{font:500 11px/1.6 var(--mono);color:var(--pale);text-align:right}
  .corps{flex:1;display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);
         gap:clamp(1.2rem,3.4vw,2.8rem);align-items:start}
  @media(max-width:960px){.corps{grid-template-columns:1fr}}
  .corps h1{font-size:clamp(1.5rem,2.4vw,2rem);max-width:24ch;margin-bottom:.5rem}
  .corps p{margin:0 0 .9rem;max-width:52ch;color:var(--demi)}
  .corps p b{color:var(--encre);font-weight:600}
  table{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:13.5px;
        margin:.4rem 0 1rem;max-width:34rem}
  th,td{padding:.4rem 0;text-align:right;border-bottom:1px solid var(--fin);
        font-variant-numeric:tabular-nums;white-space:nowrap}
  th{text-align:left;font:400 15px/1.35 var(--serif)}
  td.r{color:var(--pale);font-size:12px;padding-left:1rem}
  tr:last-child th,tr:last-child td{border-bottom:none;border-top:1.5px solid var(--encre);
    padding-top:.5rem;font-weight:600}
  .sel{all:unset;cursor:pointer;text-decoration:underline;
       text-decoration-color:var(--filet);text-underline-offset:3px;
       padding:.35rem .25rem;margin:0 -.25rem}
  .sel:focus-visible{outline:2px solid var(--vert);outline-offset:2px}
  tr.vu th,tr.vu td{background:#d9d2bd}
  tr.vu .sel{text-decoration-color:var(--encre)}
  figure{margin:0}
  figure img{width:100%;max-height:46vh;object-fit:contain;display:block}
  figcaption{font:400 12px/1.5 var(--sans);color:var(--pale);margin-top:.4rem;
             border-top:1px solid var(--filet);padding-top:.4rem}
  figcaption b{font:600 10px/1 var(--sans);letter-spacing:.13em;text-transform:uppercase;
               color:var(--demi);display:block;margin-bottom:.25rem}
  .signature{display:flex;gap:1.2rem;align-items:center;flex-wrap:wrap;
             border-top:1.5px solid var(--encre);padding-top:.9rem;margin-top:.4rem}
  .signature p{margin:0;font:400 13px/1.45 var(--sans);color:var(--demi);max-width:40ch}
""", f"""<div class="ecran">
  <div class="cartouche">
    <span class="no">01</span>
    <span class="ti">Finding<em>Two rates over the same 120 case files</em></span>
    <span class="ref">CASCADE · routing audit — KYC extraction<br>report 64bdacf · measured once · frozen</span>
  </div>
  <div class="corps">
    <div>
      <h1>{TITRE}</h1>
      <p>{THESE}</p>
      <p>The two figures are computed differently. <b>94.4%</b> is the mean of five field
        rates, each measured one field at a time; a mean of rates is not a proportion and
        carries no confidence interval. <b>76.7%</b> is a proportion — 92 files out of 120 —
        and carries one.</p>
      <table>
        <tbody>
          <tr><th><button class="sel" type="button">Mean of the five field rates</button></th><td>94.4%</td>
              <td class="r">no interval</td></tr>
          <tr><th><button class="sel" type="button">Complete case files</button></th><td>92 / 120</td>
              <td class="r">all five fields right together</td></tr>
          <tr><th><button class="sel" type="button">Per-file rate</button></th><td>76.7%</td>
              <td class="r">Wilson 95% [68.3 – 83.3]</td></tr>
        </tbody>
      </table>
      <div class="signature">{CTA}<p>{APPUI}</p></div>
    </div>
    <figure>
      <img src="rendus/plaque-hero.png" alt="{ALT}">
      <figcaption><b>Fig. 1 — accuracy by reader and field</b>One stack per reader and per
        field; one chip is ten points of measured accuracy. Green marks the reader the
        routing uses for that field. The empty channel is the human operator, who was never
        sampled field by field — the plate leaves the row open rather than filling it.</figcaption>
    </figure>
  </div>
</div>""", """<script>
/* Une ligne retenue à la fois : deux lignes soulignées ne comparent plus, elles décorent. */
const corps = document.querySelector("tbody");
corps.addEventListener("click", (e) => {
  const b = e.target.closest("button.sel"); if (!b) return;
  const tr = b.closest("tr"), deja = tr.classList.contains("vu");
  corps.querySelectorAll("tr.vu").forEach((x) => x.classList.remove("vu"));
  if (!deja) tr.classList.add("vu");
});
</script>""")


# ── 6 · LES 120 DOSSIERS ──────────────────────────────────────────────────────
# Un pourcentage ne se compte pas ; vingt-huit dossiers, si. La direction la plus directe
# pour qui a les dossiers sur son bureau — elle troque l'abstraction contre un décompte.
page("D6-cent-vingt.html", "Cascade — 28 files", """
  .haut{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.35fr);
        gap:clamp(1.4rem,4vw,3.4rem);align-items:center;flex:1;padding:1.4rem 0 .8rem}
  @media(max-width:1000px){.haut{grid-template-columns:1fr}}
  /* Douze colonnes de dix : on lit « dix » d'un coup d'œil, et au-delà de quatre unités
     personne ne compte — les rangées de dix sont ce qui rend vingt-huit comptable. */
  .champ{display:grid;grid-template-columns:repeat(12,1fr);gap:clamp(5px,.7vw,10px)}
  .champ i{display:block;aspect-ratio:1;background:var(--encre);border-radius:1px}
  .champ i.casse{background:transparent;box-shadow:inset 0 0 0 1.5px var(--rouge);
                 position:relative}
  .champ i.casse::after{content:"";position:absolute;inset:22%;
                        background:linear-gradient(45deg,transparent 44%,var(--rouge) 44%,
                          var(--rouge) 56%,transparent 56%)}
  .cles{display:flex;gap:1.6rem;flex-wrap:wrap;margin-top:.9rem;
        font:400 13.5px/1.5 var(--sans);color:var(--demi);align-items:center}
  .cles span{display:flex;gap:.45rem;align-items:center}
  .cles u{width:13px;height:13px;background:var(--encre);border-radius:1px;
          text-decoration:none;display:block}
  .cles u.k{background:transparent;box-shadow:inset 0 0 0 1.5px var(--rouge)}
  .cles b{color:var(--encre);font-family:var(--mono);font-size:15px}
  .cles .prise{display:flex;gap:.45rem;align-items:center;padding:.3rem .35rem;
               margin:-.3rem -.35rem;cursor:pointer}
  .cles .prise:focus-visible{outline:2px solid var(--vert);outline-offset:2px}
  .champ i{transition:opacity .2s ease}
  .champ.q-ok i.casse,.champ.q-casse i:not(.casse){opacity:.16}
  .taux{display:flex;gap:1.8rem;align-items:baseline;flex-wrap:wrap;margin:0 0 1.3rem}
  .taux div span{display:block;font:600 10px/1.4 var(--sans);letter-spacing:.12em;
                 text-transform:uppercase;color:var(--pale)}
  .taux div b{font:600 34px/1 var(--mono);letter-spacing:-.02em}
  .taux .moy b{color:var(--pale)}
  .taux .rem{font:400 12.5px/1.4 var(--sans);color:var(--pale);max-width:15ch}
""", f"""<div class="ecran">
  {TETE}
  <div class="haut">
    <div>
      <span class="oeil">28 of 120 files went out with a field wrong</span>
      <h1>{TITRE}</h1>
      <p class="these">{THESE}</p>
      <div class="taux">
        <div class="moy"><span>Mean of five field rates</span><b>94.4%</b></div>
        <div><span>Per-file rate</span><b>76.7%</b></div>
        <div class="rem">Wilson 95% [68.3 – 83.3] on the per-file rate. The mean carries none.</div>
      </div>
      <div class="agir">{CTA}<p>{APPUI}</p></div>
    </div>
    <div>
      <div class="champ" id="champ"></div>
      <div class="cles">
        <button class="prise" type="button" data-q="ok"><u></u><b>92</b> complete — all five fields right</button>
        <button class="prise" type="button" data-q="casse"><u class="k"></u><b>28</b> with at least one field wrong</button>
        <span>120 files, retained corpus</span>
      </div>
    </div>
  </div>
</div>""", """<script>
/* Les cases sont dessinées depuis les comptes : cent vingt carrés écrits à la main se
   désaccordent du chiffre au premier changement, et c'est alors la figure qui ment. */
const COMPLETS = 92, TOTAL = 120;
const c = document.getElementById("champ");
for (let k = 0; k < TOTAL; k++) {
  const i = document.createElement("i");
  if (k >= COMPLETS) i.className = "casse";
  c.appendChild(i);
}

/* La légende commande le champ : isoler les vingt-huit les rend comptables, ce qu'un
   pourcentage ne permet jamais. */
const cles = document.querySelector(".cles");
let q = null;
cles.addEventListener("click", (e) => {
  const b = e.target.closest("button.prise"); if (!b) return;
  q = q === b.dataset.q ? null : b.dataset.q;
  c.classList.toggle("q-ok", q === "ok");
  c.classList.toggle("q-casse", q === "casse");
});
</script>""")

print("\nsix directions : A3-hero.html (l'instrument) + les cinq écrites ici")
