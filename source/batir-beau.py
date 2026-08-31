#!/usr/bin/env python3
"""Le dessous recomposé : la typographie travaille, le mobilier disparaît.

LE VERDICT D'ARSLANE, 31 AOÛT : « on dirait un produit Excel ». Il a raison, et la
faute est identifiable : le bas de l'écran était fait de MOBILIER — cellules filetées,
étiquettes de dix pixels, trois strates de boîtes grises — et l'espace sous l'objet
restait mort. La beauté d'un rapport ne vient pas des bordures : elle vient du corps,
de l'alignement et du blanc.

CE QUI CHANGE DANS LES CINQ, AVANT TOUTE DIRECTION
  · les chiffres passent en CORPS D'AFFICHE : 94,4 → 76,7 composé comme une phrase,
    l'écart annoté sur la flèche, la moustache de Wilson sous le taux qui compte ;
  · la réserve devient une NOTE DE MARGE en italique — l'appareil d'un rapport
    imprimé, posé dans l'espace sous l'objet qui ne servait à rien ;
  · presque plus une seule bordure : ce qui séparait par un filet sépare maintenant
    par la taille et par l'espace ;
  · toute prise fait au moins 40 px et répond au survol, au clavier, à l'appui.

LA VALEUR DE CHAQUE DIRECTION, ÉCRITE AVANT DE DESSINER
  V1  la double page    l'écran composé comme une double page de rapport annuel :
                        chiffres à gauche, note de marge à droite, et les cinq
                        constats en FOLIOS sur toute la largeur — de la typographie,
                        zéro mobilier.
  V2  le pupitre        la navigation reçoit un LIEU : un second bandeau nuit en bas,
                        miroir du premier, où les cinq constats vivent en grand.
                        Vert / papier / vert : la page est reliée comme un livre.
  V3  l'escalier        les cinq constats descendent en marches vers la droite, dans
                        la diagonale morte sous l'objet : l'espace vide devient le
                        chemin de lecture.
  V4  les chapitres     la colonne sous l'objet porte les numéros 01-05 en corps
                        géant, comme les chapitres au dos d'un livre : le côté droit
                        gagne un élément aussi sculptural que l'objet.
  V5  la règle          la navigation emprunte la forme de l'objet du produit : une
                        RÈGLE GRADUÉE pleine largeur, cinq stations, le curseur sur
                        la station courante. Un instrument, pas des boutons.
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
X = bn.X

# ── LE HAUT, ARRÊTÉ, IDENTIQUE PARTOUT ───────────────────────────────────────
HAUT = f"""  <div class="tete"><b>CASCADE</b><span>routing audit, KYC extraction</span>
    <span class="d">report 64bdacf, measured once and frozen</span></div>
  <span class="oeil">{E0["oeil"]}</span>
  <div class="haut"><h1>{bp.titre_html(E0["titre"])}</h1></div>
  <figure class="plaque"><img src="rendus/etats/objet-01.webp" alt="Seven readers down,
    five fields across, one stack of chips per cell; five green cells mark the
    published routing."></figure>
  <span class="socle-ombre"></span>"""

# ── LES CHIFFRES EN CORPS D'AFFICHE ──────────────────────────────────────────
# Une phrase composée, pas trois cellules : 94,4 tombe à 76,7, l'écart est écrit sur
# la flèche qui les relie, et l'intervalle est dessiné sous le taux qui compte.
MOU = (f'<svg class="mou-b" viewBox="0 0 210 22" role="img" '
       f'aria-label="Wilson 95% interval from 68.3 to 83.3 percent.">'
       f'<line class="ax" x1="6" y1="10" x2="204" y2="10"></line>'
       f'<path class="br" d="M{X(68.3)} 4 L{X(68.3)} 16 M{X(68.3)} 10 L{X(83.3)} 10 '
       f'M{X(83.3)} 4 L{X(83.3)} 16"></path>'
       f'<circle class="pt" cx="{X(76.7)}" cy="10" r="3"></circle>'
       f'<text class="g" x="{X(68.3)}" y="21" text-anchor="middle">68.3</text>'
       f'<text class="g" x="{X(83.3)}" y="21" text-anchor="middle">83.3</text></svg>')

CHIFFRES = f"""<div class="gf">
      <div class="gc"><span class="ge">On the dashboard</span>
        <span class="gv">94.4%</span>
        <span class="gn">Mean of five field rates.<br>Not a proportion, so no
          interval exists.</span></div>
      <div class="gfl" aria-hidden="true"><span class="gk">17.7 points</span>
        <svg viewBox="0 0 96 12" class="gfleche"><line x1="2" y1="6" x2="86" y2="6"
          stroke="currentColor" stroke-width="1.6"></line>
          <path d="M86 6 L77 1.5 M86 6 L77 10.5" stroke="currentColor"
          stroke-width="1.6" fill="none"></path></svg>
        <span class="gk">the gap</span></div>
      <div class="gc cle"><span class="ge">On your desk</span>
        <span class="gv">76.7%</span>
        {MOU}
        <span class="gn">All five fields right on the same file,<br>92 of 120
          case files.</span></div>
    </div>"""

# ── LA NOTE DE MARGE : la réserve, en appareil de rapport imprimé ────────────
APARTE = """<aside class="aparte">
    <p class="ap-t">What this does not prove</p>
    <p>Both rates are computed correctly. <b>Neither one is wrong.</b> They answer
      different questions, and only one of them is the question at your desk.</p>
    <p class="ap-fig">Figure 1 — one stack per reader and per field; the empty row is
      the human operator.</p>
  </aside>"""

RESERVE_G = """<div class="reserve-g">
      <p class="ap-t">What this does not prove</p>
      <p>Both rates are computed correctly. <b>Neither one is wrong.</b> They answer
        different questions, and only one is the question at your desk.</p>
      <p class="ap-fig">Figure 1 — one stack per reader and per field; the empty row
        is the human operator.</p>
    </div>"""

BEAU = """
  h1{margin:0}
  .legende{display:none}
  .plaque{display:block}
  .plaque img{width:100%;display:block;opacity:1;transition:none;position:static}
  .bas{max-width:none}

  /* ── les chiffres en corps d'affiche ─────────────────────────────────────── */
  .gf{display:flex;gap:clamp(1.3rem,2.6vw,2.6rem);align-items:flex-start}
  .gc{display:flex;flex-direction:column;gap:.3rem}
  .ge{font:600 11px/1.3 var(--sans);letter-spacing:.14em;text-transform:uppercase;
      color:var(--pale)}
  .gv{font:600 clamp(2.5rem,4.1vw,3.7rem)/1 var(--texte);letter-spacing:-.032em;
      font-variation-settings:"opsz" 60;color:var(--encre);
      font-variant-numeric:tabular-nums}
  .gc.cle .gv{color:var(--vert-titre)}
  .gn{font:400 13.5px/1.45 var(--sans);color:var(--demi);margin-top:.15rem}
  .gfl{display:flex;flex-direction:column;align-items:center;gap:.15rem;
       color:var(--pale);padding-top:2.1rem}
  .gfl .gk{font:600 10.5px/1.2 var(--sans);letter-spacing:.12em;
           text-transform:uppercase}
  .gfleche{width:clamp(3.4rem,5.5vw,6rem);height:12px;display:block}
  .mou-b{width:100%;max-width:12rem;height:22px;display:block;margin-top:.2rem}
  .mou-b .ax{stroke:var(--filet-clair);stroke-width:1}
  .mou-b .br{stroke:var(--encre);stroke-width:1.4;fill:none}
  .mou-b .pt{fill:var(--vert-titre)}
  .mou-b .g{font:500 9px/1 var(--mono);fill:var(--pale)}

  /* ── la note de marge ────────────────────────────────────────────────────── */
  .aparte{position:absolute;z-index:4;right:clamp(1.2rem,3.4vw,3.2rem);
          width:min(26%,21rem);
          top:calc(clamp(4.4rem,9vh,7rem) + 0.81 * min(40vw,600px) + 1.4rem)}
  .aparte p,.reserve-g p{margin:0 0 .45rem;
      font:italic 400 14.5px/1.5 var(--texte);color:var(--demi)}
  .aparte b,.reserve-g b{font-style:italic;font-weight:600;color:var(--encre)}
  .ap-t{font:600 10.5px/1.4 var(--sans)!important;font-style:normal!important;
        letter-spacing:.13em;text-transform:uppercase;color:var(--pale)!important;
        margin-bottom:.4rem!important}
  .ap-fig{font:400 11.5px/1.5 var(--sans)!important;font-style:normal!important;
          color:var(--pale)!important;margin:.55rem 0 0!important}
  .reserve-g{max-width:44ch;margin-top:clamp(.6rem,1.8vh,1.2rem)}
  @media (max-height:820px){
    .aparte{position:static;width:min(70%,46ch);margin-top:clamp(.4rem,1.1vh,.7rem)}
    .aparte p,.reserve-g p{font-size:13.5px;margin-bottom:.35rem}
  }

  /* ── la prise, partout ───────────────────────────────────────────────────── */
  .b-lien{all:unset;cursor:pointer;display:block}
  .b-lien:focus-visible{outline:none;
    box-shadow:0 0 0 2px var(--papier-haut),0 0 0 4.5px var(--nuit-b)}
  .lit-b::after{content:"reading";font:600 9.5px/1 var(--sans);letter-spacing:.11em;
                text-transform:uppercase;color:var(--vert-titre);margin-left:.55rem}
