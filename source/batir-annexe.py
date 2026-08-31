#!/usr/bin/env python3
"""L'annexe, version 2 : le haut du héros, les sections en liste ouvrable.

CE QU'ARSLANE A DEMANDÉ LE 31 AOÛT (à valider sur UNE page : Sécurité)
  · le titre sur une bande verte, comme l'écran héros ;
  · un design 3D propre à la page, en rapport avec elle — ici la forme ANNEAUX :
    des boucles fermées ; chaque appel réseau de l'outil revient à sa machine, et
    c'est précisément ce que cette page prouve. Le vocabulaire des couleurs ne
    bouge pas : aucun « retenu » sur une annexe, rien n'y est mis en avant ;
  · les titres de sections en liste OUVRABLE, les paragraphes dessous — des
    <details> natifs : l'adresse et le clavier marchent sans script ;
  · la configuration minimum pour faire tourner l'outil, là où c'est logique —
    ici : la même équipe demande « qu'est-ce qui sort » et « que faut-il pour
    que ça tourne ». Uniquement du vérifié.

Le moyen de vérifier vit maintenant DANS chaque section ouverte, en fin de
propos, puisque la marge ne peut plus s'aligner sur des sections repliées.
"""
import importlib.util
import json
import pathlib

BASE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("bn", BASE / "batir-nav.py")
bn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bn)

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
               "the cover — nothing leaves it.",
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
# jour, c'est LA constante à changer — ici, dans batir-hero.py et assembler.py.
BASE_URL = "https://arslanesempai-ui.github.io/cascade-site/"
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


SCRIPT_IMPRESSION = """<script>
/* l'impression ouvre les sections, puis les referme comme elles étaient */
addEventListener("beforeprint", () => {
  for (const d of document.querySelectorAll("details")) {
    d.dataset.avant = d.open ? "1" : ""; d.open = true; }});
addEventListener("afterprint", () => {
  for (const d of document.querySelectorAll("details")) {
    d.open = d.dataset.avant === "1"; }});
</script>"""

