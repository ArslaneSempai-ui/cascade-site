#!/usr/bin/env python3
"""THE LIST-COUNT GUARD (Crusetra V4, 6 October 2026).

On 5 October Screening went from seven public sanctions sources to ten (the sources-plus merge,
crusetra-screening 27e7fac), and nine sentences of the served site still said seven. The count is
not ours to type: it is the number of lists in the tool's committed manifest
(listes-manifest.json), and this guard reads it there.

It refuses, in every served page outside the other tools' folders and the Routing sample, a count
of lists or sources (« seven sanctions lists », « 7 public sources », « the seven sources ») that
is not the manifest's. A dated count passes: « the seven sources of 4 October » describes a record
screened on that day's lists, and says so.

Its own witness runs first: planted sentences must be refused, the true ones must pass, or it exits
2. The assembler adds the outer witness (a planted page in docs/ must turn it red).

  python3 garde-listes.py --docs ../docs      exit 0 clean, 1 refused, 2 broken guard
"""
import html
import json
import pathlib
import re
import sys

ICI = pathlib.Path(__file__).parent
sys.path.insert(0, str(ICI))
from outil import OUTILS  # noqa: E402

MANIFESTE = OUTILS["screening"]["outil_chemin"] / "listes-manifest.json"
MOTS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
        10: "ten", 11: "eleven", 12: "twelve"}
NOMBRES = {v: k for k, v in MOTS.items()}
COMPTE = re.compile(r"\b(" + "|".join(MOTS.values()) + r"|\d+)\s+(?:public\s+|official\s+)?(?:sanctions?\s+)?(?:lists|sources)\b",
                    re.I)
DATE = re.compile(r"\s+of\s+\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\b")
# the other tools' pages and the Routing sample count other things (« 8 sources on 3 fields » is Routing's)
HORS = ("routing/", "monitoring/", "scoring/", "dossier/", "rapports/routing", "method.html", "security.html",
        "instrument.html")


def compte_du_manifeste():
    listes = json.loads(MANIFESTE.read_text())["listes"]
    return len(listes)


def lu(texte):
    sans = re.sub(r"<(script|style)\b.*?</\1>", lambda m: "\n" * m.group(0).count("\n"), texte, flags=re.S | re.I)
    sans = re.sub(r"<[^>]*>", lambda m: " " + "\n" * m.group(0).count("\n"), sans)
    return html.unescape(sans)


def fautes_du_texte(nom, texte, n):
    fautes = []
    t = lu(texte)
    for m in COMPTE.finditer(t):
        mot = m.group(1).lower()
        dit = int(mot) if mot.isdigit() else NOMBRES[mot]
        if dit == n or DATE.match(t, m.end()):
            continue
        ligne = t.count("\n", 0, m.start()) + 1
        fautes.append(f"{nom}:{ligne}: « {' '.join(m.group(0).split())} », the manifest holds {MOTS.get(n, n)} lists")
    return fautes


def fautes_du_site(docs, n):
    fautes = []
    for f in sorted(docs.rglob("*.html")):
        nom = str(f.relative_to(docs))
        if nom.startswith(HORS):
            continue
        fautes += fautes_du_texte(nom, f.read_text(), n)
    return fautes


def temoin(n):
    faux = MOTS[n - 3] if n > 3 else "twelve"
    plantes = [f"<h2>Your names, screened against {faux} sanctions lists.</h2>",
               f"<p>We screen it against {n + 1} public sources and send back a PDF.</p>",
               f"<li>The dates of the {faux} sources, and a seal</li>"]
    saines = [f"<p>We screen each name against {MOTS.get(n, n)} public sources: OFAC SDN and the others.</p>",
              f"<p>1,000 invented counterparties, screened against the {faux} sources of 4 October: lit marks.</p>",
              "<p>Crusetra Screening compares names seven ways, at every threshold.</p>"]
    manquees = [p for p in plantes if not fautes_du_texte("temoin", p, n)]
    bruit = [s for s in saines if fautes_du_texte("temoin", s, n)]
    if manquees or bruit:
        sys.exit(f"GARDE CASSÉE (garde-listes): {len(manquees)} planted count(s) passed ({'; '.join(manquees)}), "
                 f"{len(bruit)} refusal(s) on true sentences ({'; '.join(bruit)})")
    return len(plantes)


if __name__ == "__main__":
    try:
        n = compte_du_manifeste()
        plantes = temoin(n)
    except SystemExit as e:
        print(e)
        sys.exit(2)
    except (OSError, KeyError, ValueError) as e:
        print(f"GARDE CASSÉE (garde-listes): the manifest {MANIFESTE.name} does not read ({e})")
        sys.exit(2)
    docs = pathlib.Path(sys.argv[sys.argv.index("--docs") + 1]) if "--docs" in sys.argv else ICI.parent / "docs"
    fautes = fautes_du_site(docs, n)
    if fautes:
        print(f"LIST COUNTS REFUSED ({len(fautes)}):")
        for f in fautes[:40]:
            print("  " + f)
        sys.exit(1)
    print(f"  listes tenues : {MOTS.get(n, n)} sources, lues dans le manifeste de Screening "
          f"(témoin : {plantes} comptes plantés refusés, 3 phrases vraies passées)")
