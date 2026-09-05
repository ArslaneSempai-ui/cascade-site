#!/usr/bin/env python3
"""Plume l'alpha d'un rendu « ombre » vers les bords, puis écrit le WebP.

  python3 plumer.py /tmp/tamis/tamis-03.png ../rendus/etats/tamis-03.webp

Pourquoi : la tour de tamis est haute et large ; en capteur d'ombre sous un HDRI,
le plan se voile faiblement (alpha 15-27 sur 255, mesuré) jusqu'aux BORDS de
l'image, et sur le parchemin de la séquence ce voile dessine un rectangle : le
cadre du rendu devient visible. Le plateau vert, plat, n'occultait pas assez de
ciel pour que ça se voie (alpha 0 loin de l'objet). Ici l'alpha est multiplié
par une rampe qui tombe à zéro sur les MARGE derniers pixels de chaque bord, et
les alphas résiduels sous SEUIL sont éteints. L'objet ne touche jamais la marge :
la caméra le cadre avec de l'air (tamis-etats.py, marge 1.09) ; le script le
VÉRIFIE et refuse sinon, plutôt que de rogner un socle en silence.
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

MARGE = 90       # largeur de la rampe, en pixels, depuis chaque bord
SEUIL = 6        # alpha (sur 255) sous lequel un pixel est éteint
OPAQUE = 200     # un pixel au-dessus est « de l'objet » : il ne doit pas être dans la marge
# Le voile du capteur d'ombre (alpha 15-27 loin de l'objet) est retiré comme un
# PLANCHER, puis le reste est ré-étalé : l'ombre de contact (alpha 60-255 sous le
# socle) garde son dégradé, le voile disparaît sans contour. Un seuil dur à 30
# aurait dessiné la ligne où le voile s'arrête ; vu sur le parchemin : une tache.
PLANCHER = 30

src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
sonde = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0", str(src)],
                       capture_output=True, text=True, check=True)
W, H = (int(x) for x in sonde.stdout.strip().split(","))
px = bytearray(subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-f", "rawvideo",
                               "-pix_fmt", "rgba", "-"], capture_output=True, check=True).stdout)
assert len(px) == W * H * 4, f"taille brute inattendue : {len(px)}"

rampe = [min(1.0, (i + 1) / (MARGE + 1)) for i in range(max(W, H))]
objet_en_marge = 0
for y in range(H):
    fy = min(rampe[y], rampe[H - 1 - y])
    base = y * W * 4
    for x in range(W):
        i = base + x * 4 + 3
        a = px[i]
        if a == 0:
            continue
        f = min(fy, rampe[x], rampe[W - 1 - x])
        if f < 1.0 and a >= OPAQUE:
            objet_en_marge += 1
        if a < OPAQUE:   # l'objet garde son alpha ; seuls l'ombre et le voile sont ré-étalés
            a = max(0, a - PLANCHER) * 255 // (255 - PLANCHER)
        a = int(a * f)
        px[i] = 0 if a < SEUIL else a
if objet_en_marge:
    sys.exit(f"{src.name} : {objet_en_marge} pixels d'objet dans la marge de {MARGE} px : "
             "le cadrage est trop serré, reculer la caméra plutôt que de plumer l'objet")

with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
    tmp = pathlib.Path(t.name)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
                "-s", f"{W}x{H}", "-i", "-", str(tmp)], input=bytes(px), check=True)
dst.parent.mkdir(parents=True, exist_ok=True)
if not shutil.which("cwebp"):
    sys.exit("cwebp absent (brew install webp)")
subprocess.run(["cwebp", "-quiet", "-q", "92", str(tmp), "-o", str(dst)], check=True)
tmp.unlink()
print(f"{src.name} → {dst} ({dst.stat().st_size} o), rampe {MARGE} px, seuil {SEUIL}")
