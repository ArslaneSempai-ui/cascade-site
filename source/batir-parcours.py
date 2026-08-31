#!/usr/bin/env python3
"""Les cinq parcours, mis en valeur sous le vert, et le passage de l'un à l'autre.

CE QU'ARSLANE A DEMANDÉ LE 31 AOÛT
  1. la méthode : de haut en bas, toujours. Le haut est arrêté — en-tête, titre sur toute
     la hauteur du vert, objet seul à droite. On descend.
  2. « les 5 choix des parcours de l'outil mis en valeur en dessous » : le menu n'est plus
     une réglure, c'est le bloc principal du bas.
  3. cliquer sur l'un d'eux ouvre l'écran de cette étape : le titre change, le menu marque
     la nouvelle étape, ET L'OBJET CHANGE — les pièces vertes et rouges suivent l'étape.

CE QUE L'OBJET DIT, ÉTAPE PAR ÉTAPE
L'objet n'illustre pas : il PORTE le constat. Sept lecteurs en lignes, cinq champs en
colonnes, une pile par case, sa hauteur vaut la justesse. La couleur dit ce que la hauteur
ne peut pas dire, et elle change avec l'étape :
  01  cinq cases vertes  le routage publié, celui qui est en vigueur
  02  une case descend   le routage visé : « nom » passe de large à gen-4b, et c'est LA
                         seule différence entre les deux routages — retrouvée dans
                         document.json lignes 5-11 et 27-33
  03  deux trous         là où le lecteur de règles rendait 0 %, il ne rend plus rien.
                         L'abstention, dessinée : la case rouge devient un vide
  04  aucun vert         rien n'est tenu pour un résultat — c'est l'écran de ce qu'on
                         refuse de publier
  05  tout est vert      les 16 807 routages énumérés, un par un

PAS DE JAVASCRIPT POUR LE FOND
Les cinq écrans sont dans le HTML et c'est l'ADRESSE qui choisit lequel se montre, par
`:target` et `:has()`. Conséquences, et c'est pour elles qu'on le fait ainsi : le bouton
Retour marche, le lien s'envoie par courriel et ouvre le bon constat, la mise en favori
tient, et une extension qui bloque les scripts ne casse rien. Le JavaScript n'ajoute
qu'une chose — l'objet qui se dévoile — et son absence ne retire rien.

LA HAUTEUR DU VERT NE PEUT PLUS SAUTER
Les cinq titres sont EMPILÉS DANS LA MÊME CELLULE de grille. La cellule prend la hauteur
du plus haut, à toutes les largeurs, pour toujours, et se remet à jour toute seule quand
le texte change. `visibility:hidden` et non `display:none` : un enfant retiré du flux ne
dimensionne plus la cellule, et la réserve s'effondrerait au premier clic. Sans cela, le
titre 03 (cinq lignes) contre le titre 01 (quatre) ferait descendre l'arête verte d'environ
quatre-vingts pixels — et personne ne dirait « la bande a bougé », on dirait « la sculpture
a bougé », sur ce qu'on avait promis fixe.
"""
import importlib.util
import pathlib

BASE = pathlib.Path(__file__).parent
_spec = importlib.util.spec_from_file_location("bn", BASE / "batir-nav.py")
bn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bn)

