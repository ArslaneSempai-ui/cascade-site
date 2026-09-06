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

MARGE = 90       # largeur de la rampe, en pixels, depuis chaque bord (--marge N pour un objet cadré serré)
SEUIL = 6        # alpha (sur 255) sous lequel un pixel est éteint
OPAQUE = 200     # un pixel au-dessus est « de l'objet » : il ne doit pas être dans la marge
# --coupe : la coupe est VOULUE (un gros plan sur une pièce, chorégraphie du 9/09) ; l'objet
# peut toucher le bord : aucun refus, et la rampe ne touche pas les pixels d'objet — elle plume
# encore le voile du capteur d'ombre et l'ombre jusqu'au bord.
COUPE = False
if "--coupe" in sys.argv:
    COUPE = True
    sys.argv.remove("--coupe")
if "--marge" in sys.argv:
    # le rack lapis remplit son cadre (rack-etats.py, marge caméra 1.07) : à 90 px de rampe
    # il serait refusé, à 40 le voile s'efface encore sans contour (vu sur le parchemin)
    k = sys.argv.index("--marge")
    MARGE = int(sys.argv[k + 1])
    del sys.argv[k:k + 2]
    if not 20 <= MARGE <= 200:
        sys.exit(f"--marge {MARGE} : entre 20 et 200 px, sinon la rampe ne plume rien ou tout")
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
        # coupe voulue : la rampe plume le voile et l'ombre jusqu'au bord, JAMAIS l'objet ; une
        # image de gros plan et une image large se plument donc de la même façon (pas de saut
        # de bord d'une image à l'autre dans une séquence)
        a = int(a * f) if not (COUPE and a >= OPAQUE) else a
        px[i] = 0 if a < SEUIL else a
if objet_en_marge and not COUPE:
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
print(f"{src.name} → {dst} ({dst.stat().st_size} o), " + (f"coupe voulue, rampe {MARGE} px hors objet" if COUPE else f"rampe {MARGE} px") + f", seuil {SEUIL}")
