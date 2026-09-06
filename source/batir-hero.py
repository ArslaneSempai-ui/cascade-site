#!/usr/bin/env python3
"""LA PAGE D'ACCUEIL, refonte du 3 septembre : une seule page qui se scrolle.

CE QU'ARSLANE A ARRÊTÉ (maquette M1A, validée écran par écran)
  · le héros nuit : la question en Literata géant, le lede en deux lignes,
    le bloc commande centré, l'indication de scroll ;
  · la séquence : le rail-filmstrip à l'encre verte à gauche (vignettes des
    cinq états), le plateau 3D annoté au centre, la fiche en colonne à droite ;
    le design 3D garde sa taille et sa place, c'est l'intérieur qui change ;
  · le film : l'affiche du master, lecture sur YouTube ;
  · la couture papier au double filet entre les deux blocs nuit ;
  · l'instrument : la table de routage, le bouton fantôme en bas à droite ;
  · les annexes en tuiles, le pied nuit.

CE QUE CETTE PAGE REFUSE
  · le tiret cadratin, nulle part (assembler.py porte le refus mécanique) ;
  · un chiffre tapé : la table vient de landing.json de l'outil, l'hypothèse
    humaine de assumptions.ts, le compte de tests du README : si une source
    manque, la bâtisse s'arrête au lieu de recopier ;
  · une boîte de scène qui perd son ratio : les annotations (repère viewBox)
    et leurs chips (pour cent de la boîte) divergeraient : hauteur bornée par
    la place disponible, ratio 1.42 tenu ;
  · une page morte sans JavaScript : sans lui, la séquence se déplie en
    colonne statique, tout se lit.
"""
import json
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).parent
OUTIL = pathlib.Path.home() / "Documents" / "cascade"

# ── les sources, avec témoins : pas de source, pas de page ───────────────────
if not (OUTIL / "landing.json").exists():
    sys.exit(f"landing.json introuvable dans {OUTIL} : la table ne se tape pas, elle se lit")
LANDING = json.loads((OUTIL / "landing.json").read_text())

_assomptions = (OUTIL / "src" / "assumptions.ts").read_text()
_m = re.search(r"humanAccuracy:\s*(0\.\d+),", _assomptions)
if not _m:
    sys.exit("l'hypothèse humanAccuracy est introuvable dans assumptions.ts : refus de l'inventer")
HUMAIN = float(_m.group(1)) * 100          # 85.0 : une hypothèse déclarée, jamais mesurée

_m = re.search(r"\*\*(\d+) tests\*\* across (\d+) files", (OUTIL / "README.md").read_text())
if not _m:
    sys.exit("le compte de tests est introuvable dans le README de l'outil : refus de le recopier")
N_TESTS, N_FICHIERS = _m.group(1), _m.group(2)

from outil import SCEAU_ROUTING, etiquette_sur_objet, SEUIL_OBJET
SCEAU = SCEAU_ROUTING   # lu dans le relevé scellé du vert, jamais tapé (8/09)
DEPOT_URL = "https://github.com/ArslaneSempai-ui/cascade-routing"


def qte(v):
    """96.6 -> « 96.6 », 100.0 -> « 100 », 0 -> « 0 » : la valeur du relevé, sans zéro de traîne."""
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


# ── la table de l'instrument : GÉNÉRÉE depuis landing.json, jamais tapée ─────
CHAMPS = LANDING["fields"]
_tiers = LANDING["tiers"]
PALIERS = [t["id"] for t in _tiers if t["id"] != "human"] + ["human*"]
ROUTAGE = {c: [t["id"] for t in _tiers].index(LANDING["routing"]["fields"][c]) for c in CHAMPS}
_n_socle = {t["n"] for t in _tiers[:3]}
_n_gen = {t["n"] for t in _tiers if t["id"].startswith("gen-")}
assert len(_n_socle) == 1 and len(_n_gen) == 1, "les n des paliers ne sont plus homogènes"
N_SOCLE, N_GEN = _n_socle.pop(), _n_gen.pop()


def table_html():
    tetes = "".join(f"<th scope='col'>{p}</th>" for p in PALIERS)
    lignes = ""
    for c in CHAMPS:
        cells = ""
        for j, t in enumerate(_tiers):
            if t["id"] == "human":
                v = qte(HUMAIN)
            else:
                v = qte(t["acc"][c]["accuracy"])
            choisi = " choisi" if ROUTAGE[c] == j else ""
            cells += f"<td class='cell{choisi}'><span>{v}<small>%</small></span></td>"
        lignes += f"<tr><th scope='row'>{c}</th>{cells}</tr>"
    return f'''<div class="t-scroll"><table class="routage">
      <caption class="sr">Accuracy of each tier on each field, measured on held-out records</caption>
      <thead><tr><th scope="col">field</th>{tetes}</tr></thead><tbody>{lignes}</tbody></table></div>
      <p class="t-note">Measured on {N_SOCLE:,} held-out records for rules, small, large; {N_GEN} for the
      generative tiers. *The human tier is assumed at {qte(HUMAIN)}% until you measure it:
      <code>npm run measure:humans</code> grades your own reviewers. Green cells mark the
      published routing.</p>'''


# ── le contenu de la séquence : les cinq trouvailles, mot pour mot du publié ─
SCENES = [
    dict(num="01", titre="The gap",
         phrase="Both numbers are true. Only one leaves your desk.",
         a="94.4<small>%</small>", b="76.7<small>%</small>", cote="17.7 points apart"),
    dict(num="02", titre="The cheaper routing",
         phrase="Cost separates the two routings. Accuracy does not.",
         a="$191", b="$54", cote="3.5&#215; cheaper"),
    dict(num="03", titre="Silence over a guess",
         phrase="A blank gets read again. A wrong value gets filed.",
         a="30<small>%</small>", b="62.3<small>%</small>", cote="after abstention"),
    dict(num="04", titre="What we withhold",
         phrase="Every count held across two passes. Every duration moved.",
         a="identical", b="16&#8211;60<small>%</small>", cote="withheld"),
    dict(num="05", titre="The engagement",
         phrase="Every routing enumerated. One report you can argue with.",
         a="16,807", b="120<small>&nbsp;files</small>", cote="the full span"),
]

LEGS = [
    ("The dashboard mean.",
     "All five fields, correct. The number the desk works from."),
    ("What the published routing costs, per 100,000 documents.",
     "The routing aimed at the file. No file comes out worse."),
    ("When every value is delivered, right or wrong.",
     "When the tool stays silent instead of guessing."),
    ("Every count, run twice, to the digit.",
     "Every duration moved. So durations stay withheld."),
    ("Every routing tried, end to end. Not a sample.",
     f"Held out and frozen, {N_TESTS} tests counted on your machine."),
]

# ── les annotations du plateau : géométrie vérifiée sur les rendus ───────────
# Rangée du fond = rules (2 zéros orange : name à gauche, address à droite, 3 verts
# publiés entre) ; vert gauche-centre = name vers large ; canal creux = l'humain.
# Chaque phrase sort du site ou de l'outil publiés, rien d'inventé.
APPELS = [
    [
        (0.505, 0.30, 0.68, 0.05, "one chip: ten points of measured accuracy"),
        (0.21, 0.42, 0.04, 0.10, "the published pick: name goes to the large reader"),
        (0.70, 0.70, 0.80, 0.94, "the empty row: the human tier, never sampled"),
    ],
    [
        (0.30, 0.625, 0.09, 0.88, "name changes reader: the file-aimed pick"),
        (0.21, 0.42, 0.04, 0.10, "the published pick it replaces"),
        (0.417, 0.138, 0.60, 0.05, "a pick both routings share"),
    ],
    [
        (0.135, 0.30, 0.05, 0.09, "an emptied cell: silence instead of a wrong value"),
        (0.522, 0.172, 0.66, 0.06, "85 wrong values removed, 12 right lost"),
    ],
    [
        (0.33, 0.86, 0.10, 0.95, "run twice: every count identical, to the digit"),
        (0.55, 0.35, 0.73, 0.08, "nothing turns green: the durations moved, withheld"),
    ],
    [
        (0.47, 0.40, 0.70, 0.06, "every stack green: 16,807 routings crossed"),
        (0.70, 0.70, 0.80, 0.94, "still empty: the human tier, never sampled"),
    ],
]

# l'image (1374x1120) posée en contain dans la boîte 1.42:1 (viewBox 1420x1000) ;
# la boîte DOIT garder ce ratio (height + aspect-ratio), sinon chips et lignes divergent
IH, IW = 1000.0, 1000.0 * (1374 / 1120)
MX = (1420 - IW) / 2


APPEL_MAX = 60   # caractères : deux lignes dans une chip .ap-eti, jamais trois (Arslane, 8/09 : « 2 lignes max »)


def verifier_appel(txt, ou):
    """Une explication en transparence sur un plateau tient en DEUX lignes, sur toutes les
    couleurs ; au-delà, la chip couvre l'objet qu'elle explique. La règle est mécanique :
    une étiquette trop longue ne se bâtit pas. Le maximum publié tenait en 59."""
    if len(txt) > APPEL_MAX:
        sys.exit(f"annotation trop longue ({len(txt)} > {APPEL_MAX}) sur {ou} : « {txt} » ; deux lignes max")
    if not txt.strip():
        sys.exit(f"annotation vide sur {ou}")
    return txt


def appels_html(i):
    lignes, etiquettes = "", ""
    for (ax, ay, lx, ly, txt) in APPELS[i]:
        verifier_appel(txt, f"routing, scène {i + 1}")
        # l'étiquette sur le crème, jamais sur l'objet (Arslane, 9/09) : même garde que les quatre outils
        image_v = BASE / "rendus" / "etats" / f"objet-0{i + 1}.webp"
        if image_v.exists() and (BASE / "rendus" / "sequences" / "objet" / "manifest.json").exists():
            part = etiquette_sur_objet(image_v, lx, ly)
            if part > SEUIL_OBJET:
                sys.exit(f"routing, scène {i + 1} : l'étiquette « {txt} » couvre l'objet ({part:.0%}) : la poser sur le crème")
        x1, y1 = MX + lx * IW, ly * IH
        x2, y2 = MX + ax * IW, ay * IH
        lignes += (f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" pathLength="1"/>'
                   f'<circle cx="{x2:.0f}" cy="{y2:.0f}" r="4"/>')
        etiquettes += (f'<span class="ap-eti" style="left:{x1 / 14.20:.1f}%;top:{y1 / 10.0:.1f}%">{txt}</span>')
    return (f'<svg class="appels" viewBox="0 0 1420 1000" aria-hidden="true">{lignes}</svg>{etiquettes}')


def scene_html(i, s):
    return f'''
    <div class="scene{' actif' if i == 0 else ''}" id="scene-{i}" data-i="{i}">
      <img class="objet" src="rendus/etats/objet-{s['num']}.webp"
        alt="The measured relief, state {s['num']}: {s['titre']}">
      {appels_html(i)}
      <figure class="fiche">
        <figcaption class="fiche-t"><span>finding {s['num']}</span><span class="ft-cote">{s['cote']}</span></figcaption>
        <p class="fiche-phrase">{s['phrase']}</p>
        <div class="paire">
          <div class="val"><span class="chiffre pale-v">{s['a']}</span><span class="leg">{LEGS[i][0]}</span></div>
          <div class="val"><span class="chiffre vert-v">{s['b']}</span><span class="leg">{LEGS[i][1]}</span></div>
        </div>
      </figure>
    </div>'''


def rail_html():
    items = "".join(
        f'''<li><button class="jalon{' actif' if i == 0 else ''}" data-i="{i}" aria-label="Go to finding {s['num']}: {s['titre']}">
        <img class="j-vig" src="rendus/etats/objet-{s['num']}.webp" alt="">
        <span class="j-num">{s['num']}</span><span class="j-corps"><span class="j-titre">{s['titre']}</span>
        <span class="j-cote">{s['cote']}</span></span></button></li>''' for i, s in enumerate(SCENES))
    return f'<nav class="rail" aria-label="Findings"><span class="jauge" aria-hidden="true"><i></i></span><ul>{items}</ul></nav>'


MENUS = [
    ("methode", "Method &amp; reproducibility", "One method, no secrets. Run it twice, compare.", "ANNEXE-METHODE.html"),
    ("securite", "Security &amp; data handling", "Every place the tool touches.", "ANNEXE-SECURITE.html"),
    ("questions", "Questions", "Eight objections a bank's reviewers actually raise.", "ANNEXE-QUESTIONS.html"),
    ("terms", "Terms of engagement", "What the grant allows, for how long, and what a client buys.", "ANNEXE-TERMS.html"),
    ("privacy", "Privacy", "No data is collected. Written down, and verifiable.", "ANNEXE-PRIVACY.html"),
    ("accessibilite", "Accessibility", "Usable by keyboard, by screen reader, and with motion turned off.", "ANNEXE-ACCESSIBILITE.html"),
]


