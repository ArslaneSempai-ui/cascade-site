#!/usr/bin/env python3
"""LE TÉMOIN DES TARIFS (engagement.html en noir, trois colonnes, l'année en voies — 11/09).

Deux moitiés :
- STATIQUE, auto-témoignée par mutation : la structure décidée (trois .col dont la
  troisième .haute, robots, prix, CTA ; l'axe aux trois voies eval/camp/lic, les
  cartes .pap datées, le curseur-slider, l'état, « run the year », la note finale ;
  les disparus .chemin/.pas/.refus ABSENTS) et la COHÉRENCE des montants : les
  constantes du JS servi (LIC, CAMP) doivent être les montants écrits des cartes —
  un prix tapé qui divergerait de sa constante mentirait dans l'une des deux voix ;
- NAVIGATEUR (sonde CDP) : le compte-à-l'arrivée retombe sur l'écrit, le curseur
  répond au clavier, chaque montant de #etat dérive des constantes LUES du JS servi
  (9 000 et 21 000 ne sont écrits nulle part : calculés), et sans JavaScript le
  curseur et le bouton se cachent pendant que les cartes restent pleines.

Chrome absent sur 9222 : la moitié navigateur REFUSE (code 3), jamais un vert qui
n'a pas regardé. usage: python3 temoin-tarifs.py [--docs DIR] [--statique]
"""
import http.server
import pathlib
import re
import subprocess
import sys
import threading
import urllib.request

BASE = pathlib.Path(__file__).parent


def relever(html):
    fautes = []

    def dire(quoi):
        fautes.append(quoi)

    cols = re.findall(r'<div class="col( haute)?">', html)
    if len(cols) != 3 or not cols[2]:
        dire(f"trois colonnes attendues, la troisième .haute : vu {len(cols)} col(s), "
             f"haute={'oui' if cols and cols[-1] else 'non'}")
    for morceau, n_attendu in (('<img class="col-robot"', 3), ('class="c-prix"', 3), ('class="c-liste"', 3),
                               ('<a class="cta"', 3)):
        n = len(re.findall(re.escape(morceau), html))
        if n != n_attendu:
            dire(f"{morceau} : {n} au lieu de {n_attendu}")
    if len(re.findall(r'<a class="cta"[^>]*>.*?<span class="b">', html, re.S)) != 3:
        dire("chaque CTA doit porter son span.b")

    voies = re.findall(r'class="voie"[^>]*data-l="([a-z]+)"', html) or re.findall(r'data-l="([a-z]+)"[^>]*class="voie"', html)
    if sorted(set(voies) & {"eval", "camp", "lic"}) != ["camp", "eval", "lic"]:
        dire(f"l'axe doit porter les trois voies eval/camp/lic : vu {voies}")
    if 'id="axe"' not in html:
        dire("l'axe (#axe) est absent")
    n_pap = len(re.findall(r'class="pap[" ]', html))
    if n_pap < 3:
        dire(f"{n_pap} carte(s) .pap : l'année en veut plus")
    if not re.search(r'class="pap[^"]*"[^>]*style="[^"]*--d', html) and "--d" not in html:
        dire("les cartes .pap ne portent pas leur jour (--d)")
    for morceau in ('class="graduations"', 'class="regle"', 'id="etat"', 'id="courir"',
                    'class="note-fin"'):
        if morceau not in html:
            dire(f"{morceau} est absent")
    cur = re.search(r'id="curseur"[^>]*', html)
    if not cur:
        dire("le curseur (#curseur) est absent")
    elif 'role="slider"' not in cur.group(0) or "aria-valuenow" not in cur.group(0) or "tabindex" not in cur.group(0):
        dire("le curseur n'est pas un vrai slider clavier (role, aria-valuenow, tabindex)")

    for disparu in ("chemin", '"pas"', "refus-carte", 'class="refus"'):
        if disparu.strip('"') in ("chemin",) and re.search(r'class="chemin', html):
            dire("l'ancien .chemin vit encore")
    for vieux in (r'class="chemin', r'class="pas[" ]', r'class="refus'):
        if re.search(vieux, html):
            dire(f"un sélecteur disparu vit encore : {vieux}")

    # la cohérence constantes ↔ cartes : LIC et CAMP du JS servi sont les prix écrits
    m = re.search(r"const LIC = (\d+), PART = ([\d.]+), CAMP = (\d+)", html)
    if not m:
        dire("les constantes LIC/PART/CAMP sont introuvables dans le JS servi")
    else:
        lic, camp = int(m.group(1)), int(m.group(3))
        prix = [re.sub(r"<[^>]+>", "", p) for p in re.findall(r'<p class="c-prix"[^>]*>(.*?)</p>', html, re.S)]
        texte_prix = " ".join(prix)
        for nom, v in (("LIC", lic), ("CAMP", camp)):
            if f"${v:,}" not in texte_prix:
                dire(f"la constante {nom} (${v:,}) n'est pas le prix écrit d'une carte : "
                     "les deux voix divergent")
        for calcule in (round(lic * float(m.group(2))), round(lic * (1 - float(m.group(2))))):
            if f"${calcule:,}" in html:
                dire(f"${calcule:,} est ÉCRIT dans la page servie : il doit rester calculé, jamais tapé")
    return fautes


