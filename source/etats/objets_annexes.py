#!/usr/bin/env python3
"""Les cinq objets des annexes — un par page, un seul monde.

Le monde est celui du cadenas : aluminium anodisé mat (jamais miroir), UN élément
vert par objet — celui qui porte l'idée de la page —, ombre de contact courte (les
remplissages n'ombragent pas, leçon payée sur le cadenas), même caméra que le reste.

  jetons     Method        deux pièces frappées du même motif : refais la mesure,
                           obtiens la même pièce. Le vert : le motif, identique.
  cle        Questions     ce qui ouvre le cadenas de la page Sécurité. Le vert :
                           l'anneau de tête — encore une boucle.
  poignee    Terms         la poignée de mains (choix d'Arslane) : deux avant-bras
                           géométriques, mains croisées. Un bras vert, un gris.
  enveloppe  Privacy       une enveloppe de métal plié, muette ; la seule marque
                           est la pastille verte du sceau.
  rampe      Accessibility la marche et la rampe qui arrivent AU MÊME niveau.
                           La rampe en vert.

  blender -b -P objets_annexes.py -- --objet cle --sortie /chemin --qualite apercu
"""
import argparse
import math
import sys

import bmesh
import bpy

ap = argparse.ArgumentParser()
ap.add_argument("--objet", required=True,
                choices=["jetons", "cle", "poignee", "maillons", "enveloppe", "rampe"])
ap.add_argument("--sortie", default="/tmp/objet")
ap.add_argument("--qualite", default="apercu", choices=["apercu", "livraison"])
ap.add_argument("--large", type=int, default=700)
ap.add_argument("--azimut", type=float, default=-118.0)
ap.add_argument("--elevation", type=float, default=42.0)
args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
APERCU = args.qualite == "apercu"


def srgb(hexa):
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
    # le grain : un bruit fin module la rugosité autour de sa valeur, et un
    # micro-relief casse la perfection de la primitive
    bruit = nt.nodes.new("ShaderNodeTexNoise")
    bruit.inputs["Scale"].default_value = 38.0
    bruit.inputs["Detail"].default_value = 6.0
    plage = nt.nodes.new("ShaderNodeMapRange")
    plage.inputs["From Min"].default_value = 0.0
    plage.inputs["From Max"].default_value = 1.0
    plage.inputs["To Min"].default_value = max(0.0, rugosite - 0.06)
    plage.inputs["To Max"].default_value = rugosite + 0.06
    nt.links.new(bruit.outputs["Fac"], plage.inputs["Value"])
    nt.links.new(plage.outputs["Result"], p.inputs["Roughness"])
    relief = nt.nodes.new("ShaderNodeBump")
    relief.inputs["Strength"].default_value = 0.06
    nt.links.new(bruit.outputs["Fac"], relief.inputs["Height"])
    nt.links.new(relief.outputs["Normal"], p.inputs["Normal"])
    return m


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

# ── le monde : un studio réel — le métal a quelque chose à réfléchir ────────
monde = bpy.context.scene.world = bpy.data.worlds.new("studio")
monde.use_nodes = True
nw = monde.node_tree
env = nw.nodes.new("ShaderNodeTexEnvironment")
import os as _os
env.image = bpy.data.images.load(
    _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "monde-studio.hdr"))
fond = nw.nodes["Background"]
fond.inputs["Strength"].default_value = 0.85
nw.links.new(env.outputs["Color"], fond.inputs["Color"])
# tourné pour que le grand panneau lumineux du studio frappe les faces caméra
mappage = nw.nodes.new("ShaderNodeMapping")
coords = nw.nodes.new("ShaderNodeTexCoord")
mappage.inputs["Rotation"].default_value[2] = math.radians(150)
nw.links.new(coords.outputs["Generated"], mappage.inputs["Vector"])
nw.links.new(mappage.outputs["Vector"], env.inputs["Vector"])

M_GRIS = matiere("m_gris", srgb("#9aa2ad"), rugosite=0.28, metal=0.88)
M_VERT = matiere("m_vert", srgb("#2f8a60"), rugosite=0.34, metal=0.70)
M_SOMBRE = matiere("m_sombre", srgb("#2b2e28"), rugosite=0.5, metal=0.25)


def beveler(obj, largeur, segments=5):
    b = obj.modifiers.new("bevel", "BEVEL")
    b.width = largeur
    b.segments = segments


def lisser(obj):
    for f in obj.data.polygons:
        f.use_smooth = True


def boite(nom, dims, pos, mat, bevel=0.05):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    o = bpy.context.object
    o.name = nom
    o.scale = dims
    if bevel:
        beveler(o, bevel)
    o.data.materials.append(mat)
    return o


def cylindre(nom, r, depth, pos, mat, rot=(0, 0, 0), bevel=0.03):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r, depth=depth,
                                        location=pos, rotation=rot)
    o = bpy.context.object
    o.name = nom
    if bevel:
        beveler(o, bevel, 4)
    lisser(o)
    o.data.materials.append(mat)
    return o


