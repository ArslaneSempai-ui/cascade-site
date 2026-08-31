#!/usr/bin/env python3
"""Le bandeau confirmé, et six façons d'occuper ce qui vit sous le vert.

CE QU'ARSLANE A CONFIRMÉ LE 29 AOÛT
  · la disposition du bandeau : papier en haut, vert en travers, papier en bas ;
  · l'objet dedans, et la police, Literata ;
  · le titre passe sur TOUTE LA LONGUEUR du vert, en une seule ligne ;
  · le texte, s'il y en a, monte le plus haut possible dans sa zone.

CE QUI VARIE, ET C'EST LÀ-DESSUS QU'ON TRANCHE
Ce qui vit SOUS le vert. Six occupations, chacune avec une idée qui lui appartient :
  N1 les cent vingt marques   compter des dossiers plutôt que lire un pourcentage
  N2 le relevé qui solde      la différence comme un solde, sous un filet gras
  N3 la réglette              l'écart comme une distance sur une échelle graduée
  N4 le tableau de rapport    assumer d'être un extrait du livrable, en-têtes compris
  N5 les deux arithmétiques   la seule qui explique POURQUOI les deux chiffres diffèrent
  N6 la fiche et l'appel      le livrable à gauche, la décision à droite

TOUT CE QUI A ÉTÉ CORRIGÉ LE 29 AOÛT EST CONSERVÉ ICI
La garde sans JavaScript inversée, `100dvh`, les deux couleurs recalculées, les prises
actionnables au clavier, le point de rupture, l'échelle typographique à trois marches, zéro
tiret cadratin. Le détail est dans `batir-six.py`, qui reste la référence de cette passe.

LE TITRE SUR UNE SEULE LIGNE
Quarante-neuf signes à traverser la page : la taille se calcule sur la largeur de la fenêtre
(3,4 vw) et non sur une valeur fixe, sinon la ligne casse à la première largeur venue. Sous
le point de rupture elle se replie normalement, parce qu'une ligne unique de quarante-neuf
signes sur un téléphone serait illisible.
"""
import pathlib

BASE = pathlib.Path(__file__).parent

ALT = ("Six rows of chip stacks on a plate, one stack per reader and per field, each chip "
       "worth ten points of measured accuracy. The seventh row has no tiles at all: the "
       "human operator was never sampled field by field.")
LEGENDE = ("One stack per reader and per field, its height the accuracy we measured. "
           "<b>The empty row is the human operator</b>, who was never sampled field by "
           "field, so the plate leaves the row open rather than filling it.")

POSES = "\n      ".join(
    f'<img src="rendus/arc/p{i}.webp"{" class=\"vu\"" if i == 4 else ""} '
    f'{("alt=\"" + ALT + "\"" if i == 4 else "alt=\"\" aria-hidden=\"true\"")}>'
    for i in range(9))