def menus_html():
    tuiles = "".join(f'''
      <a class="tuile" href="{href}">
        <span class="tuile-img"><img src="rendus/etats/objet-{cle}.webp" alt=""></span>
        <span class="tuile-corps"><span class="tuile-t">{titre}</span>
        <span class="tuile-d">{desc}</span></span>
        <span class="tuile-fl" aria-hidden="true">&#8594;</span>
      </a>''' for cle, titre, desc, href in MENUS)
    return f'''<section class="menus"><div class="colonne">
      <h2 class="h2">The appendices your reviewers will ask for.</h2>
      <div class="grille">{tuiles}</div>
      <div class="rangee-fine">
        <a class="lien-fin" href="ENGAGEMENT.html">Pricing, in figures <span aria-hidden="true">&#8594;</span></a>
        <a class="lien-fin" href="CONTACT.html">Contact <span aria-hidden="true">&#8594;</span></a>
        <a class="lien-fin" href="MENTIONS.html">The fine print <span aria-hidden="true">&#8594;</span></a>
        <a class="lien-fin" href="{DEPOT_URL}">The repository, public <span aria-hidden="true">&#8594;</span></a>
      </div></div></section>'''


# ── la mise en dépliage : partagée par le petit écran ET l'absence de script ─
DEPLIE = '''
    .sequence{height:auto}
    .colle{position:static;height:auto;flex-direction:column;padding:60px 22px;gap:28px}
    .rail{width:100%}
    .rail ul{flex-direction:row;flex-wrap:wrap;gap:2px 14px}
    .jalon{padding:8px 0 8px 10px}
    .jalon .j-titre{font-size:15px}
    .j-vig{display:none}
    .appels,.ap-eti{display:none}
    .scenes{aspect-ratio:auto;height:auto;margin:0;position:static}
    .scene{position:static;opacity:1;transform:none;pointer-events:auto;margin-bottom:44px}
    .scene .objet{position:static;height:auto}
    .scene .fiche{position:static;transform:none;width:100%;margin:0}
'''

