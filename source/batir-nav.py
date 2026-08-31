#!/usr/bin/env python3
"""Le premier écran arrêté, et quatre façons d'atteindre les autres depuis lui.

CE QU'ARSLANE A ARRÊTÉ LE 29 AOÛT
  · le titre EN GRAND À GAUCHE, occupant toute la hauteur du vert, du haut au bas ;
  · l'objet seul à droite, comme avant ;
  · la zone du dessous : le tableau, dont les visuels sont à perfectionner ;
  · le bouton, à perfectionner aussi ;
  · et depuis cet écran, on doit atteindre les autres. C'est une question d'ergonomie
    autant que de dessin, donc quatre réponses plutôt qu'une.

CE QUI VARIE, ET C'EST LÀ-DESSUS QU'ON TRANCHE
  U1 l'index en tête       les cinq constats en haut à droite, le courant souligné
  U2 la réglure du bas     une bande pleine largeur au-dessus du pied, avec l'avancement
  U3 le rail vertical      les numéros en marge gauche, à la manière d'un onglet de dossier
  U4 la pagination         « 01 sur 05 » en bas à droite, avec le titre du suivant en amorce

CE QUE LE TABLEAU A GAGNÉ
Il était trois lignes grises. Il porte maintenant l'intervalle DESSINÉ à côté du chiffre
(une moustache à l'échelle, pas un texte entre crochets), un solde à filet gras, et un état
retenu qui se voit. Le lecteur peut comparer les deux lignes sans quitter le tableau.

CE QUE LE BOUTON A GAGNÉ
Il était un rectangle noir. Il garde son poids mais gagne une flèche, un remplissage qui
entre par le côté d'où vient le curseur, et un libellé plus court : trois mots au lieu de
quatre, parce qu'un appel qui se lit en un coup d'œil se clique.
"""
import pathlib

BASE = pathlib.Path(__file__).parent

ALT = ("Six rows of chip stacks on a plate, one stack per reader and per field, each chip "
       "worth ten points of measured accuracy. The seventh row has no tiles at all: the "
       "human operator was never sampled field by field.")
LEGENDE = ("One stack per reader and per field. The empty row is the human operator, never "
           "sampled field by field.")

POSES = "\n      ".join(
    f'<img src="rendus/arc/p{i}.webp"{" class=\"vu\"" if i == 4 else ""} '
    f'{("alt=\"" + ALT + "\"" if i == 4 else "alt=\"\" aria-hidden=\"true\"")}>'
    for i in range(9))

# Les cinq écrans du rapport. Le premier est celui qu'on dessine ; les quatre autres sont
# nommés parce qu'une navigation qui ne dit pas où elle mène n'est pas une navigation.
ECRANS = [("01", "The gap"), ("02", "The cheaper routing"), ("03", "Silence over a guess"),
          ("04", "What we withhold"), ("05", "The engagement")]

