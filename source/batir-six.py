#!/usr/bin/env python3
"""Six maquettes d'écran d'accueil pour cascade, après la passe de correction groupée.

CE QUI EST FIXE, PARCE QUE TRANCHÉ
  · Literata, et le titre en deux phrases dont la seconde en vert ;
  · le beige tiré du vert (crème + 10 % de #1b3229 = #dbd7c5) : les deux moitiés partagent
    leur dominante, c'est ce qui les empêche de se heurter ;
  · la coupe est FRANCHE. Adoucir au masque ne rapprochait pas les deux moitiés, ça
    dissolvait le champ ;
  · l'objet tourne pour de vrai, neuf poses rendues sur vingt-huit degrés d'azimut.

CE QUI VARIE, ET C'EST LÀ-DESSUS QU'ON TRANCHE
  géométrie      A diagonale · B partage vertical · C bandeau · D encart monté ·
                 E champ inversé · F double page
  les chiffres   six formes, chacune avec une idée : un relevé qui SOLDE · une réglette où
                 l'écart est une distance · cent vingt marques comptables · une fiche
                 technique · deux chiffres et une accolade · un tableau de rapport.

────────────────────────────────────────────────────────────────────────────────────────
LA PASSE DE CORRECTION DU 29 AOÛT

Deux évaluations indépendantes (revue de design à l'aveugle d'un côté, détecteur mécanique
et mesures de l'autre) plus les interdits de `taste-skill`. Corrigé en UNE passe et non en
douze retouches. Les six qui comptent :

1 · SANS JAVASCRIPT, LA PAGE ÉTAIT VIDE. Le bloc d'animation mettait tout à `opacity:0` et
    seule une classe posée par le script rétablissait. Mesuré ET regardé : deux rectangles,
    un beige un vert, rien d'autre. Une politique de sécurité qui bloque le script en
    ligne, un poste administré, un 404 sur la feuille de fontes : trois chemins vers le
    même écran blanc. La garde est INVERSÉE : le contenu est l'état par défaut, et un
    script synchrone dans l'en-tête pose `.js` pour AUTORISER l'animation.
    Ce défaut ne s'est vu sur aucune capture parce qu'aucun contrôle ne coupait le script.

2 · LE TITRE ÉTAIT EN ITALIQUE PAR ACCIDENT, ET EN FAUX GRAS. Le `<i>` que j'emploie comme
    enveloppe d'animation est un élément italique et je n'avais pas remis `font-style` à
    zéro dessus, alors que je le fais à quatre autres endroits du même fichier. Literata ne
    livrant l'italique qu'en 400 pour un titre demandé en 600, le navigateur SYNTHÉTISAIT
    le gras. Six titres en faux oblique, sur une page qui vend la discipline de mesure.

3 · AUCUNE REQUÊTE DE LARGEUR. Entre 900 et 1280 px la colonne « intervalle », qui EST
    l'argument, tombait sur le champ vert : encre sombre sur fond sombre. À 390 px l'objet
    recouvrait le texte dans cinq maquettes sur six. Deux points de rupture, et une règle
    absolue : aucune géométrie de fond ne traverse un bloc de texte.

4 · LE PIED MOURAIT SUR LE VERT. Il était défini une fois pour le papier puis hérité sur
    trois fonds sombres : 1,91 contre 1 pour « Nothing leaves the network », la seule
    phrase qui décide si une banque continue à lire. Le champ s'arrête maintenant
    au-dessus du pied dans les six, ce que seule la diagonale faisait.

5 · DEUX COULEURS ÉCHOUAIENT AA, MESURÉES ET NON ESTIMÉES. `--pale` #67634f donnait 3,72
    contre le papier le plus sombre et portait les deux phrases les plus persuasives ;
    `--vert-vif` #3f8f66 donnait 4,06 sur le vert. Remplacées par #55523f (4,85) et
    #57b184 (6,82), calculées.

6 · LA MISE EN PAGE CONTREDISAIT LE TITRE. Il dit « Both numbers are true » et je grisais
    94,4, c'est-à-dire le chiffre que le lecteur publie en interne depuis deux ans. On lui
    offrait son objection au moment exact où il cherche une raison de partir. Même encre,
    même graisse : ce qui sépare les deux taux est déjà dessiné, la présence ou l'absence
    de l'intervalle.

Et l'interdit qui traverse tout : `taste-skill` bannit le tiret cadratin à ZÉRO occurrence,
pas « avec parcimonie ». Les six pages en étaient pleines.
"""
import pathlib

BASE = pathlib.Path(__file__).parent

