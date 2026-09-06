#!/usr/bin/env python3
"""THE DAYS, AS A SCENE (pricing page, 10/09) : the buying path rendered in the robots' studio and
scrubbed by the buyer's own hand. One frame per step of the day axis (units 0..150 : days 0..130
to scale, then month 12) ; the page shows the frame of the current unit and overlays the live text.

  blender -b -P scene-tarifs.py -- --unite 52 --sortie /tmp/scene            (one frame, to judge)
  blender -b -P scene-tarifs.py -- --sequence 36 --sortie /tmp/scene         (the sequence)

Objects, along X (one unit of the axis = 0.04 Blender units, the stage runs 0..6) :
  the tool (the robot, salute pose) at day 0 ; the counter (a chrome ring whose thirty ticks light
  as the days pass) at day 30 ; at the signature (45) the engagement letter and the commercial
  licence land ; the invoice on signature stands behind them ; the sealed report at 76 ; the
  balance invoice at 105 ; the renewal card at 150. The faces of the papers are printed textures
  (scratchpad/tarifs-scene/faces/*.png). Same softboxes, same film, the camera pulled back.
"""
import argparse, math, os, sys

sys.path.insert(0, os.path.join(os.path.expanduser("~"), "Documents", "cascade-video", "gammes", "commun"))
import bpy      # noqa: E402
import galet    # noqa: E402
import mathutils as mu  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--unite", type=float, default=None)
ap.add_argument("--sequence", type=int, default=0)
ap.add_argument("--sortie", default="/tmp/scene")
ap.add_argument("--faces", default=os.path.join("/private/tmp/claude-501/-Users-arslanechr-Downloads-atlas-final-en-fr/9eaa6456-ea12-48c5-bd77-6279f40c9def/scratchpad/tarifs-scene/faces"))
ap.add_argument("--large", type=int, default=1800)
ap.add_argument("--haut", type=int, default=680)
ap.add_argument("--taa", type=int, default=48)
args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
r = math.radians
g = galet.construire(1400)
sc = g.sc
sc.eevee.taa_render_samples = args.taa
sc.render.resolution_x, sc.render.resolution_y = args.large, args.haut

# ── the robot salutes at day 0 (the routing pose), moved to the left of the stage ──────────────
def poser(corps=(0, 0, 0), loc=(0, 0, 0), tete=(0, 0, 0), bg=(0, 0, 0), bd=(0, 0, 0), dard=0.0):
    Mc = g.matrice("corps", tuple(map(r, corps)), loc)
    M = {"corps": Mc, "tete": Mc @ g.matrice("tete", tuple(map(r, tete))),
         "bras-g": Mc @ g.matrice("bras-g", tuple(map(r, bg))), "bras-d": Mc @ g.matrice("bras-d", tuple(map(r, bd)))}
    M_dard = g.CV @ mu.Matrix.Rotation(r(dard), 4, "Z") @ g.CV.inverted()
    for fam, paires in g.BASES.items():
        for o, base in paires:
            m = M[fam] @ base
            if o in g.YEUX:
                m = M[fam] @ M_dard @ base
            o.matrix_basis = m

for oeil in g.YEUX:
    p = oeil.data.materials[0].node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = g.srgb("#bff0d6"); p.inputs["Emission Color"].default_value = g.srgb("#bff0d6"); p.inputs["Emission Strength"].default_value = 2.4
SALUT = dict(corps=(0, 1.5, -4), tete=(1, 0, 3), bg=(0, 6, 0), bd=(14, -128, 0), dard=0.0)
poser(**SALUT)
# the robot is parented to a pivot at the origin (galet) : move that pivot to the left of the stage
pivot = next(o for o in bpy.data.objects if o.type == "EMPTY" and any(ch in [x for objs in g.FAMILLES.values() for x in objs] for ch in o.children))
ECH = 0.04                      # one unit of the axis, in Blender units
def X(u): return u * ECH
pivot.location = (X(0) + 0.42, 0.0, 0.0)
pivot.scale = (0.82, 0.82, 0.82)

# ── materials ──────────────────────────────────────────────────────────────────────────────────
SOL = g.matiere("sol", g.srgb("#040405"), 1.0, 0.0)
PAPIER = g.matiere("papier", g.srgb("#b9b39f"), 0.7, 0.0)
CHROME = g.matiere("chrome", g.srgb("#b8bcc4"), 0.22, 1.0)
VERT = g.matiere_emissive("vert", g.srgb("#57b184"), 2.2)
ETEINT = g.matiere("eteint", g.srgb("#23262a"), 0.5, 0.3)
FANTOME = g.matiere("fantome", g.srgb("#2c2e33"), 0.85, 0.0)
FACES = {}     # face plane name -> its printed material (Blender objects take no ad hoc attributes)


def matiere_face(nom, chemin):
    m = bpy.data.materials.new(nom); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes["Principled BSDF"]
    p.inputs["Roughness"].default_value = 0.68
    tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = bpy.data.images.load(chemin)
    mix = nt.nodes.new("ShaderNodeMixRGB"); mix.blend_type = "MULTIPLY"; mix.inputs["Fac"].default_value = 1.0
    mix.inputs["Color2"].default_value = (0.58, 0.58, 0.58, 1.0)
    nt.links.new(tex.outputs["Color"], mix.inputs["Color1"]); nt.links.new(mix.outputs["Color"], p.inputs["Base Color"])
    return m


# the ground : a wide dark plane that receives the shadows, the page's own black
bpy.ops.mesh.primitive_plane_add(size=400, location=(3.0, 0.0, -0.40))
sol = bpy.context.object; sol.data.materials.append(SOL)


