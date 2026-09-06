#!/usr/bin/env python3
"""THE PROPS OF THE BUYING PATH (pricing page, 10/09) : the objects a bank's reviewer sees cross
the network boundary, rendered in the robots' own studio (galet.construire : same softboxes,
same film, same camera) so they belong to the same room as the robots above them.

  blender -b -P props-tarifs.py -- --objet feuille  --sortie /tmp/props    (a sheet, frontal)
  blender -b -P props-tarifs.py -- --objet feuille3q                        (a sheet, three-quarter)
  blender -b -P props-tarifs.py -- --objet enveloppe                        (a closed envelope)
  blender -b -P props-tarifs.py -- --objet facture                          (a short sheet, a card)
  blender -b -P props-tarifs.py -- --objet plaque                           (the boundary : a dark slab with a lit edge)

The robot is built by construire() and hidden from the render. The PNG is cropped with rogner_v2.py.
"""
import argparse, math, os, sys

sys.path.insert(0, os.path.join(os.path.expanduser("~"), "Documents", "cascade-video", "gammes", "commun"))
import bpy      # noqa: E402
import galet    # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--objet", required=True, choices=["feuille", "feuille3q", "enveloppe", "facture", "plaque"])
ap.add_argument("--sortie", default="/tmp/props")
ap.add_argument("--large", type=int, default=1400)
ap.add_argument("--taa", type=int, default=64)
args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
r = math.radians
g = galet.construire(args.large)
sc = g.sc
sc.eevee.taa_render_samples = args.taa

# the robot leaves the stage
for objs in g.FAMILLES.values():
    for o in objs:
        o.hide_render = True
for o in bpy.data.objects:
    if o.type == "MESH" and any(o in objs for objs in g.FAMILLES.values()):
        o.hide_render = True

PAPIER = g.matiere("papier", g.srgb("#dbd7c5"), 0.72, 0.0)
ONYX = g.matiere("onyx", g.srgb("#141418"), 0.16, 0.4)
LISERE = g.matiere_emissive("lisere-vert", g.srgb("#57b184"), 2.6)

# the camera looks from azimuth -32° : a « frontal » object faces that direction
AZ = r(-32)


def boite(nom, dims, loc, rot, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = nom
    o.scale = dims
    o.rotation_euler = rot
    o.data.materials.append(mat)
    return o


def feuille(frontal=True, haut=0.88, large=0.66, yaw=0.0):
    # a US-letter sheet standing, its face toward the camera, a hair of lean
    rot = (r(90 - 8), 0, AZ + r(90) + r(yaw)) if frontal else (r(90 - 10), 0, AZ + r(90) + r(-26))
    return boite("feuille", (large, haut, 0.006), (0, 0, haut / 2 - 0.30), rot, PAPIER)


if args.objet == "feuille":
    feuille(True)
elif args.objet == "feuille3q":
    feuille(False)
elif args.objet == "facture":
    feuille(True, haut=0.56, large=0.66, yaw=4)
elif args.objet == "enveloppe":
    # a closed envelope, landscape, lying at three-quarter with a faint lift
    e = boite("enveloppe", (0.72, 0.48, 0.03), (0, 0, -0.10), (r(12), 0, AZ + r(90) + r(-18)), PAPIER)
    # the flap : a thin wedge on the face
    boite("rabat", (0.72, 0.26, 0.004), (0, 0.0, -0.10 + 0.018), (r(12), 0, AZ + r(90) + r(-18)), PAPIER)
elif args.objet == "plaque":
    # the boundary : a tall thin dark slab, a lit green edge on its face
    boite("plaque", (0.09, 1.7, 0.09), (0, 0, 0.45), (r(90), 0, AZ + r(90)), ONYX)
    # the lit slit sits proud of the slab face, toward the camera (else it hides inside the slab)
    import math as _m
    dx, dy = 0.05 * _m.cos(AZ), 0.05 * _m.sin(AZ)
    boite("fente", (0.014, 1.62, 0.02), (dx, dy, 0.45), (r(90), 0, AZ + r(90)), LISERE)

os.makedirs(args.sortie, exist_ok=True)
sc.render.filepath = os.path.join(args.sortie, f"prop-{args.objet}.png")
bpy.ops.render.render(write_still=True)
print(f"prop {args.objet} : {sc.render.filepath}")
