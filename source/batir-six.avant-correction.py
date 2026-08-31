#!/usr/bin/env python3
"""Six maquettes complètes — même idée, six géométries, six traitements des chiffres.

CE QUI EST FIXE, PARCE QUE TRANCHÉ
  · Literata, et le titre « Both numbers are true. / Only one leaves your desk. » ;
  · le beige tiré du vert (crème + 10 % de #1b3229 = #dbd7c5) : les deux moitiés partagent
    leur dominante, c'est ce qui les empêche de se heurter ;
  · la coupe est FRANCHE. J'avais essayé de l'adoucir au masque : ça n'adoucissait pas la
    cassure, ça dissolvait le champ. La cassure se règle par la couleur, pas par le flou ;
  · l'objet tourne pour de vrai — neuf poses rendues sur vingt-huit degrés d'azimut.

CE QUI VARIE, ET C'EST LÀ-DESSUS QU'ON TRANCHE
  géométrie      A diagonale · B partage vertical · C bandeau · D encart monté ·
                 E champ inversé · F double page
  les chiffres   Ils étaient trois cases grises sous le titre, et c'était mou. Six
                 traitements, chacun avec une idée : un relevé qui SOLDE · une réglette où
                 l'écart est une distance · cent vingt marques comptables · une fiche
                 technique · deux chiffres et une accolade · un tableau de rapport.

GARDÉ EN TÊTE POUR APRÈS
Les passages d'un écran à l'autre. Rien ici n'est une longue page qu'on déroule : chaque
maquette est un écran entier, et l'objet est posé en absolu pour qu'il puisse RESTER en
place pendant qu'un panneau change autour de lui. C'est la condition mécanique d'une
transition d'écran, et elle est déjà remplie.
"""
import pathlib

BASE = pathlib.Path(__file__).parent
ALT = ("The measurement in relief: six rows of chip stacks on a plate, one stack per reader "
       "and per field, each chip worth ten points of measured accuracy. The seventh row has "
       "no tiles at all — the human operator was never sampled field by field.")

POSES = "\n      ".join(
    f'<img src="rendus/arc/p{i}.webp"{" class=\"vu\"" if i == 4 else ""} '
    f'{chr(97) and ("alt=\"" + ALT + "\"" if i == 4 else "alt=\"\" aria-hidden=\"true\"")}>'
    for i in range(9))

