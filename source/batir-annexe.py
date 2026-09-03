#!/usr/bin/env python3
"""L'annexe, version 3 : le chrome du nouveau monde, le corps ouvrable conservé.

CE QUI EST GARDÉ DE LA VERSION 2 (validée par Arslane le 31 août)
  · les titres de sections en liste OUVRABLE (<details> natifs) ;
  · le moyen de vérifier DANS chaque section, en petit terminal actionnable ;
  · l'objet 3D propre à chaque page, dans la tête ;
  · la lecture en deux colonnes au large.

CE QUI CHANGE (harmonisation du 4 septembre, appliquée aux 8 pages)
  · la palette et les fontes sont CELLES du héros (Literata + Roboto Mono) :
    les deux mondes avaient dérivé de quelques teintes ;
  · la manchette tete/tampon/œil disparaît : la barre FIXE des pages
    principales la remplace (marque, nav, sceau ; nuit en haut, parchemin
    posé après 40 px de défilement, exactement comme l'index) ;
  · la bande verte au tiers de page devient la TÊTE de page : nuit dès le
    premier pixel, « Appendix X » en mono vert, le titre à gauche, l'objet
    à droite — le squelette de la page instrument ;
  · le pied devient celui des pages principales (bande nuit, promesse,
    sceau), augmenté du rang des huit annexes.
"""
import importlib.util
import json
import pathlib

BASE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("bn", BASE / "batir-nav.py")
bn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bn)

SCEAU = "1151f5a1cfaae0c0"

# ── les six annexes : une lettre, une source, un objet, une sortie ───────────
# L'ordre suit bn.ANNEXES ; la lettre d'appendice en découle (A-F).
PAGES = [
    {
        "nav": "Method and reproducibility",
        "json": "annexe-methode.json",
        "html": "ANNEXE-METHODE.html",
        "titre_onglet": "Cascade, method and reproducibility",
        "objet": "rendus/etats/objet-methode.webp",
        "alt": "A matte aluminium balance with two pans at exactly the same "
               "height; the right pan is the site's deep green.",
    },
    {
        "nav": "Security and data handling",
        "json": "annexe-securite.json",
        "html": "ANNEXE-SECURITE.html",
        "titre_onglet": "Cascade, security and data handling",
        "objet": "rendus/etats/objet-securite.webp",
        "alt": "A matte aluminium padlock; its shackle, closed, is the same "
               "deep green as the site's accents.",
    },
    {
        "nav": "Questions",
        "json": "annexe-questions.json",
        "html": "ANNEXE-QUESTIONS.html",
        "titre_onglet": "Cascade, questions",
        "objet": "rendus/etats/objet-questions.webp",
        "alt": "A matte aluminium key lying across the frame; its bow is a "
               "fat green ring.",
    },
    {
        "nav": "Terms of engagement",
        "json": "annexe-terms.json",
        "html": "ANNEXE-TERMS.html",
        "titre_onglet": "Cascade, terms of engagement",
        "objet": "rendus/etats/objet-terms.webp",
        "alt": "A thick page with three lines of text, a green signature "
               "stroke, and a pen resting with its tip at the stroke's end.",
    },
    {
        "nav": "Privacy",
        "json": "annexe-privacy.json",
        "html": "ANNEXE-PRIVACY.html",
        "titre_onglet": "Cascade, privacy",
        "objet": "rendus/etats/objet-privacy.webp",
        "alt": "A folder ajar: cream paper showing inside, a green tab on "
               "the cover: nothing leaves it.",
    },
    {
        "nav": "Accessibility",
        "json": "annexe-accessibilite.json",
        "html": "ANNEXE-ACCESSIBILITE.html",
        "titre_onglet": "Cascade, accessibility",
        "objet": "rendus/etats/objet-accessibilite.webp",
        "alt": "A summit with two slopes: a green ramp rising on the left, "
               "grey steps on the right, arriving at the same platform.",
    },
]
LETTRES = "ABCDEF"

# ── la production : adresses publiées et carte de partage ────────────────────
# L'URL de base est le dépôt Pages DÉDIÉ du site (choix du 31/08 : ne pas
# toucher au docs/ généré de cascade-routing) ; si l'hébergement change un
# jour, c'est LA constante à changer : ici, dans batir-hero.py et assembler.py.
BASE_URL = "https://cascade-routing.com/"
PROD = {
    "HERO.html": "index.html",
    "ANNEXE-METHODE.html": "method.html",
    "ANNEXE-SECURITE.html": "security.html",
    "ANNEXE-QUESTIONS.html": "questions.html",
    "ANNEXE-TERMS.html": "terms.html",
    "ANNEXE-PRIVACY.html": "privacy.html",
    "ANNEXE-ACCESSIBILITE.html": "accessibility.html",
    "CONTACT.html": "contact.html",
    "MENTIONS.html": "colophon.html",
    "404.html": "404.html",
}

