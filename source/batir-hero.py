#!/usr/bin/env python3
"""LE HÉROS COMPLET : un seul écran pour tout l'outil, cinq états, un pupitre.

CE QU'ARSLANE A ARRÊTÉ LE 31 AOÛT
  · un seul écran pour tout l'outil : pas de défilement, pas d'autres pages —
    les boutons du bas donnent accès à chaque partie ;
  · au clic : le titre change, les infos changent, ET l'objet 3D change — le même
    design, mais les données dedans changent (les cinq rendus d'état existent) ;
  · on reste sur le héros jusqu'à ce qu'il soit totalement complet.

CE QUE CETTE PAGE EST
La fusion de deux choses déjà validées par la mesure :
  · le MOTEUR de PARCOURS.html — cinq adresses réelles (#e01…#e05), :target fait
    tout sans script, le Retour marche, la bande verte ne bouge pas d'un pixel
    (les cinq titres empilés dans la même cellule de grille) ;
  · l'ESTHÉTIQUE des compositions V — chiffres en corps d'affiche, réserve en
    note de marge italique, presque aucune bordure, et le PUPITRE : un second
    bandeau nuit en bas, miroir du premier, où vivent les cinq accès.

LE PUPITRE EST LE TABLEAU DE COMMANDE DE L'OUTIL
Il ne change jamais : cinq entrées avec leur question, la courante marquée par
trois signes (filet vert, graisse, le mot « reading »), et les six annexes dans
son pied. Tout le reste — titre, œil, chiffres, note, objet — pivote en place.

CHAQUE ÉTAT A SES PROPRES CHIFFRES, COMPOSÉS, PAS TABULÉS
Un état = deux ou trois grandeurs en corps d'affiche, l'écart écrit sur la flèche
quand il y a un écart, et une note de marge qui dit ce que ça ne prouve pas PLUS
ce qui a changé dans l'objet. Chaque chiffre vient du dépôt, retrouvé à la ligne
et contre-éprouvé ; ce qui n'a pas survécu à la contre-épreuve ne s'affiche pas.
"""
import importlib.util
import pathlib

BASE = pathlib.Path(__file__).parent


def charge(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, BASE / fichier)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


bn = charge("bn", "batir-nav.py")
bp = charge("bp", "batir-parcours.py")
X = bn.X

