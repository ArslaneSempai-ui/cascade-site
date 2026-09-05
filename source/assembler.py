#!/usr/bin/env python3
"""Assemble le site : bâtit les pages, puis remplit docs/ et source/.

Lancé depuis source/, il se reconnaît et ne recopie pas la chaîne sur
elle-même. Ce qu'il produit :
  docs/    le site bâti, noms de production (index.html, security.html…),
           prêt pour n'importe quel hébergement statique ;
  source/  toute la chaîne de fabrication — bâtisseurs, contenus JSON, relevé,
           scripts Blender — pour que le site reste re-bâtissable.

Le branchement sur la publication N'EST PAS fait ici : docs/ du dépôt
cascade-routing est GÉNÉRÉ par `npm run pages` et gardé par des tests
d'empreintes (.sources.json) — y verser ce site est une opération dans ce
dépôt-là, à décider séparément.

Contrôle de liens avec témoin positif : avant de croire « zéro lien cassé »,
le contrôle doit attraper un lien cassé planté exprès.
"""
import pathlib
import re
import shutil
import sys

MAQ = pathlib.Path(__file__).parent
SITE = pathlib.Path.home() / "Documents" / "cascade-site"
DOCS = SITE / "docs"
BASE_URL = "https://cascade-routing.com/"
# Le chemin sous lequel le site est servi se déduit de l'URL : « /cascade-site/ »
# aujourd'hui, « / » le jour du domaine propre. Trois usages en dépendent (la
# base de la 404, l'icône tactile, le contrôle de liens) — ils lisent tous ICI.
from urllib.parse import urlparse
PREFIXE = urlparse(BASE_URL).path

# Le sous-dossier de l'outil rouge : ces pages s'émettent QUAND leurs sources
# existent (les lots S2/S3 les écrivent) ; absentes, l'assembleur le DIT et
# continue : le vert ne dépend pas du rouge. Présentes, toutes les gardes
# s'appliquent, plus une : un commentaire « placeholder » refuse la production.
PROD_SCREENING = {
    "HERO-SCREENING.html": "screening/index.html",
    "INSTRUMENT-SCREENING.html": "screening/instrument.html",
    "ANNEXE-SCREENING-METHODE.html": "screening/method.html",
    "ANNEXE-SCREENING-SECURITE.html": "screening/security.html",
}

