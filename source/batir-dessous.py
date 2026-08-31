#!/usr/bin/env python3
"""Le dessous : six mécanismes pour quitter cet écran, un par maquette.

CE QU'ARSLANE A ARRÊTÉ LE 31 AOÛT
Le haut est clos : titre sur toute la hauteur du vert, objet seul à droite. La méthode
est de haut en bas, donc la seule zone qui varie ici est LE DESSOUS — l'affichage et
les boutons qui mènent aux autres pages. Le bloc de chiffres et la réserve restent :
ils sont le constat, pas la navigation.

LA VALEUR DE CHACUNE, ÉCRITE AVANT DE DESSINER
(un mécanisme par maquette ; si deux se décrivent pareil, c'est la même — règle des
six formes)

  W1  les onglets du dossier   la page est un rapport : les cinq constats sont les
                               onglets d'une chemise, l'ouvert est relié au contenu.
                               La position se voit sans lire.
  W2  les deux lecteurs        une banque lit à deux : celui qui décide suit les
                               constats, celui qui vérifie saute aux annexes. Chacun
                               sa porte, côte à côte, à poids égal.
  W3  le sommaire              le site EST le rapport, donc il navigue comme un
                               rapport : une table des matières, constats et annexes,
                               avec des points de conduite.
  W4  le fil de lecture        l'écran pousse vers l'avant : position « 01 sur 05 »
                               toujours lisible, et le SUIVANT annoncé avec sa
                               question — on sait ce qu'on va lire avant de cliquer.
  W5  les deux gestes          une page de vente n'a que deux gestes qui comptent :
                               mesurer (la vente) ou continuer à lire. Deux boutons
                               francs, l'index complet en une ligne discrète dessous.
  W6  les vignettes d'état     le menu MONTRE l'état que la sculpture prendra : la
                               vraie vignette du rendu de chaque étape dans son
                               bouton. L'objet devient la carte du site.

TOUT EST FAISABLE SUR LE MOTEUR EXISTANT
Chaque mécanisme est du HTML et du CSS posés sur la mécanique :target déjà construite
dans PARCOURS.html — cinq adresses réelles, Retour qui marche, aucun script requis.
Les vignettes de W6 sont les cinq rendus déjà produits, recadrés à la même boîte.
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

E0 = bp.ECRANS[0]
ANNEXES = bn.ANNEXES

# ── le tronc commun : tout ce qui est arrêté, identique dans les six ─────────
TRONC = f"""  <div class="tete"><b>CASCADE</b><span>routing audit, KYC extraction</span>
    <span class="d">report 64bdacf, measured once and frozen</span></div>
  <span class="oeil">{E0["oeil"]}</span>
  <div class="haut"><h1>{bp.titre_html(E0["titre"])}</h1></div>
  <figure class="plaque"><img src="rendus/etats/objet-01.webp" alt="Seven readers down,
    five fields across, one stack of chips per cell; five green cells mark the
    published routing."></figure>
  <span class="socle-ombre"></span>
  <div class="bas">
    {bp.bande_html(E0["chiffres"])}
    <p class="reserve"><b>What this does not prove.</b> {E0["reserve"]}</p>
    <p class="leg-fig"><b>Figure 1</b>Seven readers down, five fields across; one stack
      per cell, its height the accuracy. The empty row is the human operator, never
      sampled field by field.</p>
  </div>"""

PIED_MIN = ('<div class="pied"><span class="dit">On your records, on your machine. '
            '<b>Nothing leaves the network.</b></span></div>')

COMMUN_W = """
  h1{margin:0}
  .legende{display:none}
  .plaque img{width:100%;display:block;opacity:1;transition:none;position:static}
  /* Toute prise se voit : au survol, au clavier, à l'appui. Rien de mort. */
  .d-lien{all:unset;cursor:pointer;display:block}
  .d-lien:focus-visible{outline:none;
    box-shadow:0 0 0 2px var(--papier-haut),0 0 0 4.5px var(--nuit-b)}
  .dessous{position:relative;z-index:5;margin-top:auto}
  .no-d{font:500 11.5px/1 var(--mono);letter-spacing:.05em;color:var(--filet)}
  .ti-d{font:400 15px/1.25 var(--texte);color:var(--demi)}
  .qu-d{font:400 12.5px/1.4 var(--sans);color:var(--pale)}
  .lit::after{content:" reading";font:600 9.5px/1 var(--sans);letter-spacing:.1em;
              text-transform:uppercase;color:var(--vert-titre)}
