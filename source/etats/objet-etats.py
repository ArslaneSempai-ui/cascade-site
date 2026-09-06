#!/usr/bin/env python3
"""LE PLATEAU À JETONS DU VERT, AUX VRAIS CHIFFRES : les cinq états de l'objet du héros Routing.
  python3 objet-etats.py --etat 1 --qualite apercu --sortie /tmp/objet
  python3 objet-etats.py --etat 2 --qualite apercu --sequence 36 --depart=-10,60,1.5 --sortie /tmp/objet
  python3 plumer.py /tmp/objet/objet-01.png ../rendus/etats/objet-01.webp

Les états `rendus/etats/objet-01..05.webp` sont entrés dans le dépôt le 31/08 SANS leur script
(constat du 9/09, BRIEF-CHOREGRAPHIE.md) : ils venaient du skill design-arslane,
`scripts/sequence.py --forme colonnes`, dont le jeu de démonstration EST la matrice du vert du
20/08 (sept paliers × cinq champs, la ligne humaine jamais échantillonnée). Ce script est le
chaînon manquant : il LIT la matrice dans le relevé du site (landing.json, outil.py), écrit le
jeu de données de chaque état, et appelle sequence.py — image seule, ou transition de caméra
(`--sequence`, même contrat que les quatre autres plateaux : la dernière image est le cadrage
de l'état).

Les cinq états, un par finding (batir-hero.py, SCENES et APPELS du vert) :
  1  the gap        : la matrice, le routage publié en vert (name → large, birth/document/
                      country → rules, address → gen-4b), deux zéros orange (rules sur name et
                      address : le palier est aveugle), la ligne humaine creuse
  2  the cheaper    : le routage VISÉ AU FICHIER en vert — gen-4b, rules, rules, rules, gen-4b
                      (README du vert, tableau « what aiming at the file delivers », 54 $)
  3  silence        : les deux zéros orange VIDÉS (l'abstention : une case muette, pas fausse)
  4  what we withhold : rien en vert (les comptes tiennent deux fois, les durées sont retenues)
  5  the engagement : toutes les cases mesurées en vert (16 807 routages parcourus)
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(ICI))          # source/ : outil.py
from outil import OUTILS                           # noqa: E402

SEQUENCE_PY = os.path.join(os.path.expanduser("~"), ".claude", "skills", "design-arslane", "scripts", "sequence.py")
BLENDER = "/Applications/Blender.app/Contents/MacOS/Blender"

ap = argparse.ArgumentParser()
ap.add_argument("--etat", type=int, required=True, choices=[1, 2, 3, 4, 5])
ap.add_argument("--sortie", default="/tmp/objet")
ap.add_argument("--qualite", default="apercu", choices=["apercu", "livraison"])
ap.add_argument("--azimut", type=float, default=-62.0)
ap.add_argument("--elevation", type=float, default=44.0)
ap.add_argument("--marge", type=float, default=1.06)
ap.add_argument("--sequence", type=int, default=0, help="nombre d'images de la transition ; 0 = l'état seul")
ap.add_argument("--depart", default="", help="caméra de départ azimut,elevation,marge")
ap.add_argument("--via", default="", help="point de contrôle azimut,elevation,marge (aller-retour)")
ap.add_argument("--releve", default=None, help="le fichier de chiffres à lire ; défaut : OUTILS['routing']['releve']")
# les cibles et les réglages de coût, passés tels quels à sequence.py (même contrat que les autres plateaux)
ap.add_argument("--cible", default="tout", help="tout | case:i,j | ligne:i | colonne:j")
ap.add_argument("--cible-depart", default="", help="la cible au départ de la transition")
ap.add_argument("--echantillons", type=int, default=0, help="échantillons des images de passage ; 0 = ceux de la qualité")
ap.add_argument("--echantillons-arrivee", type=int, default=0, help="échantillons de la dernière image ; 0 = comme les autres")
ap.add_argument("--large", type=int, default=0, help="largeur de l'image ; 0 = celle de la qualité")
args = ap.parse_args()

# ── LES DONNÉES : lues dans le relevé du site, jamais tapées ─────────────────
releve = os.path.expanduser(args.releve or str(OUTILS["routing"]["releve"]))
L = json.load(open(releve))
TIERS = [t["id"] for t in L["tiers"]]
CHAMPS = list(L["fields"])
def valeur(t, f):
    # landing.json porte DÉJÀ des pour cent (79.7 = 79,7 %) : multiplié par 100 le 9/09, le plateau
    # rendait des piles cent fois trop hautes et une image vide ; refusé au lieu de deviner
    a = t["acc"][f].get("accuracy")
    if a is None:
        return None
    if not 0 <= a <= 100:
        sys.exit(f"[objet] accuracy hors de [0, 100] pour {t['id']}/{f} : {a} ; landing.json est en pour cent")
    return round(a, 1)
VALEURS = [[valeur(t, f) for f in CHAMPS] for t in L["tiers"]]
PUBLIE = {f: L["routing"]["fields"][f] for f in CHAMPS}
# le routage visé au fichier n'est pas dans landing.json : il vient du README du vert
# (tableau « what aiming at the file delivers », 54 $ le millier), recopié ici avec sa source
VISE_FICHIER = {"name": "gen-4b", "birth": "rules", "document": "rules", "country": "rules", "address": "gen-4b"}
for f, t in VISE_FICHIER.items():
    if t not in TIERS:
        sys.exit(f"[objet] le routage visé au fichier cite un palier inconnu du relevé : {t}")

def cellules(routage):
    return [[TIERS.index(routage[f]), CHAMPS.index(f)] for f in CHAMPS]

if args.etat == 1:
    valeurs, retenu = VALEURS, cellules(PUBLIE)
elif args.etat == 2:
    valeurs, retenu = VALEURS, cellules(VISE_FICHIER)
elif args.etat == 3:
    # l'abstention : une case aveugle (0 %) devient muette — vidée, pas fausse
    valeurs = [[None if v == 0 else v for v in ligne] for ligne in VALEURS]
    retenu = cellules(PUBLIE)
elif args.etat == 4:
    valeurs, retenu = VALEURS, []
else:
    valeurs = VALEURS
    retenu = [[i, j] for i, ligne in enumerate(VALEURS) for j, v in enumerate(ligne) if v is not None]

donnees = {"lignes": TIERS, "colonnes": CHAMPS, "valeurs": valeurs, "retenu": retenu,
           "_source": os.path.basename(releve), "_etat": args.etat}
os.makedirs(args.sortie, exist_ok=True)
fd, chemin_donnees = tempfile.mkstemp(prefix=f"objet-donnees-0{args.etat}-", suffix=".json", dir=args.sortie)
with os.fdopen(fd, "w") as f:
    json.dump(donnees, f, indent=1)

# ── LE RENDU : sequence.py du skill, image seule ou transition ────────────────
commande = [BLENDER, "-b", "-P", SEQUENCE_PY, "--",
            # piles + studio : la forme et la lumière des états du site (comparés côte à côte le 9/09)
            "--forme", "piles", "--donnees", chemin_donnees, "--sortie", args.sortie,
            "--qualite", args.qualite, "--fond", "ombre", "--lumiere", "studio",
            "--cible", args.cible, "--large", str(args.large or 0),
            "--echantillons", str(args.echantillons), "--echantillons-arrivee", str(args.echantillons_arrivee),
            "--azimut", str(args.azimut), "--elevation", str(args.elevation), "--marge", str(args.marge),
            "--prefixe", "objet", "--etat", str(args.etat)]
if args.sequence:
    if not args.depart:
        sys.exit("[objet] --sequence exige --depart=azimut,elevation,marge")
    commande += ["--images", str(args.sequence), f"--depart={args.depart}"]
    if args.via:
        commande += [f"--via={args.via}"]
    if args.cible_depart:
        commande += ["--cible-depart", args.cible_depart]
else:
    commande += ["--images", "1"]
print("[objet]", " ".join(os.path.basename(c) if c.startswith("/") else c for c in commande), flush=True)
code = subprocess.call(commande)
if code != 0:
    sys.exit(f"[objet] sequence.py a rendu {code}")
if not args.sequence:
    # sequence.py nomme l'image seule img-000.png : l'état prend son nom de famille
    os.replace(os.path.join(args.sortie, "img-000.png"), os.path.join(args.sortie, f"objet-0{args.etat}.png"))
    print(f"[objet] état {args.etat} → {args.sortie}/objet-0{args.etat}.png (ouvrir l'image et la regarder)")
else:
    print(f"[objet] transition : {args.sequence} images vers l'état {args.etat} dans {args.sortie}")
