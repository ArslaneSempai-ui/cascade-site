#!/usr/bin/env python3
"""LA TOUR DE TAMIS, AUX VRAIS CHIFFRES : les cinq états du plateau rouge.

  B=/Applications/Blender.app/Contents/MacOS/Blender
  "$B" -b -P tamis-etats.py -- --etat 3 --qualite apercu --sortie /tmp/tamis
  "$B" -b -P tamis-etats.py -- --etat 3 --qualite livraison --sortie /tmp/tamis
  cwebp -q 92 /tmp/tamis/tamis-03.png -o ../rendus/etats/tamis-03.webp

La thèse de l'objet (look-dev : equipe-cascade/rubis/tamis.py) : un SEUIL est un
tamis. Sept tamis empilés, du plus strict en haut au plus laxiste en bas ; sur
chacun, ce que CE seuil retient sur les 120 paires écrites du relevé public :
un jeton rubis par vraie correspondance retenue, un jeton gris par fausse
alerte retenue. Le tamis que la frontière retient porte le cadre rubis poli ;
les vraies correspondances qu'il laisse passer gisent au pied.

AUCUN CHIFFRE TAPÉ : chaque compte de jetons est lu dans
~/Documents/cascade-screening/releve-public.json, dont le scellé est vérifié par
outil.lire_releve_scelle avant qu'un seul objet n'existe. Le relevé mesure
chaque cellule sur les 120 paires, indépendamment : la tour montre sept mesures
côte à côte, pas une chute physique de jetons d'un étage à l'autre.

Les cinq états, un par finding (findings-screening.json) :
  1  exact : le tamis du haut, presque vide, et les rubis passés au pied
  2  jaro-winkler au seuil le plus lâche : le tamis du bas, plein
  3  la frontière : le tamis rubis poli, au milieu
  4  la même cellule, deux provenances : deux tamis côte à côte, paires écrites
     (gros jetons) et variantes fabriquées (petits jetons, à part)
  5  votre historique : la tour, et une feuille au pied avec des jetons pâles,
     non mesurés (l'absence de mesure se voit : rien n'est coloré à leur place)
Les états 1, 2, 3, 5 partagent LA MÊME caméra (cadrée une fois sur une boîte
fixe) : le fondu d'un état à l'autre ne fait pas sauter la tour.
"""
import argparse
import math
import os
import random
import sys

import bpy
from mathutils import Vector

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(ICI))          # source/ : outil.py
from outil import OUTILS, lire_releve_scelle      # noqa: E402

SKILL = os.path.join(os.path.expanduser("~"), ".claude", "skills", "design-arslane")
HDRI = os.path.join(SKILL, "assets", "hdri")

ap = argparse.ArgumentParser()
ap.add_argument("--etat", type=int, required=True, choices=[1, 2, 3, 4, 5])
ap.add_argument("--sortie", default="/tmp/tamis")
ap.add_argument("--qualite", default="apercu", choices=["apercu", "livraison"])
ap.add_argument("--fond", default="ombre", choices=["papier", "ombre", "sombre"])
ap.add_argument("--azimut", type=float, default=-72.0)
ap.add_argument("--elevation", type=float, default=27.0)
ap.add_argument("--frontiere", default="jaro-winkler:0.56",
                help="la cellule retenue par la règle de l'outil (optimise : borne basse du "
                     "rappel >= 0,90, puis le moins de fausses alertes), palier:seuil")
args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])

APERCU = args.qualite == "apercu"
# le cadre des états verts : 1374 × 1120 ; l'aperçu garde le rapport
LARGE, HAUT = (916, 747) if APERCU else (1374, 1120)
ECHANTILLONS = 24 if APERCU else 240
P_PAPIER = "#dbd7c5"

# ── LES DONNÉES : lues, scellées, jamais tapées ──────────────────────────────
RELEVE = lire_releve_scelle(OUTILS["screening"]["releve"])
AUTH = RELEVE["authored"]
SYNT = RELEVE["synthetic"]
PALIER_F, SEUIL_F = args.frontiere.split(":")

# du plus strict (haut) au plus lâche (bas) ; exact est le tamis le plus strict
# qui soit (l'identité après normalisation), puis jaro-winkler descend
TAMIS = [("exact", "0.50"), ("jaro-winkler", "0.90"), ("jaro-winkler", "0.80"),
         ("jaro-winkler", "0.70"), ("jaro-winkler", "0.60"), ("jaro-winkler", "0.56"),
         ("jaro-winkler", "0.50")]


