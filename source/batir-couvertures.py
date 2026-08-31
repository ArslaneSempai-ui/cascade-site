#!/usr/bin/env python3
"""Quatre couvertures — la direction 4, avec les quatre changements demandés.

CE QUI CHANGE PAR RAPPORT À D4
  · l'objet part à DROITE et déborde du cadre, au lieu d'être centré ;
  · le titre est retravaillé — et il change d'une couverture à l'autre, parce que « beau et
    catchy » est justement ce qu'on ne peut pas trancher sans le voir posé ;
  · le fond porte une VRAIE couleur. Le crème précédent lisait comme du blanc : quatre
    stratégies distinctes plutôt que quatre nuances de la même ;
  · l'animation est une séquence composée, pas trois fondus : le sol, puis l'objet qui monte
    et dont l'ombre s'installe, puis le titre ligne par ligne, puis l'appel. Plus le suivi du
    curseur, qui donne du poids à l'objet.

CE QUI NE CHANGE PAS
Les chiffres, l'objet, l'anglais, et le refus d'affirmer plus que la mesure n'autorise.

SUR LA COULEUR ET UNE DÉCISION DÉJÀ PRISE
La direction « console » — noir, terminal, monospace partout — a été écartée le 17 août avec
ses mots : « exactement l'esthétique outil d'IA que tu as écartée, et elle parle aux
ingénieurs plutôt qu'aux gens qui décident ». « Nuit » ci-dessous N'EST PAS ce retour : fond
vert profond de l'identité, titre en serif à l'italienne, aucun élément d'interface. C'est
une couverture de rapport, pas une console. Elle est là parce qu'une couleur sombre est la
seule qui fasse vraiment briller le métal de la plaque — si elle rouvre quand même quelque
chose de tranché, elle se jette.

DURÉES ET GARDE
Chaque transition reste sous six cents millisecondes — au-delà, `ergonomie.mjs` signale à
juste titre qu'un mouvement « semble planté ». La séquence dure plus longtemps que ça, mais
par DÉCALAGE : neuf temps de cent millisecondes, pas une transition d'une seconde et demie.
"""
import pathlib

BASE = pathlib.Path(__file__).parent

ALT = ("The measurement in relief: six rows of chip stacks on a plate, one stack per reader "
       "and per field, each chip worth ten points of measured accuracy. The seventh row has "
       "no tiles at all — the human operator was never sampled field by field.")