COMMUN = """
  :root{
    --papier:#dbd7c5; --papier-haut:#e2ddcb; --papier-bas:#cdccb9;
    --encre:#1b1d18; --demi:#4a4739; --pale:#55523f;
    --filet:#9d9a83; --filet-clair:#bab7a0;
    --nuit-a:#1b3229; --nuit-b:#14251e; --nuit-c:#0e1a15;
    --sur-vert:#e4ecdf; --sur-vert-pale:#a9bdaf; --vert-titre:#23543f; --vert-vif:#57b184;
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
                  var(--papier-bas) 100%)}
  .ecran{min-height:100dvh;display:flex;flex-direction:column;position:relative;
         overflow:hidden;padding:1.25rem clamp(1.2rem,3.4vw,3.2rem) 1rem;
         max-width:104rem;margin:0 auto}

  /* LE BANDEAU, DANS LE FLUX. Saigné de part et d'autre par une marge négative
     compensée en marge intérieure : le vert touche les deux bords de l'écran, et sa hauteur
     est celle de son contenu. Posé en absolu à hauteur fixe, il laissait le texte du bas
     remonter dedans dès que la zone grandissait, sombre sur sombre. */
  .haut{position:absolute;inset:13.5vh 0 44vh -50vw;width:200vw;z-index:1;
        /* La marge intérieure doit rattraper CELLE DE L'ÉCRAN en plus de la saignée,
           sinon le titre s'aligne sur le bord de la fenêtre et non sur la colonne : il
           partait 3,4 vw à gauche de tout le reste de la page. */
        padding:2.4rem calc(50vw + clamp(1.2rem,3.4vw,3.2rem)) 0;
        background:linear-gradient(163deg,var(--nuit-a) 0%,var(--nuit-b) 54%,var(--nuit-c) 100%)}

  .tete{display:flex;gap:1.1rem;align-items:baseline;flex-wrap:wrap;padding-bottom:.5rem;
        position:relative;z-index:5}
  .tete b{font:600 13px/1 var(--sans);letter-spacing:.2em}
  .tete span{font-size:15px;color:var(--demi)}
  .tete .d{margin-left:auto;font:600 11px/1 var(--sans);letter-spacing:.12em;
           text-transform:uppercase;color:var(--pale)}
  .oeil{font:600 11px/1.4 var(--sans);letter-spacing:.15em;text-transform:uppercase;
        color:var(--pale);display:block;margin-top:1.6rem;position:relative;z-index:5}

  /* LE TITRE TRAVERSE LE VERT. Une seule ligne, calée sur la largeur de la fenêtre : une
     taille fixe casserait la ligne à la première largeur venue. */
  h1{margin:0 0 1.5rem;position:relative;z-index:3;white-space:nowrap;letter-spacing:-.022em;
     font:600 3.92vw/1.16 var(--texte);font-variation-settings:"opsz" 60;color:var(--sur-vert)}
  /* 3,92 vw et non 3,4 : MESURÉ, la ligne n'occupait que 85 % de la largeur, et « sur toute
     la longueur du vert » veut dire la longueur, pas les cinq sixièmes. À 3,92 elle occupe
     98 %, ce qui laisse la marge qu'exige la variation de métrique d'une fonte à l'autre. */
  h1 .deux{color:var(--vert-vif)}
  .ligne > i{font-style:normal}

  /* L'objet déborde sous la bande, sur le papier : c'est voulu, et c'est `.ecran` qui le
     coupe au bord de l'écran. Son `right` se compte depuis le bord de la boîte saignée. */
  .plaque{position:absolute;right:46vw;top:2.6rem;width:min(41vw,620px);margin:0;z-index:2}
  .plaque img{width:100%;display:block;opacity:0;transition:opacity .11s linear}
  .plaque img:not(:first-child){position:absolute;inset:0}
  .plaque img.vu{opacity:1}
  @media (prefers-reduced-motion:reduce){.plaque img{transition:none}}
  /* La légende vit dans la bande, sous le titre, à gauche : accrochée sous l'objet elle
     tombait sur l'appel, et la moitié gauche du vert restait vide. */
  .legende{position:relative;z-index:3;margin:0;max-width:34ch;
           font:400 15px/1.5 var(--texte);color:var(--sur-vert-pale)}
  .legende b{color:var(--sur-vert);font-weight:600}
  .socle-ombre{position:absolute;z-index:0;right:48vw;top:calc(100% - 4rem);
               width:min(32vw,500px);height:7rem;
               border-radius:50%;pointer-events:none;
               background:radial-gradient(closest-side,rgba(4,10,7,.55),rgba(4,10,7,0))}

  /* SOUS LE VERT. Le texte monte en haut de sa zone, les chiffres suivent, la décision
     tient la droite. */
  /* Ancrée, comme la bande : à `margin-top:auto` elle remontait dans le vert dès qu'elle
     grandissait, et le texte passait sombre sur sombre. */
  .bas{position:absolute;left:clamp(1.2rem,3.4vw,3.2rem);right:clamp(1.2rem,3.4vw,3.2rem);
       top:57.5vh;z-index:3;display:flex;flex-direction:column;gap:.85rem;
       align-items:flex-start;max-width:62%}
  .sous{margin:0;font-size:16px;color:var(--demi);max-width:74ch}
  .agir{display:flex;gap:1.2rem;align-items:center;flex-wrap:wrap}
  .bouton{text-decoration:none;font:600 15px/1 var(--sans);padding:1rem 1.6rem;
          background:var(--encre);color:#f4f0e4;border:1px solid var(--encre);
          display:inline-block;white-space:nowrap;
          transition:transform .16s var(--montee),box-shadow .16s ease}
  .bouton:hover{transform:translateY(-1px);box-shadow:0 4px 14px rgba(20,37,30,.28)}
  .bouton:active{transform:translateY(1px);box-shadow:none}
  .bouton:focus-visible,.prise:focus-visible,.sel:focus-visible,.rg-g:focus-visible,
  .lg:focus-visible{outline:none;
    box-shadow:0 0 0 2px var(--papier-haut),0 0 0 4.5px var(--nuit-b)}
  .promesse{margin:0;font:400 15px/1.45 var(--texte);color:var(--demi);max-width:27ch}

  .pied{display:flex;gap:1.2rem;align-items:baseline;flex-wrap:wrap;padding:.75rem 0 .1rem;
        margin-top:auto;position:relative;z-index:5;font:400 15px/1.5 var(--sans);
        color:var(--pale);border-top:1px solid var(--filet-clair)}
  .pied b{color:var(--demi);font-weight:600}

  .n{font-family:var(--mono);font-variant-numeric:tabular-nums;letter-spacing:-.02em}
  .prise{all:unset;cursor:pointer;display:block}
  .vu-x{background:rgba(35,84,63,.16);box-shadow:inset 3px 0 0 var(--vert-titre)}

  /* N1 · LES CENT VINGT MARQUES */
  .grille{display:grid;grid-template-columns:repeat(30,1fr);gap:4px;margin-bottom:.6rem;
          max-width:44rem}
  .grille i{display:block;aspect-ratio:1;background:var(--encre);border-radius:1px;
            transition:opacity .2s ease}
  .grille i.k{background:transparent;box-shadow:inset 0 0 0 1.4px var(--vert-titre)}
  .grille.q-ok i.k,.grille.q-k i:not(.k){opacity:.15}
  .cles{display:flex;gap:1.2rem;flex-wrap:wrap;font:400 15px/1.5 var(--sans);color:var(--pale)}
  .lg{all:unset;cursor:pointer;display:flex;gap:.45rem;align-items:baseline;
      padding:.6rem .35rem;margin:-.4rem -.35rem}
  .cles u{width:12px;height:12px;background:var(--encre);border-radius:1px;flex:none;
          text-decoration:none;display:block;transform:translateY(1px)}
  .cles u.k{background:transparent;box-shadow:inset 0 0 0 1.4px var(--vert-titre)}
  .cles b{font:600 15px/1 var(--mono);color:var(--encre)}

  /* N2 · LE RELEVÉ QUI SOLDE */
  .solde{width:100%;max-width:40rem;border-collapse:collapse}
  .solde th{text-align:left;font:400 15px/1.35 var(--texte);padding:.1rem 0;
            border-bottom:1px solid var(--filet-clair)}
  .solde td{text-align:right;padding:.45rem 0 .45rem 1rem;font-family:var(--mono);
            font-size:15px;font-variant-numeric:tabular-nums;white-space:nowrap;
            border-bottom:1px solid var(--filet-clair)}
  .solde td.r{color:var(--pale);font-size:12px;font-family:var(--sans);white-space:normal}
  .solde tr:last-child th,.solde tr:last-child td{border-bottom:none;
    border-top:1.6px solid var(--encre);padding-top:.5rem;font-weight:600}
  .solde tr:last-child td:not(.r){font-size:18px;color:var(--vert-titre)}
  .sel{all:unset;cursor:pointer;display:block;padding:.6rem .3rem;margin:0 -.3rem;
       border-bottom:1px dotted var(--filet)}

  /* N3 · LA RÉGLETTE */
  .reglette{width:100%;max-width:44rem;margin:0}
  .reglette svg{width:100%;height:auto;display:block;overflow:visible}
  .rg-axe{stroke:var(--filet);stroke-width:1}
  .rg-t{stroke:var(--filet)} .rg-t.maj{stroke:var(--pale)}
  .rg-ch{font:500 11px/1 var(--mono);fill:var(--pale)}
  .rg-val{font:600 17px/1 var(--mono);fill:var(--encre)}
  .rg-lab{font:400 12px/1 var(--sans);fill:var(--pale)}
  .rg-aig{stroke:var(--encre);stroke-width:2.2}
  .rg-int{stroke:var(--encre);stroke-width:1.4;fill:none}
  .rg-ec{stroke:var(--vert-titre);stroke-width:1.2;fill:none}
  .rg-ect{font:600 12.5px/1 var(--mono);fill:var(--vert-titre)}
  .rg-g{cursor:pointer} .rg-g rect{fill:transparent}
  .rg-g[aria-pressed="true"] rect{fill:rgba(35,84,63,.16)}
  .efface{opacity:.32;transition:opacity .2s ease}

  /* N4 · LE TABLEAU DE RAPPORT */
  .tab{width:100%;max-width:44rem;border-collapse:collapse}
  .tab caption{text-align:left;font:600 11px/1.4 var(--sans);letter-spacing:.12em;
               text-transform:uppercase;color:var(--pale);padding-bottom:.4rem}
  .tab thead th{font:600 11px/1.3 var(--sans);letter-spacing:.08em;text-transform:uppercase;
                color:var(--pale);text-align:right;padding:0 0 .3rem 1rem;
                border-bottom:1.4px solid var(--encre)}
  .tab thead th:first-child{text-align:left;padding-left:0}
  .tab td{padding:.36rem 0 .36rem 1rem;text-align:right;font-family:var(--mono);font-size:15px;
          font-variant-numeric:tabular-nums;white-space:nowrap;
          border-bottom:1px solid var(--filet-clair)}
  .tab tbody th{padding:.1rem 0;text-align:left;font:400 15px/1.4 var(--texte);
                border-bottom:1px solid var(--filet-clair)}
  .tab td.r{color:var(--pale);font-family:var(--sans);font-size:12px;white-space:normal}
  .tab tr.cle td:not(.r){color:var(--vert-titre);font-weight:600}

  /* N5 · LES DEUX ARITHMÉTIQUES. La seule forme qui explique POURQUOI les deux chiffres
     diffèrent : cinq taux qu'on moyenne d'un côté, cent vingt dossiers qu'on compte de
     l'autre. Deux opérations, deux unités, séparées par un filet. */
  .deux-arith{display:grid;grid-template-columns:1fr 1px 1fr;gap:0 clamp(1rem,2.6vw,2.2rem);
              max-width:52rem;align-items:start}
  .deux-arith .sep{background:var(--filet-clair)}
  .deux-arith h2{margin:0 0 .35rem;font:600 11px/1.4 var(--sans);letter-spacing:.13em;
                 text-transform:uppercase;color:var(--pale)}
  .champ-l{display:grid;grid-template-columns:7.5rem 2.8rem minmax(0,1fr);gap:.55rem;
           align-items:center;padding:.24rem .3rem;margin:0 -.3rem;width:calc(100% + .6rem);
           text-align:left;transition:opacity .2s ease}
  .deux-arith.choisi .champ-l:not([aria-pressed="true"]){opacity:.34}
  .champ-l[aria-pressed="true"] .b i{background:var(--vert-titre)}
  .champ-l[aria-pressed="true"] .q,.champ-l[aria-pressed="true"] .v{font-weight:600}
  .champ-l .q{font:400 14px/1.3 var(--texte)}
  .champ-l .v{font:500 13px/1 var(--mono);font-variant-numeric:tabular-nums;text-align:right}
  .champ-l .b{height:8px;background:var(--filet-clair)}
  .champ-l .b i{display:block;height:100%;background:var(--pale)}
  .moy{display:grid;grid-template-columns:7.5rem 2.8rem minmax(0,1fr);gap:.55rem;
       align-items:baseline;border-top:1.5px solid var(--encre);margin-top:.3rem;
       padding-top:.3rem}
  .moy .q{font:600 15px/1.3 var(--texte)}
  .moy .v{font:600 17px/1 var(--mono);text-align:right}
  .moy .r{font:400 12px/1.4 var(--sans);color:var(--pale)}
  .mini{display:grid;grid-template-columns:repeat(30,1fr);gap:3px;margin:.1rem 0 .35rem}
  .mini i{display:block;aspect-ratio:1;background:var(--encre);border-radius:1px}
  .mini i.k{background:transparent;box-shadow:inset 0 0 0 1.2px var(--vert-titre)}

  /* N6 · LA FICHE ET L'APPEL */
  .fiche{max-width:36rem;border:1px solid var(--filet);background:rgba(255,252,244,.42)}
  .fiche .cart{display:flex;gap:.7rem;align-items:baseline;border-bottom:1px solid var(--filet);
               padding:.4rem .85rem;font:600 11px/1.4 var(--sans);letter-spacing:.12em;
               text-transform:uppercase;color:var(--pale)}
  .fiche .cart em{margin-left:auto;font-style:normal;font-family:var(--mono);letter-spacing:0}
  .fiche dl{margin:0;padding:.05rem .85rem .25rem}
  .fiche .l{display:grid;grid-template-columns:1fr auto;gap:.6rem;align-items:baseline;
            padding:.34rem .3rem;margin:0 -.3rem;width:calc(100% + .6rem);text-align:left;
            border-bottom:1px dotted var(--filet-clair)}
  .fiche .l:last-child{border-bottom:none}
  .fiche dt{font:400 15px/1.4 var(--texte)}
  .fiche dt small{display:block;font:400 12px/1.4 var(--sans);color:var(--pale)}
  .fiche dd{margin:0;font:600 17px/1 var(--mono);font-variant-numeric:tabular-nums}
  .fiche .cle dd{color:var(--vert-titre)}

  /* ── LA SÉQUENCE D'ENTRÉE, gardée derrière `.js` ─────────────────────────────
     Sans JavaScript rien n'est masqué : le contenu est l'état par défaut. */
  @media (prefers-reduced-motion:no-preference){
    .js .ecran .champ{transform:scaleY(.86);transform-origin:50% 20%;opacity:.88}
    .js .ecran .plaque{opacity:0;transform:translate3d(24px,20px,0) scale(.986)}
    .js .ecran .socle-ombre{opacity:0}
    .js .ecran .ligne > i{display:inline-block;transform:translateY(104%)}
    .js .ecran .oeil,.js .ecran .bas,.js .ecran .pied,.js .ecran .tete{opacity:0}
    .js .ecran .bas{transform:translateY(10px)}
    .js .go .champ{transform:none;opacity:1;
      transition:transform .58s var(--montee),opacity .4s ease}
    .js .go .plaque{opacity:1;transform:none;
      transition:opacity .5s var(--montee) .18s,transform .58s var(--montee) .18s}
    .js .go .socle-ombre{opacity:1;transition:opacity .5s ease .28s}
    .js .go .tete{opacity:1;transition:opacity .4s ease .06s}
    .js .go .oeil{opacity:1;transition:opacity .4s ease .3s}
    .js .go .ligne > i{transform:none;transition:transform .54s var(--montee)}
    .js .go .ligne:nth-of-type(1) > i{transition-delay:.36s}
    .js .go .ligne:nth-of-type(2) > i{transition-delay:.44s}
    .js .go .bas{opacity:1;transform:none;
      transition:opacity .42s ease .62s,transform .48s var(--montee) .62s}
    .js .go .pied{opacity:1;transition:opacity .42s ease .78s}
  }
  .ligne{display:inline-block;overflow:hidden;vertical-align:bottom;
         padding-bottom:.16em;margin-bottom:-.16em}
  @media (prefers-reduced-motion:reduce){.ligne{overflow:visible}}

  /* ── LE POINT DE RUPTURE. Une ligne unique de quarante-neuf signes est illisible sur un
     téléphone : sous 1200 px elle se replie, le bandeau descend, et le texte tient le
     papier. Aucune géométrie de fond ne traverse un bloc de texte. */
  @media (max-width:1200px){
    .ecran{padding-bottom:0}
    .haut{position:static;inset:auto;width:auto;margin:.8rem -50vw 0;
          padding:1.4rem 50vw 44vh}
    h1{white-space:normal;font-size:clamp(1.7rem,4.6vw,2.6rem);margin:0 0 1rem}
    h1 .deux{color:var(--vert-titre)}
    .oeil{margin-top:1.2rem}
    .plaque{right:44vw;top:auto;bottom:1.5vh;width:min(96vw,540px)}
    .legende{display:none}
    .socle-ombre{display:none}
    .bas{position:static;top:auto;max-width:none;margin-top:1.2rem}
    .agir{flex-direction:row;align-items:center;flex-wrap:wrap}
    .pied{display:none}
    .grille,.mini{grid-template-columns:repeat(15,1fr)}
    .deux-arith{grid-template-columns:1fr;gap:1.2rem}
    .deux-arith .sep{display:none}
  }
"""