COMMUN = """
  :root{
    --papier:#dbd7c5; --papier-haut:#e2ddcb; --papier-bas:#cdccb9;
    --encre:#1b1d18; --demi:#4a4739; --pale:#67634f; --filet:#a9a690; --filet-clair:#c2bfa9;
    --nuit-a:#1b3229; --nuit-b:#14251e; --nuit-c:#0e1a15;
    --sur-vert:#dfe8df; --sur-vert-pale:#93a89b; --vert-titre:#23543f; --vert-vif:#3f8f66;
    --sans:ui-sans-serif,-apple-system,"Helvetica Neue",sans-serif;
    --mono:ui-monospace,"SF Mono",Menlo,monospace;
    --texte:"Literata",Georgia,serif;
    --montee:cubic-bezier(.16,.84,.32,1);
  }
  *{box-sizing:border-box}
  html{background:var(--papier)}
  body{margin:0;color:var(--encre);font:400 16px/1.55 var(--texte);
       -webkit-font-smoothing:antialiased;overflow-x:hidden;
       background:linear-gradient(168deg,var(--papier-haut) 0%,var(--papier) 54%,
                  var(--papier-bas) 100%);background-attachment:fixed}
  .ecran{min-height:100vh;display:flex;flex-direction:column;position:relative;overflow:hidden;
         padding:1.25rem clamp(1.2rem,3.4vw,3.2rem) 1rem;max-width:104rem;margin:0 auto}

  /* Le champ vert. La coupe est nette : aucun dégradé, aucun masque doux. */
  .champ{position:absolute;z-index:0;
         background:linear-gradient(163deg,var(--nuit-a) 0%,var(--nuit-b) 54%,var(--nuit-c) 100%)}

  .tete{display:flex;gap:1.1rem;align-items:baseline;flex-wrap:wrap;padding-bottom:.5rem;
        position:relative;z-index:5}
  .tete b{font:600 13px/1 var(--sans);letter-spacing:.2em}
  .tete span{font-size:14.5px;color:var(--demi)}
  .tete .d{margin-left:auto;font:600 10px/1 var(--sans);letter-spacing:.14em;
           text-transform:uppercase;color:var(--pale)}

  /* NEUF POSES, recadrées sur une boîte commune : recadrer chacune sur la sienne ferait
     sauter l'objet de deux pixels, et deux pixels se voient plus que trois degrés. La pose
     du milieu porte `vu` dans le balisage — sans script, l'objet est là. */
  .plaque{position:absolute;margin:0;pointer-events:none;z-index:2}
  .plaque img{width:100%;display:block;opacity:0;transition:opacity .11s linear}
  .plaque img:not(:first-child){position:absolute;inset:0}
  .plaque img.vu{opacity:1}
  @media (prefers-reduced-motion:reduce){.plaque img{transition:none}}
  .socle-ombre{position:absolute;z-index:1;border-radius:50%;pointer-events:none;
               background:radial-gradient(closest-side,rgba(4,10,7,.55),rgba(4,10,7,0))}

  .bloc{position:relative;z-index:3;display:flex;flex-direction:column;justify-content:center;
        flex:1;padding:1rem 0}
  .oeil{font:600 10px/1.4 var(--sans);letter-spacing:.17em;text-transform:uppercase;
        color:var(--pale);display:block;margin-bottom:.9rem}
  h1{margin:0 0 .95rem;text-wrap:balance;letter-spacing:-.021em;
     font:600 clamp(1.85rem,3.5vw,3rem)/1.14 var(--texte);font-variation-settings:"opsz" 48}
  h1 .deux{color:var(--vert-titre)}
  .sous{margin:0 0 1.5rem;max-width:36ch;font-size:16px;color:var(--demi)}

  .agir{display:flex;gap:1.1rem;align-items:center;flex-wrap:wrap;margin-top:1.5rem}
  .bouton{text-decoration:none;font:600 15px/1 var(--sans);padding:1rem 1.6rem;
          background:var(--encre);color:#f2ede0;border:1px solid var(--encre);
          display:inline-block;transition:background .18s ease,color .18s ease}
  .bouton:hover{background:transparent;color:var(--encre)}
  .bouton:focus-visible{outline:2px solid var(--vert-titre);outline-offset:4px}
  .agir p{margin:0;font:400 13.5px/1.45 var(--sans);color:var(--pale);max-width:27ch}

  .pied{display:flex;gap:1.4rem;align-items:baseline;flex-wrap:wrap;padding:.8rem 0 .1rem;
        position:relative;z-index:5;font:400 13px/1.5 var(--sans);color:var(--pale);
        border-top:1px solid var(--filet-clair)}
  .pied b{color:var(--demi);font-weight:600}

  /* ── LES CHIFFRES : socle commun aux six traitements ─────────────────────── */
  .n{font-family:var(--mono);font-variant-numeric:tabular-nums;letter-spacing:-.02em}
  .prise{all:unset;cursor:pointer;display:block}
  .prise:focus-visible{outline:2px solid var(--vert-titre);outline-offset:2px}
  dfn{font-style:normal}

  /* A · LE RELEVÉ QUI SOLDE. Trois lignes dont la dernière est un solde, avec son filet
     gras : la différence n'est pas un troisième chiffre à côté des deux autres, elle est
     ce qu'ils FONT ensemble, et un livre de comptes sait dire ça depuis six siècles. */
  .solde{width:100%;max-width:33rem;border-collapse:collapse}
  .solde th{text-align:left;font:400 15px/1.35 var(--texte);padding:.42rem 0;
            border-bottom:1px solid var(--filet-clair)}
  .solde td{text-align:right;padding:.42rem 0 .42rem 1rem;border-bottom:1px solid var(--filet-clair);
            font-family:var(--mono);font-size:14.5px;font-variant-numeric:tabular-nums;
            white-space:nowrap}
  .solde td.r{color:var(--pale);font-size:11.5px;font-family:var(--sans);letter-spacing:.02em}
  .solde tr:last-child th,.solde tr:last-child td{border-bottom:none;
    border-top:1.6px solid var(--encre);padding-top:.5rem;font-weight:600}
  .solde tr:last-child th{font-size:15.5px}
  .solde tr:last-child td:not(.r){font-size:18px;color:var(--vert-titre)}
  /* La prise doit faire 24 px au doigt. Le padding sur une boîte EN LIGNE agrandit la
     cible sans toucher la hauteur de ligne, donc sans décaler le relevé. */
  .solde .sel{all:unset;cursor:pointer;border-bottom:1px dotted var(--filet);
              padding:.32rem .25rem;margin:0 -.25rem}
  .solde .sel:focus-visible{outline:2px solid var(--vert-titre);outline-offset:2px}
  .solde tr.vu th,.solde tr.vu td{background:rgba(35,84,63,.09)}

  /* B · LA RÉGLETTE. L'écart cesse d'être un nombre et devient une DISTANCE : on le mesure
     du doigt sur l'échelle au lieu de croire une soustraction sur parole. */
  .reglette{width:100%;max-width:620px}
  .reglette svg{width:100%;height:auto;display:block;overflow:visible}
  .rg-axe{stroke:var(--filet);stroke-width:1}
  .rg-t{stroke:var(--filet)} .rg-t.maj{stroke:var(--pale)}
  .rg-ch{font:500 10px/1 var(--mono);fill:var(--pale)}
  .rg-val{font:600 17px/1 var(--mono);letter-spacing:-.02em}
  .rg-lab{font:400 11px/1 var(--sans);fill:var(--pale)}
  .rg-a .rg-val{fill:var(--demi)} .rg-b .rg-val{fill:var(--encre)}
  .rg-aig{stroke-width:2.2} .rg-a .rg-aig{stroke:var(--demi)} .rg-b .rg-aig{stroke:var(--encre)}
  .rg-int{stroke:var(--encre);stroke-width:1.4;fill:none}
  .rg-ec{stroke:var(--vert-titre);stroke-width:1.2;fill:none}
  .rg-ect{font:600 12px/1 var(--mono);fill:var(--vert-titre)}
  .rg-g{cursor:pointer} .rg-g:focus-visible{outline:2px solid var(--vert-titre)}
  .efface{opacity:.3;transition:opacity .2s ease}

  /* C · LES CENT VINGT MARQUES. Un pourcentage ne se compte pas ; vingt-huit dossiers, si.
     Douze colonnes de dix, parce qu'au-delà de quatre unités personne ne compte sans
     regrouper. */
  .marques{max-width:35rem}
  .grille{display:grid;grid-template-columns:repeat(20,1fr);gap:4px;margin-bottom:.7rem}
  .grille i{display:block;aspect-ratio:1;background:var(--encre);border-radius:1px}
  .grille i.k{background:transparent;box-shadow:inset 0 0 0 1.4px var(--vert-titre)}
  .grille.q-ok i.k,.grille.q-k i:not(.k){opacity:.15}
  .grille i{transition:opacity .2s ease}
  .cles{display:flex;gap:1.4rem;flex-wrap:wrap;font:400 13px/1.5 var(--sans);color:var(--pale)}
  .cles .prise{display:flex;gap:.45rem;align-items:baseline;padding:.3rem .3rem;
               margin:-.3rem -.3rem}
  .cles u{width:11px;height:11px;background:var(--encre);border-radius:1px;text-decoration:none;
          display:block;transform:translateY(1px)}
  .cles u.k{background:transparent;box-shadow:inset 0 0 0 1.4px var(--vert-titre)}
  .cles b{font:600 15px/1 var(--mono);color:var(--encre)}

  /* D · LA FICHE. Un encadré à filets, en chiffres tabulaires, avec son cartouche : ça ne
     ressemble pas à un site, ça ressemble à ce qu'ils recevront. */
  .fiche{max-width:32rem;border:1px solid var(--filet);background:rgba(255,252,244,.42)}
  .fiche .cart{display:flex;gap:.7rem;align-items:baseline;border-bottom:1px solid var(--filet);
               padding:.45rem .8rem;font:600 9.5px/1.4 var(--sans);letter-spacing:.14em;
               text-transform:uppercase;color:var(--pale)}
  .fiche .cart em{margin-left:auto;font-style:normal;font-family:var(--mono);letter-spacing:0}
  .fiche dl{margin:0;padding:.35rem .8rem .6rem}
  .fiche .l{display:grid;grid-template-columns:1fr auto;gap:.6rem;align-items:baseline;
            padding:.4rem 0;border-bottom:1px dotted var(--filet-clair)}
  .fiche .l:last-child{border-bottom:none}
  .fiche dt{font:400 14px/1.4 var(--texte)}
  .fiche dt small{display:block;font:400 11px/1.4 var(--sans);color:var(--pale)}
  .fiche dd{margin:0;font:600 16.5px/1 var(--mono);font-variant-numeric:tabular-nums}
  .fiche .cle dd{color:var(--vert-titre)}

  /* E · DEUX CHIFFRES ET UNE ACCOLADE. La forme la plus directe : les deux nombres l'un
     sous l'autre, et l'accolade qui les prend ensemble porte leur différence. */
  .accolade{display:grid;grid-template-columns:auto 13px auto;grid-template-rows:auto auto;
            gap:.35rem .95rem;align-items:center;max-width:34rem}
  .accolade .f.a{grid-column:1;grid-row:1}
  .accolade .f.b{grid-column:1;grid-row:2}
  .accolade .f{padding:.55rem 0}
  .accolade .f b{display:block;font:600 clamp(1.7rem,2.6vw,2.3rem)/1 var(--mono);
                 letter-spacing:-.03em}
  .accolade .f i{display:block;font:400 12px/1.4 var(--sans);font-style:normal;
                 color:var(--pale);margin-top:.25rem}
  .accolade .f.a b{color:var(--demi)}
  .accolade .br{grid-column:2;grid-row:1/3;border-left:1.4px solid var(--vert-titre);
                border-top:1.4px solid var(--vert-titre);border-bottom:1.4px solid var(--vert-titre);
                border-radius:3px 0 0 3px;height:100%;width:11px;position:relative}
  .accolade .et{grid-column:3;grid-row:1/3;align-self:center;color:var(--vert-titre)}
  .accolade .et b{display:block;font:600 1.35rem/1 var(--mono);letter-spacing:-.02em}
  .accolade .et i{display:block;font:400 11.5px/1.4 var(--sans);font-style:normal;
                  color:var(--pale);margin-top:.2rem}

  /* F · LE TABLEAU DE RAPPORT. Avec ses en-têtes de colonne : la version qui assume d'être
     un extrait de document plutôt qu'un bloc de page d'accueil. */
  .tab{width:100%;max-width:36rem;border-collapse:collapse}
  .tab caption{text-align:left;font:600 9.5px/1.4 var(--sans);letter-spacing:.14em;
               text-transform:uppercase;color:var(--pale);padding-bottom:.45rem}
  .tab thead th{font:600 9.5px/1.3 var(--sans);letter-spacing:.11em;text-transform:uppercase;
                color:var(--pale);text-align:right;padding:0 0 .35rem 1rem;
                border-bottom:1.4px solid var(--encre)}
  .tab thead th:first-child{text-align:left;padding-left:0}
  .tab td,.tab tbody th{padding:.45rem 0 .45rem 1rem;text-align:right;
                        border-bottom:1px solid var(--filet-clair);font-family:var(--mono);
                        font-size:14.5px;font-variant-numeric:tabular-nums;white-space:nowrap}
  .tab tbody th{text-align:left;padding-left:0;font:400 14.5px/1.4 var(--texte)}
  .tab td.r{color:var(--pale);font-family:var(--sans);font-size:11.5px}
  .tab tr.cle td:not(.r){color:var(--vert-titre);font-weight:600}

  /* ── la séquence d'entrée : temps décalés, chacun sous six cents millisecondes ── */
  @media (prefers-reduced-motion:no-preference){
    .ecran .champ{transform:translateX(3%);opacity:.86}
    .ecran .plaque{opacity:0;transform:translate3d(24px,24px,0) scale(.986)}
    .ecran .socle-ombre{opacity:0;transform:scaleX(.82)}
    .ecran .ligne > i{display:block;transform:translateY(102%)}
    .ecran .oeil,.ecran .sous,.ecran .chiffres,.ecran .agir,.ecran .pied,.ecran .tete{opacity:0}
    .ecran .sous,.ecran .chiffres,.ecran .agir{transform:translateY(10px)}
    .go .champ{transform:none;opacity:1;transition:transform .56s var(--montee),opacity .4s ease}
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
    .go .chiffres{opacity:1;transform:none;
      transition:opacity .42s ease .70s,transform .48s var(--montee) .70s}
    .go .agir{opacity:1;transform:none;
      transition:opacity .42s ease .80s,transform .48s var(--montee) .80s}
    .go .pied{opacity:1;transition:opacity .42s ease .88s}
  }
  .ligne{display:block;overflow:hidden;padding-bottom:.16em;margin-bottom:-.16em}
  @media (prefers-reduced-motion:reduce){.ligne{overflow:visible}}
"""

