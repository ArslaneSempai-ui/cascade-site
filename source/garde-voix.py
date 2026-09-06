#!/usr/bin/env python3
"""LA GARDE DE LA VOIX (VOIX.md, tranchée par Arslane le 9/09) : sept motifs mécaniques
sur la copy SERVIE (docs/, par le cueilleur de inventaire-copy.py) et sur les findings.
Chaque refus donne la page et la ligne (ou la fiche). Ce que la garde ne juge pas :
le style. Elle attrape les formes que la voix a bannies, rien de plus.

Les sept motifs, du contrat du chef (10/09) :
  1. le titre à deux temps : h1/h2/h3 ou titre de finding fait de deux phrases dont la
     seconde a moins de six mots (« Exact never alarms. It also never finds. ») ;
  2. « , not » et « rather than » : bannis des titres, étiquettes et fiches ; dans la
     prose, au plus UN par page ;
  3. la densité des absolus every/nothing/never/always : plus de 1 pour 80 mots sur une
     page est un refus nommé ;
  4. un bloc de plus de 30 caractères repris tel quel sur plus de 2 pages, hors nav et
     hors pied ;
  5. les mots d'objet (sieve, blade, brass, stone, ivory, lectern, shelf, pile, bay,
     keystone, house, seam, amethyst, onyx, lapis, ruby) dans la copy, hors alt et hors
     scènes : les métaphores restent dans les images ;
  6. « fa » ou « fp » nus ; et dans une étiquette ou une fiche, un nombre entier laissé
     sans unité ni pour cent là où l'un des deux est attendu ;
  7. les formules de sincérité affichée : « before your eyes », « says so », « in its
     own words », « honest », « walks », « refuses to ».

LE TÉMOIN TOURNE D'ABORD, à chaque lancement : deux pages factices (temoin-voix/),
l'une fautive sur les sept motifs, l'autre saine. Si un motif ne mord plus, la garde
refuse de rendre un relevé : un zéro sans témoin ne prouve rien.

usage: python3 garde-voix.py [--docs DIR]      code 0 = voix tenue ; 1 = refus ; 2 = garde cassée
"""
import importlib.util
import json
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).parent
_spec = importlib.util.spec_from_file_location("inventaire_copy", BASE / "inventaire-copy.py")
_ic = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ic)
Cueilleur = _ic.Cueilleur

TITRES_TAGS = {"h1", "h2", "h3"}
MOTS_OBJET = re.compile(r"\b(sieve|blade|brass|stone|ivory|lectern|shelf|pile|bay|keystone|house|seam|amethyst|onyx|lapis|ruby)s?\b", re.I)
ABSOLUS = re.compile(r"\b(every|nothing|never|always)\b", re.I)
SINCERITE = re.compile(r"before your eyes|says so|in its own words|\bhonest\b|\bwalks\b|refuses to", re.I)
# les RESTES de la passe de copy (compteur du chef, 10/09, versé au motif 7) : les mots
# de la maison que VOIX.md a bannis et que la relecture humaine n'a plus à chercher
RESTES = re.compile(r"\btwins?\b|look-?alikes?|\barchetypes?\b|\brhythms?\b|\bfiche|\btonight\b"
                    r"|named row|the walk\b|\bhonestly\b|\bplainly\b|content content"
                    r"|verified by you\b|measured at home|photographs?|buy the bigger model", re.I)
# « tier » appartient aux pages Routing (VOIX §4) : ailleurs, un refus — sauf la forme
# définie « model tier », qui est la définition que VOIX impose
TIER = re.compile(r"\btiers?\b", re.I)
PAGES_NON_ROUTING = ("screening/", "monitoring/", "scoring/", "dossier/")
NUS = re.compile(r"\b(fa|fp)\b")
OPPOSITION = re.compile(r", not\b|\brather than\b", re.I)
# un nombre entier « nu » dans une étiquette ou une fiche : ni décimal (0.90 est un
# seuil), ni suivi d'une unité ou d'un %, ni collé à un mot-unité de la maison
UNITES = r"(?:%|percent|days?|d\b|files?|pairs?|cases?|words?|tests?|pages?|blocks?|controls?|questions?|ko\b|kb\b|px\b|s\b|ms\b|of\b|×|x\b|matchers?|scenarios?|factors?|tiers?|thresholds?|routings?|seals?|alerts?|escalations?|reviews?|char(?:acter)?s?)"
# « finding 01 » et les ordinaux à zéro de tête (01..05) sont des numéros de fiche,
# pas des mesures sans unité : le motif 6 vise le chiffre qui PRÉTEND mesurer
NOMBRE_NU = re.compile(r"(?<![\d.])(?<!finding )(?<!seq-)(\d{2,})(?!\.\d)(?!\s*" + UNITES + r")(?!\d)", re.I)


def est_titre(tag, cls, sorte_texte):
    return tag in TITRES_TAGS or "j-titre" in cls or "fiche-t" in cls