# Les annexes. Elles ne sont pas des pages de bas de site : pour une banque, la méthode, la
# sécurité et la licence sont des pièces du dossier d'achat. Elles vivent dans le pied parce
# qu'on y revient, pas parce qu'on les cache.
ANNEXES = ["Method and reproducibility", "Security and data handling", "Questions",
           "Terms of engagement", "Privacy", "Accessibility"]

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
         overflow:hidden;max-width:104rem;margin:0 auto;
         padding:clamp(.8rem,1.6vh,1.25rem) clamp(1.2rem,3.4vw,3.2rem) clamp(.6rem,1.2vh,1rem)}

  /* MESURÉ, ET C'ÉTAIT LA FAUTE DE FOND. Le vert était ancré en vh (12,5 en haut, 50 en
     bas) et le titre en vw : les deux ne bougeaient pas ensemble. À 1440x900 le titre
     remplissait 94 % du vert ; à 1440x700, 121 % — il en sortait. Le bandeau rentre dans
     le flux et prend la hauteur de son titre plus une marge : « le titre va du haut du
     vert au bas du vert » devient vrai par construction, à n'importe quelle fenêtre, au
     lieu d'être vrai à une seule taille.
     La marge latérale vaut exactement 50vw, donc le titre retombe sur la colonne de la
     page ; le débord de -50vw de chaque côté garde le plein-papier. */
  .haut{position:relative;z-index:1;margin:clamp(.6rem,1.6vh,1.4rem) -50vw 0;width:200vw;
        padding:clamp(1.3rem,3vh,2.4rem) 50vw;
        display:flex;flex-direction:column;justify-content:center;
        background:linear-gradient(163deg,var(--nuit-a) 0%,var(--nuit-b) 54%,var(--nuit-c) 100%)}

  .tete{display:flex;gap:1.1rem;align-items:baseline;flex-wrap:wrap;padding-bottom:.5rem;
        position:relative;z-index:5}
  .tete b{font:600 13px/1 var(--sans);letter-spacing:.2em}
  .tete span{font-size:15px;color:var(--demi)}
  .tete .d{margin-left:auto;font:600 11px/1 var(--sans);letter-spacing:.12em;
           text-transform:uppercase;color:var(--pale)}
  .oeil{font:600 11px/1.4 var(--sans);letter-spacing:.15em;text-transform:uppercase;
        color:var(--pale);display:block;margin-top:clamp(.6rem,2vh,1.5rem);
        position:relative;z-index:5}

  /* LE TITRE. En grand à gauche, occupant toute la hauteur du vert : quatre lignes, une
     taille calée sur la largeur de la fenêtre, et la moitié droite laissée à l'objet. */
  h1{margin:0;position:relative;z-index:3;max-width:min(48vw,760px);letter-spacing:-.026em;
     font:600 min(clamp(1.9rem,5.2vw,4.7rem),7.2vh)/1.06 var(--texte);
     font-variation-settings:"opsz" 72;color:var(--sur-vert)}
  h1 .deux{color:var(--vert-vif)}
  .ligne > i{font-style:normal}

  /* L'objet, seul à droite. Il déborde du vert par le bas, sur le papier. */
  /* En vh pur, à 700 de haut l'objet remontait dans l'en-tête. Il se pose sous elle. */
  .plaque{position:absolute;right:-4vw;top:clamp(4.4rem,9vh,7rem);
          width:min(40vw,600px);margin:0;z-index:2}
  .plaque img{width:100%;display:block;opacity:0;transition:opacity .11s linear}
  .plaque img:not(:first-child){position:absolute;inset:0}
  .plaque img.vu{opacity:1}
  @media (prefers-reduced-motion:reduce){.plaque img{transition:none}}
  .socle-ombre{position:absolute;z-index:0;right:-1vw;top:calc(clamp(4.4rem,9vh,7rem) + 27vw);
               width:min(30vw,460px);height:6rem;border-radius:50%;pointer-events:none;
               background:radial-gradient(closest-side,rgba(4,10,7,.5),rgba(4,10,7,0))}
  /* La légende quitte le vert, que le titre remplit désormais : elle se pose sur le papier,
     sous l'objet, du côté où elle le regarde. */
  /* MESURÉ : posée à 53vh, elle tombait sur l'objet (haut 477, bas de l'objet 548) et se
     lisait sur son ombre. Une hauteur en vh est une hauteur devinée : l'objet est large en
     vw, donc sa hauteur ne suit pas celle de la fenêtre. La légende descend maintenant DANS
     la figure, sous l'image, et se replace toute seule à n'importe quelle taille. */
  .legende{display:block;margin:1.1rem 0 0;max-width:30ch;margin-left:auto;
           margin-right:calc(4vw + clamp(1.2rem,3.4vw,3.2rem));
           text-align:right;font:400 13px/1.5 var(--sans);color:var(--pale)}
  .legende b{color:var(--demi);font-weight:600}

  /* Posé à 51vh, il ne savait pas où le vert s'arrête. Il le suit maintenant. */
  .bas{position:relative;z-index:3;margin-top:clamp(.7rem,2vh,1.4rem);
       display:flex;flex-direction:column;gap:clamp(.5rem,1.4vh,.9rem);
       align-items:flex-start;max-width:56%}
  .sous{margin:0;font-size:16px;color:var(--demi);max-width:62ch}

  /* ── LE TABLEAU, perfectionné ────────────────────────────────────────────────
     Il était trois lignes grises et un intervalle écrit entre crochets. L'intervalle est
     maintenant DESSINÉ à l'échelle, à côté de son chiffre : une moustache se compare d'un
     regard, une paire de crochets se lit. Et la ligne qui n'en a pas montre ce vide à la
     place où l'autre a le sien. */
  .tab{width:100%;max-width:46rem;border-collapse:collapse}
  .tab caption{text-align:left;font:600 11px/1.4 var(--sans);letter-spacing:.12em;
               text-transform:uppercase;color:var(--pale);padding-bottom:.5rem}
  .tab thead th{font:600 10.5px/1.3 var(--sans);letter-spacing:.09em;text-transform:uppercase;
                color:var(--pale);text-align:right;padding:0 0 .4rem 1.1rem;
                border-bottom:1.6px solid var(--encre)}
  .tab thead th:first-child{text-align:left;padding-left:0}
  .tab tbody th{padding:0;text-align:left;border-bottom:1px solid var(--filet-clair)}
  .tab td{padding:.36rem 0 .36rem 1.1rem;text-align:right;font-family:var(--mono);font-size:16px;
          font-variant-numeric:tabular-nums;white-space:nowrap;
          border-bottom:1px solid var(--filet-clair)}
  .tab td.f{width:14rem;padding-right:.2rem}
  .sel{all:unset;cursor:pointer;display:block;padding:.4rem .3rem;margin:0 -.3rem;
       font:400 16px/1.4 var(--texte)}
  .sel small{display:block;font:400 12px/1.4 var(--sans);color:var(--pale);margin-top:.1rem}
  .tab tr[aria-selected="true"] th,.tab tr[aria-selected="true"] td{
    background:rgba(35,84,63,.13)}
  .tab tr[aria-selected="true"] th{box-shadow:inset 3px 0 0 var(--vert-titre)}
  .tab tr.cle th,.tab tr.cle td{border-bottom:none;border-top:1.6px solid var(--encre);
    padding-top:.55rem}
  .tab tr.cle td:not(.f){font-size:19px;font-weight:600;color:var(--vert-titre)}
  .tab tr.cle .sel{font-weight:600}
  /* La moustache : même échelle pour les deux lignes, sinon la comparaison est truquée. */
  .mou{width:100%;height:26px;display:block}
  .mou .ax{stroke:var(--filet-clair);stroke-width:1}
  .mou .br{stroke:var(--encre);stroke-width:1.5;fill:none}
  .mou .pt{fill:var(--encre)}
  .mou .vide{font:400 11px/1 var(--sans);fill:var(--pale);font-style:italic}
  .mou .g{font:500 9.5px/1 var(--mono);fill:var(--pale)}

  /* ── LE BOUTON, perfectionné ─────────────────────────────────────────────────
     Il garde son poids et gagne trois choses : une flèche qui dit qu'il mène quelque part,
     un remplissage qui entre par la gauche au survol plutôt qu'une disparition, et un
     libellé de trois mots. Un appel qui se lit d'un coup se clique. */
  .bouton{position:relative;overflow:hidden;isolation:isolate;text-decoration:none;
          font:600 16px/1 var(--sans);padding:.92rem 1.45rem;display:inline-flex;
          align-items:center;gap:.7rem;white-space:nowrap;
          background:var(--encre);color:#f4f0e4;border:1px solid var(--encre);
          transition:transform .16s var(--montee),box-shadow .16s ease}
  .bouton::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--vert-titre);
                  transform:scaleX(0);transform-origin:left;
                  transition:transform .26s var(--montee)}
  .bouton:hover{transform:translateY(-1px);box-shadow:0 5px 16px rgba(20,37,30,.3)}
  .bouton:hover::before{transform:scaleX(1)}
  .bouton:active{transform:translateY(1px);box-shadow:none}
  .bouton .fl{font:400 17px/1 var(--sans);transition:transform .2s var(--montee)}
  .bouton:hover .fl{transform:translateX(3px)}
  .bouton:focus-visible,.sel:focus-visible,.lien:focus-visible{outline:none;
    box-shadow:0 0 0 2px var(--papier-haut),0 0 0 4.5px var(--nuit-b)}
  .promesse{margin:0;font:400 15px/1.45 var(--texte);color:var(--demi);max-width:30ch}
  .agir{display:flex;gap:1.2rem;align-items:center;flex-wrap:wrap}

  .pied{display:flex;gap:.6rem 2rem;align-items:baseline;flex-wrap:wrap;
        padding:clamp(.45rem,1.2vh,.75rem) 0 .2rem;margin-top:auto;position:relative;z-index:5;
        font:400 clamp(12.5px,1vw,14px)/1.45 var(--sans);color:var(--pale);
        border-top:1px solid var(--filet-clair)}
  .pied .dit{color:var(--demi)} .pied b{color:var(--encre);font-weight:600}
  .annexes{display:flex;gap:clamp(.7rem,1.4vw,1.25rem);flex-wrap:wrap;margin-left:auto}
  .annexes .lien{padding:.4rem .2rem;margin:-.4rem -.2rem;color:var(--pale);
                 border-bottom:1px solid transparent}
  .annexes .lien:hover{color:var(--encre);border-bottom-color:var(--filet)}

  /* PALIER MESURÉ 1080-1360. La page dépassait de 26 à 54 px sur ce palier ; ce qui suit
     rend exactement ce qu'il fallait, sans réduire un seul corps de texte lu. */
  /* La contrainte qui cassait n'était pas la largeur mais la HAUTEUR : à 1100x740 la pile
     dépassait de 98 px alors qu'à 1152x760, vingt pixels plus haut, elle n'en dépassait
     que 57. Un palier en hauteur rend donc ce qu'un palier en largeur ne trouvait pas. */
  @media (min-width:1081px) and (max-height:840px){
    .haut{padding-top:clamp(.8rem,1.9vh,1.4rem);padding-bottom:clamp(.8rem,1.9vh,1.4rem)}
    .oeil{margin-top:.35rem}
    h1{font-size:min(clamp(1.9rem,5.2vw,4.7rem),6.9vh)}
    .tab td{padding-top:.16rem;padding-bottom:.16rem}
    .tab caption{margin-bottom:.25rem}
    .bas{gap:.38rem;margin-top:.4rem}
    .sous{font-size:15px;line-height:1.45}
    .agir{gap:.9rem}
    .tete{padding-bottom:.25rem}
    .pied{padding-top:.4rem}
    .ecran{padding-bottom:.5rem}
  }
  /* Sous 1150 les six annexes du pied passaient à la ligne : 27 px payés pour un repli. */
  @media (max-width:1150px){
    .pied{font-size:12px;gap:.4rem 1.2rem}
    .annexes{gap:.55rem}
  }

  @media (min-width:1081px) and (max-width:1360px){
    .tab td{padding-top:.22rem;padding-bottom:.22rem}
    .tab caption{margin-bottom:.3rem}
    .bas{gap:.45rem}
    .sous{font-size:15.5px}
    .nav{padding-top:.45rem}
    .agir{gap:1rem}
  }

  /* ── LA NAVIGATION. Socle commun aux quatre dispositions. ─────────────────── */
  .lien{all:unset;cursor:pointer;display:block}
  .nav .no{font:500 11px/1 var(--mono);letter-spacing:.06em}
  .nav .ti{font:400 15px/1.35 var(--texte)}
  .nav [aria-current="true"] .ti{font-weight:600}

  @media (prefers-reduced-motion:no-preference){
    .js .ecran .haut{transform:scaleY(.9);transform-origin:50% 30%;opacity:.9}
    .js .ecran .plaque{opacity:0;transform:translate3d(22px,18px,0) scale(.988)}
    .js .ecran .socle-ombre{opacity:0}
    .js .ecran .ligne > i{display:inline-block;transform:translateY(104%)}
    .js .ecran .oeil,.js .ecran .bas,.js .ecran .legende,.js .ecran .pied,
    .js .ecran .tete,.js .ecran .nav{opacity:0}
    .js .ecran .bas{transform:translateY(10px)}
    .js .go .haut{transform:none;opacity:1;
      transition:transform .6s var(--montee),opacity .4s ease}
    .js .go .plaque{opacity:1;transform:none;
      transition:opacity .5s var(--montee) .2s,transform .58s var(--montee) .2s}
    .js .go .socle-ombre{opacity:1;transition:opacity .5s ease .3s}
    .js .go .tete{opacity:1;transition:opacity .4s ease .06s}
    .js .go .oeil{opacity:1;transition:opacity .4s ease .28s}
    .js .go .ligne > i{transform:none;transition:transform .56s var(--montee)}
    .js .go .ligne:nth-of-type(1) > i{transition-delay:.3s}
    .js .go .ligne:nth-of-type(2) > i{transition-delay:.37s}
    .js .go .ligne:nth-of-type(3) > i{transition-delay:.44s}
    .js .go .ligne:nth-of-type(4) > i{transition-delay:.51s}
    .js .go .bas{opacity:1;transform:none;
      transition:opacity .42s ease .62s,transform .48s var(--montee) .62s}
    .js .go .legende{opacity:1;transition:opacity .42s ease .7s}
    .js .go .nav{opacity:1;transition:opacity .42s ease .78s}
    .js .go .pied{opacity:1;transition:opacity .42s ease .84s}
  }
  .ligne{display:inline-block;overflow:hidden;vertical-align:bottom;
         padding-bottom:.16em;margin-bottom:-.16em}
  @media (prefers-reduced-motion:reduce){.ligne{overflow:visible}}

  @media (max-width:1080px){
    .ecran{padding-bottom:0}
    .haut{position:static;inset:auto;width:auto;margin:.8rem -50vw 0;
          padding:1.4rem calc(50vw + 1.2rem) 42vh;display:block}
    h1{max-width:none;font-size:min(clamp(1.8rem,7.2vw,2.8rem),9vh);color:var(--sur-vert)}
    .plaque{right:-6vw;top:auto;bottom:1.5vh;width:min(96vw,520px);position:absolute}
    .haut{margin-left:-1.2rem;margin-right:-1.2rem;width:auto;
          padding:clamp(.9rem,2.2vh,1.4rem) 1.2rem}
    .bas{max-width:none}
    .socle-ombre,.legende{display:none}
    .bas{position:static;max-width:none;margin-top:1.2rem}
    .pied{display:none}
    .tab{max-width:none} .tab td.f{width:auto;display:none}
    .tab thead th:nth-child(2){display:none}
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
    if (o) o.style.transform = `translate3d(${(x * 8).toFixed(2)}px,0,0)`;
    if (Math.abs(vx - x) > 1e-3 || Math.abs(vy - y) > 1e-3) requestAnimationFrame(boucle);
    else tourne = false;
  }
})();

