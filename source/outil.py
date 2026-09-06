#!/usr/bin/env python3
"""LA TABLE DES OUTILS : ce qui change quand la page change d'outil, et rien d'autre.

Le site est le CATALOGUE de la marque (ARCHITECTURE-CATALOGUE.md) : la barre, le
pied, la nuit, le parchemin et les gardes sont partagés ; la couleur d'accent, le
robot, le relevé scellé, les textes et le sous-dossier sont PAR OUTIL, et ils
vivent tous ici. Un bâtisseur qui tape une de ces valeurs chez lui recrée la
divergence que cette table existe pour fermer.

LA PALETTE : le vert historique reste écrit sous ses noms (--vert-*) pour que la
page verte reste identique À L'OCTET ; le rubis introduit les variables
--accent-* et ALIASE les --vert-* dessus, si bien que tout le CSS partagé écrit
en var(--vert-*) rend rubis sans être touché. Le jour où une palette neutre est
voulue partout, le vert bascule sur le même mécanisme en un seul endroit : ici.
"""
import hashlib
import filecmp
import json
import pathlib
import sys

_MAISON = pathlib.Path.home() / "Documents"


def _canonique(x, racine=True):
    """Le JSON canonique de empreinteDuReleve (cascade-screening/src/empreinte.ts),
    porté en Python : clés triées, la clé `empreinte` exclue À LA RACINE seulement."""
    if isinstance(x, list):
        return [_canonique(v, False) for v in x]
    if isinstance(x, dict):
        return {k: _canonique(x[k], False) for k in sorted(x)
                if not (racine and k == "empreinte")}
    return x


def _stringify(x):
    """JSON.stringify, à l'octet : séparateurs compacts, unicode brut, et les
    nombres au format de JS (les floats de Python impriment pareil ; un float
    ENTIER comme 1.0 imprimerait « 1.0 » là où JS écrit « 1 » : converti)."""
    def entier(o):
        if isinstance(o, float) and o.is_integer():
            return int(o)
        if isinstance(o, list):
            return [entier(v) for v in o]
        if isinstance(o, dict):
            return {k: entier(v) for k, v in o.items()}
        return o
    return json.dumps(entier(x), separators=(",", ":"), ensure_ascii=False)


def empreinte_du_releve(releve):
    return hashlib.sha256(_stringify(_canonique(releve)).encode()).hexdigest()[:16]


def lire_releve_scelle(chemin):
    """Le relevé public d'un outil, REFUSÉ si absent ou si son scellé ment :
    une page bâtie sur un relevé retouché publierait des chiffres que personne
    n'a mesurés, avec l'autorité du site."""
    chemin = pathlib.Path(chemin)
    if not chemin.exists():
        sys.exit(f"{chemin} introuvable : les chiffres ne se tapent pas, ils se lisent")
    releve = json.loads(chemin.read_text())
    porte = releve.get("empreinte")
    if not isinstance(porte, str) or not porte:
        sys.exit(f"{chemin} ne porte aucun scellé : rien ne prouve que c'est le relevé mesuré")
    calcule = empreinte_du_releve(releve)
    if calcule != porte:
        sys.exit(f"{chemin} ne correspond plus à son scellé (porté {porte}, calculé {calcule}) : "
                 "le fichier a changé après scellement, rien ne se bâtit dessus")
    return releve


# ── la palette, en deux rendus ───────────────────────────────────────────────
# Le vert : la ligne HISTORIQUE, à l'octet — elle est comparée par les tests de
# non-régression de l'assemblage (docs/ inchangé). Le rubis : les --accent-*
# remplis, et les --vert-* aliasés dessus pour que le CSS partagé suive.
PALETTE_VERTE = "--vert-titre:#23543f;--vert-vif:#57b184;--vert-clair:#a5f7cb;"
PALETTE_RUBIS = ("--accent-titre:#7a1f2e;--accent-vif:#d64a5c;--accent-clair:#ffc2c9;"
                 "--vert-titre:var(--accent-titre);--vert-vif:var(--accent-vif);"
                 "--vert-clair:var(--accent-clair);")