# le carré diagonal de la marque, en icône d'onglet
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
           "viewBox='0 0 16 16'%3E%3Cpath d='M0 0h16L0 16z' fill='%2314251e'/%3E"
           "%3Cpath d='M16 0v16H0z' fill='%2323543f'/%3E%3C/svg%3E")


def og(titre, description, fichier):
    """La carte de partage : ce que Teams ou un mail interne montre du lien."""
    import html as _h
    d = _h.escape(description, quote=True)
    t = _h.escape(titre, quote=True)
    url = BASE_URL + PROD[fichier]
    return (f'<meta property="og:type" content="website">\n'
            f'<meta property="og:title" content="{t}">\n'
            f'<meta property="og:description" content="{d}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{BASE_URL}og.png">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="description" content="{d}">')


# la barre se pose sur le parchemin après 40 px, comme sur l'index ; et
# l'impression ouvre les sections, puis les referme comme elles étaient
SCRIPT = """<script>
const barre = document.querySelector(".barre");
const poser = () => {
  barre.classList.toggle("posee", scrollY > 40);
  barre.classList.toggle("sur-nuit", scrollY <= 40);
};
addEventListener("scroll", poser, {passive: true}); poser();
addEventListener("beforeprint", () => {
  for (const d of document.querySelectorAll("details")) {
    d.dataset.avant = d.open ? "1" : ""; d.open = true; }});
addEventListener("afterprint", () => {
  for (const d of document.querySelectorAll("details")) {
    d.open = d.dataset.avant === "1"; }});
</script>"""

