#!/usr/bin/env python3
"""Assemble le site hors du scratchpad, vers ~/Documents/cascade-site.

Le scratchpad est éphémère ; ce script sort les DEUX choses qui comptent :
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
BASE_URL = "https://arslanesempai-ui.github.io/cascade-routing/"

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

# ── docs/ : les pages, renommées, liens réécrits ─────────────────────────────
if DOCS.exists():
    shutil.rmtree(DOCS)
DOCS.mkdir(parents=True)

for vieux, neuf in PROD.items():
    t = (MAQ / vieux).read_text()
    for v, n in PROD.items():
        t = t.replace(v, n)
    if neuf == "404.html":
        # servie pour N'IMPORTE QUEL chemin manquant : ses liens relatifs
        # doivent se résoudre depuis la racine du site, pas depuis le chemin raté
        t = t.replace('<meta charset="utf-8">',
                      f'<meta charset="utf-8"><base href="{BASE_URL}">', 1)
    (DOCS / neuf).write_text(t)

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
(DOCS / "rendus" / "etats").mkdir(parents=True)
for w in (MAQ / "rendus" / "etats").glob("objet-*.webp"):
    shutil.copy(w, DOCS / "rendus" / "etats" / w.name)
shutil.copy(MAQ / "releve.json", DOCS / "releve.json")
shutil.copy(MAQ / "og.png", DOCS / "og.png")
(DOCS / ".nojekyll").write_text("")

# ── le contrôle de liens, témoin d'abord ─────────────────────────────────────
def liens_casses(dossier):
    casses = []
    for page in sorted(dossier.glob("*.html")):
        for m in re.finditer(r'(?:href|src)="([^"]+)"', page.read_text()):
            u = m.group(1)
            if u.startswith(("http", "#", "data:", "mailto:")):
                continue
            if not (dossier / u.split("#")[0]).exists():
                casses.append(f"{page.name} → {u}")
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
if SRC.exists():
    shutil.rmtree(SRC)
SRC.mkdir()
for f in MAQ.iterdir():
    if f.name in PROD or f.name in {"__pycache__", "apercu", "directions",
                                    "refonte", "controle", "PARCOURS.html",
                                    "og.png"}:
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
