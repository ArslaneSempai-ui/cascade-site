#!/usr/bin/env python3
"""THE ADDRESS GUARD (Crusetra, waves 2 and 3, 6 October 2026).

The served site names one domain, one contact address, and our repositories under their GitHub
names. All of them are written once, in outil.py (DOMAINE, SITE_URL, CONTACT, GITHUB, DEPOTS,
DEPOT_SITE); the content JSON may still type the address in prose, and this guard is what keeps
those typed copies equal to the constant.

It refuses, file by file and line by line, in every served text file (html, css, js, json, xml,
txt, svg, CNAME, .well-known/security.txt):
  1. the former domain cascade-routing.com, in any case (the former address included);
  2. a repository link or Pages address that names a repository outside DEPOTS and DEPOT_SITE
     (the former cascade-routing, cascade-screening... included), and the former clone folder
     `cd cascade-<tool>`;
  3. an e-mail address other than CONTACT;
  4. a link to our own domain that does not start with SITE_URL (http://, www.);
  5. a CNAME file that does not hold DOMAINE alone.
In the PDFs it reads the bytes: the former domain, and every mailto: or link annotation.

Its own witness runs first, in process: a planted text carrying each fault must be refused by the
matching rule, and a clean text must pass. Otherwise it exits 2: a broken guard's zero means
nothing. The assembler adds the outer witness (a planted page in docs/ must turn it red).

  python3 garde-adresses.py --docs ../docs      exit 0 clean, 1 refused, 2 broken guard
"""
import pathlib
import re
import sys

ICI = pathlib.Path(__file__).parent
sys.path.insert(0, str(ICI))
from outil import DOMAINE, SITE_URL, CONTACT, GITHUB, DEPOTS, DEPOT_SITE  # noqa: E402

ANCIEN_DOMAINE = re.compile(r"cascade-routing\.com", re.I)
_PROPRIETAIRE = re.escape(GITHUB.removeprefix("https://").split("/")[1])   # ArslaneSempai-ui
DEPOT = re.compile(r"github\.com/" + _PROPRIETAIRE + r"/([A-Za-z0-9_.-]+)", re.I)
PAGES = re.compile(_PROPRIETAIRE + r"\.github\.io/([A-Za-z0-9_.-]+)", re.I)
ANCIEN_CLONE = re.compile(r"\bcd\s+cascade-(?:routing|screening|monitoring|scoring|dossier)\b", re.I)
ADRESSE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
NOTRE_URL = re.compile(r"(?:https?:)?//(?:www\.)?" + re.escape(DOMAINE) + r"\b[^\s\"'<>)]*", re.I)
PERMIS = set(DEPOTS.values()) | {DEPOT_SITE}
# the former names are refused even if outil.py were set back to them: the guard does not take
# its whole truth from the file it guards
ANCIENS_DEPOTS = {f"cascade-{o}" for o in ("routing", "screening", "monitoring", "scoring", "dossier")}
TEXTES = {".html", ".css", ".js", ".mjs", ".json", ".xml", ".txt", ".svg", ".webmanifest", ""}
# an asset name such as robot@2x.png reads as an address to the pattern; none ships today, and
# the exception stays narrow: an image or font extension after the @ part is not a mail domain
_PAS_UN_COURRIEL = re.compile(r"\.(?:png|jpe?g|webp|gif|svg|avif|woff2?|css|js)$", re.I)


def fautes_du_texte(nom, texte):
    """The refusals of one served text, as (rule, "name:line: excerpt")."""
    fautes = []
    for n, ligne in enumerate(texte.splitlines(), 1):
        ou = f"{nom}:{n}"
        for m in ANCIEN_DOMAINE.finditer(ligne):
            fautes.append((1, f"{ou}: former domain « {m.group(0)} »"))
        for motif in (DEPOT, PAGES):
            for m in motif.finditer(ligne):
                depot = m.group(1).removesuffix(".git")
                if depot not in PERMIS or depot in ANCIENS_DEPOTS:
                    fautes.append((2, f"{ou}: repository « {m.group(0)} » is not one of {sorted(PERMIS)}"))
        for m in ANCIEN_CLONE.finditer(ligne):
            fautes.append((2, f"{ou}: former clone folder « {m.group(0)} »"))
        for m in ADRESSE.finditer(ligne):
            a = m.group(0)
            if a != CONTACT and not _PAS_UN_COURRIEL.search(a):
                fautes.append((3, f"{ou}: address « {a} » is not {CONTACT}"))
        for m in NOTRE_URL.finditer(ligne):
            if not m.group(0).startswith(SITE_URL.rstrip("/")):
                fautes.append((4, f"{ou}: « {m.group(0)} » does not start with {SITE_URL}"))
    return fautes


