#!/usr/bin/env python3
"""Cinq fois « Field », mariées — le beige tiré du vert, cinq fontes à largeur naturelle.

CE QUI CHANGE, ET POURQUOI
1 · LA CASSURE. Le beige précédent était une crème neutre posée à côté d'un vert profond :
    deux couleurs sans parent commun, donc une rupture. Celui-ci est FABRIQUÉ à partir du
    vert — dix pour cent de #1b3229 mélangés dans la crème donnent #dbd7c5, un beige qui
    porte la même dominante. Mesuré, pas supposé : l'encre y tient 11,77 contre 1, le vert
    du titre 6,03.
    Et la coupe elle-même ne se fait plus au couteau : un masque en dégradé remplace la
    découpe nette, si bien que les deux moitiés se rejoignent sur quelques dizaines de
    pixels au lieu de se heurter.

2 · LES FONTES ÉTIRÉES. Trois des cinq précédentes étaient étroites — Archivo posée à
    `wdth 88`, Instrument Serif étroite par dessin, Fraunces déformée par `WONK`. Aucune des
    cinq ci-dessous n'est condensée, ni par dessin ni par réglage : Source Serif 4, Literata,
    Newsreader, IBM Plex Serif et EB Garamond sont toutes des fontes de lecture à largeur
    normale. C'est ce qui manquait pour que le titre tienne dans sa structure.

3 · L'OBJET TOURNE POUR DE VRAI. Le suivi du curseur déplaçait la photographie de treize
    pixels : ça donne du poids, ça ne tourne pas. La caméra a fait vingt-huit degrés d'azimut
    en neuf rendus, et le curseur choisit la pose parmi les neuf.

4 · LE TITRE EN DEUX PHRASES, la seconde en vert. La structure est désormais FIXE : ce qui
    varie d'une version à l'autre, ce sont la fonte et les deux phrases — pas la mécanique.

5 · LES CHIFFRES REMONTENT dans le bloc. Ils vivaient en pied, loin de l'argument qu'ils
    prouvent ; ils forment maintenant un relevé à trois cases sous le titre, avec ses filets.
    Le bas de la colonne gauche était vide ; il porte maintenant la preuve.
"""
import pathlib

BASE = pathlib.Path(__file__).parent

ALT = ("The measurement in relief: six rows of chip stacks on a plate, one stack per reader "
       "and per field, each chip worth ten points of measured accuracy. The seventh row has "
       "no tiles at all — the human operator was never sampled field by field.")

