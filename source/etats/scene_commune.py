"""LES BRIQUES DE SCÈNE des plateaux (copie publique de equipe-cascade/lookdev_commun.py ; les états
de production les importent d'ici, sans dépendre du dossier privé de l'équipe). Blender 5.2, Cycles, Metal.

  import sys, os; sys.path.insert(0, os.path.expanduser("~/Documents/equipe-cascade"))
  from lookdev_commun import Scene
  sc = Scene(fond="papier", apercu=True); sc.table_rase(); ...

Rien ici ne parse d'arguments : chaque planche garde les siens.
"""
import math
import os
import sys

import bpy
from mathutils import Vector

SKILL = os.path.join(os.path.expanduser("~"), ".claude", "skills", "design-arslane")
HDRI = os.path.join(SKILL, "assets", "hdri")
P_PAPIER = "#dbd7c5"


def srgb(hexa):
    h = hexa.lstrip("#")
    out = []
    for k in (0, 2, 4):
        c = int(h[k:k + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


class Scene:
    def __init__(self, fond="papier", apercu=True):
        self.fond = fond
        self.apercu = apercu
        self.echantillons = 48 if apercu else 256

    # ── le monde ──────────────────────────────────────────────────────────────
    def table_rase(self):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        sc = bpy.context.scene
        sc.render.engine = "CYCLES"
        c = sc.cycles
        c.samples = self.echantillons
        c.use_denoising = True
        c.use_adaptive_sampling = True
        c.adaptive_threshold = 0.005
        c.transmission_bounces = 12
        c.transparent_max_bounces = 12
        c.diffuse_bounces = 3
        c.glossy_bounces = 6
        c.max_bounces = 14
        c.sample_clamp_indirect = 8.0
        c.caustics_reflective = False
        c.caustics_refractive = False
        try:
            bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "METAL"
            c.device = "GPU"
        except Exception:
            c.device = "CPU"
        sc.view_settings.view_transform = "Khronos PBR Neutral"
        sc.view_settings.look = "None"

    def monde_hdri(self, fichier="contraste.hdr", force=1.0, rotation=math.pi * 0.35):
        chemin = os.path.join(HDRI, fichier)
        if not os.path.exists(chemin):
            sys.exit(f"HDRI absent : {chemin}")
        w = bpy.data.worlds.new("monde")
        bpy.context.scene.world = w
        w.use_nodes = True
        nt = w.node_tree
        nt.nodes.clear()
        sortie = nt.nodes.new("ShaderNodeOutputWorld")
        fond = nt.nodes.new("ShaderNodeBackground")
        fond.inputs["Strength"].default_value = force
        env = nt.nodes.new("ShaderNodeTexEnvironment")
        env.image = bpy.data.images.load(chemin)
        map_ = nt.nodes.new("ShaderNodeMapping")
        map_.inputs["Rotation"].default_value[2] = rotation
        coord = nt.nodes.new("ShaderNodeTexCoord")
        nt.links.new(coord.outputs["Generated"], map_.inputs["Vector"])
        nt.links.new(map_.outputs["Vector"], env.inputs["Vector"])
        nt.links.new(env.outputs["Color"], fond.inputs["Color"])
        if self.fond == "ombre":
            nt.links.new(fond.outputs["Background"], sortie.inputs["Surface"])
            bpy.context.scene.render.film_transparent = True
            return
        fond_uni = nt.nodes.new("ShaderNodeBackground")
        fond_uni.inputs["Color"].default_value = (*srgb(P_PAPIER), 1)
        chemin_l = nt.nodes.new("ShaderNodeLightPath")
        melange = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(chemin_l.outputs["Is Camera Ray"], melange.inputs["Fac"])
        nt.links.new(fond.outputs["Background"], melange.inputs[1])
        nt.links.new(fond_uni.outputs["Background"], melange.inputs[2])
        nt.links.new(melange.outputs["Shader"], sortie.inputs["Surface"])

    def lampe_cle(self, position=(-3.5, -4.0, 5.0), energie=1400.0, taille=3.0, couleur="#fff4e2"):
        L = bpy.data.lights.new("cle", "AREA")
        L.energy = energie
        L.size = taille
        L.color = srgb(couleur)
        o = bpy.data.objects.new("cle", L)
        bpy.context.collection.objects.link(o)
        o.location = position
        o.rotation_euler = (Vector((0, 0, 0)) - Vector(position)).to_track_quat("-Z", "Y").to_euler()
        return o

    def sol_papier(self, z=0.0):
        bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, z - 0.002))
        o = bpy.context.object
        o.name = "sol_papier"
        pose(o, matiere("m_papier", P_PAPIER, rugosite=0.94))
        if self.fond == "ombre":
            o.is_shadow_catcher = True

    # ── la caméra ─────────────────────────────────────────────────────────────
    def camera(self, azimut, elevation, focale=60, marge=1.06, ouverture=0.0, r=10.0, boite=None):
        from bpy_extras.object_utils import world_to_camera_view
        mn, mx = boite if boite is not None else boite_du_sujet()
        centre = (mn + mx) / 2
        az, el = math.radians(azimut), math.radians(elevation)
        position = centre + Vector((math.cos(el) * math.cos(az) * r, math.cos(el) * math.sin(az) * r, math.sin(el) * r))
        cam = bpy.data.cameras.new("cam")
        cam.lens = focale
        o = bpy.data.objects.new("cam", cam)
        bpy.context.collection.objects.link(o)
        o.location = position
        bpy.context.scene.camera = o
        direction = centre - position
        o.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
        axe = -direction.normalized()
        coins = [Vector((x, y, z)) for x in (mn.x, mx.x) for y in (mn.y, mx.y) for z in (mn.z, mx.z)]
        for _ in range(240):
            bpy.context.view_layer.update()
            uv = [world_to_camera_view(bpy.context.scene, o, p) for p in coins]
            u = max(max(abs(v.x - .5), abs(v.y - .5)) * 2 for v in uv)
            if u * marge > 1.0:
                o.location = Vector(o.location) + axe * 0.1
            elif u * marge < 0.95:
                o.location = Vector(o.location) - axe * 0.1
            else:
                break
        if ouverture:
            cam.dof.use_dof = True
            cam.dof.focus_distance = (Vector(o.location) - centre).length
            cam.dof.aperture_fstop = ouverture
        return o

    def rendre(self, chemin, large, haut):
        sc = bpy.context.scene
        sc.render.resolution_x, sc.render.resolution_y = large, haut
        sc.render.resolution_percentage = 100
        sc.render.image_settings.file_format = "PNG"
        sc.render.image_settings.color_mode = "RGBA"
        sc.render.film_transparent = (self.fond != "papier")
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        sc.render.filepath = chemin
        bpy.ops.render.render(write_still=True)


