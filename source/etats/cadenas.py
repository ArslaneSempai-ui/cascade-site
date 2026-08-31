#!/usr/bin/env python3
"""Le cadenas de la page Sécurité — un objet NEUF, pas une variation de la plaque.

Demandé par Arslane le 31 août : « un tout autre objet… le plus logique c'est un
cadenas ». Il partage le MONDE du reste — aluminium anodisé mat (jamais miroir :
rugosité ≥ 0,26), ombre de contact réelle dans l'alpha, même caméra (azimut -118,
élévation 42) — mais pas la géométrie. Le vocabulaire des couleurs tient en un
choix : le corps en métal gris, et L'ANSE EN VERT — c'est elle, la boucle qui se
referme, comme chaque appel réseau revient à sa machine.

  blender -b -P cadenas.py -- --sortie /chemin --qualite apercu|livraison --large 700
"""
import argparse
import math
import sys

import bpy

ap = argparse.ArgumentParser()
ap.add_argument("--sortie", default="/tmp/cadenas")
ap.add_argument("--qualite", default="apercu", choices=["apercu", "livraison"])
ap.add_argument("--large", type=int, default=700)
ap.add_argument("--azimut", type=float, default=-118.0)
ap.add_argument("--elevation", type=float, default=42.0)
args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])

APERCU = args.qualite == "apercu"


def srgb(hexa):
    """#rrggbb → linéaire. Sans cette conversion le vert sort délavé (mesuré sur la
    plaque : #14603f posé brut rendait beaucoup trop clair)."""
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    h = hexa.lstrip("#")
    return (lin(int(h[0:2], 16)), lin(int(h[2:4], 16)), lin(int(h[4:6], 16)), 1.0)


def matiere(nom, rgba, rugosite, metal):
    m = bpy.data.materials.new(nom)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = rgba
    p.inputs["Metallic"].default_value = metal
    bruit = nt.nodes.new("ShaderNodeTexNoise")
    bruit.inputs["Scale"].default_value = 38.0
    bruit.inputs["Detail"].default_value = 6.0
    plage = nt.nodes.new("ShaderNodeMapRange")
    plage.inputs["To Min"].default_value = max(0.0, rugosite - 0.06)
    plage.inputs["To Max"].default_value = rugosite + 0.06
    nt.links.new(bruit.outputs["Fac"], plage.inputs["Value"])
    nt.links.new(plage.outputs["Result"], p.inputs["Roughness"])
    relief = nt.nodes.new("ShaderNodeBump")
    relief.inputs["Strength"].default_value = 0.06
    nt.links.new(bruit.outputs["Fac"], relief.inputs["Height"])
    nt.links.new(relief.outputs["Normal"], p.inputs["Normal"])
    return m


# ── scène nue ────────────────────────────────────────────────────────────────
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.samples = 96 if APERCU else 640
sc.cycles.use_denoising = True
sc.render.film_transparent = True
sc.view_settings.view_transform = "Khronos PBR Neutral"
sc.render.resolution_x = args.large
sc.render.resolution_y = args.large
try:
    sc.cycles.device = "GPU"
    bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "METAL"
    for d in bpy.context.preferences.addons["cycles"].preferences.get_devices_for_type("METAL"):
        d.use = True
except Exception:
    pass

# ── le monde : le même studio réel que les objets d'annexes ──────────────────
monde = bpy.context.scene.world = bpy.data.worlds.new("studio")
monde.use_nodes = True
nw = monde.node_tree
env = nw.nodes.new("ShaderNodeTexEnvironment")
import os as _os
env.image = bpy.data.images.load(
    _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "monde-studio.hdr"))
nw.nodes["Background"].inputs["Strength"].default_value = 0.85
nw.links.new(env.outputs["Color"], nw.nodes["Background"].inputs["Color"])
mappage = nw.nodes.new("ShaderNodeMapping")
coords = nw.nodes.new("ShaderNodeTexCoord")
mappage.inputs["Rotation"].default_value[2] = math.radians(150)
nw.links.new(coords.outputs["Generated"], mappage.inputs["Vector"])
nw.links.new(mappage.outputs["Vector"], env.inputs["Vector"])