CSS = '''
  :root{--papier:#dbd7c5;--papier-haut:#e2ddcb;--papier-bas:#cdccb9;--encre:#1b1d18;
    --demi:#4a4739;--pale:#55523f;--filet:#9d9a83;--filet-clair:#bab7a0;
    --nuit-a:#1b3229;--nuit-b:#14251e;--nuit-c:#0e1a15;--sur-vert:#e4ecdf;--sur-vert-pale:#a9bdaf;
    --vert-titre:#23543f;--vert-vif:#57b184;--vert-clair:#a5f7cb;
    --texte:"Literata",Georgia,serif;--mono:"Roboto Mono",ui-monospace,Menlo,monospace;
    --sans:ui-sans-serif,-apple-system,"Helvetica Neue",sans-serif;
    --montee:cubic-bezier(.16,.84,.32,1)}
  *{box-sizing:border-box;margin:0}
  html{scroll-behavior:smooth}
  @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
  body{background:var(--papier);color:var(--encre);font-family:var(--texte);line-height:1.55}
  img{max-width:100%;display:block}
  ::selection{background:var(--vert-titre);color:var(--sur-vert)}
  html{caret-color:var(--vert-vif);scrollbar-color:var(--vert-titre) var(--papier-bas)}
  a{text-underline-offset:4px;color:inherit}
  .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
  :focus-visible{outline:3px solid var(--vert-vif);outline-offset:3px;border-radius:2px}
  .colonne{max-width:1180px;margin:0 auto;padding:0 48px}
  .h2{font-size:clamp(28px,3.2vw,44px);font-weight:600;letter-spacing:-.015em;
    line-height:1.08;text-wrap:balance;margin:0 0 .8em}

  /* la barre */
  .barre{position:fixed;inset:0 0 auto 0;z-index:40;display:flex;align-items:center;gap:28px;
    padding:14px 32px;transition:background .3s,box-shadow .3s}
  .barre.posee{background:color-mix(in srgb,var(--papier-haut) 88%,transparent);
    backdrop-filter:blur(10px);box-shadow:0 1px 0 color-mix(in srgb,var(--filet) 55%,transparent)}
  .barre.sur-nuit .marque{color:var(--sur-vert)}
  .barre.sur-nuit nav a{color:var(--sur-vert-pale)}
  .barre.sur-nuit nav a:hover{color:var(--sur-vert)}
  .barre.sur-nuit .sceau{color:var(--sur-vert-pale)}
  .marque{font-weight:700;font-size:19px;letter-spacing:.01em;text-decoration:none;padding:10px 0}
  .barre nav{display:flex;gap:16px;margin-left:auto}
  .barre nav a{font-size:14.5px;text-decoration:none;color:var(--demi);padding:13px 6px}
  .barre nav a:hover{color:var(--encre);text-decoration:underline;
    text-decoration-color:var(--vert-vif);text-decoration-thickness:1.5px}
  .sceau{font-family:var(--mono);font-size:11px;color:var(--pale);letter-spacing:.04em}
  html:not(.js) .barre{position:absolute}
  html:not(.js) .barre .marque{color:var(--sur-vert)}
  html:not(.js) .barre nav a{color:var(--sur-vert-pale)}
  html:not(.js) .barre .sceau{color:var(--sur-vert-pale)}

  /* le héros */
  .hero{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;
    text-align:center;gap:26px;padding:120px 24px 130px;position:relative;color:var(--sur-vert);
    background:radial-gradient(130% 105% at 50% -18%,var(--nuit-a),var(--nuit-b) 50%,var(--nuit-c))}
  .hero .lede{color:var(--sur-vert-pale);margin-top:32px;max-width:87ch;text-wrap:wrap}
  .hero .lede b{color:var(--sur-vert)}
  .hero .commande{margin-top:34px;background:color-mix(in srgb,var(--nuit-a) 52%,transparent);
    border-color:color-mix(in srgb,var(--vert-vif) 34%,transparent);
    box-shadow:0 26px 70px rgba(0,0,0,.5)}
  .hero .cue{color:var(--sur-vert-pale)}
  .marque-h{font-family:var(--mono);font-size:12px;letter-spacing:.22em;text-transform:uppercase;
    color:var(--sur-vert-pale)}
  .h1{font-size:clamp(44px,7vw,92px);font-weight:600;letter-spacing:-.02em;line-height:1.02;
    text-wrap:balance;max-width:14ch}
  .lede{font-size:clamp(16px,1.35vw,19px);color:var(--demi);max-width:78ch;line-height:1.6;text-wrap:balance}
  .lede b{color:var(--encre)}
  .commande{background:var(--nuit-b);color:var(--sur-vert);border:1px solid color-mix(in srgb,var(--vert-vif) 40%,transparent);
    border-radius:10px;padding:18px 26px;text-align:left;font-family:var(--mono);font-size:12.5px;
    box-shadow:0 24px 60px rgba(14,26,21,.28);max-width:min(92vw,680px)}
  /* une commande longue se REPLIE au lieu de glisser sous un ascenseur invisible : la
     troisième ligne du bleu (deux fichiers) dépassait la boîte à 1440 sans aucun indice ;
     les commandes courtes du vert et du rouge tiennent sur leur ligne, rien ne bouge pour elles */
  .commande .ln{white-space:normal;overflow-wrap:anywhere;display:block;padding:2px 0}
  .commande .ln::before{content:"$ ";color:var(--vert-vif)}
  .commande .note{display:block;margin-top:8px;font-size:11px;color:var(--sur-vert-pale);text-align:center;
    font-family:var(--sans);letter-spacing:.02em}
  .entree{opacity:0;transform:translateY(18px);animation:lever .7s var(--montee) forwards}
  .entree:nth-child(2){animation-delay:.08s}.entree:nth-child(3){animation-delay:.16s}
  .entree:nth-child(4){animation-delay:.24s}
  @keyframes lever{to{opacity:1;transform:none}}
  html:not(.js) .entree{animation:none;opacity:1;transform:none}
  .cue{position:absolute;bottom:24px;left:50%;transform:translateX(-50%);display:flex;
    flex-direction:column;align-items:center;gap:10px;font-family:var(--mono);font-size:10.5px;
    letter-spacing:.22em;text-transform:uppercase;color:var(--pale)}
  .cue .fil{position:relative;width:1px;height:44px;overflow:hidden;
    background:color-mix(in srgb,currentColor 35%,transparent)}
  .cue .fil::after{content:"";position:absolute;left:-1px;top:-10px;width:3px;height:10px;
    border-radius:2px;background:var(--vert-vif);animation:cue 2.2s cubic-bezier(.4,0,.6,1) infinite}
  @keyframes cue{70%,100%{transform:translateY(54px)}}
  @media (prefers-reduced-motion:reduce){.entree{animation:none;opacity:1;transform:none}
    .cue .fil::after{animation:none;top:0}}

  /* le rideau : le deuxième écran, un pan par outil dans SES couleurs (posées en
     variables sur le pan, pas dans la palette de la page), le courant marqué */
  .rideau{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));
    position:relative;color:var(--sur-vert)}
  /* cinq pierres : à 340 px de pan minimum, 1440 n'en range que quatre et le cinquième
     tombe seul sur une deuxième rangée (vu le 8/09 sur toutes les pages). Dès 1200 px les
     cinq tiennent sur une rangée à 240 px ; en dessous, trois puis deux (rangées entières). */
  @media (min-width:1200px){.rideau{grid-template-columns:repeat(auto-fit,minmax(min(100%,235px),1fr))}}
  .rideau-titre{position:absolute;top:84px;left:0;right:0;z-index:2;text-align:center;padding:0 24px;
    font-family:var(--mono);font-size:11.5px;letter-spacing:.22em;text-transform:uppercase;
    color:var(--sur-vert-pale)}
  .pan{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
    gap:16px;min-height:100vh;padding:130px 40px 80px;text-decoration:none;color:inherit;outline-offset:-6px;
    background:radial-gradient(120% 100% at 50% -10%,var(--pan-a),var(--pan-b) 55%,var(--pan-c))}
  .pan img{height:clamp(150px,24vh,230px);width:auto;filter:drop-shadow(0 20px 36px rgba(0,0,0,.55));
    transition:transform .35s var(--montee)}
  .pan .p-eti{font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;
    color:var(--pan-vif)}
  .pan .p-h{font-size:clamp(28px,3.4vw,50px);font-weight:600;line-height:1.05;letter-spacing:-.02em;
    text-wrap:balance;max-width:14ch;display:flex;align-items:center;justify-content:center;min-height:3.2em}
  .pan .p-d{font-size:15px;color:var(--sur-vert-pale);max-width:38ch;line-height:1.5}
  .pan .p-ouvrir{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
    margin-top:8px;padding:10px 16px;border-radius:8px;transition:background .2s,color .2s;
    border:1px solid color-mix(in srgb,var(--sur-vert) 30%,transparent)}
  a.pan:hover .p-ouvrir,a.pan:focus-visible .p-ouvrir{background:var(--sur-vert);color:var(--nuit-c)}
  .pan[aria-current] .p-ouvrir{border-style:dashed;color:var(--sur-vert-pale)}
  /* le survol d'un pan (Arslane, 6/09) : un halo de SA couleur qui suit la souris,
     le robot qui se soulève, la question qui monte d'un souffle, l'autre pan qui
     s'assombrit ; au clavier, le focus donne le même halo, centré */
  .pan{position:relative;isolation:isolate}
  .pan::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:0;z-index:0;
    transition:opacity .4s var(--montee);
    background:radial-gradient(560px 460px at var(--mx,50%) var(--my,42%),
      color-mix(in srgb,var(--pan-vif) 26%,transparent),transparent 70%)}
  .pan>*{position:relative;z-index:1}
  a.pan:hover::before,a.pan:focus-visible::before{opacity:1}
  a.pan:hover{box-shadow:inset 0 0 0 2px color-mix(in srgb,var(--pan-vif) 60%,transparent)}
  a.pan:hover img{transform:translateY(-12px) scale(1.04)}
  a.pan:hover .p-h{transform:translateY(-4px)}
  a.pan:hover .p-eti{text-shadow:0 0 18px color-mix(in srgb,var(--pan-vif) 80%,transparent)}
  /* l'autre pan s'assombrit (un filtre, pas une opacité : en transparence il
     laissait voir le parchemin et virait au gris délavé, vu sur capture) */
  .pan{transition:transform .8s var(--montee),opacity .8s var(--montee),filter .45s var(--montee)}
  .rideau:has(a.pan:hover) .pan:not(:hover){filter:brightness(.72) saturate(.85)}
  /* l'entrée et l'ouverture du rideau (Arslane, 6/09 : « le slide de l'écran 1 à 2
     n'a rien de spécial ») : les pans arrivent des deux côtés quand le rideau
     entre dans la vue, et s'écartent au clic avant d'ouvrir l'outil ; sans script,
     rien ne bouge et les pans sont des liens */
  .rideau{overflow:hidden;background:var(--ouverture,var(--papier))}   /* derrière les pans : la nuit de l'outil qu'on ouvre */
  .pan{transition:transform .8s var(--montee),opacity .8s var(--montee)}
  .rideau .p-h,.rideau img,.rideau .p-d,.rideau .p-ouvrir,.rideau .p-eti{transition:transform .9s var(--montee),opacity .9s}
  html.js .rideau:not(.vu) .cote-g{transform:translateX(-18%);opacity:0}
  html.js .rideau:not(.vu) .cote-d{transform:translateX(18%);opacity:0}
  html.js .rideau:not(.vu) .pan img{transform:translateY(28px);opacity:0}
  html.js .rideau.vu .pan img{transition-delay:.25s}
  .rideau.ouvre .cote-g{transform:translateX(-102%)}
  .rideau.ouvre .cote-d{transform:translateX(102%)}
  .rideau.ouvre .rideau-titre{opacity:0;transition:opacity .3s}

  /* la séquence : rail-filmstrip, plateau annoté, fiche colonne */
  .sequence{height:560vh;position:relative}
  /* L'OBJET PREND LA PLACE (Arslane, 9/09 : « agrandir l'objet dans le héros », comme le
     prototype de la chorégraphie où la scène faisait 56 vw) : le rail passe de 380 à 290 px (vignettes 60, titres 17),
     l'écart et les marges se resserrent, la scène monte à 62 vh ; la réserve de la formule
     ci-dessous = écart 32 + fiche 270 + marges 64 = 366 px, sur une largeur plafonnée à 1400. */
  .colle{position:sticky;top:0;height:100vh;display:flex;align-items:center;gap:min(3vw,32px);
    padding:80px 32px 40px;max-width:1400px;margin:0 auto}
  .rail{width:min(290px,22vw);flex:none;position:relative;padding-left:18px}
  .rail .jauge{position:absolute;left:0;top:6px;bottom:6px;width:3px;
    background:color-mix(in srgb,var(--vert-titre) 25%,transparent);border-radius:1px}
  .rail .jauge i{position:absolute;left:0;top:0;width:100%;height:0%;
    background:var(--vert-vif);border-radius:1px}
  .rail ul{list-style:none;padding:0;display:flex;flex-direction:column;gap:4px}
  .jalon{display:flex;gap:16px;align-items:center;width:100%;text-align:left;background:none;
    border:0;border-left:3px solid transparent;padding:12px 0 12px 16px;cursor:pointer;
    font-family:var(--texte);color:color-mix(in srgb,var(--vert-titre) 80%,var(--pale));
    transition:color .25s,border-color .25s,background .25s}
  .j-vig{display:block;width:60px;aspect-ratio:1.42/1;object-fit:contain;flex:none;align-self:center;
    filter:grayscale(.65) drop-shadow(0 4px 6px rgba(27,29,24,.18));opacity:.5;transform:scale(.94);
    transition:opacity .3s,filter .3s,transform .3s var(--montee)}
  .jalon.actif .j-vig{filter:drop-shadow(0 6px 10px rgba(27,29,24,.25));opacity:1;transform:scale(1.06)}
  .jalon .j-num{font-family:var(--mono);font-size:12px;letter-spacing:.1em;
    color:color-mix(in srgb,var(--vert-titre) 90%,transparent)}
  .jalon.actif .j-num{color:var(--vert-vif)}
  .jalon .j-titre{display:block;font-size:17px;font-weight:600;letter-spacing:-.01em;line-height:1.18}
  .jalon:hover{color:var(--vert-titre)}
  .jalon.actif{color:var(--vert-titre);border-left-color:var(--vert-vif);
    background:linear-gradient(90deg,color-mix(in srgb,var(--vert-vif) 12%,transparent),transparent 72%);
    border-radius:0 10px 10px 0}
  .j-cote{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.1em;
    text-transform:uppercase;color:var(--vert-vif);margin-top:6px;opacity:0;max-height:0;
    overflow:hidden;transition:opacity .3s,max-height .3s}
  .jalon.actif .j-cote{opacity:1;max-height:2em}
  .theatre{flex:1;min-width:0;position:relative;display:flex;flex-direction:column;gap:20px}
  .scenes{position:relative;aspect-ratio:1.42/1;width:auto;margin:0 auto 0 0;
    height:min(62vh,calc((min(100vw,1400px) - min(290px,22vw) - 366px)/1.42))}
  .scene{position:absolute;inset:0;opacity:0;transform:translateY(14px);
    transition:opacity .45s var(--montee),transform .45s var(--montee);pointer-events:none}
  .scene.actif{opacity:1;transform:none;pointer-events:auto}
  .scene .objet{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;
    filter:drop-shadow(0 30px 40px rgba(27,29,24,.22))}
  .scene .fiche{position:absolute;left:100%;top:50%;right:auto;bottom:auto;
    transform:translateY(-50%);margin-left:20px;width:250px}

  /* les annotations : lignes d'épure, chips vert translucide, 2 lignes max */
  .appels{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
  .appels line{stroke:color-mix(in srgb,var(--vert-vif) 70%,transparent);stroke-width:1.5;
    vector-effect:non-scaling-stroke;stroke-dasharray:1;stroke-dashoffset:1;
    transition:stroke-dashoffset .7s .25s var(--montee)}
  .appels circle{fill:color-mix(in srgb,var(--vert-vif) 80%,transparent)}
  .scene.actif .appels line{stroke-dashoffset:0}
  .ap-eti{position:absolute;transform:translate(-50%,-50%);width:max-content;max-width:240px;
    text-wrap:balance;font-family:var(--mono);font-size:11.5px;line-height:1.45;
    color:var(--vert-titre);background:color-mix(in srgb,var(--vert-vif) 13%,transparent);
    backdrop-filter:blur(3px);padding:5px 9px;
    border:1px solid color-mix(in srgb,var(--vert-vif) 32%,transparent);
    border-radius:6px;opacity:0;transition:opacity .4s .55s;pointer-events:none}
  .scene.actif .ap-eti{opacity:1}

  /* la fiche : Literata partout, une seule ligne mono */
  .fiche{background:linear-gradient(180deg,color-mix(in srgb,var(--nuit-b) 96%,transparent),
      color-mix(in srgb,var(--nuit-a) 92%,transparent));
    border:1px solid color-mix(in srgb,var(--vert-vif) 42%,transparent);border-radius:12px;
    color:var(--sur-vert);padding:16px 22px 14px;box-shadow:0 18px 50px rgba(14,26,21,.32)}
  .fiche-t{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
    color:var(--sur-vert-pale);border-bottom:1px solid color-mix(in srgb,var(--sur-vert-pale) 25%,transparent);
    padding-bottom:8px;margin-bottom:12px;display:flex;flex-direction:column;gap:4px;align-items:flex-start}
  .ft-cote{color:var(--vert-clair)}
  .fiche-phrase{font-size:16.5px;font-style:italic;color:var(--sur-vert);line-height:1.4;
    margin:0 0 14px;text-wrap:balance}
  .paire{display:grid;grid-template-columns:1fr;gap:14px}
  .val{min-width:0}
  .chiffre{font-family:var(--texte);font-weight:600;font-size:clamp(26px,2.6vw,40px);display:block;
    font-variant-numeric:lining-nums tabular-nums;letter-spacing:-.01em}
  .chiffre small{font-size:.55em;font-weight:400}
  .pale-v{color:var(--sur-vert-pale)}
  .vert-v{color:var(--vert-clair);text-shadow:0 0 18px color-mix(in srgb,var(--vert-vif) 55%,transparent)}
  .fiche .leg{display:block;font-family:var(--texte);font-size:13px;color:var(--sur-vert-pale);
    margin-top:5px;line-height:1.5}

  /* le film */
  .film{padding:110px 0 120px;color:var(--sur-vert);
    background:linear-gradient(180deg,var(--nuit-a),var(--nuit-b))}
  .film .h2{color:var(--sur-vert)}
  .film-duree{text-align:center;font-family:var(--mono);font-size:12px;letter-spacing:.1em;color:var(--vert-clair);
    text-transform:uppercase;margin:-.4em 0 1.6em}
  .lecteur{position:relative;display:block;border-radius:16px;overflow:hidden;
    border:1px solid color-mix(in srgb,var(--vert-vif) 30%,transparent);
    box-shadow:0 34px 90px rgba(0,0,0,.55);cursor:pointer}
  .lecteur img{width:100%;transition:transform .4s var(--montee)}
  .lecteur:hover img{transform:scale(1.02)}
  .lecteur .jouer{position:absolute;inset:0;margin:auto;width:92px;height:92px;border-radius:50%;
    background:color-mix(in srgb,var(--nuit-c) 68%,transparent);backdrop-filter:blur(6px);
    border:1.5px solid var(--vert-clair);display:flex;align-items:center;justify-content:center;
    transition:transform .25s var(--montee),background .25s}
  .lecteur:hover .jouer{transform:scale(1.1);background:color-mix(in srgb,var(--vert-titre) 70%,transparent)}
  .lecteur .jouer svg{margin-left:6px}
  .lecteur .duree{position:absolute;right:16px;bottom:14px;font-family:var(--mono);font-size:12px;
    letter-spacing:.08em;color:var(--sur-vert);background:color-mix(in srgb,var(--nuit-c) 72%,transparent);
    padding:5px 10px;border-radius:6px}
  .film-note{display:flex;justify-content:flex-end;gap:16px;flex-wrap:wrap;margin-top:16px;
    font-size:14px;color:var(--sur-vert-pale)}
  .film-note .ou{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase}
  /* l'affiche composée : la place du film d'un outil AVANT que sa vidéo existe
     (Arslane, 6/09 : « une partie pour mettre une vidéo sur toutes les couleurs »).
     Le robot penché de l'outil, sa question, sa nuit ; le jour venu, l'affiche
     rendue remplace la composition, le lecteur et la note ne bougent pas. */
  .lecteur .affiche{display:block;aspect-ratio:16/9;position:relative;overflow:hidden;
    background:radial-gradient(120% 120% at 82% 105%,var(--nuit-a),var(--nuit-c) 70%)}
  .lecteur .affiche img{position:absolute;right:5%;bottom:-9%;width:34%;height:auto;
    filter:drop-shadow(0 30px 60px rgba(0,0,0,.6))}
  .affiche .af-t{position:absolute;left:6%;top:14%;max-width:54%;color:var(--sur-vert)}
  .affiche .af-eti{display:block;font-family:var(--mono);font-size:clamp(10px,1vw,13px);
    letter-spacing:.2em;text-transform:uppercase;color:var(--vert-vif);margin-bottom:.9em}
  .affiche .af-q{display:block;font-size:clamp(20px,3.3vw,48px);font-weight:600;line-height:1.05;
    letter-spacing:-.02em;text-wrap:balance}
  /* sur l'affiche composée le bouton quitte le centre (il couvrait la question au
     téléphone, relu sur capture 375) : en bas à gauche, dans l'air sous le titre */
  .lecteur .affiche~.jouer{inset:auto auto 9% 6%;margin:0}
  @media (max-width:700px){.lecteur .affiche~.jouer{width:56px;height:56px}
    .lecteur .affiche~.jouer svg{width:18px;height:20px;margin-left:4px}}

  /* la couture : une bande de papier au double filet entre les deux blocs nuit */
  .couture{background:var(--papier);padding:56px 0}
  .couture .colonne{display:flex;align-items:center;gap:18px}
  .couture .filet{flex:1;border-top:3px double var(--filet)}
  .couture .sceau-c{font-family:var(--mono);font-size:11px;letter-spacing:.14em;
    text-transform:uppercase;color:var(--pale);white-space:nowrap}

  /* l'instrument */
  .instrument{padding:110px 0 120px;color:var(--sur-vert);
    background:linear-gradient(180deg,var(--nuit-b) 0%,var(--nuit-c) 100%)}
  .instrument .h2{color:var(--sur-vert)}
  .instrument .t-note{color:var(--sur-vert-pale)}
  .t-scroll{overflow-x:auto;border-radius:14px;box-shadow:0 30px 80px rgba(0,0,0,.5);
    border:1px solid color-mix(in srgb,var(--vert-vif) 26%,transparent)}
  .routage{width:100%;border-collapse:collapse;background:color-mix(in srgb,var(--nuit-a) 72%,var(--nuit-b));
    color:var(--sur-vert);font-family:var(--mono);font-size:13px;min-width:720px}
  .routage th,.routage td{padding:12px 14px;text-align:center;
    border:1px solid color-mix(in srgb,var(--sur-vert-pale) 14%,transparent)}
  .routage thead th{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--sur-vert-pale)}
  .routage tbody th{text-align:left;font-size:11px;letter-spacing:.1em;text-transform:uppercase;
    color:var(--sur-vert-pale)}
  .cell{transition:background .16s,box-shadow .16s}
  .cell:hover{background:color-mix(in srgb,var(--vert-vif) 12%,transparent);
    box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--vert-vif) 55%,transparent)}
  .cell.choisi{background:color-mix(in srgb,var(--vert-vif) 18%,transparent);color:var(--vert-clair);
    box-shadow:inset 0 0 0 1.5px var(--vert-vif)}
  .cell small{font-size:.7em;color:var(--sur-vert-pale)}
  .t-note{font-size:12.5px;color:var(--pale);margin-top:14px;max-width:none;line-height:1.55}
  /* le bandeau qui ouvre l'instrument, sous la vidéo (Arslane, 6/09 : « impressionnant,
     effet souris, sur chaque couleur ») : large, la couleur de l'outil en halo qui suit la
     souris, un éclat qui balaie, la flèche qui glisse dans son disque, la lueur qui monte ;
     au clavier le focus donne le même état, centré ; mouvement réduit : halo fixe */
  .ouvrir-ligne{display:flex;margin-top:40px}
  .ouvrir{position:relative;isolation:isolate;overflow:hidden;display:flex;align-items:center;gap:28px;
    width:100%;min-height:104px;padding:24px 28px 24px 34px;border-radius:16px;text-decoration:none;
    color:var(--sur-vert);font-family:var(--texte);
    background:linear-gradient(180deg,color-mix(in srgb,var(--nuit-a) 72%,var(--nuit-b)),var(--nuit-b));
    border:1px solid color-mix(in srgb,var(--vert-vif) 42%,transparent);
    transition:transform .4s var(--montee),border-color .3s,box-shadow .4s var(--montee)}
  .ouvrir::before{content:"";position:absolute;inset:0;z-index:0;opacity:0;transition:opacity .4s;
    background:radial-gradient(460px 280px at var(--mx,18%) var(--my,50%),
      color-mix(in srgb,var(--vert-vif) 16%,transparent),transparent 70%)}
  .ouvrir::after{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;
    background:linear-gradient(105deg,transparent 42%,color-mix(in srgb,var(--sur-vert) 5%,transparent) 50%,transparent 58%);
    transform:translateX(-130%)}
  .ouvrir>*{position:relative;z-index:1}
  .ouvrir-eti{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;
    color:var(--vert-vif);margin-bottom:8px}
  .ouvrir-t{display:block;font-size:clamp(21px,2.3vw,30px);font-weight:600;letter-spacing:-.012em;line-height:1.12}
  .ouvrir-s{display:block;margin-top:7px;font-size:14.5px;color:var(--sur-vert-pale);max-width:60ch}
  .ouvrir .fl{margin-left:auto;flex:none;width:68px;height:68px;border-radius:50%;display:grid;place-items:center;
    font-family:var(--sans);font-size:34px;line-height:1;color:var(--vert-clair);
    border:1px solid color-mix(in srgb,var(--vert-vif) 50%,transparent);
    transition:transform .4s var(--montee),background .3s,color .3s,border-color .3s}
  /* sobre (Arslane, 7/09 : « c'est moche, plus sobre pour toutes les couleurs ») : pas de
     disque plein ni de flèche qui tourne ; l'anneau s'éclaire, la flèche glisse, c'est tout */
  .ouvrir:hover,.ouvrir:focus-visible{transform:translateY(-2px);
    border-color:color-mix(in srgb,var(--vert-vif) 70%,transparent);
    box-shadow:0 22px 56px color-mix(in srgb,var(--vert-vif) 14%,transparent)}
  .ouvrir:hover::before,.ouvrir:focus-visible::before{opacity:1}
  .ouvrir:hover::after{transform:translateX(130%);transition:transform 1.1s var(--montee)}
  .ouvrir:hover .fl,.ouvrir:focus-visible .fl{transform:translateX(8px);
    border-color:var(--vert-vif);background:color-mix(in srgb,var(--vert-vif) 12%,transparent)}
  @media (max-width:700px){.ouvrir{gap:16px;padding:20px 20px 20px 22px}.ouvrir .fl{width:52px;height:52px;font-size:26px}
    .ouvrir-s{display:none}}

  /* les annexes en tuiles */
  .menus{padding:110px 0 90px;background:var(--papier)}
  .grille{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
  .tuile{display:flex;flex-direction:column;gap:0;background:var(--papier-haut);
    border:1px solid color-mix(in srgb,var(--filet) 55%,transparent);border-radius:14px;
    text-decoration:none;overflow:hidden;position:relative;
    transition:transform .2s var(--montee),border-color .2s,background .2s}
  .tuile:hover{transform:translateY(-2px);border-color:var(--vert-titre);
    background:color-mix(in srgb,var(--papier-haut) 60%,#fff)}
  .tuile-img{display:block;height:150px;overflow:hidden;
    background:radial-gradient(120% 90% at 50% 8%,#fff 0%,var(--papier-haut) 70%)}
  .tuile-img img{height:100%;width:100%;object-fit:contain;padding:14px;
    transition:transform .3s var(--montee)}
  .tuile:hover .tuile-img img{transform:scale(1.06)}
  .tuile-corps{padding:16px 18px 20px}
  .tuile-t{display:block;font-size:18px;font-weight:600;letter-spacing:-.01em}
  .tuile-d{display:block;font-size:13.5px;color:var(--demi);margin-top:6px;line-height:1.55}
  .tuile-fl{position:absolute;right:16px;bottom:14px;font-family:var(--sans);font-size:18px;
    color:var(--vert-titre);opacity:0;transform:translateX(-8px);
    transition:opacity .22s,transform .22s var(--montee)}
  .tuile:hover .tuile-fl{opacity:1;transform:none}
  .rangee-fine{display:flex;gap:14px;margin-top:18px;flex-wrap:wrap}
  .lien-fin{flex:1;min-width:180px;display:flex;justify-content:space-between;align-items:center;
    font-size:15px;text-decoration:none;color:var(--demi);
    border:1px solid color-mix(in srgb,var(--filet) 55%,transparent);border-radius:10px;
    padding:14px 18px;transition:border-color .2s,color .2s}
  .lien-fin:hover{border-color:var(--vert-titre);color:var(--encre)}

  /* le pied */
  .pied{background:var(--nuit-c);color:var(--sur-vert);padding:64px 0}
  .pied .colonne{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:baseline}
  .pied-p{font-size:clamp(18px,2vw,26px);font-weight:600;letter-spacing:-.01em}
  .pied-p em{font-style:italic;color:var(--vert-clair)}
  .pied .sceau{color:var(--sur-vert-pale)}

  @media (max-width:960px){
    .colonne{padding:0 22px}
    .barre{padding:12px 18px;gap:14px}
    .barre nav{display:none}
    .pan{min-height:62vh;padding:130px 24px 56px}
  }
  /* sous 700 px les pans s'empilent : seul le premier laisse la place au titre */
  @media (max-width:700px){
    .rideau{grid-template-columns:1fr}
    .pan{padding-top:84px}
    .rideau-titre+.pan{padding-top:124px}
    /* au téléphone, une commande coupée par un ascenseur horizontal se lit
       comme une commande cassée : elle se replie, entière */
    .commande .ln{white-space:normal;overflow-wrap:anywhere}
    .grille{grid-template-columns:1fr}
    .couture .sceau-c{white-space:normal;text-align:center}
  }
  /* fenêtre réduite (641-1080) : le théâtre colle n'a pas la place d'être digne,
     la séquence se déplie en colonne, comme au téléphone et sans script */
  @media (max-width:1080px){''' + DEPLIE + '''
  }
  /* entre 1081 et 1220, le plateau est trop petit pour porter ses annotations */
  @media (max-width:1220px){
    .appels,.ap-eti{display:none!important}
  }
NOJS
  @media (prefers-reduced-motion:reduce){
    *{transition-duration:.01ms!important;animation-duration:.01ms!important}}
'''