def est_etiquette_ou_fiche(cls, sorte_texte):
    return sorte_texte == "étiquette-3D" or "fiche" in cls or "ap-eti" in cls


def deux_temps(texte):
    phrases = [p.strip() for p in re.split(r"(?<=[.!?])\s+", texte.strip()) if p.strip()]
    if len(phrases) != 2:
        return False
    seconde = re.findall(r"[A-Za-z''’-]+", phrases[1])
    return 0 < len(seconde) < 6


def blocs_du_dossier(docs):
    """[(page, ligne, zone, tag, cls, sorte, texte)] pour chaque page servie, plus les
    findings (page = le fichier json, ligne = le numéro de fiche)."""
    tous = []
    for page in sorted(docs.rglob("*.html")):
        rel = str(page.relative_to(docs))
        c = Cueilleur()
        c.feed(page.read_text(encoding="utf-8"))
        for tag, cls, texte, ligne, zone, commun in c.blocs_situes:
            if len(texte) < 3:
                continue
            tous.append((rel, ligne, zone, tag, cls, _ic.sorte(tag, cls, texte), texte, commun))
        # les attributs alt/aria restent hors des motifs 1-6 (exemptés par le contrat) ;
        # le motif 7 les couvre : une sincérité affichée dans un alt reste de la copy
        for tag, k, texte in c.attrs_textes:
            tous.append((rel, 0, f"attribut-{k}", tag, "", f"attribut {k}", texte, ""))
    return tous


def blocs_findings(source):
    tous = []
    for f in sorted(source.glob("findings-*.json")):
        d = json.loads(f.read_text())
        findings = d.get("findings", d) if isinstance(d, dict) else d
        for i, fd in enumerate(findings if isinstance(findings, list) else []):
            num = fd.get("num", i + 1)
            for k, v in fd.items():
                if k in ("source", "annotations") or not isinstance(v, str) or not v.strip():
                    continue
                genre = "titre-finding" if k in ("titre", "title") else "fiche"
                tous.append((f.name, f"fiche {num} · {k}", "corps", "json", "fiche", genre, v.strip(), ""))
            for a in fd.get("annotations", []):
                if isinstance(a, (list, tuple)) and len(a) == 5 and str(a[4]).strip():
                    tous.append((f.name, f"fiche {num} · étiquette", "corps", "json", "ap-eti", "étiquette-3D", str(a[4]).strip(), ""))
    return tous


def relever(docs, source):
    refus = []
    communs = {}                # valeur data-commun → pages où elle apparaît

    def dire(motif, page, ou, quoi):
        refus.append((motif, page, ou, quoi))

    blocs = blocs_du_dossier(docs) + (blocs_findings(source) if source else [])
    pages = sorted({b[0] for b in blocs if b[0].endswith(".html")})

    # motifs 1, 2, 5, 6, 7 : bloc par bloc
    for page, ligne, zone, tag, cls, sorte_t, texte, commun in blocs:
        est_alt = zone.startswith("attribut-")
        titre = sorte_t == "titre-finding" or (not est_alt and est_titre(tag, cls, sorte_t))
        eti_fiche = sorte_t in ("étiquette-3D", "fiche") or (not est_alt and est_etiquette_ou_fiche(cls, sorte_t))
        if titre and deux_temps(texte):
            dire(1, page, ligne, f"titre à deux temps : « {texte[:70]} »")
        if (titre or eti_fiche) and OPPOSITION.search(texte):
            dire(2, page, ligne, f"« , not » / « rather than » dans un {'titre' if titre else 'étiquette/fiche'} : « {texte[:70]} »")
        if not est_alt and zone != "scene" and MOTS_OBJET.search(texte):
            mot = MOTS_OBJET.search(texte).group(0)
            dire(5, page, ligne, f"mot d'objet « {mot} » hors scène et hors alt : « {texte[:70]} »")
        if not est_alt and NUS.search(texte):
            dire(6, page, ligne, f"« {NUS.search(texte).group(0)} » nu : « {texte[:70]} »")
        if eti_fiche and not est_alt:
            m = NOMBRE_NU.search(texte)
            if m and not m.group(1).startswith("0"):
                dire(6, page, ligne, f"nombre sans unité ni pour cent « {m.group(1)} » : « {texte[:70]} »")
        if SINCERITE.search(texte):
            dire(7, page, ligne, f"sincérité affichée « {SINCERITE.search(texte).group(0)} » : « {texte[:70]} »")
        if RESTES.search(texte):
            dire(7, page, ligne, f"reste de la maison « {RESTES.search(texte).group(0)} » : « {texte[:70]} »")
        if (page.startswith(PAGES_NON_ROUTING) and TIER.search(texte)
                and "model tier" not in texte.lower()):
            dire(7, page, ligne, f"« tier » hors des pages Routing : « {texte[:70]} »")

    # motifs 2-prose et 3 : à la page
    for p in pages:
        du_p = [b for b in blocs if b[0] == p and not b[2].startswith("attribut-")]
        prose = [b for b in du_p
                 if not (b[5] in ("titre-finding", "étiquette-3D", "fiche")
                         or est_titre(b[3], b[4], b[5]) or est_etiquette_ou_fiche(b[4], b[5]))]
        n_opp = sum(len(OPPOSITION.findall(b[6])) for b in prose)
        if n_opp > 1:
            dire(2, p, "page", f"{n_opp} « , not » / « rather than » dans la prose (au plus un par page)")
        mots = sum(len(re.findall(r"[A-Za-z''’-]+", b[6])) for b in du_p)
        absolus = sum(len(ABSOLUS.findall(b[6])) for b in du_p)
        if mots and absolus * 80 > mots:
            dire(3, p, "page", f"{absolus} absolus pour {mots} mots (plus de 1 pour 80)")

    # motif 4 : les répétitions entre pages, hors nav et hors pied. Un composant
    # FONCTIONNEL partagé (l'aide de la carte, le bloc des trois commandes, le
    # paragraphe allowlist des pages sécurité) est identique PAR CONSTRUCTION :
    # Écriture le déclare data-commun="…" sur son conteneur ; la garde l'exempte
    # et le compte à part — une répétition NON déclarée reste un refus
    par_texte = {}
    for page, ligne, zone, tag, cls, sorte_t, texte, commun in blocs:
        if not page.endswith(".html") or zone in ("nav", "pied") or zone.startswith("attribut-") or len(texte) <= 30:
            continue
        if commun:
            communs.setdefault(commun, set()).add(page)
            continue
        par_texte.setdefault(texte, set()).add(page)
    for texte, ou in sorted(par_texte.items()):
        if len(ou) > 2:
            dire(4, f"{len(ou)} pages", ", ".join(sorted(ou)[:4]) + ("…" if len(ou) > 4 else ""),
                 f"bloc repris tel quel : « {texte[:70]} »")
    return refus, communs