# LA NUIT suit l'outil aussi (Arslane, 6/09 : « pourquoi le terminal à droite n'est
# pas rouge aussi ? ») : sur la page rouge, le héros, le panneau des findings, la
# section instrument et le pied sont une nuit rubis, la même que l'instrument rouge
# et que le pan du rideau ; le parchemin, lui, reste celui de la maison.
NUIT_VERTE = "--nuit-a:#1b3229;--nuit-b:#14251e;--nuit-c:#0e1a15;--sur-vert:#e4ecdf;--sur-vert-pale:#a9bdaf;"
NUIT_RUBIS = "--nuit-a:#33191f;--nuit-b:#241217;--nuit-c:#180b0f;--sur-vert:#efe0e2;--sur-vert-pale:#c0a6ab;"
PALETTE_LAPIS = ("--accent-titre:#1f3f7a;--accent-vif:#4f8ae0;--accent-clair:#c3d8ff;"
                 "--vert-titre:var(--accent-titre);--vert-vif:var(--accent-vif);"
                 "--vert-clair:var(--accent-clair);")
NUIT_LAPIS = "--nuit-a:#16213a;--nuit-b:#101a30;--nuit-c:#0a111f;--sur-vert:#e6ecf7;--sur-vert-pale:#a8b7d4;"
PALETTE_AMETHYSTE = ("--accent-titre:#4b2a7a;--accent-vif:#9b6fe0;--accent-clair:#e2d3ff;"
                     "--vert-titre:var(--accent-titre);--vert-vif:var(--accent-vif);"
                     "--vert-clair:var(--accent-clair);")
NUIT_AMETHYSTE = "--nuit-a:#241a3a;--nuit-b:#1a1230;--nuit-c:#100b1f;--sur-vert:#ede6f7;--sur-vert-pale:#b9a9d4;"
PALETTE_ONYX = ("--accent-titre:#1c1c22;--accent-vif:#8a8a96;--accent-clair:#e8e6df;"
                "--vert-titre:var(--accent-titre);--vert-vif:var(--accent-vif);"
                "--vert-clair:var(--accent-clair);")
NUIT_ONYX = "--nuit-a:#121216;--nuit-b:#0c0c10;--nuit-c:#070709;--sur-vert:#efede6;--sur-vert-pale:#b8b6ad;"