def _prefixe_nojs(css):
    """Chaque sélecteur du dépliage préfixé html:not(.js) : sans script, la page se déplie."""
    def f(m):
        sels = ",".join("html:not(.js) " + s.strip() for s in m.group(2).split(","))
        return m.group(1) + sels + "{"
    return re.sub(r"(^\s*)([.\w][^{}]*)\{", f, css, flags=re.M)


CSS = CSS.replace("NOJS", _prefixe_nojs(DEPLIE))

JS = '''
  const reduit = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const barre = document.querySelector(".barre");
  function poserBarre() {
    barre.classList.toggle("posee", scrollY > 40);
    barre.classList.toggle("sur-nuit", scrollY <= 40);
  }
  addEventListener("scroll", poserBarre, {passive: true});
  poserBarre();

  // le halo qui suit la souris : sur les pans du rideau et sur le bandeau de l'instrument
  // (mouvement réduit : le halo reste centré, rien ne suit)
  if (!reduit) {
    document.querySelectorAll("a.pan, .ouvrir").forEach((el) => el.addEventListener("pointermove", (ev) => {
      const r = el.getBoundingClientRect();
      el.style.setProperty("--mx", (ev.clientX - r.left) + "px");
      el.style.setProperty("--my", (ev.clientY - r.top) + "px");
    }, {passive: true}));
  }

  // le rideau : les pans entrent quand il arrive dans la vue ; au clic sur un pan,
  // le rideau s'écarte puis l'outil s'ouvre sur sa page (mouvement réduit : lien nu)
  const rideau = document.querySelector(".rideau");
  if (rideau) {
    if (!reduit && "IntersectionObserver" in window) {
      const io = new IntersectionObserver((entrees) => {
        if (entrees.some((e) => e.isIntersecting)) { rideau.classList.add("vu"); io.disconnect(); }
      }, {threshold: 0.18});
      io.observe(rideau);
    } else {
      rideau.classList.add("vu");
    }
    rideau.querySelectorAll("a.pan").forEach((pan) => pan.addEventListener("click", (ev) => {
      if (reduit || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.button !== 0) return;
      ev.preventDefault();
      // le rideau s'écarte sur la nuit de l'outil choisi : la page qui suit commence dans cette nuit
      rideau.style.setProperty("--ouverture", getComputedStyle(pan).getPropertyValue("--pan-b"));
      rideau.classList.add("ouvre");
      setTimeout(() => { location.href = pan.href; }, 620);
    }));
  }

  const seq = document.querySelector(".sequence");
  const scenes = [...document.querySelectorAll(".scene")];
  const jalons = [...document.querySelectorAll(".jalon")];
  const jauge = document.querySelector(".jauge i");
  let courant = -1;
  function poser(i) {
    if (i === courant) return;
    courant = i;
    scenes.forEach((s, k) => { s.classList.toggle("actif", k === i); s.setAttribute("aria-hidden", k === i ? "false" : "true"); });
    jalons.forEach((j, k) => j.classList.toggle("actif", k === i));
  }
  function surScroll() {
    if (innerWidth <= 1080) return;
    const r = seq.getBoundingClientRect();
    const total = r.height - innerHeight;
    const p = Math.min(1, Math.max(0, -r.top / total));
    if (jauge) jauge.style.height = (p * 100).toFixed(1) + "%";
    poser(Math.min(scenes.length - 1, Math.floor(p * scenes.length)));
  }
  addEventListener("scroll", surScroll, {passive: true});
  jalons.forEach((j, k) => j.addEventListener("click", () => {
    const r = seq.offsetTop + (seq.offsetHeight - innerHeight) * ((k + 0.5) / scenes.length);
    scrollTo({top: innerWidth <= 1080 ? scenes[k].offsetTop - 90 : r,
              behavior: reduit ? "auto" : "smooth"});
  }));
  poser(0); surScroll();
'''

scenes = "".join(scene_html(i, s) for i, s in enumerate(SCENES))

# ── les données structurées : ce que les moteurs lisent, RIEN d'inventé ──────
# La description est la meta description, mot pour mot : une seule voix.
# L'offre à 0 est la seule vraie : le grant d'évaluation de trente jours,
# écrit dans la licence publique. Aucune note, aucun avis, aucun prix payant
# ici : les prix de l'engagement vivent sur leur page, en clair (assembler.py
# porte les refus). L'OS reprend le README de l'outil : macOS ou Linux ;
# Windows non testé, donc non affirmé.
DONNEES_STRUCTUREES = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Organization", "@id": "https://cascade-routing.com/#org",
         "name": "Cascade", "url": "https://cascade-routing.com/",
         "logo": "https://cascade-routing.com/og.png",
         "email": "contact@cascade-routing.com"},
        {"@type": "SoftwareApplication", "name": "Cascade Routing",
         "url": "https://cascade-routing.com/routing/",
         "applicationCategory": "DeveloperApplication",
         "operatingSystem": "macOS, Linux (Node 24+)",
         "downloadUrl": "https://github.com/ArslaneSempai-ui/cascade-routing",
         "description": "A routing audit for KYC extraction: measured on sealed "
                        "records, rerun on your machine. On your records, on "
                        "your machine: nothing leaves the network.",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD",
                    "description": "Thirty-day evaluation on your own records, "
                                   "granted in the public licence."},
         "publisher": {"@id": "https://cascade-routing.com/#org"}},
    ],
}, ensure_ascii=True)

from outil import (OUTILS, PALETTE_VERTE, PALETTE_RUBIS, PALETTE_LAPIS, PALETTE_ONYX,
                   PALETTE_AMETHYSTE, NUIT_AMETHYSTE,
                   NUIT_VERTE, NUIT_RUBIS, NUIT_LAPIS, NUIT_ONYX,
                   lire_releve_scelle, lien, manques, ETATS_PREFIXE, ICONES_PREFIXE)


def outils_vivants():
    """Les outils que les pages MONTRENT : un pan de rideau, une entrée de nav ou un
    nœud de graphe qui pointe vers une page ou un robot absents casserait tout le
    site pour un outil pas prêt. Routing et Screening sont en ligne ; un outil
    suivant entre TOUT SEUL le jour où ses findings ET son robot de rideau existent
    — la promesse « le rideau gagne le pan tout seul », tenue par un test
    d'existence plutôt que par une liste à retoucher."""
    vivants = []
    for o in OUTILS.values():
        if o["id"] in ("routing", "screening"):
            vivants.append(o)      # en ligne : leurs pièces sont commitées
            continue
        m = manques(o["id"], BASE)
        if not m:
            vivants.append(o)
        else:
            print(f"  rideau : {o['id']} pas encore prêt ({len(m)} pièce(s) : "
                  f"{', '.join(m[:3])}{'…' if len(m) > 3 else ''}) : pan non montré")
    return vivants

NOMBRES = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