def temoin():
    """Les deux pages factices : la fautive doit déclencher les SEPT motifs, la saine
    aucun. Un motif muet = garde cassée, aucun relevé n'est rendu."""
    d = BASE / "temoin-voix"
    fautifs, communs_f = relever(d / "fautive", None)
    vus = {m for m, *_ in fautifs}
    if vus != {1, 2, 3, 4, 5, 6, 7}:
        sys.exit(f"GARDE CASSÉE : la page fautive du témoin ne déclenche que les motifs "
                 f"{sorted(vus)} sur les sept — aucun relevé n'est rendu (code 2)")
    if "commande" not in communs_f:
        sys.exit("GARDE CASSÉE : le bloc data-commun de la fautive n'est pas compté à part "
                 "— l'exemption déclarée ne fonctionne plus (code 2)")
    if any(m == 4 and "declared shared" in quoi for m, _, _, quoi in fautifs):
        sys.exit("GARDE CASSÉE : le bloc DÉCLARÉ data-commun de la fautive est refusé au "
                 "motif 4 — l'exemption ne s'applique plus (code 2)")
    if not any(m == 7 and "reste de la maison" in quoi for m, _, _, quoi in fautifs):
        sys.exit("GARDE CASSÉE : le reste de la maison planté (twins/archetypes/measured at "
                 "home) n'est plus vu (code 2)")
    if not any(m == 7 and "hors des pages Routing" in quoi for m, _, _, quoi in fautifs):
        sys.exit("GARDE CASSÉE : le « tier » planté sous screening/ n'est plus vu (code 2)")
    sains, _ = relever(d / "saine", None)
    if sains:
        sys.exit("GARDE CASSÉE : la page saine du témoin déclenche "
                 f"{[(m, q[:60]) for m, _, _, q in sains[:3]]} — la garde rougit sur du propre (code 2)")
    return len(fautifs)


if __name__ == "__main__":
    docs = pathlib.Path(sys.argv[sys.argv.index("--docs") + 1]) if "--docs" in sys.argv else BASE.parent / "docs"
    n_temoin = temoin()
    print(f"  témoin : les sept motifs mordent ({n_temoin} refus sur la fautive, 0 sur la saine)")
    refus, communs = relever(docs, BASE)
    if communs:
        print("  communs déclarés : " + " ; ".join(
            f"{k} sur {len(v)} page(s)" for k, v in sorted(communs.items())))
    if not refus:
        print(f"voix tenue : 0 refus sur {len(list(docs.rglob('*.html')))} pages servies "
              f"(et le témoin a prouvé que les sept motifs regardent)")
        sys.exit(0)
    par_motif = {}
    for m, page, ou, quoi in refus:
        par_motif.setdefault(m, []).append((page, ou, quoi))
    for m in sorted(par_motif):
        lignes = par_motif[m]
        print(f"── motif {m} · {len(lignes)} refus")
        for page, ou, quoi in lignes[:8]:
            print(f"  {page}:{ou} · {quoi}")
        if len(lignes) > 8:
            print(f"  … et {len(lignes) - 8} autres")
    print(f"{len(refus)} refus : la voix de VOIX.md n'est pas tenue")
    sys.exit(1)