PROD = {
    "HERO.html": "index.html",
    "INSTRUMENT.html": "instrument.html",
    "ENGAGEMENT.html": "engagement.html",
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

# ── bâtir d'abord : les pages naissent à côté de ce script ───────────────────
# L'audit du 31/08 a montré l'inverse en danger : un rmtree AVANT de vérifier
# ses entrées détruisait docs/ puis plantait, puisque source/ ne portait pas
# les pages bâties. Ordre tenu : bâtir, vérifier, seulement ensuite effacer.
import subprocess
for batisseur in ("batir-hero.py", "batir-instrument.py", "batir-instrument-screening.py",
                  "batir-offre.py", "batir-annexe.py", "batir-404.py"):
    subprocess.run([sys.executable, str(MAQ / batisseur)], check=True,
                   cwd=str(MAQ), capture_output=True)
manquants = [v for v in PROD if not (MAQ / v).exists()]
if manquants:
    sys.exit(f"pages absentes après bâtisse : {manquants} — rien n'est effacé")
if not (MAQ / "og.png").exists():
    sys.exit("og.png absent — le régénérer depuis og-card.html (capture 1200x630)")

# ── docs/ : les pages, renommées, liens réécrits ─────────────────────────────
if DOCS.exists():
    shutil.rmtree(DOCS)
DOCS.mkdir(parents=True)

def csp(t):
    """La politique de sécurité de contenu, par empreintes : seuls NOS styles
    et NOS scripts, hachés sur leur contenu final, ont le droit de tourner.
    Tout le reste — connexions, cadres, formulaires, scripts étrangers — est
    refusé. GitHub Pages ne pose pas d'en-têtes ; la balise meta porte tout ce
    qu'une meta peut porter (frame-ancestors, lui, exige un en-tête)."""
    import base64
    import hashlib

    def h(s):
        e = base64.b64encode(hashlib.sha256(s.encode()).digest()).decode()
        return f"'sha256-{e}'"

    styles = re.findall(r"<style>(.*?)</style>", t, re.S)
    scripts = re.findall(r"<script>(.*?)</script>", t, re.S)
    style_src = "'self' " + " ".join(h(s) for s in styles)
    # les attributs style="…" (les drapeaux de l'instrument du héros) ne sont
    # pas couverts par les hachés d'éléments : CSP3 les admet un par un via
    # 'unsafe-hashes' — chaque VALEUR d'attribut est hachée, rien d'autre ne passe
    attributs = sorted(set(re.findall(r'style="([^"]*)"', t)))
    if attributs:
        style_src += " 'unsafe-hashes' " + " ".join(h(a) for a in attributs)
    script_src = " ".join(h(s) for s in scripts) if scripts else "'none'"
    regle = ("default-src 'none'; "
             f"style-src {style_src}; "
             f"script-src {script_src}; "
             "font-src 'self'; img-src 'self' data:; "
             "base-uri 'self'; "
             "form-action 'none'; connect-src 'none'")
    return t.replace(
        '<meta charset="utf-8">',
        f'<meta charset="utf-8">\n'
        f'<meta http-equiv="Content-Security-Policy" content="{regle}">\n'
        f'<meta name="referrer" content="no-referrer">', 1)


def entete_prod(t, neuf):
    """Les métadonnées de production : canonique, couleur d'onglet, icône
    tactile, compléments de la carte de partage."""
    # la racine et /index.html sont la même page : une seule adresse canonique,
    # la racine, sinon les moteurs comptent deux pages et partagent leur poids
    adresse = BASE_URL if neuf == "index.html" else BASE_URL + neuf
    if neuf.endswith("/index.html"):
        adresse = BASE_URL + neuf.removesuffix("index.html")
    # la couleur d'onglet suit la nuit de l'outil : rubis sous screening/
    theme = "#241217" if neuf.startswith("screening/") else "#14251e"
    extra = (f'<link rel="canonical" href="{adresse}">\n'
             f'<link rel="apple-touch-icon" href="{PREFIXE}apple-touch-icon.png">\n'
             f'<meta name="theme-color" content="{theme}">')
    t = t.replace('<meta name="viewport" content="width=device-width,initial-scale=1">',
                  '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
                  + extra, 1)
    t = t.replace('<meta name="twitter:card" content="summary_large_image">',
                  '<meta property="og:site_name" content="Cascade">\n'
                  '<meta property="og:locale" content="en_US">\n'
                  '<meta property="og:image:width" content="1200">\n'
                  '<meta property="og:image:height" content="630">\n'
                  '<meta name="twitter:card" content="summary_large_image">', 1)
    return t


SCREENING_EMISES = {v: n for v, n in PROD_SCREENING.items() if (MAQ / v).exists()}
for v in PROD_SCREENING:
    if v not in SCREENING_EMISES:
        print(f"  screening : {v} absent (lot S2/S3) : non émis, dit ici")


def renommer_liens(t, page_screening):
    """Les noms SOURCE deviennent les noms de production. Dans une page du
    sous-dossier, une sœur rouge se lie par son nom NU (même dossier) ; depuis
    la racine, par son chemin complet. Les noms rouges se remplacent d'abord :
    plus longs, ils contiennent des fragments qui ressemblent aux verts."""
    for v, n in SCREENING_EMISES.items():
        t = t.replace(v, n.removeprefix("screening/") if page_screening else n)
    for v, n in PROD.items():
        t = t.replace(v, n)
    return t


for vieux, neuf in {**PROD, **SCREENING_EMISES}.items():
    t = (MAQ / vieux).read_text()
    t = renommer_liens(t, neuf.startswith("screening/"))
    (DOCS / neuf).parent.mkdir(parents=True, exist_ok=True)
    if neuf == "404.html":
        # servie pour N'IMPORTE QUEL chemin manquant : ses liens relatifs
        # doivent se résoudre depuis la racine du site, pas depuis le chemin raté
        t = t.replace('<meta charset="utf-8">',
                      f'<meta charset="utf-8"><base href="{PREFIXE}">', 1)
    (DOCS / neuf).write_text(csp(entete_prod(t, neuf)))

# ── le refus du « placeholder » en production, témoin d'abord ────────────────
# Une page rouge bâtie sur le plateau vert porte un commentaire « placeholder » ;
# la production la refuse : un brouillon qui ressemble à une page finie se
# publie par accident, jamais par décision.
# Le MARQUEUR « <!-- placeholder: » et jamais le mot nu : la prose légitime du
# site dit « replaced by a placeholder » (Security, Privacy), et une garde qui
# rougit sur la prose se fait retirer : première passe rouge, mesurée ce soir.
def _pages_placeholder(dossier):
    return [str(p.relative_to(dossier)) for p in sorted(dossier.rglob("*.html"))
            if "<!-- placeholder:" in p.read_text()]

_tp = DOCS / "zz-temoin-placeholder.html"
_tp.write_text("<!-- placeholder: temoin -->")
if not _pages_placeholder(DOCS):
    sys.exit("GARDE CASSÉE : le témoin « placeholder » planté n'a pas été vu")
_tp.unlink()
brouillons = _pages_placeholder(DOCS)
if brouillons:
    sys.exit(f"PLACEHOLDER en production : {brouillons} : la page attend ses vrais "
             "rendus (tamis-0*.webp) : elle ne part pas comme ça")

# ── le refus du cadratin : décision du 3 septembre, aucune page ne le porte ──
fautives = [str(p.relative_to(DOCS)) for p in sorted(DOCS.rglob("*.html"))
            if any(m in p.read_text() for m in ("\u2014", "&#8212;", "&mdash;"))]
if fautives:
    sys.exit(f"CADRATIN dans les pages bâties : {fautives} : réécrire la source, pas la page")

# ── les données structurées : lisibles, exactes, sans mensonge SEO ───────────
# Trois refus : un bloc ld+json qui ne parse pas ; une clé de notation
# (aggregateRating, review…) qui n'aurait aucune mesure derrière elle ; un prix
# autre que le 0 du grant d'évaluation (les prix payants vivent en clair sur la
# page engagement, jamais dans le balisage). Et la couture source → moteur :
# la FAQ émise est comparée à SA SOURCE (annexe-questions.json), question par
# question, même normalisation que l'émission.
import html as _html
import json as _json

def _nu(fragment):
    return " ".join(_html.unescape(re.sub(r"<[^>]+>", "", fragment)).split())

def _cles(o):
    if isinstance(o, dict):
        yield from o
        for v in o.values():
            yield from _cles(v)
    elif isinstance(o, list):
        for v in o:
            yield from _cles(v)

INTERDITES = {"aggregateRating", "review", "ratingValue", "reviewCount",
              "bestRating", "worstRating"}
blocs_vus = {}
for page in sorted(DOCS.rglob("*.html")):
    for brut in re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                           page.read_text(), re.S):
        try:
            donnees = _json.loads(brut)
        except ValueError as e:
            sys.exit(f"JSON-LD invalide dans {page.name} : {e}")
        mauvaises = INTERDITES & set(_cles(donnees))
        if mauvaises:
            sys.exit(f"JSON-LD de {page.name} : {sorted(mauvaises)} : "
                     "aucune mesure derrière : retirer")
        for prix in re.findall(r'"price"\s*:\s*"?([^",}]*)', brut):
            if prix.strip() != "0":
                sys.exit(f"JSON-LD de {page.name} : price={prix} : les prix "
                         "vivent en clair sur la page engagement, pas ici")
        blocs_vus.setdefault(str(page.relative_to(DOCS)), []).append(donnees)