SCRIPT = """<script>
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
    x += (vx - x) * .07; y += (vy - y) * .07;
    const k = Math.min(8, Math.max(0, Math.round((x + 1) / 2 * 8)));
    if (k !== pose) { poses[pose].classList.remove("vu"); poses[k].classList.add("vu"); pose = k; }
    p.style.transform = `translate3d(0,${(-y * 6).toFixed(2)}px,0)`;
    if (o) o.style.transform = `translate3d(${(x * 9).toFixed(2)}px,0,0)`;
    if (Math.abs(vx - x) > 1e-3 || Math.abs(vy - y) > 1e-3) requestAnimationFrame(boucle);
    else tourne = false;
  }
})();

/* Les prises répondent au clavier : un `<g>` de SVG ne reçoit pas de clic synthétique à
   l'appui sur Entrée, il faut poser l'écoute à la main. */
(() => {
  const z = document.querySelector(".bas");
  if (!z) return;
  const basculer = (b) => {
    const deja = b.getAttribute("aria-pressed") === "true";
    z.querySelectorAll('[aria-pressed="true"]').forEach((x) => x.setAttribute("aria-pressed", "false"));
    z.querySelectorAll(".vu-x").forEach((x) => x.classList.remove("vu-x"));
    z.querySelectorAll(".efface").forEach((x) => x.classList.remove("efface"));
    const daz = z.querySelector(".deux-arith");
    if (daz) daz.classList.remove("choisi");
    const g = z.querySelector(".grille");
    if (g) g.classList.remove("q-ok", "q-k");
    if (deja) return;
    b.setAttribute("aria-pressed", "true");
    const quoi = b.dataset.prise;
    if (!b.closest("svg")) (b.closest("tr") || b).classList.add("vu-x");
    if (g && (quoi === "ok" || quoi === "k")) g.classList.add(quoi === "ok" ? "q-ok" : "q-k");
    const da = z.querySelector(".deux-arith");
    if (da) da.classList.toggle("choisi", quoi === "c");
    if (quoi === "A" || quoi === "B")
      z.querySelectorAll(quoi === "A" ? ".rg-b" : ".rg-a").forEach((x) => x.classList.add("efface"));
  };
  z.addEventListener("click", (e) => { const b = e.target.closest("[data-prise]"); if (b) basculer(b); });
  z.addEventListener("keydown", (e) => {
    if (e.key !== "Enter" && e.key !== " ") return;
    const b = e.target.closest("[data-prise]"); if (!b) return;
    e.preventDefault(); basculer(b);
  });
})();

/* Cent vingt cases dessinées depuis les comptes : écrites à la main elles se désaccordent
   du chiffre au premier changement, et c'est alors la figure qui ment. */
(() => {
  const COMPLETS = 92, TOTAL = 120;
  for (const g of document.querySelectorAll(".grille,.mini"))
    for (let i = 0; i < TOTAL; i++) {
      const e = document.createElement("i");
      if (i >= COMPLETS) e.className = "k";
      g.appendChild(e);
    }
})();

/* La graduation vient de la même échelle que les aiguilles. */
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

document.fonts.ready.then(() => requestAnimationFrame(() =>
  requestAnimationFrame(() => document.body.classList.add("go"))));
</script>"""