SCRIPT = """<script>
/* ── LA PIÈCE TOURNE. Neuf poses rendues, le curseur en choisit une. Un déplacement de
   quelques pixels donne du poids ; il ne tourne pas. */
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
    const k = Math.min(8, Math.max(0, Math.round((x + 1) / 2 * 8)));
    if (k !== pose) { poses[pose].classList.remove("vu"); poses[k].classList.add("vu"); pose = k; }
    /* La verticale reste un déplacement : la caméra n'a pas changé d'élévation, et faire
       tourner l'objet en hauteur mentirait sur ce qui a été rendu. */
    p.style.transform = `translate3d(0,${(-y * 7).toFixed(2)}px,0)`;
    if (o) o.style.transform = `translate3d(${(x * 10).toFixed(2)}px,${(y * 3).toFixed(2)}px,0)`;
    if (Math.abs(vx - x) > 1e-3 || Math.abs(vy - y) > 1e-3) requestAnimationFrame(boucle);
    else tourne = false;
  }
})();

/* Les prises des blocs de chiffres. Une seule retenue à la fois : deux mises en avant ne
   comparent plus, elles décorent. */
(() => {
  const z = document.querySelector(".chiffres");
  if (!z) return;
  z.addEventListener("click", (e) => {
    const b = e.target.closest("[data-prise]"); if (!b) return;
    const quoi = b.dataset.prise;
    const deja = b.getAttribute("aria-pressed") === "true";
    z.querySelectorAll('[aria-pressed="true"]').forEach((x) => x.setAttribute("aria-pressed", "false"));
    z.querySelectorAll(".vu").forEach((x) => x.classList.remove("vu"));
    z.querySelectorAll(".efface").forEach((x) => x.classList.remove("efface"));
    const g = document.querySelector(".grille");
    if (g) g.classList.remove("q-ok", "q-k");
    if (deja) return;
    b.setAttribute("aria-pressed", "true");
    const tr = b.closest("tr"); if (tr) tr.classList.add("vu");
    if (g && quoi) g.classList.add(quoi === "ok" ? "q-ok" : "q-k");
    if (quoi === "A" || quoi === "B") {
      const autre = quoi === "A" ? ".rg-b" : ".rg-a";
      document.querySelectorAll(autre).forEach((x) => x.classList.add("efface"));
    }
  });
})();

/* La séquence attend les fontes : lancée avant, ses premiers temps se jouent sur une fonte
   de secours et le titre saute au milieu du mouvement. */
document.fonts.ready.then(() => requestAnimationFrame(() =>
  requestAnimationFrame(() => document.body.classList.add("go"))));
</script>"""