# ── matières : la famille anodisée de l'identité ─────────────────────────────
M_CORPS = matiere("m_corps", srgb("#9aa2ad"), rugosite=0.28, metal=0.88)
M_ANSE = matiere("m_anse", srgb("#2f8a60"), rugosite=0.34, metal=0.70)
M_SOMBRE = matiere("m_sombre", srgb("#2b2e28"), rugosite=0.5, metal=0.25)


def beveler(obj, largeur, segments=5):
    b = obj.modifiers.new("bevel", "BEVEL")
    b.width = largeur
    b.segments = segments
    for f in obj.data.polygons:
        f.use_smooth = False


def lisser(obj):
    for f in obj.data.polygons:
        f.use_smooth = True


# ── le cadenas ───────────────────────────────────────────────────────────────
# Le corps : une dalle biseautée, posée au sol — l'ombre de contact est réelle.
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.45))
corps = bpy.context.object
corps.scale = (1.06, 0.42, 0.9)
beveler(corps, 0.07, 6)
corps.data.materials.append(M_CORPS)

# L'anse : un tore debout, ses jambes plongent dans le corps. C'est ELLE qui est
# verte : la boucle refermée.
bpy.ops.mesh.primitive_torus_add(
    major_radius=0.33, minor_radius=0.072,
    major_segments=64, minor_segments=32,
    location=(0, 0, 0.98), rotation=(math.radians(90), 0, 0))
anse = bpy.context.object
lisser(anse)
anse.data.materials.append(M_ANSE)

# L'entrée de clé : un cercle sombre en creux et sa fente, sur la face avant.
bpy.ops.mesh.primitive_cylinder_add(
    vertices=48, radius=0.065, depth=0.03,
    location=(0, -0.215, 0.42), rotation=(math.radians(90), 0, 0))
trou = bpy.context.object
lisser(trou)
trou.data.materials.append(M_SOMBRE)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.215, 0.3))
fente = bpy.context.object
fente.scale = (0.045, 0.03, 0.17)
fente.data.materials.append(M_SOMBRE)

# Une inclinaison franche, cousine de la plaque du héros.
for o in (corps, anse, trou, fente):
    o.rotation_euler.z += math.radians(22)
    o.select_set(True)
bpy.ops.object.transform_apply(rotation=True)

# ── le sol capteur d'ombre ───────────────────────────────────────────────────
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
sol = bpy.context.object
sol.is_shadow_catcher = True

# ── la lumière du studio ─────────────────────────────────────────────────────
bpy.ops.object.light_add(type="SUN", location=(4, -3, 7))
soleil = bpy.context.object
soleil.data.energy = 3.4
soleil.data.angle = math.radians(9)
soleil.rotation_euler = (math.radians(16), 0, math.radians(125))


# ── la caméra, aux angles du héros ───────────────────────────────────────────
az = math.radians(args.azimut)
el = math.radians(args.elevation)
r = 4.6
cible = (0, 0, 0.62)
pos = (r * math.cos(el) * math.cos(az), r * math.cos(el) * math.sin(az),
       cible[2] + r * math.sin(el))
bpy.ops.object.camera_add(location=pos)
cam = bpy.context.object
cam.data.lens = 72
sc.camera = cam
bpy.ops.object.empty_add(location=cible)
mire = bpy.context.object
suivi = cam.constraints.new("TRACK_TO")
suivi.target = mire
suivi.track_axis = "TRACK_NEGATIVE_Z"
suivi.up_axis = "UP_Y"

sc.render.filepath = f"{args.sortie}/img-000.png"
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGBA"
bpy.ops.render.render(write_still=True)
print(f"cadenas rendu : {sc.render.filepath}")
