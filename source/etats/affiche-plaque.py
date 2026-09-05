#!/usr/bin/env python3
"""LA PLAQUE DE L'AFFICHE D'UN OUTIL : le robot de la couleur, pose « il présente »
(les deux paumes levées portent les chiffres), cadrage et papier de l'étalon du film.

  blender -b -P affiche-plaque.py -- --accent rubis --sortie /tmp/affiche/plaque.png [--apercu]

C'est la frame du film que l'affiche verte a prise (plan 1, les deux hologrammes
tenus) : mêmes briques que cascade-video (galet, cadrage de l'étalon gamme 10,
cyclo papier émissif de la bible), teinte de l'outil posée sur les matières
seulement (poses-rubis.py : ni le pivot ni la caméra ne bougent). Les chiffres
projetés ne sont PAS ici : la carte HTML les pose par-dessus depuis le relevé
(affiche-composer.py), comme la carte c1 du film sur sa plaque.
"""
import argparse
import json
import math
import os
import sys

VIDEO = os.path.join(os.path.expanduser("~"), "Documents", "cascade-video")
sys.path.insert(0, os.path.join(VIDEO, "gammes", "commun"))
import galet          # noqa: E402
import mathutils as mu  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--accent", default="rubis", choices=["rubis", "vert"])
ap.add_argument("--sortie", default="/tmp/affiche/plaque.png")
ap.add_argument("--apercu", action="store_true")
args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])

B = json.load(open(os.path.join(VIDEO, "v9", "bible.json")))
g = galet.construire(large=800)
import bpy  # noqa: E402

sc = g.sc
if not args.apercu:
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 128
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = 0.01
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.denoising_input_passes = "RGB_ALBEDO_NORMAL"
    sc.cycles.seed = 4
    sc.render.use_persistent_data = False        # frames noires en session longue (02/09)
    try:
        bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "METAL"
        sc.cycles.device = "GPU"
    except Exception:
        pass
sc.render.resolution_x = B["format"]["largeur"]
sc.render.resolution_y = B["format"]["hauteur"]
sc.render.film_transparent = False
sc.view_settings.view_transform = "AgX"
try:
    sc.view_settings.look = "AgX - Base Contrast"
except Exception:
    pass
sc.view_settings.exposure = B["image"]["exposition"]

# ── la teinte de l'outil, sur les matières seulement (le look « pierre » du site) ──
def teinter_bsdf(p, hexa, emission=None):
    c = g.srgb(hexa)
    p.inputs["Base Color"].default_value = c
    if emission is not None:
        p.inputs["Emission Color"].default_value = c
        p.inputs["Emission Strength"].default_value = emission


if args.accent == "rubis":
    teinter_bsdf(g.ANT_BSDF, "#7a0f1f", emission=0.12)
    g.ANT_BSDF.inputs["Roughness"].default_value = 0.18
    g.ANT_BSDF.inputs["Metallic"].default_value = 0.35
    teinter_bsdf(g.M_VERT.node_tree.nodes["Principled BSDF"], "#8e1626")
    yeux = "#ffb3bd"          # il PROJETTE : les yeux prennent la couleur de l'outil (film : #3fe087)
else:
    yeux = "#3fe087"
for oeil in g.YEUX:
    p = oeil.data.materials[0].node_tree.nodes["Principled BSDF"]
    teinter_bsdf(p, yeux, emission=3.0)

# ── caméra : le cadrage de l'étalon gamme 10 (sf1-plate.py, plan 1) ─────────
cam = sc.camera
az, el, dist = math.radians(-38), math.radians(10), 6.2
cam.location = (dist * math.cos(el) * math.cos(az) + 0.53 * -0.28,
                dist * math.cos(el) * math.sin(az) + 0.85 * -0.28,
                dist * math.sin(el) + 0.22)
cam.data.lens = B["image"]["objectif_mm"]
cam.constraints[0].target.location = (0, 0, 0.34)

# ── le cyclo papier émissif de la bible, mat ────────────────────────────────
MP = B["monde_papier"]
dir_vue = (mu.Vector((0, 0, 0.3)) - mu.Vector(cam.location)).normalized()
bpy.ops.mesh.primitive_plane_add(size=34, location=mu.Vector((0, 0, 0.9)) + 3.4 * dir_vue)
cyclo = bpy.context.object
suivi = cyclo.constraints.new("TRACK_TO")
suivi.target = cam
suivi.track_axis = "TRACK_Z"
suivi.up_axis = "UP_Y"
m_papier = bpy.data.materials.new("m_papier")
m_papier.use_nodes = True
nt = m_papier.node_tree
em = nt.nodes.new("ShaderNodeEmission")
em.inputs["Strength"].default_value = MP["emission_strength"]
sortie_m = nt.nodes["Material Output"]
for lien in list(nt.links):
    if lien.to_node == sortie_m:
        nt.links.remove(lien)
nt.links.new(em.outputs["Emission"], sortie_m.inputs["Surface"])
co = nt.nodes.new("ShaderNodeTexCoord")
ma = nt.nodes.new("ShaderNodeMapping")
s = MP["gradient_scale"]
ma.inputs["Scale"].default_value = (s, s, s)
gr = nt.nodes.new("ShaderNodeTexGradient")
gr.gradient_type = "SPHERICAL"
ra = nt.nodes.new("ShaderNodeValToRGB")
ra.color_ramp.elements[0].color = g.srgb(MP["bords"])
ra.color_ramp.elements[1].position = MP["gradient_pos_clair"]
ra.color_ramp.elements[1].color = g.srgb(MP["poche"])
nt.links.new(co.outputs["Object"], ma.inputs["Vector"])
nt.links.new(ma.outputs["Vector"], gr.inputs["Vector"])
nt.links.new(gr.outputs["Fac"], ra.inputs["Fac"])
nt.links.new(ra.outputs["Color"], em.inputs["Color"])
cyclo.data.materials.append(m_papier)

cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = B["image"]["ouverture"]
cam.data.dof.focus_object = sorted(g.YEUX, key=lambda o: o.name)[0]

# ── la pose : l'étalon héros + les deux paumes levées qui portent les chiffres ──
# (plan 1 du film à la tenue : bras-g +56°, bras-d −56° sur la base héros ; la
# tête revient face caméra, le regard droit)
r = math.radians
Mc = g.matrice("corps", (0, r(1.0), r(-6)), (0, 0, 0.012))
M = {"corps": Mc,
     "tete": Mc @ g.matrice("tete", (r(2.5), 0, r(-11 + 6))),
     "bras-g": Mc @ g.matrice("bras-g", (0, r(-14 + 56), 0)),
     "bras-d": Mc @ g.matrice("bras-d", (0, r(-26 - 56), 0))}
M_dard = g.CV @ mu.Matrix.Rotation(r(-2.5 + 4.0), 4, "Z") @ g.CV.inverted()
for fam, paires in g.BASES.items():
    for o, base in paires:
        m = M[fam] @ base
        if o in g.YEUX:
            m = M[fam] @ M_dard @ base
        o.matrix_basis = m

os.makedirs(os.path.dirname(os.path.abspath(args.sortie)), exist_ok=True)
sc.render.filepath = os.path.abspath(args.sortie)
bpy.ops.render.render(write_still=True)
print(f"plaque {args.accent} : {args.sortie} ({'EEVEE' if args.apercu else 'Cycles'})")