def cellule(table, palier, seuil):
    c = table["tables"][palier][seuil]
    return c["rappel"]["succes"], c["fauxPositifs"]["succes"]


COMPTES = [cellule(AUTH, p, s) for p, s in TAMIS]            # (rubis, gris) par tamis
I_FRONTIERE = TAMIS.index((PALIER_F, SEUIL_F))
RUBIS_F, _ = COMPTES[I_FRONTIERE]
RATES = AUTH["nMatch"] - RUBIS_F                              # les vrais hits que la frontière laisse passer
for (p, s), (r, g) in zip(TAMIS, COMPTES):
    print(f"[tamis] {p}@{s} : {r} rubis / {AUTH['nMatch']}, {g} gris / {AUTH['nDifferent']}", flush=True)
print(f"[tamis] frontière {PALIER_F}@{SEUIL_F} : {RATES} vrais hits au pied", flush=True)


# ── outils de scène (recopiés de sequence.py : il parse ses arguments à l'import) ──
def srgb(hexa):
    h = hexa.lstrip("#")
    out = []
    for k in (0, 2, 4):
        c = int(h[k:k + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


def table_rase():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    c = sc.cycles
    c.samples = ECHANTILLONS
    c.use_denoising = True
    c.use_adaptive_sampling = True
    c.adaptive_threshold = 0.006
    c.adaptive_min_samples = 0
    c.transmission_bounces = 0
    c.diffuse_bounces = 2
    c.glossy_bounces = 4
    c.max_bounces = 6
    c.sample_clamp_indirect = 10.0
    sc.render.use_persistent_data = True
    try:
        bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "METAL"
        c.device = "GPU"
    except Exception:
        c.device = "CPU"
    v = sc.view_settings
    v.view_transform = "Khronos PBR Neutral"
    v.look = "None"


def matiere(nom, base, rugosite=0.4, metal=0.0):
    m = bpy.data.materials.new(nom)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*base, 1)
    p.inputs["Roughness"].default_value = rugosite
    p.inputs["Metallic"].default_value = metal
    return m


def pose(obj, mat):
    obj.data.materials.append(mat)
    return obj


def monde_hdri(fichier, force=1.0, rotation=0.0):
    w = bpy.data.worlds.new("monde")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    sortie = nt.nodes.new("ShaderNodeOutputWorld")
    fond = nt.nodes.new("ShaderNodeBackground")
    fond.inputs["Strength"].default_value = force
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    chemin = os.path.join(HDRI, fichier)
    if not os.path.exists(chemin):
        sys.exit(f"HDRI absent : {chemin}")
    env.image = bpy.data.images.load(chemin)
    map_ = nt.nodes.new("ShaderNodeMapping")
    map_.inputs["Rotation"].default_value[2] = rotation
    coord = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(coord.outputs["Generated"], map_.inputs["Vector"])
    nt.links.new(map_.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], fond.inputs["Color"])
    if args.fond in ("sombre", "ombre"):
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
    bpy.context.scene.render.film_transparent = False


def sol_papier(z):
    if args.fond == "sombre":
        return
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, z - 0.002))
    o = bpy.context.object
    o.name = "sol_papier"
    pose(o, matiere("m_papier", srgb(P_PAPIER), rugosite=0.94))
    if args.fond == "ombre":
        o.is_shadow_catcher = True


def post_traitement(halo=0.0):
    """Le halo du plateau vert est coupé ici : sur 560 jetons métalliques, la
    lueur s'accroche à chaque reflet et sème une poussière rouge dans l'alpha,
    visible sur le parchemin de la séquence (vu sur le rendu de livraison 03)."""
    if not halo:
        return
    sc = bpy.context.scene
    ng = bpy.data.node_groups.new("post", "CompositorNodeTree")
    sc.compositing_node_group = ng
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers")
    glare = ng.nodes.new("CompositorNodeGlare")
    for nom, valeur in [("Type", "Fog Glow"), ("Quality", "Medium" if APERCU else "High"),
                        ("Threshold", 0.85), ("Strength", halo), ("Size", 7)]:
        try:
            glare.inputs[nom].default_value = valeur
        except (KeyError, TypeError, AttributeError) as e:
            print(f"[tamis] halo : réglage « {nom} » ignoré ({type(e).__name__})", flush=True)
    sortie = ng.nodes.new("NodeGroupOutput")
    ng.links.new(rl.outputs["Image"], glare.inputs["Image"])
    ng.links.new(glare.outputs["Image"], sortie.inputs["Image"])


