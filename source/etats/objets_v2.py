#!/usr/bin/env python3
"""Les objets des annexes, v2 — refaits d'après de VRAIS exemples, pas d'imagination.

Références étudiées le 31 août 2026 : le pack 3dicons de Vijay Verma (CC0, rendus
posés dans etats/refs/), Shapefest. La grammaire du genre, mesurée sur pièces :

  1. GONFLEMENT — le biseau fait 12-18 % de la plus petite dimension ; les tubes
     sont deux fois plus gras qu'un tube « réaliste » ; aucune plaque mince.
  2. POSE DEUX AXES — lacet ~30° ET tangage ~15° : l'objet culbute, il FLOTTE.
     Pas de sol, pas d'ombre de contact. (Leur version « clay » prouve que la
     géométrie porte tout ; la matière vient en second.)
  3. CAMÉRA PROCHE — ~46 mm, élévation ~16°, l'objet remplit le cadre.
  4. GRADIENT SUR CHAQUE FACE — un grand softbox chaud en haut-gauche, un rebond
     froid à droite, un liseré derrière. Jamais une face plate.
  5. DEUX TONS — corps satiné sombre + partie accent : notre gris anodisé + vert.

  cadenas    Security       corps coussin, anse verte — la boucle qui se referme
  balance    Method         deux plateaux AU MÊME NIVEAU : deux passes, même
                            résultat — c'est l'objet qui le dit
  cle        Questions      anneau vert gras, tige pleine, panneton massif
  stylo      Terms          la page épaisse, la signature verte, le stylo posé —
                            l'engagement écrit
  dossier    Privacy        le dossier fermé, ceint d'une sangle verte : vos
                            archives ne partent nulle part
  podium     Accessibility  rampe verte devant, marches derrière, le même palier

  blender -b -P objets_v2.py -- --objet cle --sortie /chemin --qualite apercu
"""
import argparse
import math
import sys

import bpy

ap = argparse.ArgumentParser()
ap.add_argument("--objet", required=True,
                choices=["cadenas", "balance", "cle", "stylo", "dossier", "podium"])
ap.add_argument("--sortie", default="/tmp/objet")
ap.add_argument("--qualite", default="apercu", choices=["apercu", "livraison"])
ap.add_argument("--large", type=int, default=700)
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
    bruit = nt.nodes.new("ShaderNodeTexNoise")
    bruit.inputs["Scale"].default_value = 38.0
    bruit.inputs["Detail"].default_value = 6.0
    plage = nt.nodes.new("ShaderNodeMapRange")
    plage.inputs["To Min"].default_value = max(0.0, rugosite - 0.05)
    plage.inputs["To Max"].default_value = rugosite + 0.05
    nt.links.new(bruit.outputs["Fac"], plage.inputs["Value"])
    nt.links.new(plage.outputs["Result"], p.inputs["Roughness"])
    relief = nt.nodes.new("ShaderNodeBump")
    relief.inputs["Strength"].default_value = 0.04
    nt.links.new(bruit.outputs["Fac"], relief.inputs["Height"])
    nt.links.new(relief.outputs["Normal"], p.inputs["Normal"])
    return m


# ── scène ────────────────────────────────────────────────────────────────────
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

# ── le monde : HDRI de base + trois softbox pour les gradients ───────────────
monde = bpy.context.scene.world = bpy.data.worlds.new("studio")
monde.use_nodes = True
nw = monde.node_tree
env = nw.nodes.new("ShaderNodeTexEnvironment")
import os as _os
env.image = bpy.data.images.load(
    _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "monde-studio.hdr"))
nw.nodes["Background"].inputs["Strength"].default_value = 0.9
nw.links.new(env.outputs["Color"], nw.nodes["Background"].inputs["Color"])
mappage = nw.nodes.new("ShaderNodeMapping")
coords = nw.nodes.new("ShaderNodeTexCoord")
mappage.inputs["Rotation"].default_value[2] = math.radians(150)
nw.links.new(coords.outputs["Generated"], mappage.inputs["Vector"])
nw.links.new(mappage.outputs["Vector"], env.inputs["Vector"])


def softbox(nom, taille, energie, pos, teinte=(1, 1, 1)):
    bpy.ops.object.light_add(type="AREA", location=pos)
    l = bpy.context.object
    l.name = nom
    l.data.size = taille
    l.data.energy = energie
    l.data.color = teinte
    # visée vers l'origine
    d = math.sqrt(pos[0] ** 2 + pos[1] ** 2 + pos[2] ** 2)
    l.rotation_euler = (
        math.acos(pos[2] / d),
        0,
        math.atan2(pos[1], pos[0]) + math.pi / 2,
    )
    bpy.ops.object.empty_add(location=(0, 0, 0))
    mire = bpy.context.object
    c = l.constraints.new("TRACK_TO")
    c.target = mire
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    return l