def choix_outils(outil):
    """LE RIDEAU : le deuxième écran, tranché par Arslane le 6/09 sur une planche de
    trois formes, puis précisé le même soir (décision A) : sur la page de la MARQUE
    (outil=None) les pans sont tous FERMÉS, aucun n'est « ouvert d'office » ; sur la
    page d'un outil, son pan est marqué aria-current. Un pan par outil de la table,
    chacun dans SES couleurs (posées en variables sur le pan : la page rubis aliase
    la palette, et le pan vert doit y rester vert), avec son robot, sa question et
    « Open X ». Cliquer un pan mène à SA page, ancrée sur son propre rideau (#tools).
    Le script (JS) ajoute l'entrée des pans au défilement et l'ouverture du rideau au
    clic ; sans script, ce sont des liens. Grille auto-fit : un troisième robot
    prendra sa place sans qu'on touche ici. Les classes cote-g / cote-d disent de
    quel côté un pan glisse : la première moitié à gauche, la seconde à droite."""
    pans = ""
    outils = outils_vivants()
    for i, o in enumerate(outils):
        cote = "cote-g" if i < len(outils) / 2 else "cote-d"
        style = (f'--pan-vif:{o["vif"]};--pan-a:{o["nuit"][0]};'
                 f'--pan-b:{o["nuit"][1]};--pan-c:{o["nuit"][2]}')
        prefixe = outil["prefixe_racine"] if outil else ""
        corps = (f'<span class="p-eti">{o["etiquette"]}</span>'
                 f'<img src="{prefixe}rendus/{o["robot_rideau"]}" alt="">'
                 f'<span class="p-h">{o["question"]}</span>'
                 f'<span class="p-d">{o["pitch"]}</span>')
        if outil is not None and o["id"] == outil["id"]:
            pans += (f'\n  <div class="pan {cote}" style="{style}" aria-current="page">{corps}'
                     f'<span class="p-ouvrir">You are here &#183; {o["nom"]}</span></div>')
        else:
            pans += (f'\n  <a class="pan {cote}" style="{style}" href="{prefixe}{o["page_hero"]}#tools">{corps}'
                     f'<span class="p-ouvrir">Open {o["nom"]} <span aria-hidden="true">&#8594;</span></span></a>')
    n = NOMBRES.get(len(outils), str(len(outils)))
    return (f'<section class="rideau" id="tools" aria-label="The instruments">'
            f'\n  <span class="rideau-titre">Cascade &#183; {n} instruments, one method</span>'
            f'{pans}\n</section>')


def film_html(outil):
    """LA PLACE DU FILM d'un outil, la même sur chaque couleur : le titre, le lecteur,
    la note « hosted on YouTube · link pending upload » tant que la vidéo n'est pas
    en ligne. Sans vidéo rendue, l'affiche est COMPOSÉE (nuit de l'outil, robot
    penché, question) : aucune durée n'est affichée, parce qu'aucune n'est mesurée ;
    le vert, dont le film existe, garde son affiche rendue et ses 57 secondes."""
    if outil.get("affiche"):
        # l'affiche RENDUE, comme le vert : le robot de la couleur, paumes ouvertes,
        # projetant deux chiffres du relevé (etats/affiche-plaque.py + affiche-composer.py)
        visuel = (f'<img src="{lien(outil, "rendus/" + outil["affiche"])}" '
                  f'alt="{outil["affiche_alt"]}">')
    else:
        visuel = (f'<span class="affiche" role="img" aria-label="The {outil["nom"]} robot, leaning in, beside the question the film answers">'
                  f'<span class="af-t"><span class="af-eti">Cascade &#183; {outil["nom"]}</span><span class="af-q">{outil["question"]}</span></span>'
                  f'<img src="{lien(outil, "rendus/" + outil["robots"][0])}" alt=""></span>')
    return f"""
<section class="film"><div class="colonne">
  <h2 class="h2">Cascade {outil["nom"]}, on film.</h2>
  <p class="film-duree">The five findings, explained</p>
  <a class="lecteur" href="https://www.youtube.com/@cascade-routing" aria-label="Watch the film of Cascade {outil["nom"]}, opens on YouTube">
    {visuel}
    <span class="jouer" aria-hidden="true"><svg width="30" height="34" viewBox="0 0 30 34" fill="none"><path d="M2 2l26 15L2 32V2z" fill="#e4ecdf"/></svg></span>
  </a>
  <div class="film-note">
    <span class="ou">hosted on YouTube &#183; link pending upload</span>
  </div>
</div></section>
"""


# ═══════════════════ LA CHORÉGRAPHIE AU SCROLL (lot P-C1) ═══════════════════
# Quand rendus/sequences/<prefixe>/manifest.json existe, la page gagne un canevas
# sous les scènes et le script du scrub ; SANS manifeste, les trois morceaux sont
# vides et la page d'aujourd'hui sort octet pour octet — un outil sans séquence
# n'est pas un outil cassé. Le mouvement est validé par Arslane sur le prototype
# du rack (9/09) ; les gardes des séquences (identité, fraîcheur, poids,
# complétude) sont le lot M-C1, dans l'assembleur.

CSS_SCRUB = """
  canvas.scrub{position:absolute;inset:0;width:100%;height:100%;z-index:0}
  .colle.scrub .scene .objet{visibility:hidden}
  @media (max-width:1080px){canvas.scrub{display:none}}
"""

# Le contrat du geste : p vient du même calcul que surScroll ; k = floor(p·5),
# q = p·5 − k, t = min(1, q / mouvement), image = round(t·(n−1)). q ≥ mouvement :
# la scène k est active (annotations, fiche, jalon) ; sinon aucune, le canevas seul.
# Une lecture par image d'animation (rAF), jamais une par événement ; la transition 0
# entière avant le premier dessin, les suivantes derrière, dans l'ordre ; une image
# manquante prend la voisine ; tout échec de la transition 0 rend la page d'aujourd'hui,
# sans erreur en console. Le script tourne APRÈS le JS commun : ses classes gagnent
# dans la même image d'animation (rAF après les écouteurs de scroll, avant la peinture).
JS_SCRUB = """
(() => {
  const M = JSON.parse(document.getElementById("seq-manifeste").textContent);
  const colle = document.querySelector(".colle");
  const seqEl = document.querySelector(".sequence");
  const canevas = document.querySelector("canvas.scrub");
  const scenesS = [...document.querySelectorAll(".scene")];
  const jalonsS = [...document.querySelectorAll(".jalon")];
  if (!colle || !seqEl || !canevas || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const ctx = canevas.getContext("2d");
  const nom = (k, i) => M.chemin + M.prefixe + "-seq-0" + (k + 1) + "-" + String(i).padStart(3, "0") + M.ext;
  const T = [];
  let pret = false, mort = false, demande = false, dernier = "";
  const charge = (k, i) => new Promise((r) => {
    const im = new Image();
    im.onload = () => r(im);
    im.onerror = () => r(null);
    im.src = nom(k, i);
  });
  const chargeTransition = async (k) => {
    T[k] = await Promise.all(Array.from({ length: M.n }, (_, i) => charge(k, i)));
    return T[k].some((im) => im !== null);
  };
  const voisine = (k, i) => {
    const t = T[k];
    if (!t) return null;
    for (let d = 0; d < M.n; d++) {
      if (t[i - d]) return t[i - d];
      if (t[i + d]) return t[i + d];
    }
    return null;
  };
  function peindre(force) {
    if (mort || !pret) return;
    if (innerWidth <= 1080) { colle.classList.remove("scrub"); dernier = ""; return; }
    const r = seqEl.getBoundingClientRect();
    const total = r.height - innerHeight;
    const p = Math.min(1, Math.max(0, -r.top / total));
    const brut = Math.min(M.transitions - 1e-9, p * M.transitions);
    const k = Math.floor(brut), q = brut - k;
    const t = Math.min(1, q / M.mouvement);
    const i = Math.round(t * (M.n - 1));
    const arret = q >= M.mouvement;
    scenesS.forEach((s, x) => {
      const a = arret && x === k;
      s.classList.toggle("actif", a);
      s.setAttribute("aria-hidden", a ? "false" : "true");
    });
    jalonsS.forEach((j, x) => j.classList.toggle("actif", arret && x === k));
    const cle = k + ":" + i + ":" + canevas.clientWidth;
    if (!force && cle === dernier) return;
    dernier = cle;
    colle.classList.add("scrub");
    const dpr = Math.min(2, devicePixelRatio || 1);
    const lw = Math.round(canevas.clientWidth * dpr), lh = Math.round(canevas.clientHeight * dpr);
    if (canevas.width !== lw || canevas.height !== lh) { canevas.width = lw; canevas.height = lh; }
    const im = voisine(k, i);
    if (!im) return;
    const e = Math.min(canevas.width / im.naturalWidth, canevas.height / im.naturalHeight);
    const w = im.naturalWidth * e, h = im.naturalHeight * e;
    ctx.clearRect(0, 0, canevas.width, canevas.height);
    ctx.drawImage(im, (canevas.width - w) / 2, (canevas.height - h) / 2, w, h);
  }
  const auCadre = () => {
    if (demande) return;
    demande = true;
    requestAnimationFrame(() => { demande = false; peindre(false); });
  };
  addEventListener("scroll", auCadre, { passive: true });
  addEventListener("resize", auCadre);
  (async () => {
    if (!(await chargeTransition(0))) { mort = true; return; }
    pret = true;
    peindre(true);
    for (let k = 1; k < M.transitions; k++) await chargeTransition(k);
  })();
})();
"""


def sequence_scrub(prefixe):
    """Les trois morceaux du scrub (canevas, CSS, script) quand le manifeste des
    séquences de l'outil existe ; trois chaînes vides sinon — le repli est
    l'ABSENCE des morceaux, pas un script qui se tait, pour que la page sans
    séquence reste celle d'aujourd'hui octet pour octet (témoin cmp du rouge)."""
    chemin = BASE / "rendus" / "sequences" / prefixe / "manifest.json"
    if not chemin.exists():
        return "", "", ""
    m = json.loads(chemin.read_text())
    for cle in ("prefixe", "n", "transitions", "ext", "large", "haut", "mouvement"):
        if cle not in m:
            sys.exit(f"manifest.json de {prefixe} : clé « {cle} » absente ; le scrub ne devine rien")
    if m["prefixe"] != prefixe:
        sys.exit(f"manifest.json : prefixe « {m['prefixe']} » sous le dossier {prefixe}/ : les séquences d'un autre plateau")
    donnees = json.dumps({"prefixe": m["prefixe"], "n": m["n"], "transitions": m["transitions"],
                          "ext": m["ext"], "mouvement": m["mouvement"],
                          "chemin": f"../rendus/sequences/{prefixe}/"}, ensure_ascii=True)
    canevas = f'<canvas class="scrub" width="{m["large"]}" height="{m["haut"]}" aria-hidden="true"></canvas>'
    script = (f'\n<script type="application/json" id="seq-manifeste">{donnees}</script>'
              f'\n<script>{JS_SCRUB}</script>')
    return canevas, CSS_SCRUB, script


_CANEVAS_V, _CSS_SCRUB_V, _SCRUB_V = sequence_scrub(ETATS_PREFIXE["routing"])

PAGE = f'''<!doctype html><html lang="en">
<meta charset="utf-8"><title>Cascade &#183; KYC routing audit</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta property="og:type" content="website">
<meta property="og:title" content="Cascade: routing audit, KYC extraction">
<meta property="og:description" content="A routing audit for KYC extraction: measured on sealed records, rerun on your machine. On your records, on your machine: nothing leaves the network.">
<meta property="og:url" content="https://cascade-routing.com/routing/">
<meta property="og:image" content="https://cascade-routing.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="description" content="A routing audit for KYC extraction: measured on sealed records, rerun on your machine. On your records, on your machine: nothing leaves the network.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M0 0h16L0 16z' fill='%2314251e'/%3E%3Cpath d='M16 0v16H0z' fill='%2323543f'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<link rel="stylesheet" href="fontes/roboto-mono.css">
<script type="application/ld+json">{DONNEES_STRUCTUREES}</script>
<script>document.documentElement.classList.add("js")</script>
<style>{CSS}{_CSS_SCRUB_V}</style>
<header class="barre sur-nuit">
  <a class="marque" href="ACCUEIL.html">CASCADE</a>
  <nav aria-label="Site">
    <a href="INSTRUMENT.html">Instrument</a>
    <a href="ENGAGEMENT.html">Pricing</a>
    <a href="ANNEXE-METHODE.html">Method</a>
    <a href="ANNEXE-SECURITE.html">Security</a>
    <a href="ANNEXE-QUESTIONS.html">Questions</a>
    <a href="CONTACT.html">Contact</a>
  </nav>
  <span class="sceau">seal {SCEAU} &#183; measured, then frozen</span>
</header>

<main>
<section class="hero">
  <h1 class="h1 entree">Where should the next dollar&nbsp;go?</h1>
  <p class="lede entree">Seven tiers, from a regular expression to a human, measured on your own records.<br>
    The answer is rarely &ldquo;buy the bigger model&rdquo;, and every figure
    <b>can be verified by you</b>.</p>
  <div class="commande entree" role="group" aria-label="The first measurement, before any install">
    <code class="ln">git clone {DEPOT_URL}</code>
    <code class="ln">node src/premiere-reponse.mjs</code>
    <span class="note">The conclusion, from the sealed records. Before npm install, under a second.</span>
  </div>
  <div class="cue" aria-hidden="true"><span>scroll</span><span class="fil"></span></div>
</section>

{choix_outils(OUTILS["routing"])}

<section class="sequence" aria-label="The five findings">
  <div class="colle">
    {rail_html()}
    <div class="theatre">
      <div class="scenes">{_CANEVAS_V}{scenes}</div>
    </div>
  </div>
</section>

<section class="instrument"><div class="colonne">
  <h2 class="h2">Pick any cell, read what your routing costs.</h2>
  {table_html()}
  <div class="ouvrir-ligne"><a class="ouvrir" href="INSTRUMENT.html">
    <span><span class="ouvrir-eti">Cascade &#183; Routing</span><span class="ouvrir-t">Open the live instrument</span>
    <span class="ouvrir-s">Every field at every tier, accuracy and cost read live from the sealed record, and a budget slider that chooses the way the tool does.</span></span>
    <span class="fl" aria-hidden="true">&#8594;</span></a></div>
</div></section>

<div class="couture" aria-hidden="true"><div class="colonne">
  <span class="filet"></span>
  <span class="sceau-c">measured, then frozen &#183; seal {SCEAU}</span>
  <span class="filet"></span>
</div></div>

<section class="film"><div class="colonne">
  <h2 class="h2">Cascade, in 57 seconds.</h2>
  <p class="film-duree">The five findings, explained</p>
  <a class="lecteur" href="https://www.youtube.com/@cascade-routing" aria-label="Watch the film: 57 seconds, opens on YouTube">
    <img src="rendus/affiche-film.jpg" alt="The Cascade robot, palms up, projecting the two rates: the dashboard 94.4%, your desk 76.7%">
    <span class="jouer" aria-hidden="true"><svg width="30" height="34" viewBox="0 0 30 34" fill="none"><path d="M2 2l26 15L2 32V2z" fill="#e4ecdf"/></svg></span>
    <span class="duree">0:57</span>
  </a>
  <div class="film-note">
    <span class="ou">hosted on YouTube &#183; link pending upload</span>
  </div>
</div></section>

{menus_html()}
</main>

<footer class="pied"><div class="colonne">
  <p class="pied-p">On your records, on your machine. <em>Nothing leaves the network.</em></p>
  <span class="sceau">120 files &#183; {N_TESTS} tests &#183; seal {SCEAU}</span>
</div></footer>

<script>{JS}</script>{_SCRUB_V}
'''

