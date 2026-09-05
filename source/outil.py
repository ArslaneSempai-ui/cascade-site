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

OUTILS = {
    "routing": {
        "id": "routing",
        "nom": "Routing",
        "sous_dossier": "",             # la racine du site
        "prefixe_racine": "",           # depuis ses pages, la racine est ici
        "question": "Where should the next dollar&nbsp;go?",
        "palette": PALETTE_VERTE,
        "favicon_accent": "%2323543f",
        "robots": ("robot-penche.webp", "robot-agrippe.webp"),
        "releve": _MAISON / "cascade" / "landing.json",     # pas de scellé : garde d'absence seule (historique)
        "outil_chemin": _MAISON / "cascade",
        "depot": "https://github.com/ArslaneSempai-ui/cascade-routing",
    },
    "screening": {
        "id": "screening",
        "nom": "Screening",
        "sous_dossier": "screening/",
        "prefixe_racine": "../",
        "question": "Which matcher suffices, at which&nbsp;threshold?",
        "palette": PALETTE_RUBIS,
        "favicon_accent": "%237a1f2e",
        "robots": ("robot-rubis-penche.webp", "robot-rubis-agrippe.webp"),
        "releve": _MAISON / "cascade-screening" / "releve-public.json",  # scellé, vérifié par lire_releve_scelle
        "outil_chemin": _MAISON / "cascade-screening",
        "depot": "https://github.com/ArslaneSempai-ui/cascade-screening",
    },
}


def lien(outil, cible):
    """Le lien d'une page de CET outil vers une cible de la MAISON (nom source,
    ex. « ENGAGEMENT.html », « rendus/x.webp ») : préfixé pour sortir du
    sous-dossier quand il y en a un. Les liens entre pages d'un même outil ne
    passent pas ici : ils restent nus, sœurs de dossier."""
    return outil["prefixe_racine"] + cible