# ── LES CINQ ÉTATS, CHACUN SUR SON INSTRUMENT ───────────────────────────────
# La forme F5 retenue par Arslane : une échelle dessinée porte les grandeurs de
# l'état. Chaque état a son DOMAINE propre — pourcentages, dollars, divergence,
# énumération — parce qu'étirer un domaine pour en faire tenir un autre serait un
# mensonge d'axe. L'armature, elle, ne bouge pas : en-tête, axe, drapeau haut,
# drapeau bas, aux mêmes hauteurs dans les cinq états.
ETATS = [
    {
        "no": "01",
        "cap": "The two rates, on the same drawn scale",
        "dom": (60, 100), "reperes": [60, 70, 80, 90, 100], "unite": "",
        "plage": (76.7, 94.4, "17.7 points"),
        "wilson": (68.3, 83.3),
        "haut_d": (94.4, "94.4%", "The dashboard mean."),
        "bas_d": (76.7, "76.7%",
                  "On your desk: all five fields right on the same file, 92 of 120. "
                  "Wilson 95%: 68.3 to 83.3."),
        "reserve": ("<b>Neither number is wrong:</b> they answer different questions, "
                    "and only one of them is the question at your desk."),
        "fig": "Five green cells mark the published routing, one per field.",
    },
    {
        "no": "02",
        "cap": "Cost per 100 000 documents, on assumed prices",
        "dom": (0, 200), "reperes": [0, 50, 100, 150, 200], "unite": "$",
        "plage": (54, 191, "3.5&#215; cheaper"),
        "wilson": None,
        "haut_d": (191, "$191", "The published routing."),
        "bas_d": (54, "$54",
                  "The routing aimed at the file: no file gets worse, 3 gained, "
                  "0 lost. p&nbsp;=&nbsp;0.25, accuracy undecided."),
        "reserve": ("<b>The sample decides cost, not accuracy:</b> cheaper is decided, "
                    "better is not — and both dollar figures rest on assumed prices."),
        "fig": "One cell steps down: the name field moves from large to gen-4b. That "
               "is the only difference between the two routings.",
    },
    {
        "no": "03",
        "cap": "Precision, before and after silence",
        "dom": (0, 100), "reperes": [0, 25, 50, 75, 100], "unite": "",
        "plage": (30, 62.3, "after abstention"),
        "wilson": (48.8, 74.1),
        "haut_d": (30, "30%", "Every value delivered."),
        "bas_d": (62.3, "62.3%",
                  "With silence, on the hard corpus: 33 of 53 right. "
                  "85 wrong removed, 12 right lost."),
        "reserve": ("<b>Where the break-even sits is your decision, not ours:</b> we "
                    "publish the curve, you place the point."),
        "fig": "Where the rules reader returned 0%, it now returns nothing: the two "
               "red cells become gaps. Abstention, drawn.",
    },
    {
        "no": "04",
        "cap": "Divergence between two passes of the same bench, in per cent",
        "dom": (0, 60), "reperes": [0, 20, 40, 60], "unite": "%",
        "plage": (16, 60, "withheld"),
        "wilson": None,
        "haut_d": (0, "identical", "Every count, to the digit."),
        "bas_d": (38, "16&#8211;60%",
                  "Every median duration moved. 32 conclusions retracted, "
                  "11 caught first."),
        "bas_sans_point": True,
        "reserve": ("<b>Removing a measurement is a discipline, not a guarantee</b> "
                    "about the figures we keep."),
        "fig": "No cell is green: nothing here is held up as a result.",
    },
    {
        "no": "05",
        "cap": "The routing space, enumerated end to end",
        "dom": (0, 16807), "reperes": [0, 16807], "unite": "",
        "plage": (0, 16807, "the full span"),
        "wilson": None,
        "haut_d": (16807, "16&#8239;807",
                   "Every combination of seven readers over five fields. Not a sample."),
        "bas_d": (8403, "120 files &#183; 618 tests",
                  "Held out and frozen; the tests run on your machine."),
        "bas_sans_point": True,
        "reserve": ("<b>The corpus here is synthetic:</b> which is exactly why the real "
                    "measurement runs on your records, on your machine."),
        "fig": "Every cell is green: the full enumeration, one routing at a time.",
    },
]


def _pc(v, dom):
    a, b = dom
    return round((v - a) / (b - a) * 100, 2)


def _cal(x):
    """Le drapeau se recale près des bords au lieu d'en sortir : à fleur du bord
    quand le point y est, sinon décalé d'autant qu'il faut."""
    if x > 92:
        return "left:100%;transform:translateX(-100%);text-align:right", -1.0
    if x > 80:
        return "transform:translateX(-85%);text-align:right", -0.85
    if x < 6:
        return "left:0;transform:none;text-align:left", 0.0
    if x < 14:
        return "transform:translateX(-12%);text-align:left", -0.12
    return "", -0.5