TITRE_H1 = ('<span class="ligne"><i>Both numbers are true.</i></span>'
            '<span class="ligne"><i class="deux">Only one leaves your desk.</i></span>')
SOUS = ("94.4% is the mean of five field rates. 76.7% is the share of files where all five "
        "are right together — 92 of 120.")
AGIR = ('<div class="agir"><a class="bouton" href="#">Have your routing measured</a>'
        '<p>If nothing comes out cheaper without breaking a file, the report says so.</p></div>')
PIED = ('<div class="pied"><span>On your records, on your machine. <b>Nothing leaves the '
        'network.</b></span><span>One measurement, frozen, delivered as a report you can '
        'contest line by line.</span></div>')


# ── les six traitements des chiffres ─────────────────────────────────────────
INFO = {}

INFO["solde"] = """<table class="solde">
        <tbody>
          <tr><th><button class="sel" type="button" data-prise="">Mean of five field rates</button></th>
              <td>94.4%</td><td class="r">no interval</td></tr>
          <tr><th><button class="sel" type="button" data-prise="">Per-file rate · 92 of 120</button></th>
              <td>76.7%</td><td class="r">Wilson 95% [68.3 – 83.3]</td></tr>
          <tr><th>Difference</th><td>17.7</td><td class="r">points</td></tr>
        </tbody>
      </table>"""