noeuds_index = blocs_vus.get("index.html", [{}])[0].get("@graph", [])
types_index = {n.get("@type") for n in noeuds_index}
if not {"Organization", "SoftwareApplication"} <= types_index:
    sys.exit(f"index.html : Organization + SoftwareApplication attendus dans le "
             f"@graph, vu {sorted(t for t in types_index if t)}")

source_q = _json.loads((MAQ / "annexe-questions.json").read_text())
attendues = [_nu(s["h2"]).strip("“” ") for s in source_q["sections"]]
faq = next((b for b in blocs_vus.get("questions.html", [])
            if b.get("@type") == "FAQPage"), None)
if faq is None:
    sys.exit("questions.html : FAQPage absent des données structurées")
publiees = [e["name"] for e in faq.get("mainEntity", [])]
if publiees != attendues:
    sys.exit("FAQPage : les questions émises ne recomposent pas la source : "
             f"{sorted(set(attendues) ^ set(publiees))}")

# le héros rouge, quand il est émis, porte le même socle de graphe que le vert
if "screening/index.html" in blocs_vus:
    types_r = {noeud.get("@type")
               for noeud in blocs_vus["screening/index.html"][0].get("@graph", [])}
    if not {"Organization", "SoftwareApplication"} <= types_r:
        sys.exit(f"screening/index.html : Organization + SoftwareApplication attendus, "
                 f"vu {sorted(x for x in types_r if x)}")