"""

SCRIPT = """<script>
document.fonts.ready.then(() => requestAnimationFrame(() =>
  requestAnimationFrame(() => document.body.classList.add("go"))));
</script>"""

# ══ V1 · LA DOUBLE PAGE ══════════════════════════════════════════════════════
V1_CSS = """
  .folios{position:relative;z-index:5;margin-top:auto;display:flex;
          justify-content:space-between;align-items:baseline;
          gap:clamp(.8rem,2vw,2rem)}
  .folios .b-lien{display:flex;gap:.6rem;align-items:baseline;
                  padding:.8rem .2rem .55rem;border-bottom:3px solid transparent;
                  transition:border-color .16s ease}
  .folios .fno{font:600 17px/1 var(--texte);color:var(--pale);
               font-variant-numeric:tabular-nums}
  .folios .fti{font:400 16.5px/1.2 var(--texte);color:var(--demi);
               white-space:nowrap}
  .folios .b-lien:hover{border-bottom-color:var(--filet)}
  .folios .b-lien:hover .fti{color:var(--encre)}
  .folios .b-lien.la{border-bottom-color:var(--vert-titre)}
  .folios .b-lien.la .fno{color:var(--vert-titre)}
  .folios .b-lien.la .fti{color:var(--encre);font-weight:600}
  .pied{border-top:1px solid var(--filet-clair)}
  @media (max-width:1080px){.folios{flex-wrap:wrap;justify-content:flex-start}
    .aparte{position:static;width:auto;margin-top:.8rem}}