CSS = """
  :root{--papier:#dbd7c5;--papier-haut:#e2ddcb;--papier-bas:#cdccb9;--encre:#1b1d18;
    --demi:#4a4739;--pale:#55523f;--filet:#9d9a83;--filet-clair:#bab7a0;
    --nuit-a:#1b3229;--nuit-b:#14251e;--nuit-c:#0e1a15;--sur-vert:#e4ecdf;--sur-vert-pale:#a9bdaf;
    --vert-titre:#23543f;--vert-vif:#57b184;--vert-clair:#a5f7cb;
    --texte:"Literata",Georgia,serif;--mono:"Roboto Mono",ui-monospace,Menlo,monospace;
    --sans:ui-sans-serif,-apple-system,"Helvetica Neue",sans-serif;
    --montee:cubic-bezier(.16,.84,.32,1)}
  *{box-sizing:border-box;margin:0}
  html{scroll-behavior:smooth;overflow-x:clip;caret-color:var(--vert-vif);
    scrollbar-color:var(--vert-titre) var(--papier-bas)}
  @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
  body{background:var(--papier);color:var(--encre);font-family:var(--texte);line-height:1.55}
  img{max-width:100%;display:block}
  ::selection{background:var(--vert-titre);color:var(--sur-vert)}
  a{text-underline-offset:4px;color:inherit}
  :focus-visible{outline:3px solid var(--vert-vif);outline-offset:3px;border-radius:2px}
  .colonne{max-width:1180px;margin:0 auto;padding:0 48px}

  /* ── la barre : celle des pages principales, à l'identique ──────────────── */
  .barre{position:fixed;inset:0 0 auto 0;z-index:40;display:flex;align-items:center;gap:28px;
    padding:14px 32px;transition:background .3s,box-shadow .3s}
  .barre.posee{background:color-mix(in srgb,var(--papier-haut) 88%,transparent);
    backdrop-filter:blur(10px);box-shadow:0 1px 0 color-mix(in srgb,var(--filet) 55%,transparent)}
  .barre.sur-nuit .marque{color:var(--sur-vert)}
  .barre.sur-nuit nav a{color:var(--sur-vert-pale)}
  .barre.sur-nuit nav a:hover{color:var(--sur-vert)}
  .barre.sur-nuit .sceau{color:var(--sur-vert-pale)}
  .marque{font-weight:700;font-size:19px;letter-spacing:.01em;text-decoration:none;
    padding:10px 0;color:var(--encre)}
  .barre nav{display:flex;gap:16px;margin-left:auto}
  .barre nav a{font-size:14.5px;text-decoration:none;color:var(--demi);padding:13px 6px}
  .barre nav a:hover{color:var(--encre);text-decoration:underline;
    text-decoration-color:var(--vert-vif);text-decoration-thickness:1.5px}
  .barre nav a[aria-current]{font-weight:600}
  .sceau{font-family:var(--mono);font-size:11px;color:var(--pale);letter-spacing:.04em}
  html:not(.js) .barre{position:absolute}
  html:not(.js) .barre .marque{color:var(--sur-vert)}
  html:not(.js) .barre nav a{color:var(--sur-vert-pale)}
  html:not(.js) .barre .sceau{color:var(--sur-vert-pale)}

  /* ── la tête : nuit dès le premier pixel, titre à gauche, objet à droite ── */
  .tete-nuit{position:relative;padding:132px 0 48px;color:var(--sur-vert);
    background:radial-gradient(120% 100% at 50% -20%,#0f231b,var(--nuit-b) 70%)}
  .tete-nuit .colonne{display:grid;grid-template-columns:minmax(0,1fr) auto;
    gap:18px 40px;align-items:center}
  .ariane{grid-column:1/-1;display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}
  .ariane .fno{font-family:var(--mono);font-size:11.5px;letter-spacing:.15em;
    text-transform:uppercase;color:var(--vert-vif)}
  .ariane .fti{font-family:var(--mono);font-size:11.5px;letter-spacing:.15em;
    text-transform:uppercase;color:var(--sur-vert-pale)}
  .retour{margin-left:auto;font-family:var(--mono);font-size:12px;
    text-decoration:none;color:var(--sur-vert-pale);padding:4px 0}
  .retour:hover{color:var(--sur-vert);text-decoration:underline;
    text-decoration-color:var(--vert-vif)}
  h1{font-size:clamp(32px,4.2vw,56px);font-weight:600;letter-spacing:-.02em;
    line-height:1.06;text-wrap:balance;max-width:21ch}
  h1 .deux{color:var(--vert-vif)}
  .plaque{margin:0;width:min(24vw,300px);height:min(24vh,230px)}
  .plaque img{width:100%;height:100%;object-fit:contain;
    filter:drop-shadow(0 18px 34px rgba(0,0,0,.45))}

  /* ── le document : la liste ouvrable, telle que validée ─────────────────── */
  .doc{padding:38px 0 8px}
  .lede{margin:0 0 26px;font-style:italic;font-size:17px;line-height:1.55;
    color:var(--demi);max-width:88ch}
  details{border-top:1px solid var(--filet-clair)}
  details:last-of-type{border-bottom:1px solid var(--filet-clair)}
  summary{cursor:pointer;list-style:none;display:flex;gap:.8rem;align-items:baseline;
    padding:.95rem .2rem .95rem 0;
    font:500 11.5px/1.4 var(--mono);letter-spacing:.13em;
    text-transform:uppercase;color:var(--pale);
    transition:color .16s ease}
  summary::-webkit-details-marker{display:none}
  summary .cr{font:400 14px/1 var(--sans);color:var(--filet);flex:none;
    transition:transform .2s var(--montee),color .16s ease;width:1em}
  summary:hover{color:var(--encre)}
  summary:hover .cr{color:var(--encre)}
  details[open] summary{color:var(--encre)}
  details[open] summary .cr{transform:rotate(90deg);color:var(--vert-titre)}
  .sec-corps{padding:0 0 1.4rem 1.8rem;max-width:148ch}
  @media (min-width:1100px){
    .sec-corps{columns:2;column-gap:clamp(2.6rem,5vw,5.5rem)}
    .sec-corps p,.sec-corps ul,.sec-corps .ap{break-inside:avoid-column}
    .sec-corps > p:first-child{margin-top:0}
  }
  .sec-corps p{margin:0 0 .8rem;font-size:15.5px;line-height:1.65;color:var(--encre)}
  .sec-corps p:last-child{margin-bottom:0}
  .sec-corps b{font-weight:600}
  .sec-corps .v{color:var(--vert-titre);font-weight:600}
  ul{margin:.2rem 0 .8rem;padding:0;list-style:none;font-size:15.5px;line-height:1.65}
  li{padding-left:1.1rem;position:relative;margin-bottom:.25rem}
  li::before{content:"";position:absolute;left:0;top:.72em;width:6px;height:1.5px;
    background:var(--filet)}
  code{font:400 13.5px/1.5 var(--mono);background:rgba(27,29,24,.055);
    padding:.06rem .3rem}

  /* le moyen de vérifier : les commandes dans un petit écran de terminal :
     actionnables telles quelles : et les références de source EN DESSOUS, parce
     qu'un chemin de fichier ne se tape pas dans un shell. */
  .ap{margin:1rem 0 0;border-left:2px solid var(--vert-titre);padding:.15rem 0 .15rem .9rem}
  .ap-t{font:500 10px/1.4 var(--mono);letter-spacing:.14em;text-transform:uppercase;
    color:var(--vert-titre);display:block;margin-bottom:.3rem}
  .ap p{margin:0 0 .5rem;font:italic 400 13.5px/1.5 var(--texte);
    color:var(--demi)!important;font-size:13.5px!important}
  .term{max-width:44ch;background:linear-gradient(163deg,var(--nuit-a),var(--nuit-b));
    border:1px solid color-mix(in srgb,var(--vert-vif) 22%,transparent);
    border-radius:8px;overflow:hidden;box-shadow:0 6px 18px rgba(20,37,30,.22)}
  .term-bar{display:flex;gap:.32rem;align-items:center;padding:.42rem .6rem;
    background:rgba(0,0,0,.28)}
  .term-bar i{width:7px;height:7px;border-radius:50%;background:var(--sur-vert-pale);opacity:.45}
  .term-bar span{margin-left:auto;font:500 9px/1 var(--mono);letter-spacing:.14em;
    text-transform:uppercase;color:var(--sur-vert-pale)}
  .term-corps{padding:.65rem .8rem .75rem;font:400 12.5px/1.75 var(--mono);
    color:var(--sur-vert)}
  .term-corps .cmd{display:block;white-space:pre-wrap;overflow-wrap:break-word;
    background:none;padding:0}
  /* l'invite est un ::before : elle ne part pas dans le presse-papier */
  .term-corps .cmd::before{content:"$ ";color:var(--vert-vif);font-weight:600}
  .term-corps .sortie{display:block;color:var(--sur-vert-pale);opacity:.9}
  .term-corps .sortie::before{content:"# "}
  .ap p.refs{margin:.5rem 0 0;font:400 11.5px/1.5 var(--mono)!important;
    font-style:normal!important;color:var(--pale)!important}
  .refs b{font:600 9.5px/1.5 var(--mono);letter-spacing:.13em;
    text-transform:uppercase;color:var(--pale);margin-right:.5rem}

  /* ── la plomberie : colonne de lecture simple, filets fins, pas d'objet ──── */
  .pl-doc{max-width:78ch;padding:38px 0 8px}
  .pl-doc .lede{max-width:none}
  .pl-sec{border-top:1px solid var(--filet-clair);padding:1rem 0 1.3rem}
  .pl-sec:last-of-type{border-bottom:1px solid var(--filet-clair)}
  .pl-sec h2{margin:0 0 .55rem;font:500 11.5px/1.4 var(--mono);
    letter-spacing:.13em;text-transform:uppercase;color:var(--pale)}
  .pl-sec p{margin:0 0 .8rem;font-size:15.5px;line-height:1.65;color:var(--encre)}
  .pl-sec p:last-child{margin-bottom:0}
  .pl-sec b{font-weight:600}

  /* ── le pied : celui des pages principales, plus le rang des annexes ────── */
  .pied{background:var(--nuit-c);color:var(--sur-vert);padding:44px 0;margin-top:56px}
  .pied .colonne{display:flex;flex-direction:column;gap:18px}
  .pied-h{display:flex;justify-content:space-between;gap:12px 24px;flex-wrap:wrap;
    align-items:baseline}
  .pied-p{font-size:clamp(17px,1.8vw,23px);font-weight:600}
  .pied-p em{font-style:italic;color:var(--vert-clair)}
  .pied .sceau{color:var(--sur-vert-pale)}
  .annexes{display:flex;gap:4px 18px;flex-wrap:wrap;
    border-top:1px solid color-mix(in srgb,var(--sur-vert-pale) 22%,transparent);
    padding-top:16px}
  .annexes a{font-size:13.5px;text-decoration:none;color:var(--sur-vert-pale);
    padding:6px 2px}
  .annexes a:hover{color:var(--sur-vert);text-decoration:underline;
    text-decoration-color:var(--vert-vif)}
  .annexes a[aria-current="true"]{color:var(--sur-vert);font-weight:600;
    box-shadow:0 1.5px 0 var(--vert-vif)}

  @media (prefers-reduced-motion:reduce){
    summary .cr,summary,.barre{transition:none}
  }
  /* ── 641-1080 : la fenêtre de bureau NON MAXIMISÉE ─────────────────────────
     On MAINTIENT la composition du large : l'objet reste à droite du titre,
     plus petit (constat d'Arslane, 31/08 : la mise en page téléphone agrandie
     donnait un objet géant dans une bande gonflée). */
  @media (max-width:1080px){
    .barre{padding:12px 18px;gap:14px}
    .barre nav{display:none}
    .tete-nuit{padding-top:104px}
    .colonne{padding:0 26px}
  }
  @media (min-width:641px) and (max-width:1080px){
    .plaque{width:min(28vw,260px);height:min(22vh,200px)}
  }
  @media (max-width:640px){
    .tete-nuit .colonne{display:block}
    .plaque{width:min(62vw,300px);height:min(26vh,190px);margin:20px auto 0}
    h1{max-width:none}
    .retour{margin-left:0}
    .sec-corps{padding-left:.2rem}
    .colonne{padding:0 22px}
  }

  /* ── l'impression : le mémo qu'un comité fait circuler ───────────────────── */
  @media print{
    body{background:#fff;color:#1b1d18}
    .barre,.plaque,.retour,.annexes{display:none}
    .tete-nuit{background:none;color:#1b1d18;padding:12px 0 4px}
    h1{color:#1b1d18;max-width:none;font-size:26pt}
    h1 .deux{color:#23543f}
    .ariane .fno{color:#23543f}
    .ariane .fti{color:#55523f}
    .pied{background:none;color:#1b1d18;margin-top:20px;padding:10px 0;
      border-top:1px solid #999}
    .pied-p em{color:#23543f}
    .pied .sceau{color:#55523f}
    .sec-corps{columns:1;max-width:none}
    details,.pl-sec{break-inside:avoid}
    .term{box-shadow:none}
    summary .cr{display:none}
  }
"""