def temoin(html):
    intacte = relever(html)
    if intacte:
        return intacte
    mutations = [
        (html.replace("const LIC = 30000", "const LIC = 31000"), "divergent", "la constante muée"),
        (html.replace('class="voie"', 'class="voix"', 1), "voies", "la voie retirée"),
        (html.replace('<div class="col haute">', '<div class="col">'), "haute", "la troisième colonne abaissée"),
        (html.replace("</main>", '<p class="refus-carte">x</p></main>') if "</main>" in html
         else html + '<p class="refus-carte">x</p>', "disparu", "l'ancien refus replanté"),
    ]
    for mue, attendu, nom in mutations:
        if not any(attendu in f for f in relever(mue)):
            sys.exit(f"GARDE CASSÉE : {nom} ne rougit plus (aucune faute ne parle de "
                     f"« {attendu} ») — aucun relevé n'est rendu (code 2)")
    return []


if __name__ == "__main__":
    docs = pathlib.Path(sys.argv[sys.argv.index("--docs") + 1]) if "--docs" in sys.argv else BASE.parent / "docs"
    html = (docs / "engagement.html").read_text(encoding="utf-8")
    fautes = temoin(html)
    if fautes:
        for f in fautes:
            print("  ROUGE", f)
        sys.exit(f"{len(fautes)} refus : la page des tarifs ne tient pas sa structure")
    print("  statique : structure tenue, constantes = prix écrits, montants dérivés jamais tapés, "
          "quatre mutations rougissent")
    if "--statique" in sys.argv:
        print("témoin des tarifs : moitié statique seule (--statique), dit")
        sys.exit(0)
    try:
        urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=2)
    except OSError:
        sys.exit("runtime NON PROBÉ : Chrome n'écoute pas sur 9222 ; un témoin qui n'a pas "
                 "regardé ne rend pas de vert — code 3 (ou relancer avec --statique, dit)")
    serveur = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), lambda *a: http.server.SimpleHTTPRequestHandler(*a, directory=str(docs)))
    port = serveur.server_address[1]
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    try:
        import html as _html
        import json as _json
        statiques = [re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", p))).strip()
                     for p in re.findall(r'<p class="c-prix"[^>]*>(.*?)</p>', html, re.S)]
        r = subprocess.run(["node", str(BASE / "temoin-tarifs-sonde.mjs"),
                            f"http://127.0.0.1:{port}/engagement.html", _json.dumps(statiques)],
                           capture_output=True, text=True, timeout=120)
        print("\n".join("  " + l for l in r.stdout.strip().splitlines()))
        if r.returncode != 0:
            if r.stderr.strip():
                print("  sonde stderr :", r.stderr.strip().splitlines()[-1][:140])
            sys.exit("la moitié navigateur est rouge : le détail est au-dessus")
    finally:
        serveur.shutdown()
    print("témoin des tarifs : les deux moitiés vertes, et il a regardé")