"""
V1_HTML = (f'<div class="bas">{CHIFFRES}</div>{APARTE}'
           '<nav class="folios" aria-label="Findings">'
           + "".join(
               f'<a class="b-lien{" la" if e["no"] == "01" else ""}" href="#e{e["no"]}"'
               f'{" aria-current=\"true\"" if e["no"] == "01" else ""}>'
               f'<span class="fno{" lit-b" if e["no"] == "01" else ""}">{e["no"]}</span>'
               f'<span class="fti">{e["onglet"]}</span></a>'
               for e in bp.ECRANS)
           + '</nav>' + bn.PIED)

# ══ V2 · LE PUPITRE ══════════════════════════════════════════════════════════
V2_CSS = """
  .pupitre{position:relative;z-index:5;margin:auto -50vw 0;width:200vw;
           padding:.9rem calc(50vw + 2 * clamp(1.2rem,3.4vw,3.2rem)) 0 50vw;
           background:linear-gradient(163deg,var(--nuit-a) 0%,var(--nuit-b) 74%)}
  .pup-nav{display:grid;grid-template-columns:repeat(5,1fr);
           gap:clamp(.6rem,1.6vw,1.6rem)}
  .pup-nav .b-lien{padding:.55rem .2rem .8rem;border-top:3px solid transparent;
                   transition:border-color .16s ease}
  .pup-nav .no{display:block;font:500 11.5px/1 var(--mono);letter-spacing:.06em;
               color:var(--sur-vert-pale)}
  .pup-nav .ti{display:block;margin:.3rem 0 .2rem;font:400 17px/1.2 var(--texte);
               color:var(--sur-vert)}
  .pup-nav .qu{display:block;font:400 12.5px/1.4 var(--sans);
               color:var(--sur-vert-pale)}
  .pup-nav .b-lien:hover{border-top-color:var(--sur-vert-pale)}
  .pup-nav .b-lien.la{border-top-color:var(--vert-vif)}
  .pup-nav .b-lien.la .no{color:var(--vert-vif)}
  .pup-nav .b-lien.la .ti{font-weight:600}
  .pup-nav .b-lien.la .no::after{content:" reading";font:600 9.5px/1 var(--sans);
    letter-spacing:.11em;text-transform:uppercase;color:var(--vert-vif)}
  .pup-nav .b-lien:focus-visible{box-shadow:0 0 0 2px var(--nuit-b),
    0 0 0 4.5px var(--sur-vert)}
  .pied-nuit{display:flex;gap:.6rem 2rem;align-items:baseline;flex-wrap:wrap;
             margin-top:.5rem;padding:.55rem 0 .7rem;
             border-top:1px solid rgba(228,236,223,.16);
             font:400 12.5px/1.45 var(--sans);color:var(--sur-vert-pale)}
  .pied-nuit b{color:var(--sur-vert);font-weight:600}
  .pied-nuit .annexes{display:flex;gap:clamp(.7rem,1.4vw,1.25rem);flex-wrap:wrap;
                      margin-left:auto}
  .pied-nuit .b-lien{display:inline;padding:.3rem .1rem;color:var(--sur-vert-pale)}
  .pied-nuit .b-lien:hover{color:var(--sur-vert)}
  .pied-nuit .b-lien:focus-visible{box-shadow:0 0 0 2px var(--nuit-b),
    0 0 0 4.5px var(--sur-vert)}
  @media (max-height:820px){
    .pup-nav .qu{display:none}
    .pup-nav .b-lien{padding:.4rem .2rem .55rem}
    .pied-nuit{margin-top:.3rem;padding:.4rem 0 .5rem}
  }
  @media (max-width:1080px){.pup-nav{grid-template-columns:1fr 1fr}
    .aparte{position:static;width:auto;margin:.8rem 0}}