# la clé chaude en haut-gauche fait le gradient principal ; le rebond froid à
# droite remplit sans écraser ; le liseré derrière détache l'objet du vide
softbox("cle_lum", 5.0, 900, (2.6, -3.0, 3.4), (1.0, 0.97, 0.92))
softbox("rebond", 4.0, 180, (-3.4, -1.0, 0.6), (0.90, 0.94, 1.0))
softbox("lisere", 3.0, 320, (-1.2, 3.2, 2.2), (1.0, 1.0, 1.0))

M_GRIS = matiere("m_gris", srgb("#8d95a1"), rugosite=0.30, metal=0.92)
M_VERT = matiere("m_vert", srgb("#2e9065"), rugosite=0.30, metal=0.75)
M_SOMBRE = matiere("m_sombre", srgb("#23261f"), rugosite=0.45, metal=0.30)
M_PAPIER = matiere("m_papier", srgb("#d8d5c9"), rugosite=0.55, metal=0.05)


def beveler(obj, largeur, segments=10):
    b = obj.modifiers.new("bevel", "BEVEL")
    b.width = largeur
    b.segments = segments


def lisser(obj):
    # tout lisse, puis une coupure d'arête au-delà de 40° : les biseaux fondent,
    # les grands plats restent nets — sans ça le biseau dessine un « cadre »
    for f in obj.data.polygons:
        f.use_smooth = True
    fente = obj.modifiers.new("nettete", "EDGE_SPLIT")
    fente.split_angle = math.radians(40)
    fente.use_edge_angle = True


def boite(dim, pos, mat, biseau=None, seg=10):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    o = bpy.context.object
    o.scale = dim
    # le biseau par défaut : 15 % de la plus petite dimension — la règle du genre
    beveler(o, biseau if biseau else 0.15 * min(dim), seg)
    lisser(o)
    o.data.materials.append(mat)
    return o


def cylindre(r, prof, pos, mat, rot=(0, 0, 0), biseau=None, seg=10):
    bpy.ops.mesh.primitive_cylinder_add(vertices=72, radius=r, depth=prof,
                                        location=pos, rotation=rot)
    o = bpy.context.object
    beveler(o, biseau if biseau else 0.15 * min(r, prof), seg)
    lisser(o)
    o.data.materials.append(mat)
    return o


def tore(maj, mino, pos, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=maj, minor_radius=mino,
                                     major_segments=96, minor_segments=48,
                                     location=pos, rotation=rot)
    o = bpy.context.object
    lisser(o)
    o.data.materials.append(mat)
    return o


def tube(points, rayon, mat):
    """Un boyau lisse le long d'une suite de points — la signature, entre autres."""
    c = bpy.data.curves.new("tube", "CURVE")
    c.dimensions = "3D"
    c.bevel_depth = rayon
    c.bevel_resolution = 10
    c.use_fill_caps = True
    sp = c.splines.new("NURBS")
    sp.points.add(len(points) - 1)
    for k, (x, y, z) in enumerate(points):
        sp.points[k].co = (x, y, z, 1)
    sp.use_endpoint_u = True
    sp.order_u = 3
    o = bpy.data.objects.new("tube", c)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    return o


PIECES = []


def garder(*objs):
    PIECES.extend(objs)


# ── les objets ───────────────────────────────────────────────────────────────
# La caméra vit en (+X, -Y) : une façade tournée d'un lacet POSITIF d'environ
# 25-35° présente son trois-quarts à l'objectif. DIST règle le remplissage.
if args.objet == "cadenas":
    # Le corps : un coussin — profondeur 60 % de la largeur, biseau énorme.
    corps = boite((1.00, 0.60, 0.80), (0, 0, -0.10), M_GRIS, biseau=0.16)
    # L'anse verte : GRASSE (tube ⌀ 0.26), elle plonge dans le corps.
    anse = tore(0.34, 0.13, (0, 0, 0.52), M_VERT, rot=(math.radians(90), 0, 0))
    # L'entrée de clé, sombre, en façade.
    trou = cylindre(0.085, 0.05, (0, -0.315, 0.02), M_SOMBRE,
                    rot=(math.radians(90), 0, 0), biseau=0.012)
    fente = boite((0.075, 0.05, 0.20), (0, -0.315, -0.13), M_SOMBRE, biseau=0.02)
    garder(corps, anse, trou, fente)
    POSE = (math.radians(8), math.radians(-6), math.radians(30))
    DIST = 3.0