def tore(nom, R, r, pos, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r,
                                     major_segments=64, minor_segments=32,
                                     location=pos, rotation=rot)
    o = bpy.context.object
    o.name = nom
    lisser(o)
    o.data.materials.append(mat)
    return o


def coin(nom, long_, larg, haut, pos, mat):
    """Un coin (rampe) : le prisme triangulaire construit sommet par sommet."""
    maille = bpy.data.meshes.new(nom)
    bm = bmesh.new()
    v = [bm.verts.new(p) for p in [
        (0, 0, 0), (long_, 0, 0), (long_, larg, 0), (0, larg, 0),
        (long_, 0, haut), (long_, larg, haut)]]
    for idx in [(0, 1, 2, 3), (1, 4, 5, 2), (0, 3, 5, 4), (0, 4, 1), (3, 2, 5)]:
        bm.faces.new([v[i] for i in idx])
    bm.normal_update()
    bm.to_mesh(maille)
    bm.free()
    o = bpy.data.objects.new(nom, maille)
    bpy.context.collection.objects.link(o)
    o.location = pos
    beveler(o, 0.03, 4)
    o.data.materials.append(mat)
    return o


def tube(nom, points, rayon, mat):
    """Un tube plein le long d'une polyligne adoucie — bras, anses, tiges."""
    c = bpy.data.curves.new(nom, type="CURVE")
    c.dimensions = "3D"
    c.bevel_depth = rayon
    c.bevel_resolution = 8
    c.use_fill_caps = True
    sp = c.splines.new("NURBS")
    sp.points.add(len(points) - 1)
    for pt, (x, y, z) in zip(sp.points, points):
        pt.co = (x, y, z, 1)
    sp.use_endpoint_u = True
    sp.order_u = 3
    o = bpy.data.objects.new(nom, c)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    return o


def prisme(nom, sommets, epaisseur, pos, mat, bevel=0.02):
    """Un polygone plat extrudé — rabats, plaques taillées."""
    maille = bpy.data.meshes.new(nom)
    bm = bmesh.new()
    bas = [bm.verts.new((x, y, 0)) for x, y in sommets]
    haut = [bm.verts.new((x, y, epaisseur)) for x, y in sommets]
    bm.faces.new(list(reversed(bas)))
    bm.faces.new(haut)
    n = len(sommets)
    for i in range(n):
        bm.faces.new([bas[i], bas[(i + 1) % n], haut[(i + 1) % n], haut[i]])
    bm.normal_update()
    bm.to_mesh(maille)
    bm.free()
    o = bpy.data.objects.new(nom, maille)
    bpy.context.collection.objects.link(o)
    o.location = pos
    if bevel:
        beveler(o, bevel, 4)
    o.data.materials.append(mat)
    return o


pieces = []

if args.objet == "jetons":
    # Deux pièces frappées : jante en relief, face creusée, le même motif vert
    # frappé au centre — l'identité, pas la ressemblance.
    for i, (x, y) in enumerate([(-0.60, 0.14), (0.60, -0.14)]):
        pieces.append(cylindre(f"corps{i}", 0.5, 0.12, (x, y, 0.06), M_GRIS, bevel=0.03))
        pieces.append(tore(f"jante{i}", 0.44, 0.035, (x, y, 0.115), M_GRIS))
        pieces.append(cylindre(f"face{i}", 0.40, 0.02, (x, y, 0.115), M_GRIS, bevel=0))
        pieces.append(boite(f"m{i}a", (0.34, 0.085, 0.05), (x, y, 0.13), M_VERT, 0.02))
        pieces.append(boite(f"m{i}b", (0.085, 0.34, 0.05), (x, y, 0.13), M_VERT, 0.02))
    cible_z, r_cam = 0.08, 4.3

elif args.objet == "cle":
    # La clé : l'anneau vert (la boucle), un collet tourné, une tige pleine, et
    # UN panneton taillé — les encoches sont dans la pièce, pas des cubes posés.
    pieces.append(tore("anneau", 0.30, 0.085, (-0.78, 0, 0.085), M_VERT))
    pieces.append(cylindre("collet", 0.12, 0.18, (-0.42, 0, 0.085), M_GRIS,
                           rot=(0, math.radians(90), 0), bevel=0.02))
    pieces.append(boite("tige", (1.2, 0.13, 0.13), (0.22, 0, 0.085), M_GRIS, 0.045))
    panneton = prisme("panneton",
        [(0.0, 0.0), (0.42, 0.0), (0.42, -0.34), (0.34, -0.34), (0.34, -0.12),
         (0.26, -0.12), (0.26, -0.26), (0.16, -0.26), (0.16, -0.12),
         (0.08, -0.12), (0.08, -0.20), (0.0, -0.20)],
        0.11, (0.62, 0.065, 0.03), M_GRIS, 0.018)
    pieces.append(panneton)
    cible_z, r_cam = 0.07, 4.3