print(f"  données structurées : "
      f"{sum(len(v) for v in blocs_vus.values())} blocs valides sur "
      f"{len(blocs_vus)} pages ; FAQ recomposée : {len(publiees)} questions")

# ── les ressources réellement référencées ────────────────────────────────────
refs = set()
for page in DOCS.rglob("*.html"):
    for m in re.finditer(r'(?:href|src)="([^"]+)"', page.read_text()):
        u = m.group(1)
        if u.startswith(("http", "#", "data:", "mailto:")):
            continue
        refs.add(str((page.parent / u.split("#")[0]).resolve().relative_to(DOCS.resolve()))
                 if not u.startswith("/") else u.split("#")[0])

(DOCS / "fontes").mkdir()
shutil.copy(MAQ / "fontes" / "literata.css", DOCS / "fontes" / "literata.css")
for w in (MAQ / "fontes").glob("literata-*.woff2"):
    shutil.copy(w, DOCS / "fontes" / w.name)
shutil.copy(MAQ / "fontes" / "roboto-mono.css", DOCS / "fontes" / "roboto-mono.css")
shutil.copy(MAQ / "fontes" / "roboto-mono.woff2", DOCS / "fontes" / "roboto-mono.woff2")
(DOCS / "rendus" / "etats").mkdir(parents=True)
for w in (MAQ / "rendus" / "etats").glob("objet-*.webp"):
    shutil.copy(w, DOCS / "rendus" / "etats" / w.name)
shutil.copy(MAQ / "rendus" / "affiche-film.jpg", DOCS / "rendus" / "affiche-film.jpg")
for rb in ("robot-penche.webp", "robot-agrippe.webp"):
    shutil.copy(MAQ / "rendus" / rb, DOCS / "rendus" / rb)
if SCREENING_EMISES:
    for rb in ("robot-rubis-penche.webp", "robot-rubis-agrippe.webp"):
        shutil.copy(MAQ / "rendus" / rb, DOCS / "rendus" / rb)
    for w in (MAQ / "rendus" / "etats").glob("tamis-*.webp"):
        shutil.copy(w, DOCS / "rendus" / "etats" / w.name)
shutil.copy(MAQ / "releve.json", DOCS / "releve.json")
shutil.copy(MAQ / "og.png", DOCS / "og.png")
(DOCS / ".nojekyll").write_text("")

# Le fichier CNAME : c'est LUI qui déclare le domaine propre à GitHub Pages, et
# docs/ est régénéré à chaque assemblage — s'il n'était pas émis ici, la
# première reconstruction après la bascule ferait tomber le domaine.
HOTE = urlparse(BASE_URL).hostname
if not HOTE.endswith(".github.io"):
    (DOCS / "CNAME").write_text(HOTE + "\n")

# ── robots, plan du site, security.txt : les portes d'entrée normées ─────────
(DOCS / "robots.txt").write_text(
    f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n")
(DOCS / ".well-known").mkdir()
(DOCS / ".well-known" / "security.txt").write_text(
    "Contact: mailto:contact@cascade-routing.com\n"
    "Contact: https://github.com/ArslaneSempai-ui/cascade-site/issues\n"
    "Contact: https://github.com/ArslaneSempai-ui/cascade-routing/issues\n"
    "Expires: 2027-08-31T00:00:00.000Z\n"
    "Preferred-Languages: en, fr\n"
    f"Canonical: {BASE_URL}.well-known/security.txt\n")
shutil.copy(MAQ / "apple-touch-icon.png", DOCS / "apple-touch-icon.png")
publiques = ([n for n in PROD.values() if n != "404.html"]
             + [n for n in SCREENING_EMISES.values()])
(DOCS / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{BASE_URL}{'' if n == 'index.html' else n.removesuffix('index.html') if n.endswith('/index.html') else n}</loc></url>\n"
              for n in publiques)
    + "</urlset>\n")