elif args.objet == "balance":
    # La balance : deux plateaux AU MÊME NIVEAU. Deux passes, même résultat.
    # Le plateau vert est votre re-mesure ; il pèse exactement pareil.
    socle = cylindre(0.42, 0.18, (0, 0, -0.61), M_GRIS, biseau=0.05)
    colonne = cylindre(0.12, 0.96, (0, 0, -0.065), M_GRIS, biseau=0.035)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(0, 0, 0.44),
                                         segments=48, ring_count=24)
    chapiteau = bpy.context.object
    lisser(chapiteau)
    chapiteau.data.materials.append(M_GRIS)
    fleau = boite((1.34, 0.13, 0.13), (0, 0, 0.42), M_GRIS, biseau=0.05)
    s1 = cylindre(0.065, 0.40, (-0.60, 0, 0.22), M_GRIS, biseau=0.018)
    s2 = cylindre(0.065, 0.40, (0.60, 0, 0.22), M_GRIS, biseau=0.018)
    p1 = cylindre(0.34, 0.12, (-0.60, 0, -0.04), M_GRIS, biseau=0.035)
    p2 = cylindre(0.34, 0.12, (0.60, 0, -0.04), M_VERT, biseau=0.035)
    garder(socle, colonne, chapiteau, fleau, s1, s2, p1, p2)
    POSE = (math.radians(8), math.radians(-6), math.radians(26))
    DIST = 3.3

elif args.objet == "cle":
    # Couchée dans le plan de l'image, anneau en bas-gauche, panneton qui
    # grimpe vers le haut-droit — la diagonale de la référence.
    anneau = tore(0.30, 0.115, (-0.62, 0, 0), M_VERT, rot=(math.radians(90), 0, 0))
    collet = cylindre(0.13, 0.18, (-0.30, 0, 0), M_GRIS,
                      rot=(0, math.radians(90), 0), biseau=0.022)
    tige = cylindre(0.10, 1.10, (0.28, 0, 0), M_GRIS,
                    rot=(0, math.radians(90), 0), biseau=0.035)
    d1 = boite((0.14, 0.09, 0.28), (0.72, 0, -0.18), M_GRIS, biseau=0.03)
    d2 = boite((0.12, 0.09, 0.20), (0.47, 0, -0.14), M_GRIS, biseau=0.028)
    garder(anneau, collet, tige, d1, d2)
    # la tige est le long de X : le roulis (X) fait basculer les dents vers
    # l'objectif, le tangage (Y) fait grimper le panneton en diagonale
    POSE = (math.radians(-14), math.radians(-24), math.radians(14))
    DIST = 3.2

elif args.objet == "stylo":
    # La page épaisse, la signature verte, le stylo posé. L'engagement écrit —
    # « plain terms », noir sur blanc, et la marque verte qui s'y engage.
    page = boite((1.16, 0.84, 0.07), (0, 0, 0), M_GRIS, biseau=0.028)
    # trois lignes de texte : des barres sombres en léger relief, en haut
    for k, lg in enumerate([0.84, 0.84, 0.56]):
        l = boite((lg, 0.055, 0.022), (-0.5 + lg / 2, 0.26 - k * 0.13, 0.045),
                  M_SOMBRE, biseau=0.008)
        garder(l)
    # la signature : un boyau vert qui ondule, posé sur la page, en bas-gauche
    sig = tube([(-0.46, -0.30, 0.075), (-0.30, -0.14, 0.075),
                (-0.16, -0.34, 0.075), (0.02, -0.12, 0.075),
                (0.16, -0.30, 0.075), (0.30, -0.22, 0.075)], 0.032, M_VERT)
    # le stylo : couché en diagonale, dressé de 10°, la pointe posée au bout
    # de la signature. Son axe : Rz(38°)·Ry(80°)·ẑ = (0.776, 0.606, 0.174).
    stylo_rot = (0, math.radians(80), math.radians(38))
    ax = (0.776, 0.606, 0.174)
    bout = (0.32, -0.24, 0.08)

    def le_long(t):
        return (bout[0] + t * ax[0], bout[1] + t * ax[1], bout[2] + t * ax[2])

    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.012, radius2=0.072,
                                    depth=0.20, location=le_long(0.10),
                                    rotation=stylo_rot)
    pointe = bpy.context.object
    lisser(pointe)
    pointe.data.materials.append(M_SOMBRE)
    bague = cylindre(0.076, 0.07, le_long(0.24), M_VERT,
                     rot=stylo_rot, biseau=0.012)
    corps_s = cylindre(0.076, 0.68, le_long(0.56), M_GRIS,
                       rot=stylo_rot, biseau=0.022)
    garder(page, sig, corps_s, pointe, bague)
    POSE = (math.radians(48), 0, math.radians(14))
    DIST = 2.9