OUTILS = {
    "routing": {
        "id": "routing",
        "nom": "Routing",
        # depuis le 6/09 (décision A d'Arslane), la racine est la page de la MARQUE ;
        # Routing vit sous routing/ comme Screening sous screening/
        "sous_dossier": "routing/",
        "prefixe_racine": "../",
        "question": "Which model tier reads each field?",
        "palette": PALETTE_VERTE,
        "favicon_accent": "%2323543f",
        "robots": ("robot-penche.webp", "robot-agrippe.webp"),
        "releve": _MAISON / "cascade" / "landing.json",     # pas de scellé : garde d'absence seule (historique)
        # le RELEVÉ SCELLÉ du vert (son relevé de référence, marqué et re-scellé le 8/09) : la
        # source unique du sceau que les pages vertes citent ; landing.json reste le fichier de chiffres
        "releve_scelle": _MAISON / "cascade" / "profiles-2026-08-20-coeur-rendu.json",
        "outil_chemin": _MAISON / "cascade",
        "depot": "https://github.com/ArslaneSempai-ui/cascade-routing",
        # le rideau (deuxième écran) : ce que le pan de CET outil dit de lui, sur
        # TOUTE page ; ses teintes vivent ici parce que la page rubis aliase la
        # palette et que le pan vert doit y rester vert
        "page_hero": "HERO.html",
        "etiquette": "Routing &#183; identity-field extraction",
        "pitch": "Seven model tiers per field, from a regular expression to a human, measured on sealed public records.",
        "robot_rideau": "robot-salut.webp",           # il salue (etats/robots-rideau.py)
        "vif": "#57b184",
        "nuit": ("#1b3229", "#14251e", "#0e1a15"),
    },
    "screening": {
        "id": "screening",
        "nom": "Screening",
        "sous_dossier": "screening/",
        "prefixe_racine": "../",
        # pas d'insécable ici : « which threshold? » d'un bloc déborde à 320 px (mesuré)
        "question": "Which matcher suffices, at which threshold?",
        "palette": PALETTE_RUBIS,
        "favicon_accent": "%237a1f2e",
        "robots": ("robot-rubis-penche.webp", "robot-rubis-agrippe.webp"),
        "releve": _MAISON / "cascade-screening" / "releve-public.json",  # scellé, vérifié par lire_releve_scelle
        "outil_chemin": _MAISON / "cascade-screening",
        "depot": "https://github.com/ArslaneSempai-ui/cascade-screening",
        "page_hero": "HERO-SCREENING.html",
        "etiquette": "Screening &#183; name matching",
        "pitch": "Seven matchers, from strict equality to a multilingual embedding, measured on your own alert history.",
        "robot_rideau": "robot-rubis-curieux.webp",   # il se penche, curieux (etats/robots-rideau.py)
        # l'affiche du film : la plaque 3D (etats/affiche-plaque.py) + la carte des deux
        # chiffres de la frontière lus dans le relevé (etats/affiche-composer.py)
        "affiche": "affiche-screening.jpg",
        "affiche_alt": "The ruby Cascade robot, palms up, projecting the two rates of the "
                       "best-trade-off cell: recall on the left, false alerts on the right.",
        "vif": "#d64a5c",
        "nuit": ("#33191f", "#241217", "#180b0f"),      # la nuit rubis de NUIT_RUBIS
    },
    "monitoring": {
        "id": "monitoring",
        "nom": "Monitoring",
        "sous_dossier": "monitoring/",
        "prefixe_racine": "../",
        "question": "Which scenario suffices, at which threshold?",
        "palette": PALETTE_LAPIS,
        "favicon_accent": "%231f3f7a",
        "robots": ("robot-lapis-penche.webp", "robot-lapis-montre.webp"),
        "releve": _MAISON / "cascade-monitoring" / "releve-public.json",  # scellé, vérifié par lire_releve_scelle
        "outil_chemin": _MAISON / "cascade-monitoring",
        # le dépôt n'existe pas encore en ligne : lien mort jusqu'au push d'Arslane,
        # exactement comme le rouge avant le sien
        "depot": "https://github.com/ArslaneSempai-ui/cascade-monitoring",
        "page_hero": "HERO-MONITORING.html",
        "etiquette": "Monitoring &#183; transaction monitoring",
        "pitch": "Seven scenarios, from a bare amount to a peer profile, measured on your own dispositioned alerts.",
        "robot_rideau": "robot-lapis-montre.webp",    # il montre (rendu du chef)
        # l'affiche : plaque lapis (affiche-plaque.py --accent lapis) + les deux chiffres
        # de la fiche 03 lus dans le relevé (ici deux BORNES BASSES, champ « bas » :
        # aucune cellule ne tient le plancher, l'affiche le dit avec les deux meilleures)
        "affiche": "affiche-monitoring.jpg",
        "affiche_alt": "The lapis Cascade robot, palms up, projecting the two highest lower "
                       "bounds of recall any single scenario reaches: amount on the left, "
                       "peer on the right, both under the 0.90 floor.",
        "vif": "#4f8ae0",
        "nuit": ("#16213a", "#101a30", "#0a111f"),      # la nuit lapis de NUIT_LAPIS
    },
    "scoring": {
        "id": "scoring",
        "nom": "Scoring",
        "sous_dossier": "scoring/",
        "prefixe_racine": "../",
        "question": "Which risk factor suffices, at which threshold?",
        "palette": PALETTE_AMETHYSTE,
        "favicon_accent": "%234b2a7a",
        "robots": ("robot-amethyste-penche.webp", "robot-amethyste-pese.webp"),
        "releve": _MAISON / "cascade-scoring" / "releve-public.json",   # scellé par le lot A-L4 (à venir) : l'entrée reste gated par manques()
        "outil_chemin": _MAISON / "cascade-scoring",
        "depot": "https://github.com/ArslaneSempai-ui/cascade-scoring",
        "page_hero": "HERO-SCORING.html",
        "etiquette": "Scoring &#183; risk rating",
        "pitch": "Seven risk factors, from a country list to the deviation from the declared profile, measured on your own periodic-review outcomes.",
        "robot_rideau": "robot-amethyste-pese.webp",    # il pèse : sa pose à lui
        "affiche": "affiche-scoring.jpg",
        "affiche_alt": "The amethyst Cascade robot, palms up, projecting the two lower bounds of recall "
                       "the card names: product on the left, behaviour on the right, both under the 0.90 floor.",
        "vif": "#9b6fe0",
        "nuit": ("#241a3a", "#1a1230", "#100b1f"),
    },
    "dossier": {
        "id": "dossier",
        "nom": "Dossier",
        "sous_dossier": "dossier/",
        "prefixe_racine": "../",
        "question": "Is the whole chain measured, signed and current?",
        "palette": PALETTE_ONYX,
        "favicon_accent": "%231c1c22",
        "robots": ("robot-onyx-penche.webp", "robot-onyx-tient.webp"),
        "releve": _MAISON / "cascade-dossier" / "releve-public.json",   # scellé 2497928ec273023c (D1 lu + D2 mesuré)
        "outil_chemin": _MAISON / "cascade-dossier",
        "depot": "https://github.com/ArslaneSempai-ui/cascade-dossier",
        "page_hero": "HERO-DOSSIER.html",
        "etiquette": "Dossier &#183; the audit dossier",
        "pitch": "Four signed reports, five controls, one dossier a reviewer verifies without us.",
        "robot_rideau": "robot-onyx-tient.webp",        # il tient la pièce
        "affiche": "affiche-dossier.jpg",
        "affiche_encre": "#2a2a31",                    # le gris vif de l'onyx s'efface sur la plaque : l'encre projetée est plus sombre
        "affiche_alt": "The onyx Cascade robot, palms up, projecting two counts from the sealed public dossier: "
                       "the questions holding the fresh control on the left, those not holding it on the right.",
        "vif": "#8a8a96",
        "nuit": ("#121216", "#0c0c10", "#070709"),
    },
}