"""


def lien(no, titre, question="", cls="", cur=False):
    q = f'<span class="qu-d">{question}</span>' if question else ""
    c = ' aria-current="true"' if cur else ""
    return (f'<a class="d-lien {cls}{" la" if cur else ""}" href="#e{no}"{c}>'
            f'<span class="no-d{" lit" if cur else ""}">{no}</span>'
            f'<span class="ti-d">{titre}</span>{q}</a>')


# ══ W1 · LES ONGLETS DU DOSSIER ══════════════════════════════════════════════
W1_CSS = """
  .dessous{display:flex;gap:3px;align-items:flex-end;
           border-bottom:1.6px solid var(--encre)}
  .d-lien{flex:1;display:flex;gap:.55rem;align-items:baseline;
          padding:.55rem .8rem .6rem;border:1px solid var(--filet-clair);
          border-bottom:none;background:linear-gradient(rgba(255,252,244,.28),
          rgba(255,252,244,.08));transition:background .16s ease,padding .16s ease}
  .d-lien:hover{background:rgba(255,252,244,.55);padding-bottom:.75rem}
  /* L'onglet ouvert est RELIÉ : plus haut, plus clair, et il passe par-dessus le
     filet gras — la chemise est ouverte à cette page. */
  .d-lien.la{background:linear-gradient(rgba(255,252,244,.85),rgba(255,252,244,.5));
             border-color:var(--encre);padding:.75rem .8rem .9rem;
             margin-bottom:-1.6px;border-bottom:1.6px solid var(--papier-haut)}
  .d-lien.la .ti-d{color:var(--encre);font-weight:600}
  .pied{border-top:none;margin-top:0;padding-top:.6rem}
  @media (max-width:1080px){.dessous{flex-wrap:wrap;border-bottom:none}
    .d-lien{border-bottom:1px solid var(--filet-clair)}}
"""
W1_HTML = ('<nav class="dessous" aria-label="Findings">'
           + "".join(lien(e["no"], e["onglet"], cur=e["no"] == "01")
                     for e in bp.ECRANS)
           + "</nav>" + bn.PIED.replace('class="pied"', 'class="pied"', 1))

# ══ W2 · LES DEUX LECTEURS ═══════════════════════════════════════════════════
W2_CSS = """
  .dessous{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);
           column-gap:clamp(1.6rem,4vw,3.6rem);align-items:start;
           border-top:1px solid var(--filet-clair);padding-top:.5rem}
  .dessous h2{margin:0 0 .35rem;font:600 10.5px/1.3 var(--sans);letter-spacing:.13em;
              text-transform:uppercase;color:var(--pale)}
  .col-lire .liste{display:grid;grid-template-columns:1fr 1fr;
                   grid-auto-flow:column;grid-template-rows:repeat(3,auto);
                   column-gap:1.2rem}
  .col-lire .d-lien{display:flex;gap:.6rem;align-items:baseline;padding:.28rem .5rem;
                    margin-left:-.5rem;border-left:2px solid transparent}
  .col-lire .d-lien:hover{border-left-color:var(--filet);background:rgba(255,252,244,.4)}
  .col-lire .d-lien.la{border-left-color:var(--vert-titre);
                       background:rgba(35,84,63,.07)}
  .col-lire .d-lien.la .ti-d{color:var(--encre);font-weight:600}
  .col-verif{border-left:1px solid var(--filet-clair);
             padding-left:clamp(1.2rem,2.6vw,2.4rem)}
  .col-verif .d-lien{display:flex;gap:.6rem;align-items:baseline;
                     border:1px solid var(--filet-clair);
                     padding:.3rem .7rem;margin-bottom:.3rem;
                     background:linear-gradient(rgba(255,252,244,.5),
                     rgba(255,252,244,.15));transition:border-color .16s ease}
  .col-verif .d-lien:hover{border-color:var(--filet)}
  .col-verif .et-d{font:600 9.5px/1.4 var(--sans);letter-spacing:.11em;
                   text-transform:uppercase;color:var(--pale);flex:none}
  .col-verif .ti-d{font-size:14.5px;color:var(--encre);white-space:nowrap;
                   overflow:hidden;text-overflow:ellipsis}
  @media (max-width:1080px){.dessous{grid-template-columns:1fr}
    .col-verif{border-left:none;padding-left:0;margin-top:.8rem}}