# ── le socle commun : identité, séquence d'entrée, suivi du curseur ───────────
COMMUN = """
  :root{
    --encre:#16181c; --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
    --sans:ui-sans-serif,-apple-system,"Helvetica Neue",sans-serif;
    --mono:ui-monospace,"SF Mono",Menlo,monospace;
    --montee:cubic-bezier(.16,.84,.32,1);
  }
  *{box-sizing:border-box}
  body{margin:0;color:var(--encre);font:400 16px/1.55 var(--serif);
       -webkit-font-smoothing:antialiased;overflow-x:hidden}
  /* Le débordement de l'objet est VOULU, mais il ne doit pas devenir une barre de défilement
     horizontale : c'est l'écran qui le coupe, à son propre bord. `overflow-x:hidden` sur
     <body> ne suffit pas — la racine continue de compter la largeur qui dépasse. */
  .ecran{min-height:100vh;display:flex;flex-direction:column;position:relative;overflow:hidden;
         padding:1.3rem clamp(1.2rem,3.6vw,3.4rem) 1.1rem;max-width:100rem;margin:0 auto}
  .tete{display:flex;gap:1.1rem;align-items:baseline;flex-wrap:wrap;
        padding-bottom:.5rem;position:relative;z-index:3}
  .tete b{font:600 13px/1 var(--sans);letter-spacing:.22em}
  .tete span{font-size:14.5px}
  .tete .d{margin-left:auto;font:600 10px/1 var(--sans);letter-spacing:.14em;
           text-transform:uppercase}

  /* L'objet sort du cadre à droite. Le débordement est voulu : un objet coupé par le bord
     se lit comme une pièce trop grande pour la page, et c'est ce qui lui donne son échelle. */
  .plaque{position:absolute;margin:0;pointer-events:none;z-index:1}
  .plaque img{width:100%;display:block}
  .socle-ombre{position:absolute;border-radius:50%;pointer-events:none;z-index:0}

  .bloc{position:relative;z-index:2;display:flex;flex-direction:column;justify-content:center;
        flex:1;padding:1rem 0}
  .oeil{font:600 10px/1.4 var(--sans);letter-spacing:.17em;text-transform:uppercase;
        display:block;margin-bottom:1rem}
  h1{margin:0 0 1rem;letter-spacing:-.025em;text-wrap:balance}
  h1 .num{font-family:var(--mono);font-weight:600;letter-spacing:-.045em;
          font-variant-numeric:tabular-nums}
  .sous{margin:0 0 1.8rem;max-width:36ch;font-size:17.5px}
  .agir{display:flex;gap:1.2rem;align-items:center;flex-wrap:wrap}
  .bouton{text-decoration:none;font:600 15px/1 var(--sans);padding:1rem 1.6rem;
          border:1px solid currentColor;display:inline-block;
          transition:background .18s ease,color .18s ease}
  .bouton:focus-visible{outline:2px solid currentColor;outline-offset:4px}
  .agir p{margin:0;font:400 13.5px/1.45 var(--sans);max-width:30ch}

  .pied{display:flex;gap:1.7rem;align-items:baseline;flex-wrap:wrap;padding:.8rem 0 .3rem;
        position:relative;z-index:3;font:400 13.5px/1.5 var(--sans)}
  .pied .prise{all:unset;cursor:pointer;white-space:nowrap;padding:.35rem .3rem;
               margin:-.35rem -.3rem;border-bottom:1px dotted currentColor}
  .pied .prise:focus-visible{outline:2px solid currentColor;outline-offset:2px}
  .pied b{font:600 15.5px/1 var(--mono);font-variant-numeric:tabular-nums}
  .pied dfn{display:none;font-style:normal;white-space:normal;font-size:12.5px;
            margin-left:.45rem}
  .pied .prise[aria-expanded="true"] dfn{display:inline}

  /* ── LA SÉQUENCE D'ENTRÉE ───────────────────────────────────────────────────
     Neuf temps décalés de cent millisecondes, chacun sous six cents : le sol s'installe,
     l'objet monte pendant que son ombre s'ouvre, le titre se découvre ligne par ligne, et
     l'appel arrive en dernier. Un fondu unique sur toute la page ne raconte rien ; c'est
     l'ORDRE qui dit ce qui compte. */
  @media (prefers-reduced-motion:no-preference){
    .ecran .plaque{opacity:0;transform:translate3d(26px,26px,0) scale(.985)}
    .ecran .socle-ombre{opacity:0;transform:scaleX(.82)}
    .ecran .ligne > i{display:block;transform:translateY(102%)}
    .ecran .oeil,.ecran .sous,.ecran .agir,.ecran .pied,.ecran .tete{opacity:0}
    .ecran .sous,.ecran .agir{transform:translateY(10px)}
    .go .plaque{opacity:1;transform:none;
      transition:opacity .5s var(--montee) .12s,transform .58s var(--montee) .12s}
    .go .socle-ombre{opacity:1;transform:none;
      transition:opacity .5s ease .22s,transform .56s var(--montee) .22s}
    .go .tete{opacity:1;transition:opacity .4s ease .05s}
    .go .oeil{opacity:1;transition:opacity .4s ease .30s}
    .go .ligne > i{transform:none;transition:transform .52s var(--montee)}
    .go .ligne:nth-child(1) > i{transition-delay:.36s}
    .go .ligne:nth-child(2) > i{transition-delay:.44s}
    .go .ligne:nth-child(3) > i{transition-delay:.52s}
    .go .sous{opacity:1;transform:none;
      transition:opacity .42s ease .60s,transform .48s var(--montee) .60s}
    .go .agir{opacity:1;transform:none;
      transition:opacity .42s ease .70s,transform .48s var(--montee) .70s}
    .go .pied{opacity:1;transition:opacity .42s ease .80s}
  }
  /* Le masque des lignes de titre n'existe QUE pour le mouvement : sans mouvement réduit il
     doit disparaître, sinon il rogne les jambages des lettres pour rien. */
  /* Un masque à ras du texte coupe les jambages de « dashboard » et de « go ». Il lui
     faut de la place sous la ligne de base, reprise ensuite en marge négative pour que
     l'interligne ne bouge pas. */
  .ligne{display:block;overflow:hidden;padding-bottom:.16em;margin-bottom:-.16em}
  @media (prefers-reduced-motion:reduce){.ligne{overflow:visible}}
"""