def inst_html(e):
    dom = e["dom"]
    xa = _pc(e["haut_d"][0], dom)
    xb = _pc(e["bas_d"][0], dom)
    pa, pb, plabel = e["plage"]
    xpa, xpb = _pc(pa, dom), _pc(pb, dom)
    # Les repères en spans positionnés en pour cent, comme les points : un SVG
    # est un élément REMPLACÉ — avec une hauteur fixée, son ratio de viewBox
    # impose sa largeur (660 px) et il déborde sous 660 px de conteneur.
    # Mesuré le 31/08 à 375 px : les repères 90 et 100 partaient dans le clip.
    reps = []
    n = len(e["reperes"])
    for i, v in enumerate(e["reperes"]):
        x = _pc(v, dom)
        anc = ("left:0" if i == 0 else
               ("left:100%;transform:translateX(-100%)" if i == n - 1 else
                f"left:{x}%;transform:translateX(-50%)"))
        lab = f"{v:,}".replace(",", "&#8239;")
        reps.append(f'<span style="{anc}">{lab}</span>')
    wil = ""
    if e["wilson"]:
        lo, hi = _pc(e["wilson"][0], dom), _pc(e["wilson"][1], dom)
        wil = (f'<span class="wil" style="left:{lo}%;width:{hi - lo}%"><i></i></span>')
    sa, _ = _cal(xa)
    sb, _ = _cal(xb)
    pt_b = "" if e.get("bas_sans_point") else         f'<span class="pt b" style="left:{xb}%"></span>'
    # l'emprise horizontale des deux drapeaux, en pour cent d'une largeur plancher
    DEMI = 200 / 600 * 100 / 2          # demi-drapeau : ~16,7 %
    _, ta = _cal(xa)
    _, tb = _cal(xb)
    empa = (xa + ta * DEMI * 2, xa + (1 + ta) * DEMI * 2)
    empb = (xb + tb * DEMI * 2, xb + (1 + tb) * DEMI * 2)

    def libre(x, demi_label=11):
        g, d = empa                      # seul le drapeau HAUT partage son étage
        return not (x + demi_label > g - 3 and x - demi_label < d + 3)

    base = min(xpa, xpb)
    span = abs(xpb - xpa)
    xm = next((base + span * f for f in (0.5, 0.72, 0.28, 0.88, 0.12, 0.05)
               if libre(base + span * f)), base + span * 0.5)
    sm, _ = _cal(xm)
    return f"""<div class="inst">
      <span class="cap-i"><b>Figure 2</b>{e["cap"]}</span>
      <div class="porte">
        <span class="plage" style="left:{min(xpa, xpb)}%;width:{abs(xpb - xpa)}%"></span>
        <span class="axe"></span><span class="grads"></span>
        <div class="reps">{"".join(reps)}</div>
        {wil}
        <span class="pt a" style="left:{xa}%"></span>
        {pt_b}
        <span class="ecart-l" style="left:{xm}%;{sm}">{plabel}</span>
        <div class="drapeau d-a" style="left:{xa}%;{sa}">
          <span class="gv">{e["haut_d"][1]}</span><p>{e["haut_d"][2]}</p></div>
        <div class="drapeau d-b" style="left:{xb}%;{sb}">
          <span class="gv de">{e["bas_d"][1]}</span><p>{e["bas_d"][2]}</p></div>
      </div>
    </div>"""


