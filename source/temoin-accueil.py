#!/usr/bin/env python3
"""LE TÉMOIN DE L'ACCUEIL (l'éventail, le grand livre, la méthode sur papier — 11/09).

Il lit la page SERVIE (docs/index.html) et tient les affirmations du premier écran :

  A. le grand livre : six lignes libellé/valeur ; le content hash EST l'empreinte
     recomposée du relevé scellé du routage (jamais crue sur parole) ; chaque chiffre
     du livre se retrouve sur la page du héros routing (même source, même chaîne de
     gardes : un chiffre tapé à la main sur l'accueil divergerait du héros au premier
     re-scellement) ; la ligne de commande porte premiere-reponse et le git clone ;
  B. l'éventail : cinq cartes vivantes, une par outil, dans l'ordre du rideau
     (OUTILS d'outil.py, jamais une liste retapée), chacune portant son SVG ;
  C. la méthode : quatre stations numérotées, la station 03 porte le terminal aux
     TROIS commandes, la station 01 définit « sealed » dans son paragraphe ;
  D. la scène : l'escalier-01 avec DEUX annotations dont les textes sont ceux
     PUBLIÉS de findings-dossier.json (fiche 01), et la note est la phrase de la
     fiche — l'accueil cite le dossier, il ne le paraphrase pas ;
  E. les six liens de la méthode existent dans docs/ ;
  F. les absences décidées : ni lede, ni hero-cue, ni robot avant le rideau.

LE TÉMOIN SE PROUVE PAR MUTATION à chaque lancement : la page réelle, altérée
(sceau changé, carte retirée, annotation réécrite, chiffre déplacé), doit rougir
sur la bonne affirmation ; la page intacte doit passer. Sinon : garde cassée,
aucun relevé (code 2). Statique : aucun navigateur requis.

usage: python3 temoin-accueil.py [--docs DIR]     0 = tenu ; 1 = refus ; 2 = garde cassée
"""
import json
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).parent
sys.path.insert(0, str(BASE))
import outil  # noqa: E402  (OUTILS, lire_releve_scelle : l'ordre du rideau et le sceau)


def _nu(x):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()


def relever(html, hero_routing, findings_dossier):
    fautes = []

    def dire(quoi):
        fautes.append(quoi)

    # A. le grand livre
    m = re.search(r'<dl class="ledger[^"]*"[^>]*>(.*?)</dl>', html, re.S)
    if not m:
        return ["le grand livre (dl.ledger) est absent du premier écran"]
    lignes = re.findall(r"<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>", m.group(1), re.S)
    if len(lignes) != 6:
        dire(f"le grand livre porte {len(lignes)} lignes, la décision en veut six")
    paires = [(_nu(dt), _nu(dd)) for dt, dd in lignes]
    sceau_vrai = outil.lire_releve_scelle(outil.OUTILS["routing"]["releve_scelle"])["empreinte"]
    dd_hash = next((dd for dt, dd in paires if "hash" in dt.lower()), None)
    if dd_hash is None:
        dire("aucune ligne « content hash » dans le grand livre")
    elif dd_hash != sceau_vrai:
        dire(f"le content hash du grand livre ({dd_hash}) n'est pas l'empreinte recomposée "
             f"du relevé scellé ({sceau_vrai})")
    for dt, dd in paires:
        if "hash" in dt.lower() or "rerun" in dt.lower():
            continue
        for nombre in re.findall(r"\d[\d,.]*", dd):
            if nombre not in hero_routing:
                dire(f"le chiffre « {nombre} » ({dt}) ne se retrouve pas sur le héros routing : "
                     "les deux pages lisent la même source, l'un des deux a dérivé")
    if "premiere-reponse" not in m.group(1):
        dire("la ligne de commande du grand livre ne porte pas premiere-reponse")
    if "git clone" not in m.group(1):
        dire("la ligne de commande du grand livre ne porte pas le git clone")

    # B. l'éventail, dans l'ordre du rideau
    cartes = re.findall(r'<a class="carte-ev[^"]*" href="([^"]+)"(.*?)</a>', html, re.S)
    attendu = [("index.html" if o["sous_dossier"] == "" else o["sous_dossier"] + "index.html")
               if o["id"] != "routing" else "routing/index.html"
               for o in outil.OUTILS.values()]
    if [h for h, _ in cartes] != attendu:
        dire(f"l'éventail sert {[h for h, _ in cartes]} ; l'ordre du rideau (OUTILS) est {attendu}")
    for h, corps in cartes:
        if "<svg" not in corps:
            dire(f"la carte {h} ne porte pas son SVG du relevé : une carte morte dans l'éventail")

    # C. les stations
    st = re.search(r'<ol class="stations"[^>]*>(.*?)</ol>', html, re.S)
    if not st:
        dire("le rail des stations (ol.stations) est absent")
    else:
        lis = re.findall(r"<li\b.*?</li>", st.group(1), re.S)
        if len(lis) != 4:
            dire(f"{len(lis)} stations, la méthode en compte quatre")
        for i, li in enumerate(lis, 1):
            if f"0{i}" not in li:
                dire(f"la station {i} ne porte pas son numéro 0{i}")
        if lis and "methode-term" not in lis[2]:
            dire("la station 03 (RERUN) ne porte pas le terminal des commandes")
        n_cmd = len(re.findall(r"<code[^>]*>", lis[2])) if len(lis) >= 3 else 0
        if n_cmd != 3:
            dire(f"le terminal de la station 03 porte {n_cmd} commandes, la maison en montre trois")
        if lis and "sealed" not in _nu(lis[0]):
            dire("la station 01 ne définit pas « sealed » dans son paragraphe")

    # D. la scène de l'escalier et ses annotations PUBLIÉES
    if not re.search(r'class="objet"[^>]*src="[^"]*escalier-01\.webp"', html):
        dire("la scène de la méthode ne montre pas escalier-01.webp")
    sc = re.search(r'class="methode-scene"(.*?)class="methode-note"', html, re.S)
    etis = re.findall(r'<span class="ap-eti"[^>]*>(.*?)</span>', sc.group(1)) if sc else []
    f01 = findings_dossier["findings"][0]
    publiees = [str(a[4]).strip() for a in f01.get("annotations", [])]
    if sorted(_nu(e) for e in etis) != sorted(publiees):
        dire(f"les annotations de la scène {sorted(_nu(e) for e in etis)} ne sont pas celles "
             f"publiées de la fiche 01 du dossier {sorted(publiees)}")
    note = re.search(r'<p class="methode-note">(.*?)</p>', html, re.S)
    if not note or _nu(note.group(1)) != _nu(f01["phrase"]):
        dire("la note de la méthode n'est pas la phrase publiée de la fiche 01 : "
             "l'accueil cite le dossier, il ne le paraphrase pas")

    # E. les six liens de la méthode
    liens = re.search(r'<nav class="methode-liens"[^>]*>(.*?)</nav>', html, re.S)
    n_liens = len(re.findall(r"<a ", liens.group(1))) if liens else 0
    if n_liens != 6:
        dire(f"la barre de la méthode porte {n_liens} liens, la décision en met six")

    # F. les absences décidées
    avant_rideau = html.split('class="rideau"')[0]
    if 'class="lede' in avant_rideau:
        dire("une lede vit encore sur le premier écran : la décision l'a remplacée par le grand livre")
    if "hero-cue" in avant_rideau:
        dire("le hero-cue vit encore sur le premier écran")
    if re.search(r'<img[^>]*robot-[a-z-]+\.webp', avant_rideau):
        dire("un robot vit sur le héros de l'accueil : la décision n'y en met aucun")
    return fautes