def boite_du_sujet():
    mn, mx, vu = Vector((1e9,) * 3), Vector((-1e9,) * 3), False
    for o in bpy.context.scene.objects:
        if o.type != "MESH" or o.name.startswith("sol"):
            continue
        for coin in o.bound_box:
            p = o.matrix_world @ Vector(coin)
            mn = Vector((min(mn[i], p[i]) for i in range(3)))
            mx = Vector((max(mx[i], p[i]) for i in range(3)))
            vu = True
    return (mn, mx) if vu else (Vector((-1, -1, 0)), Vector((1, 1, 1)))


def camera(position, boite, focale=72, ouverture=0.0, marge=1.14):
    """Cadre la BOÎTE donnée (pas la scène) : les états qui partagent une boîte
    partagent la caméra, et la tour garde sa taille d'un fondu à l'autre."""
    from bpy_extras.object_utils import world_to_camera_view
    mn, mx = boite
    centre = (mn + mx) / 2
    cam = bpy.data.cameras.new("cam")
    cam.lens = focale
    if ouverture:
        cam.dof.use_dof = True
        cam.dof.focus_distance = (Vector(position) - centre).length
        cam.dof.aperture_fstop = ouverture
    o = bpy.data.objects.new("cam", cam)
    bpy.context.collection.objects.link(o)
    o.location = Vector(position)
    bpy.context.scene.camera = o
    direction = centre - Vector(position)
    o.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    axe = -direction.normalized()
    coins = [Vector((x, y, z)) for x in (mn.x, mx.x) for y in (mn.y, mx.y) for z in (mn.z, mx.z)]
    for _ in range(120):
        bpy.context.view_layer.update()
        uv = [world_to_camera_view(bpy.context.scene, o, p) for p in coins]
        u = max(max(abs(v.x - .5), abs(v.y - .5)) * 2 for v in uv)
        if u * marge <= 1.0:
            break
        o.location = Vector(o.location) + axe * 0.20
        if ouverture:
            cam.dof.focus_distance = (Vector(o.location) - centre).length
    return o


def chanfrein(o, part=0.010, n=2, plancher=0.006):
    bpy.context.view_layer.update()
    petit = min(d for d in o.dimensions if d > 1e-6)
    m = o.modifiers.new("chanfrein", "BEVEL")
    m.width, m.segments = max(plancher, petit * part), n
    m.harden_normals = True
    bpy.ops.object.shade_smooth()
    wn = o.modifiers.new("normales", "WEIGHTED_NORMAL")
    wn.mode = "FACE_AREA"
    wn.keep_sharp = True
    return o


# ── LA PALETTE : celle du plateau vert, le rubis à la place du vert ──────────
def matieres():
    return {
        "cadre":       matiere("m_cadre", srgb("#8a8378"), rugosite=0.62, metal=0.18),
        "cadre_clair": matiere("m_cadre_clair", srgb("#aaa293"), rugosite=0.30, metal=0.40),  # le tamis du finding
        "rubis_cadre": matiere("m_rubis_cadre", srgb("#a3182b"), rugosite=0.14, metal=0.62),  # la frontière
        "maille":      matiere("m_maille", srgb("#5d6068"), rugosite=0.58, metal=0.60),
        "axe":         matiere("m_axe", srgb("#6f727a"), rugosite=0.40, metal=0.80),
        "gris":        matiere("m_gris", srgb("#9aa2ad"), rugosite=0.26, metal=0.88),
        "gris_poli":   matiere("m_gris_poli", srgb("#b9c1cc"), rugosite=0.11, metal=0.92),
        "rubis":       matiere("m_rubis", srgb("#8e1626"), rugosite=0.30, metal=0.70),
        "rubis_poli":  matiere("m_rubis_poli", srgb("#a3182b"), rugosite=0.14, metal=0.62),
        "papier":      matiere("m_feuille", srgb("#f1ede2"), rugosite=0.88),
        "inconnu":     matiere("m_inconnu", srgb("#cfc8b8"), rugosite=0.55, metal=0.05),   # non mesuré : ni rubis ni gris
    }


# ── LE SUJET ─────────────────────────────────────────────────────────────────
R = 1.70          # rayon des tamis : 111 jetons doivent tenir sur le plus plein
TUBE = 0.075
PAS_Z = 0.74
SOCLE = 0.30
JETON_R, JETON_E = 0.10, 0.045   # un jeton se compte ; 111 tiennent dans le disque
PETIT_R, PETIT_E = 0.042, 0.022  # une variante fabriquée : plus petite, à part