/* Le tableau : une ligne retenue à la fois. Deux mises en avant ne comparent plus. */
(() => {
  const t = document.querySelector(".tab tbody");
  if (!t) return;
  const basculer = (b) => {
    const tr = b.closest("tr"), deja = tr.getAttribute("aria-selected") === "true";
    t.querySelectorAll('[aria-selected="true"]').forEach((x) => x.setAttribute("aria-selected", "false"));
    if (!deja) tr.setAttribute("aria-selected", "true");
  };
  t.addEventListener("click", (e) => { const b = e.target.closest("button.sel"); if (b) basculer(b); });
  t.addEventListener("keydown", (e) => {
    if (e.key !== "Enter" && e.key !== " ") return;
    const b = e.target.closest("button.sel"); if (!b) return;
    e.preventDefault(); basculer(b);
  });
})();

document.fonts.ready.then(() => requestAnimationFrame(() =>
  requestAnimationFrame(() => document.body.classList.add("go"))));
</script>"""

TITRE = ('<span class="ligne"><i>Both numbers</i></span> '
         '<span class="ligne"><i>are true.</i></span> '
         '<span class="ligne"><i class="deux">Only one leaves</i></span> '
         '<span class="ligne"><i class="deux">your desk.</i></span>')
SOUS = ("94.4% is the number on your dashboard. 76.7% is the one on your desk: the share of "
        "files where all five fields are right together, 92 of 120.")
AGIR = ('<div class="agir"><a class="bouton" href="#">Measure my routing'
        '<span class="fl" aria-hidden="true">&#8594;</span></a>'
        '<p class="promesse">If nothing comes out cheaper without breaking a file, the '
        'report says so.</p></div>')
PIED = ('<div class="pied">'
        '<span class="dit">On your records, on your machine. <b>Nothing leaves the '
        'network.</b></span>'
        '<nav class="annexes" aria-label="Appendices">'
        + "".join(f'<button class="lien" type="button">{a}</button>' for a in ANNEXES)
        + '</nav></div>')

# La moustache est dessinée sur la MÊME échelle pour les deux lignes : 60 à 100 sur 210
# unités. Une échelle par ligne rendrait la comparaison fausse tout en la rendant jolie.
def X(v): return round(6 + ((v - 60) / 40) * 198, 1)

TABLEAU = f"""<table class="tab">
        <caption>Table 1, the two rates over the same 120 case files</caption>
        <thead><tr><th>Figure</th><th>95% interval</th><th>Value</th></tr></thead>
        <tbody>
          <tr aria-selected="false">
            <th><button class="sel" type="button">Mean of five field rates
              <small>not a proportion, so none can be computed</small></button></th>
            <td class="f"><svg class="mou" viewBox="0 0 210 26" role="img"
                 aria-label="No interval: a mean of rates is not a proportion.">
              <line class="ax" x1="6" y1="13" x2="204" y2="13"></line>
              <text class="vide" x="105" y="17" text-anchor="middle">no interval</text>
              <circle class="pt" cx="{X(94.4)}" cy="13" r="3.4"></circle></svg></td>
            <td>94.4%</td></tr>
          <tr aria-selected="false">
            <th><button class="sel" type="button">Per-file rate, 92 of 120
              <small>all five fields right on the same file</small></button></th>
            <td class="f"><svg class="mou" viewBox="0 0 210 26" role="img"
                 aria-label="Wilson 95% interval from 68.3 to 83.3 percent.">
              <line class="ax" x1="6" y1="13" x2="204" y2="13"></line>
              <path class="br" d="M{X(68.3)} 6 L{X(68.3)} 20 M{X(68.3)} 13 L{X(83.3)} 13 M{X(83.3)} 6 L{X(83.3)} 20"></path>
              <circle class="pt" cx="{X(76.7)}" cy="13" r="3.4"></circle>
              <text class="g" x="{X(68.3)}" y="25" text-anchor="middle">68.3</text>
              <text class="g" x="{X(83.3)}" y="25" text-anchor="middle">83.3</text></svg></td>
            <td>76.7%</td></tr>
          <tr class="cle" aria-selected="false">
            <th><button class="sel" type="button">Difference
              <small>over the same 120 case files</small></button></th>
            <td class="f"><svg class="mou" viewBox="0 0 210 26" role="img"
                 aria-label="The two rates are 17.7 points apart on the same scale.">
              <path class="br" style="stroke:#23543f"
                    d="M{X(76.7)} 17 L{X(76.7)} 11 L{X(94.4)} 11 L{X(94.4)} 17"></path>
              <text class="g" style="fill:#23543f" x="{round((X(76.7)+X(94.4))/2,1)}" y="25"
                    text-anchor="middle">17.7 points</text></svg></td>
            <td>17.7</td></tr>
        </tbody>
      </table>"""


def nav_html(disposition):
    items = "".join(
        f'<button class="lien" type="button" aria-current="{"true" if i == 0 else "false"}">'
        f'<span class="no">{no}</span><span class="ti">{ti}</span></button>'
        for i, (no, ti) in enumerate(ECRANS))
    if disposition == "pagination":
        return ('<nav class="nav" aria-label="Findings">'
                '<button class="lien prec" type="button" disabled aria-label="Previous finding">'
                '<span aria-hidden="true">&#8592;</span></button>'
                '<span class="cpt"><b>01</b> of 05</span>'
                '<button class="lien suiv" type="button">'
                '<span class="no">NEXT, 02</span><span class="ti">The cheaper routing</span>'
                '<span class="fl" aria-hidden="true">&#8594;</span></button></nav>')
    return f'<nav class="nav" aria-label="Findings">{items}</nav>'


def page(nom, titre, css, disposition, place="pied"):
    nav = nav_html(disposition)
    tete_nav = nav if place == "tete" else ""
    corps_nav = nav if place != "tete" else ""
    (BASE / nom).write_text(f"""<!doctype html>