"""
V2_HTML = (f'<div class="bas">{CHIFFRES}</div>{APARTE}'
           '<div class="pupitre"><nav class="pup-nav" aria-label="Findings">'
           + "".join(
               f'<a class="b-lien{" la" if e["no"] == "01" else ""}" href="#e{e["no"]}"'
               f'{" aria-current=\"true\"" if e["no"] == "01" else ""}>'
               f'<span class="no">{e["no"]}</span><span class="ti">{e["onglet"]}</span>'
               f'<span class="qu">{e["question"]}</span></a>' for e in bp.ECRANS)
           + '</nav>'
           '<div class="pied-nuit"><span>On your records, on your machine. '
           '<b>Nothing leaves the network.</b></span>'
           '<nav class="annexes" aria-label="Appendices">'
           + "".join(f'<a class="b-lien" href="#annexe-{i}">{a}</a>'
                     for i, a in enumerate(bn.ANNEXES))
           + '</nav></div></div>')

# ══ V3 · L'ESCALIER ══════════════════════════════════════════════════════════
V3_CSS = """
  .marches{position:relative;z-index:5;margin-top:auto;
           display:grid;grid-template-columns:repeat(5,1fr);
           gap:0 clamp(.9rem,2vw,1.8rem);align-items:start;
           padding-bottom:clamp(2.2rem,4.2vh,3.2rem)}
  .marches .b-lien{border-top:2px solid var(--encre);padding:.5rem .1rem .55rem;
                   transition:border-color .16s ease,transform .2s var(--montee)}
  .marches .b-lien:nth-child(1){transform:translateY(0)}
  .marches .b-lien:nth-child(2){transform:translateY(.9rem)}
  .marches .b-lien:nth-child(3){transform:translateY(1.8rem)}
  .marches .b-lien:nth-child(4){transform:translateY(2.7rem)}
  .marches .b-lien:nth-child(5){transform:translateY(3.6rem)}
  .marches .no{display:block;font:600 19px/1 var(--texte);color:var(--pale);
               font-variant-numeric:tabular-nums}
  .marches .ti{display:block;margin-top:.25rem;font:400 15.5px/1.2 var(--texte);
               color:var(--demi)}
  .marches .b-lien:hover{border-top-color:var(--filet)}
  .marches .b-lien:hover .ti{color:var(--encre)}
  .marches .b-lien.la{border-top-color:var(--vert-titre);border-top-width:3px}
  .marches .b-lien.la .no{color:var(--vert-titre)}
  .marches .b-lien.la .ti{color:var(--encre);font-weight:600}
  @media (max-width:1080px){.marches{grid-template-columns:1fr 1fr;padding-bottom:1rem}
    .marches .b-lien{transform:none!important}}