# Routing vit sous routing/ (décision A du 6/09) : chaque lien relatif de la page
# sort du sous-dossier par ../ ; ceux qui le portent déjà (le rideau, via la table)
# ne le reçoivent pas deux fois ; les absolus, les ancres et les data: sont laissés
PAGE = re.sub(r'(href|src)="(?!(?:https?:|#|data:|mailto:|\.\./))([^"]+)"', r'\1="../\2"', PAGE)
assert "—" not in PAGE, "un cadratin s'est glissé dans la page"
(BASE / "HERO.html").write_text(PAGE, encoding="utf-8")
print("HERO.html", f"{len(PAGE) / 1e3:.0f} ko")


def batir_accueil():
    """LA PAGE DE LA MARQUE, à la racine (décision A d'Arslane, 6/09) : un héros court
    qui pose la question commune aux instruments, puis le rideau à pans FERMÉS, puis
    les portes de la maison et le pied. Aucun chiffre : les chiffres vivent chez les
    outils, chacun sous son sceau."""
    vivants = outils_vivants()
    n = NOMBRES.get(len(vivants), str(len(vivants)))
    graphe = [{"@type": "Organization", "@id": "https://cascade-routing.com/#org",
               "name": "Cascade", "url": "https://cascade-routing.com/",
               "logo": "https://cascade-routing.com/og.png",
               "email": "contact@cascade-routing.com"}]
    for o in vivants:
        graphe.append({"@type": "SoftwareApplication", "name": f"Cascade {o['nom']}",
                       "url": f"https://cascade-routing.com/{o['sous_dossier']}",
                       "applicationCategory": "DeveloperApplication",
                       "operatingSystem": "macOS, Linux (Node 24+)",
                       "downloadUrl": o["depot"],
                       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD",
                                  "description": "Thirty-day evaluation on your own records, "
                                                 "granted in the public licence."},
                       "publisher": {"@id": "https://cascade-routing.com/#org"}})
    donnees = json.dumps({"@context": "https://schema.org", "@graph": graphe}, ensure_ascii=True)
    description = ("Cascade: instruments for compliance decisions, one method. Every tier "
                   "measured on sealed records, the frontier read with its interval, rerun on "
                   "your own machine. Nothing of yours goes up.")
    page = f'''<!doctype html><html lang="en">
<meta charset="utf-8"><title>Cascade &#183; measured instruments for compliance</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta property="og:type" content="website">
<meta property="og:title" content="Cascade: {n} instruments, one method">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://cascade-routing.com/">
<meta property="og:image" content="https://cascade-routing.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="description" content="{description}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M0 0h16L0 16z' fill='%2314251e'/%3E%3Cpath d='M16 0v16H0z' fill='%2323543f'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<link rel="stylesheet" href="fontes/roboto-mono.css">
<script type="application/ld+json">{donnees}</script>
<script>document.documentElement.classList.add("js")</script>
<style>{CSS}</style>
<header class="barre sur-nuit">
  <a class="marque" href="ACCUEIL.html">CASCADE</a>
  <nav aria-label="Site">
    {chr(10).join(f'    <a href="{o["page_hero"]}">{o["nom"]}</a>' for o in vivants).lstrip()}
    <a href="ENGAGEMENT.html">Pricing</a>
    <a href="CONTACT.html">Contact</a>
  </nav>
  <span class="sceau">measured, then frozen</span>
</header>

<main>
<section class="hero">
  <span class="marque-h entree">Cascade &#183; {n} instruments, one method</span>
  <h1 class="h1 entree">Which tier suffices?</h1>
  <p class="lede entree">Instruments for compliance decisions, and one method behind all of them:
    every tier is measured on sealed records, the frontier is read with its interval,
    and the whole sweep reruns on your own machine. <b>Nothing of yours goes up.</b></p>
  <div class="cue" aria-hidden="true"><span>choose</span><span class="fil"></span></div>
</section>

{choix_outils(None)}

<section class="menus"><div class="colonne">
  <h2 class="h2">The house, in common.</h2>
  <div class="rangee-fine">
    <a class="lien-fin" href="ENGAGEMENT.html">Pricing, in figures <span aria-hidden="true">&#8594;</span></a>
    <a class="lien-fin" href="ANNEXE-TERMS.html">Terms of engagement <span aria-hidden="true">&#8594;</span></a>
    <a class="lien-fin" href="ANNEXE-PRIVACY.html">Privacy <span aria-hidden="true">&#8594;</span></a>
    <a class="lien-fin" href="ANNEXE-ACCESSIBILITE.html">Accessibility <span aria-hidden="true">&#8594;</span></a>
    <a class="lien-fin" href="CONTACT.html">Contact <span aria-hidden="true">&#8594;</span></a>
    <a class="lien-fin" href="MENTIONS.html">The fine print <span aria-hidden="true">&#8594;</span></a>
  </div></div></section>
</main>

<footer class="pied"><div class="colonne">
  <p class="pied-p">On your records, on your machine. <em>Nothing leaves the network.</em></p>
  <span class="sceau">measured, then frozen</span>
</div></footer>

<script>{JS}</script>
'''
    assert "—" not in page, "un cadratin s'est glissé dans la page de la marque"
    (BASE / "ACCUEIL.html").write_text(page, encoding="utf-8")
    print("ACCUEIL.html", f"{len(page) / 1e3:.0f} ko")


batir_accueil()


# ═════════════════════════ LE CATALOGUE : bâtir(outil) ═════════════════════════
# Le vert ci-dessus est la page historique ; depuis la décision du rideau (6/09)
# il porte le deuxième écran comme le rubis, par la même fonction choix_outils.
# Le rubis se bâtit ICI, par la même structure d'écrans, avec les paramètres de
# source/outil.py et les textes du lot S3 (findings-screening.json). Une page
# rouge sans ses données ne se bâtit pas : l'absence est DITE, jamais improvisée.

RUBIS = OUTILS["screening"]
LAPIS = OUTILS["monitoring"]

# ── LES SPÉCIFICITÉS PAR OUTIL de la page héros : tout ce qui n'est ni structure ni
# table d'outil vit ici, pour que le troisième outil soit une ENTRÉE et non une
# quatrième copie de la fonction (la divergence des copies est la maladie que le
# catalogue existe pour fermer). Le rubis garde ses textes À L'OCTET : témoin cmp.
def _refaire_dossier(releve, src, o):
    """Les chiffres de l'onyx, refaits depuis le relevé scellé du Dossier, dans la
    grammaire d'adresses que findings-dossier.json déclare lui-même (lot D3, d950517) :
    {cle, champ} lit releve[cle][champ] (mesure "longueur" en prend la taille) ;
    {compte-verdicts: {controle, tenu}} compte les verdicts de ce contrôle et de ce
    tenu à travers les questions ; {compte-questions: {etat}} compte les questions à
    cet état ; {question, champ} lit releve["questions"][question][champ], le champ
    d'UNE question (lot D3 post-signatures, 9d62c47 : « 16 days since the oldest
    measurement, routing » est questions.routing.joursDepuis, pas un compte).
    Une adresse inconnue est un refus nommé, jamais un zéro silencieux."""
    if "cle" in src:
        v = releve[src["cle"]][src["champ"]]
        if src.get("mesure") == "longueur":
            v = len(v)
        return [str(v)]
    if "question" in src:
        q = releve["questions"].get(src["question"])
        if q is None or src["champ"] not in q:
            sys.exit(f"findings-dossier.json : {src} n'existe pas dans le relevé scellé du Dossier "
                     f"(questions : {', '.join(releve['questions'])}) ; la fiche cite un chiffre "
                     "que le relevé ne porte pas")
        return [str(q[src["champ"]])]
    if "compte-verdicts" in src:
        c = src["compte-verdicts"]
        return [str(sum(1 for q in releve["questions"].values()
                        for verd in q.get("verdicts") or []
                        if verd["controle"] == c["controle"] and verd["tenu"] is c["tenu"]))]
    if "compte-questions" in src:
        e = src["compte-questions"]
        return [str(sum(1 for q in releve["questions"].values() if q.get("etat") == e["etat"]))]
    sys.exit(f"findings-dossier.json : adresse inconnue {src} ; la grammaire du fichier "
             "connaît cle/champ, compte-verdicts et compte-questions")


def _table_dossier(spec, releve, findings):
    """La table du héros onyx : les questions de la chaîne contre les cinq contrôles du
    contrat, lues du relevé scellé. Pas de palier ni de seuil ici : la cellule marquée
    d'une ligne est l'état atteint SANS TROU dans l'ordre du contrat ; une ligne sans
    relevé public est dite non jugée, jamais devinée."""
    ordre = releve["controles"]["presents"]
    tetes = "".join(f"<th scope='col'>{c}</th>" for c in ordre)
    lignes = ""
    for nom_q, q in releve["questions"].items():
        if not q.get("present"):
            lignes += (f"<tr><th scope='row'>{nom_q}</th><td class='cell' colspan='{len(ordre)}'>"
                       f"<small>no public record yet: nothing judged, and said</small></td></tr>")
            continue
        verd = {v["controle"]: v["tenu"] for v in q.get("verdicts", [])}
        etat = q.get("etat")
        cells = ""
        for c in ordre:
            if c not in verd:
                cells += "<td class='cell'><small>not judged</small></td>"
            elif verd[c]:
                marque = " choisi" if c == etat else ""
                cells += f"<td class='cell{marque}'><span>&#10003;</span><br><small>held</small></td>"
            else:
                cells += "<td class='cell'><span>&#215;</span><br><small>not held</small></td>"
        lignes += f"<tr><th scope='row'>{nom_q}</th>{cells}</tr>"
    cv, rg = releve["couverture"], releve["reglages"]
    note = (f"{cv['n']} of the {cv['sur']} questions carry a sealed public record. In each row the "
            "marked cell is the state reached with no gap in the contract&#8217;s order; a row "
            "without one reaches none, and the record says so. Declared rhythm "
            f"{rg['rythmeJours']} days, as of {rg['auJour']}.")
    return f'''<div class="t-scroll"><table class="routage">
      <caption class="sr">{spec["table_caption"]}</caption>
      <thead><tr><th scope="col">{spec["table_ligne"]}</th>{tetes}</tr></thead><tbody>{lignes}</tbody></table></div>
      <p class="t-note">{note}</p>'''