INFO["reglette"] = """<figure class="reglette" style="margin:0">
        <svg viewBox="0 0 620 132" role="img"
             aria-label="Scale from 50 to 100 percent. The mean of five field rates sits at 94.4, with no interval. The per-file rate sits at 76.7 with a Wilson interval from 68.3 to 83.3. The two are 17.7 points apart.">
          <g id="rg-grad"></g>
          <line class="rg-axe" x1="20" y1="34" x2="600" y2="34"></line>
          <g class="rg-g rg-b" tabindex="0" role="button" aria-pressed="false" data-prise="B"
             aria-label="Per-file rate, 76.7 percent, Wilson interval 68.3 to 83.3">
            <path class="rg-int" d="M232.3 58 L232.3 82 M232.3 70 L406.3 70 M406.3 58 L406.3 82"></path>
            <line class="rg-aig" x1="329.7" y1="52" x2="329.7" y2="88"></line>
            <circle cx="329.7" cy="70" r="4.6" fill="currentColor"></circle>
            <text class="rg-val" x="329.7" y="44" text-anchor="middle">76.7</text>
            <text class="rg-lab" x="232.3" y="100" text-anchor="middle">68.3</text>
            <text class="rg-lab" x="406.3" y="100" text-anchor="middle">83.3</text>
            <text class="rg-lab" x="424" y="100">Wilson 95%</text>
          </g>
          <g class="rg-g rg-a" tabindex="0" role="button" aria-pressed="false" data-prise="A"
             aria-label="Mean of five field rates, 94.4 percent, no interval">
            <line class="rg-aig" x1="535" y1="52" x2="535" y2="88"></line>
            <circle cx="535" cy="70" r="4.6" fill="currentColor"></circle>
            <text class="rg-val" x="535" y="44" text-anchor="middle">94.4</text>
            <text class="rg-lab" x="535" y="100" text-anchor="middle">no interval</text>
          </g>
          <path class="rg-ec" d="M329.7 122 L329.7 116 L535 116 L535 122"></path>
          <text class="rg-ect" x="432" y="130" text-anchor="middle">17.7 points apart</text>
        </svg>
      </figure>"""