HERO_CSS = """
  /* LA CRÈME (demande d'Arslane : « trop blanc »). Recalculée, pas estimée :
     encre 11,1:1 · demi 6,1:1 · pale 4,7:1 sur le ton le plus sombre. */
  :root{--papier-haut:#e3dcc2;--papier:#d8d1b6;--papier-bas:#cbc4aa;
        --pale:#4f4c3a;--filet-clair:#b3ac91}
  h1{margin:0}
  .legende{display:none}

  /* ── la manchette ─────────────────────────────────────────────────────────── */
  .tete{display:flex;gap:1rem;align-items:baseline;flex-wrap:wrap}
  .marque{display:inline-flex;gap:.55rem;align-items:center}
  .carre{width:12px;height:12px;flex:none;
         background:linear-gradient(135deg,var(--nuit-a) 0 62%,var(--vert-titre) 62%)}
  .marque b{font:700 14px/1 var(--sans);letter-spacing:.26em;color:var(--encre)}
  .sep-v{width:1px;align-self:stretch;background:var(--filet-clair);margin:.15rem 0}
  .desc{font:italic 400 15px/1.3 var(--texte);color:var(--demi)}
  .tete .tampon{margin-left:auto;border:1px solid var(--filet);padding:.34rem .7rem;
          font:500 10px/1.4 var(--mono);letter-spacing:.14em;text-transform:uppercase;
          color:var(--pale)}
  .oeil{display:flex;align-items:center;gap:.9rem;text-transform:none;
        letter-spacing:0}
  .oeil .fno{font:600 11px/1.4 var(--sans);letter-spacing:.14em;
             text-transform:uppercase;color:var(--vert-titre)}
  .oeil .fti{font:600 11px/1.4 var(--sans);letter-spacing:.15em;
             text-transform:uppercase;color:var(--pale)}
  .oeil::after{content:"";flex:1;height:1px;background:var(--filet-clair)}
  .plaque{display:grid}
  /* l'objet ne bouge pas : fondu croisé pur, cadrage commun mesuré au pixel */
  .plaque img{width:100%;display:block;grid-area:1/1;position:static;
              opacity:0;visibility:hidden;transform:none;
              transition:opacity .24s ease,visibility 0s linear .24s}
  .plaque img.la{opacity:1;visibility:visible;
                 transition:opacity .26s ease .04s,visibility 0s}
  .bas{max-width:none}
  .haut{padding-top:clamp(1.1rem,2.6vh,2rem);padding-bottom:clamp(1.1rem,2.6vh,2rem)}
  .haut .pile > h1{align-self:center;margin-top:-0.155em;margin-bottom:0.155em}

  /* ── la pile : ce qui change vit dans UNE cellule, la plus haute dimensionne ── */
  .pile{display:grid}
  .pile > *{grid-area:1/1}
  /* sortie : un fondu bref, sur place ; le transform saute une fois invisible */
  .vue{visibility:hidden;opacity:0;pointer-events:none;
       transform:translateY(9px);
       transition:opacity .13s ease,visibility 0s linear .13s,transform 0s .13s}
  /* entrée : le contenu monte vers sa place, en cascade de lecture */
  .vue.la{visibility:visible;opacity:1;pointer-events:auto;transform:none;
          transition:opacity .3s var(--montee) .05s,
                     transform .36s var(--montee) .05s,visibility 0s .05s}
  .haut .vue.la{transition-delay:.05s}
  .bas .vue.la{transition-delay:.11s}
  .bas .pile-note .vue.la{transition-delay:.15s}
  .fig-objet .vue.la{transition-delay:.19s}
  @media (prefers-reduced-motion:reduce){
    .vue,.vue.la,.plaque img{transition:none!important;transform:none!important}
  }

  /* ── l'instrument : la forme F5, déclinée par état ───────────────────────
     L'armature est FIXE : en-tête, axe, drapeau haut, drapeau bas aux mêmes
     hauteurs dans les cinq états — la bascule change les chiffres dans un cadre
     immobile. Près des bords, le drapeau se recale au lieu de sortir. */
  /* MESURÉ : .bas est un flex en align-items:flex-start, donc la pile enfant
     rétrécissait à son contenu — l'instrument faisait 210 px et tous ses
     pourcentages s'écrasaient dedans. La pile s'étire, l'instrument reprend
     53 % de la vraie colonne. */
  .bas > .pile{align-self:stretch}
  .inst{width:min(53%,47rem)}
  .cap-i{display:block;margin-bottom:.3rem;font:400 12.5px/1.4 var(--sans);
         color:var(--demi)}
  .cap-i b{font:600 10px/1.4 var(--sans);letter-spacing:.14em;
           text-transform:uppercase;color:var(--pale);margin-right:.5rem}
  /* MESURÉ le 31/08 au soir : le drapeau bas (96px + 77px de contenu) sortait
     de la boîte de 15 px À TOUTES les largeurs — seul le blanc d'en dessous
     masquait la collision ; à l'étroit, « to 83.3. » écrasait la note. */
  .porte{position:relative;height:176px}
  .axe{position:absolute;left:0;right:0;top:78px;height:1.5px;background:var(--encre)}
  .grads{position:absolute;left:0;right:0;top:79.5px;height:5px;
         background:repeating-linear-gradient(90deg,var(--filet-clair) 0 1px,
                    transparent 1px 5%)}
  .reps{position:absolute;left:0;right:0;top:86px;height:14px;display:block}
  .reps span{position:absolute;top:0;font:500 10px/1.4 var(--sans);color:var(--pale);
             white-space:nowrap}
  .plage{position:absolute;top:72px;height:14px;background:rgba(35,84,63,.16)}
  .pt{position:absolute;top:78.75px;width:9px;height:9px;border-radius:50%;
      transform:translate(-50%,-50%)}
  .pt.a{background:var(--encre)}
  .pt.b{background:var(--vert-titre)}
  .wil{position:absolute;top:72px;height:13px;border-left:1.5px solid var(--vert-titre);
       border-right:1.5px solid var(--vert-titre)}
  .wil i{position:absolute;left:0;right:0;top:6px;height:1.5px;
         background:var(--vert-titre);display:block}
  .drapeau{position:absolute;transform:translateX(-50%);text-align:center;width:200px}
  .drapeau .gv{font:600 1.7rem/1 var(--texte);letter-spacing:-.02em;
               font-variant-numeric:tabular-nums;display:block}
  .drapeau .gv.de{color:var(--vert-titre)}
  .drapeau p{margin:.2rem 0 0;font:400 11.5px/1.35 var(--sans);color:var(--demi)}
  .d-a{top:2px}
  .d-a p{max-width:185px;margin-left:auto;margin-right:auto}
  .d-b{top:96px}
  .ecart-l{position:absolute;top:52px;transform:translateX(-50%);
           font:600 10.5px/1 var(--sans);letter-spacing:.13em;text-transform:uppercase;
           color:var(--vert-titre);white-space:nowrap}

  /* ── la note : dans la colonne de lecture, même marge que titre et chiffres ── */
  /* l'exemple au milieu, la note contre la bande : deux marges automatiques se
     partagent le blanc, et la note reste collée au pupitre */
  .bas{margin-top:auto}
  .pile-note{margin-top:auto;margin-bottom:.85rem;position:relative;z-index:3}
  .pupitre{margin-top:0!important}
  .note-flux{margin:0;max-width:none;font:italic 400 14.5px/1.5 var(--texte);
             color:var(--demi)}
  .note-flux b{font-style:italic;font-weight:600;color:var(--encre)}
  .note-flux .nt-l{font:600 10.5px/1.4 var(--sans);font-style:normal;
                   letter-spacing:.14em;text-transform:uppercase;color:var(--pale);
                   margin-right:.55rem}
  .note-flux .nt-fig{display:none;font:400 12px/1.5 var(--sans);font-style:normal;
                     color:var(--pale)}
  /* ── sous l'objet : SA légende seulement, posée sur un filet de légende ────── */
  .fig-objet{position:absolute;z-index:4;right:clamp(1.2rem,3.4vw,3.2rem);
             width:min(24%,19rem);
             top:calc(clamp(4.4rem,9vh,7rem) + 0.81 * min(40vw,600px) + 1.2rem);
             border-top:1px solid var(--filet-clair);padding-top:.45rem}
  .fig-objet p{margin:0;font:400 12px/1.5 var(--sans);color:var(--pale)}
  .fig-objet .no{font:600 10px/1.4 var(--sans);letter-spacing:.14em;
                 text-transform:uppercase;color:var(--demi);margin-right:.45rem}

  /* ── le pupitre : le tableau de commande, permanent ──────────────────────── */
  .pupitre{position:relative;z-index:5;margin:auto -50vw 0;width:200vw;
           padding:.9rem calc(50vw + 2 * clamp(1.2rem,3.4vw,3.2rem)) 0 50vw;
           background:linear-gradient(163deg,var(--nuit-a) 0%,var(--nuit-b) 74%)}
  .b-lien{all:unset;cursor:pointer;display:block}
  .pup-nav{display:grid;grid-template-columns:repeat(5,1fr);
           gap:clamp(.6rem,1.6vw,1.6rem)}
  .pup-nav .b-lien{display:flex;gap:.6rem;align-items:baseline;
                   padding:.55rem .2rem .6rem;border-top:3px solid transparent;
                   transition:border-color .16s ease}
  .pup-nav .no{font:600 10.5px/1 var(--sans);letter-spacing:.14em;
               color:var(--sur-vert-pale)}
  .pup-nav .ti{font:400 16.5px/1.2 var(--texte);color:var(--sur-vert)}
  /* la question reste lisible aux lecteurs d'écran, invisible à l'œil */
  .pup-nav .qu{position:absolute;width:1px;height:1px;overflow:hidden;
               clip-path:inset(50%)}
  .pup-nav .b-lien:hover{border-top-color:var(--sur-vert-pale)}
  .pup-nav .b-lien.la{border-top-color:var(--vert-vif)}
  .pup-nav .b-lien.la .no{color:var(--vert-vif)}
  .pup-nav .b-lien.la .ti{font-weight:600}

  .pup-nav .b-lien:focus-visible{outline:none;
    box-shadow:0 0 0 2px var(--nuit-b),0 0 0 4.5px var(--sur-vert)}
  .pied-nuit{display:flex;gap:.6rem 2rem;align-items:baseline;flex-wrap:wrap;
             margin-top:.5rem;padding:.55rem 0 .7rem;
             border-top:1px solid rgba(228,236,223,.16);
             font:400 12.5px/1.45 var(--sans);color:var(--sur-vert-pale)}
  .pied-nuit b{color:var(--sur-vert);font-weight:600}
  .pied-nuit .annexes{display:flex;gap:clamp(.7rem,1.4vw,1.25rem);flex-wrap:wrap;
                      margin-left:auto}
  .pied-nuit .b-lien{display:inline;padding:.3rem .1rem;color:var(--sur-vert-pale)}
  .pied-nuit .b-lien:hover{color:var(--sur-vert)}
  .pied-nuit .b-lien:focus-visible{outline:none;
    box-shadow:0 0 0 2px var(--nuit-b),0 0 0 4.5px var(--sur-vert)}
  .ancre{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}

  @media (max-height:840px){
    .porte{height:152px}
    .axe{top:62px}
    .grads{top:63.5px}
    .reps{top:69px}
    .plage{top:56px}
    .pt{top:62.75px}
    .wil{top:56px}
    .ecart-l{top:42px}
    .d-b{top:78px}
    .drapeau .gv{font-size:1.4rem}
    .drapeau p{font-size:11px}
    .cap-i{margin-bottom:.15rem}
    .pup-nav .b-lien{padding:.4rem .2rem .5rem}
    .pied-nuit{margin-top:.25rem;padding:.35rem 0 .4rem}
    .fig-objet{display:none}
    .note-flux .nt-fig{display:inline;margin-left:.5rem}
    .note-flux{font-size:13.5px}
    .pile-note{margin-top:.35rem}
    .bas{margin-top:.5rem}
    .pied-nuit{padding-bottom:.3rem}
    .note-flux{font-size:13px}
  }
  @media (max-width:1080px){
    .pup-nav{grid-template-columns:1fr 1fr}
    .fig-objet{display:none}
    .note-flux .nt-fig{display:inline;margin-left:.5rem}
    .inst{width:100%}
    /* l'objet revient EN FLUX sous la bande — la règle commune l'envoyait en
       absolute au fond de l'écran, derrière le pupitre (constat du 31/08) */
    /* À DROITE, mordant sur la bande — pas centré dans le vide : la version
       centrée était la composition téléphone étirée sur une fenêtre de bureau
       non maximisée (constat d'Arslane, 31/08 au soir). `relative` et non
       `static` : il faut un z-index pour peindre l'objet PAR-DESSUS le vert. */
    /* `inset:auto` : le commun pose `right:-6vw` pour sa version absolue —
       inerte sur static, ce décalage AGIT sur relative (38 px mesurés à 640) */
    .plaque{position:relative;inset:auto;z-index:2;width:min(46vw,400px);
            transform:none;
            margin:calc(-1 * min(5vw,2.8rem)) clamp(1.2rem,3.4vw,3.2rem) .2rem auto}
    .js .ecran .plaque{transform:none}
  }
  @media (max-width:640px){
    /* le téléphone : la pile centrée validée — l'objet quitte le bord droit */
    .plaque{width:min(58vw,300px);margin:1.1rem auto .3rem}
    /* les drapeaux couvrent 60 % de l'axe à cette largeur : aucun créneau
       libre pour l'étiquette d'écart — les drapeaux portent déjà les chiffres */
    .ecart-l{display:none}
    .tete{display:block}
    .sep-v{display:none}
    .desc{display:block;margin-top:.35rem}
    .tete .tampon{display:block;margin:.6rem 0 0;text-align:center;
            font-size:9px;letter-spacing:.09em;padding:.3rem .4rem;
            white-space:nowrap}
  }
"""