def feuille(nom, u, larg, haut, face, dx=0.0, dy=0.0, dz=0.0, incl=-14.0, yaw=0.0, epaisseur=0.008):
    """A sheet standing on the ground, leaning back a little, its printed face toward the camera."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(X(u) + dx, dy, -0.40 + haut / 2 + dz))
    o = bpy.context.object; o.name = nom
    o.scale = (larg, epaisseur, haut)
    o.rotation_euler = (r(incl), 0, r(yaw))
    o.data.materials.append(PAPIER)
    # the face : a plane just in front of the sheet, with the printed texture
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    f = bpy.context.object; f.name = nom + "-face"
    f.scale = (larg * 0.985, haut * 0.985, 1)
    f.rotation_euler = (r(90), 0, 0)
    f.parent = o
    f.matrix_parent_inverse = mu.Matrix.Identity(4)
    f.location = (0, -0.6, 0)           # in the sheet's local space (y is thickness) : just in front
    f.scale = (0.985, 0.985, 1)
    FACES[f.name] = matiere_face(nom + "-mat", os.path.join(args.faces, face))
    f.data.materials.append(FACES[f.name])
    return o


def cadran(u):
    """The counter : a chrome ring standing at day 30, thirty ticks that light as the days pass."""
    bpy.ops.mesh.primitive_torus_add(location=(X(u), 0.0, 0.02), major_radius=0.36, minor_radius=0.038, major_segments=64, minor_segments=16)
    t = bpy.context.object; t.name = "cadran"; t.rotation_euler = (r(90), 0, 0); t.data.materials.append(CHROME)
    ticks = []
    for i in range(30):
        a = r(90 - i * 12)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(X(u) + 0.285 * math.cos(a), -0.05, 0.02 + 0.285 * math.sin(a)))
        k = bpy.context.object; k.name = f"tick-{i:02d}"; k.scale = (0.022, 0.012, 0.05)
        k.rotation_euler = (0, a - r(90), 0)
        k.data.materials.append(ETEINT)
        ticks.append(k)
    return t, ticks


# ── the objects ────────────────────────────────────────────────────────────────────────────────
cadran_o, TICKS = cadran(30)
LETTRE = feuille("lettre", 45, 0.58, 0.74, "lettre.png", dx=0.08, yaw=6)
LICENCE = feuille("licence", 45, 0.58, 0.74, "licence.png", dx=0.74, yaw=-5)
FACTURE = feuille("facture", 45, 0.58, 0.41, "facture.png", dx=0.41, dy=0.46, dz=0.02, incl=-22, yaw=2)
RAPPORT = feuille("rapport", 76, 0.58, 0.74, "rapport.png", dx=0.34, dy=0.30, yaw=-8)
SOLDE = feuille("solde", 105, 0.58, 0.41, "solde.png", yaw=4)
RENOUV = feuille("renouvellement", 150, 0.54, 0.38, "renouvellement.png", dx=-0.34, yaw=-10)
APPARITIONS = [(LETTRE, 45), (LICENCE, 45), (FACTURE, 46), (RAPPORT, 76), (SOLDE, 105), (RENOUV, 150)]

# ── the camera : pulled back, almost frontal, a little elevation, the whole stage in frame ────
cam = sc.camera
cam.constraints.clear()
cible = (X(76), 0.0, 0.08)
az, el, dist = r(-6), r(10), 9.1
cam.location = (cible[0] + dist * math.cos(el) * math.sin(az), cible[1] - dist * math.cos(el) * math.cos(az), cible[2] + dist * math.sin(el))
cam.data.lens = 50
direction = mu.Vector(cible) - cam.location
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
sc.render.film_transparent = True
# the key light follows the stage : lift the softboxes above the middle of the axis
for l in bpy.data.objects:
    if l.type == "LIGHT":
        l.location = (l.location.x + X(75), l.location.y, l.location.z + 0.6)
        l.data.energy *= 0.8


def etat(u):
    """What the stage shows at axis unit u : the ticks lit, the papers present or hidden below."""
    jour = u if u <= 130 else 130 + (u - 130) / 20 * 235
    for i, k in enumerate(TICKS):
        k.data.materials[0] = VERT if jour >= (i + 1) * 1.0 and i < 30 and jour >= i + 1 else ETEINT
    for o, seuil in APPARITIONS:
        present = u >= seuil - 0.5
        o.data.materials[0] = PAPIER if present else FANTOME
        for ch in o.children:
            ch.data.materials[0] = FACES[ch.name] if present else FANTOME
        o.delta_location = (0, 0, 0)
        if present:
            # a small settle : the paper arrives from 6 cm above during the two units after its date
            reste = max(0.0, min(1.0, (seuil + 2 - u) / 2.0)) if u < seuil + 2 else 0.0
            o.delta_location = (0, 0, 0.06 * reste)


os.makedirs(args.sortie, exist_ok=True)
if args.sequence:
    n = args.sequence
    for i in range(n):
        u = i / (n - 1) * 150
        etat(u)
        sc.render.filepath = os.path.join(args.sortie, f"jours-{i:02d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"image {i:02d} · unité {u:.1f}")
else:
    u = 52.0 if args.unite is None else args.unite
    etat(u)
    sc.render.filepath = os.path.join(args.sortie, f"jours-u{int(u):03d}.png")
    bpy.ops.render.render(write_still=True)
    print(f"image unique · unité {u} · {sc.render.filepath}")