INFO["marques"] = """<div class="marques">
        <div class="grille" id="grille"></div>
        <div class="cles">
          <button class="prise" type="button" aria-pressed="false" data-prise="ok"><u></u>
            <span><b>92</b> complete — all five fields right</span></button>
          <button class="prise" type="button" aria-pressed="false" data-prise="k"><u class="k"></u>
            <span><b>28</b> with at least one field wrong</span></button>
          <span style="align-self:center"><b class="n" style="color:var(--vert-titre);
            font:600 15px/1 var(--mono)">76.7%</b> per file · 120 in the corpus</span>
        </div>
      </div>"""

INFO["fiche"] = """<div class="fiche">
        <div class="cart"><span>Measured once · frozen</span><em>64bdacf</em></div>
        <dl>
          <div class="l"><dt>Mean of five field rates<small>not a proportion · no interval</small></dt>
            <dd>94.4%</dd></div>
          <div class="l"><dt>Per-file rate<small>92 of 120 · Wilson 95% [68.3 – 83.3]</small></dt>
            <dd>76.7%</dd></div>
          <div class="l cle"><dt>Difference<small>over the same 120 case files</small></dt>
            <dd>17.7</dd></div>
        </dl>
      </div>"""

INFO["accolade"] = """<div class="accolade">
        <div class="f a"><b>94.4%</b><i>mean of five field rates · no interval</i></div>
        <span class="br"></span>
        <div class="et"><b>17.7</b><i>points apart</i></div>
        <div class="f b"><b>76.7%</b><i>per file · 92 of 120 · Wilson [68.3 – 83.3]</i></div>
      </div>"""

INFO["tableau"] = """<table class="tab">
        <caption>Table 1 — the two rates, over the same 120 case files</caption>
        <thead><tr><th>Figure</th><th>Value</th><th>Interval</th></tr></thead>
        <tbody>
          <tr><th>Mean of five field rates</th><td>94.4%</td><td class="r">none — not a proportion</td></tr>
          <tr><th>Per-file rate · 92 of 120</th><td>76.7%</td><td class="r">Wilson 95% [68.3 – 83.3]</td></tr>
          <tr class="cle"><th>Difference</th><td>17.7</td><td class="r">points</td></tr>
        </tbody>
      </table>"""

GRILLE_JS = """<script>
/* Cent vingt cases dessinées depuis les comptes : écrites à la main, elles se désaccordent
   du chiffre au premier changement, et c'est alors la figure qui ment. */
(() => {
  const g = document.getElementById("grille"); if (!g) return;
  const COMPLETS = 92, TOTAL = 120;
  for (let i = 0; i < TOTAL; i++) {
    const e = document.createElement("i");
    if (i >= COMPLETS) e.className = "k";
    g.appendChild(e);
  }
})();
</script>"""