# la nav du haut : celle des pages principales, avec la page courante marquée
def barre_html(courante):
    liens = [("INSTRUMENT.html", "Instrument"), ("ENGAGEMENT.html", "Engagement"),
             ("ANNEXE-METHODE.html", "Method"), ("ANNEXE-SECURITE.html", "Security"),
             ("ANNEXE-QUESTIONS.html", "Questions"), ("CONTACT.html", "Contact")]
    nav = "".join(
        f'<a href="{h}"' + (' aria-current="page"' if h == courante else "")
        + f'>{n}</a>' for h, n in liens)
    return (f'<header class="barre sur-nuit">\n'
            f'  <a class="marque" href="HERO.html">CASCADE</a>\n'
            f'  <nav aria-label="Site">{nav}</nav>\n'
            f'  <span class="sceau">seal {SCEAU} &#183; measured, then frozen</span>\n'
            f'</header>')


def pied_html(courante):
    """Le pied commun : la promesse, le sceau, puis le rang des annexes."""
    liens = [(p["html"], p["nav"]) for p in PAGES]
    liens += [("CONTACT.html", "Contact"), ("MENTIONS.html", "Colophon")]
    rang = "".join(
        f'<a href="{h}"' + (' aria-current="true"' if h == courante else "")
        + f'>{n}</a>' for h, n in liens)
    return (f'<footer class="pied"><div class="colonne">\n'
            f'  <div class="pied-h">\n'
            f'    <p class="pied-p">On your records, on your machine. '
            f'<em>Nothing leaves the network.</em></p>\n'
            f'    <span class="sceau">seal {SCEAU} &#183; measured, then frozen</span>\n'
            f'  </div>\n'
            f'  <nav class="annexes" aria-label="Appendices">{rang}</nav>\n'
            f'</div></footer>')