COMMUN = """
  :root{
    /* Le beige est tiré du vert : crème + 10 % de #1b3229. Les deux moitiés de l'écran ont
       donc la même dominante, ce qui est la condition pour qu'elles se marient. */
    --papier:#dbd7c5; --papier-haut:#e2ddcb; --papier-bas:#cdccb9;
    --encre:#1b1d18; --demi:#4a4739; --pale:#67634f; --filet:#aaa792;
    --nuit-a:#1b3229; --nuit-b:#14251e; --nuit-c:#0e1a15; --lueur:rgba(58,102,82,.55);
    --vert-clair:#cfe0d4; --vert-titre:#23543f;
    --sans:ui-sans-serif,-apple-system,"Helvetica Neue",sans-serif;
    --mono:ui-monospace,"SF Mono",Menlo,monospace;
    --montee:cubic-bezier(.16,.84,.32,1);
  }
  *{box-sizing:border-box}
  html{background:var(--papier)}
  body{margin:0;color:var(--encre);font:400 16px/1.55 var(--texte);
       -webkit-font-smoothing:antialiased;overflow-x:hidden;
       background:linear-gradient(168deg,var(--papier-haut) 0%,var(--papier) 54%,
                  var(--papier-bas) 100%);
       background-attachment:fixed}
  .ecran{min-height:100vh;display:flex;flex-direction:column;position:relative;overflow:hidden;
         padding:1.3rem clamp(1.2rem,3.6vw,3.4rem) 1.1rem;max-width:100rem;margin:0 auto}

  /* La coupe se fait au masque et non au couteau : un dégradé perpendiculaire à la diagonale
     retire l'escalier du bord sans le dissoudre — une dizaine de pixels, pas davantage.
     Ce qui adoucit la CASSURE, ce n'est pas le flou du bord : c'est le beige, qui porte
     maintenant la dominante du vert. Le flou seul avait fait disparaître le champ. */
  /* Soixante pour cent et non soixante-six : à soixante-six, le point final de « 94% »
     tombait SUR le vert. Un titre qui déborde d'un pixel sur l'autre moitié se lit comme
     une erreur de gabarit, pas comme une composition. */
  .champ{position:absolute;inset:0 0 5.4rem auto;width:60%;z-index:0;
         background:
           radial-gradient(58% 62% at 62% 26%, var(--lueur) 0%, rgba(58,102,82,0) 66%),
           linear-gradient(163deg, var(--nuit-a) 0%, var(--nuit-b) 52%, var(--nuit-c) 100%);
         -webkit-mask-image:linear-gradient(99deg, transparent 0 13%, #000 14%, #000 100%);
         mask-image:linear-gradient(99deg, transparent 0 13%, #000 14%, #000 100%)}

  .tete{display:flex;gap:1.1rem;align-items:baseline;flex-wrap:wrap;padding-bottom:.5rem;
        position:relative;z-index:4}
  .tete b{font:600 13px/1 var(--sans);letter-spacing:.2em}
  .tete span{font-size:14.5px;color:var(--demi)}
  .tete .d{margin-left:auto;font:600 10px/1 var(--sans);letter-spacing:.14em;
           text-transform:uppercase;color:var(--vert-clair)}

  /* NEUF POSES, PAS UNE IMAGE QUI GLISSE.
     Le suivi du curseur déplaçait la photographie de quelques pixels : ça donne du poids,
     mais ça ne tourne pas. Ici la caméra a réellement fait vingt-huit degrés d'azimut en
     neuf rendus, et le curseur choisit la pose. Les neuf sont recadrées sur une boîte
     COMMUNE — recadrer chacune sur la sienne ferait sauter l'objet de deux pixels d'une
     pose à l'autre, et un saut de deux pixels se voit plus qu'une rotation de trois degrés.
     La pose du milieu porte la classe `vu` dans le balisage : sans script, l'objet est là. */
  .plaque{position:absolute;margin:0;pointer-events:none;z-index:2;
          right:-6vw;top:8vh;width:min(60vw,900px)}
  .plaque img{width:100%;display:block;opacity:0;transition:opacity .11s linear}
  .plaque img:not(:first-child){position:absolute;inset:0}
  .plaque img.vu{opacity:1}
  @media (prefers-reduced-motion:reduce){.plaque img{transition:none}}
  .socle-ombre{position:absolute;z-index:1;right:0;top:53vh;width:min(42vw,640px);height:12vh;
               border-radius:50%;pointer-events:none;
               background:radial-gradient(closest-side,rgba(4,10,7,.62),rgba(4,10,7,0))}

  .bloc{position:relative;z-index:3;display:flex;flex-direction:column;justify-content:center;
        flex:1;padding:1rem 0;max-width:35rem}
  .oeil{font:600 10px/1.4 var(--sans);letter-spacing:.17em;text-transform:uppercase;
        color:var(--pale);display:block;margin-bottom:.9rem}
  h1{margin:0 0 1rem;text-wrap:balance}
  h1 .deux{color:var(--vert-titre)}
  .sous{margin:0 0 1.3rem;max-width:36ch;font-size:16.5px;color:var(--demi)}

  /* Le relevé : trois cases sous le titre, chacune une prise. Les chiffres vivaient en pied,
     à deux mètres de l'argument qu'ils prouvent — ils sont maintenant à côté de lui. */
  .releve{display:grid;grid-template-columns:auto auto auto;justify-content:start;
          gap:0 clamp(1rem,2.2vw,1.9rem);border-top:1px solid var(--filet);
          border-bottom:1px solid var(--filet);margin:0 0 1.5rem}
  .case{all:unset;cursor:pointer;padding:.65rem .3rem;display:block;position:relative}
  .case + .case::before{content:"";position:absolute;left:calc(-1 * clamp(.5rem,1.1vw,.95rem));
                        top:.55rem;bottom:.55rem;width:1px;background:var(--filet)}
  .case:focus-visible{outline:2px solid var(--vert-titre);outline-offset:-2px}
  .case b{display:block;font:600 clamp(1.25rem,1.9vw,1.6rem)/1 var(--mono);
          font-variant-numeric:tabular-nums;letter-spacing:-.02em}
  .case.cle b{color:var(--vert-titre)}
  .case i{display:block;font:400 11.5px/1.35 var(--sans);font-style:normal;color:var(--pale);
          margin-top:.3rem;max-width:19ch}
  .case dfn{display:none;font-style:normal;font:400 12px/1.4 var(--sans);color:var(--demi);
            margin-top:.35rem;max-width:24ch}
  .case[aria-expanded="true"] dfn{display:block}
  .case[aria-expanded="true"] b{text-decoration:underline;text-underline-offset:4px;
                                text-decoration-thickness:1px}

  .agir{display:flex;gap:1.2rem;align-items:center;flex-wrap:wrap}
  .bouton{text-decoration:none;font:600 15px/1 var(--sans);padding:1rem 1.6rem;
          background:var(--encre);color:#f2ede0;border:1px solid var(--encre);
          display:inline-block;transition:background .18s ease,color .18s ease}
  .bouton:hover{background:transparent;color:var(--encre)}
  .bouton:focus-visible{outline:2px solid var(--vert-titre);outline-offset:4px}
  .agir p{margin:0;font:400 13.5px/1.45 var(--sans);color:var(--pale);max-width:28ch}

  .pied{display:flex;gap:1.4rem;align-items:baseline;flex-wrap:wrap;padding:.85rem 0 .2rem;
        position:relative;z-index:4;font:400 13.5px/1.5 var(--sans);color:var(--pale);
        border-top:1px solid var(--filet)}
  .pied b{color:var(--demi);font-weight:600}

  /* ── la séquence d'entrée : neuf temps décalés, chacun sous six cents millisecondes ── */
  @media (prefers-reduced-motion:no-preference){
    .ecran .champ{transform:translateX(3.5%);opacity:.86}
    .ecran .plaque{opacity:0;transform:translate3d(26px,26px,0) scale(.985)}
    .ecran .socle-ombre{opacity:0;transform:scaleX(.82)}
    .ecran .ligne > i{display:block;transform:translateY(102%)}
    .ecran .oeil,.ecran .sous,.ecran .releve,.ecran .agir,.ecran .pied,.ecran .tete{opacity:0}
    .ecran .sous,.ecran .releve,.ecran .agir{transform:translateY(10px)}
    .go .champ{transform:none;opacity:1;
      transition:transform .56s var(--montee),opacity .4s ease}
    .go .plaque{opacity:1;transform:none;
      transition:opacity .5s var(--montee) .14s,transform .58s var(--montee) .14s}
    .go .socle-ombre{opacity:1;transform:none;
      transition:opacity .5s ease .24s,transform .56s var(--montee) .24s}
    .go .tete{opacity:1;transition:opacity .4s ease .06s}
    .go .oeil{opacity:1;transition:opacity .4s ease .32s}
    .go .ligne > i{transform:none;transition:transform .52s var(--montee)}
    .go .ligne:nth-of-type(1) > i{transition-delay:.38s}
    .go .ligne:nth-of-type(2) > i{transition-delay:.48s}
    .go .sous{opacity:1;transform:none;
      transition:opacity .42s ease .60s,transform .48s var(--montee) .60s}
    .go .releve{opacity:1;transform:none;
      transition:opacity .42s ease .70s,transform .48s var(--montee) .70s}
    .go .agir{opacity:1;transform:none;
      transition:opacity .42s ease .80s,transform .48s var(--montee) .80s}
    .go .pied{opacity:1;transition:opacity .42s ease .88s}
  }
  .ligne{display:block;overflow:hidden;padding-bottom:.16em;margin-bottom:-.16em}
  @media (prefers-reduced-motion:reduce){.ligne{overflow:visible}}
"""