def fautes_du_pdf(nom, octets):
    fautes = []
    for m in re.finditer(rb"cascade-routing\.com", octets, re.I):
        fautes.append((1, f"{nom}@{m.start()}: former domain in the PDF bytes"))
    for m in re.finditer(rb"/URI\s*\(([^)]*)\)", octets):
        uri = m.group(1).decode("latin-1")
        if uri.startswith("mailto:") and uri.removeprefix("mailto:").split("?")[0] != CONTACT:
            fautes.append((3, f"{nom}: link annotation « {uri} » is not mailto:{CONTACT}"))
        for f in fautes_du_texte(nom, uri):
            fautes.append(f)
    return fautes


def fautes_du_site(docs):
    fautes = []
    for f in sorted(p for p in docs.rglob("*") if p.is_file()):
        nom = str(f.relative_to(docs))
        if f.suffix.lower() == ".pdf":
            fautes += fautes_du_pdf(nom, f.read_bytes())
        elif f.suffix.lower() in TEXTES:
            try:
                texte = f.read_text()
            except UnicodeDecodeError:
                continue
            fautes += fautes_du_texte(nom, texte)
    cname = docs / "CNAME"
    if not SITE_URL.removeprefix("https://").rstrip("/").endswith(".github.io"):
        if not cname.exists():
            fautes.append((5, f"CNAME absent: the custom domain {DOMAINE} would not be declared"))
        elif cname.read_text() != DOMAINE + "\n":
            fautes.append((5, f"CNAME holds « {cname.read_text().strip()} », not {DOMAINE}"))
    return fautes


def temoin():
    """Each planted fault, one per line, must be refused by its own rule; a clean text must pass."""
    plantes = [("<a href=\"mailto:contact@cascade-routing.com\">x</a>", 1),
               ("<p>see crusetra.com or CASCADE-ROUTING.COM</p>", 1),
               ("<a href=\"https://github.com/ArslaneSempai-ui/cascade-screening\">x</a>", 2),
               ("<a href=\"https://github.com/ArslaneSempai-ui/some-other-repo\">x</a>", 2),
               ("<a href=\"https://arslanesempai-ui.github.io/cascade-routing/\">x</a>", 2),
               ("<code>cd cascade-routing</code>", 2),
               ("<p>write to someone@example.org</p>", 3),
               (f"<a href=\"http://www.{DOMAINE}/pricing\">x</a>", 4)]
    manquees = [ligne for ligne, regle in plantes
                if regle not in {r for r, _ in fautes_du_texte("temoin", ligne)}]
    propre = (f"<a href=\"mailto:{CONTACT}\">{CONTACT}</a> "
              f"<a href=\"{GITHUB}{DEPOTS['routing']}/issues\">x</a> <code>cd {DEPOTS['routing']}</code> "
              f"<a href=\"{GITHUB}{DEPOTS['dossier']}.git\">x</a> "
              f"<a href=\"{SITE_URL}engagement.html\">x</a> <img src=\"robot@2x.png\">")
    bruit = fautes_du_texte("temoin", propre)
    if not fautes_du_pdf("temoin.pdf", b"/URI (mailto:contact@cascade-routing.com)>>"):
        manquees.append("PDF: mailto of the former address")
    if not fautes_du_pdf("temoin.pdf", b"/URI (mailto:someone@example.org)>>"):
        manquees.append("PDF: mailto of a foreign address")
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        (pathlib.Path(d) / "CNAME").write_text("cascade-routing.com\n")
        if 5 not in {r for r, _ in fautes_du_site(pathlib.Path(d))}:
            manquees.append("CNAME of the former domain")
    if manquees or bruit:
        sys.exit(f"GARDE CASSÉE (garde-adresses): {len(manquees)} planted fault(s) passed "
                 f"({'; '.join(manquees)}), {len(bruit)} refusal(s) on the clean text")


if __name__ == "__main__":
    try:
        temoin()
    except SystemExit as e:
        print(e)
        sys.exit(2)
    docs = pathlib.Path(sys.argv[sys.argv.index("--docs") + 1]) if "--docs" in sys.argv else ICI.parent / "docs"
    fautes = fautes_du_site(docs)
    if fautes:
        print(f"ADDRESSES REFUSED ({len(fautes)}):")
        for _, f in fautes[:60]:
            print("  " + f)
        sys.exit(1)
    print(f"  adresses tenues : {DOMAINE}, {CONTACT}, {len(PERMIS)} dépôts permis, CNAME {DOMAINE} "
          f"(témoin : 11 fautes plantées, chacune refusée par sa règle)")