# L'alt décrit un ENCODAGE ; la page doit donc le décrire aussi pour qui voit, sinon le
# non-voyant reçoit une figure de données et le voyant une nature morte.
ALT = ("Six rows of chip stacks on a plate, one stack per reader and per field, each chip "
       "worth ten points of measured accuracy. The seventh row has no tiles at all: the "
       "human operator was never sampled field by field.")
LEGENDE = ("One stack per reader and per field. The empty row is the human operator, "
           "never sampled field by field.")

POSES = "\n      ".join(
    f'<img src="rendus/arc/p{i}.webp"{" class=\"vu\"" if i == 4 else ""} '
    f'{("alt=\"" + ALT + "\"" if i == 4 else "alt=\"\" aria-hidden=\"true\"")}>'
    for i in range(9))

COMMUN = """
  :root{
    --papier:#dbd7c5; --papier-haut:#e2ddcb; --papier-bas:#cdccb9;
    --encre:#1b1d18; --demi:#4a4739;
    /* MESURÉ : #55523f donne 4,85 contre le papier le plus sombre, là où le précédent
       #67634f tombait à 3,72 et portait les deux phrases les plus persuasives. */
    --pale:#55523f; --filet:#9d9a83; --filet-clair:#bab7a0;
    --nuit-a:#1b3229; --nuit-b:#14251e; --nuit-c:#0e1a15;
    /* MESURÉ : #57b184 donne 6,82 contre le vert le plus sombre, contre 4,06 pour le
       précédent #3f8f66, qui échouait AA sur la phrase verte du titre. */
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
  /* `100dvh` et non `100vh` : sous Safari mobile, la barre d'adresse qui se rétracte fait
     sauter toute la mise en page d'un écran calé sur `vh`. */
  .ecran{min-height:100dvh;display:flex;flex-direction:column;position:relative;
         overflow:hidden;padding:1.25rem clamp(1.2rem,3.4vw,3.2rem) 1rem;
         max-width:104rem;margin:0 auto}

  .champ{position:absolute;z-index:0;
         background:linear-gradient(163deg,var(--nuit-a) 0%,var(--nuit-b) 54%,var(--nuit-c) 100%)}

  .tete{display:flex;gap:1.1rem;align-items:baseline;flex-wrap:wrap;padding-bottom:.5rem;
        position:relative;z-index:5}
  .tete b{font:600 13px/1 var(--sans);letter-spacing:.2em}
  .tete span{font-size:15px;color:var(--demi)}
  .tete .d{margin-left:auto;font:600 11px/1 var(--sans);letter-spacing:.12em;
           text-transform:uppercase;color:var(--pale)}

  .plaque{position:absolute;margin:0;z-index:2}
  .plaque img{width:100%;display:block;opacity:0;transition:opacity .11s linear}
  .plaque img:not(:first-child){position:absolute;inset:0}
  .plaque img.vu{opacity:1}
  @media (prefers-reduced-motion:reduce){.plaque img{transition:none}}
  /* L'objet occupait la moitié de l'écran et ne portait aucune part de l'argument. Sa
     septième rangée est vide parce que l'opérateur humain n'a jamais été échantillonné
     champ par champ : c'est une constatation d'audit, elle se lit maintenant. */
  .plaque figcaption{position:absolute;left:6%;right:6%;bottom:-2.5rem;
                     font:400 12px/1.45 var(--sans);color:var(--sur-vert-pale);
                     max-width:46ch}
  .socle-ombre{position:absolute;z-index:1;border-radius:50%;pointer-events:none;
               background:radial-gradient(closest-side,rgba(4,10,7,.55),rgba(4,10,7,0))}

  .bloc{position:relative;z-index:3;display:flex;flex-direction:column;justify-content:center;
        flex:1;padding:1rem 0}
  .oeil{font:600 11px/1.4 var(--sans);letter-spacing:.15em;text-transform:uppercase;
        color:var(--pale);display:block;margin-bottom:.9rem}
  h1{margin:0 0 .95rem;text-wrap:balance;letter-spacing:-.021em;
     font:600 clamp(1.85rem,3.5vw,3rem)/1.14 var(--texte);font-variation-settings:"opsz" 48}
  h1 .deux{color:var(--vert-titre)}
  /* Le `<i>` est une enveloppe d'ANIMATION, pas une emphase : sans cette remise à zéro,
     six titres sortent en italique synthétiquement graissé. */
  .ligne > i{font-style:normal}
  .sous{margin:0 0 1.4rem;max-width:38ch;font-size:16px;color:var(--demi)}

  .agir{display:flex;gap:1.2rem;align-items:center;flex-wrap:wrap;margin-top:1.4rem}
  .bouton{text-decoration:none;font:600 15px/1 var(--sans);padding:1rem 1.6rem;
          background:var(--encre);color:#f4f0e4;border:1px solid var(--encre);
          display:inline-block;transition:transform .16s var(--montee),box-shadow .16s ease}
  /* Le survol rendait le bouton TRANSPARENT, donc moins visible qu'au repos. À l'envers.
     Il se soulève maintenant, et s'enfonce au clic. */
  .bouton:hover{transform:translateY(-1px);box-shadow:0 4px 14px rgba(20,37,30,.28)}
  .bouton:active{transform:translateY(1px);box-shadow:none}
  /* Un anneau d'une seule couleur ne survit pas aux deux fonds : mesuré, le vert du titre
     tombe à 1,84 contre le vert sombre. Deux anneaux concentriques, un clair un sombre,
     et l'un des deux ressort toujours. */
  .bouton:focus-visible,.prise:focus-visible,.sel:focus-visible,.rg-g:focus-visible,
  .lg:focus-visible{outline:none;
    box-shadow:0 0 0 2px var(--papier-haut),0 0 0 4.5px var(--nuit-b)}
  /* La phrase de falsifiabilité était en 13,5 px dans la couleur la plus pâle, en légende
     du bouton. C'est la meilleure phrase de la page pour un sceptique : elle passe à la
     taille et à la couleur du texte courant, À CÔTÉ du bouton. */
  .promesse{margin:0;font:400 15px/1.45 var(--texte);color:var(--demi);max-width:29ch}

  .pied{display:flex;gap:1.2rem;align-items:baseline;flex-wrap:wrap;padding:.8rem 0 .1rem;
        position:relative;z-index:5;font:400 15px/1.5 var(--sans);color:var(--pale);
        border-top:1px solid var(--filet-clair)}
  .pied b{color:var(--demi);font-weight:600}

  /* ── LES CHIFFRES : socle commun aux six traitements ───────────────────────
     ÉCHELLE TYPOGRAPHIQUE. Il y avait sept tailles de petit texte entre 11 et 18 px, un
     rapport de 1,45 du plus petit au plus grand : ce n'est pas une échelle, c'est du
     bruit, et rien n'y dit ce qui compte. Trois marches, et chacune a un emploi :
     11 px l'étiquette en capitales, 12 px la note, 15 px le texte courant. */
  .n{font-family:var(--mono);font-variant-numeric:tabular-nums;letter-spacing:-.02em}
  .prise{all:unset;cursor:pointer;display:block}
  dfn{font-style:normal}
  /* L'état « retenu » était une teinte à 9 % d'opacité, sous le seuil de perception. Il
     porte maintenant un fond franc et un filet épais. */
  .vu-x{background:rgba(35,84,63,.16);box-shadow:inset 3px 0 0 var(--vert-titre)}

  /* A · LE RELEVÉ QUI SOLDE. La différence n'est pas un troisième chiffre posé à côté des
     deux autres : elle est ce qu'ils font ensemble, et un livre de comptes sait dire ça
     depuis six siècles. */
  .solde{width:100%;max-width:34rem;border-collapse:collapse}
  .solde th{text-align:left;font:400 15px/1.35 var(--texte);padding:.1rem 0;
            border-bottom:1px solid var(--filet-clair)}
  .solde td{text-align:right;padding:.5rem 0 .5rem 1rem;border-bottom:1px solid var(--filet-clair);
            font-family:var(--mono);font-size:15px;font-variant-numeric:tabular-nums;
            white-space:nowrap}
  .solde td.r{color:var(--pale);font-size:12px;font-family:var(--sans);white-space:normal}
  .solde tr:last-child th,.solde tr:last-child td{border-bottom:none;
    border-top:1.6px solid var(--encre);padding-top:.55rem;font-weight:600}
  .solde tr:last-child th{font-size:15px}
  .solde tr:last-child td:not(.r){font-size:18px;color:var(--vert-titre)}
  /* La prise doit faire 44 px au doigt : le padding l'agrandit sans toucher la hauteur de
     ligne, donc sans décaler le relevé. */
  .sel{all:unset;cursor:pointer;display:block;padding:.62rem .3rem;margin:0 -.3rem;
       border-bottom:1px dotted var(--filet)}

  /* B · LA RÉGLETTE. L'écart cesse d'être un nombre et devient une DISTANCE, et l'absence
     d'intervalle occupe la place où l'autre a le sien. */
  .reglette{width:100%;max-width:620px}
  .reglette svg{width:100%;height:auto;display:block;overflow:visible}
  .rg-axe{stroke:var(--filet);stroke-width:1}
  .rg-t{stroke:var(--filet)} .rg-t.maj{stroke:var(--pale)}
  .rg-ch{font:500 11px/1 var(--mono);fill:var(--pale)}
  /* Même encre, même graisse pour les deux taux : griser 94,4 contredisait le titre. */
  .rg-val{font:600 17px/1 var(--mono);fill:var(--encre)}
  .rg-lab{font:400 12px/1 var(--sans);fill:var(--pale)}
  .rg-aig{stroke:var(--encre);stroke-width:2.2}
  .rg-int{stroke:var(--encre);stroke-width:1.4;fill:none}
  .rg-ec{stroke:var(--vert-titre);stroke-width:1.2;fill:none}
  .rg-ect{font:600 12.5px/1 var(--mono);fill:var(--vert-titre)}
  .rg-g{cursor:pointer}
  .rg-g rect{fill:transparent}
  .rg-g[aria-pressed="true"] rect{fill:rgba(35,84,63,.16)}
  .efface{opacity:.32;transition:opacity .2s ease}

  /* C · LES CENT VINGT MARQUES. Un pourcentage ne se compte pas ; vingt-huit dossiers, si. */
  .marques{max-width:35rem}
  .grille{display:grid;grid-template-columns:repeat(20,1fr);gap:4px;margin-bottom:.7rem}
  .grille i{display:block;aspect-ratio:1;background:var(--encre);border-radius:1px;
            transition:opacity .2s ease}
  .grille i.k{background:transparent;box-shadow:inset 0 0 0 1.4px var(--vert-titre)}
  .grille.q-ok i.k,.grille.q-k i:not(.k){opacity:.15}
  .cles{display:flex;gap:1.2rem;flex-wrap:wrap;font:400 15px/1.5 var(--sans);
        color:var(--pale)}
  .lg{all:unset;cursor:pointer;display:flex;gap:.45rem;align-items:baseline;
      padding:.62rem .35rem;margin:-.4rem -.35rem}
  .cles u{width:12px;height:12px;background:var(--encre);border-radius:1px;
          text-decoration:none;display:block;transform:translateY(1px);flex:none}
  .cles u.k{background:transparent;box-shadow:inset 0 0 0 1.4px var(--vert-titre)}
  .cles b{font:600 15px/1 var(--mono);color:var(--encre)}

  /* D · LA FICHE. Ça ne ressemble pas à un site, ça ressemble à ce qu'ils recevront. */
  .fiche{max-width:33rem;border:1px solid var(--filet);background:rgba(255,252,244,.42)}
  .fiche .cart{display:flex;gap:.7rem;align-items:baseline;border-bottom:1px solid var(--filet);
               padding:.45rem .85rem;font:600 11px/1.4 var(--sans);letter-spacing:.12em;
               text-transform:uppercase;color:var(--pale)}
  .fiche .cart em{margin-left:auto;font-style:normal;font-family:var(--mono);letter-spacing:0}
  .fiche dl{margin:0;padding:.2rem .85rem .5rem}
  .fiche .l{display:grid;grid-template-columns:1fr auto;gap:.6rem;align-items:baseline;
            padding:.62rem .3rem;margin:0 -.3rem;border-bottom:1px dotted var(--filet-clair);
            width:calc(100% + .6rem);text-align:left}
  .fiche .l:last-child{border-bottom:none}
  .fiche dt{font:400 15px/1.4 var(--texte)}
  .fiche dt small{display:block;font:400 12px/1.4 var(--sans);color:var(--pale)}
  .fiche dd{margin:0;font:600 17px/1 var(--mono);font-variant-numeric:tabular-nums}
  .fiche .cle dd{color:var(--vert-titre)}

  /* E · DEUX CHIFFRES ET UNE ACCOLADE. */
  .accolade{display:grid;grid-template-columns:auto 13px auto;grid-template-rows:auto auto;
            gap:.35rem .95rem;align-items:center;max-width:34rem}
  .accolade .f{grid-column:1;padding:.55rem .3rem;margin:0 -.3rem;text-align:left;width:100%}
  .accolade .f.a{grid-row:1} .accolade .f.b{grid-row:2}
  .accolade .f b{display:block;font:600 clamp(1.7rem,2.6vw,2.3rem)/1 var(--mono);
                 letter-spacing:-.03em}
  .accolade .f i{display:block;font:400 12px/1.4 var(--sans);font-style:normal;
                 color:var(--pale);margin-top:.25rem}
  .accolade .br{grid-column:2;grid-row:1/3;border-left:1.4px solid var(--vert-titre);
                border-top:1.4px solid var(--vert-titre);border-bottom:1.4px solid var(--vert-titre);
                border-radius:3px 0 0 3px;height:100%;width:11px}
  .accolade .et{grid-column:3;grid-row:1/3;align-self:center;color:var(--vert-titre)}
  .accolade .et b{display:block;font:600 1.35rem/1 var(--mono);letter-spacing:-.02em}
  .accolade .et i{display:block;font:400 12px/1.4 var(--sans);font-style:normal;
                  color:var(--pale);margin-top:.2rem}

  /* F · LE TABLEAU DE RAPPORT. */
  .tab{width:100%;max-width:37rem;border-collapse:collapse}
  .tab caption{text-align:left;font:600 11px/1.4 var(--sans);letter-spacing:.12em;
               text-transform:uppercase;color:var(--pale);padding-bottom:.45rem}
  .tab thead th{font:600 11px/1.3 var(--sans);letter-spacing:.08em;text-transform:uppercase;
                color:var(--pale);text-align:right;padding:0 0 .35rem 1rem;
                border-bottom:1.4px solid var(--encre)}
  .tab thead th:first-child{text-align:left;padding-left:0}
  .tab td{padding:.5rem 0 .5rem 1rem;text-align:right;
          border-bottom:1px solid var(--filet-clair);font-family:var(--mono);font-size:15px;
          font-variant-numeric:tabular-nums;white-space:nowrap}
  .tab tbody th{padding:.1rem 0;text-align:left;border-bottom:1px solid var(--filet-clair);
                font:400 15px/1.4 var(--texte)}
  .tab td.r{color:var(--pale);font-family:var(--sans);font-size:12px;white-space:normal}
  .tab tr.cle td:not(.r){color:var(--vert-titre);font-weight:600}

  /* ── LA SÉQUENCE D'ENTRÉE ────────────────────────────────────────────────────
     Tout est gardé derrière `.js`, posée par un script SYNCHRONE dans l'en-tête. Sans
     JavaScript, rien n'est masqué : le contenu est l'état par défaut, jamais le mouvement. */
  @media (prefers-reduced-motion:no-preference){
    .js .ecran .champ{transform:translateX(3%);opacity:.86}
    .js .ecran .plaque{opacity:0;transform:translate3d(24px,24px,0) scale(.986)}
    .js .ecran .socle-ombre{opacity:0;transform:scaleX(.82)}
    .js .ecran .ligne > i{display:block;transform:translateY(102%)}
    .js .ecran .oeil,.js .ecran .sous,.js .ecran .chiffres,.js .ecran .agir,
    .js .ecran .pied,.js .ecran .tete{opacity:0}
    .js .ecran .sous,.js .ecran .chiffres,.js .ecran .agir{transform:translateY(10px)}
    .js .go .champ{transform:none;opacity:1;
      transition:transform .56s var(--montee),opacity .4s ease}
    .js .go .plaque{opacity:1;transform:none;
      transition:opacity .5s var(--montee) .14s,transform .58s var(--montee) .14s}
    .js .go .socle-ombre{opacity:1;transform:none;
      transition:opacity .5s ease .24s,transform .56s var(--montee) .24s}
    .js .go .tete{opacity:1;transition:opacity .4s ease .06s}
    .js .go .oeil{opacity:1;transition:opacity .4s ease .32s}
    .js .go .ligne > i{transform:none;transition:transform .52s var(--montee)}
    .js .go .ligne:nth-of-type(1) > i{transition-delay:.38s}
    .js .go .ligne:nth-of-type(2) > i{transition-delay:.48s}
    .js .go .sous{opacity:1;transform:none;
      transition:opacity .42s ease .60s,transform .48s var(--montee) .60s}
    .js .go .chiffres{opacity:1;transform:none;
      transition:opacity .42s ease .70s,transform .48s var(--montee) .70s}
    .js .go .agir{opacity:1;transform:none;
      transition:opacity .42s ease .80s,transform .48s var(--montee) .80s}
    .js .go .pied{opacity:1;transition:opacity .42s ease .88s}
  }
  .ligne{display:block;overflow:hidden;padding-bottom:.16em;margin-bottom:-.16em}
  @media (prefers-reduced-motion:reduce){.ligne{overflow:visible}}

  /* ── LE POINT DE RUPTURE ─────────────────────────────────────────────────────
     Il n'y en avait AUCUN. Sous 1200 px, une seule loi pour les six : le champ redevient
     une bande basse, l'objet vit dedans, le texte tient le papier. Aucune géométrie de
     fond ne traverse un bloc de texte. */
  @media (max-width:1200px){
    .ecran{padding-bottom:0}
    .champ{inset:auto 0 0 0 !important;width:100% !important;height:46vh !important;
           clip-path:none !important;transform:none !important;border:none !important}
    .plaque{left:auto !important;right:-6vw !important;top:auto !important;
            bottom:1.5vh !important;width:min(96vw,560px) !important}
    .plaque figcaption{position:static;margin-top:.5rem}
    .socle-ombre{display:none}
    .bloc{max-width:none !important;padding:1rem 0 48vh !important;justify-content:flex-start}
    .oeil{color:var(--pale) !important}
    h1{color:var(--encre) !important} h1 .deux{color:var(--vert-titre) !important}
    .sous{color:var(--demi) !important;max-width:44ch}
    .promesse{color:var(--demi) !important}
    .bouton{background:var(--encre) !important;color:#f4f0e4 !important;
            border-color:var(--encre) !important}
    .tete b,.tete span{color:var(--encre) !important}
    .tete .d{color:var(--pale) !important}
    .pied{display:none}
    .couture,.folio{display:none}
    .chiffres{position:static !important;bottom:auto !important}
    .agir{position:static !important;bottom:auto !important;left:auto !important}
    .grille{grid-template-columns:repeat(12,1fr)}
    .accolade .f b{font-size:1.7rem}
  }
  @media (max-width:560px){
    .champ{height:38vh !important}
    .bloc{padding-bottom:40vh !important}
    .solde,.tab,.fiche,.reglette,.marques,.accolade{max-width:none}
    .accolade{grid-template-columns:auto 13px}
    .accolade .et{grid-column:1/3;grid-row:3;align-self:start;padding-top:.4rem}
  }
"""

