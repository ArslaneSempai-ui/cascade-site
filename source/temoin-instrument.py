#!/usr/bin/env python3
"""LE TÉMOIN DE BOUT EN BOUT DES CINQ INSTRUMENTS VIVANTS (cartes du 9/09).

Il sert docs/ (127.0.0.1, port éphémère) et joue la sonde CDP sur les cinq pages :
la ligne tirée et le curseur sont UNE valeur, la grille reste dans le DOM peinte
par les chiffres du JSON, l'auto-contrôle passe, le caret s'arrête sous
prefers-reduced-motion, et chaque chiffre du panneau se retrouve dans le relevé
embarqué. Le viewport est FORCÉ à 1440×900 dans la sonde : le panneau caché du
navigateur intégré rend un viewport de 29 px et fausse tout test de survol.

Chrome doit tourner sur 9222 ; absent, le témoin REFUSE (code 3) au lieu de
rendre un vert qui n'a pas regardé. docs/ doit être assemblé : ce témoin regarde
LES PAGES SERVIES, celles que le lecteur reçoit.
"""
import http.server
import pathlib
import re
import subprocess
import sys
import threading
import urllib.request

BASE = pathlib.Path(__file__).parent
DOCS = BASE.parent / "docs"
# la phrase du what-if de l'onyx se LIT dans le module qui l'émet, jamais retapée :
# la passe de copy du 11/09 a changé « rhythm » en « validity period » et le témoin,
# qui portait la phrase en dur, a rougi sur une page juste — la troisième copie d'un
# fait ment toujours la première
def phrase_what_if():
    src = (BASE / "instrument_carte.py").read_text(encoding="utf-8")
    m = re.search(r'"(if the [a-z ]+ were) "', src)
    if not m:
        sys.exit("le témoin ne retrouve plus la phrase du what-if dans instrument_carte.py : "
                 "l'aligner ici plutôt que de croire un rouge ou un vert")
    return m.group(1)


PAGES = [
    ("instrument.html", "vert"),
    ("screening/instrument.html", "grille"),
    ("monitoring/instrument.html", "grille"),
    ("scoring/instrument.html", "grille"),
    ("dossier/instrument.html", "onyx"),
]

try:
    urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=2)
except OSError:
    sys.exit("runtime NON PROBÉ : Chrome n'écoute pas sur 9222 (le banc du chef le tient) ; "
             "un témoin qui n'a pas regardé ne rend pas de vert — code 3")

absentes = [p for p, _ in PAGES if not (DOCS / p).exists()]
if absentes:
    sys.exit(f"docs/ ne porte pas {absentes} : assembler d'abord (ce témoin regarde les pages servies)")

serveur = http.server.ThreadingHTTPServer(
    ("127.0.0.1", 0), lambda *a: http.server.SimpleHTTPRequestHandler(*a, directory=str(DOCS)))
port = serveur.server_address[1]
threading.Thread(target=serveur.serve_forever, daemon=True).start()

fautes = 0
try:
    for page, genre in PAGES:
        print(f"── {page} ({genre})")
        r = subprocess.run(["node", str(BASE / "temoin-instrument-sonde.mjs"),
                            f"http://127.0.0.1:{port}/{page}", genre, phrase_what_if()],
                           capture_output=True, text=True, timeout=120)
        print("\n".join("  " + l for l in (r.stdout.strip().splitlines() or ["(sonde muette)"])))
        if r.returncode != 0:
            fautes += 1
            if r.stderr.strip():
                print("  sonde stderr :", r.stderr.strip().splitlines()[-1][:140])
finally:
    serveur.shutdown()

if fautes:
    sys.exit(f"{fautes} page(s) rouge(s) : le détail est au-dessus, ligne par ligne")
print("témoin des instruments : cinq pages vertes, et il a regardé")
