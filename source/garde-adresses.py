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
  5. a CNAME file that does not hold DOMAINE alone;
  6. a path of the machine the site was built on (/Users/<name>, /home/<name>, ~/Documents, a
     macOS temp folder): the site names the public repositories, never where a folder sits here;
  7. a `git clone <repository>` followed by another command before `cd <repository>`: npm ci would
     then run outside the clone (V4, 6 October 2026: ten blocks had it).
Rule 2 also refuses a former repository name written bare, outside any link (« (releve-entites.json,
cascade-screening) » in the served releve.json until V4).
In the PDFs it reads the bytes: the former domain, a machine path, and every mailto: or link annotation.

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
ANCIEN_NOM = re.compile(r"\bcascade-(?:routing|screening|monitoring|scoring|dossier|site)\b", re.I)
CHEMIN_LOCAL = re.compile(r"/Users/[^/\s\"'<>]+|/home/[^/\s\"'<>]+/|~/Documents\b|/(?:private/)?var/folders/", re.I)
CLONE = re.compile(r"\bgit clone\s+(\S+)")
COMMANDE = re.compile(r"(?:^|[\s$>;&|(])(cd|npm|npx|node|python3?|zsh|bash|sh)\s+(\S+)")
ADRESSE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
NOTRE_URL = re.compile(r"(?:https?:)?//(?:www\.)?" + re.escape(DOMAINE) + r"\b[^\s\"'<>)]*", re.I)
PERMIS = set(DEPOTS.values()) | {DEPOT_SITE}
# the former names are refused even if outil.py were set back to them: the guard does not take
# its whole truth from the file it guards
ANCIENS_DEPOTS = {f"cascade-{o}" for o in ("routing", "screening", "monitoring", "scoring", "dossier", "site")}
N_PLANTEES = 0
TEXTES = {".html", ".css", ".js", ".mjs", ".json", ".xml", ".txt", ".svg", ".webmanifest", ""}
# an asset name such as robot@2x.png reads as an address to the pattern; none ships today, and
# the exception stays narrow: an image or font extension after the @ part is not a mail domain
_PAS_UN_COURRIEL = re.compile(r"\.(?:png|jpe?g|webp|gif|svg|avif|woff2?|css|js)$", re.I)


def _texte_lu(texte):
    """The text a reader sees, tags turned to spaces (each newline inside a tag kept, so the line
    numbers still match the file) and entities decoded: `&amp;&amp; cd x` reads as `&& cd x`."""
    import html as _html
    sans = re.sub(r"<[^>]*>", lambda m: " " + "\n" * m.group(0).count("\n"), texte)
    return _html.unescape(sans)


def fautes_des_clones(nom, texte):
    """Rule 7: after each `git clone <url>`, the first command must be `cd <repository>`."""
    fautes = []
    lu = _texte_lu(texte)
    for m in CLONE.finditer(lu):
        depot = m.group(1).rstrip("/").rsplit("/", 1)[-1].removesuffix(".git")
        suite = COMMANDE.search(lu[m.end():m.end() + 400])
        if suite and not (suite.group(1) == "cd" and suite.group(2).rstrip("/") == depot):
            ligne = lu.count("\n", 0, m.start()) + 1
            fautes.append((7, f"{nom}:{ligne}: « git clone {m.group(1)} » is followed by « {suite.group(1)} {suite.group(2)} » "
                              f"before « cd {depot} »"))
    return fautes


def fautes_du_texte(nom, texte):
    """The refusals of one served text, as (rule, "name:line: excerpt")."""
    fautes = fautes_des_clones(nom, texte)
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
        for m in ANCIEN_NOM.finditer(ligne):
            fautes.append((2, f"{ou}: former repository name « {m.group(0)} »"))
        for m in CHEMIN_LOCAL.finditer(ligne):
            fautes.append((6, f"{ou}: machine path « {m.group(0)} »"))
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
    for m in re.finditer(rb"/Users/|~/Documents|/var/folders/", octets):
        fautes.append((6, f"{nom}@{m.start()}: machine path in the PDF bytes"))
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
               (f"<a href=\"http://www.{DOMAINE}/pricing\">x</a>", 4),
               ("\"16\": \"scellé 68157020f83b6741 (releve-entites.json, cascade-screening)\"", 2),
               ("\"859\": \"README.md:265 de ~/Documents/cascade\"", 6),
               ("<p>built in /Users/Someone/Documents/x</p>", 6),   # capital S: the pre-push hook refuses /Users/[a-z]
               (f"<code>git clone {GITHUB}{DEPOTS['screening']}.git</code><code>npm ci --ignore-scripts</code>", 7),
               (f"<code class=\"ln\">git clone {GITHUB}{DEPOTS['dossier']}</code>\n<code class=\"ln\">cd {DEPOTS['routing']}</code>", 7)]
    manquees = [ligne for ligne, regle in plantes
                if regle not in {r for r, _ in fautes_du_texte("temoin", ligne)}]
    propre = (f"<a href=\"mailto:{CONTACT}\">{CONTACT}</a> "
              f"<a href=\"{GITHUB}{DEPOTS['routing']}/issues\">x</a> <code>cd {DEPOTS['routing']}</code> "
              f"<a href=\"{GITHUB}{DEPOTS['dossier']}.git\">x</a> "
              f"<a href=\"{SITE_URL}engagement.html\">x</a> <img src=\"robot@2x.png\"> "
              f"<div><span>$</span> git clone {GITHUB}{DEPOTS['screening']}.git</div>\n<div><span>$</span> cd {DEPOTS['screening']}</div>"
              f"<div><span>$</span> npm ci --ignore-scripts</div> <dd>node src/premiere-reponse.mjs</dd>"
              f"<small>git clone {GITHUB}{DEPOTS['routing']} &amp;&amp; cd {DEPOTS['routing']}</small> "
              f"<code>CASCADE_OFFLINE=1</code> <p>~/.cascade, the former marker</p>")
    bruit = fautes_du_texte("temoin", propre)
    if not fautes_du_pdf("temoin.pdf", b"/URI (mailto:contact@cascade-routing.com)>>"):
        manquees.append("PDF: mailto of the former address")
    if not fautes_du_pdf("temoin.pdf", b"/URI (mailto:someone@example.org)>>"):
        manquees.append("PDF: mailto of a foreign address")
    if 6 not in {r for r, _ in fautes_du_pdf("temoin.pdf", b"/Title (file:///Users/Someone/x.html)")}:
        manquees.append("PDF: machine path")
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        (pathlib.Path(d) / "CNAME").write_text("cascade-routing.com\n")
        if 5 not in {r for r, _ in fautes_du_site(pathlib.Path(d))}:
            manquees.append("CNAME of the former domain")
    global N_PLANTEES
    N_PLANTEES = len(plantes) + 4
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
          f"(témoin : {N_PLANTEES} fautes plantées, chacune refusée par sa règle)")