SUIVI = """<script>
/* ── LE POIDS DE L'OBJET ────────────────────────────────────────────────────
   Le curseur ne fait pas « bouger l'image » : il déplace la pièce de quelques pixels et
   décale son ombre EN SENS INVERSE, ce qui est ce que fait une vraie ombre portée quand on
   tourne autour d'un objet posé. Sans le décalage inverse, l'ombre suit l'objet comme un
   autocollant et tout le poids se perd.
   Le lissage est un rattrapage à chaque image plutôt qu'une transition CSS : une transition
   redémarre à chaque mouvement de souris et produit un retard élastique. */
(() => {
  const doux = matchMedia("(prefers-reduced-motion: reduce)");
  if (doux.matches) return;
  const p = document.querySelector(".plaque"), o = document.querySelector(".socle-ombre");
  if (!p) return;
  let vx = 0, vy = 0, x = 0, y = 0, tourne = false;
  addEventListener("pointermove", (e) => {
    vx = (e.clientX / innerWidth - .5) * 2;      // -1 à droite… 1 à gauche
    vy = (e.clientY / innerHeight - .5) * 2;
    if (!tourne) { tourne = true; requestAnimationFrame(boucle); }
  }, { passive: true });
  function boucle() {
    x += (vx - x) * .07; y += (vy - y) * .07;    // rattrapage : jamais de retard élastique
    p.style.transform = `translate3d(${(-x * 13).toFixed(2)}px,${(-y * 9).toFixed(2)}px,0)`;
    if (o) o.style.transform = `translate3d(${(x * 9).toFixed(2)}px,${(y * 4).toFixed(2)}px,0)`;
    if (Math.abs(vx - x) > 1e-3 || Math.abs(vy - y) > 1e-3) requestAnimationFrame(boucle);
    else tourne = false;
  }
})();

/* Une définition à la fois, repliée par défaut : une couverture qui déplie tout n'en est
   plus une. */
(() => {
  const pied = document.querySelector(".pied");
  if (!pied) return;
  pied.addEventListener("click", (e) => {
    const b = e.target.closest("button.prise"); if (!b) return;
    const ouvert = b.getAttribute("aria-expanded") === "true";
    pied.querySelectorAll('[aria-expanded="true"]').forEach((x) =>
      x.setAttribute("aria-expanded", "false"));
    b.setAttribute("aria-expanded", ouvert ? "false" : "true");
  });
})();

/* La séquence part après la première image rendue : lancée avant, les premiers temps
   passent pendant que la police charge et on ne voit que la fin. */
requestAnimationFrame(() => requestAnimationFrame(() =>
  document.body.classList.add("go")));
</script>"""


def pied(couleur_faible):
    return f"""  <div class="pied">
    <button class="prise" type="button" aria-expanded="false"><b>94.4%</b> mean of five field
      rates<dfn style="color:{couleur_faible}">— five fields measured one at a time, then
      divided by five. Not a proportion, so no interval.</dfn></button>
    <button class="prise" type="button" aria-expanded="false"><b>76.7%</b> per file · 92 of
      120<dfn style="color:{couleur_faible}">— a file counts only when all five fields are
      right together. Wilson 95% [68.3 – 83.3].</dfn></button>
    <button class="prise" type="button" aria-expanded="false"><b>17.7</b> points apart<dfn
      style="color:{couleur_faible}">— the distance between the two, over the same 120
      files.</dfn></button>
    <span style="color:{couleur_faible};white-space:normal">On your records, on your machine.
      Nothing leaves the network.</span>
  </div>"""


