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

# ── bâtir d'abord : les pages naissent à côté de ce script ───────────────────
# L'audit du 31/08 a montré l'inverse en danger : un rmtree AVANT de vérifier
# ses entrées détruisait docs/ puis plantait, puisque source/ ne portait pas
# les pages bâties. Ordre tenu : bâtir, vérifier, seulement ensuite effacer.
import subprocess
for batisseur in ("batir-hero.py", "batir-annexe.py"):
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
    extra = (f'<link rel="canonical" href="{BASE_URL}{neuf}">\n'
             f'<link rel="apple-touch-icon" href="{PREFIXE}apple-touch-icon.png">\n'
             f'<meta name="theme-color" content="#14251e">')
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


for vieux, neuf in PROD.items():
    t = (MAQ / vieux).read_text()
    for v, n in PROD.items():
        t = t.replace(v, n)
    if neuf == "404.html":
        # servie pour N'IMPORTE QUEL chemin manquant : ses liens relatifs
        # doivent se résoudre depuis la racine du site, pas depuis le chemin raté
        t = t.replace('<meta charset="utf-8">',
                      f'<meta charset="utf-8"><base href="{PREFIXE}">', 1)
    (DOCS / neuf).write_text(csp(entete_prod(t, neuf)))

# ── le refus du cadratin : décision du 3 septembre, aucune page ne le porte ──
fautives = [p.name for p in sorted(DOCS.glob("*.html"))
            if any(m in p.read_text() for m in ("\u2014", "&#8212;", "&mdash;"))]
if fautives:
    sys.exit(f"CADRATIN dans les pages bâties : {fautives} : réécrire la source, pas la page")

# ── les ressources réellement référencées ────────────────────────────────────
refs = set()
for page in DOCS.glob("*.html"):
    for m in re.finditer(r'(?:href|src)="([^"]+)"', page.read_text()):
        u = m.group(1)
        if u.startswith(("http", "#", "data:", "mailto:")):
            continue
        refs.add(u.split("#")[0])

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
publiques = [n for n in PROD.values() if n != "404.html"]
(DOCS / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{BASE_URL}{n}</loc></url>\n" for n in publiques)
    + "</urlset>\n")

# ── la garde de dérive : le compte de tests que le site PUBLIE ───────────────
# Le 31 août, le dépôt est passé de 584/65 à 595/66 en une heure et le site a
# continué d'afficher l'ancien — sur la page même qui promet qu'un tel chiffre
# « cannot silently rot ». La règle vérifiable devient donc un refus.
# Elle dit AUSSI quand elle n'a pas pu regarder : un silence se lirait comme un
# accord, et c'est exactement le vert vide qu'on cherche à éviter.
DEPOT = pathlib.Path.home() / "Documents" / "cascade" / "README.md"
publie = set()
for page in DOCS.glob("*.html"):
    publie |= set(re.findall(r"(\d+) tests(?: across (\d+) files)?",
                             page.read_text()))
comptes = {n for n, _ in publie}
fichiers = {f for _, f in publie if f}
if not DEPOT.exists():
    print(f"  ! compte de tests NON VÉRIFIÉ : {DEPOT} absent — "
          f"le site publie {sorted(comptes)} tests / {sorted(fichiers)} fichiers")
else:
    m = re.search(r"\*\*(\d+) tests\*\* across (\d+) files", DEPOT.read_text())
    if not m:
        sys.exit(f"la phrase des tests est introuvable dans {DEPOT} — "
                 f"garde cassée, son silence ne vaut rien")
    vrai_n, vrai_f = m.group(1), m.group(2)
    if comptes - {vrai_n} or fichiers - {vrai_f}:
        sys.exit(f"DÉRIVE DU COMPTE DE TESTS : le dépôt dit {vrai_n} tests / "
                 f"{vrai_f} fichiers, le site publie {sorted(comptes)} / "
                 f"{sorted(fichiers)} — corriger les JSON avant d'assembler")
    print(f"  compte de tests vérifié contre le dépôt : {vrai_n} tests, "
          f"{vrai_f} fichiers")

# ── la garde des citations : « Where it lives » doit encore dire vrai ────────
# Le site invite un relecteur bancaire à OUVRIR chaque chemin. Une citation qui
# a glissé de vingt lignes le fait tomber sur autre chose, et c'est pire qu'une
# absence de citation. Mesuré le 31/08 : le durcissement de l'outil a déplacé 7
# des 38 citations — un contrôle de bornes serait passé, elles pointaient toutes
# dans un fichier de la bonne taille. On vérifie donc le CONTENU de la ligne.
ANCRES = MAQ / "ancres-citations.json"
OUTIL = pathlib.Path.home() / "Documents" / "cascade"
citees = set()
for page in DOCS.glob("*.html"):
    citees |= set(re.findall(r"[A-Za-z0-9_./-]+\.(?:ts|mjs|json|md|js):\d+",
                             page.read_text()))
if not ANCRES.exists():
    print(f"  ! citations NON VÉRIFIÉES : {ANCRES.name} absent — {len(citees)} citées")
elif not OUTIL.exists():
    print(f"  ! citations NON VÉRIFIÉES : {OUTIL} absent — {len(citees)} citées")
else:
    import json as _json
    ancres = _json.loads(ANCRES.read_text())["ancres"]
    fautes = []
    for c in sorted(citees):
        if c not in ancres:
            fautes.append(f"{c} — aucune ancre déclarée"); continue
        chemin, n = c.rsplit(":", 1)
        f = OUTIL / chemin
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
        sys.exit("CITATIONS QUI NE DISENT PLUS VRAI :\n  " + "\n  ".join(fautes)
                 + "\n  corriger les JSON, puis régénérer ancres-citations.json")
    print(f"  citations vérifiées ligne à ligne contre l'outil : {len(citees)}")

# ── le contrôle de liens, témoin d'abord ─────────────────────────────────────
def liens_casses(dossier):
    casses = []
    for page in sorted(dossier.glob("*.html")):
        for m in re.finditer(r'(?:href|src)="([^"]+)"', page.read_text()):
            u = m.group(1).split("#")[0]
            if u.startswith(("http", "data:", "mailto:")) or not u:
                continue
            # racine-relatif sous le préfixe du site : {PREFIXE}x → x,
            # et le préfixe nu est le répertoire — servi comme index.html
            if u.startswith(PREFIXE):
                u = u.removeprefix(PREFIXE) or "index.html"
            elif u.startswith("/"):
                casses.append(f"{page.name} → {m.group(1)} (racine hors préfixe)")
                continue
            if not (dossier / u).exists():
                casses.append(f"{page.name} → {m.group(1)}")
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
