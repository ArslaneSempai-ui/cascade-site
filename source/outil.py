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
        "question": "Where should the next dollar&nbsp;go?",
        "palette": PALETTE_VERTE,
        "favicon_accent": "%2323543f",
        "robots": ("robot-penche.webp", "robot-agrippe.webp"),
        "releve": _MAISON / "cascade" / "landing.json",     # pas de scellé : garde d'absence seule (historique)
        "outil_chemin": _MAISON / "cascade",
        "depot": "https://github.com/ArslaneSempai-ui/cascade-routing",
        # le rideau (deuxième écran) : ce que le pan de CET outil dit de lui, sur
        # TOUTE page ; ses teintes vivent ici parce que la page rubis aliase la
        # palette et que le pan vert doit y rester vert
        "page_hero": "HERO.html",
        "etiquette": "Routing &#183; extraction",
        "pitch": "Seven tiers, from a regular expression to a human, measured on sealed records.",
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
                       "frontier cell: recall on the left, false alerts on the right.",
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
        "etiquette": "Monitoring &#183; transactions",
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
                       "the fiche names: product on the left, behaviour on the right, both under the 0.90 floor.",
        "vif": "#9b6fe0",
        "nuit": ("#241a3a", "#1a1230", "#100b1f"),
    },
    "dossier": {
        "id": "dossier",
        "nom": "Dossier",
        "sous_dossier": "dossier/",
        "prefixe_racine": "../",
        "question": "Is the whole chain measured, sealed and fresh?",
        "palette": PALETTE_ONYX,
        "favicon_accent": "%231c1c22",
        "robots": ("robot-onyx-penche.webp", "robot-onyx-tient.webp"),
        "releve": _MAISON / "cascade-dossier" / "releve-public.json",   # scellé 2497928ec273023c (D1 lu + D2 mesuré)
        "outil_chemin": _MAISON / "cascade-dossier",
        "depot": "https://github.com/ArslaneSempai-ui/cascade-dossier",
        "page_hero": "HERO-DOSSIER.html",
        "etiquette": "Dossier &#183; the regulator&#8217;s piece",
        "pitch": "Four sealed answers, five controls, one dossier a reviewer verifies without us.",
        "robot_rideau": "robot-onyx-tient.webp",        # il tient la pièce
        "affiche": "affiche-dossier.jpg",
        "affiche_encre": "#2a2a31",                    # le gris vif de l'onyx s'efface sur la plaque : l'encre projetée est plus sombre
        "affiche_alt": "The onyx Cascade robot, palms up, projecting two counts from the public dossier: "
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
    return m


def lien(outil, cible):
    """Le lien d'une page de CET outil vers une cible de la MAISON (nom source,
    ex. « ENGAGEMENT.html », « rendus/x.webp ») : préfixé pour sortir du
    sous-dossier quand il y en a un. Les liens entre pages d'un même outil ne
    passent pas ici : ils restent nus, sœurs de dossier."""
    return outil["prefixe_racine"] + cible