# ── LES CINQ ÉCRANS ──────────────────────────────────────────────────────────
# Chaque chiffre affiché ici a été retrouvé dans ~/Documents/cascade, fichier et ligne,
# puis passé à une contre-épreuve qui devait le réfuter. Ce qui n'a pas été retrouvé ne
# s'affiche pas. Les réserves ne sont pas des concessions : chez Cascade, la réserve est
# le produit, et elle a la même place que le chiffre.
ECRANS = [
    {
        "no": "01",
        "onglet": "The gap",
        "oeil": "Finding 01, two rates over one desk",
        "titre": [("Both numbers", 0), ("are true.", 0),
                  ("Only one leaves", 1), ("your desk.", 1)],
        "question": "Which rate do you act on?",
        "chiffres": [
            ("On the dashboard", "94.4%", "Mean of five field rates", "vide", False),
            ("On your desk", "76.7%", "All five fields right on the same file, 92 of 120",
             "wilson", True),
            ("The gap", "17.7", "Points, over the same 120 case files", "ecart", False),
        ],
        "reserve": ("Both rates are computed correctly. Neither one is wrong. They answer "
                    "different questions, and only one of them is the question at your desk."),
    },
    {
        "no": "02",
        "onglet": "The cheaper routing",
        "oeil": "Finding 02, one field changes reader",
        "titre": [("Cost separates", 0), ("the two routings.", 0),
                  ("Accuracy", 1), ("does not.", 1)],
        "question": "Can a cheaper reader hold?",
        "chiffres": [
            ("Published routing", "$191", "Per 100 000 documents, on assumed prices",
             None, False),
            ("Aiming at the file", "$54", "3.5 times cheaper, worse on no file in this set",
             None, True),
            ("What it settles", "p = 0.25", "Three files change verdict. The sample cannot "
             "decide accuracy", None, False),
        ],
        "reserve": ("The bench file itself records decidable: false. Cost is what this "
                    "sample establishes; accuracy stays undecided. Both dollar figures are "
                    "measured latencies multiplied by assumed prices."),
    },
    {
        "no": "03",
        "onglet": "Silence over a guess",
        "oeil": "Finding 03, the break-even for silence",
        "titre": [("A blank gets", 0), ("read again.", 0),
                  ("A wrong value", 1), ("gets filed.", 1)],
        "question": "Is a blank worth more than a wrong value?",
        "chiffres": [
            ("Wrong values removed", "85", "Out of 150 fields, on the hard corpus",
             None, False),
            ("Right values lost", "12", "The price of silence, 7.1 removed for each one",
             None, False),
            ("What survives", "62.3%", "Precision of what is delivered, against 30% with "
             "no abstention", None, True),
        ],
        "reserve": ("Where the break-even sits is your decision, not ours: it depends on "
                    "what a wrong value costs you against what a blank costs you. We "
                    "publish the curve, you place the point."),
    },
    {
        "no": "04",
        "onglet": "What we withhold",
        "oeil": "Finding 04, withheld for non-reproducibility",
        "titre": [("Every count held", 0), ("across two passes.", 0),
                  ("Every duration", 1), ("moved.", 1)],
        "question": "What did we refuse to publish?",
        "chiffres": [
            ("Counts, two passes", "identical", "Every count matched to the digit",
             None, False),
            ("Durations, two passes", "16 to 60%", "Median duration moved between the "
             "same two passes", None, True),
            ("Conclusions retracted", "32", "Of which 11 were caught before anyone saw them",
             None, False),
        ],
        "reserve": ("No duration from this bench appears anywhere on this site. Removing a "
                    "measurement is a discipline, not a guarantee about the ones we keep."),
    },
    {
        "no": "05",
        "onglet": "The engagement",
        "oeil": "Finding 05, what the engagement delivers",
        "titre": [("Every routing", 0), ("enumerated.", 0),
                  ("One report you", 1), ("can argue with.", 1)],
        "question": "What runs, and for how long?",
        "chiffres": [
            ("Routings enumerated", "16 807", "Every combination, not a sample", None, True),
            ("Case files", "120", "Held out, five fields each", None, False),
            ("Tests shipped", "584", "Across 65 files, running on your machine", None, False),
        ],
        "reserve": ("You supply nothing: the measurement runs on your records, on your "
                    "machine. You receive a frozen report, contestable line by line, in "
                    "thirty days."),
    },
]