# ── ce qu'il faut à un outil pour être MONTRÉ et ÉMIS : une seule définition,
#    consommée par le rideau (batir-hero) ET par la porte d'émission (assembler).
#    Deux définitions ont divergé en une heure le 7/09 : le rideau montrait un pan
#    vers une page que l'assembleur refusait d'émettre : liens morts sur tout le site.
ETATS_PREFIXE = {"routing": "objet", "screening": "tamis", "monitoring": "rack",
                 "scoring": "rayonnage", "dossier": "escalier"}   # rack, rayonnage, escalier : tranchés par Arslane sur planches
ICONES_PREFIXE = {"screening": "objet-screening", "monitoring": "objet-monitoring",
                  "scoring": "objet-scoring", "dossier": "objet-dossier"}
ICONES_NOMS = ("methode", "securite", "terms", "privacy", "accessibilite")


def manques(outil_id, base):
    """La liste de ce qui MANQUE à un outil du catalogue pour être prêt : vide = prêt.
    Routing et Screening sont en ligne et leurs pièces sont commitées : liste vide par
    construction ; le test reste exécuté pour eux, pour qu'une pièce retirée se voie."""
    base = pathlib.Path(base)
    o = OUTILS[outil_id]
    m = []
    if outil_id != "routing":
        chemin_f = base / f"findings-{outil_id}.json"
        if not chemin_f.exists():
            m.append(f"findings-{outil_id}.json")
        else:
            # un fichier de findings livré AVANT le scellé de son relevé porte pret:false
            # (le lot des textes refuse de deviner les chiffres) : il compte comme absent,
            # en le disant — sinon le rideau montrerait un pan dont le héros refuse de se bâtir
            try:
                f = json.loads(chemin_f.read_text())
            except ValueError:
                f = {"pret": False}
            if not f.get("pret", True):
                m.append(f"findings-{outil_id}.json (pret: false : les chiffres attendent leur sceau)")
            elif "sceau" in f and f["sceau"] != lire_releve_scelle(o["releve"])["empreinte"]:
                # le relevé a été re-scellé depuis que les textes ont dérivé leurs chiffres
                # (une re-mesure post-A-L4, par exemple) : le héros refuserait de se bâtir,
                # et le rideau montrerait un pan mort — LA définition de « prêt » doit le
                # voir AVANT, sinon les deux divergent exactement comme bassins/rack
                m.append(f"findings-{outil_id}.json (sceau {f['sceau']} : le relevé porte "
                         f"{lire_releve_scelle(o['releve'])['empreinte']}, à re-dériver)")
        # les SOURCES des deux annexes comptent parmi les pièces : le 9/09, le pan
        # scoring s'est montré sur quatre pages pendant que la porte d'émission disait
        # « il manque ANNEXE-SCORING-*.html » — six liens morts ; la même définition
        # de « prêt » doit couvrir TOUT ce que le bloc émet
        for piece in (f"annexe-{outil_id}-methode.json", f"annexe-{outil_id}-securite.json"):
            if not (base / piece).exists():
                m.append(piece)
    if not (base / "rendus" / o["robot_rideau"]).exists():
        m.append(f"rendus/{o['robot_rideau']}")
    prefixe = ETATS_PREFIXE[outil_id]
    m += [f"rendus/etats/{prefixe}-0{i}.webp" for i in range(1, 6)
          if not (base / "rendus" / "etats" / f"{prefixe}-0{i}.webp").exists()]
    if outil_id in ICONES_PREFIXE:
        m += [f"rendus/etats/{ICONES_PREFIXE[outil_id]}-{n}.webp" for n in ICONES_NOMS
              if not (base / "rendus" / "etats" / f"{ICONES_PREFIXE[outil_id]}-{n}.webp").exists()]
    m += manques_sequences(outil_id, base)
    m += manques_etiquettes(outil_id, base)
    return m


