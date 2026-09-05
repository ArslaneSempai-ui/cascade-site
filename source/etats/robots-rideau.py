#!/usr/bin/env python3
"""LES ROBOTS DU RIDEAU : une pose naturelle et DIFFÉRENTE par couleur (Arslane, 6/09 :
« des positions plus naturelles et différentes »).

  blender -b -P robots-rideau.py -- --outil routing   --sortie /tmp/robots
  blender -b -P robots-rideau.py -- --outil screening --sortie /tmp/robots

  vert (routing)    « salue » : debout, la tête tournée vers nous, la main droite levée
  rubis (screening) « curieux » : penché en avant, la tête inclinée, une main qui présente

Mêmes briques que le film et que le site (galet.construire : studio, softbox, film
transparent) ; seules les matières changent avec l'outil (poses-rubis.py, look
« pierre »). Le PNG se rogne ensuite avec rogner_v2.py vers rendus/robot-*.webp.
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.expanduser("~"), "Documents", "cascade-video", "gammes", "commun"))
import bpy      # noqa: E402
import galet    # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--outil", required=True, choices=["routing", "screening"])
ap.add_argument("--sortie", default="/tmp/robots")
ap.add_argument("--large", type=int, default=1400)
ap.add_argument("--taa", type=int, default=64)
args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])

r = math.radians
g = galet.construire(args.large)
sc = g.sc
sc.eevee.taa_render_samples = args.taa


def teinter_bsdf(p, hexa, emission=None):
    c = g.srgb(hexa)
    p.inputs["Base Color"].default_value = c
    if emission is not None:
        p.inputs["Emission Color"].default_value = c
        p.inputs["Emission Strength"].default_value = emission


if args.outil == "screening":
    # le look « pierre » du robot rubis du site
    teinter_bsdf(g.ANT_BSDF, "#7a0f1f", emission=0.12)
    g.ANT_BSDF.inputs["Roughness"].default_value = 0.18
    g.ANT_BSDF.inputs["Metallic"].default_value = 0.35
    teinter_bsdf(g.M_VERT.node_tree.nodes["Principled BSDF"], "#8e1626")
    yeux = "#f3e7e2"
else:
    yeux = "#bff0d6"
for oeil in g.YEUX:
    teinter_bsdf(oeil.data.materials[0].node_tree.nodes["Principled BSDF"], yeux, emission=2.4)


def poser(corps=(0, 0, 0), loc=(0, 0, 0), tete=(0, 0, 0), bg=(0, 0, 0), bd=(0, 0, 0), dard=0.0):
    Mc = g.matrice("corps", tuple(map(r, corps)), loc)
    M = {"corps": Mc,
         "tete": Mc @ g.matrice("tete", tuple(map(r, tete))),
         "bras-g": Mc @ g.matrice("bras-g", tuple(map(r, bg))),
         "bras-d": Mc @ g.matrice("bras-d", tuple(map(r, bd)))}
    import mathutils as mu
    M_dard = g.CV @ mu.Matrix.Rotation(r(dard), 4, "Z") @ g.CV.inverted()
    for fam, paires in g.BASES.items():
        for o, base in paires:
            m = M[fam] @ base
            if o in g.YEUX:
                m = M[fam] @ M_dard @ base
            o.matrix_basis = m


# bras : +y lève le gauche, −y lève le droit (conventions du film, plans 1 et 6)
POSES = {
    # le vert salue : le buste à peine tourné, la tête vers nous, la main droite haute,
    # le bras gauche détendu le long du corps
    # (±64° = bras à l'horizontale ; 0 = le long du corps ; au-delà de 64 le bras monte)
    "routing":   dict(corps=(0, 1.5, -4), tete=(1, 0, 3), bg=(0, 6, 0), bd=(14, -128, 0), dard=0.0),
    # le rubis est curieux : penché en avant, la tête inclinée sur le côté (roulis), le
    # regard vers nous, la main gauche qui présente, la droite posée en retrait
    "screening": dict(corps=(9, 0, 6), tete=(5, 13, -8), bg=(8, 72, 0), bd=(2, -22, 0), dard=0.0),
}
poser(**POSES[args.outil])
os.makedirs(args.sortie, exist_ok=True)
sc.render.filepath = os.path.join(args.sortie, f"robot-{args.outil}.png")
bpy.ops.render.render(write_still=True)
print(f"robot {args.outil} : {sc.render.filepath}")