PARCOURS_CSS = """
  /* ── LA PILE : les cinq écrans occupent LA MÊME cellule de grille ──────────
     La cellule prend la hauteur du plus haut, à toute largeur et pour toujours ; la
     réserve se met à jour seule quand le texte change. C'est la seule façon de tenir
     « le titre va du haut du vert au bas du vert » sur cinq titres de longueurs
     différentes sans écrire un nombre en dur qui sera faux à la prochaine retouche. */
  .pile{display:grid}
  .pile > *{grid-area:1 / 1}
  /* visibility, JAMAIS display:none : un enfant retiré du flux ne dimensionne plus la
     cellule, et la hauteur réservée s'effondrerait au premier clic. */
  .vue{visibility:hidden;opacity:0;pointer-events:none;
       transition:opacity .22s ease,visibility 0s linear .22s}
  .vue.la{visibility:visible;opacity:1;pointer-events:auto;
          transition:opacity .22s ease .04s,visibility 0s}

  .haut{padding-top:clamp(1.1rem,2.6vh,2rem);padding-bottom:clamp(1.1rem,2.6vh,2rem)}
  h1{margin:0}

  /* MESURÉ, ET LE PREMIER PLACEMENT ÉTAIT LE MAUVAIS. Ancrée sous l'objet, la légende
     est hors du flux ; les cartes, elles, prennent toute la largeur et REMONTENT quand la
     fenêtre baisse. À 1440x900 elles la touchaient de 3 px, à 1440x760 de 103. Aucun
     réglage de la légende ne règle ça : c'est la carte qui monte, pas la légende qui
     descend. Elle rentre donc dans le flux, à gauche, sous la réserve — et la pile qui
     réserve la hauteur du bloc réserve la sienne du même coup. */
  .legende{display:none}
  .leg-fig{margin:.15rem 0 0;max-width:56ch;font:400 12.5px/1.5 var(--sans);
           color:var(--pale)}
  .leg-fig b{color:var(--demi);font-weight:600;letter-spacing:.1em;
             text-transform:uppercase;font-size:10.5px;margin-right:.5rem}

  /* ── L'OBJET : cinq états, la même caméra ─────────────────────────────────
     Rendus au même azimut (-118) et à la même élévation (42), donc la boîte englobante
     est identique au pixel — mesurée, pas supposée. Seules les pièces changent. */
  .plaque img{width:100%;display:block;grid-area:1 / 1}
  .plaque{display:grid}

  /* ── LE BLOC DE CHIFFRES ──────────────────────────────────────────────────
     Trois cellules, la même forme aux cinq écrans : étiquette, valeur, ce qu'elle
     mesure. Une forme qui change d'un écran à l'autre se lit comme un rechargement. */
  .bande{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
         border-top:1.6px solid var(--encre);border-bottom:1px solid var(--filet-clair);
         max-width:min(52rem, calc(104vw - min(40vw,600px)
                  - 2 * clamp(1.2rem,3.4vw,3.2rem) - 1.5rem))}
  .cel{padding:.6rem 1.1rem .65rem 0;border-right:1px solid var(--filet-clair)}
  .cel:last-child{border-right:none;padding-right:0}
  .cel:not(:first-child){padding-left:1.1rem}
  .cel .et{display:block;font:600 10.5px/1.3 var(--sans);letter-spacing:.1em;
           text-transform:uppercase;color:var(--pale)}
  .cel .v{display:block;margin:.18rem 0 .1rem;
          font:600 clamp(1.5rem,2.4vw,2.05rem)/1 var(--texte);
          font-variant-numeric:tabular-nums;letter-spacing:-.02em}
  .cel.cle .v{color:var(--vert-titre)}
  .cel .q{display:block;font:400 12.5px/1.4 var(--sans);color:var(--pale);max-width:27ch}
  .mou{width:100%;max-width:13rem;height:24px;display:block;margin-top:.15rem}
  .mou .ax{stroke:var(--filet-clair);stroke-width:1}
  .mou .br{stroke:var(--encre);stroke-width:1.5;fill:none}
  .mou .pt{fill:var(--encre)}
  .mou .vide{font:400 10.5px/1 var(--sans);fill:var(--pale);font-style:italic}
  .mou .g{font:500 9px/1 var(--mono);fill:var(--pale)}

  .reserve{margin:.55rem 0 0;max-width:62ch;font:400 14px/1.5 var(--sans);
           color:var(--demi);border-left:2px solid var(--vert-titre);padding-left:.8rem}
  .reserve b{color:var(--encre);font-weight:600}

  .bas{position:relative;z-index:3;margin-top:clamp(.6rem,1.7vh,1.1rem);
       display:flex;flex-direction:column;gap:clamp(.45rem,1.2vh,.8rem);
       align-items:flex-start}

  /* ── LES CINQ PARCOURS, MIS EN VALEUR ─────────────────────────────────────
     Ce n'est plus une réglure de navigation, c'est le bloc principal du bas : cinq
     cartes pleine largeur, chacune portant son numéro, son titre et la question à
     laquelle elle répond. On choisit en sachant ce qu'on va lire. */
  .choix{position:relative;z-index:5;margin-top:clamp(.9rem,3.4vh,2.4rem);
         margin-bottom:.35rem;
         display:grid;grid-template-columns:repeat(5,1fr);gap:clamp(.35rem,.9vw,.7rem)}
  .choix .lien{all:unset;cursor:pointer;display:block;
               border:1px solid var(--filet-clair);
               padding:clamp(.6rem,1.5vh,1rem) clamp(.7rem,1vw,1.05rem)
                       clamp(.7rem,1.7vh,1.1rem);
               background:linear-gradient(168deg,rgba(255,252,244,.55),
                          rgba(255,252,244,.14));
               transition:border-color .16s ease,transform .16s var(--montee),
                          box-shadow .16s ease,background .16s ease}
  .choix .lien:hover{border-color:var(--filet);transform:translateY(-1px);
                     box-shadow:0 4px 12px rgba(20,37,30,.12)}
  .choix .lien:active{transform:translateY(0);box-shadow:none}
  .choix .lien:focus-visible{outline:none;
    box-shadow:0 0 0 2px var(--papier-haut),0 0 0 4.5px var(--nuit-b)}
  .choix .no{display:block;font:500 11.5px/1 var(--mono);letter-spacing:.05em;
             color:var(--filet)}
  .choix .ti{display:block;margin:.28rem 0 .3rem;
             font:400 clamp(15px,1.2vw,17.5px)/1.18 var(--texte);color:var(--demi);
             letter-spacing:-.008em}
  .choix .qu{display:block;font:400 12.5px/1.4 var(--sans);color:var(--pale);
             display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
             overflow:hidden}
  /* L'état courant ne tient JAMAIS à la seule couleur : un filet vert épais en tête de
     carte, le titre en gras, et le mot « reading » écrit. Trois marques, dont deux
     survivent à un écran monochrome et au daltonisme. */
  .choix .lien.la{border-color:var(--vert-titre);
                  box-shadow:inset 0 3px 0 var(--vert-titre);
                  background:linear-gradient(168deg,rgba(255,252,244,.8),
                             rgba(255,252,244,.4))}
  .choix .lien.la .no{color:var(--vert-titre)}
  .choix .lien.la .ti{color:var(--encre);font-weight:600}
  .choix .lien.la .no::after{content:" reading";font:600 9.5px/1 var(--sans);
                             letter-spacing:.1em;text-transform:uppercase;
                             color:var(--vert-titre)}
  .ancre{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}

  /* MESURÉ : neuf pixels de trop à 1280x800, et neuf seulement. Ils sont rendus par
     l'écart au-dessus des cartes et la marge de la légende, pas par un texte lu. */
  @media (min-width:1081px) and (max-width:1360px){
    .choix{margin-top:clamp(.6rem,2vh,1.4rem)}
    .leg-fig{margin-top:.05rem;font-size:12px}
  }
  @media (max-width:1200px){ .choix .qu{display:none} }
  @media (max-width:1080px){
    .choix{grid-template-columns:1fr 1fr}
    .bande{grid-template-columns:1fr;max-width:none}
    .cel{border-right:none;border-bottom:1px solid var(--filet-clair);padding-left:0}
    .cel:last-child{border-bottom:none}
  }
"""