def anneau(x, z, mat, nom):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=TUBE, major_segments=96,
                                     minor_segments=24, location=(x, 0, z))
    o = bpy.context.object
    o.name = nom
    bpy.ops.object.shade_smooth()
    return pose(o, mat)


def maille(x, z, pas, mat):
    """La grille du tamis. Le pas EST le seuil : large en haut (strict), fin en bas."""
    n = int((2 * R) / pas)
    for k in range(-n // 2, n // 2 + 1):
        d = k * pas
        if abs(d) >= R - 0.02:
            continue
        demi = math.sqrt(max(0.0, R * R - d * d))
        for horizontale in (True, False):
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=12, radius=0.014, depth=2 * demi,
                location=(x + (d if not horizontale else 0), d if horizontale else 0, z),
                rotation=(0, math.pi / 2, 0) if horizontale else (math.pi / 2, 0, 0))
            pose(bpy.context.object, mat)


def places(rayon_jeton, graine):
    """Une grille jitterée dans le disque, hors de l'axe et du cadre."""
    rnd = random.Random(graine)
    pas = rayon_jeton * 2.25
    n = int(R / pas) + 1
    out = []
    for gx in range(-n, n + 1):
        for gy in range(-n, n + 1):
            x = gx * pas + rnd.uniform(-0.25, 0.25) * rayon_jeton
            y = gy * pas + rnd.uniform(-0.25, 0.25) * rayon_jeton
            if 0.20 + rayon_jeton < math.hypot(x, y) < R - rayon_jeton - 0.10:
                out.append((x, y))
    rnd.shuffle(out)
    return out


def jetons(x0, z, n_gris, n_rubis, M, graine, rayon=JETON_R, epaisseur=JETON_E, nature=("rubis", "gris")):
    ou = places(rayon, graine)
    if len(ou) < n_rubis + n_gris:
        sys.exit(f"tamis trop petit : {n_rubis + n_gris} jetons pour {len(ou)} places")
    for k in range(n_rubis + n_gris):
        x, y = ou[k]
        bpy.ops.mesh.primitive_cylinder_add(vertices=32 if rayon > 0.06 else 16, radius=rayon, depth=epaisseur,
                                            location=(x0 + x, y, z + 0.014 + epaisseur / 2))
        o = bpy.context.object
        est_rubis = k < n_rubis
        if est_rubis:
            pose(o, M["rubis_poli" if k % 3 == 0 else "rubis"])
        else:
            pose(o, M["gris" if k % 3 == 0 else "gris_poli"])
        if rayon > 0.06:
            chanfrein(o, 0.02)


def socle(x, rayon, epaisseur, M):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=rayon, depth=epaisseur, location=(x, 0, -epaisseur / 2))
    s = bpy.context.object
    s.name = f"socle_{x:.1f}"
    pose(s, M["cadre"])
    chanfrein(s, 0.012)
    return s


def tour(M, accent=None):
    """La tour entière : sept tamis, leurs jetons lus dans le relevé, la frontière en
    rubis poli, le tamis du finding (accent) en cadre clair, les vrais hits ratés au pied."""
    n = len(TAMIS)
    haut = (n - 1) * PAS_Z + 0.9
    socle(0, R + 0.42, SOCLE, M)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.06, depth=haut, location=(0, 0, haut / 2))
    pose(bpy.context.object, M["axe"])
    for k in range(RATES):
        # devant la tour ; à l'état 5 la feuille du client occupe le devant-droit,
        # et un vrai hit raté posé SUR sa feuille contredirait « uncoloured until
        # measured » : les ratés passent au devant-gauche (l'état 4 sépare 3 et 5,
        # aucun fondu direct ne montre le déplacement)
        a = -math.pi / 2 + (k - (RATES - 1) / 2) * 0.42 - (0.72 if args.etat == 5 else 0.0)
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=JETON_R, depth=JETON_E,
                                            location=((R + 0.16) * math.cos(a), (R + 0.16) * math.sin(a), JETON_E / 2))
        pose(bpy.context.object, M["rubis"])
        chanfrein(bpy.context.object, 0.02)
    for i, (rubis, gris) in enumerate(COMPTES):
        niveau = n - 1 - i                         # i = 0 : le plus strict, en haut
        z = 0.45 + niveau * PAS_Z
        pas = 0.11 + niveau / (n - 1) * 0.59       # la maille EST le seuil
        if i == I_FRONTIERE:
            cadre = M["rubis_cadre"]
        elif accent is not None and i == accent:
            cadre = M["cadre_clair"]
        else:
            cadre = M["cadre"]
        anneau(0, z, cadre, f"tamis_{i}")
        maille(0, z, pas, M["maille"])
        jetons(0, z, gris, rubis, M, graine=100 + i)