# Le sceau du vert, LU dans son relevé scellé et vérifié : cinq bâtisseurs le tapaient à la main
# (1151f5a1cfaae0c0) et le relevé a été re-scellé le 8/09 (marques kind/version) : un sceau
# recopié rouille ; celui-ci suit le fichier.
# ── les gardes des séquences (lot M-C1) ─────────────────────────────────────────
#
# Quatre gardes, DANS manques() — la même définition de « prêt » que le rideau, le héros
# et l'assembleur (la divergence bassins/rack a coûté des liens morts sur tout le site) :
#   identité    l'état k EST la dernière image de sa transition, octet pour octet — sinon
#               l'arrêt du mouvement montrerait une autre image que celle qui porte les
#               annotations d'Écriture ;
#   fraîcheur   manifest.sceau == le sceau du relevé public de l'outil — des séquences
#               rendues sur un relevé re-scellé montreraient les chiffres d'avant ;
#   poids       la somme des images d'une page ≤ BUDGET_SEQUENCE_KO, constante déclarée —
#               dépasser n'est pas interdit, dépasser en silence l'est ;
#   complétude  n × 5 fichiers présents, aux pixels du manifeste — une image manquante est
#               un refus côté bâtisseur ; la voisine, c'est le repli du NAVIGATEUR en
#               direct, jamais une émission silencieusement trouée.
# Un outil SANS séquence n'est pas un outil cassé : sans manifeste, aucune garde ne parle.

# Le budget d'une page de séquences, en kilo-octets. AUCUN chiffre non mesuré : le chef le
# pose après le premier rendu de livraison (mesure + date dans ce commentaire-là). Tant
# qu'il vaut None, des séquences livrées sont REFUSÉES : un budget non écrit est une
# intention, et une intention ne se dépasse jamais.
# MESURÉ le 9/09/2026 sur les deux premières livraisons : le rack, 5 × 24 images webp q92 = 10156 ko ;
# le tamis (maille, jetons : deux fois plus de détail) = 17 712 ko à q92, 13256 ko replumé à q80, la
# qualité des images de passage désormais (plumer --q 80). Le budget est la plus lourde plus 8 %,
# arrondi au demi-millier ; une page au-dessus refuse d'être assemblée (garde « poids », M-C1).
# Piste si l'on veut plus léger : rendre les images de passage à 1100 px (le contrat des tailles
# uniques est à revoir avec Mesure et Portfolio d'abord).
BUDGET_SEQUENCE_KO = 14500

def taille_webp(chemin):
    """(largeur, hauteur) d'un webp, lues dans l'en-tête (VP8X / VP8L / VP8), sans
    dépendance. Un fichier illisible rend None : la garde le dira, elle ne plantera pas."""
    try:
        d = pathlib.Path(chemin).read_bytes()[:30]
    except OSError:
        return None
    if len(d) < 30 or d[:4] != b"RIFF" or d[8:12] != b"WEBP":
        return None
    quatre = d[12:16]
    if quatre == b"VP8X":
        return (int.from_bytes(d[24:27], "little") + 1, int.from_bytes(d[27:30], "little") + 1)
    if quatre == b"VP8L":
        if d[20] != 0x2F:
            return None
        bits = int.from_bytes(d[21:25], "little")
        return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
    if quatre == b"VP8 ":
        if d[23:26] != b"\x9d\x01\x2a":
            return None
        return (int.from_bytes(d[26:28], "little") & 0x3FFF, int.from_bytes(d[28:30], "little") & 0x3FFF)
    return None


def sceau_du_releve(outil_id):
    """Le sceau du relevé public d'un outil — le vert par son relevé scellé historique
    (landing.json n'en porte pas), les quatre autres par leur releve-public.json."""
    o = OUTILS[outil_id]
    chemin = o["releve_scelle"] if outil_id == "routing" else o["releve"]
    return lire_releve_scelle(chemin)["empreinte"]


_BUDGET_DECLARE = object()   # sentinelle : « lis la constante » ; un témoin injecte la sienne