# ── la garde de dérive : le compte de tests que le site PUBLIE ───────────────
# Le 31 août, le dépôt est passé de 584/65 à 595/66 en une heure et le site a
# continué d'afficher l'ancien — sur la page même qui promet qu'un tel chiffre
# « cannot silently rot ». La règle vérifiable devient donc un refus.
# Elle dit AUSSI quand elle n'a pas pu regarder : un silence se lirait comme un
# accord, et c'est exactement le vert vide qu'on cherche à éviter.
# Chaque OUTIL est vérifié contre SON dépôt : le compte du rouge sur une page
# rouge, celui du vert sur une page verte. Croiser les deux ferait rougir un
# site juste : les deux dépôts n'ont pas le même compte, et c'est normal.
def verifier_comptes(pages, depot, etiquette):
    publie = set()
    for page in pages:
        publie |= set(re.findall(r"(\d+) tests(?: across (\d+) files)?",
                                 page.read_text()))
    if not publie:
        return
    comptes = {n for n, _ in publie}
    fichiers = {f for _, f in publie if f}
    if not depot.exists():
        print(f"  ! compte de tests {etiquette} NON VÉRIFIÉ : {depot} absent — "
              f"le site publie {sorted(comptes)} / {sorted(fichiers)}")
        return
    m = re.search(r"\*\*(\d+) tests\*\*(?: across (\d+) files)?", depot.read_text())
    if not m:
        sys.exit(f"la phrase des tests est introuvable dans {depot} — "
                 f"garde cassée, son silence ne vaut rien")
    vrai_n, vrai_f = m.group(1), m.group(2)
    if comptes - {vrai_n} or (vrai_f and fichiers - {vrai_f}):
        sys.exit(f"DÉRIVE DU COMPTE DE TESTS ({etiquette}) : le dépôt dit {vrai_n} / "
                 f"{vrai_f}, le site publie {sorted(comptes)} / {sorted(fichiers)} "
                 f"— corriger les JSON avant d'assembler")
    print(f"  compte de tests {etiquette} vérifié : {vrai_n} tests")

verifier_comptes(sorted(DOCS.glob("*.html")),
                 pathlib.Path.home() / "Documents" / "cascade" / "README.md", "routing")
verifier_comptes(sorted((DOCS / "screening").glob("*.html")) if (DOCS / "screening").exists() else [],
                 pathlib.Path.home() / "Documents" / "cascade-screening" / "README.md", "screening")

# ── la garde des citations : « Where it lives » doit encore dire vrai ────────
# Le site invite un relecteur bancaire à OUVRIR chaque chemin. Une citation qui
# a glissé de vingt lignes le fait tomber sur autre chose, et c'est pire qu'une
# absence de citation. Mesuré le 31/08 : le durcissement de l'outil a déplacé 7
# des 38 citations — un contrôle de bornes serait passé, elles pointaient toutes
# dans un fichier de la bonne taille. On vérifie donc le CONTENU de la ligne.
# Chaque OUTIL contre SON dépôt et SON fichier d'ancres (ancrer-citations.py les
# régénère) : les pages rouges citent cascade-screening, les vertes cascade.
def verifier_citations(pages, ancres_fichier, outil, etiquette):
    citees = set()
    for page in pages:
        citees |= set(re.findall(r"[A-Za-z0-9_./-]+\.(?:ts|mjs|json|md|js):\d+",
                                 page.read_text()))
    if not citees:
        return
    if not ancres_fichier.exists():
        print(f"  ! citations {etiquette} NON VÉRIFIÉES : {ancres_fichier.name} absent — "
              f"{len(citees)} citées")
        return
    if not outil.exists():
        print(f"  ! citations {etiquette} NON VÉRIFIÉES : {outil} absent — {len(citees)} citées")
        return
    ancres = _json.loads(ancres_fichier.read_text())["ancres"]
    fautes = []
    for c in sorted(citees):
        if c not in ancres:
            fautes.append(f"{c} — aucune ancre déclarée"); continue
        chemin, n = c.rsplit(":", 1)
        f = outil / chemin
        if not f.exists():
            fautes.append(f"{c} — fichier absent de l'outil"); continue
        lignes = f.read_text(errors="replace").splitlines()
        n = int(n)
        if n > len(lignes):
            fautes.append(f"{c} — au-delà de la fin ({len(lignes)} lignes)"); continue
        if lignes[n - 1].strip() != ancres[c]:
            ou = [i + 1 for i, x in enumerate(lignes) if x.strip() == ancres[c]]
            fautes.append(f"{c} — la ligne a changé"
                          + (f", le contenu est en {chemin}:{ou[0]}" if len(ou) == 1
                             else ", contenu introuvable"))
    if fautes:
        sys.exit(f"CITATIONS {etiquette.upper()} QUI NE DISENT PLUS VRAI :\n  " + "\n  ".join(fautes)
                 + f"\n  corriger les JSON, puis régénérer {ancres_fichier.name} (ancrer-citations.py)")
    print(f"  citations {etiquette} vérifiées ligne à ligne contre l'outil : {len(citees)}")