# ── les matières ─────────────────────────────────────────────────────────────
def matiere(nom, base, rugosite=0.45, metal=0.0, transmission=0.0, ior=1.45, alpha=1.0, emission=None, force=0.0):
    m = bpy.data.materials.new(nom)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*srgb(base), 1)
    p.inputs["Roughness"].default_value = rugosite
    p.inputs["Metallic"].default_value = metal
    if transmission:
        p.inputs["Transmission Weight"].default_value = transmission
        p.inputs["IOR"].default_value = ior
    if alpha < 1.0:
        p.inputs["Alpha"].default_value = alpha
    if emission:
        p.inputs["Emission Color"].default_value = (*srgb(emission), 1)
        p.inputs["Emission Strength"].default_value = force
    return m


def matiere_pierre(nom, sombre, moyen, clair, paillette=None, polie=False, echelle=110.0):
    """Une pierre semée : trois tons par un bruit fin à paliers constants ; l'éventuelle
    paillette (or de la pyrite, ou rien) devient métallique par l'alpha de la rampe."""
    m = bpy.data.materials.new(nom)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    bruit = nt.nodes.new("ShaderNodeTexNoise")
    bruit.inputs["Scale"].default_value = echelle
    bruit.inputs["Detail"].default_value = 10.0
    bruit.inputs["Roughness"].default_value = 0.75
    rampe = nt.nodes.new("ShaderNodeValToRGB")
    cr = rampe.color_ramp
    cr.interpolation = "CONSTANT"
    cr.elements[0].position = 0.0
    cr.elements[0].color = (*srgb(sombre), 0.0)
    e1 = cr.elements.new(0.40)
    e1.color = (*srgb(moyen), 0.0)
    e2 = cr.elements.new(0.55)
    e2.color = (*srgb(clair), 0.0)
    if paillette:
        cr.elements[-1].position = 0.64
        cr.elements[-1].color = (*srgb(paillette), 1.0)
    else:
        cr.elements[-1].position = 0.999
        cr.elements[-1].color = (*srgb(clair), 0.0)
    nt.links.new(bruit.outputs["Fac"], rampe.inputs["Fac"])
    nt.links.new(rampe.outputs["Color"], p.inputs["Base Color"])
    nt.links.new(rampe.outputs["Alpha"], p.inputs["Metallic"])
    p.inputs["Roughness"].default_value = 0.22 if polie else 0.62
    return m