OEIL = "Two rates, one desk"
TITRE = ('<span class="ligne"><i>Both numbers are true.</i></span> '
         '<span class="ligne"><i class="deux">Only one leaves your desk.</i></span>')
SOUS = ("94.4% is the number on your dashboard. 76.7% is the one on your desk: the share of "
        "files where all five fields are right together, 92 of 120.")
AGIR = ('<div class="agir"><a class="bouton" href="#">Have your routing measured</a>'
        '<p class="promesse">If nothing comes out cheaper without breaking a file, the '
        'report says so.</p></div>')
PIED = ('<div class="pied"><span>On your records, on your machine. <b>Nothing leaves the '
        'network.</b></span><span>One measurement, frozen, delivered as a report you can '
        'contest line by line.</span></div>')

BAS = {}

BAS["marques"] = """<div>
        <div class="grille" role="img"
             aria-label="120 marks, one per case file. 92 are filled: all five fields right. 28 are open: at least one field wrong."></div>
        <div class="cles">
          <button class="lg" type="button" aria-pressed="false" data-prise="ok"><u></u>
            <span><b>92</b> complete, all five fields right</span></button>
          <button class="lg" type="button" aria-pressed="false" data-prise="k"><u class="k"></u>
            <span><b>28</b> with at least one field wrong</span></button>
        </div>
      </div>"""