CSS = """
  *{box-sizing:border-box}
  :root{
    --papier:#d8d1b6;--papier-haut:#e3dcc2;--papier-bas:#cbc4aa;
    --encre:#1b1d18;--demi:#4a4739;--pale:#4f4c3a;--filet:#9d9a83;
    --filet-clair:#b3ac91;--vert-titre:#23543f;--vert-vif:#57b184;
    --nuit-a:#1b3229;--nuit-b:#14251e;--nuit-c:#122019;
    --sur-vert:#e4ecdf;--sur-vert-pale:#a9bdaf;
    --sans:ui-sans-serif,-apple-system,"Helvetica Neue",sans-serif;
    --mono:ui-monospace,"SF Mono",Menlo,monospace;
    --texte:"Literata",Georgia,serif;
    --montee:cubic-bezier(.16,.84,.32,1)}
  html{background:var(--papier);overflow-x:clip}
  body{margin:0;color:var(--encre);font:400 16px/1.6 var(--texte);
       -webkit-font-smoothing:antialiased;overflow-x:hidden;
       background:linear-gradient(168deg,var(--papier-haut) 0%,var(--papier) 54%,
                  var(--papier-bas) 100%)}
  .page{max-width:104rem;margin:0 auto;position:relative;
        padding:clamp(.8rem,1.6vh,1.25rem) clamp(1.2rem,3.4vw,3.2rem) 2.2rem}

  /* ── la manchette du héros, à l'identique ─────────────────────────────────── */
  .tete{display:flex;gap:1rem;align-items:baseline;flex-wrap:wrap}
  .marque{display:inline-flex;gap:.55rem;align-items:center}
  .marque a{all:unset;cursor:pointer;display:inline-flex;gap:.55rem;
            align-items:center;padding:.25rem .3rem;margin:-.25rem -.3rem}
  .marque a:focus-visible{outline:none;
    box-shadow:0 0 0 2px var(--papier-haut),0 0 0 4.5px var(--nuit-b)}
  .carre{width:12px;height:12px;flex:none;
         background:linear-gradient(135deg,var(--nuit-a) 0 62%,var(--vert-titre) 62%)}
  .marque b{font:700 14px/1 var(--sans);letter-spacing:.26em;color:var(--encre)}
  .sep-v{width:1px;align-self:stretch;background:var(--filet-clair);margin:.15rem 0}
  .desc{font:italic 400 15px/1.3 var(--texte);color:var(--demi)}
  .tampon{margin-left:auto;border:1px solid var(--filet);padding:.34rem .7rem;
          font:500 10px/1.4 var(--mono);letter-spacing:.14em;text-transform:uppercase;
          color:var(--pale)}
  .oeil{display:flex;align-items:center;gap:.9rem;margin-top:clamp(.6rem,2vh,1.5rem)}
  .oeil .fno{font:600 11px/1.4 var(--sans);letter-spacing:.14em;
             text-transform:uppercase;color:var(--vert-titre)}
  .oeil .fti{font:600 11px/1.4 var(--sans);letter-spacing:.15em;
             text-transform:uppercase;color:var(--pale)}
  .oeil::after{content:"";flex:1;height:1px;background:var(--filet-clair)}
  .retour{all:unset;cursor:pointer;font:400 13px/1.4 var(--sans);color:var(--pale);
          padding:.3rem .4rem;margin:-.3rem -.4rem}
  .retour:hover{color:var(--encre)}
  .retour:focus-visible{outline:none;
    box-shadow:0 0 0 2px var(--papier-haut),0 0 0 4.5px var(--nuit-b)}

  /* ── la bande verte du héros, le titre à l'encre centrée ─────────────────── */
  .haut{position:relative;z-index:1;margin:clamp(.8rem,2vh,1.4rem) -50vw 0;width:200vw;
        padding:clamp(1.1rem,2.6vh,2rem) 50vw;
        display:flex;flex-direction:column;justify-content:center;
        background:linear-gradient(163deg,var(--nuit-a) 0%,var(--nuit-b) 54%,
                   var(--nuit-c) 100%)}
  h1{margin:-0.155em 0 0.155em;position:relative;z-index:3;
     max-width:min(48vw,760px);letter-spacing:-.026em;
     font:600 min(clamp(1.9rem,5.2vw,4.2rem),7.2vh)/1.06 var(--texte);
     font-variation-settings:"opsz" 72;color:var(--sur-vert)}
  h1 .deux{color:var(--vert-vif)}

  /* ── l'objet de la page : DANS la bande, centré sur elle ─────────────────── */
  /* Une seule règle pour les six pages (demande d'Arslane, 31 août) : la même
     boîte pour tous — l'image s'y loge en gardant ses proportions, un portrait
     ne sort plus géant — et le centre de l'objet est le centre de la bande,
     le débord est le même en haut et en bas. */
  /* la bande déborde de 50vw de chaque côté : le right se compte depuis là */
  .plaque{position:absolute;right:calc(50vw + clamp(3rem,9vw,10rem));top:50%;
          transform:translateY(-50%);margin:0;z-index:2;
          width:min(26vw,420px);height:min(30vh,320px)}
  .plaque img{width:100%;height:100%;object-fit:contain;display:block}
  .socle-ombre{display:none}
  .fig-objet{position:absolute;z-index:4;right:clamp(4rem,11vw,12rem);
             width:min(24%,19rem);
             top:calc(clamp(3.6rem,7vh,6rem) + 1.203 * min(20vw,290px) + 1rem);
             border-top:1px solid var(--filet-clair);padding-top:.45rem}
  .fig-objet p{margin:0;font:400 12px/1.5 var(--sans);color:var(--pale)}
  .fig-objet .no{font:600 10px/1.4 var(--sans);letter-spacing:.14em;
                 text-transform:uppercase;color:var(--demi);margin-right:.45rem}

  /* ── le document : la liste ouvrable ──────────────────────────────────────── */
  .doc{max-width:none;margin-top:clamp(1.4rem,3.4vh,2.6rem)}
  /* l'objet ne descend plus sous la bande : le chapeau court jusqu'à droite */
  .lede{margin:0 0 1.6rem;font:italic 400 16.5px/1.55 var(--texte);color:var(--demi)}
  details{border-top:1px solid var(--filet-clair)}
  details:last-of-type{border-bottom:1px solid var(--filet-clair)}
  summary{cursor:pointer;list-style:none;display:flex;gap:.8rem;align-items:baseline;
          padding:.95rem .2rem .95rem 0;
          font:600 11.5px/1.4 var(--sans);letter-spacing:.14em;
          text-transform:uppercase;color:var(--pale);
          transition:color .16s ease}
  summary::-webkit-details-marker{display:none}
  summary .cr{font:400 14px/1 var(--sans);color:var(--filet);flex:none;
              transition:transform .2s var(--montee),color .16s ease;width:1em}
  summary:hover{color:var(--encre)}
  summary:hover .cr{color:var(--encre)}
  summary:focus-visible{outline:none;
    box-shadow:0 0 0 2px var(--papier-haut),0 0 0 4.5px var(--nuit-b)}
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

  /* le moyen de vérifier : les commandes dans un petit écran de terminal —
     actionnables telles quelles — et les références de source EN DESSOUS, parce
     qu'un chemin de fichier ne se tape pas dans un shell. */
  .ap{margin:1rem 0 0;border-left:2px solid var(--vert-titre);padding:.15rem 0 .15rem .9rem}
  .ap-t{font:600 10px/1.4 var(--sans);letter-spacing:.14em;text-transform:uppercase;
        color:var(--vert-titre);display:block;margin-bottom:.3rem}
  .ap p{margin:0 0 .5rem;font:italic 400 13.5px/1.5 var(--texte);
        color:var(--demi)!important;font-size:13.5px!important}
  .term{max-width:44ch;background:linear-gradient(163deg,var(--nuit-a),var(--nuit-b));
        box-shadow:0 6px 18px rgba(20,37,30,.22)}
  .term-bar{display:flex;gap:.32rem;align-items:center;padding:.42rem .6rem;
            background:rgba(0,0,0,.28)}
  .term-bar i{width:7px;height:7px;background:var(--sur-vert-pale);opacity:.45}
  .term-bar span{margin-left:auto;font:600 9px/1 var(--sans);letter-spacing:.14em;
                 text-transform:uppercase;color:var(--sur-vert-pale)}
  .term-corps{padding:.65rem .8rem .75rem;font:400 12.5px/1.75 var(--mono);
              color:var(--sur-vert)}
  .term-corps .cmd{display:block;white-space:pre-wrap;overflow-wrap:break-word}
  /* l'invite est un ::before : elle ne part pas dans le presse-papier */
  .term-corps .cmd::before{content:"$ ";color:var(--vert-vif);font-weight:600}
  .term-corps .sortie{display:block;color:var(--sur-vert-pale);opacity:.9}
  .term-corps .sortie::before{content:"# "}
  .ap p.refs{margin:.5rem 0 0;font:400 11.5px/1.5 var(--mono)!important;
             font-style:normal!important;color:var(--pale)!important}
  .refs b{font:600 9.5px/1.5 var(--sans);letter-spacing:.13em;
          text-transform:uppercase;color:var(--pale);margin-right:.5rem}

  /* ── la plomberie : colonne de lecture simple, filets fins, pas d'objet ──── */
  .pl-doc{max-width:78ch;margin-top:clamp(1.4rem,3.4vh,2.6rem)}
  .pl-doc .lede{max-width:none}
  .pl-sec{border-top:1px solid var(--filet-clair);padding:1rem 0 1.3rem}
  .pl-sec:last-of-type{border-bottom:1px solid var(--filet-clair)}
  .pl-sec h2{margin:0 0 .55rem;font:600 11.5px/1.4 var(--sans);
             letter-spacing:.14em;text-transform:uppercase;color:var(--pale)}
  .pl-sec p{margin:0 0 .8rem;font-size:15.5px;line-height:1.65;color:var(--encre)}
  .pl-sec p:last-child{margin-bottom:0}
  .pl-sec b{font-weight:600}

  .pied{display:flex;gap:.6rem 2rem;align-items:baseline;flex-wrap:wrap;
        margin-top:2.2rem;border-top:1px solid var(--filet-clair);
        padding-top:.7rem;font:400 13px/1.5 var(--sans);color:var(--pale)}
  .pied b{color:var(--encre);font-weight:600}
  .annexes{display:flex;gap:clamp(.7rem,1.4vw,1.25rem);flex-wrap:wrap;margin-left:auto}
  .annexes a{all:unset;cursor:pointer;padding:.35rem .2rem;margin:-.35rem -.2rem;
             color:var(--pale)}
  .annexes a:hover{color:var(--encre)}
  .annexes a[aria-current="true"]{color:var(--encre);font-weight:600;
    box-shadow:0 1.5px 0 var(--vert-titre)}
  .annexes a:focus-visible{outline:none;
    box-shadow:0 0 0 2px var(--papier-haut),0 0 0 4.5px var(--nuit-b)}

  @media (prefers-reduced-motion:reduce){
    summary .cr,summary,.retour,.annexes a{transition:none}
  }
  @media (max-width:1080px){
    /* la bande donne 100vw au titre : on lui rend la marge droite de la page,
       sinon le clip de la racine mange la fin des lignes (mesuré à 375) */
    .haut{padding-right:calc(50vw + clamp(1.2rem,3.4vw,3.2rem))}
    .plaque{position:static;transform:none;width:min(70vw,340px);height:auto;
            margin:1rem auto 0}
    .plaque img{height:auto}
    .oeil .fno{white-space:nowrap}
    .socle-ombre,.fig-objet{display:none}
    h1{max-width:none}
    .sec-corps{padding-left:.2rem}
  }

  /* ── l'impression : le mémo qu'un comité fait circuler ───────────────────── */
  @media print{
    body{background:#fff}
    .haut{background:none;margin:.4rem 0 0;width:auto;padding:.4rem 0}
    h1{color:#1b1d18;max-width:none;font-size:26pt}
    h1 .deux{color:#23543f}
    .plaque,.retour,.annexes,.oeil::after{display:none}
    .pied{border-top:1px solid #999}
    .sec-corps{columns:1;max-width:none}
    details,.pl-sec{break-inside:avoid}
    .term{box-shadow:none}
    summary .cr{display:none}
  }
"""


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


