#!/usr/bin/env python3
"""Le témoin de la garde « les étiquettes sur le crème » (outil.etiquette_sur_objet) : une image
factice, un carré opaque au centre ; une étiquette posée sur le carré doit être vue, une
étiquette dans un coin doit passer. Un témoin qui ne rougit plus arrête l'émission."""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from outil import etiquette_sur_objet, SEUIL_OBJET, CHIP_DEMI, IW_ANNOT  # noqa: E402

W, H = 1374, 1120
px = bytearray(W * H * 4)
for y in range(H // 3, 2 * H // 3):
    for x in range(W // 3, 2 * W // 3):
        i = (y * W + x) * 4
        px[i:i + 4] = b"\x20\x20\x20\xff"
with tempfile.TemporaryDirectory() as d:
    png, webp = os.path.join(d, "t.png"), os.path.join(d, "t.webp")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-i", "-", png], input=bytes(px), check=True)
    subprocess.run(["cwebp", "-quiet", "-q", "80", png, "-o", webp], check=True)
    dessus = etiquette_sur_objet(webp, 0.5, 0.5)
    coin = etiquette_sur_objet(webp, 0.08, 0.06)
    hors = etiquette_sur_objet(webp, 0.02, 0.5)   # à cheval sur la marge de l'image : du crème
    # le seuil ET l'échelle (relecture de Mesure) : une chip à cheval sur le bord GAUCHE du carré,
    # dont 15 % puis 5 % de la largeur entrent dedans ; si la boîte de la chip dérivait d'échelle,
    # ces deux parts bougeraient et l'une des deux pinces lâcherait
    demi_l = CHIP_DEMI[0] / IW_ANNOT          # demi-largeur de la chip, en fraction de l'image
    bord = 1 / 3                              # le bord gauche du carré, en fraction de l'image
    quinze = etiquette_sur_objet(webp, bord + (0.15 - 0.5) * 2 * demi_l, 0.5)
    cinq = etiquette_sur_objet(webp, bord + (0.05 - 0.5) * 2 * demi_l, 0.5)
if not dessus > SEUIL_OBJET:
    sys.exit(f"témoin cassé : une étiquette sur le carré n'est pas vue ({dessus:.0%})")
if not coin < SEUIL_OBJET or not hors < SEUIL_OBJET:
    sys.exit(f"témoin cassé : une étiquette sur le crème est refusée (coin {coin:.0%}, marge {hors:.0%})")
if not (0.12 <= quinze <= 0.18 and quinze > SEUIL_OBJET):
    sys.exit(f"témoin cassé : la chip à 15 % dans le carré donne {quinze:.0%} (échelle ou seuil dérivés)")
if not (0.03 <= cinq <= 0.07 and cinq < SEUIL_OBJET):
    sys.exit(f"témoin cassé : la chip à 5 % dans le carré donne {cinq:.0%} (échelle ou seuil dérivés)")
print(f"témoin des étiquettes : sur l'objet {dessus:.0%} (vu), coin {coin:.0%}, marge {hors:.0%} (passent), "
      f"bord 15 % → {quinze:.0%} (vu), bord 5 % → {cinq:.0%} (passe)")