SCRIPT = """<script>
/* ── LA PIÈCE TOURNE. Neuf poses rendues, le curseur en choisit une. */
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
    p.style.transform = `translate3d(0,${(-y * 7).toFixed(2)}px,0)`;
    if (o) o.style.transform = `translate3d(${(x * 10).toFixed(2)}px,${(y * 3).toFixed(2)}px,0)`;
    if (Math.abs(vx - x) > 1e-3 || Math.abs(vy - y) > 1e-3) requestAnimationFrame(boucle);
    else tourne = false;
  }
})();

/* ── LES PRISES. Elles étaient focalisables mais INACTIONNABLES : le gestionnaire n'écoutait
   que `click`, jamais `keydown`. Entrée et Espace ne faisaient rien, sur des éléments qui
   s'annoncent « bouton ». Les `<g>` d'un SVG ne reçoivent pas de `click` synthétique au
   clavier : il faut poser l'écoute à la main. */
(() => {
  const z = document.querySelector(".chiffres");
  if (!z) return;
  const basculer = (b) => {
    const deja = b.getAttribute("aria-pressed") === "true";
    z.querySelectorAll('[aria-pressed="true"]').forEach((x) => x.setAttribute("aria-pressed", "false"));
    z.querySelectorAll(".vu-x").forEach((x) => x.classList.remove("vu-x"));
    z.querySelectorAll(".efface").forEach((x) => x.classList.remove("efface"));
    const g = z.querySelector(".grille");
    if (g) g.classList.remove("q-ok", "q-k");
    if (deja) return;
    b.setAttribute("aria-pressed", "true");
    const quoi = b.dataset.prise;
    if (!b.closest("svg")) (b.closest("tr") || b).classList.add("vu-x");
    if (g && (quoi === "ok" || quoi === "k")) g.classList.add(quoi === "ok" ? "q-ok" : "q-k");
    if (quoi === "A" || quoi === "B")
      z.querySelectorAll(quoi === "A" ? ".rg-b" : ".rg-a")
       .forEach((x) => x.classList.add("efface"));
  };
  z.addEventListener("click", (e) => {
    const b = e.target.closest("[data-prise]"); if (b) basculer(b);
  });
  z.addEventListener("keydown", (e) => {
    if (e.key !== "Enter" && e.key !== " ") return;
    const b = e.target.closest("[data-prise]"); if (!b) return;
    e.preventDefault(); basculer(b);
  });
})();

/* La séquence attend les fontes : lancée avant, ses premiers temps se jouent sur une fonte
   de secours et le titre saute au milieu du mouvement. */
document.fonts.ready.then(() => requestAnimationFrame(() =>
  requestAnimationFrame(() => document.body.classList.add("go"))));
</script>"""

