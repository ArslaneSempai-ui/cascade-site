#!/usr/bin/env python3
"""THE COPY INVENTORY : every sentence a reader can see on the served site, in one table.
Arslane, 9/09/2026 : the whole copy is to be rewritten in ONE pass (« trop flagrant que c'est
IA, des fois même pas compréhensible »), never sentence by sentence with screenshots. The pass
starts with this inventory : what is written, where, how long, and what kind of line it is.

Reads docs/*.html (what is served, after assembly) and the findings-*.json (the labels and the
cards of the five heroes, which the builders inline). Writes, next to the site :
  inventaire-copy.json   one record per text block : page, kind, selector hint, text, chars
  inventaire-copy.md     the same, readable, grouped by page, with counts
usage: python3 inventaire-copy.py [--sortie DIR]   (default : ../.verif-final/)
"""
import json, pathlib, re, sys
from html.parser import HTMLParser

BASE = pathlib.Path(__file__).parent
DOCS = BASE.parent / "docs"
OUT = pathlib.Path(sys.argv[sys.argv.index("--sortie") + 1]) if "--sortie" in sys.argv else BASE.parent / ".verif-final"
OUT.mkdir(parents=True, exist_ok=True)

TEXTE = {"h1", "h2", "h3", "h4", "p", "li", "button", "a", "figcaption", "caption", "label", "dt", "dd", "th", "td", "summary", "blockquote"}
SAUT = {"script", "style", "svg", "noscript", "template"}
SORTES = {"h1": "titre", "h2": "titre", "h3": "titre", "h4": "titre", "p": "paragraphe", "li": "puce", "button": "bouton",
          "a": "lien", "figcaption": "légende", "caption": "légende", "label": "étiquette", "dt": "terme", "dd": "définition",
          "th": "cellule", "td": "cellule", "summary": "résumé", "blockquote": "citation"}


class Cueilleur(HTMLParser):
    """Collects the text of every block-level text element, with its class hint."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pile = []          # (tag, classes, buffer)
        self.saut = 0
        self.blocs = []
        self.attrs_textes = []  # alt / aria-label / title / placeholder

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in SAUT:
            self.saut += 1
        for k in ("alt", "aria-label", "title", "placeholder"):
            if a.get(k, "").strip():
                self.attrs_textes.append((tag, k, a[k].strip()))
        if tag in TEXTE and not self.saut:
            self.pile.append([tag, a.get("class", ""), []])

    def handle_endtag(self, tag):
        if tag in SAUT and self.saut:
            self.saut -= 1
        if tag in TEXTE and self.pile and self.pile[-1][0] == tag:
            t, cls, buf = self.pile.pop()
            texte = re.sub(r"\s+", " ", "".join(buf)).strip()
            if texte:
                self.blocs.append((t, cls, texte))
            if self.pile:                      # nested text also counts for the parent
                self.pile[-1][2].append(" " + texte + " ")

    def handle_data(self, data):
        if self.saut or not self.pile:
            return
        self.pile[-1][2].append(data)


def sorte(tag, cls, texte):
    if "ap-eti" in cls or "eti" in cls.split():
        return "étiquette-3D"
    if "j-titre" in cls or "j-cote" in cls:
        return "rail"
    if "tm-" in cls or "preuve" in cls or "lect" in cls or "carte-aide" in cls:
        return "terminal"
    if "sr" in cls.split():
        return "lecteur-d'écran"
    if re.fullmatch(r"[\d\s.,%$€:/()\-–+]+", texte):
        return "chiffre"
    return SORTES.get(tag, tag)


records = []
vus = set()
for page in sorted(DOCS.rglob("*.html")):
    rel = str(page.relative_to(DOCS))
    c = Cueilleur()
    c.feed(page.read_text(encoding="utf-8"))
    for tag, cls, texte in c.blocs:
        if len(texte) < 3:
            continue
        cle = (rel, texte)
        if cle in vus:
            continue
        vus.add(cle)
        records.append({"page": rel, "sorte": sorte(tag, cls, texte), "balise": tag, "classe": cls, "texte": texte, "car": len(texte)})
    for tag, k, texte in c.attrs_textes:
        cle = (rel, texte)
        if cle in vus:
            continue
        vus.add(cle)
        records.append({"page": rel, "sorte": f"attribut {k}", "balise": tag, "classe": "", "texte": texte, "car": len(texte)})

# the findings : labels and cards of the five heroes (inlined by the builders, but listed by source)
for f in sorted(BASE.glob("findings-*.json")):
    d = json.loads(f.read_text())
    findings = d["findings"] if isinstance(d, dict) and "findings" in d else d
    for i, fd in enumerate(findings if isinstance(findings, list) else []):
        for k in ("titre", "title", "kicker", "sous", "corps", "body", "texte", "chiffre_legende", "legende"):
            v = fd.get(k)
            if isinstance(v, str) and v.strip():
                records.append({"page": f.name, "sorte": f"finding {fd.get('num', i + 1)} · {k}", "balise": "json", "classe": "", "texte": v.strip(), "car": len(v.strip())})
        for a in fd.get("annotations", []):
            if isinstance(a, (list, tuple)) and len(a) == 5:
                records.append({"page": f.name, "sorte": f"finding {fd.get('num', i + 1)} · étiquette-3D", "balise": "json", "classe": "", "texte": a[4], "car": len(a[4])})

(OUT / "inventaire-copy.json").write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")

# the readable table
lignes = ["# Inventaire de la copy du site (servi)", "",
          f"{len(records)} blocs de texte · {sum(r['car'] for r in records)} caractères · "
          f"{len({r['page'] for r in records})} sources", ""]
par_page = {}
for r in records:
    par_page.setdefault(r["page"], []).append(r)
for page, rs in par_page.items():
    lignes += [f"## {page} · {len(rs)} blocs · {sum(r['car'] for r in rs)} car", "", "| sorte | car | texte |", "|---|---:|---|"]
    for r in rs:
        t = r["texte"].replace("|", "\\|")
        lignes.append(f"| {r['sorte']} | {r['car']} | {t} |")
    lignes.append("")
(OUT / "inventaire-copy.md").write_text("\n".join(lignes), encoding="utf-8")
sortes = {}
for r in records:
    s = r["sorte"].split(" · ")[-1] if r["sorte"].startswith("finding") else r["sorte"]
    sortes[s] = sortes.get(s, 0) + 1
print(f"{len(records)} blocs, {sum(r['car'] for r in records)} caractères, {len(par_page)} sources → {OUT / 'inventaire-copy.md'}")
print("par sorte :", ", ".join(f"{k} {v}" for k, v in sorted(sortes.items(), key=lambda x: -x[1])))