BAS["solde"] = """<table class="solde">
        <tbody>
          <tr><th><button class="sel" type="button" data-prise="a" aria-pressed="false">Mean of five field rates</button></th>
              <td>94.4%</td><td class="r">no interval</td></tr>
          <tr><th><button class="sel" type="button" data-prise="b" aria-pressed="false">Per-file rate, 92 of 120</button></th>
              <td>76.7%</td><td class="r">Wilson 95% [68.3 to 83.3]</td></tr>
          <tr><th>Difference</th><td>17.7</td><td class="r">points</td></tr>
        </tbody>
      </table>"""

BAS["reglette"] = """<figure class="reglette">
        <svg viewBox="0 0 620 132" role="img"
             aria-label="Scale from 50 to 100 percent. The mean of five field rates sits at 94.4, with no interval. The per-file rate sits at 76.7 with a Wilson interval from 68.3 to 83.3. The two are 17.7 points apart.">
          <g id="rg-grad"></g>
          <line class="rg-axe" x1="20" y1="34" x2="600" y2="34"></line>
          <g class="rg-g rg-b" tabindex="0" role="button" aria-pressed="false" data-prise="B"
             aria-label="Per-file rate, 76.7 percent, Wilson interval 68.3 to 83.3">
            <rect x="210" y="42" width="218" height="64"></rect>
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
            <rect x="490" y="42" width="90" height="64"></rect>
            <line class="rg-aig" x1="535" y1="52" x2="535" y2="88"></line>
            <circle cx="535" cy="70" r="4.6" fill="currentColor"></circle>
            <text class="rg-val" x="535" y="44" text-anchor="middle">94.4</text>
            <text class="rg-lab" x="535" y="100" text-anchor="middle">no interval</text>
          </g>
          <path class="rg-ec" d="M329.7 122 L329.7 116 L535 116 L535 122"></path>
          <text class="rg-ect" x="432" y="130" text-anchor="middle">17.7 points apart</text>
        </svg>
      </figure>"""