def moustache(kind):
    """Les mêmes moustaches que le tableau de l'écran 01, à la même échelle 60-100."""
    X = bn.X
    if kind == "vide":
        return ('<svg class="mou" viewBox="0 0 210 24" role="img" '
                'aria-label="No interval: a mean of rates is not a proportion.">'
                '<line class="ax" x1="6" y1="12" x2="204" y2="12"></line>'
                '<text class="vide" x="105" y="16" text-anchor="middle">no interval</text>'
                f'<circle class="pt" cx="{X(94.4)}" cy="12" r="3.2"></circle></svg>')
    if kind == "wilson":
        return ('<svg class="mou" viewBox="0 0 210 24" role="img" '
                'aria-label="Wilson 95% interval from 68.3 to 83.3 percent.">'
                '<line class="ax" x1="6" y1="12" x2="204" y2="12"></line>'
                f'<path class="br" d="M{X(68.3)} 6 L{X(68.3)} 18 M{X(68.3)} 12 '
                f'L{X(83.3)} 12 M{X(83.3)} 6 L{X(83.3)} 18"></path>'
                f'<circle class="pt" cx="{X(76.7)}" cy="12" r="3.2"></circle>'
                f'<text class="g" x="{X(68.3)}" y="23" text-anchor="middle">68.3</text>'
                f'<text class="g" x="{X(83.3)}" y="23" text-anchor="middle">83.3</text></svg>')
    return ('<svg class="mou" viewBox="0 0 210 24" role="img" '
            'aria-label="A gap of 17.7 points between the two rates.">'
            f'<path class="br" d="M{X(76.7)} 7 L{X(76.7)} 17 M{X(76.7)} 12 L{X(94.4)} 12 '
            f'M{X(94.4)} 7 L{X(94.4)} 17"></path>'
            f'<text class="g" x="{(X(76.7) + X(94.4)) / 2:.1f}" y="23" '
            'text-anchor="middle">17.7 points</text></svg>')