# Le surtitre disait « The number on your dashboard, and the one on your desk » : une PHRASE
# de cinquante-quatre signes composée en capitales. On reconnaît un mot à sa silhouette, et
# les capitales la suppriment ; au-delà d'une étiquette courte c'est illisible. L'étiquette
# est redevenue courte et ce qu'elle disait est passé dans le texte courant, où il se lit,
# et où il répond enfin à la question que la page ne traitait pas : lequel des deux chiffres
# est sur SON écran.
OEIL = "Two rates, one desk"
TITRE_H1 = ('<span class="ligne"><i>Both numbers are true.</i></span>'
            '<span class="ligne"><i class="deux">Only one leaves your desk.</i></span>')
SOUS = ("94.4% is the number on your dashboard. 76.7% is the one on your desk: the share "
        "of files where all five fields are right together, 92 of 120.")
AGIR = ('<div class="agir"><a class="bouton" href="#">Have your routing measured</a>'
        '<p class="promesse">If nothing comes out cheaper without breaking a file, the '
        'report says so.</p></div>')
PIED = ('<div class="pied"><span>On your records, on your machine. <b>Nothing leaves the '
        'network.</b></span><span>One measurement, frozen, delivered as a report you can '
        'contest line by line.</span></div>')


# ── les six traitements des chiffres ─────────────────────────────────────────
INFO = {}

