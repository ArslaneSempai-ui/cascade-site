#!/usr/bin/env python3
"""LES TÉMOINS DES GARDES DE SÉQUENCES (lot M-C1) — chaque garde rougit, prouvé ici.

Un arbre de séquences FACTICE est construit dans un dossier temporaire (de vrais en-têtes
VP8L, deux images par transition), puis mué défaut par défaut : sceau changé, image
retirée, état remplacé, taille menteuse, budget dépassé, budget non déclaré. La garde qui
ne voit plus son défaut fait échouer CE script — et l'assembleur refuse d'émettre tant
qu'un témoin est rouge : un zéro de manques() ne se croit qu'après.

Sceau et budget sont INJECTÉS (paramètres de manques_sequences) : aucun témoin ne dépend
de la valeur du jour de BUDGET_SEQUENCE_KO ni d'un relevé de la maison — la leçon du
mauvais rouge (un témoin qui fige l'état transitoire rougit le jour où l'état avance).
"""
import json
import pathlib
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from outil import manques_sequences, taille_webp   # noqa: E402

SCEAU = "cafe0123cafe0123"
PREFIXE = "rack"          # monitoring : un préfixe réel, pour que ETATS_PREFIXE le connaisse
N, TRANSITIONS = 2, 5


def webp_vp8l(large, haut, bourrage=0):
    """Un webp VP8L minimal : en-tête vrai (la garde lit les pixels), corps sans intérêt."""
    bits = (large - 1) | ((haut - 1) << 14)
    donnees = b"\x2f" + bits.to_bytes(4, "little") + b"\x00" * (5 + bourrage)
    tranche = b"VP8L" + len(donnees).to_bytes(4, "little") + donnees + (b"\x00" if len(donnees) % 2 else b"")
    return b"RIFF" + (4 + len(tranche)).to_bytes(4, "little") + b"WEBP" + tranche


def arbre_sain(base):
    """Le témoin NÉGATIF d'abord : un arbre complet et cohérent, manques vide."""
    seq = base / "rendus" / "sequences" / PREFIXE
    etats = base / "rendus" / "etats"
    seq.mkdir(parents=True)
    etats.mkdir(parents=True)
    for k in range(1, TRANSITIONS + 1):
        for i in range(N):
            (seq / f"{PREFIXE}-seq-0{k}-{i:03d}.webp").write_bytes(webp_vp8l(916, 747, bourrage=k + i))
        shutil.copyfile(seq / f"{PREFIXE}-seq-0{k}-{N - 1:03d}.webp", etats / f"{PREFIXE}-0{k}.webp")
    (seq / "manifest.json").write_text(json.dumps({
        "prefixe": PREFIXE, "n": N, "transitions": TRANSITIONS, "ext": ".webp",
        "large": 916, "haut": 747, "mouvement": 0.66, "sceau": SCEAU,
    }))
    return seq, etats


def cas(nom, attendu_dans, muer):
    """Un arbre sain, une mutation, et la garde DOIT nommer le défaut."""
    with tempfile.TemporaryDirectory(prefix="temoin-seq-") as t:
        base = pathlib.Path(t)
        seq, etats = arbre_sain(base)
        injecte = muer(base, seq, etats)
        m = manques_sequences("monitoring", base, sceau_attendu=SCEAU,
                              **(injecte if isinstance(injecte, dict) else {"budget_ko": 10_000}))
        if attendu_dans is None:
            if m:
                sys.exit(f"TÉMOIN « {nom} » : manques devrait être vide, il dit {m}")
        elif not any(attendu_dans in ligne for ligne in m):
            sys.exit(f"TÉMOIN « {nom} » : la garde n'a pas vu son défaut (« {attendu_dans} » absent de {m})")
        print(f"  témoin ok : {nom}")


# ── le lecteur d'en-têtes, dans les deux sens ────────────────────────────────────────────
assert taille_webp.__doc__  # le module est bien chargé
with tempfile.TemporaryDirectory() as _t:
    _f = pathlib.Path(_t) / "x.webp"
    _f.write_bytes(webp_vp8l(1374, 1120))
    if taille_webp(_f) != (1374, 1120):
        sys.exit(f"TÉMOIN « lecteur vp8l » : {taille_webp(_f)} lu, (1374, 1120) écrit")
    _f.write_bytes(b"RIFF\x00\x00\x00\x00WEBPXXXX" + b"\x00" * 20)
    if taille_webp(_f) is not None:
        sys.exit("TÉMOIN « en-tête inconnu » : un fourcc inconnu doit rendre None, pas deviner")
print("  témoin ok : lecteur d'en-têtes webp (endroit et envers)")

# ── la ligne de base verte, et l'absence qui n'est pas un défaut ─────────────────────────
cas("arbre sain : manques vide", None, lambda base, seq, etats: None)
cas("pas de manifeste : pas de séquences, pas un outil cassé", None,
    lambda base, seq, etats: (seq / "manifest.json").unlink())

# ── chaque garde rougit sur SON défaut ───────────────────────────────────────────────────
cas("fraîcheur : sceau d'un autre relevé", "séquences rendues sur un autre relevé",
    lambda base, seq, etats: (seq / "manifest.json").write_text(
        (seq / "manifest.json").read_text().replace(SCEAU, "beef4567beef4567")))
cas("complétude : une image retirée", "image manquante",
    lambda base, seq, etats: (seq / f"{PREFIXE}-seq-03-000.webp").unlink())
cas("complétude : une taille qui ment", "le manifeste dit 916×747",
    lambda base, seq, etats: (seq / f"{PREFIXE}-seq-02-001.webp").write_bytes(webp_vp8l(400, 300)))
cas("complétude : le déluge est résumé", "autre(s) défaut(s) de complétude",
    lambda base, seq, etats: [(seq / f"{PREFIXE}-seq-0{k}-{i:03d}.webp").unlink()
                              for k in range(1, 5) for i in range(N)])
cas("identité : l'état n'est plus la dernière image", "n'est pas la dernière image",
    lambda base, seq, etats: (etats / f"{PREFIXE}-04.webp").write_bytes(webp_vp8l(916, 747, bourrage=99)))
cas("identité : l'état remplacé par la 2e image ment aussi", "n'est pas la dernière image",
    lambda base, seq, etats: shutil.copyfile(seq / f"{PREFIXE}-seq-01-000.webp", etats / f"{PREFIXE}-01.webp"))
cas("poids : le budget déclaré est dépassé", "le budget déclaré est 0.3 Ko",
    lambda base, seq, etats: {"budget_ko": 0.3})
cas("poids : un budget non déclaré refuse les séquences livrées", "BUDGET_SEQUENCE_KO non déclaré",
    lambda base, seq, etats: {"budget_ko": None})
cas("manifeste : une clé absente est nommée", "clé(s) absente(s) : sceau",
    lambda base, seq, etats: (seq / "manifest.json").write_text(json.dumps(
        {k: v for k, v in json.loads((seq / "manifest.json").read_text()).items() if k != "sceau"})))

print("témoins des gardes de séquences : tous verts (11)")