def section(sec, ouvert=False):
    corps = "".join(sec["html"])
    ap = ""
    if sec.get("verif"):
        v = sec["verif"]
        lignes = "".join(
            f'<code class="cmd">{c["c"]}</code>'
            + (f'<span class="sortie">{c["n"]}</span>' if c.get("n") else "")
            for c in v.get("cmd", []))
        refs = (f'<p class="refs"><b>Where it lives</b>{v["refs"]}</p>'
                if v.get("refs") else "")
        ap = (f'<div class="ap"><span class="ap-t">{v["t"]}</span>'
              f'<p>{v["p"]}</p>'
              f'<div class="term"><div class="term-bar">'
              f'<i></i><i></i><i></i><span>run it yourself</span></div>'
              f'<div class="term-corps">{lignes}</div></div>{refs}</div>')
    return (f'<details{" open" if ouvert else ""}>'
            f'<summary><span class="cr" aria-hidden="true">&#9656;</span>{sec["h2"]}'
            f'</summary><div class="sec-corps">{corps}{ap}</div></details>')


TETE_COMMUNE = ('<meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">')


def _texte(fragment):
    """Le texte nu d'un fragment : balises retirées, entités résolues."""
    import html as _h
    import re as _re
    return " ".join(_h.unescape(_re.sub(r"<[^>]+>", "", fragment)).split())