INFO["solde"] = """<table class="solde">
        <tbody>
          <tr><th><button class="sel" type="button" data-prise="a" aria-pressed="false">Mean of five field rates</button></th>
              <td>94.4%</td><td class="r">no interval</td></tr>
          <tr><th><button class="sel" type="button" data-prise="b" aria-pressed="false">Per-file rate, 92 of 120</button></th>
              <td>76.7%</td><td class="r">Wilson 95% [68.3 to 83.3]</td></tr>
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

INFO["marques"] = """<div class="marques">
        <div class="grille" id="grille" role="img"
             aria-label="120 marks, one per case file. 92 are filled: all five fields right. 28 are open: at least one field wrong."></div>
        <div class="cles">
          <button class="lg" type="button" aria-pressed="false" data-prise="ok"><u></u>
            <span><b>92</b> complete, all five fields right</span></button>
          <button class="lg" type="button" aria-pressed="false" data-prise="k"><u class="k"></u>
            <span><b>28</b> with at least one field wrong</span></button>
          <span style="align-self:center"><b class="n" style="color:var(--vert-titre);
            font:600 15px/1 var(--mono)">76.7%</b> per file, 120 in the corpus</span>
        </div>
      </div>"""

INFO["fiche"] = """<div class="fiche">
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

INFO["accolade"] = """<div class="accolade">
        <button class="f a prise" type="button" data-prise="a" aria-pressed="false">
          <b>94.4%</b><i>mean of five field rates, no interval</i></button>
        <button class="f b prise" type="button" data-prise="b" aria-pressed="false">
          <b>76.7%</b><i>per file, 92 of 120, Wilson [68.3 to 83.3]</i></button>
        <span class="br"></span>
        <div class="et"><b>17.7</b><i>points apart</i></div>
      </div>"""