def feuille(M):
    """L'export du client, au pied : une feuille, et dessus des jetons qui n'ont
    pas de couleur parce qu'ils n'ont pas de mesure. La feuille glisse sous le
    socle : rien d'elle ne sort du cadre commun."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.05, -1.75, 0.011))
    f = bpy.context.object
    f.name = "feuille"
    f.scale = (2.1, 2.8, 0.022)
    f.rotation_euler[2] = math.radians(14)
    pose(f, M["papier"])
    rnd = random.Random(7)
    for k in range(9):
        gx, gy = (k % 3 - 1) * 0.42, (k // 3 - 1) * 0.55
        x, y = 1.05 + gx + rnd.uniform(-0.06, 0.06), -1.75 - 0.35 + gy + rnd.uniform(-0.06, 0.06)
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=JETON_R, depth=JETON_E,
                                            location=(x, y, 0.022 + JETON_E / 2))
        pose(bpy.context.object, M["inconnu"])
        chanfrein(bpy.context.object, 0.02)


def deux_tamis(M):
    """Finding 04 : la MÊME cellule (la frontière), deux provenances côte à côte.
    À gauche les paires écrites, gros jetons ; à droite les variantes fabriquées,
    petits jetons, sur leur propre pied : jamais mêlées."""
    ecart = R + 0.75
    z = 1.25
    for x, table, rayon, ep, cadre, graine in (
            (-ecart, AUTH, JETON_R, JETON_E, "rubis_cadre", 300),
            (+ecart, SYNT, PETIT_R, PETIT_E, "cadre", 301)):
        socle(x, R + 0.32, SOCLE * 0.8, M)
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.06, depth=z + 0.2, location=(x, 0, (z + 0.2) / 2))
        pose(bpy.context.object, M["axe"])
        rubis, gris = cellule(table, PALIER_F, SEUIL_F)
        anneau(x, z, M[cadre], f"tamis_{x:.1f}")
        maille(x, z, 0.11 + (len(TAMIS) - 1 - I_FRONTIERE) / (len(TAMIS) - 1) * 0.59, M["maille"])
        jetons(x, z, gris, rubis, M, graine=graine, rayon=rayon, epaisseur=ep)
        print(f"[tamis] état 4, {table['provenance'] if isinstance(table.get('provenance'), str) else 'table'} "
              f"x={x:+.1f} : {rubis} rubis, {gris} gris", flush=True)


def rendre():
    table_rase()
    monde_hdri("contraste.hdr", force=1.15, rotation=math.pi * 0.35)
    M = matieres()
    r = 9.0
    # les deux tamis de l'état 4 sont plats : vus de plus haut, leur contenu se lit
    az, el = math.radians(args.azimut), math.radians(args.elevation if args.etat != 4 else 40.0)
    position = (math.cos(el) * math.cos(az) * r, math.cos(el) * math.sin(az) * r, math.sin(el) * r)
    if args.etat == 4:
        deux_tamis(M)
        boite = boite_du_sujet()
    else:
        accent = {1: 0, 2: len(TAMIS) - 1, 3: I_FRONTIERE, 5: None}[args.etat]
        tour(M, accent=accent)
        # la boîte COMMUNE aux états de la tour : la tour, plus la place de la feuille
        # de l'état 5, pour que la caméra soit la même dans les quatre états
        mn, mx = boite_du_sujet()
        boite = (Vector((mn.x, mn.y - 1.05, mn.z)), Vector((mx.x + 0.15, mx.y, mx.z)))
        if args.etat == 5:
            feuille(M)
    sol_papier(-SOCLE if args.etat != 4 else -SOCLE * 0.8)
    post_traitement()
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = LARGE, HAUT
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.render.film_transparent = (args.fond != "papier")
    os.makedirs(args.sortie, exist_ok=True)
    camera(position, boite, focale=72, ouverture=0.0 if APERCU else 11.0, marge=1.09)
    sc.render.filepath = os.path.join(args.sortie, f"tamis-0{args.etat}.png")
    bpy.ops.render.render(write_still=True)
    print(f"[tamis] rendu → {sc.render.filepath}\n[tamis] Le code de sortie 0 ne prouve rien : ouvrir l'image et la regarder.")


rendre()