BAS["tableau"] = """<table class="tab">
        <caption>Table 1, the two rates over the same 120 case files</caption>
        <thead><tr><th>Figure</th><th>Value</th><th>Interval</th></tr></thead>
        <tbody>
          <tr><th><button class="sel" type="button" data-prise="a" aria-pressed="false">Mean of five field rates</button></th>
              <td>94.4%</td><td class="r">none, not a proportion</td></tr>
          <tr><th><button class="sel" type="button" data-prise="b" aria-pressed="false">Per-file rate, 92 of 120</button></th>
              <td>76.7%</td><td class="r">Wilson 95% [68.3 to 83.3]</td></tr>
          <tr class="cle"><th>Difference</th><td>17.7</td><td class="r">points</td></tr>
        </tbody>
      </table>"""

BAS["arith"] = """<div class="deux-arith">
        <div>
          <h2>What the dashboard averages</h2>
          <button class="champ-l prise" type="button" aria-pressed="false" data-prise="c"><span class="q">Name</span><span class="v">96.6</span>
            <span class="b"><i style="width:96.6%"></i></span></button>
          <button class="champ-l prise" type="button" aria-pressed="false" data-prise="c"><span class="q">Date of birth</span><span class="v">100</span>
            <span class="b"><i style="width:100%"></i></span></button>
          <button class="champ-l prise" type="button" aria-pressed="false" data-prise="c"><span class="q">Document no.</span><span class="v">79.7</span>
            <span class="b"><i style="width:79.7%"></i></span></button>
          <button class="champ-l prise" type="button" aria-pressed="false" data-prise="c"><span class="q">Country</span><span class="v">100</span>
            <span class="b"><i style="width:100%"></i></span></button>
          <button class="champ-l prise" type="button" aria-pressed="false" data-prise="c"><span class="q">Address</span><span class="v">95.8</span>
            <span class="b"><i style="width:95.8%"></i></span></button>
          <div class="moy"><span class="q">Mean</span><span class="v">94.4%</span>
            <span class="r">472.1 divided by 5, and a mean of rates carries no interval</span></div>
        </div>
        <span class="sep"></span>
        <div>
          <h2>What the review desk counts</h2>
          <div class="mini" role="img"
               aria-label="120 marks, one per case file. 92 filled, 28 open."></div>
          <div class="moy"><span class="q">Per file</span><span class="v">76.7%</span>
            <span class="r">92 of 120, and a proportion carries Wilson 95% [68.3 to 83.3]</span></div>
        </div>
      </div>"""