def manques_sequences(outil_id, base, budget_ko=_BUDGET_DECLARE, sceau_attendu=None):
    """Ce qui manque aux SÉQUENCES d'un outil pour être prêtes : vide = prêtes, ou pas de
    séquences du tout. budget_ko et sceau_attendu sont injectables pour les témoins ; la
    production passe par les défauts (BUDGET_SEQUENCE_KO, sceau_du_releve)."""
    base = pathlib.Path(base)
    prefixe = ETATS_PREFIXE[outil_id]
    dossier = base / "rendus" / "sequences" / prefixe
    ou = f"rendus/sequences/{prefixe}"
    if not (dossier / "manifest.json").exists():
        return []
    m = []
    try:
        man = json.loads((dossier / "manifest.json").read_text())
    except ValueError as e:
        return [f"{ou}/manifest.json (illisible : {e})"]
    absentes = [k for k in ("prefixe", "n", "transitions", "ext", "large", "haut", "mouvement", "sceau")
                if k not in man]
    if absentes:
        return [f"{ou}/manifest.json (clé(s) absente(s) : {', '.join(absentes)})"]

    # fraîcheur : des séquences rendues sur un relevé re-scellé montrent les chiffres d'avant
    attendu = sceau_attendu if sceau_attendu is not None else sceau_du_releve(outil_id)
    if man["sceau"] != attendu:
        m.append(f"{ou} (sceau {man['sceau']} : le relevé porte {attendu} — séquences rendues "
                 f"sur un autre relevé, à re-rendre)")

    # complétude : n × transitions fichiers, aux pixels du manifeste
    defauts = []
    octets = 0
    for k in range(1, man["transitions"] + 1):
        for i in range(man["n"]):
            f = dossier / f"{man['prefixe']}-seq-0{k}-{i:03d}{man['ext']}"
            if not f.exists():
                defauts.append(f"{ou}/{f.name} (image manquante : pas de voisine servie en silence)")
                continue
            octets += f.stat().st_size
            t = taille_webp(f)
            if t != (man["large"], man["haut"]):
                lue = f"{t[0]}×{t[1]}" if t else "en-tête illisible"
                defauts.append(f"{ou}/{f.name} ({lue} : le manifeste dit {man['large']}×{man['haut']})")
    m += defauts[:6]
    if len(defauts) > 6:
        m.append(f"{ou} (… et {len(defauts) - 6} autre(s) défaut(s) de complétude)")

    # identité : l'état k EST la dernière image de sa transition, octet pour octet
    for k in range(1, man["transitions"] + 1):
        etat = base / "rendus" / "etats" / f"{prefixe}-0{k}.webp"
        derniere = dossier / f"{man['prefixe']}-seq-0{k}-{man['n'] - 1:03d}{man['ext']}"
        if etat.exists() and derniere.exists() and not filecmp.cmp(etat, derniere, shallow=False):
            m.append(f"rendus/etats/{prefixe}-0{k}.webp (n'est pas la dernière image de sa "
                     f"transition : l'arrêt du mouvement montrerait une autre image que "
                     f"l'état annoté)")

    # poids : un budget non écrit est une intention, et une intention ne se dépasse jamais
    budget = BUDGET_SEQUENCE_KO if budget_ko is _BUDGET_DECLARE else budget_ko
    if budget is None:
        m.append(f"{ou} (BUDGET_SEQUENCE_KO non déclaré dans outil.py : le chef le pose, "
                 f"mesure et date à l'appui, après le premier rendu de livraison)")
    elif octets / 1000 > budget:
        m.append(f"{ou} ({octets / 1000:.0f} Ko de séquences : le budget déclaré est "
                 f"{budget} Ko — dépasser se dit, il ne se constate pas en production)")
    return m


SCEAU_ROUTING = lire_releve_scelle(OUTILS["routing"]["releve_scelle"])["empreinte"]

def lien(outil, cible):
    """Le lien d'une page de CET outil vers une cible de la MAISON (nom source,
    ex. « ENGAGEMENT.html », « rendus/x.webp ») : préfixé pour sortir du
    sous-dossier quand il y en a un. Les liens entre pages d'un même outil ne
    passent pas ici : ils restent nus, sœurs de dossier."""
    return outil["prefixe_racine"] + cible