"""
V3_HTML = (f'<div class="bas">{CHIFFRES}{RESERVE_G}</div>'
           '<nav class="marches" aria-label="Findings">'
           + "".join(
               f'<a class="b-lien{" la" if e["no"] == "01" else ""}" href="#e{e["no"]}"'
               f'{" aria-current=\"true\"" if e["no"] == "01" else ""}>'
               f'<span class="no{" lit-b" if e["no"] == "01" else ""}">{e["no"]}</span>'
               f'<span class="ti">{e["onglet"]}</span></a>' for e in bp.ECRANS)
           + '</nav>' + bn.PIED)

# ══ V4 · LES CHAPITRES ═══════════════════════════════════════════════════════
V4_CSS = """
  .bas{max-width:min(52%,42rem)}
  .chapitres{position:absolute;z-index:5;right:clamp(1.2rem,3.4vw,3.2rem);
             width:min(34%,26rem);
             top:calc(clamp(4.4rem,9vh,7rem) + 0.81 * min(40vw,600px) + .6rem);
             display:flex;flex-direction:column}
  .chapitres .b-lien{display:flex;gap:.9rem;align-items:baseline;
                     justify-content:flex-end;padding:.28rem 0}
  .chapitres .ti{font:400 15.5px/1.2 var(--texte);color:var(--pale);
                 transition:color .16s ease}
  .chapitres .no{font:600 clamp(1.7rem,2.4vw,2.2rem)/1 var(--texte);
                 letter-spacing:-.02em;color:var(--pale);
                 font-variant-numeric:tabular-nums;transition:color .16s ease}
  .chapitres .b-lien:hover .no,.chapitres .b-lien:hover .ti{color:var(--encre)}
  .chapitres .b-lien.la .no{color:var(--vert-titre)}
  .chapitres .b-lien.la .ti{color:var(--encre);font-weight:600}
  @media (max-height:820px){
    .chapitres .b-lien{padding:.14rem 0}
    .chapitres .no{font-size:1.45rem}
  }
  @media (max-width:1080px){.chapitres{position:static;width:auto;margin-top:.8rem}
    .chapitres .b-lien{justify-content:flex-start}
    .bas{max-width:none}}