def titre_html(lignes):
    return " ".join(
        f'<span class="ligne"><i{" class=\"deux\"" if d else ""}>{t}</i></span>'
        for t, d in lignes)


def bande_html(chiffres):
    cel = []
    for et, v, q, mou, cle in chiffres:
        m = moustache(mou) if mou else ""
        cel.append(f'<div class="cel{" cle" if cle else ""}"><span class="et">{et}</span>'
                   f'<span class="v">{v}</span><span class="q">{q}</span>{m}</div>')
    return '<div class="bande">' + "".join(cel) + "</div>"


# Les règles qui font tout le travail sans une ligne de JavaScript : l'adresse choisit.
regles = []
for e in ECRANS:
    n = e["no"]
    if n == "01":
        continue
    regles.append(
        f'  .ecran:has(#e{n}:target) [data-e="{n}"]{{visibility:visible;opacity:1;'
        f'pointer-events:auto;transition:opacity .22s ease .04s,visibility 0s}}\n'
        f'  .ecran:has(#e{n}:target) [data-e]:not([data-e="{n}"]){{visibility:hidden;'
        f'opacity:0;pointer-events:none;transition:opacity .22s ease,'
        f'visibility 0s linear .22s}}\n'
        f'  .ecran:has(#e{n}:target) .choix .lien[href="#e{n}"]{{border-color:'
        f'var(--vert-titre);box-shadow:inset 0 3px 0 var(--vert-titre);'
        f'background:linear-gradient(168deg,rgba(255,252,244,.8),'
        f'rgba(255,252,244,.4))}}\n'
        f'  .ecran:has(#e{n}:target) .choix .lien[href="#e{n}"] .no{{'
        f'color:var(--vert-titre)}}\n'
        f'  .ecran:has(#e{n}:target) .choix .lien[href="#e{n}"] .ti{{'
        f'color:var(--encre);font-weight:600}}\n'
        f'  .ecran:has(#e{n}:target) .choix .lien[href="#e{n}"] .no::after{{'
        f'content:" reading";font:600 9.5px/1 var(--sans);letter-spacing:.1em;'
        f'text-transform:uppercase;color:var(--vert-titre)}}\n'
        f'  .ecran:has(#e{n}:target) .choix .lien[href="#e01"]{{border-color:'
        f'var(--filet-clair);box-shadow:none;background:linear-gradient(168deg,'
        f'rgba(255,252,244,.55),rgba(255,252,244,.14))}}\n'
        f'  .ecran:has(#e{n}:target) .choix .lien[href="#e01"] .no{{'
        f'color:var(--filet)}}\n'
        f'  .ecran:has(#e{n}:target) .choix .lien[href="#e01"] .ti{{'
        f'color:var(--demi);font-weight:400}}\n'
        f'  .ecran:has(#e{n}:target) .choix .lien[href="#e01"] .no::after{{content:""}}\n')
CIBLES = "".join(regles)