elif args.objet == "dossier":
    # La chemise à dossier, entrouverte : le papier dépasse, l'onglet est vert.
    # Vos archives — elles restent dans leur chemise, chez vous.
    fond = boite((1.14, 0.82, 0.07), (0, 0, -0.05), M_GRIS, biseau=0.028)
    papier = boite((1.02, 0.76, 0.05), (0, -0.05, 0.015), M_PAPIER, biseau=0.02)
    # la couverture : charnière au bord arrière, entrouverte de 12°
    bpy.ops.object.empty_add(location=(0, 0.41, 0.05))
    charniere = bpy.context.object
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.41, 0.035))
    couverture = bpy.context.object
    couverture.scale = (1.14, 0.82, 0.07)
    beveler(couverture, 0.028, 10)
    lisser(couverture)
    couverture.data.materials.append(M_GRIS)
    couverture.parent = charniere
    # l'onglet vert, solidaire de la couverture, qui dépasse du bord arrière —
    # côté +X, celui que la caméra voit, et posé AU-DESSUS de la couverture
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.30, 0.14, 0.055))
    onglet = bpy.context.object
    onglet.scale = (0.38, 0.20, 0.06)
    beveler(onglet, 0.022, 8)
    lisser(onglet)
    onglet.data.materials.append(M_VERT)
    onglet.parent = charniere
    charniere.rotation_euler = (math.radians(-12), 0, 0)  # le bord avant se lève
    garder(fond, papier, charniere)
    POSE = (math.radians(16), math.radians(-6), math.radians(28))
    DIST = 3.0

elif args.objet == "podium":
    # Une seule masse : la rampe verte devant, les marches derrière, et les
    # deux arrivent SUR LE MÊME palier. Deux chemins, une arrivée.
    # L'emblème à deux versants : le palier au SOMMET, la rampe verte qui monte
    # à gauche, les marches à droite. La silhouette raconte tout, quel que soit
    # l'angle — c'est l'échec des « voies parallèles » qui l'a appris.
    base = boite((2.20, 0.80, 0.16), (0, 0, -0.40), M_GRIS, biseau=0.05)
    palier = boite((0.50, 0.72, 0.62), (0.10, 0, -0.01), M_GRIS, biseau=0.06)
    # le versant droit : deux marches pleines qui descendent du palier
    m1 = boite((0.25, 0.72, 0.41), (0.475, 0, -0.115), M_GRIS, biseau=0.05)
    m2 = boite((0.25, 0.72, 0.21), (0.725, 0, -0.215), M_GRIS, biseau=0.045)
    # le versant gauche : la rampe verte, d'une pièce, qui MORD le palier
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.585, 0, -0.01))
    rampe = bpy.context.object
    rampe.scale = (1.06, 0.72, 0.13)
    rampe.rotation_euler = (0, math.radians(-35.5), 0)
    beveler(rampe, 0.045, 8)
    lisser(rampe)
    rampe.data.materials.append(M_VERT)
    garder(base, palier, m1, m2, rampe)
    POSE = (math.radians(8), math.radians(-4), math.radians(22))
    DIST = 3.6

# ── la pose deux axes : l'objet culbute, il flotte ───────────────────────────
bpy.ops.object.empty_add(location=(0, 0, 0))
pivot = bpy.context.object
pivot.name = "pivot"
for o in PIECES:
    if o.parent is None:
        o.parent = pivot
pivot.rotation_euler = POSE

# ── la caméra : proche, 46 mm, élévation 16° ─────────────────────────────────
az = math.radians(-32)
el = math.radians(16)
r = DIST
pos = (r * math.cos(el) * math.cos(az), r * math.cos(el) * math.sin(az),
       r * math.sin(el))
bpy.ops.object.camera_add(location=pos)
cam = bpy.context.object
cam.data.lens = 46
sc.camera = cam
bpy.ops.object.empty_add(location=(0, 0, 0))
mire = bpy.context.object
suivi = cam.constraints.new("TRACK_TO")
suivi.target = mire
suivi.track_axis = "TRACK_NEGATIVE_Z"
suivi.up_axis = "UP_Y"

sc.render.filepath = f"{args.sortie}/img-000.png"
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGBA"
bpy.ops.render.render(write_still=True)
print(f"{args.objet} v2 rendu : {sc.render.filepath}")