SUIVI = """<script>
/* Le curseur donne son poids à la pièce : elle se déplace de quelques pixels, son ombre part
   EN SENS INVERSE. Rattrapage image par image — une transition CSS redémarrerait à chaque
   mouvement de souris et produirait un retard élastique. */
(() => {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const p = document.querySelector(".plaque"), o = document.querySelector(".socle-ombre");
  const poses = [...p.querySelectorAll("img")];
  let vx = 0, vy = 0, x = 0, y = 0, tourne = false, pose = 4;
  addEventListener("pointermove", (e) => {
    vx = (e.clientX / innerWidth - .5) * 2;
    vy = (e.clientY / innerHeight - .5) * 2;
    if (!tourne) { tourne = true; requestAnimationFrame(boucle); }
  }, { passive: true });
  function boucle() {
    /* Rattrapage image par image : une transition CSS redémarrerait à chaque mouvement de
       souris et rendrait un retard élastique. */
    x += (vx - x) * .07; y += (vy - y) * .07;
    /* La pose suit l'horizontale. Le curseur à gauche montre la face gauche : le sens est
       celui d'un objet qu'on ferait pivoter du doigt, pas celui d'une image qu'on pousse. */
    const k = Math.min(poses.length - 1, Math.max(0,
      Math.round((x + 1) / 2 * (poses.length - 1))));
    if (k !== pose) {
      poses[pose].classList.remove("vu");
      poses[k].classList.add("vu");
      pose = k;
    }
    /* La verticale reste un léger déplacement — la caméra n'a pas changé d'élévation, donc
       la faire tourner en hauteur mentirait sur ce qui a été rendu. */
    p.style.transform = `translate3d(0,${(-y * 7).toFixed(2)}px,0)`;
    o.style.transform = `translate3d(${(x * 10).toFixed(2)}px,${(y * 3).toFixed(2)}px,0)`;
    if (Math.abs(vx - x) > 1e-3 || Math.abs(vy - y) > 1e-3) requestAnimationFrame(boucle);
    else tourne = false;
  }
})();

/* Une case dépliée à la fois : trois définitions ouvertes repoussent l'appel sous le pli. */
(() => {
  const r = document.querySelector(".releve");
  r.addEventListener("click", (e) => {
    const b = e.target.closest("button.case"); if (!b) return;
    const ouvert = b.getAttribute("aria-expanded") === "true";
    r.querySelectorAll('[aria-expanded="true"]').forEach((x) =>
      x.setAttribute("aria-expanded", "false"));
    b.setAttribute("aria-expanded", ouvert ? "false" : "true");
  });
})();

/* La séquence attend les fontes : lancée avant, ses premiers temps se jouent sur une fonte
   de secours et le titre saute au milieu du mouvement. */
document.fonts.ready.then(() => requestAnimationFrame(() =>
  requestAnimationFrame(() => document.body.classList.add("go"))));
</script>"""