def nav_annexes(courante):
    """Le pied commun : les six annexes, puis le contact et le colophon."""
    liens = [(p["html"], p["nav"]) for p in PAGES]
    liens += [("CONTACT.html", "Contact"), ("MENTIONS.html", "Colophon")]
    return "".join(
        f'<a href="{h}"' + (' aria-current="true"' if h == courante else "")
        + f'>{n}</a>' for h, n in liens)


for lettre, page in zip(LETTRES, PAGES):
    faits = json.loads((BASE / page["json"]).read_text())
    nav = nav_annexes(page["html"])
    sections = "".join(section(x, i == 0) for i, x in enumerate(faits["sections"]))

    (BASE / page["html"]).write_text(f"""<!doctype html><html lang="en">
<meta charset="utf-8"><title>{page["titre_onglet"]}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
{og(page["titre_onglet"], faits["lede"], page["html"])}
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="fontes/literata.css">
<style>{CSS}</style>
<div class="page">
  <div class="tete">
    <span class="marque"><a href="HERO.html">
      <i class="carre" aria-hidden="true"></i><b>CASCADE</b></a></span>
    <span class="sep-v" aria-hidden="true"></span>
    <span class="desc">Routing audit, KYC extraction</span>
    <span class="tampon">Seal 1151f5a1cfaae0c0 &#183; measured, then frozen</span></div>
  <div class="oeil"><span class="fno">Appendix {lettre}</span>
    <span class="fti">{page["nav"]}</span>
    <a class="retour" href="HERO.html">&#8592; Back to the findings</a></div>

  <div class="haut"><h1>{faits["titre"]}</h1>
    <figure class="plaque"><img src="{page["objet"]}"
      alt="{page["alt"]}"></figure></div>
  <span class="socle-ombre"></span>

  <div class="doc">
    <p class="lede">{faits["lede"]}</p>
    {sections}
  </div>

  <div class="pied">
    <span>On your records, on your machine. <b>Nothing leaves the network.</b></span>
    <nav class="annexes" aria-label="Appendices">{nav}</nav>
  </div>
</div>
""" + SCRIPT_IMPRESSION + "\n", encoding="utf-8")
    print(f"  {page['html']}")