REGLETTE_JS = """<script>
/* La graduation vient de la même échelle que les aiguilles. Écrite à la main, elle se
   désaccorde dès qu'une borne bouge — et c'est l'échelle qui ment. */
(() => {
  const g = document.getElementById("rg-grad"); if (!g) return;
  const X = (v) => 20 + ((v - 50) / 50) * 580;
  const ns = "http://www.w3.org/2000/svg";
  for (let v = 50; v <= 100 + 1e-9; v += 2.5) {
    const maj = Math.abs(v % 10) < 1e-9;
    const l = document.createElementNS(ns, "line");
    l.setAttribute("class", "rg-t" + (maj ? " maj" : ""));
    l.setAttribute("x1", X(v)); l.setAttribute("x2", X(v));
    l.setAttribute("y1", maj ? 20 : 27); l.setAttribute("y2", 34);
    g.appendChild(l);
    if (maj) {
      const t = document.createElementNS(ns, "text");
      t.setAttribute("class", "rg-ch"); t.setAttribute("x", X(v)); t.setAttribute("y", 13);
      t.setAttribute("text-anchor", "middle");
      t.textContent = v === 100 ? "100%" : String(v);
      g.appendChild(t);
    }
  }
})();
</script>"""


def page(nom, titre, geo_css, info, extra_js="", corps_extra="", tete_d="var(--pale)"):
    (BASE / nom).write_text(f"""<!doctype html>
<meta charset="utf-8"><title>{titre}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%2314251e'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<style>{COMMUN}{geo_css}</style>
<div class="ecran">
  <span class="champ"></span>{corps_extra}
  <div class="tete"><b>CASCADE</b><span>routing audit — KYC extraction</span>
    <span class="d" style="color:{tete_d}">report 64bdacf · measured once · frozen</span></div>
  <figure class="plaque">
      {POSES}
  </figure>
  <span class="socle-ombre"></span>
  <div class="bloc">
    <span class="oeil">Two rates, the same 120 case files</span>
    <h1>{TITRE_H1}</h1>
    <p class="sous">{SOUS}</p>
    <div class="chiffres">
      {INFO[info]}
    </div>
    {AGIR}
  </div>
  {PIED}
</div>
{SCRIPT}
{extra_js}
""")
    print("  écrit :", nom)


# ── A · LA DIAGONALE ─────────────────────────────────────────────────────────
page("M1-diagonale.html", "Cascade — diagonal field", """
  .champ{inset:0 0 4.9rem auto;width:59%;clip-path:polygon(14% 0,100% 0,100% 100%,0 100%)}
  .plaque{right:-5vw;top:8vh;width:min(58vw,880px)}
  .socle-ombre{right:0;top:53vh;width:min(40vw,620px);height:12vh}
  .bloc{max-width:35rem}
""", "solde")

# ── B · LE PARTAGE VERTICAL ──────────────────────────────────────────────────
# La coupe droite est plus calme que la diagonale : elle laisse toute la place à la réglette,
# qui a besoin d'une largeur franche pour que l'écart se mesure du doigt.
page("M2-vertical.html", "Cascade — vertical split", """
  .champ{inset:0 0 0 auto;width:54%}
  .plaque{right:-4vw;top:11vh;width:min(56vw,860px)}
  .socle-ombre{right:1vw;top:56vh;width:min(38vw,580px);height:11vh}
  .bloc{max-width:39rem;padding-right:2rem}
  .pied{border-top-color:var(--filet-clair)}
""", "reglette", REGLETTE_JS)

# ── C · LE BANDEAU ───────────────────────────────────────────────────────────
# Le vert traverse l'écran en bande : le titre est posé dessus en clair, l'objet dedans, et
# les chiffres restent sur le papier en dessous. La géométrie la plus éloignée des autres.
page("M3-bandeau.html", "Cascade — band", """
  .champ{inset:22vh 0 34vh -50vw;width:200vw}
  .plaque{right:-3vw;top:9vh;width:min(52vw,800px)}
  .socle-ombre{right:2vw;top:52vh;width:min(34vw,520px);height:10vh}
  .bloc{max-width:34rem;justify-content:flex-start;padding-top:23.5vh}
  .oeil{color:var(--sur-vert-pale)}
  h1{color:var(--sur-vert)}
  h1 .deux{color:var(--vert-vif)}
  .sous{color:var(--sur-vert-pale);margin-bottom:0}
  .chiffres{position:absolute;left:clamp(1.2rem,3.4vw,3.2rem);bottom:5.4rem;z-index:4}
  .agir{position:absolute;left:clamp(1.2rem,3.4vw,3.2rem);bottom:1.1rem;margin:0;z-index:4}
  .agir p{display:none}
  .pied{display:none}
""", "marques", GRILLE_JS, tete_d="var(--pale)")