def matiere_eau_ridee(nom, base="#2b63c9"):
    m = matiere(nom, base, rugosite=0.08, transmission=0.7, ior=1.33)
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    bruit = nt.nodes.new("ShaderNodeTexNoise")
    bruit.inputs["Scale"].default_value = 9.0
    bruit.inputs["Detail"].default_value = 6.0
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.25
    bump.inputs["Distance"].default_value = 0.05
    nt.links.new(bruit.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], p.inputs["Normal"])
    return m


def pose(obj, mat):
    obj.data.materials.append(mat)
    return obj


# ── la géométrie ─────────────────────────────────────────────────────────────
def boite_du_sujet():
    mn, mx = Vector((1e9,) * 3), Vector((-1e9,) * 3)
    for o in bpy.context.scene.objects:
        if o.type != "MESH" and o.type != "CURVE":
            continue
        if o.name.startswith("sol") or o.hide_render:
            continue
        for coin in o.bound_box:
            p = o.matrix_world @ Vector(coin)
            mn = Vector((min(mn[i], p[i]) for i in range(3)))
            mx = Vector((max(mx[i], p[i]) for i in range(3)))
    return mn, mx


def chanfrein(o, part=0.010, n=3, plancher=0.004):
    bpy.context.view_layer.update()
    petit = min(d for d in o.dimensions if d > 1e-6)
    m = o.modifiers.new("chanfrein", "BEVEL")
    m.width, m.segments = max(plancher, petit * part), n
    m.harden_normals = True
    bpy.ops.object.shade_smooth()
    return o


def boite(nom, dims, pos, mat, biseau=0.02, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos, rotation=rot)
    o = bpy.context.object
    o.name = nom
    o.scale = dims
    pose(o, mat)
    bpy.ops.object.transform_apply(scale=True)
    if biseau:
        chanfrein(o, biseau)
    return o


def cylindre(nom, r, h, pos, mat, verts=64, rot=(0, 0, 0), biseau=0.03):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=pos, rotation=rot)
    o = bpy.context.object
    o.name = nom
    pose(o, mat)
    if biseau:
        chanfrein(o, biseau)
    else:
        bpy.ops.object.shade_smooth()
    return o