# ── la plomberie : contact, 404, colophon — colonne simple, sans objet ───────
PLOMBERIE = json.loads((BASE / "plomberie.json").read_text())
for page in PLOMBERIE["pages"]:
    nav = nav_annexes(page["html"])
    sections = "".join(
        f'<div class="pl-sec"><h2>{s["h2"]}</h2>{"".join(s["html"])}</div>'
        for s in page["sections"])

    (BASE / page["html"]).write_text(f"""<!doctype html><html lang="en">
<meta charset="utf-8"><title>{page["titre_onglet"]}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
{og(page["titre_onglet"], page["lede"], page["html"])}
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="fontes/literata.css">
<style>{CSS}</style>
<div class="page">
  <div class="tete">
    <span class="marque"><a href="HERO.html">
      <i class="carre" aria-hidden="true"></i><b>CASCADE</b></a></span>
    <span class="sep-v" aria-hidden="true"></span>
    <span class="desc">Routing audit, KYC extraction</span>
    <span class="tampon">Seal 1151f5a1cfaae0c0 &#183; measured, then frozen</span></div>
  <div class="oeil"><span class="fno">{page["fno"]}</span>
    <a class="retour" href="HERO.html">&#8592; Back to the findings</a></div>

  <div class="haut"><h1>{page["titre"]}</h1></div>

  <div class="pl-doc">
    <p class="lede">{page["lede"]}</p>
    {sections}
  </div>

  <div class="pied">
    <span>On your records, on your machine. <b>Nothing leaves the network.</b></span>
    <nav class="annexes" aria-label="Appendices">{nav}</nav>
  </div>
</div>
""", encoding="utf-8")
    print(f"  {page['html']}")