INFO["tableau"] = """<table class="tab">
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
   désaccorde dès qu'une borne bouge, et c'est l'échelle qui ment. */
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


def page(nom, titre, geo_css, info, extra_js="", corps_extra=""):
    (BASE / nom).write_text(f"""<!doctype html>
<meta charset="utf-8"><title>{titre}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%2314251e'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<!-- Synchrone, avant le style : c'est ce qui AUTORISE l'animation. Sans JavaScript la
     classe n'existe pas, rien n'est masqué, et la page reste entière. -->
<script>document.documentElement.classList.add("js")</script>
<style>{COMMUN}{geo_css}</style>
<div class="ecran">
  <span class="champ"></span>{corps_extra}
  <div class="tete"><b>CASCADE</b><span>routing audit, KYC extraction</span>
    <span class="d">report 64bdacf, measured once and frozen</span></div>
  <figure class="plaque">
      {POSES}
    <figcaption>{LEGENDE}</figcaption>
  </figure>
  <span class="socle-ombre"></span>
  <div class="bloc">
    <span class="oeil">{OEIL}</span>
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
# Le champ s'arrête au-dessus du pied. C'était la seule géométrie dont le bas de page était
# intact par construction ; c'est devenu la règle des six.
page("M1-diagonale.html", "Cascade, diagonal field", """
  .champ{inset:0 0 4.9rem auto;width:59%;clip-path:polygon(14% 0,100% 0,100% 100%,0 100%)}
  .plaque{right:-5vw;top:7vh;width:min(58vw,880px)}
  .socle-ombre{right:0;top:52vh;width:min(40vw,620px);height:12vh}
  .bloc{max-width:36rem}
""", "solde")