verifier_citations(sorted(DOCS.glob("*.html")), MAQ / "ancres-citations.json",
                   pathlib.Path.home() / "Documents" / "cascade", "routing")
verifier_citations(sorted((DOCS / "screening").glob("*.html")) if (DOCS / "screening").exists() else [],
                   MAQ / "ancres-citations-screening.json",
                   pathlib.Path.home() / "Documents" / "cascade-screening", "screening")

# ── le contrôle de liens, témoin d'abord ─────────────────────────────────────
def liens_casses(dossier):
    casses = []
    for page in sorted(dossier.rglob("*.html")):
        for m in re.finditer(r'(?:href|src)="([^"]+)"', page.read_text()):
            u = m.group(1).split("#")[0]
            if u.startswith(("http", "data:", "mailto:")) or not u:
                continue
            # racine-relatif sous le préfixe du site : {PREFIXE}x → x ; sinon
            # RELATIF AU RÉPERTOIRE DE LA PAGE (../x depuis screening/), et un
            # répertoire se sert comme son index.html
            if u.startswith(PREFIXE):
                cible = dossier / (u.removeprefix(PREFIXE) or "index.html")
            elif u.startswith("/"):
                casses.append(f"{page.relative_to(dossier)} → {m.group(1)} (racine hors préfixe)")
                continue
            else:
                cible = (page.parent / u).resolve()
                d = dossier.resolve()
                if d != cible and d not in cible.parents:
                    casses.append(f"{page.relative_to(dossier)} → {m.group(1)} (sort du site)")
                    continue
            if cible.is_dir():
                cible = cible / "index.html"
            if not cible.exists():
                casses.append(f"{page.relative_to(dossier)} → {m.group(1)}")
    return casses

temoin = DOCS / "zz-temoin.html"
temoin.write_text('<a href="fantome-inexistant.css">x</a>')
if not any("fantome-inexistant" in c for c in liens_casses(DOCS)):
    sys.exit("CONTRÔLE CASSÉ : le témoin planté n'a pas été trouvé — zéro sans valeur")
temoin.unlink()

casses = liens_casses(DOCS)
if casses:
    sys.exit("LIENS CASSÉS :\n  " + "\n  ".join(casses))

# ── source/ : la chaîne de fabrication, sans les déchets ─────────────────────
SRC = SITE / "source"
if MAQ.resolve() == SRC.resolve():
    # lancé depuis source/ : la chaîne est déjà là, rien à recopier
    print(f"docs/ : {len(PROD)} pages + ressources ; témoin retrouvé, "
          f"0 lien cassé sur {len(refs)} référencés")
    sys.exit(0)
if SRC.exists():
    shutil.rmtree(SRC)
SRC.mkdir()
for f in MAQ.iterdir():
    if f.name in PROD or f.name in {"__pycache__", "apercu", "directions",
                                    "refonte", "controle", "PARCOURS.html"}:
        continue
    if f.name.startswith("U") and f.suffix == ".html":
        continue
    if f.is_dir():
        if f.name == "fontes":
            (SRC / "fontes").mkdir()
            for w in f.iterdir():
                if w.name.startswith("literata"):
                    shutil.copy(w, SRC / "fontes" / w.name)
        else:
            shutil.copytree(f, SRC / f.name,
                            ignore=shutil.ignore_patterns("__pycache__"))
    else:
        shutil.copy(f, SRC / f.name)

nb_docs = len(list(DOCS.rglob("*")))
nb_src = len(list(SRC.rglob("*")))
print(f"docs/ : {len(PROD)} pages + ressources, {nb_docs} entrées ; "
      f"témoin retrouvé, 0 lien cassé sur {len(refs)} référencés")
print(f"source/ : {nb_src} entrées")
