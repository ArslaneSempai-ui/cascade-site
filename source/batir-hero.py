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

SCEAU = "1151f5a1cfaae0c0"
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
      generative tiers. *The human tier is assumed at {qte(HUMAIN)}%, never measured. Green cells mark the
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
    ("The mean the dashboard shows.",
     "A file with all five fields right. The number a desk lives with."),
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
        (0.70, 0.70, 0.80, 0.90, "the empty row: the human tier, never sampled"),
    ],
    [
        (0.30, 0.625, 0.09, 0.80, "name changes reader: the file-aimed pick"),
        (0.21, 0.42, 0.04, 0.10, "the published pick it replaces"),
        (0.417, 0.138, 0.60, 0.05, "a pick both routings share"),
    ],
    [
        (0.135, 0.30, 0.05, 0.13, "an emptied cell: silence instead of a wrong value"),
        (0.522, 0.172, 0.66, 0.06, "85 wrong values removed, 12 right lost"),
    ],
    [
        (0.33, 0.86, 0.10, 0.95, "run twice: every count identical, to the digit"),
        (0.55, 0.35, 0.73, 0.08, "nothing turns green: the durations moved, withheld"),
    ],
    [
        (0.47, 0.40, 0.70, 0.06, "every stack green: 16,807 routings crossed"),
        (0.70, 0.70, 0.80, 0.90, "still empty: the human tier, never sampled"),
    ],
]

# l'image (1374x1120) posée en contain dans la boîte 1.42:1 (viewBox 1420x1000) ;
# la boîte DOIT garder ce ratio (height + aspect-ratio), sinon chips et lignes divergent
IH, IW = 1000.0, 1000.0 * (1374 / 1120)
MX = (1420 - IW) / 2


def appels_html(i):
    lignes, etiquettes = "", ""
    for (ax, ay, lx, ly, txt) in APPELS[i]:
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
    ("securite", "Security &amp; data handling", "Every place the tool touches, checked rather than described.", "ANNEXE-SECURITE.html"),
    ("questions", "Questions", "Eight objections a bank's reviewers actually raise.", "ANNEXE-QUESTIONS.html"),
    ("terms", "Terms of engagement", "What the grant allows, for how long, and what a client buys.", "ANNEXE-TERMS.html"),
    ("privacy", "Privacy", "What is collected: nothing. Written down, verifiable.", "ANNEXE-PRIVACY.html"),
    ("accessibilite", "Accessibility", "The page holds without a mouse, without motion, without sight.", "ANNEXE-ACCESSIBILITE.html"),
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
        <a class="lien-fin" href="ENGAGEMENT.html">The engagement, in figures <span aria-hidden="true">&#8594;</span></a>
        <a class="lien-fin" href="CONTACT.html">Contact <span aria-hidden="true">&#8594;</span></a>
        <a class="lien-fin" href="MENTIONS.html">Colophon <span aria-hidden="true">&#8594;</span></a>
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
    text-align:center;gap:26px;padding:120px 24px 90px;position:relative;color:var(--sur-vert);
    background:radial-gradient(130% 105% at 50% -18%,var(--nuit-a),var(--nuit-b) 50%,var(--nuit-c))}
  .hero .lede{color:var(--sur-vert-pale);margin-top:32px}
  .hero .lede b{color:var(--sur-vert)}
  .hero .commande{margin-top:34px;background:color-mix(in srgb,var(--nuit-a) 52%,transparent);
    border-color:color-mix(in srgb,var(--vert-vif) 34%,transparent);
    box-shadow:0 26px 70px rgba(0,0,0,.5)}
  .hero .cue{color:var(--sur-vert-pale)}
  .h1{font-size:clamp(44px,7vw,92px);font-weight:600;letter-spacing:-.02em;line-height:1.02;
    text-wrap:balance;max-width:14ch}
  .lede{font-size:clamp(16px,1.35vw,19px);color:var(--demi);max-width:78ch;line-height:1.6;text-wrap:balance}
  .lede b{color:var(--encre)}
  .commande{background:var(--nuit-b);color:var(--sur-vert);border:1px solid color-mix(in srgb,var(--vert-vif) 40%,transparent);
    border-radius:10px;padding:18px 26px;text-align:left;font-family:var(--mono);font-size:12.5px;
    box-shadow:0 24px 60px rgba(14,26,21,.28);max-width:min(92vw,680px)}
  .commande .ln{white-space:nowrap;overflow-x:auto;display:block;padding:2px 0}
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

  /* la séquence : rail-filmstrip, plateau annoté, fiche colonne */
  .sequence{height:560vh;position:relative}
  .colle{position:sticky;top:0;height:100vh;display:flex;align-items:center;gap:min(4vw,56px);
    padding:80px 48px 40px;max-width:1400px;margin:0 auto}
  .rail{width:min(380px,29vw);flex:none;position:relative;padding-left:18px}
  .rail .jauge{position:absolute;left:0;top:6px;bottom:6px;width:3px;
    background:color-mix(in srgb,var(--vert-titre) 25%,transparent);border-radius:1px}
  .rail .jauge i{position:absolute;left:0;top:0;width:100%;height:0%;
    background:var(--vert-vif);border-radius:1px}
  .rail ul{list-style:none;padding:0;display:flex;flex-direction:column;gap:4px}
  .jalon{display:flex;gap:16px;align-items:center;width:100%;text-align:left;background:none;
    border:0;border-left:3px solid transparent;padding:12px 0 12px 16px;cursor:pointer;
    font-family:var(--texte);color:color-mix(in srgb,var(--vert-titre) 80%,var(--pale));
    transition:color .25s,border-color .25s,background .25s}
  .j-vig{display:block;width:74px;aspect-ratio:1.42/1;object-fit:contain;flex:none;align-self:center;
    filter:grayscale(.65) drop-shadow(0 4px 6px rgba(27,29,24,.18));opacity:.5;transform:scale(.94);
    transition:opacity .3s,filter .3s,transform .3s var(--montee)}
  .jalon.actif .j-vig{filter:drop-shadow(0 6px 10px rgba(27,29,24,.25));opacity:1;transform:scale(1.06)}
  .jalon .j-num{font-family:var(--mono);font-size:12px;letter-spacing:.1em;
    color:color-mix(in srgb,var(--vert-titre) 90%,transparent)}
  .jalon.actif .j-num{color:var(--vert-vif)}
  .jalon .j-titre{display:block;font-size:19px;font-weight:600;letter-spacing:-.01em;line-height:1.15}
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
    height:min(46vh,calc((100vw - min(380px,29vw) - 442px)/1.42))}
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
  .ouvrir-ligne{display:flex;justify-content:flex-end;margin-top:36px}
  .ouvrir{display:inline-flex;align-items:baseline;gap:12px;background:transparent;
    color:var(--vert-clair);text-decoration:none;font-family:var(--texte);font-size:17px;font-weight:600;
    padding:14px 26px;border-radius:10px;border:1px solid color-mix(in srgb,var(--vert-vif) 55%,transparent);
    transition:background .2s,color .2s,border-color .2s,box-shadow .2s}
  .ouvrir .fl{font-family:var(--sans);transition:transform .2s var(--montee)}
  .ouvrir:hover{background:var(--vert-vif);color:var(--nuit-c);border-color:var(--vert-vif);
    box-shadow:0 14px 36px color-mix(in srgb,var(--vert-vif) 32%,transparent)}
  .ouvrir:hover .fl{transform:translateX(4px)}

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