RELEVE = """    <div class="releve">
      <button class="case cle" type="button" aria-expanded="false"><b>17.7</b>
        <i>points apart</i><dfn>The distance between a field-by-field average and a per-file
        rate, over the same 120 files.</dfn></button>
      <button class="case" type="button" aria-expanded="false"><b>94.4%</b>
        <i>mean of five field rates</i><dfn>Five fields measured one at a time, then divided
        by five. Not a proportion, so it carries no interval.</dfn></button>
      <button class="case" type="button" aria-expanded="false"><b>76.7%</b>
        <i>per file · 92 of 120</i><dfn>A file counts only when all five fields are right
        together. Wilson 95% interval [68.3 – 83.3].</dfn></button>
    </div>"""


# Neuf poses : la cinquième (index 4) est celle du repos, et c'est elle qui porte la
# description — les huit autres sont le même objet sous un autre angle, donc muettes pour
# un lecteur d'écran, qui les entendrait sinon neuf fois.
POSES = "\n    ".join(
    f'<img src="rendus/arc/p{i}.webp"{" class=\"vu\"" if i == 4 else ""} '
    f'{"alt=\"" + ALT + "\"" if i == 4 else 'alt="" aria-hidden="true"'}>'
    for i in range(9))


def page(nom, titre, fontes, css, oeil, p1, p2, sous):
    liens = "\n".join(f'<link rel="stylesheet" href="fontes/{f}.css">' for f in fontes)
    (BASE / nom).write_text(f"""<!doctype html>
<meta charset="utf-8"><title>{titre}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%2314251e'/%3E%3C/svg%3E">
{liens}
<style>{COMMUN}{css}</style>
<div class="ecran">
  <span class="champ"></span>
  <div class="tete"><b>CASCADE</b><span>routing audit — KYC extraction</span>
    <span class="d">report 64bdacf · measured once · frozen</span></div>
  <figure class="plaque">{POSES}</figure>
  <span class="socle-ombre"></span>
  <div class="bloc">
    <span class="oeil">{oeil}</span>
    <h1><span class="ligne"><i>{p1}</i></span>
        <span class="ligne"><i class="deux">{p2}</i></span></h1>
    <p class="sous">{sous}</p>
{RELEVE}
    <div class="agir"><a class="bouton" href="#">Have your routing measured</a>
      <p>If nothing comes out cheaper without breaking a file, the report says so.</p></div>
  </div>
  <div class="pied"><span>On your records, on your machine. <b>Nothing leaves the
    network.</b></span><span>One measurement, frozen, delivered as a report you can
    contest line by line.</span></div>
</div>
{SUIVI}
""")
    print("  écrit :", nom)