"""
V4_HTML = (f'<div class="bas">{CHIFFRES}{RESERVE_G}</div>'
           '<nav class="chapitres" aria-label="Findings">'
           + "".join(
               f'<a class="b-lien{" la" if e["no"] == "01" else ""}" href="#e{e["no"]}"'
               f'{" aria-current=\"true\"" if e["no"] == "01" else ""}>'
               f'<span class="ti{" lit-b" if e["no"] == "01" else ""}">{e["onglet"]}</span>'
               f'<span class="no">{e["no"]}</span></a>' for e in bp.ECRANS)
           + '</nav>' + bn.PIED)

# ══ V5 · LA RÈGLE GRADUÉE ════════════════════════════════════════════════════
V5_CSS = """
  .regle{position:relative;z-index:5;margin-top:auto;padding-top:1.1rem}
  /* le trait maître, et ses graduations fines : l'instrument du produit */
  .regle::before{content:"";position:absolute;left:0;right:0;top:1.1rem;height:2px;
                 background:var(--encre)}
  .regle::after{content:"";position:absolute;left:0;right:0;top:calc(1.1rem + 2px);
                height:7px;background:repeating-linear-gradient(90deg,
                var(--filet-clair) 0 1px,transparent 1px 14px)}
  .stations{display:flex;justify-content:space-between;
            gap:clamp(.6rem,1.5vw,1.5rem)}
  .stations .b-lien{position:relative;padding:1.15rem .2rem .5rem;
                    text-align:left;min-width:0}
  .stations .b-lien::before{content:"";position:absolute;left:.1rem;top:-.35rem;
                            width:2px;height:16px;background:var(--pale);
                            transition:background .16s ease}
  .stations .no{display:block;font:600 13px/1 var(--mono);letter-spacing:.05em;
                color:var(--pale)}
  .stations .ti{display:block;margin-top:.25rem;font:400 15.5px/1.2 var(--texte);
                color:var(--demi);white-space:nowrap}
  .stations .b-lien:hover::before{background:var(--encre)}
  .stations .b-lien:hover .ti{color:var(--encre)}
  .stations .b-lien.la::before{width:3px;height:22px;top:-.55rem;
                               background:var(--vert-titre)}
  .stations .b-lien.la .no{color:var(--vert-titre)}
  .stations .b-lien.la .ti{color:var(--encre);font-weight:600}
  .pied{border-top:none}
  @media (max-width:1080px){.stations{flex-wrap:wrap}
    .regle::before,.regle::after{display:none}
    .stations .b-lien::before{display:none}
    .aparte{position:static;width:auto;margin-top:.8rem}}
"""
V5_HTML = (f'<div class="bas">{CHIFFRES}</div>{APARTE}'
           '<div class="regle"><nav class="stations" aria-label="Findings">'
           + "".join(
               f'<a class="b-lien{" la" if e["no"] == "01" else ""}" href="#e{e["no"]}"'
               f'{" aria-current=\"true\"" if e["no"] == "01" else ""}>'
               f'<span class="no{" lit-b" if e["no"] == "01" else ""}">{e["no"]}</span>'
               f'<span class="ti">{e["onglet"]}</span></a>' for e in bp.ECRANS)
           + '</nav></div>' + bn.PIED)

VARIANTES = [
    ("V1", "double-page", V1_CSS, V1_HTML, "Cascade, the spread"),
    ("V2", "pupitre", V2_CSS, V2_HTML, "Cascade, the console"),
    ("V3", "escalier", V3_CSS, V3_HTML, "Cascade, the stair"),
    ("V4", "chapitres", V4_CSS, V4_HTML, "Cascade, the chapters"),
    ("V5", "regle", V5_CSS, V5_HTML, "Cascade, the rule"),
]

for code, nom, css, html, titre in VARIANTES:
    (BASE / f"{code}-{nom}.html").write_text(f"""<!doctype html>
<meta charset="utf-8"><title>{titre}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%2314251e'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<script>document.documentElement.classList.add("js")</script>
<style>{bn.COMMUN}{BEAU}{css}</style>
<div class="ecran">
{HAUT}
  {html}
</div>
{SCRIPT}
""", encoding="utf-8")
    print(f"  {code}-{nom}.html")