# ── D · L'ENCART MONTÉ ───────────────────────────────────────────────────────
# Le vert n'est plus une moitié d'écran mais une PLANCHE montée, avec sa marge de papier tout
# autour. L'objet déborde de son coin : c'est ce débordement qui empêche l'encart de ressembler
# à une image collée.
page("M4-encart.html", "Cascade — mounted plate", """
  .champ{inset:6.5rem 2.6rem 5.6rem 42%;border:1px solid rgba(20,37,30,.5)}
  .plaque{right:-1vw;top:4vh;width:min(52vw,800px)}
  .socle-ombre{right:3vw;top:51vh;width:min(34vw,520px);height:10vh}
  .bloc{max-width:33rem}
""", "fiche")

# ── E · LE CHAMP INVERSÉ ─────────────────────────────────────────────────────
# Le vert prend la GAUCHE et porte le titre en clair ; l'objet reste à droite, sur le papier.
# La valeur s'inverse, et l'objet cesse d'être devant un fond sombre pour être posé sur la table.
page("M5-inverse.html", "Cascade — inverted field", """
  .champ{inset:0 auto 0 0;width:46%;clip-path:polygon(0 0,100% 0,86% 100%,0 100%)}
  .plaque{right:-6vw;top:12vh;width:min(56vw,860px)}
  .socle-ombre{right:0;top:57vh;width:min(38vw,580px);height:11vh;
               background:radial-gradient(closest-side,rgba(60,52,30,.30),rgba(60,52,30,0))}
  .bloc{max-width:31rem}
  .oeil{color:var(--sur-vert-pale)}
  h1{color:var(--sur-vert)}
  h1 .deux{color:var(--vert-vif)}
  .sous{color:var(--sur-vert-pale)}
  .accolade .f i{color:var(--sur-vert-pale)}
  .accolade .f.a b{color:#a8bcae} .accolade .f.b b{color:var(--sur-vert)}
  .accolade .br{border-color:var(--vert-vif)}
  .accolade .et{color:var(--vert-vif)} .accolade .et i{color:var(--sur-vert-pale)}
  .bouton{background:var(--sur-vert);color:var(--nuit-b);border-color:var(--sur-vert)}
  .bouton:hover{background:transparent;color:var(--sur-vert)}
  .agir p{color:var(--sur-vert-pale)}
  .tete b,.tete span{color:var(--sur-vert)}
""", "accolade", tete_d="var(--pale)")

# ── F · LA DOUBLE PAGE ───────────────────────────────────────────────────────
# Un filet vertical au milieu et deux folios : la mise en page d'un rapport ouvert. Le vert
# tient la page de droite entière, l'objet y est monté comme une planche hors-texte.
page("M6-double.html", "Cascade — spread", """
  .champ{inset:0 0 0 50%}
  .couture{position:absolute;left:50%;top:0;bottom:0;width:1px;
           background:rgba(20,37,30,.28);z-index:4}
  .folio{position:absolute;bottom:1.1rem;font:500 10px/1 var(--mono);letter-spacing:.14em;
         color:var(--pale);z-index:5}
  .folio.g{display:none}   /* il tombait dans le pied de page : deux textes au même endroit */
  .folio.d{right:clamp(1.2rem,3.4vw,3.2rem);color:var(--sur-vert-pale)}
  .plaque{right:-4vw;top:13vh;width:min(50vw,760px)}
  .socle-ombre{right:1vw;top:58vh;width:min(34vw,520px);height:10vh}
  .bloc{max-width:38rem;padding-right:3rem}
  .pied{width:52%;padding-bottom:.6rem}
""", "tableau", "", corps_extra=('<span class="couture"></span>'
                                 '<span class="folio g">FINDING 01</span>'
                                 '<span class="folio d">PLATE 1 — ACCURACY BY READER AND FIELD</span>'))

print("\nsix maquettes")