def page(nom, titre, css, corps):
    (BASE / nom).write_text(f"""<!doctype html>
<meta charset="utf-8"><title>{titre}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%23c98f5e'/%3E%3C/svg%3E">
<style>{COMMUN}{css}</style>
{corps}
{SUIVI}
""")
    print("  écrit :", nom)


# ── C1 · ARGILE ───────────────────────────────────────────────────────────────
# La terre cuite de l'identité, portée au fond au lieu d'être réservée aux limites. Chaude,
# franchement colorée, et l'encre y reste à plus de douze contre un.
page("C1-argile.html", "Cascade — 94 on the dashboard", """
  html{background:#c9a184}
  body{background:
        radial-gradient(64% 58% at 76% 26%, rgba(240,214,192,.72) 0%, rgba(240,214,192,0) 66%),
        linear-gradient(158deg, #e0bfa4 0%, #d3a888 46%, #bd8c6d 100%);
       background-attachment:fixed}
  .tete,.tete b{color:#43291c}
  .tete span{color:#6d4a35}
  .plaque{right:-7vw;top:8vh;width:min(60vw,900px)}
  .socle-ombre{right:-2vw;top:52vh;width:min(44vw,660px);height:12vh;
               background:radial-gradient(closest-side,rgba(58,30,14,.30),rgba(58,30,14,0))}
  .bloc{max-width:34rem}
  .oeil{color:#7d573f}
  h1{font:600 clamp(2.4rem,4.8vw,4.4rem)/1.07 var(--serif);color:#2e1b11}
  h1 .num{color:#7d2f18}
  .sous{color:#5d3f2d}
  .bouton{background:#2e1b11;color:#f0dcc9;border-color:#2e1b11}
  .bouton:hover{background:transparent;color:#2e1b11}
  .agir p{color:#6d4a35}
  .pied{color:#6d4a35;border-top:1px solid rgba(70,40,22,.28);margin-top:.4rem}
  .pied b{color:#2e1b11}
""", f"""<div class="ecran">
  <div class="tete"><b>CASCADE</b><span>routing audit — KYC extraction</span>
    <span class="d" style="color:#8a6247">report 64bdacf · measured once · frozen</span></div>
  <figure class="plaque"><img src="rendus/plaque-hero.png" alt="{ALT}"></figure>
  <span class="socle-ombre"></span>
  <div class="bloc">
    <span class="oeil">Two rates, the same 120 case files</span>
    <h1><span class="ligne"><i><span class="num">94%</span> on the dashboard.</i></span>
        <span class="ligne"><i><span class="num">77%</span> out the door.</i></span></h1>
    <p class="sous">Both are true. Only one counts a file as right when all five fields are
      right together — and only that one ever reaches your review desk.</p>
    <div class="agir"><a class="bouton" href="#">Have your routing measured</a>
      <p>If nothing comes out cheaper without breaking a file, the report says so.</p></div>
  </div>
{pied("#8a6247")}
</div>""")