<meta charset="utf-8"><title>{titre}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%2314251e'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<script>document.documentElement.classList.add("js")</script>
<style>{COMMUN}{css}</style>
<div class="ecran">
  <div class="tete"><b>CASCADE</b><span>routing audit, KYC extraction</span>{tete_nav}
    <span class="d">report 64bdacf, measured once and frozen</span></div>
  <span class="oeil">Finding 01, two rates over one desk</span>
  <div class="haut"><h1>{TITRE}</h1></div>
  <figure class="plaque">
      {POSES}
    <figcaption class="legende">{LEGENDE}</figcaption>
  </figure>
  <span class="socle-ombre"></span>

  <div class="bas">
    <p class="sous">{SOUS}</p>
    {TABLEAU}
    {AGIR}
  </div>
  {corps_nav}
  {PIED}
</div>
{SCRIPT}
""")
    print("  écrit :", nom)


# ── U1 · L'INDEX EN TÊTE ─────────────────────────────────────────────────────
# Les cinq constats vivent dans l'en-tête, à côté du nom. Toujours visible, jamais dans le
# chemin, et il dit dès la première seconde que le rapport a cinq parties.
page("U1-index-tete.html", "Cascade, index in the header", """
  .tete .nav{display:flex;gap:1.3rem;margin-left:2rem;align-items:baseline}
  .tete .nav .lien{display:flex;gap:.4rem;align-items:baseline;padding:.5rem .2rem;
                   margin:-.5rem -.2rem;color:var(--pale)}
  .tete .nav .no{color:var(--filet)}
  .tete .nav .ti{font-size:14px}
  .tete .nav [aria-current="true"]{color:var(--encre)}
  .tete .nav [aria-current="true"] .no{color:var(--vert-titre)}
  .tete .nav [aria-current="true"] .ti{border-bottom:1.5px solid var(--vert-titre);
                                       padding-bottom:2px}
  .tete .nav .lien:hover .ti{border-bottom:1.5px solid var(--filet);padding-bottom:2px}
  .tete .d{display:none}
  @media (max-width:1080px){.tete .nav{display:none}}
