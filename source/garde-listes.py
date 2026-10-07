#!/usr/bin/env python3
"""THE LIST-COUNT GUARD (Crusetra V4, 6 October 2026).

On 5 October Screening went from seven public sanctions sources to ten (the sources-plus merge,
crusetra-screening 27e7fac), and nine sentences of the served site still said seven. The count is
not ours to type: it is the number of lists in the tool's committed manifest
(listes-manifest.json), and this guard reads it there.

It refuses, in every served page, a count of lists or sources (« seven sanctions lists », « 7 public
sources », « the seven sources ») that is not the manifest's. A dated count passes: « the seven
sources of 4 October » describes a record screened on that day's lists, and says so.

The other tools' folders, their annexes and the Routing sample count other things (« 8 sources on
3 fields » is Routing's). Until 7 October 2026 they were skipped whole, so « Crusetra Screening reads
seven sanctions lists. » planted on routing/index.html passed. They are read now: there, a count is
about Screening's lists when its sentence names sanctions or Screening, and then it must agree with
the manifest as well.

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
# the other tools' pages, the Routing annexes and the Routing sample count other things (« 8 sources on
# 3 fields » is Routing's): there, only a count whose sentence names sanctions or Screening is read
AUTRES = ("routing/", "monitoring/", "scoring/", "dossier/", "rapports/routing", "method.html", "security.html",
          "instrument.html")
DES_LISTES = re.compile(r"\b(?:sanction|screening)", re.I)
# a sentence ends at a stop or at a block element: the menu's « Screening » is not in the next heading
BLOC = re.compile(r"</?(?:p|h[1-6]|li|ul|ol|dl|dt|dd|td|th|tr|table|div|section|article|header|footer|nav|aside|"
                  r"main|figure|figcaption|blockquote|pre|br|summary|details|title)\b[^>]*>", re.I)
FIN = re.compile("[.!?](?=\\s|$)|\u2029")


def compte_du_manifeste():
    listes = json.loads(MANIFESTE.read_text())["listes"]
    return len(listes)


def lu(texte, blocs=False):
    """The text a reader sees, line for line. With blocs, a block element's tag becomes U+2029 instead of a
    space: the same length, so a position in one text is the same position in the other."""
    sans = re.sub(r"<(script|style)\b.*?</\1>", lambda m: "\n" * m.group(0).count("\n"), texte, flags=re.S | re.I)
    sans = re.sub(r"<[^>]*>", lambda m: ("\u2029" if blocs and BLOC.fullmatch(m.group(0)) else " ")
                  + "\n" * m.group(0).count("\n"), sans)
    return html.unescape(sans)


def phrase(tb, m):
    """The sentence that holds the match, in the text read with blocs: from the previous stop to the next."""
    debut = max([f.end() for f in FIN.finditer(tb, 0, m.start())] or [0])
    fin = FIN.search(tb, m.end())
    return tb[debut:fin.end() if fin else len(tb)]


def fautes_du_texte(nom, texte, n, autre_outil=False):
    fautes = []
    t = lu(texte)
    tb = lu(texte, blocs=True) if autre_outil else t
    for m in COMPTE.finditer(t):
        mot = m.group(1).lower()
        dit = int(mot) if mot.isdigit() else NOMBRES[mot]
        if dit == n or DATE.match(t, m.end()):
            continue
        if autre_outil and not DES_LISTES.search(phrase(tb, m)):
            continue
        ligne = t.count("\n", 0, m.start()) + 1
        fautes.append(f"{nom}:{ligne}: « {' '.join(m.group(0).split())} », the manifest holds {MOTS.get(n, n)} lists")
    return fautes


def fautes_du_site(docs, n):
    fautes = []
    for f in sorted(docs.rglob("*.html")):
        nom = str(f.relative_to(docs))
        fautes += fautes_du_texte(nom, f.read_text(), n, autre_outil=nom.startswith(AUTRES))
    return fautes


def temoin(n):
    faux = MOTS[n - 3] if n > 3 else "twelve"
    plantes = [f"<h2>Your names, screened against {faux} sanctions lists.</h2>",
               f"<p>We screen it against {n + 1} public sources and send back a PDF.</p>",
               f"<li>The dates of the {faux} sources, and a seal</li>"]
    saines = [f"<p>We screen each name against {MOTS.get(n, n)} public sources: OFAC SDN and the others.</p>",
              f"<p>1,000 invented counterparties, screened against the {faux} sources of 4 October: lit marks.</p>",
              "<p>Crusetra Screening compares names seven ways, at every threshold.</p>"]
    # on another tool's page: a sentence about Screening's lists is read, Routing's own counts are not
    plantes_ailleurs = [f"<p>Crusetra Screening reads {faux} sanctions lists.</p>",
                        f"<p>The names go to Screening, which checks {n + 1} public sources.</p>"]
    saines_ailleurs = ["<nav><a>Routing</a> <a>Screening</a></nav><h2>Two sources, one set of cases</h2>",
                       "<p>Measured with tool commit 7e82950, 8 sources on 3 fields.</p>",
                       "<p>Two sources are compared on the same cases.</p>",
                       f"<p>Screening reads {MOTS.get(n, n)} sanctions lists.</p>"]
    manquees = ([p for p in plantes if not fautes_du_texte("temoin", p, n)]
                + [p for p in plantes_ailleurs if not fautes_du_texte("routing/temoin", p, n, autre_outil=True)])
    bruit = ([s for s in saines if fautes_du_texte("temoin", s, n)]
             + [s for s in saines_ailleurs if fautes_du_texte("routing/temoin", s, n, autre_outil=True)])
    if manquees or bruit:
        sys.exit(f"GARDE CASSÉE (garde-listes): {len(manquees)} planted count(s) passed ({'; '.join(manquees)}), "
                 f"{len(bruit)} refusal(s) on true sentences ({'; '.join(bruit)})")
    return len(plantes) + len(plantes_ailleurs), len(saines) + len(saines_ailleurs)


if __name__ == "__main__":
    try:
        n = compte_du_manifeste()
        plantes, saines = temoin(n)
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
    print(f"  listes tenues : {MOTS.get(n, n)} sources, lues dans le manifeste de Screening, sur toutes les "
          f"pages servies (témoin : {plantes} comptes plantés refusés, {saines} phrases vraies passées)")