# ── LES ÉTIQUETTES SUR LE CRÈME, JAMAIS SUR L'OBJET (Arslane, 9/09 : « les infos directement
# sur le modèle, ça les rend illisibles ; mets-les toujours sur le fond crème ») ──────────
# Une annotation est une pointe (ax, ay) SUR l'objet et une étiquette (lx, ly) à côté. Depuis
# les gros plans, l'objet remplit l'image et une étiquette posée au hasard tombe dessus. La
# règle est mécanique : l'alpha de l'image d'état est lu sous la boîte de l'étiquette ; plus
# d'un dixième de pixels d'objet, et le bloc de l'outil n'est pas prêt (manques()).
# Géométrie du héros (batir-hero.py) : viewBox 1420×1000, l'image (rapport 1374/1120) centrée ;
# une chip .ap-eti fait au plus 240 px sur 2 lignes dans une scène de ~744 px pour 1420 unités.
IW_ANNOT = 1000.0 * (1374 / 1120)
MX_ANNOT = (1420 - IW_ANNOT) / 2
# La chip fait 240 px FIXES (max-width) sur ~44 px de haut pour deux lignes, mais la scène rétrécit
# avec la fenêtre : 744 px à 1440, ~477 px à 1081 (la plus petite fenêtre encore annotée, avant
# le @media ≤ 1080 qui empile). Son empreinte en unités du viewBox est donc la plus grande sur la
# plus PETITE scène : 240/477 × 1420 = 714 de large, 44/336 × 1000 = 131 de haut. La garde se
# calibre là (relecture de Mesure, 9/09) : une étiquette qui passe ici passe à toutes les tailles.
# Depuis le 9/09 (15h40) la chip est en POUR CENT de la scène (32,3 % de large, police en cqi) : son
# empreinte est la même en unités du viewBox à toutes les fenêtres, 240×44 px sur la scène de 744 px.
CHIP_DEMI = (round(240 / 744 * 1420 / 2), round(44 / (744 / 1.42) * 1000 / 2))   # (229, 42)
SEUIL_OBJET = 0.10             # part de pixels d'objet tolérée sous l'étiquette
_ALPHAS = {}


def alpha_webp(chemin):
    """(W, H, alpha) d'un webp, par dwebp (libwebp) ; mis en cache par chemin."""
    import subprocess
    chemin = str(chemin)
    if chemin in _ALPHAS:
        return _ALPHAS[chemin]
    try:
        brut = subprocess.run(["dwebp", chemin, "-pam", "-o", "-"], capture_output=True, check=True).stdout
    except FileNotFoundError:
        raise SystemExit("dwebp absent (brew install webp) : la garde des étiquettes ne peut pas lire l'alpha des états ; refus, pas de vert par absence")
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"dwebp refuse {chemin} : {e.stderr.decode(errors='replace')[:200]}")
    fin = brut.index(b"ENDHDR\n") + 7
    tete = dict(l.split(" ", 1) for l in brut[:fin].decode().splitlines() if " " in l)
    W, H, prof = int(tete["WIDTH"]), int(tete["HEIGHT"]), int(tete["DEPTH"])
    px = brut[fin:]
    alpha = px[prof - 1::prof] if prof == 4 else bytes([255]) * (W * H)
    _ALPHAS[chemin] = (W, H, alpha)
    return _ALPHAS[chemin]


def etiquette_sur_objet(image, lx, ly, demi=CHIP_DEMI):
    """La part de pixels d'OBJET (alpha > 40) sous la boîte de l'étiquette centrée en (lx, ly),
    coordonnées relatives à l'image comme dans findings-*.json. Hors de l'image = du crème."""
    W, H, alpha = alpha_webp(image)
    cx, cy = MX_ANNOT + lx * IW_ANNOT, ly * 1000.0
    ex = W / IW_ANNOT
    x0, x1 = int((cx - demi[0] - MX_ANNOT) * ex), int((cx + demi[0] - MX_ANNOT) * ex)
    y0, y1 = int((cy - demi[1]) * H / 1000.0), int((cy + demi[1]) * H / 1000.0)
    total = max(1, (x1 - x0) * (y1 - y0))
    objet = 0
    for y in range(max(0, y0), min(H, y1)):
        ligne = alpha[y * W + max(0, x0): y * W + min(W, x1)]
        objet += sum(1 for a in ligne if a > 40)
    return objet / total


def etiquette_dans_scene(lx, ly, demi=CHIP_DEMI, tolerance=8):
    """La boîte de l'étiquette tient dans la scène (viewBox 1420×1000) : au-delà elle couvre le rail
    ou la fiche, et le lecteur perd l'un ou l'autre."""
    cx, cy = MX_ANNOT + lx * IW_ANNOT, ly * 1000.0
    return (cx - demi[0] >= -tolerance and cx + demi[0] <= 1420 + tolerance
            and cy - demi[1] >= -tolerance and cy + demi[1] <= 1000 + tolerance)


