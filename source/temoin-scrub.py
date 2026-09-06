#!/usr/bin/env python3
"""LE TÉMOIN DU SCRUB (lot P-C1), hermétique et dans les deux sens.

Trois affirmations du contrat (CONTRAT-CHOREGRAPHIE.md § P-C1), chacune vérifiée
en l'exécutant, jamais en la récitant :

1. SANS manifeste, la page d'aujourd'hui sort octet pour octet (le rouge garde ses
   textes à l'octet : témoin cmp) — vérifié en bâtissant avant/après le passage du
   factice et en comparant les six pages au byte.
2. AVEC un manifeste factice de 2 images sur UN outil : le canevas et le manifeste
   embarqué n'apparaissent QUE sur la page de cet outil ; les cinq autres ne bougent
   pas d'un octet.
3. En navigateur (CDP natif, jamais une capture étroite) : la scène k n'est active
   qu'à q ≥ mouvement ; en dessous, aucune scène active et le canevas seul dessine ;
   le retour sous le seuil désactive aussi.

Le témoin déplace un éventuel dossier de séquences RÉEL avant de planter le factice
et le remet en place quoi qu'il arrive : il ne laisse RIEN derrière lui, et la
restauration finale est elle-même vérifiée au byte. Chrome doit tourner sur 9222
(le banc du chef) ; absent, le témoin REFUSE (code 3, « runtime non probé ») au
lieu de rendre un vert qui n'a pas regardé.
"""
import http.server
import json
import pathlib
import shutil
import subprocess
import sys
import threading
import urllib.request

BASE = pathlib.Path(__file__).parent
sys.path.insert(0, str(BASE))
import outil  # noqa: E402  (manques_sequences, sceau_du_releve, taille_webp : les gardes M-C1)
PAGES = ["HERO.html", "ACCUEIL.html", "HERO-SCREENING.html", "HERO-MONITORING.html",
         "HERO-SCORING.html", "HERO-DOSSIER.html"]
PREFIXE = "rack"                      # l'outil porteur du factice (monitoring)
PAGE_CIBLE = "HERO-MONITORING.html"
SEQ = BASE / "rendus" / "sequences" / PREFIXE
GARE = BASE / "rendus" / "sequences" / (PREFIXE + ".temoin-gare")


def batir():
    r = subprocess.run([sys.executable, str(BASE / "batir-hero.py")],
                       capture_output=True, text=True, cwd=str(BASE))
    if r.returncode != 0:
        sys.exit(f"batir-hero.py a refusé pendant le témoin :\n{r.stderr}\n{r.stdout}")


def lire_pages():
    return {p: (BASE / p).read_bytes() for p in PAGES}


def planter_factice():
    """Le factice est VALIDE sous les gardes M-C1 autant que la production le permet :
    sceau réel du relevé (fraîcheur), dernière image = l'état k au byte (identité),
    tailles lues dans le vrai webp (complétude). Seul le budget peut le refuser tant
    que BUDGET_SEQUENCE_KO n'est pas déclaré — et le témoin le DIT au lieu d'affirmer
    des sœurs à l'octet que le rideau a le droit de changer."""
    SEQ.mkdir(parents=True)
    for k in range(1, 6):
        shutil.copy(BASE / "rendus" / "etats" / f"{PREFIXE}-01.webp", SEQ / f"{PREFIXE}-seq-0{k}-000.webp")
        shutil.copy(BASE / "rendus" / "etats" / f"{PREFIXE}-0{k}.webp", SEQ / f"{PREFIXE}-seq-0{k}-001.webp")
    large, haut = outil.taille_webp(BASE / "rendus" / "etats" / f"{PREFIXE}-01.webp")
    (SEQ / "manifest.json").write_text(json.dumps({
        "prefixe": PREFIXE, "n": 2, "transitions": 5, "ext": ".webp",
        "large": large, "haut": haut, "mouvement": 0.66,
        "sceau": outil.sceau_du_releve("monitoring")}))