# Les règles :target — l'adresse choisit l'état, aucun script requis.
regles = []
for e in ETATS:
    n = e["no"]
    if n == "01":
        continue
    regles.append(
        f'  .ecran:has(#e{n}:target) [data-e="{n}"]{{visibility:visible;opacity:1;'
        f'pointer-events:auto;transition:opacity .22s ease .04s,visibility 0s}}\n'
        f'  .ecran:has(#e{n}:target) [data-e]:not([data-e="{n}"]){{visibility:hidden;'
        f'opacity:0;pointer-events:none;transition:opacity .22s ease,'
        f'visibility 0s linear .22s}}\n'
        f'  .ecran:has(#e{n}:target) .pup-nav .b-lien[href="#e{n}"]{{'
        f'border-top-color:var(--vert-vif)}}\n'
        f'  .ecran:has(#e{n}:target) .pup-nav .b-lien[href="#e{n}"] .no{{'
        f'color:var(--vert-vif)}}\n'
        f'  .ecran:has(#e{n}:target) .pup-nav .b-lien[href="#e{n}"] .ti{{'
        f'font-weight:600}}\n'

        f'  .ecran:has(#e{n}:target) .pup-nav .b-lien[href="#e01"]{{'
        f'border-top-color:transparent}}\n'
        f'  .ecran:has(#e{n}:target) .pup-nav .b-lien[href="#e01"] .no{{'
        f'color:var(--sur-vert-pale)}}\n'
        f'  .ecran:has(#e{n}:target) .pup-nav .b-lien[href="#e01"] .ti{{'
        f'font-weight:400}}\n'
)
CIBLES = "".join(regles)