def prisme(nom, r, h, pos, mat, cotes=6, rot=(0, 0, 0), biseau=0.02):
    """Un prisme à n côtés (un cristal à six faces, une vis à huit) : un cylindre à peu de sommets, sans lissage."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=cotes, radius=r, depth=h, location=pos, rotation=rot)
    o = bpy.context.object
    o.name = nom
    pose(o, mat)
    bpy.context.view_layer.update()
    m = o.modifiers.new("chanfrein", "BEVEL")
    m.width, m.segments = max(0.003, r * biseau), 2
    m.harden_normals = True
    return o


def cone(nom, r1, r2, h, pos, mat, verts=48, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=h, location=pos, rotation=rot)
    o = bpy.context.object
    o.name = nom
    pose(o, mat)
    bpy.ops.object.shade_smooth()
    return o


def tore(nom, R_, r_, pos, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R_, minor_radius=r_, location=pos, rotation=rot,
                                     major_segments=64, minor_segments=16)
    o = bpy.context.object
    o.name = nom
    pose(o, mat)
    bpy.ops.object.shade_smooth()
    return o


def sphere(nom, r, pos, mat, subdiv=4):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdiv, radius=r, location=pos)
    o = bpy.context.object
    o.name = nom
    pose(o, mat)
    bpy.ops.object.shade_smooth()
    return o


def trace(nom, points, mat, rayon=0.006):
    cu = bpy.data.curves.new(nom, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = rayon
    cu.bevel_resolution = 5
    cu.fill_mode = "FULL"
    sp = cu.splines.new("POLY")
    sp.points.add(len(points) - 1)
    for i, p in enumerate(points):
        sp.points[i].co = (*p, 1.0)
    o = bpy.data.objects.new(nom, cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    return o


def planche_html(titre, sous_titre, formes, dossier, accent="#4f8ae0", nuit="#0f1626", panneau="#16213a", bord="#2b3a5c"):
    """La planche : six figures, chacune son numéro, son titre et sa phrase de valeur ;
    formes = [(fichier_png, numero_et_nom, titre, valeur), …]."""
    figs = "".join(
        f'<figure><img src="{png}" alt=""><figcaption><span class="n">{n}</span><div class="t">{t}</div><div class="v">{v}</div></figcaption></figure>'
        for png, n, t, v in formes)
    html = f"""<!doctype html><html lang="fr"><meta charset="utf-8"><title>{titre}</title>