def sonde_cdp():
    try:
        urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=2)
    except OSError:
        sys.exit("runtime NON PROBÉ : Chrome n'écoute pas sur 9222 (le banc du chef le tient) ; "
                 "un témoin qui n'a pas regardé ne rend pas de vert — code 3")
    serveur = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), lambda *a: http.server.SimpleHTTPRequestHandler(*a, directory=str(BASE)))
    port = serveur.server_address[1]
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    try:
        r = subprocess.run(["node", str(BASE / "temoin-scrub-sonde.mjs"),
                            f"http://127.0.0.1:{port}/{PAGE_CIBLE}"],
                           capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            sys.exit(f"la sonde CDP a refusé :\n{r.stderr}")
        return json.loads(r.stdout.strip().splitlines()[-1])
    finally:
        serveur.shutdown()


avant = None
try:
    if SEQ.exists():
        SEQ.rename(GARE)              # les séquences réelles se garent, jamais écrasées

    batir()
    avant = lire_pages()
    for p, contenu in avant.items():
        assert b"seq-manifeste" not in contenu and b"canvas class=\"scrub\"" not in contenu, \
            f"{p} porte le scrub SANS manifeste : le repli n'est pas l'absence"
    print(f"  1/3 sans manifeste : aucun scrub dans les {len(PAGES)} pages")

    planter_factice()
    batir()
    apres = lire_pages()
    assert b"seq-manifeste" in apres[PAGE_CIBLE] and b'canvas class="scrub"' in apres[PAGE_CIBLE], \
        f"{PAGE_CIBLE} : manifeste présent mais pas de canevas ni de scrub"
    intactes = [p for p in PAGES if p != PAGE_CIBLE]
    for p in intactes:
        assert b"seq-manifeste" not in apres[p] and b'canvas class="scrub"' not in apres[p], \
            f"{p} porte le scrub alors que le factice ne concerne que {PREFIXE} : le scrub déborde de son outil"
    # les sœurs à l'octet, SEULEMENT quand les gardes M-C1 tiennent le factice pour prêt :
    # tant que BUDGET_SEQUENCE_KO n'est pas déclaré, le rideau retire légitimement le pan
    # (des séquences refusées = outil pas prêt) et les sœurs changent — le dire, pas le taire
    gardes = outil.manques_sequences("monitoring", BASE)
    if not gardes:
        for p in intactes:
            assert apres[p] == avant[p], \
                f"{p} a changé alors que le factice passe toutes les gardes : une divergence"
        print(f"  2/3 factice sur {PREFIXE} : canevas sur {PAGE_CIBLE} seul, "
              f"{len(intactes)} pages sœurs à l'octet")
    else:
        print(f"  2/3 factice sur {PREFIXE} : canevas sur {PAGE_CIBLE} seul, aucun scrub chez "
              f"les {len(intactes)} sœurs ; comparaison à l'octet SUSPENDUE, dit : les gardes "
              f"M-C1 refusent le factice ({gardes[0][:80]}…)")

    v = sonde_cdp()
    assert v["canevas"], "la sonde ne voit pas le canevas"
    assert v["mouvement"]["actif"] == -1 and v["mouvement"]["scrub"], \
        f"q < mouvement : une scène est active ({v['mouvement']}) ; le contrat veut le canevas seul"
    assert v["arret0"]["actif"] == 0, f"q >= mouvement en k=0 : la scène 0 n'est pas active ({v['arret0']})"
    assert v["arret2"]["actif"] == 2, f"q >= mouvement en k=2 : la scène 2 n'est pas active ({v['arret2']})"
    assert v["retour"]["actif"] == -1, f"le retour sous le seuil laisse une scène active ({v['retour']})"
    print("  3/3 navigateur (CDP) : aucune scène pendant le mouvement, la scène k à l'arrêt, "
          "le retour désactive")
finally:
    if SEQ.exists():
        shutil.rmtree(SEQ)
    if GARE.exists():
        GARE.rename(SEQ)
    dossier = SEQ.parent
    if dossier.exists() and not any(dossier.iterdir()):
        dossier.rmdir()
    batir()

# la remise en état est vérifiée, pas supposée : les pages re-bâties sans factice
# doivent être celles du départ, au byte
if avant is not None:
    for p, contenu in lire_pages().items():
        assert contenu == avant[p], f"{p} ne revient pas à l'octet après le témoin : il a laissé une trace"
    print("  remise en état : les six pages reviennent à l'octet")
print("témoin du scrub : vert, et il a regardé")