ancres = "".join(f'<i class="ancre" id="e{e["no"]}" aria-hidden="true"></i>'
                 for e in ETATS)
par_no = {e["no"]: e for e in bp.ECRANS}


def pile(rendu):
    return '<div class="pile">' + "".join(
        f'<{rendu(e, " la" if e["no"] == "01" else "")}' for e in ETATS) + "</div>"


def _rubrique(texte):
    fno, fti = texte.split(", ", 1)
    return (f'<span class="fno">{fno}</span><span class="fti">{fti}</span>')


yeux = "".join(
    f'<span class="oeil vue{" la" if e["no"] == "01" else ""}" data-e="{e["no"]}">'
    f'{_rubrique(par_no[e["no"]]["oeil"])}</span>' for e in ETATS)
titres = "".join(
    f'<h1 class="vue{" la" if e["no"] == "01" else ""}" data-e="{e["no"]}">'
    f'{bp.titre_html(par_no[e["no"]]["titre"])}</h1>' for e in ETATS)
objets = "".join(
    f'<img class="{"la " if e["no"] == "01" else ""}vue" data-e="{e["no"]}" '
    f'src="rendus/etats/objet-{e["no"]}.webp" '
    f'alt="Seven readers down, five fields across. {e["fig"]}">' for e in ETATS)