"""
W2_HTML = ('<div class="dessous">'
           '<div class="col-lire"><h2>Read on, the five findings</h2>'
           '<div class="liste">'
           + "".join(lien(e["no"], e["onglet"], cur=e["no"] == "01")
                     for e in bp.ECRANS)
           + '</div></div>'
           '<div class="col-verif"><h2>For your reviewers</h2>'
           '<a class="d-lien" href="#annexe-securite"><span class="et-d">Appendix</span>'
           '<span class="ti-d">Security and data handling</span></a>'
           '<a class="d-lien" href="#annexe-methode"><span class="et-d">Appendix</span>'
           '<span class="ti-d">Method and reproducibility</span></a>'
           '<a class="d-lien" href="#annexe-conditions"><span class="et-d">Appendix</span>'
           '<span class="ti-d">Terms of engagement</span></a>'
           '</div></div>'
           '<div class="pied"><span class="dit">On your records, on your machine. '
           '<b>Nothing leaves the network.</b></span>'
           '<nav class="annexes" aria-label="More">'
           '<button class="lien" type="button">Questions</button>'
           '<button class="lien" type="button">Privacy</button>'
           '<button class="lien" type="button">Accessibility</button></nav></div>')

# ══ W3 · LE SOMMAIRE ═════════════════════════════════════════════════════════
W3_CSS = """
  .dessous{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);
           column-gap:clamp(1.8rem,4.5vw,4rem);border-top:1.6px solid var(--encre);
           padding-top:.28rem}
  .dessous h2{margin:0 0 .22rem;font:600 10.5px/1.3 var(--sans);letter-spacing:.13em;
              text-transform:uppercase;color:var(--pale)}
  .d-lien{display:flex;align-items:baseline;gap:.55rem;padding:.25rem .2rem;
          margin:-.12rem -.2rem}
  .d-lien:hover .ti-d{color:var(--encre)}
  .d-lien.la .ti-d{color:var(--encre);font-weight:600}
  /* Les points de conduite d'une vraie table des matières : le fil que l'œil suit. */
  .pts{flex:1;min-width:1.5rem;border-bottom:1px dotted var(--filet);
       transform:translateY(-.28em)}
  .fol{font:400 12px/1.3 var(--sans);color:var(--pale);max-width:42%;
       white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .som-a .no-d{font-family:var(--sans);font-weight:600;font-size:11px}
  .som-a .deux-cols{display:grid;grid-template-columns:1fr 1fr;
                    grid-auto-flow:column;grid-template-rows:repeat(3,auto);
                    column-gap:1.4rem}
  .som-a .pts{min-width:.8rem}
  .pied{padding-top:.3rem}
  .fol{transform:translateY(.06em)}
  @media (max-width:1080px){.dessous{grid-template-columns:1fr}
    .som-a{margin-top:.7rem}}
"""
_som_c = "".join(
    f'<a class="d-lien{" la" if e["no"] == "01" else ""}" href="#e{e["no"]}"'
    f'{" aria-current=\"true\"" if e["no"] == "01" else ""}>'
    f'<span class="no-d{" lit" if e["no"] == "01" else ""}">{e["no"]}</span>'
    f'<span class="ti-d">{e["onglet"]}</span><span class="pts" aria-hidden="true"></span>'
    f'<span class="fol">{e["question"]}</span></a>' for e in bp.ECRANS)
_som_a = "".join(
    f'<a class="d-lien" href="#annexe-{i}"><span class="no-d">{c}</span>'
    f'<span class="ti-d">{t}</span><span class="pts" aria-hidden="true"></span></a>'
    for i, (c, t) in enumerate(zip("ABCDEF", ANNEXES)))
W3_HTML = ('<div class="dessous">'
           '<nav class="som-c" aria-label="Findings"><h2>Contents, the five findings</h2>'
           + _som_c + '</nav>'
           '<nav class="som-a" aria-label="Appendices"><h2>Appendices</h2>'
           '<div class="deux-cols">' + _som_a + '</div></nav></div>' + PIED_MIN)

# ══ W4 · LE FIL DE LECTURE ═══════════════════════════════════════════════════
W4_CSS = """
  .dessous{display:flex;align-items:stretch;gap:clamp(.9rem,2vw,1.8rem);
           border-top:1px solid var(--filet-clair);padding-top:.75rem}
  .fil-pos{display:flex;flex-direction:column;gap:.45rem;justify-content:center}
  .fil-cpt{font:500 13px/1 var(--mono);color:var(--pale);letter-spacing:.06em}
  .fil-cpt b{color:var(--encre);font-weight:600}
  .fil-seg{display:flex;gap:.3rem}
  .fil-seg .d-lien{width:2.4rem;height:24px;background:linear-gradient(
                     var(--filet-clair),var(--filet-clair)) center/100% 5px no-repeat;
                   transition:background .16s ease}
  .fil-seg .d-lien:hover{background:linear-gradient(var(--filet),var(--filet))
                         center/100% 5px no-repeat}
  .fil-seg .d-lien.la{background:linear-gradient(var(--vert-titre),var(--vert-titre))
                      center/100% 5px no-repeat}
  .fil-suiv{margin-left:auto;display:flex;gap:.9rem;align-items:center;
            border:1px solid var(--encre);padding:.7rem 1.1rem;
            background:linear-gradient(rgba(255,252,244,.6),rgba(255,252,244,.25));
            transition:transform .16s var(--montee),box-shadow .16s ease}
  .fil-suiv:hover{transform:translateY(-1px);box-shadow:0 5px 14px rgba(20,37,30,.18)}
  .fil-suiv:active{transform:translateY(1px);box-shadow:none}
  .fil-suiv .bloc-d{display:flex;flex-direction:column;gap:.15rem}
  .fil-suiv .ti-d{color:var(--encre);font-weight:600}
  .fil-suiv .fl{font:400 19px/1 var(--sans);color:var(--vert-titre);
                transition:transform .2s var(--montee)}
  .fil-suiv:hover .fl{transform:translateX(3px)}
  @media (max-width:1080px){.dessous{flex-wrap:wrap}.fil-suiv{margin-left:0;flex:1}}
"""
W4_HTML = ('<div class="dessous">'
           '<div class="fil-pos"><span class="fil-cpt"><b>01</b> of 05, the gap</span>'
           '<nav class="fil-seg" aria-label="Findings">'
           + "".join(f'<a class="d-lien{" la" if e["no"] == "01" else ""}" '
                     f'href="#e{e["no"]}" aria-label="{e["no"]}, {e["onglet"]}"'
                     f'{" aria-current=\"true\"" if e["no"] == "01" else ""}></a>'
                     for e in bp.ECRANS)
           + '</nav></div>'
           '<a class="d-lien fil-suiv" href="#e02"><span class="no-d">NEXT, 02</span>'
           '<span class="bloc-d"><span class="ti-d">The cheaper routing</span>'
           '<span class="qu-d">Can a cheaper reader hold?</span></span>'
           '<span class="fl" aria-hidden="true">&#8594;</span></a>'
           '</div>' + bn.PIED)

# ══ W5 · LES DEUX GESTES ═════════════════════════════════════════════════════
W5_CSS = """
  .dessous{display:flex;flex-direction:column;gap:.8rem}
  .gestes{display:flex;gap:1rem;flex-wrap:wrap;align-items:stretch}
  .geste{display:flex;gap:.9rem;align-items:center;padding:.85rem 1.3rem;
         transition:transform .16s var(--montee),box-shadow .16s ease}
  .geste:hover{transform:translateY(-1px);box-shadow:0 5px 16px rgba(20,37,30,.25)}
  .geste:active{transform:translateY(1px);box-shadow:none}
  .geste .fl{font:400 18px/1 var(--sans);transition:transform .2s var(--montee)}
  .geste:hover .fl{transform:translateX(3px)}
  .g-mesure{background:var(--encre);color:#f4f0e4;border:1px solid var(--encre);
            font:600 16px/1.2 var(--sans)}
  .g-lire{border:1px solid var(--encre);color:var(--encre);
          background:linear-gradient(rgba(255,252,244,.6),rgba(255,252,244,.25));
          font:400 15.5px/1.2 var(--texte)}
  .g-lire b{font-weight:600}
  .index-fin{display:flex;gap:1.4rem;flex-wrap:wrap;
             border-top:1px solid var(--filet-clair);padding-top:.55rem}
  .index-fin .d-lien{display:flex;gap:.45rem;align-items:baseline;
                     padding:.32rem .2rem;margin:-.06rem -.2rem}
  .index-fin .ti-d{font-size:13.5px}
  .index-fin .d-lien:hover .ti-d{color:var(--encre)}
  .index-fin .d-lien.la .ti-d{color:var(--encre);font-weight:600}
"""
W5_HTML = ('<div class="dessous">'
           '<div class="gestes">'
           '<a class="d-lien geste g-mesure" href="#e05">Measure my routing'
           '<span class="fl" aria-hidden="true">&#8594;</span></a>'
           '<a class="d-lien geste g-lire" href="#e02"><span>Keep reading, '
           '<b>02, the cheaper routing</b></span>'
           '<span class="fl" aria-hidden="true">&#8594;</span></a>'
           '</div>'
           '<nav class="index-fin" aria-label="Findings">'
           + "".join(lien(e["no"], e["onglet"], cur=e["no"] == "01")
                     for e in bp.ECRANS)
           + '</nav></div>' + bn.PIED)

# ══ W6 · LES VIGNETTES D'ÉTAT ════════════════════════════════════════════════
W6_CSS = """
  .dessous{display:grid;grid-template-columns:repeat(5,1fr);
           gap:clamp(.35rem,.9vw,.7rem)}
  .d-lien{display:flex;gap:.7rem;align-items:center;
          border:1px solid var(--filet-clair);padding:.45rem .6rem;
          background:linear-gradient(rgba(255,252,244,.5),rgba(255,252,244,.14));
          transition:border-color .16s ease,transform .16s var(--montee),
                     box-shadow .16s ease}
  .d-lien:hover{border-color:var(--filet);transform:translateY(-1px);
                box-shadow:0 4px 12px rgba(20,37,30,.12)}
  .d-lien:active{transform:translateY(0);box-shadow:none}
  /* La vignette est le VRAI rendu de l'état — le menu montre ce que la sculpture
     deviendra, il ne le raconte pas. */
  .d-lien img{width:3.6rem;height:auto;display:block;flex:none}
  .d-lien .bloc-d{display:flex;flex-direction:column;gap:.1rem;min-width:0}
  .d-lien .ti-d{font-size:14px;line-height:1.15}
  .d-lien.la{border-color:var(--vert-titre);box-shadow:inset 0 3px 0 var(--vert-titre);
             background:linear-gradient(rgba(255,252,244,.8),rgba(255,252,244,.4))}
  .d-lien.la .no-d{color:var(--vert-titre)}
  .d-lien.la .ti-d{color:var(--encre);font-weight:600}
  @media (max-width:1080px){.dessous{grid-template-columns:1fr 1fr}}
"""
W6_HTML = ('<nav class="dessous" aria-label="Findings">'
           + "".join(
               f'<a class="d-lien{" la" if e["no"] == "01" else ""}" '
               f'href="#e{e["no"]}"'
               f'{" aria-current=\"true\"" if e["no"] == "01" else ""}>'
               f'<img src="rendus/etats/objet-{e["no"]}.webp" alt="">'
               f'<span class="bloc-d">'
               f'<span class="no-d{" lit" if e["no"] == "01" else ""}">{e["no"]}</span>'
               f'<span class="ti-d">{e["onglet"]}</span></span></a>'
               for e in bp.ECRANS)
           + '</nav>' + bn.PIED)

SCRIPT = """<script>
document.fonts.ready.then(() => requestAnimationFrame(() =>
  requestAnimationFrame(() => document.body.classList.add("go"))));
</script>"""

VARIANTES = [
    ("W1", "onglets", W1_CSS, W1_HTML, "Cascade, file tabs"),
    ("W2", "deux-lecteurs", W2_CSS, W2_HTML, "Cascade, two readers"),
    ("W3", "sommaire", W3_CSS, W3_HTML, "Cascade, contents"),
    ("W4", "fil", W4_CSS, W4_HTML, "Cascade, the thread"),
    ("W5", "deux-gestes", W5_CSS, W5_HTML, "Cascade, two moves"),
    ("W6", "vignettes", W6_CSS, W6_HTML, "Cascade, state previews"),
]

for code, nom, css, html, titre in VARIANTES:
    (BASE / f"{code}-{nom}.html").write_text(f"""<!doctype html>
<meta charset="utf-8"><title>{titre}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%2314251e'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<script>document.documentElement.classList.add("js")</script>
<style>{bn.COMMUN}{bp.PARCOURS_CSS}{COMMUN_W}{css}</style>
<div class="ecran">
{TRONC}
  {html}
</div>
{SCRIPT}
""", encoding="utf-8")
    print(f"  {code}-{nom}.html")