def faq_ld(sections):
    """La FAQ lisible par les moteurs, générée des MÊMES sections que la page :
    une seule source, donc pas de dérive possible entre ce que lit un visiteur
    et ce que lit un moteur (assembler.py compare quand même, question par
    question). Les réponses sont le texte des paragraphes, sans le bloc de
    vérification (une commande shell n'est pas une réponse) ; les guillemets
    typographiques des titres restent dans la page, pas dans la question nue."""
    import json as _json
    entrees = []
    for sec in sections:
        q = _texte(sec["h2"]).strip("“” ")
        r = " ".join(_texte(p) for p in sec["html"])
        entrees.append({"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": r}})
    bloc = _json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                        "mainEntity": entrees}, ensure_ascii=True)
    return f'\n<script type="application/ld+json">{bloc}</script>'

for lettre, page in zip(LETTRES, PAGES):
    faits = json.loads((BASE / page["json"]).read_text())
    sections = "".join(section(x, i == 0) for i, x in enumerate(faits["sections"]))
    donnees = faq_ld(faits["sections"]) if page["html"] == "ANNEXE-QUESTIONS.html" else ""

    (BASE / page["html"]).write_text(f"""<!doctype html><html lang="en">
<meta charset="utf-8"><title>{page["titre_onglet"]}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
{og(page["titre_onglet"], faits["lede"], page["html"])}
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="fontes/literata.css">
<link rel="stylesheet" href="fontes/roboto-mono.css">{donnees}
<script>document.documentElement.classList.add("js")</script>
<style>{CSS}</style>
{barre_html(page["html"])}

<main>
<section class="tete-nuit"><div class="colonne">
  <div class="ariane">
    <span class="fno">Appendix {lettre}</span>
    <span class="fti">{page["nav"]}</span>
    <a class="retour" href="HERO.html">&#8592; Back to the findings</a>
  </div>
  <h1>{faits["titre"]}</h1>
  <figure class="plaque"><img src="{page["objet"]}" alt="{page["alt"]}"></figure>
</div></section>

<div class="colonne"><div class="doc">
  <p class="lede">{faits["lede"]}</p>
  {sections}
</div></div>
</main>

{pied_html(page["html"])}
""" + SCRIPT + "\n", encoding="utf-8")
    print(f"  {page['html']}")

# ── la plomberie : contact et colophon : colonne simple, sans objet ──────────
PLOMBERIE = json.loads((BASE / "plomberie.json").read_text())
for page in PLOMBERIE["pages"]:
    sections = "".join(
        f'<div class="pl-sec"><h2>{s["h2"]}</h2>{"".join(s["html"])}</div>'
        for s in page["sections"])

    (BASE / page["html"]).write_text(f"""<!doctype html><html lang="en">
<meta charset="utf-8"><title>{page["titre_onglet"]}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
{og(page["titre_onglet"], page["lede"], page["html"])}
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="fontes/literata.css">
<link rel="stylesheet" href="fontes/roboto-mono.css">
<script>document.documentElement.classList.add("js")</script>
<style>{CSS}</style>
{barre_html(page["html"])}

<main>
<section class="tete-nuit"><div class="colonne">
  <div class="ariane">
    <span class="fno">{page["fno"]}</span>
    <a class="retour" href="HERO.html">&#8592; Back to the findings</a>
  </div>
  <h1>{page["titre"]}</h1>
</div></section>

<div class="colonne"><div class="pl-doc">
  <p class="lede">{page["lede"]}</p>
  {sections}
</div></div>
</main>

{pied_html(page["html"])}
""" + SCRIPT + "\n", encoding="utf-8")
    print(f"  {page['html']}")