""", "index", place="tete")

# ── U2 · LA RÉGLURE DU BAS ───────────────────────────────────────────────────
# Une bande pleine largeur au-dessus du pied : les cinq constats alignés, celui qu'on lit
# marqué d'un filet plein. C'est la disposition qui montre le mieux l'AVANCEMENT.
page("U2-reglure.html", "Cascade, bottom rule", """
  .nav{position:relative;z-index:5;display:grid;grid-template-columns:repeat(5,1fr);
       gap:0;margin-top:auto;border-top:1px solid var(--filet-clair)}
  .nav .lien{display:flex;gap:.55rem;align-items:baseline;
             padding:.6rem .8rem .55rem 0;border-top:2.5px solid transparent;
             margin-top:-1.5px;color:var(--pale)}
  .nav .no{color:var(--filet)}
  .nav .ti{font-size:14px}
  .nav [aria-current="true"]{border-top-color:var(--vert-titre);color:var(--encre)}
  .nav [aria-current="true"] .no{color:var(--vert-titre)}
  .nav .lien:hover{border-top-color:var(--filet)}
  .pied{margin-top:0}
  .bas{gap:.55rem}
""", "index")

# ── U3 · LE RAIL VERTICAL ────────────────────────────────────────────────────
# Les numéros en marge gauche, comme les onglets d'un dossier suspendu. Il coûte de la
# largeur mais il tient sans rien couper, et il reste là pendant que l'écran change.
page("U3-rail.html", "Cascade, side rail", """
  .ecran{padding-left:calc(clamp(1.2rem,3.4vw,3.2rem) + 4.6rem)}
  /* MESURÉ, DEUX FOIS. Le rail traverse le vert, et son encre couleur papier y disparaît.
     Déplacer le bandeau vers la droite l'a bien sauvé, mais sa boîte de texte a gagné
     646 px au passage et le titre est tombé à 159 px de haut là où U1 en fait 317 : il ne
     remplissait plus le vert. Le bandeau garde donc sa pleine largeur et se fait DÉCOUPER
     devant le rail. Le fond de la page reparaît dans la découpe, donc il n'y a aucune
     couture de couleur à faire coïncider, et le titre retrouve sa hauteur. */
  /* La découpe part du bord GAUCHE du bandeau, qui vaut « colonne de la page moins 50vw ».
     Exprimée en 50vw + largeur du rail, elle reste juste quand la page se centre ; écrite
     avec la marge de fenêtre, elle glissait dès que .ecran atteignait sa largeur maximale. */
  .haut{clip-path:inset(0 0 0 calc(50vw + 3.4rem));padding-left:calc(50vw + 4.6rem)}
  .bas{left:calc(clamp(1.2rem,3.4vw,3.2rem) + 4.6rem)}
  .nav{position:absolute;left:0;top:0;bottom:0;z-index:6;
       width:calc(clamp(1.2rem,3.4vw,3.2rem) + 3.4rem);
       padding:12.5vh 0 0 clamp(1.2rem,3.4vw,3.2rem);
       border-right:1px solid var(--filet-clair);
       display:flex;flex-direction:column;justify-content:flex-start;gap:.1rem}
  .nav .lien{padding:.6rem .3rem;color:var(--pale);border-left:2px solid var(--filet-clair)}
  .nav .lien:first-child{border-left-color:var(--filet)}
  .nav .no{display:block}
  .nav .ti{display:none}
  .nav [aria-current="true"]{border-left-color:var(--vert-titre);color:var(--vert-titre)}
  .nav .lien:hover{border-left-color:var(--filet)}
  @media (max-width:1080px){
    .ecran{padding-left:1.2rem}
    .haut{clip-path:none;padding-left:calc(50vw + 1.2rem)}
    .bas{left:auto}
    .nav{position:static;flex-direction:row;width:auto;margin-top:.7rem;padding:0 0 .3rem;
         border-right:0;flex-wrap:nowrap;overflow-x:auto;gap:.2rem;
         scrollbar-width:none}
    .nav::-webkit-scrollbar{display:none}
    .nav .lien{white-space:nowrap;border-left:0;border-bottom:2px solid var(--filet-clair);
               padding:.35rem .55rem}
    .nav [aria-current="true"]{border-left:0;border-bottom-color:var(--vert-titre)}
    .nav .ti{display:inline;margin-left:.4rem}
  }