chiffres = "".join(
    f'<div class="vue{" la" if e["no"] == "01" else ""}" data-e="{e["no"]}">'
    f'{inst_html(e)}</div>' for e in ETATS)
notes = "".join(
    f'<p class="note-flux vue{" la" if e["no"] == "01" else ""}" data-e="{e["no"]}">'
    f'<span class="nt-l">What this does not prove</span>{e["reserve"]}'
    f'<span class="nt-fig">Figure 1 &#8212; {e["fig"]}</span></p>' for e in ETATS)
legendes = "".join(
    f'<p class="vue{" la" if e["no"] == "01" else ""}" data-e="{e["no"]}">'
    f'<span class="no">Figure 1</span>{e["fig"]}</p>' for e in ETATS)
pupitre = "".join(
    f'<a class="b-lien{" la" if e["no"] == "01" else ""}" href="#e{e["no"]}"'
    f'{" aria-current=\"true\"" if e["no"] == "01" else ""}>'
    f'<span class="no">{e["no"]}</span>'
    f'<span class="ti">{par_no[e["no"]]["onglet"]}</span>'
    f'<span class="qu">{par_no[e["no"]]["question"]}</span></a>' for e in ETATS)

SCRIPT = """<script>
/* L'adresse fait déjà tout ; le script n'ajoute que la même horloge pour la cause et
   l'effet, et le titre du document. */
(() => {
  const montrer = (n) => {
    for (const el of document.querySelectorAll("[data-e]"))
      el.classList.toggle("la", el.dataset.e === n);
    for (const a of document.querySelectorAll(".pup-nav .b-lien")) {
      const la = a.getAttribute("href") === "#e" + n;
      a.classList.toggle("la", la);
      if (la) a.setAttribute("aria-current", "true");
      else a.removeAttribute("aria-current");
    }
    const t = document.querySelector(`h1[data-e="${n}"]`);
    document.title = "Cascade, " + (t ? t.textContent.trim() : "finding " + n);
  };
  const lire = () => (location.hash.match(/^#e(0[1-5])$/) || [, "01"])[1];
  addEventListener("hashchange", () => montrer(lire()));
  montrer(lire());
})();
/* .go rallume la page ; un onglet caché ne sert AUCUN rAF (mesuré le 31/08 :
   2 s, 0 rAF, page blanche) — le filet de 1500 ms garantit l'allumage même là. */
const go = () => document.body.classList.add("go");
document.fonts.ready.then(() => requestAnimationFrame(() => requestAnimationFrame(go)));
setTimeout(go, 1500);
</script>"""