# ── B · LE PARTAGE VERTICAL ──────────────────────────────────────────────────
page("M2-vertical.html", "Cascade, vertical split", """
  .champ{inset:0 0 4.9rem auto;width:52%}
  .plaque{right:-4vw;top:9vh;width:min(56vw,860px)}
  .socle-ombre{right:1vw;top:54vh;width:min(38vw,580px);height:11vh}
  .bloc{max-width:40rem;padding-right:2rem}
""", "reglette", REGLETTE_JS)

# ── C · LE BANDEAU ───────────────────────────────────────────────────────────
# La bande remonte et se raccourcit : elle avalait vingt à soixante marques sur cent vingt,
# soit la moitié des unités de la seule figure dont toute la valeur est d'être dénombrable.
page("M3-bandeau.html", "Cascade, band", """
  .champ{inset:18vh 0 45vh -50vw;width:200vw}
  .plaque{right:-3vw;top:6vh;width:min(48vw,740px)}
  .plaque figcaption{bottom:auto;top:calc(100% + .4rem);color:var(--pale)}
  .socle-ombre{right:2vw;top:44vh;width:min(32vw,500px);height:9vh}
  .bloc{max-width:35rem;justify-content:flex-start;padding-top:19.5vh}
  .oeil{color:var(--sur-vert-pale)}
  h1{color:var(--sur-vert)}
  h1 .deux{color:var(--vert-vif)}
  .sous{color:var(--sur-vert-pale);margin-bottom:0}
  .chiffres{position:absolute;left:clamp(1.2rem,3.4vw,3.2rem);right:auto;bottom:7.8rem;z-index:4}
  .agir{position:absolute;left:clamp(1.2rem,3.4vw,3.2rem);bottom:1.2rem;margin:0;z-index:4}
  .pied{display:none}
""", "marques", GRILLE_JS)