# ── C2 · NUIT ─────────────────────────────────────────────────────────────────
# Le vert profond de l'identité porté au fond. C'est la seule des quatre où le métal de la
# plaque brille vraiment — un fond clair l'aplatit. Voir l'avertissement en tête de fichier.
page("C2-nuit.html", "Cascade — twenty-eight files", """
  html{background:#12211b}
  body{background:
        radial-gradient(58% 56% at 74% 30%, rgba(58,102,82,.55) 0%, rgba(58,102,82,0) 68%),
        linear-gradient(163deg, #1b3229 0%, #14251e 52%, #0e1a15 100%);
       background-attachment:fixed;color:#e7e2d4}
  .tete b{color:#e7e2d4} .tete span{color:#8fa79a}
  .plaque{right:-8vw;top:6vh;width:min(62vw,940px)}
  .socle-ombre{right:-3vw;top:52vh;width:min(46vw,700px);height:13vh;
               background:radial-gradient(closest-side,rgba(0,0,0,.55),rgba(0,0,0,0))}
  .bloc{max-width:33rem}
  .oeil{color:#7f9a8c}
  h1{font:600 clamp(2.3rem,4.5vw,4.1rem)/1.08 var(--serif);color:#f2ede0}
  h1 em{font-style:italic;color:#8fc7a8}
  .sous{color:#a9bcb1}
  .bouton{background:#e7e2d4;color:#12211b;border-color:#e7e2d4}
  .bouton:hover{background:transparent;color:#e7e2d4}
  .agir p{color:#8fa79a}
  .pied{color:#8fa79a;border-top:1px solid rgba(143,167,154,.26);margin-top:.4rem}
  .pied b{color:#f2ede0}
""", f"""<div class="ecran">
  <div class="tete"><b>CASCADE</b><span>routing audit — KYC extraction</span>
    <span class="d" style="color:#6f887b">report 64bdacf · measured once · frozen</span></div>
  <figure class="plaque"><img src="rendus/plaque-hero.png" alt="{ALT}"></figure>
  <span class="socle-ombre"></span>
  <div class="bloc">
    <span class="oeil">Finding — two rates over the same 120 files</span>
    <h1><span class="ligne"><i>Twenty-eight of <span class="num">120</span> files</i></span>
        <span class="ligne"><i>went out with <em>a field wrong</em>.</i></span>
        <span class="ligne"><i>The dashboard read <span class="num">94%</span>.</i></span></h1>
    <p class="sous">A field-by-field average and a per-file rate are not the same measurement.
      Only one of them describes what leaves your desk.</p>
    <div class="agir"><a class="bouton" href="#">Have your routing measured</a>
      <p>On your records, on your machine. Nothing leaves the network.</p></div>
  </div>
{pied("#6f887b")}
</div>""")


# ── C3 · CHAMP PARTAGÉ ────────────────────────────────────────────────────────
# La couleur n'est pas un fond mais un CHAMP : deux tiers d'olive à droite, le papier à
# gauche, et l'objet posé à cheval sur la frontière. La couleur devient une composition.
page("C3-champ.html", "Cascade — both numbers are true", """
  html{background:#e6e0cf}
  body{background:linear-gradient(178deg,#efe9da 0%,#e4ddca 100%);background-attachment:fixed}
  /* Le champ de couleur est un élément à part : il porte sa propre entrée, et l'objet peut
     passer devant lui au lieu d'être noyé dedans. */
  .champ{position:absolute;inset:0 0 4.6rem auto;width:64%;z-index:0;
         background:linear-gradient(148deg,#5c6b4a 0%,#47563a 54%,#36432c 100%);
         clip-path:polygon(14% 0,100% 0,100% 100%,0 100%)}
  @media (prefers-reduced-motion:no-preference){
    .ecran .champ{transform:translateX(3%);opacity:.9}
    .go .champ{transform:none;opacity:1;
      transition:transform .56s var(--montee),opacity .4s ease}
  }
  .tete b,.tete span{color:#3a3529}
  .plaque{right:-5vw;top:11vh;width:min(58vw,880px)}
  .socle-ombre{right:0;top:54vh;width:min(42vw,640px);height:12vh;
               background:radial-gradient(closest-side,rgba(20,26,14,.5),rgba(20,26,14,0))}
  .bloc{max-width:31rem}
  .oeil{color:#6d6752}
  h1{font:600 clamp(2.2rem,4.3vw,3.9rem)/1.08 var(--serif);color:#22261a}
  h1 .deux{display:block;color:#4b5a3b;font-style:italic}
  .sous{color:#55503f}
  .bouton{background:#22261a;color:#eee8d8;border-color:#22261a}
  .bouton:hover{background:transparent;color:#22261a}
  .agir p{color:#6d6752}
  .pied{color:#6d6752;border-top:1px solid rgba(60,56,40,.24);margin-top:.4rem}
  .pied b{color:#22261a}
""", f"""<div class="ecran">
  <span class="champ"></span>
  <div class="tete"><b>CASCADE</b><span>routing audit — KYC extraction</span>
    <span class="d" style="color:#cfd6c2">report 64bdacf · measured once · frozen</span></div>
  <figure class="plaque"><img src="rendus/plaque-hero.png" alt="{ALT}"></figure>
  <span class="socle-ombre"></span>
  <div class="bloc">
    <span class="oeil">Two rates, the same 120 case files</span>
    <h1><span class="ligne"><i>Both numbers</i></span>
        <span class="ligne"><i>are true.</i></span>
        <span class="ligne"><i class="deux">Only one leaves your desk.</i></span></h1>
    <p class="sous"><span class="num">94.4%</span> is the mean of five field rates.
      <span class="num">76.7%</span> is the share of files where all five are right together
      — 92 of 120.</p>
    <div class="agir"><a class="bouton" href="#">Have your routing measured</a>
      <p>On your records, on your machine.</p></div>
  </div>
{pied("#8b8570")}
</div>""")