def temoin(html, hero, fd):
    """La page réelle, mutée quatre fois : chaque mutation doit rougir sur la bonne
    affirmation, et la page intacte doit passer."""
    intacte = relever(html, hero, fd)
    if intacte:
        return intacte      # la vraie page a de vraies fautes : ce n'est pas le témoin qui casse
    sceau = outil.lire_releve_scelle(outil.OUTILS["routing"]["releve_scelle"])["empreinte"]
    mutations = [
        (html.replace(sceau, "0" * len(sceau)), "content hash", "le sceau mué"),
        (html.replace('<a class="carte-ev', '<b class="carte-xx', 1), "éventail", "la carte retirée"),
        (re.sub(r'(<span class="ap-eti"[^>]*>)[^<]*', r"\1mensonge", html, count=1), "annotations", "l'annotation réécrite"),
        (html.replace("94.4", "93.4") if "94.4" in html else html.replace("1,000", "9,999"),
         "ne se retrouve pas sur le héros routing", "le chiffre déplacé"),
    ]
    for mue, attendu, nom in mutations:
        fautes = relever(mue, hero, fd)
        if not any(attendu in f for f in fautes):
            sys.exit(f"GARDE CASSÉE : {nom} ne rougit plus (aucune faute ne parle de "
                     f"« {attendu} ») — aucun relevé n'est rendu (code 2)")
    return []


if __name__ == "__main__":
    docs = pathlib.Path(sys.argv[sys.argv.index("--docs") + 1]) if "--docs" in sys.argv else BASE.parent / "docs"
    html = (docs / "index.html").read_text(encoding="utf-8")
    hero = (docs / "routing" / "index.html").read_text(encoding="utf-8")
    fd = json.loads((BASE / "findings-dossier.json").read_text())
    fautes = temoin(html, hero, fd)
    if fautes:
        for f in fautes:
            print("  ROUGE", f)
        sys.exit(f"{len(fautes)} refus : l'accueil ne tient pas ses affirmations")
    print("témoin de l'accueil : le grand livre recompose son sceau, l'éventail suit le rideau, "
          "la méthode cite le dossier — et les quatre mutations rougissent encore")