BAS["fiche"] = """<div class="fiche">
        <div class="cart"><span>Measured once, frozen</span><em>64bdacf</em></div>
        <dl>
          <button class="l prise" type="button" data-prise="a" aria-pressed="false">
            <dt>Mean of five field rates<small>not a proportion, so no interval</small></dt>
            <dd>94.4%</dd></button>
          <button class="l prise" type="button" data-prise="b" aria-pressed="false">
            <dt>Per-file rate<small>92 of 120, Wilson 95% [68.3 to 83.3]</small></dt>
            <dd>76.7%</dd></button>
          <div class="l cle"><dt>Difference<small>over the same 120 case files</small></dt>
            <dd>17.7</dd></div>
        </dl>
      </div>"""


def page(nom, titre, bas, css=""):
    (BASE / nom).write_text(f"""<!doctype html>
<meta charset="utf-8"><title>{titre}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%2314251e'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<script>document.documentElement.classList.add("js")</script>
<style>{COMMUN}{css}</style>
<div class="ecran">
  <div class="tete"><b>CASCADE</b><span>routing audit, KYC extraction</span>
    <span class="d">report 64bdacf, measured once and frozen</span></div>
  <span class="oeil">{OEIL}</span>
  <div class="haut">
    <h1>{TITRE}</h1>
    <p class="legende">{LEGENDE}</p>
    <figure class="plaque">
      {POSES}
    </figure>
    <span class="socle-ombre"></span>
  </div>
  <div class="bas">
    <p class="sous">{SOUS}</p>
    {BAS[bas]}
    {AGIR}
  </div>
  {PIED}
</div>
{SCRIPT}
""")
    print("  écrit :", nom)


page("N1-marques.html", "Cascade, 120 marks", "marques")
page("N2-solde.html", "Cascade, the balance", "solde")
page("N3-reglette.html", "Cascade, the scale", "reglette")
page("N4-tableau.html", "Cascade, Table 1", "tableau")
page("N5-arithmetiques.html", "Cascade, two arithmetics", "arith",
     # Deux colonnes de calcul demandent plus de large ET plus de haut : MESURÉ, il manquait
     # douze pixels. La zone démarre juste sous la bande au lieu d un demi-cran plus bas.
     "\n  .bas{max-width:70%;top:56.4vh;gap:.7rem}\n")
page("N6-fiche.html", "Cascade, the data card", "fiche")

print("\nsix occupations de la zone sous le vert")