# ── D · L'ENCART MONTÉ ───────────────────────────────────────────────────────
# Le débordement de la plaque hors de l'encart faisait vingt-cinq pixels sur un objet de
# huit cents : il se lisait comme une couture de rendu et non comme un geste.
page("M4-encart.html", "Cascade, mounted plate", """
  .champ{inset:6.5rem 2.6rem 5.6rem 42%;border:1px solid rgba(20,37,30,.5)}
  .plaque{right:-1.5vw;top:1.5vh;width:min(53vw,820px)}
  .socle-ombre{right:3vw;top:50vh;width:min(34vw,520px);height:10vh}
  .bloc{max-width:34rem}
""", "fiche")

# ── E · LE CHAMP INVERSÉ ─────────────────────────────────────────────────────
# Toutes les surcharges de fond sombre sont ici, PIED COMPRIS : il était le seul oublié des
# neuf, et il portait la phrase qui décide si une banque continue à lire.
page("M5-inverse.html", "Cascade, inverted field", """
  .champ{inset:0 auto 4.9rem 0;width:46%;clip-path:polygon(0 0,100% 0,86% 100%,0 100%)}
  .plaque{right:-6vw;top:10vh;width:min(56vw,860px)}
  .plaque figcaption{color:var(--pale)}
  .socle-ombre{right:0;top:55vh;width:min(38vw,580px);height:11vh;
               background:radial-gradient(closest-side,rgba(60,52,30,.30),rgba(60,52,30,0))}
  .bloc{max-width:32rem}
  .oeil{color:var(--sur-vert-pale)}
  h1{color:var(--sur-vert)}
  h1 .deux{color:var(--vert-vif)}
  .sous{color:var(--sur-vert-pale)}
  .accolade .f i{color:var(--sur-vert-pale)}
  .accolade .f b{color:var(--sur-vert)}
  .accolade .br{border-color:var(--vert-vif)}
  .accolade .et{color:var(--vert-vif)} .accolade .et i{color:var(--sur-vert-pale)}
  .bouton{background:var(--sur-vert);color:var(--nuit-b);border-color:var(--sur-vert)}
  .promesse{color:var(--sur-vert-pale)}
  .tete b,.tete span{color:var(--sur-vert)}
""", "accolade")

# ── F · LA DOUBLE PAGE ───────────────────────────────────────────────────────
# Le filet du pied dépassait la couture d'une trentaine de pixels, posés sur la page sombre.
# Et une double page à un seul folio n'est pas une double page : celui de gauche revient,
# au-dessus du pied plutôt que dedans.
page("M6-double.html", "Cascade, spread", """
  .champ{inset:0 0 4.9rem 50%}
  .couture{position:absolute;left:50%;top:0;bottom:4.9rem;width:1px;
           background:rgba(20,37,30,.28);z-index:4}
  .folio{position:absolute;bottom:5.6rem;font:500 11px/1 var(--mono);letter-spacing:.12em;
         z-index:5;color:var(--pale)}
  .folio.g{left:clamp(1.2rem,3.4vw,3.2rem)}
  .folio.d{right:clamp(1.2rem,3.4vw,3.2rem);color:var(--sur-vert-pale)}
  .plaque{right:-4vw;top:11vh;width:min(50vw,760px)}
  .socle-ombre{right:1vw;top:56vh;width:min(34vw,520px);height:10vh}
  .bloc{max-width:39rem;padding-right:3rem}
  .pied{width:calc(50% - 1.7rem)}
""", "tableau", "", corps_extra=('<span class="couture"></span>'
                                 '<span class="folio g">FINDING 01</span>'
                                 '<span class="folio d">PLATE 1, ACCURACY BY READER AND FIELD</span>'))

print("\nsix maquettes, après la passe de correction groupée")