# ── G1 · SOURCE SERIF 4 ───────────────────────────────────────────────────────
# Fonte de lecture d'Adobe, largeur normale, dessin sobre. Le registre le plus neutre des
# cinq : celui d'un document qu'on ne remarque pas, ce qui est une qualité pour un audit.
page("G1-source.html", "Cascade — Source Serif", ["sourceserif"], """
  :root{--texte:"Source Serif 4",Georgia,serif}
  h1{font:600 clamp(2.1rem,4.1vw,3.5rem)/1.12 "Source Serif 4",Georgia,serif;
     letter-spacing:-.018em;font-variation-settings:"opsz" 44}
""", "Two rates, the same 120 case files",
     "Your dashboard says 94%.", "Your case files go out at 77%.",
     "Both figures are true, and they measure different things. Only one counts a file as "
     "right when all five fields are right together.")

# ── G2 · LITERATA ─────────────────────────────────────────────────────────────
# Serif un peu massive, très lisible, taillée pour l'écran. Elle donne de l'assise sans
# passer par du gras — utile quand le titre doit tenir devant un objet aussi présent.
page("G2-literata.html", "Cascade — Literata", ["literata"], """
  :root{--texte:"Literata",Georgia,serif}
  h1{font:600 clamp(2rem,3.9vw,3.3rem)/1.14 "Literata",Georgia,serif;letter-spacing:-.02em;
     font-variation-settings:"opsz" 48}
""", "Two rates, the same 120 case files",
     "Both numbers are true.", "Only one leaves your desk.",
     "94.4% is the mean of five field rates. 76.7% is the share of files where all five are "
     "right together — 92 of 120.")

# ── G3 · NEWSREADER ───────────────────────────────────────────────────────────
# Serif de presse : la seule des cinq dont l'italique a du caractère. Les deux phrases y
# portent chacune un chiffre, comme deux lignes d'un chapô.
page("G3-newsreader.html", "Cascade — Newsreader", ["newsreader"], """
  :root{--texte:"Newsreader",Georgia,serif}
  h1{font:600 clamp(2.15rem,4.2vw,3.6rem)/1.11 "Newsreader",Georgia,serif;
     letter-spacing:-.022em;font-variation-settings:"opsz" 60}
""", "Two rates, the same 120 case files",
     "Five fields, averaged, come to 94%.", "Together on one file, they come to 77%.",
     "Only the second describes the unit that leaves your desk — and it is the only one of "
     "the two that carries a confidence interval.")

# ── G4 · IBM PLEX ─────────────────────────────────────────────────────────────
# Serif et sans de la même famille : le registre d'entreprise, familier à une salle de
# conformité. C'est la version qui ressemble le plus à un document qu'ils reçoivent déjà.
page("G4-plex.html", "Cascade — IBM Plex", ["plexserif", "plexsans"], """
  :root{--texte:"IBM Plex Serif",Georgia,serif;
        --sans:"IBM Plex Sans",ui-sans-serif,sans-serif}
  h1{font:600 clamp(1.95rem,3.8vw,3.2rem)/1.15 "IBM Plex Serif",Georgia,serif;
     letter-spacing:-.014em}
  .oeil{font-family:"IBM Plex Sans",sans-serif}
""", "Two rates, the same 120 case files",
     "94% is the average of five fields.", "77% is the file that leaves your desk.",
     "A mean of five rates is not a proportion, and carries no interval. A per-file rate is "
     "one, and carries a Wilson interval.")

# ── G5 · EB GARAMOND ──────────────────────────────────────────────────────────
# Old-style classique, la plus fine des cinq : le registre du document imprimé. Les deux
# phrases y sont courtes, parce que cette lettre demande de l'air.
page("G5-garamond.html", "Cascade — EB Garamond", ["garamond"], """
  :root{--texte:"EB Garamond",Georgia,serif}
  h1{font:400 clamp(2.3rem,4.6vw,4rem)/1.1 "EB Garamond",Georgia,serif;letter-spacing:-.012em}
  h1 .deux{font-style:italic}
  .sous{font-size:18px}
""", "Two rates, the same 120 case files",
     "Your dashboard reports 94%.", "Your desk receives 77%.",
     "Both are true. Only one counts a file as right when all five of its fields are right "
     "together, and that is the one your review team sees.")

print("\ncinq versions mariées")