# ── C4 · OCRE ─────────────────────────────────────────────────────────────────
# Rester clair, mais avec une couleur qui se voit : le fond parcourt vraiment une teinte, du
# blé au safran, au lieu de rester sur place. Le titre garde les deux chiffres à leur taille.
page("C4-ocre.html", "Cascade — 94 and 77", """
  html{background:#e8cf9e}
  body{background:
        radial-gradient(60% 62% at 78% 22%, rgba(255,244,214,.85) 0%, rgba(255,244,214,0) 62%),
        linear-gradient(154deg, #f2e2bd 0%, #ecd6a6 44%, #ddb974 100%);
       background-attachment:fixed}
  .tete b{color:#3b2f14} .tete span{color:#6d5a2c}
  .plaque{right:-6vw;top:9vh;width:min(58vw,880px)}
  .socle-ombre{right:-1vw;top:53vh;width:min(43vw,650px);height:12vh;
               background:radial-gradient(closest-side,rgba(74,52,12,.28),rgba(74,52,12,0))}
  .bloc{max-width:35rem}
  .oeil{color:#7d6832}
  h1{font:600 clamp(2rem,3.9vw,3.4rem)/1.12 var(--serif);color:#2a2110}
  /* Les deux chiffres sont ce qu'on doit retenir : ils prennent une taille à eux, et le
     reste de la phrase se range autour. */
  h1 .num{font-size:1.34em;line-height:.9}
  h1 .b{color:#8a3a12}
  .sous{color:#5b4a22}
  .bouton{background:#2a2110;color:#f6ecd2;border-color:#2a2110}
  .bouton:hover{background:transparent;color:#2a2110}
  .agir p{color:#6d5a2c}
  .pied{color:#6d5a2c;border-top:1px solid rgba(70,56,18,.26);margin-top:.4rem}
  .pied b{color:#2a2110}
""", f"""<div class="ecran">
  <div class="tete"><b>CASCADE</b><span>routing audit — KYC extraction</span>
    <span class="d" style="color:#8a7440">report 64bdacf · measured once · frozen</span></div>
  <figure class="plaque"><img src="rendus/plaque-hero.png" alt="{ALT}"></figure>
  <span class="socle-ombre"></span>
  <div class="bloc">
    <span class="oeil">Finding — two rates over the same 120 files</span>
    <h1><span class="ligne"><i>Your dashboard says <span class="num">94%</span>.</i></span>
        <span class="ligne"><i>Your case files go out</i></span>
        <span class="ligne"><i>at <span class="num b">77%</span>.</i></span></h1>
    <p class="sous">Both figures are true, and they measure different things. Only one counts
      a file as right when all five fields are right together.</p>
    <div class="agir"><a class="bouton" href="#">Have your routing measured</a>
      <p>On your records, on your machine. Nothing leaves the network.</p></div>
  </div>
{pied("#8a7440")}
</div>""")

print("\nquatre couvertures écrites")
