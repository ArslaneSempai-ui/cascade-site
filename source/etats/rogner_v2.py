#!/usr/bin/env python3
"""Rogne les rendus de livraison sur leur contenu et plume le bord de l'alpha.

Une SEULE passe : la boîte est calculée et la plume appliquée sur la même
matrice, dans le même processus — la version en deux temps a déjà produit une
boîte périmée quand une assertion avait bloqué l'écriture intermédiaire.

  python3 rogner_v2.py /tmp/liv-cadenas/img-000.png ../rendus/etats/objet-securite.webp
"""
import pathlib
import shutil
import struct
import subprocess
import sys
import tempfile

SEUIL = 16       # alpha au-dessous duquel un pixel est « vide »
MIN_PX = 4       # pixels allumés pour qu'une ligne/colonne compte
MARGE = 14       # marge gardée autour de la boîte
PLUME = 26       # largeur du dégradé d'alpha au bord

src = pathlib.Path(sys.argv[1])
dst = pathlib.Path(sys.argv[2])

sonde = subprocess.run(
    ["ffprobe", "-v", "error", "-select_streams", "v:0",
     "-show_entries", "stream=width,height", "-of", "csv=p=0", str(src)],
    capture_output=True, text=True, check=True)
W, H = (int(x) for x in sonde.stdout.strip().split(","))

brut = subprocess.run(
    ["ffmpeg", "-v", "error", "-i", str(src), "-f", "rawvideo",
     "-pix_fmt", "rgba", "-"],
    capture_output=True, check=True).stdout
assert len(brut) == W * H * 4, f"taille brute inattendue : {len(brut)}"
px = bytearray(brut)

# ── la boîte : lignes et colonnes qui portent au moins MIN_PX pixels ─────────
lignes, colonnes = [0] * H, [0] * W
for y in range(H):
    base = y * W * 4
    for x in range(W):
        if px[base + x * 4 + 3] > SEUIL:
            lignes[y] += 1
            colonnes[x] += 1
ys = [y for y in range(H) if lignes[y] >= MIN_PX]
xs = [x for x in range(W) if colonnes[x] >= MIN_PX]
assert ys and xs, "aucun contenu au-dessus du seuil : rendu vide ?"
y0, y1 = max(0, ys[0] - MARGE), min(H, ys[-1] + 1 + MARGE)
x0, x1 = max(0, xs[0] - MARGE), min(W, xs[-1] + 1 + MARGE)
cw, ch = x1 - x0, y1 - y0

# ── rognage + plume, sur la même matrice ─────────────────────────────────────
sortie = bytearray(cw * ch * 4)
for y in range(ch):
    sy = (y0 + y) * W * 4
    dy = y * cw * 4
    sortie[dy:dy + cw * 4] = px[sy + x0 * 4: sy + x1 * 4]
    bord_y = min(y, ch - 1 - y)
    for x in range(cw):
        bord = min(bord_y, x, cw - 1 - x)
        if bord < PLUME:
            a = sortie[dy + x * 4 + 3]
            sortie[dy + x * 4 + 3] = a * (bord + 1) // (PLUME + 1)

with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
    tmp = pathlib.Path(t.name)
subprocess.run(
    ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
     "-s", f"{cw}x{ch}", "-i", "-", str(tmp)],
    input=bytes(sortie), check=True)

dst.parent.mkdir(parents=True, exist_ok=True)
if shutil.which("cwebp"):
    subprocess.run(["cwebp", "-quiet", "-q", "92", str(tmp), "-o", str(dst)],
                   check=True)
else:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp),
                    "-c:v", "libwebp", "-lossless", "0", "-q:v", "88",
                    str(dst)], check=True)
tmp.unlink()
print(f"{src.parent.name}: {W}x{H} → {cw}x{ch} → {dst} ({dst.stat().st_size} o)")