# La prise au clavier, posée APRÈS les règles d'état et à leur spécificité (l'ID dans
# :has) : à égalité de poids, la dernière règle gagne, et l'anneau de prise passe
# au-dessus de toute marque « courant ». Mesuré par ergonomie.mjs : sans ce bloc, la
# carte courante ne changeait plus du tout quand le clavier l'atteignait.
FOCUS = (".ecran .choix .lien:focus-visible,"
         + ",".join(f'.ecran:has(#e{e["no"]}:target) .choix .lien:focus-visible'
                    for e in ECRANS)
         + "{outline:none;box-shadow:0 0 0 2px var(--papier-haut),"
           "0 0 0 4.5px var(--nuit-b)}")
CIBLES += FOCUS

ancres = "".join(f'<i class="ancre" id="e{e["no"]}" aria-hidden="true"></i>' for e in ECRANS)

titres = "".join(
    f'<h1 class="vue{" la" if e["no"] == "01" else ""}" data-e="{e["no"]}">'
    f'{titre_html(e["titre"])}</h1>' for e in ECRANS)

yeux = "".join(
    f'<span class="oeil vue{" la" if e["no"] == "01" else ""}" data-e="{e["no"]}">'
    f'{e["oeil"]}</span>' for e in ECRANS)

objets = "".join(
    f'<img class="vue{" la" if e["no"] == "01" else ""}" data-e="{e["no"]}" '
    f'src="rendus/etats/objet-{e["no"]}.webp" '
    f'alt="{"Seven readers by five fields, one stack of chips per cell. " if e["no"] == "01" else ""}'
    f'{e["onglet"]}"{"" if e["no"] == "01" else ""}>' for e in ECRANS)

blocs = "".join(
    f'<div class="vue{" la" if e["no"] == "01" else ""}" data-e="{e["no"]}">'
    f'{bande_html(e["chiffres"])}'
    f'<p class="reserve"><b>What this does not prove.</b> {e["reserve"]}</p>'
    f'</div>' for e in ECRANS)

cartes = "".join(
    f'<a class="lien{" la" if e["no"] == "01" else ""}" href="#e{e["no"]}">'
    f'<span class="no">{e["no"]}</span>'
    f'<span class="ti">{e["onglet"]}</span>'
    f'<span class="qu">{e["question"]}</span></a>' for e in ECRANS)

SCRIPT = """<script>
/* Le JavaScript n'ajoute qu'une chose : la même horloge pour la cause et l'effet.
   Sans lui, l'adresse fait déjà tout le travail — c'est la raison d'être des règles
   :target ci-dessus, et non un repli. */
(() => {
  const ecran = document.querySelector(".ecran");
  const montrer = (n) => {
    for (const el of document.querySelectorAll("[data-e]"))
      el.classList.toggle("la", el.dataset.e === n);
    for (const a of document.querySelectorAll(".choix .lien"))
      a.classList.toggle("la", a.getAttribute("href") === "#e" + n);
    const t = document.querySelector(`h1[data-e="${n}"]`);
    document.title = "Cascade, " + (t ? t.textContent.trim() : "finding " + n);
  };
  const lire = () => (location.hash.match(/^#e(0[1-5])$/) || [, "01"])[1];
  addEventListener("hashchange", () => montrer(lire()));
  montrer(lire());
})();
document.fonts.ready.then(() => requestAnimationFrame(() =>
  requestAnimationFrame(() => document.body.classList.add("go"))));
</script>"""

(BASE / "PARCOURS.html").write_text(f"""<!doctype html>
<meta charset="utf-8"><title>Cascade, the gap</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%2314251e'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<style>{bn.COMMUN}{PARCOURS_CSS}{CIBLES}</style>
<div class="ecran">
  {ancres}
  <div class="tete"><b>CASCADE</b><span>routing audit, KYC extraction</span>
    <span class="d">report 64bdacf, measured once and frozen</span></div>
  <div class="pile">{yeux}</div>
  <div class="haut"><div class="pile">{titres}</div></div>
  <figure class="plaque">{objets}</figure>
  <span class="socle-ombre"></span>
  <div class="bas"><div class="pile">{blocs}</div>
    <p class="leg-fig"><b>Figure 1</b>Seven readers down, five fields across; one stack per
      cell, its height the accuracy. The empty row is the human operator, never sampled
      field by field.</p>
  </div>
  <nav class="choix" aria-label="Findings">{cartes}</nav>
  {bn.PIED}
</div>
{SCRIPT}
""", encoding="utf-8")
print("  PARCOURS.html")