""", "index")

# ── U4 · LA PAGINATION ───────────────────────────────────────────────────────
# Pas d'index : un compteur et le titre du SUIVANT. On ne montre pas la table des matières,
# on montre la prochaine chose à lire. Le moins encombrant, et le moins panoramique.
page("U4-pagination.html", "Cascade, pagination", """
  .nav{position:relative;z-index:5;display:flex;align-items:center;gap:1.1rem;
       margin-top:auto;padding-top:.9rem;border-top:1px solid var(--filet-clair);
       justify-content:flex-end}
  .nav{padding-top:.7rem}
  .nav .prec{padding:.45rem .6rem;color:var(--filet);font:400 17px/1 var(--sans)}
  .nav .prec[disabled]{opacity:.4;cursor:default}
  .nav .cpt{font:500 13px/1 var(--mono);color:var(--pale);letter-spacing:.06em}
  .nav .cpt b{color:var(--encre);font-weight:600}
  .nav .suiv{display:flex;align-items:baseline;gap:.7rem;padding:.45rem .8rem;
             margin-right:-.8rem;color:var(--demi)}
  .nav .suiv .no{color:var(--vert-titre)}
  .nav .suiv .ti{font-weight:600;color:var(--encre)}
  .nav .suiv .fl{font:400 17px/1 var(--sans);transition:transform .2s var(--montee)}
  .nav .suiv:hover .fl{transform:translateX(3px)}
  .pied{margin-top:0}
  .bas{gap:.5rem}
  .sous{font-size:15.5px}
""", "pagination")

print("\nquatre navigations sur le même premier écran")