elif args.objet == "poignee":
    # Quatrième forme, et changement de METHODE : des metaballs — des masses qui
    # fusionnent en une chair lisse. Une main est une masse continue, pas un
    # assemblage de tubes. Vert : bras, paume et quatre doigts qui enveloppent.
    # Gris : bras, paume, et le pouce qui croise par-dessus.
    import mathutils

    def masse(nom, mat, elements):
        mb = bpy.data.metaballs.new(nom)
        mb.resolution = 0.045
        mb.render_resolution = 0.03
        for typ, co, rayon, demi, direction in elements:
            e = mb.elements.new(type=typ)
            e.co = co
            e.radius = rayon
            if typ == "CAPSULE":
                e.size_x = demi
                z = mathutils.Vector((1, 0, 0))
                e.rotation = z.rotation_difference(
                    mathutils.Vector(direction).normalized())
        o = bpy.data.objects.new(nom, mb)
        bpy.context.collection.objects.link(o)
        o.data.materials.append(mat)
        for pg in o.data.polygons if hasattr(o.data, "polygons") else []:
            pg.use_smooth = True
        return o

    vert = masse("main_v", M_VERT, [
        ("CAPSULE", (-0.88, -0.50, 0.38), 0.135, 0.52, (0.86, 0.5, 0.16)),
        ("BALL", (-0.16, -0.06, 0.52), 0.20, 0, None),
        ("CAPSULE", (0.02, 0.10, 0.62), 0.062, 0.16, (0.55, -0.83, -0.2)),
        ("CAPSULE", (0.12, 0.06, 0.60), 0.062, 0.17, (0.55, -0.83, -0.25)),
        ("CAPSULE", (0.21, 0.01, 0.575), 0.06, 0.16, (0.55, -0.8, -0.3)),
        ("CAPSULE", (0.29, -0.05, 0.55), 0.055, 0.14, (0.5, -0.8, -0.35)),
    ])
    gris = masse("main_g", M_GRIS, [
        ("CAPSULE", (0.88, -0.50, 0.38), 0.135, 0.52, (-0.86, 0.5, 0.16)),
        ("BALL", (0.16, -0.02, 0.50), 0.20, 0, None),
        ("CAPSULE", (-0.06, -0.14, 0.60), 0.066, 0.19, (-0.6, 0.75, -0.2)),
    ])
    pieces += [vert, gris]
    cible_z, r_cam = 0.40, 5.0

elif args.objet == "maillons":
    ma = tore("maillon_v", 0.36, 0.095, (-0.26, 0, 0.095), M_VERT)
    mb = tore("maillon_g", 0.36, 0.095, (0.20, 0, 0.34), M_GRIS,
              rot=(math.radians(90), 0, math.radians(16)))
    pieces += [ma, mb]
    for o in pieces:
        o.rotation_euler.z += math.radians(10)
    cible_z, r_cam = 0.18, 4.2

elif args.objet == "enveloppe":
    # L enveloppe : un corps, un VRAI rabat triangulaire posé dessus, la pastille
    # verte du sceau à cheval sur sa pointe — la seule marque de l objet.
    pieces.append(boite("corps", (1.28, 0.9, 0.08), (0, 0, 0.04), M_GRIS, 0.03))
    rabat = prisme("rabat", [(-0.62, 0.44), (0.62, 0.44), (0.0, -0.10)],
                   0.025, (0, 0, 0.08), M_GRIS, 0.012)
    pieces.append(rabat)
    pieces.append(cylindre("sceau", 0.11, 0.05, (0, -0.055, 0.105), M_VERT,
                           bevel=0.015))
    for o in pieces:
        o.rotation_euler.z += math.radians(16)
    cible_z, r_cam = 0.05, 4.0

elif args.objet == "rampe":
    # L accessibilité : un socle commun, DEUX marches, et la rampe verte qui
    # arrive au même palier. Le socle unifie — plus deux primitives qui flottent.
    pieces.append(boite("socle", (2.25, 0.78, 0.07), (-0.18, 0, 0.035), M_GRIS, 0.02))
    pieces.append(boite("marche1", (0.60, 0.62, 0.165), (0.40, 0, 0.152), M_GRIS, 0.03))
    pieces.append(boite("marche2", (0.34, 0.62, 0.165), (0.53, 0, 0.317), M_GRIS, 0.03))
    pieces.append(coin("rampe", 1.26, 0.62, 0.33, (-1.18, -0.31, 0.07), M_VERT))
    for o in pieces:
        o.rotation_euler.z += math.radians(14)
    cible_z, r_cam = 0.18, 5.15

# ── le sol capteur d'ombre, la lumière, la caméra : le monde du cadenas ──────
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
bpy.context.object.is_shadow_catcher = True

bpy.ops.object.light_add(type="SUN", location=(4, -3, 7))
soleil = bpy.context.object
soleil.data.energy = 3.4
soleil.data.angle = math.radians(9)
soleil.rotation_euler = (math.radians(16), 0, math.radians(125))


az, el = math.radians(args.azimut), math.radians(args.elevation)
cible = (0, 0, cible_z)
pos = (r_cam * math.cos(el) * math.cos(az), r_cam * math.cos(el) * math.sin(az),
       cible[2] + r_cam * math.sin(el))
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
print(f"{args.objet} rendu : {sc.render.filepath}")