# La boîte d'une chip, en unités du viewBox, ESTIMÉE sur son texte : la chip est en monospace à
# 1,55 % de la largeur de scène (≈ 22 unités par em, ≈ 13,2 par caractère), padding .8em de chaque
# côté, plafonnée à 2 × CHIP_DEMI[0] de large (32,3 % de la scène) ; au-delà elle passe sur deux
# lignes. Une étiquette courte est donc plus étroite que la boîte maximale de la garde d'objet.
UNITES_PAR_CARACTERE = 13.2
def boite_etiquette(txt, demi=CHIP_DEMI):
    largeur = UNITES_PAR_CARACTERE * len(txt) + 36
    if largeur > 2 * demi[0]:
        return 2 * demi[0], 2 * demi[1]          # deux lignes : la boîte maximale
    return largeur, 50                           # une ligne


def etiquettes_qui_se_recouvrent(annotations, ecart=8):
    """Deux chips d'une MÊME scène ne doivent pas se recouvrir ni se toucher : le 9/09, sur le vert,
    « a pick both routings share » cachait la moitié de « name changes reader… » et la garde
    d'objet, qui juge chaque étiquette seule, laissait passer. Rend les paires fautives (a, b)
    d'indices dans la liste (ax, ay, lx, ly, txt), avec un écart minimal exigé entre les boîtes."""
    boites = []
    for (ax, ay, lx, ly, txt) in annotations:
        l, h = boite_etiquette(txt)
        boites.append((MX_ANNOT + lx * IW_ANNOT, ly * 1000.0, l, h))
    paires = []
    for a in range(len(boites)):
        for b in range(a + 1, len(boites)):
            xa, ya, la, ha = boites[a]
            xb, yb, lb, hb = boites[b]
            if abs(xa - xb) < (la + lb) / 2 + ecart and abs(ya - yb) < (ha + hb) / 2 + ecart:
                paires.append((a, b))
    return paires


def manques_etiquettes(outil_id, base, seuil=SEUIL_OBJET):
    """Chaque étiquette de findings-<outil>.json doit être sur le crème de SON image d'état."""
    base = pathlib.Path(base)
    chemin_f = base / f"findings-{outil_id}.json"
    if outil_id == "routing" or not chemin_f.exists():
        return []
    try:
        f = json.loads(chemin_f.read_text())
    except ValueError:
        return []
    findings = f["findings"] if isinstance(f, dict) and "findings" in f else f
    prefixe = ETATS_PREFIXE[outil_id]
    # La règle vaut pour les états CHORÉGRAPHIÉS (gros plans) : un plateau qui n'a pas encore ses
    # séquences garde ses états larges d'aujourd'hui, validés et en ligne, jusqu'à sa livraison ;
    # le juger maintenant ferait tomber trois blocs (et les liens du rideau) pour des étiquettes
    # que la livraison remplace de toute façon. Le manifeste est le signe de la livraison.
    if not (base / "rendus" / "sequences" / prefixe / "manifest.json").exists():
        return []
    m = []
    for i, fd in enumerate(findings if isinstance(findings, list) else []):
        image = base / "rendus" / "etats" / f"{prefixe}-0{i + 1}.webp"
        if not image.exists():
            continue
        for (ax, ay, lx, ly, txt) in fd.get("annotations", []):
            if not etiquette_dans_scene(lx, ly):
                m.append(f"findings-{outil_id}.json, finding {fd.get('num', i + 1)} : l'étiquette « {txt[:38]}… » "
                         "déborde de la scène (sur le rail ou la fiche) : la rentrer")
                continue
            part = etiquette_sur_objet(image, lx, ly)
            if part > seuil:
                m.append(f"findings-{outil_id}.json, finding {fd.get('num', i + 1)} : l'étiquette « {txt[:38]}… » "
                         f"couvre l'objet ({part:.0%} de pixels d'objet sous elle) : à poser sur le crème")
        annotations = fd.get("annotations", [])
        for (a, b) in etiquettes_qui_se_recouvrent(annotations):
            m.append(f"findings-{outil_id}.json, finding {fd.get('num', i + 1)} : les étiquettes « {annotations[a][4][:30]}… » "
                     f"et « {annotations[b][4][:30]}… » se recouvrent : les écarter")
    return m