(BASE / "HERO.html").write_text(f"""<!doctype html><html lang="en">
<meta charset="utf-8"><title>Cascade, the gap</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta property="og:type" content="website">
<meta property="og:title" content="Cascade — routing audit, KYC extraction">
<meta property="og:description" content="A routing audit for KYC extraction: measured on sealed records, rerun on your machine. On your records, on your machine — nothing leaves the network.">
<meta property="og:url" content="https://cascade-routing.com/index.html">
<meta property="og:image" content="https://cascade-routing.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="description" content="A routing audit for KYC extraction: measured on sealed records, rerun on your machine. On your records, on your machine — nothing leaves the network.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M0 0h16L0 16z' fill='%2314251e'/%3E%3Cpath d='M16 0v16H0z' fill='%2323543f'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<script>document.documentElement.classList.add("js")</script>
<style>{bn.COMMUN}{HERO_CSS}{CIBLES}</style>
<div class="ecran">
  {ancres}
  <div class="tete">
    <span class="marque"><i class="carre" aria-hidden="true"></i><b>CASCADE</b></span>
    <span class="sep-v" aria-hidden="true"></span>
    <span class="desc">Routing audit, KYC extraction</span>
    <span class="tampon">Seal 1151f5a1cfaae0c0 &#183; measured, then frozen</span></div>
  <div class="pile">{yeux}</div>
  <div class="haut"><div class="pile">{titres}</div></div>
  <figure class="plaque">{objets}</figure>
  <span class="socle-ombre"></span>
  <div class="bas"><div class="pile">{chiffres}</div></div>
  <div class="pile pile-note">{notes}</div>
  <aside class="fig-objet"><div class="pile">{legendes}</div></aside>
  <div class="pupitre">
    <nav class="pup-nav" aria-label="Findings">{pupitre}</nav>
    <div class="pied-nuit"><span>On your records, on your machine.
      <b>Nothing leaves the network.</b></span>
      <nav class="annexes" aria-label="Appendices">"""
    + "".join(f'<a class="b-lien" href="{h}">{a}</a>'
              for h, a in zip(["ANNEXE-METHODE.html", "ANNEXE-SECURITE.html",
                               "ANNEXE-QUESTIONS.html", "ANNEXE-TERMS.html",
                               "ANNEXE-PRIVACY.html", "ANNEXE-ACCESSIBILITE.html"],
                              bn.ANNEXES))
    + '<a class="b-lien" href="CONTACT.html">Contact</a>'
    + '<a class="b-lien" href="MENTIONS.html">Colophon</a>' 
    + """</nav></div>
  </div>
</div>
""" + SCRIPT + "\n", encoding="utf-8")
print("  HERO.html — l'outil complet, cinq etats")