<style>
  html,body{{margin:0;background:{nuit};color:#e6ecf7;font-family:Georgia,"Times New Roman",serif}}
  #p{{width:1920px;padding:36px 40px 30px;box-sizing:border-box}}
  h1{{font-size:30px;font-weight:600;margin:0 0 6px;letter-spacing:-.01em}}
  .sous{{font-family:ui-monospace,Menlo,monospace;font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:#a8b7d4;margin:0 0 24px}}
  .g{{display:grid;grid-template-columns:repeat(3,1fr);gap:26px 26px}}
  figure{{margin:0;background:{panneau};border:1px solid {bord};border-radius:6px;overflow:hidden}}
  figure img{{display:block;width:100%;aspect-ratio:916/747;object-fit:cover;background:#dbd7c5}}
  figcaption{{padding:14px 18px 16px}}
  .n{{font-family:ui-monospace,Menlo,monospace;font-size:13px;letter-spacing:.16em;color:{accent};text-transform:uppercase}}
  .t{{font-size:24px;font-weight:600;margin:4px 0 6px}}
  .v{{font-size:16px;line-height:1.35;color:#c3d0e8;font-style:italic}}
</style>
<div id="p"><h1>{titre}</h1><p class="sous">{sous_titre}</p><div class="g">{figs}</div></div></html>"""
    chemin = os.path.join(dossier, "planche.html")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(html)
    return chemin


# ── LA CHORÉGRAPHIE AU SCROLL (lot du 9/09, validée par Arslane sur le rack) ─────────────
# Une transition = n images d'une caméra qui va de `depart` à `arrivee` (azimut, élévation,
# marge), adoucie aux deux bouts ; `via` = un point de contrôle (Bézier quadratique) pour un
# aller-retour quand l'état d'arrivée garde la caméra du départ. La DERNIÈRE image est le
# cadrage de l'état : les annotations posées sur l'état restent justes à l'arrivée.
def options_sequence(ap):
    ap.add_argument("--sequence", type=int, default=0, help="nombre d'images de la transition ; 0 = l'état seul")
    ap.add_argument("--depart", default="", help="caméra de départ : azimut,elevation,marge")
    ap.add_argument("--via", default="", help="point de contrôle azimut,elevation,marge (aller-retour)")
    ap.add_argument("--cible", default="tout", help="la pièce cadrée à l'arrivée (l'état) ; « tout » = l'objet entier")
    ap.add_argument("--cible-depart", default="", help="la pièce cadrée au départ de la transition ; défaut : la cible d'arrivée")
    ap.add_argument("--echantillons", type=int, default=0, help="échantillons Cycles des images de passage ; 0 = ceux de la qualité")
    ap.add_argument("--echantillons-arrivee", type=int, default=0, help="échantillons de la DERNIÈRE image (l'état) ; 0 = comme les autres")


def lire_camera(texte):
    return tuple(float(x) for x in texte.split(","))


def chemin_camera(depart, arrivee, via, t):
    """(azimut, élévation, marge) à l'instant t ∈ [0, 1] : droite, ou Bézier près de `via`."""
    out = []
    for k in range(3):
        a, b = depart[k], arrivee[k]
        if via is None:
            out.append(a + (b - a) * t)
        else:
            c = via[k]
            out.append((1 - t) ** 2 * a + 2 * (1 - t) * t * c + t ** 2 * b)
    return tuple(out)


def adoucir(i, n):
    """0 → 1 en cosinus : un scroll qui s'arrête n'arrive jamais en plein élan."""
    return 0.5 - 0.5 * math.cos(math.pi * i / max(1, n - 1))


def boite_des(prefixes, air=(0.1, 0.1, 0.1)):
    """La boîte englobante des objets dont le nom commence par l'un des préfixes, avec de l'air :
    la CIBLE d'un gros plan (tranché par Arslane le 9/09 : des travellings vers les pièces)."""
    mn = Vector((1e9, 1e9, 1e9)); mx = Vector((-1e9, -1e9, -1e9)); n = 0
    for o in bpy.context.scene.objects:
        if o.type != "MESH" and o.type != "FONT":
            continue
        if not any(o.name.startswith(p) for p in prefixes):
            continue
        n += 1
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mn = Vector((min(mn.x, w.x), min(mn.y, w.y), min(mn.z, w.z)))
            mx = Vector((max(mx.x, w.x), max(mx.y, w.y), max(mx.z, w.z)))
    if n == 0:
        raise SystemExit(f"[cible] aucun objet ne commence par {prefixes} : la cible ne désigne rien")
    return (mn - Vector(air), mx + Vector(air))


def rendre_sequence(args, arrivee, placer, rendre_image, prefixe, boite_depart=None, boite_arrivee=None):
    """La scène est bâtie une fois ; la caméra se replace à chaque image (placer(az, el, marge)
    rend l'objet caméra, retiré avant la suivante) ; rendre_image(chemin) écrit l'image."""
    if not args.depart:
        raise SystemExit(f"[{prefixe}] --sequence exige --depart=azimut,elevation,marge")
    depart, via = lire_camera(args.depart), (lire_camera(args.via) if args.via else None)
    n = max(2, args.sequence)
    for i in range(n):
        t = adoucir(i, n)
        az, el, marge = chemin_camera(depart, arrivee, via, t)
        # les images de passage au réglage mesuré, l'image d'arrêt (l'état) en qualité pleine
        base = getattr(args, "echantillons", 0) or bpy.context.scene.cycles.samples
        bpy.context.scene.cycles.samples = (getattr(args, "echantillons_arrivee", 0) or base) if i == n - 1 else base
        if boite_depart is not None and boite_arrivee is not None:
            # le travelling glisse d'une pièce à l'autre : la boîte cadrée s'interpole aussi
            boite_t = (boite_depart[0].lerp(boite_arrivee[0], t), boite_depart[1].lerp(boite_arrivee[1], t))
            cam = placer(az, el, marge, boite_t)
        else:
            cam = placer(az, el, marge)
        rendre_image(os.path.join(args.sortie, f"{prefixe}-seq-0{args.etat}-{i:03d}.png"))
        bpy.data.objects.remove(cam, do_unlink=True)
    print(f"[{prefixe}] séquence : {n} images vers l'état {args.etat} dans {args.sortie} (la dernière = le cadrage de l'état)")