SPECS = {
    "screening": dict(
        lot="S3",
        etats=ETATS_PREFIXE["screening"],
        alt_plateau="The sieve tower",
        palette=PALETTE_RUBIS, nuit=NUIT_RUBIS,
        titre="Cascade Screening &#183; sanctions screening audit",
        og_titre="Cascade Screening: which matcher suffices, at which threshold",
        description="A sanctions-screening audit: which name matcher suffices, at which threshold, "
                    "measured on your own alert history. Nothing of yours goes up.",
        app="Cascade Screening",
        app_desc="A sanctions-screening audit: which name matcher suffices, "
                 "at which threshold, measured on your own alert history. "
                 "Nothing of yours goes up.",
        offre="Thirty-day evaluation on your own alert history, granted in the public licence.",
        lede="Seven name matchers, from strict equality to a multilingual embedding, swept across "
             "fifty&#8209;one thresholds.<br>\n    Recall and false alerts carry their intervals, "
             "and every figure\n    <b>can be verified by you</b>.",
        aria_commande="The measurement on your own alert history",
        commandes=["npm ci --ignore-scripts", "npm run measure:yours -- --alerts=your-alerts.csv"],
        note_commande="Your alert history, measured on your machine. Nothing of yours goes up.",
        instrument_h2="Pick any cell, read what your threshold costs.",
        instrument_page="INSTRUMENT-SCREENING.html",
        instrument_eti="Cascade &#183; Screening",
        instrument_sub="Every matcher at every threshold, recall and false alerts with their intervals, "
                       "live from the sealed record, and the tool's own selection rule under your recall floor.",
        annexe_methode=("Method &amp; what is measured", "What the frontier reads, and what it refuses.",
                        "ANNEXE-SCREENING-METHODE.html"),
        annexe_securite=("Security &amp; data handling", "The lists, the seal, and what never leaves.",
                         "ANNEXE-SCREENING-SECURITE.html"),
        icone_prefixe="objet-screening",
        table_ligne="matcher",
        table_caption="Recall over false alerts of each matcher at each threshold, on the written pairs",
        table_note_unites='Measured on the {nMatch} written match pairs and {nDifferent} hard\n      negatives',
        pied="On your records, on your machine. <em>Nothing of yours goes up.</em>",
    ),
    "monitoring": dict(
        lot="L5-textes",
        etats=ETATS_PREFIXE["monitoring"],   # UNE source : outil.py (la divergence bassins/rack a failli faire attendre manques() pour toujours)
        alt_plateau="The surveillance rack",
        palette=PALETTE_LAPIS, nuit=NUIT_LAPIS,
        titre="Cascade Monitoring &#183; transaction monitoring audit",
        og_titre="Cascade Monitoring: which scenario suffices, at which threshold",
        description="A transaction-monitoring audit: which scenario suffices, at which threshold, "
                    "measured on your own dispositioned alerts. Nothing of yours goes up.",
        app="Cascade Monitoring",
        app_desc="A transaction-monitoring audit: which scenario suffices, "
                 "at which threshold, measured on your own dispositioned alerts. "
                 "Nothing of yours goes up.",
        offre="Thirty-day evaluation on your own dispositioned alerts, granted in the public licence.",
        lede="Seven scenarios, from a bare amount to the deviation from a peer profile, swept across "
             "fifty&#8209;one thresholds.<br>\n    Recall and false alerts carry their intervals, "
             "and every figure\n    <b>can be verified by you</b>.",
        aria_commande="The measurement on your own dispositioned alerts",
        commandes=["npm ci --ignore-scripts",
                   "npm run measure:yours -- --alerts=your-alerts.csv --transactions=your-transactions.csv"],
        note_commande="Your dispositioned alerts, measured on your machine. Nothing of yours goes up.",
        instrument_h2="Pick any cell, read what your threshold costs.",
        instrument_page="INSTRUMENT-MONITORING.html",
        instrument_eti="Cascade &#183; Monitoring",
        instrument_sub="Every scenario at every threshold, recall and false alerts with their intervals, "
                       "live from the sealed record, and the tool's own selection rule under your recall floor.",
        annexe_methode=("Method &amp; what is measured", "What the frontier reads, and what it refuses.",
                        "ANNEXE-MONITORING-METHODE.html"),
        annexe_securite=("Security &amp; data handling", "What is rebuilt, what is assumed, and what never leaves.",
                         "ANNEXE-MONITORING-SECURITE.html"),
        icone_prefixe="objet-monitoring",
        table_ligne="scenario",
        table_caption="Recall over false alerts of each scenario at each threshold, on the written cases",
        table_note_unites='Measured on the {nMatch} written suspicious cases and {nDifferent} benign\n      look&#8209;alikes',
        pied="On your records, on your machine. <em>Nothing of yours goes up.</em>",
    ),
    "scoring": dict(
        lot="A-L5-textes",
        etats=ETATS_PREFIXE["scoring"],
        alt_plateau="The shelving of weights",
        palette=PALETTE_AMETHYSTE, nuit=NUIT_AMETHYSTE,
        titre="Cascade Scoring &#183; customer risk rating audit",
        og_titre="Cascade Scoring: which risk factor suffices, at which threshold",
        description="A customer risk-rating audit: which risk factor suffices, at which threshold, "
                    "measured on your own periodic-review outcomes. Nothing of yours goes up.",
        app="Cascade Scoring",
        app_desc="A customer risk-rating audit: which risk factor suffices, "
                 "at which threshold, measured on your own periodic-review outcomes. "
                 "Nothing of yours goes up.",
        offre="Thirty-day evaluation on your own review outcomes, granted in the public licence.",
        lede="Seven risk factors, from a country list to the deviation from the declared profile, swept across "
             "fifty&#8209;one thresholds.<br>\n    Recall and false alerts carry their intervals, "
             "and every figure\n    <b>can be verified by you</b>.",
        aria_commande="The measurement on your own periodic-review outcomes",
        commandes=["npm ci --ignore-scripts",
                   "npm run measure:yours -- --customers=your-customers.csv --reviews=your-reviews.csv"],
        note_commande="Your review outcomes, measured on your machine. Nothing of yours goes up.",
        instrument_h2="Pick any cell, read what your threshold costs.",
        instrument_page="INSTRUMENT-SCORING.html",
        instrument_eti="Cascade &#183; Scoring",
        instrument_sub="Every risk factor at every threshold, recall and false alerts with their intervals, "
                       "live from the sealed record, and the tool's own selection rule under your recall floor.",
        annexe_methode=("Method &amp; what is measured", "What the frontier reads, and what it refuses.",
                        "ANNEXE-SCORING-METHODE.html"),
        annexe_securite=("Security &amp; data handling", "The declared tables, the seal, and what never leaves.",
                         "ANNEXE-SCORING-SECURITE.html"),
        icone_prefixe=ICONES_PREFIXE["scoring"],
        table_ligne="factor",
        table_caption="Recall over false alerts of each risk factor at each threshold, on the written files",
        table_note_unites='Measured on the {nMatch} written escalated files and {nDifferent} maintained\n      look&#8209;alikes',
        pied="On your records, on your machine. <em>Nothing of yours goes up.</em>",
    ),
    "dossier": dict(
        lot="D3",
        etats=ETATS_PREFIXE["dossier"],
        alt_plateau="The staircase of seals",
        palette=PALETTE_ONYX, nuit=NUIT_ONYX,
        titre="Cascade Dossier &#183; the assembled audit trail",
        og_titre="Cascade Dossier: is the whole chain measured, sealed and fresh",
        description="One dossier over the suite&#8217;s four sealed answers: coverage, seals, "
                    "signatures, freshness and coherence, verified on your machine. "
                    "Nothing of yours goes up.",
        app="Cascade Dossier",
        app_desc="One dossier over the suite&#8217;s four sealed answers: coverage, "
                 "seals, signatures, freshness and coherence, verified on your "
                 "machine. Nothing of yours goes up.",
        offre="Thirty-day evaluation on your own sealed reports, granted in the public licence.",
        lede="Four questions (the reader, the matcher, the scenario, the factor), "
             "five controls each.<br>\n    The Dossier reads the sealed reports and answers "
             "as one piece, and every line\n    <b>can be verified by you</b>.",
        aria_commande="The dossier over your own sealed reports",
        commandes=["npm ci --ignore-scripts",
                   "npm run dossier -- --reports=a-measured.json,b-measured.json"],
        note_commande="Your sealed reports, read on your machine. Nothing of yours goes up.",
        instrument_h2="Read the whole chain in one table.",
        instrument_page="INSTRUMENT-DOSSIER.html",
        instrument_eti="Cascade &#183; Dossier",
        instrument_sub="The four questions against the five controls, states, seals and freshness "
                       "live from the sealed public dossier, and what the next control still needs.",
        annexe_methode=("Method &amp; what is verified", "What the five controls hold, and what a gap means.",
                        "ANNEXE-DOSSIER-METHODE.html"),
        annexe_securite=("Security &amp; data handling", "What is read, what is derived, and what never leaves.",
                         "ANNEXE-DOSSIER-SECURITE.html"),
        icone_prefixe=ICONES_PREFIXE["dossier"],
        table_ligne="question",
        table_caption="State reached by each question of the chain under the contract&#8217;s five controls, on the public records",
        table=_table_dossier,
        refaire=_refaire_dossier,
        pied="On your records, on your machine. <em>Nothing of yours goes up.</em>",
    ),
}


def _etats_dispo(spec):
    """Les cinq états du plateau de l'outil, fournis par le chef. Tant qu'ils manquent,
    la page se bâtit sur l'image verte AVEC un commentaire « placeholder » que
    l'assembleur refuse en production : la garde d'abord, l'image ensuite."""
    return all((BASE / "rendus" / "etats" / f"{spec['etats']}-0{i}.webp").exists() for i in range(1, 6))


def _image_etat_outil(o, spec, i):
    if _etats_dispo(spec):
        return lien(o, f"rendus/etats/{spec['etats']}-0{i}.webp"), ""
    return (lien(o, f"rendus/etats/objet-0{i}.webp"),
            f"<!-- placeholder: {spec['etats']}-0{i}.webp pending, green plateau shown -->")


def _icone_tuile(o, spec, nom):
    """L'icône 3D d'une tuile, dans l'accent de l'outil ; absente, l'icône VERTE du
    même objet la remplace avec le marqueur que l'assembleur refuse en prod."""
    voulu = BASE / "rendus" / "etats" / f"{spec['icone_prefixe']}-{nom}.webp"
    if voulu.exists():
        return lien(o, f"rendus/etats/{spec['icone_prefixe']}-{nom}.webp"), ""
    return (lien(o, f"rendus/etats/objet-{nom}.webp"),
            f"<!-- placeholder: {spec['icone_prefixe']}-{nom}.webp pending, green icon shown -->")


def _scene_outil(o, spec, i, f):
    """La scène d'un outil du catalogue : même squelette que scene_html, données du lot des textes."""
    lignes, etiquettes = "", ""
    appels_f = f.get("annotations", [])
    if len(appels_f) < 2:
        sys.exit(f"{o['id']}, finding {f.get('num', i + 1)} : {len(appels_f)} annotation(s) ; chaque plateau porte "
                 "ses explications en transparence, sur toutes les couleurs (deux au moins)")
    for (ax, ay, lx, ly, txt) in appels_f:
        verifier_appel(txt, f"{o['id']}, finding {f.get('num', i + 1)}")
        x1, y1 = MX + lx * IW, ly * IH
        x2, y2 = MX + ax * IW, ay * IH
        lignes += (f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" pathLength="1"/>'
                   f'<circle cx="{x2:.0f}" cy="{y2:.0f}" r="4"/>')
        etiquettes += f'<span class="ap-eti" style="left:{x1 / 14.20:.1f}%;top:{y1 / 10.0:.1f}%">{txt}</span>'
    appels = f'<svg class="appels" viewBox="0 0 1420 1000" aria-hidden="true">{lignes}</svg>{etiquettes}'
    img, marque = _image_etat_outil(o, spec, i + 1)
    return f"""
    <div class="scene{' actif' if i == 0 else ''}" id="scene-{i}" data-i="{i}">{marque}
      <img class="objet" src="{img}"
        alt="{spec['alt_plateau']}, state {f['num']}: {f['titre']}">
      {appels}
      <figure class="fiche">
        <figcaption class="fiche-t"><span>finding {f['num']}</span><span class="ft-cote">{f['cote']}</span></figcaption>
        <p class="fiche-phrase">{f['phrase']}</p>
        <div class="paire">
          <div class="val"><span class="chiffre pale-v">{f['a']}</span><span class="leg">{f['leg_a']}</span></div>
          <div class="val"><span class="chiffre vert-v">{f['b']}</span><span class="leg">{f['leg_b']}</span></div>
        </div>
      </figure>
    </div>"""


def _rail_outil(o, spec, findings):
    items = "".join(
        f"""<li><button class="jalon{' actif' if i == 0 else ''}" data-i="{i}" aria-label="Go to finding {f['num']}: {f['titre']}">
        <img class="j-vig" src="{_image_etat_outil(o, spec, i + 1)[0]}" alt="">
        <span class="j-num">{f['num']}</span><span class="j-corps"><span class="j-titre">{f['titre']}</span>
        <span class="j-cote">{f['cote']}</span></span></button></li>""" for i, f in enumerate(findings))
    return f'<nav class="rail" aria-label="Findings"><span class="jauge" aria-hidden="true"><i></i></span><ul>{items}</ul></nav>'