PAGE = f'''<!doctype html><html lang="en">
<meta charset="utf-8"><title>Cascade, the routing audit</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta property="og:type" content="website">
<meta property="og:title" content="Cascade: routing audit, KYC extraction">
<meta property="og:description" content="A routing audit for KYC extraction: measured on sealed records, rerun on your machine. On your records, on your machine: nothing leaves the network.">
<meta property="og:url" content="https://cascade-routing.com/index.html">
<meta property="og:image" content="https://cascade-routing.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="description" content="A routing audit for KYC extraction: measured on sealed records, rerun on your machine. On your records, on your machine: nothing leaves the network.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M0 0h16L0 16z' fill='%2314251e'/%3E%3Cpath d='M16 0v16H0z' fill='%2323543f'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<link rel="stylesheet" href="fontes/roboto-mono.css">
<script>document.documentElement.classList.add("js")</script>
<style>{CSS}</style>
<header class="barre sur-nuit">
  <a class="marque" href="index.html">CASCADE</a>
  <nav aria-label="Site">
    <a href="INSTRUMENT.html">Instrument</a>
    <a href="ENGAGEMENT.html">Engagement</a>
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
  <p class="lede entree">Seven tiers, from a regular expression to a human, measured on your own
    records. The answer is rarely <b>&ldquo;buy the bigger model&rdquo;</b>, and every figure
    here can be verified without us.</p>
  <div class="commande entree" role="group" aria-label="The first measurement, before any install">
    <code class="ln">git clone {DEPOT_URL}</code>
    <code class="ln">node src/premiere-reponse.mjs</code>
    <span class="note">The conclusion, from the sealed records. Before npm install, under a second.</span>
  </div>
  <div class="cue" aria-hidden="true"><span>scroll</span><span class="fil"></span></div>
</section>

<section class="sequence" aria-label="The five findings">
  <div class="colle">
    {rail_html()}
    <div class="theatre">
      <div class="scenes">{scenes}</div>
    </div>
  </div>
</section>

<section class="film"><div class="colonne">
  <h2 class="h2">Cascade, introduced by its robot.</h2>
  <p class="film-duree">57 seconds &#183; the five findings, told out loud</p>
  <a class="lecteur" href="https://www.youtube.com/@cascade-routing" aria-label="Watch the film: 57 seconds, opens on YouTube">
    <img src="rendus/affiche-film.jpg" alt="The Cascade robot, palms up, projecting the two rates: the dashboard 94.4%, your desk 76.7%">
    <span class="jouer" aria-hidden="true"><svg width="30" height="34" viewBox="0 0 30 34" fill="none"><path d="M2 2l26 15L2 32V2z" fill="#e4ecdf"/></svg></span>
    <span class="duree">0:57</span>
  </a>
  <div class="film-note">
    <span class="ou">hosted on YouTube &#183; link pending upload</span>
  </div>
</div></section>

<div class="couture" aria-hidden="true"><div class="colonne">
  <span class="filet"></span>
  <span class="sceau-c">measured, then frozen &#183; seal {SCEAU}</span>
  <span class="filet"></span>
</div></div>

<section class="instrument"><div class="colonne">
  <h2 class="h2">Take a cell, read what your routing costs.</h2>
  {table_html()}
  <div class="ouvrir-ligne"><a class="ouvrir" href="INSTRUMENT.html">Open the live instrument <span class="fl" aria-hidden="true">&#8594;</span></a></div>
</div></section>

{menus_html()}
</main>

<footer class="pied"><div class="colonne">
  <p class="pied-p">On your records, on your machine. <em>Nothing leaves the network.</em></p>
  <span class="sceau">120 files &#183; {N_TESTS} tests &#183; seal {SCEAU}</span>
</div></footer>

<script>{JS}</script>
'''

assert "—" not in PAGE, "un cadratin s'est glissé dans la page"
(BASE / "HERO.html").write_text(PAGE, encoding="utf-8")
print("HERO.html", f"{len(PAGE) / 1e3:.0f} ko")