def _table_outil(spec, releve, findings):
    """La grille de l'outil sur son héros, comme le vert montre la sienne : chaque palier
    présent, à sept seuils dont celui de la frontière quand elle EXISTE, rappel sur
    fausses alertes, tout lu dans le relevé scellé. La cellule de la frontière vient du
    finding 03 (source.a) quand il en cite une ; la règle de l'outil peut n'en retenir
    AUCUNE (le bleu à 0,90 sur les cas écrits) — alors aucune cellule n'est marquée, et
    la note le dit au lieu de laisser deviner."""
    src = findings[2].get("source", {}).get("a") or {}
    palier_f, seuil_f = src.get("palier"), src.get("seuil")
    seuils = sorted({"0.50", "0.60", "0.70", "0.80", "0.90", "1.00"} | ({seuil_f} if seuil_f else set()), key=float)
    auth = releve["authored"]
    tetes = "".join(f"<th scope='col'>{s}</th>" for s in seuils)
    lignes = ""
    for p in releve["paliers"]["presents"]:
        cells = ""
        for s in seuils:
            c = auth["tables"][p][s]
            choisi = " choisi" if (palier_f and (p, s) == (palier_f, seuil_f)) else ""
            cells += (f"<td class='cell{choisi}'><span>{c['rappel']['taux'] * 100:.0f}<small>%</small></span>"
                      f"<br><small>{c['fauxPositifs']['taux'] * 100:.0f}% fa</small></td>")
        lignes += f"<tr><th scope='row'>{p}</th>{cells}</tr>"
    unites = spec["table_note_unites"].format(
        nMatch=auth.get("nMatch", auth.get("nSuspicious", auth.get("nEscalated"))),
        nDifferent=auth.get("nDifferent", auth.get("nBenign", auth.get("nMaintained"))))
    champ_cite = (findings[2].get("source", {}).get("a") or {}).get("champ", "taux")
    if palier_f and champ_cite == "taux":
        frontiere = (f"The ruby cell is the tool&#8217;s frontier under its\n      default rule, {palier_f} at {seuil_f}.")
    elif palier_f:
        # la fiche 03 cite une BORNE (champ « bas ») : la cellule marquée est la plus forte
        # borne basse, pas une frontière : la règle de l'outil ne retient RIEN au plancher,
        # et l'écrire « frontier » serait le mensonge exact que le relevé refuse
        frontiere = (f"The marked cell, {palier_f} at {seuil_f}, carries the strongest recall lower"
                     "\n      bound; under its default rule the tool retains NO cell at the recall floor on"
                     "\n      these cases: the record says so, and the instrument shows it live.")
    else:
        frontiere = ("Under its default rule, the tool retains NO cell at the recall floor on these"
                     "\n      cases: the record says so, and the instrument shows the strongest bound instead.")
    return f'''<div class="t-scroll"><table class="routage">
      <caption class="sr">{spec["table_caption"]}</caption>
      <thead><tr><th scope="col">{spec["table_ligne"]}</th>{tetes}</tr></thead><tbody>{lignes}</tbody></table></div>
      <p class="t-note">{unites}: recall on top, false alerts below. {frontiere} The synthetic variants stay apart, on the instrument.</p>'''



def batir_outil_catalogue(o, spec):
    # UNE définition de « prêt » : manques(), la même que le rideau et l'assembleur.
    # Elle couvre l'absence, le pret:false et la dérive de sceau (un relevé re-scellé
    # après la dérivation des textes) : toutes des absences DITES, pas des pannes —
    # le 9/09, la dérive post-A-L4 faisait sys.exit ici et cassait l'assemblage entier
    m = manques(o["id"], BASE)
    if any(f"findings-{o['id']}.json" in x for x in m):
        print(f"{o['page_hero']} non bâti : {[x for x in m if 'findings' in x][0]} "
              f"(lot {spec['lot']}) : l'absence est dite, rien n'est improvisé")
        return False
    findings_chemin = BASE / f"findings-{o['id']}.json"
    RELEVE = lire_releve_scelle(o["releve"])
    SCEAU_O = RELEVE["empreinte"]
    _f = json.loads(findings_chemin.read_text())
    if not _f.get("pret", True):
        print(f"{o['page_hero']} non bâti : findings-{o['id']}.json porte pret:false "
              f"(lot {spec['lot']}, chiffres en attente de leur sceau) : l'absence est dite")
        return False
    if _f.get("sceau") != SCEAU_O:
        sys.exit(f"findings-{o['id']}.json cite le scellé {_f.get('sceau')} mais le relevé "
                 f"public porte {SCEAU_O} : les textes ont dérivé du relevé, lot {spec['lot']} à resceller")
    FINDINGS = _f["findings"]
    if len(FINDINGS) != 5:
        sys.exit(f"findings-{o['id']}.json porte {len(FINDINGS)} findings : la séquence en veut 5")

    # AUCUN CHIFFRE TAPÉ : chaque valeur affichée d'une fiche à `source` est REFAITE depuis
    # le relevé scellé : cellule[mesure][champ ou « taux »], ou le compte nommé : et le
    # nombre refait doit apparaître dans le HTML affiché (à une ou zéro décimale, les deux
    # écritures de la maison). Un chiffre qui ne se refait pas ne se publie pas.
    def _refaire_grille(src):
        moitie = RELEVE[src["table"]]
        if "compte" in src:
            return [str(moitie[src["compte"]])]
        c = moitie["tables"][src["palier"]][src["seuil"]][src["mesure"]]
        v = c[src.get("champ", "taux")]
        return [f"{v * 100:.1f}", f"{v * 100:.0f}"]
    # l'onyx n'a ni palier ni seuil : ses adresses parlent le contrat, et son refaire
    # vit dans le spec — le crochet, pas une quatrième copie de la boucle de garde
    _refaire = (lambda src: spec["refaire"](RELEVE, src, o)) if "refaire" in spec else _refaire_grille
    for num_f, f in enumerate(FINDINGS, 1):
        for cote_nom in ("a", "b"):
            src = (f.get("source") or {}).get(cote_nom)
            if not src:
                continue
            affiche = re.sub(r"<[^>]+>", "", f[cote_nom])
            attendus = _refaire(src)
            if not any(x in affiche for x in attendus):
                sys.exit(f"findings-{o['id']}.json, fiche {num_f}, côté {cote_nom} : "
                         f"« {affiche} » ne contient aucune écriture du chiffre refait depuis le "
                         f"relevé ({', '.join(attendus)}) : le chiffre affiché a dérivé de sa cellule")

    _m = re.search(r"\*\*(\d+) tests\*\* across (\d+) files",
                   (o["outil_chemin"] / "README.md").read_text())
    if not _m:
        sys.exit(f"le compte de tests est introuvable dans le README de {o['outil_chemin'].name}")
    n_tests_o = _m.group(1)

    canevas_o, css_scrub_o, scrub_o = sequence_scrub(spec["etats"])
    css_o = CSS.replace(PALETTE_VERTE, spec["palette"])
    assert css_o != CSS, "la palette verte n'a pas été trouvée dans le CSS : l'alias n'a rien remplacé"
    css_n = css_o.replace(NUIT_VERTE, spec["nuit"])
    assert css_n != css_o, "la nuit verte n'a pas été trouvée dans le CSS : la page garderait une nuit verte"
    css_o = css_n
    p = o["prefixe_racine"]

    donnees = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": "https://cascade-routing.com/#org",
             "name": "Cascade", "url": "https://cascade-routing.com/",
             "logo": "https://cascade-routing.com/og.png",
             "email": "contact@cascade-routing.com"},
            {"@type": "SoftwareApplication", "name": spec["app"],
             "url": f"https://cascade-routing.com/{o['sous_dossier']}",
             "applicationCategory": "DeveloperApplication",
             "operatingSystem": "macOS, Linux (Node 24+)",
             "downloadUrl": o["depot"],
             "description": spec["app_desc"],
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD",
                        "description": spec["offre"]},
             "publisher": {"@id": "https://cascade-routing.com/#org"}},
        ],
    }, ensure_ascii=True)

    scenes_o = "".join(_scene_outil(o, spec, i, f) for i, f in enumerate(FINDINGS))
    im, iq = _icone_tuile(o, spec, "methode")
    is_, iq2 = _icone_tuile(o, spec, "securite")
    tuiles = [
        (*spec["annexe_methode"], im + iq),
        (*spec["annexe_securite"], is_ + iq2),
        ("Terms of engagement", "What the grant allows, for how long, and what a client buys.",
         lien(o, "ANNEXE-TERMS.html"), _icone_tuile(o, spec, "terms")[0] + _icone_tuile(o, spec, "terms")[1]),
        ("Privacy", "No data is collected. Written down, and verifiable.",
         lien(o, "ANNEXE-PRIVACY.html"), _icone_tuile(o, spec, "privacy")[0] + _icone_tuile(o, spec, "privacy")[1]),
        ("Accessibility", "Usable by keyboard, by screen reader, and with motion turned off.",
         lien(o, "ANNEXE-ACCESSIBILITE.html"), _icone_tuile(o, spec, "accessibilite")[0] + _icone_tuile(o, spec, "accessibilite")[1]),
    ]
    def tuile_html(titre, desc, href, img_et_marque):
        # le marqueur placeholder éventuel est ACCOLÉ au chemin par _icone_tuile : on les sépare
        img, _, marque = img_et_marque.partition("<!--")
        marque = ("<!--" + marque) if marque else ""
        return f"""
      <a class="tuile" href="{href}">{marque}
        <span class="tuile-img"><img src="{img}" alt=""></span>
        <span class="tuile-corps"><span class="tuile-t">{titre}</span>
        <span class="tuile-d">{desc}</span></span>
        <span class="tuile-fl" aria-hidden="true">&#8594;</span>
      </a>"""
    tuiles_html = "".join(tuile_html(*t) for t in tuiles)
    commandes_html = "".join(f'<code class="ln">{c}</code>\n    ' for c in
                             ([f"git clone {o['depot']}"] + spec["commandes"]))

    page = f"""<!doctype html><html lang="en">
<meta charset="utf-8"><title>{spec["titre"]}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta property="og:type" content="website">
<meta property="og:title" content="{spec["og_titre"]}">
<meta property="og:description" content="{spec["description"]}">
<meta property="og:url" content="https://cascade-routing.com/{o["sous_dossier"]}">
<meta property="og:image" content="https://cascade-routing.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="description" content="{spec["description"]}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M0 0h16L0 16z' fill='%2314251e'/%3E%3Cpath d='M16 0v16H0z' fill='{o["favicon_accent"]}'/%3E%3C/svg%3E">
<link rel="stylesheet" href="{p}fontes/literata.css">
<link rel="stylesheet" href="{p}fontes/roboto-mono.css">
<script type="application/ld+json">{donnees}</script>
<script>document.documentElement.classList.add("js")</script>
<style>{css_o}{css_scrub_o}</style>
<header class="barre sur-nuit">
  <a class="marque" href="{lien(o, 'ACCUEIL.html')}">CASCADE</a>
  <nav aria-label="Site">
    <a href="{spec["instrument_page"]}">Instrument</a>
    <a href="{lien(o, 'ENGAGEMENT.html')}">Pricing</a>
    <a href="{spec["annexe_methode"][2]}">Method</a>
    <a href="{spec["annexe_securite"][2]}">Security</a>
    <a href="{lien(o, 'CONTACT.html')}">Contact</a>
  </nav>
  <span class="sceau">seal {SCEAU_O} &#183; measured, then frozen</span>
</header>

<main>
<section class="hero">
  <h1 class="h1 entree">{o["question"]}</h1>
  <p class="lede entree">{spec["lede"]}</p>
  <div class="commande entree" role="group" aria-label="{spec["aria_commande"]}">
    {commandes_html}<span class="note">{spec["note_commande"]}</span>
  </div>
  <div class="cue" aria-hidden="true"><span>scroll</span><span class="fil"></span></div>
</section>

{choix_outils(o)}

<section class="sequence" aria-label="The five findings">
  <div class="colle">
    {_rail_outil(o, spec, FINDINGS)}
    <div class="theatre">
      <div class="scenes">{canevas_o}{scenes_o}</div>
    </div>
  </div>
</section>
<section class="instrument"><div class="colonne">
  <h2 class="h2">{spec["instrument_h2"]}</h2>
  {spec.get("table", _table_outil)(spec, RELEVE, FINDINGS)}
  <div class="ouvrir-ligne"><a class="ouvrir" href="{spec["instrument_page"]}">
    <span><span class="ouvrir-eti">{spec["instrument_eti"]}</span><span class="ouvrir-t">Open the live instrument</span>
    <span class="ouvrir-s">{spec["instrument_sub"]}</span></span>
    <span class="fl" aria-hidden="true">&#8594;</span></a></div>
</div></section>

<div class="couture" aria-hidden="true"><div class="colonne">
  <span class="filet"></span>
  <span class="sceau-c">measured, then frozen &#183; seal {SCEAU_O}</span>
  <span class="filet"></span>
</div></div>
{film_html(o)}
<section class="menus"><div class="colonne">
  <h2 class="h2">The appendices your reviewers will ask for.</h2>
  <div class="grille">{tuiles_html}</div>
  <div class="rangee-fine">
    <a class="lien-fin" href="{lien(o, 'ENGAGEMENT.html')}">Pricing, in figures <span aria-hidden="true">&#8594;</span></a>
    <a class="lien-fin" href="{lien(o, 'CONTACT.html')}">Contact <span aria-hidden="true">&#8594;</span></a>
    <a class="lien-fin" href="{lien(o, 'MENTIONS.html')}">The fine print <span aria-hidden="true">&#8594;</span></a>
    <a class="lien-fin" href="{o["depot"]}">The repository, public <span aria-hidden="true">&#8594;</span></a>
  </div></div></section>
</main>

<footer class="pied"><div class="colonne">
  <p class="pied-p">{spec["pied"]}</p>
  <span class="sceau">{n_tests_o} tests &#183; seal {SCEAU_O}</span>
</div></footer>

<script>{JS}</script>{scrub_o}
"""
    assert "\u2014" not in page, "un cadratin s'est glissé dans la page"
    (BASE / o["page_hero"]).write_text(page, encoding="utf-8")
    etat = f"états {spec['etats']}" if _etats_dispo(spec) else "PLACEHOLDERS (plateau vert) : refusé en prod"
    print(o["page_hero"], f"{len(page) / 1e3:.0f} ko", "·", etat)
    return True


def batir(outil_id):
    """Le point d'entrée du catalogue : « routing » est déjà émis à l'import
    (le chemin historique) ; les outils du catalogue s'émettent ici."""
    if outil_id == "routing":
        return True
    if outil_id in SPECS:
        return batir_outil_catalogue(OUTILS[outil_id], SPECS[outil_id])
    sys.exit(f"outil inconnu : {outil_id}")


batir("screening")
batir("monitoring")
batir("scoring")
batir("dossier")
