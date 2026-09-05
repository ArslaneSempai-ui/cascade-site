#!/usr/bin/env python3
"""L'AFFICHE D'UN OUTIL : la plaque 3D (affiche-plaque.py) + la carte des deux chiffres
que le robot projette, lus dans le relevé scellé, capturée en Chrome natif, puis
réduite au format de l'affiche verte (1280x720, grain) : rendus/affiche-<outil>.jpg.

  python3 affiche-composer.py screening /tmp/affiche/plaque-rubis.png

Les deux chiffres sont ceux de la cellule que la règle de l'outil retient (la
frontière, finding 03) : rappel et fausses alertes, avec leurs cellules nommées.
Aucun chiffre n'est tapé : la carte refuse si le relevé ne porte pas la cellule.
La capture passe par scratchpad/capture.mjs (Chrome headless, port 9222) sur le
serveur de source/ (port 8812) : la page est servie, jamais ouverte en file://,
parce que les fontes de la maison sont chargées par feuille de style.
"""
import json
import pathlib
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parent
sys.path.insert(0, str(SRC))
from outil import OUTILS, lire_releve_scelle  # noqa: E402

outil_id, plaque = sys.argv[1], pathlib.Path(sys.argv[2])
O = OUTILS[outil_id]
R = lire_releve_scelle(O["releve"])

# la cellule de la frontière : la même que findings-screening.json (source, finding 03)
F = json.loads((SRC / f"findings-{outil_id}.json").read_text())
if F["sceau"] != R["empreinte"]:
    sys.exit(f"findings-{outil_id}.json cite le sceau {F['sceau']}, le relevé porte {R['empreinte']}")
src = F["findings"][2]["source"]
cell_a, cell_b = src["a"], src["b"]
def lire(c):
    return R[c["table"]]["tables"][c["palier"]][c["seuil"]][c["mesure"]]
a, b = lire(cell_a), lire(cell_b)
pc = lambda x: f"{x['taux'] * 100:.1f}".rstrip("0").rstrip(".")
chiffre_a, chiffre_b = pc(a), pc(b)
palier, seuil = cell_a["palier"], cell_a["seuil"]

# les fontes de la maison, servies depuis source/fontes
CAPTURE = pathlib.Path("/private/tmp/claude-501/-Users-arslanechr-Downloads-atlas-final-en-fr/"
                       "9eaa6456-ea12-48c5-bd77-6279f40c9def/scratchpad/capture.mjs")
plaque_web = ICI / f"affiche-{outil_id}-plaque.png"
plaque_web.write_bytes(plaque.read_bytes())

# les PAUMES, en % du cadre (plaque relue : la gauche basse, la droite haute) ; chaque
# hologramme se pose au-dessus de sa paume et son faisceau descend jusqu'à elle
PAUMES = {"g": (24.0, 76.0), "d": (78.0, 58.0)}
HAUT = {"g": 30.0, "d": 11.0}                  # le haut de chaque hologramme
LARGEUR_FAISCEAU = 22.0                        # % du cadre (420 px sur 1920)
POS = {c: {"x": PAUMES[c][0] - 15.0, "y": HAUT[c]} for c in PAUMES}
FAISCEAU = {c: {"x": PAUMES[c][0] - LARGEUR_FAISCEAU / 2, "y": HAUT[c] + 22.0,
                "h": PAUMES[c][1] - (HAUT[c] + 22.0)} for c in PAUMES}
html = f"""<!doctype html><html lang="en"><meta charset="utf-8"><title>affiche {outil_id}</title>
<link rel="stylesheet" href="../fontes/literata.css"><link rel="stylesheet" href="../fontes/roboto-mono.css">
<style>
  html,body{{margin:0;background:#000}}
  #scene{{position:relative;width:1920px;height:1080px;overflow:hidden}}
  #scene *{{margin:0;box-sizing:border-box}}
  #plate{{position:absolute;inset:0;width:1920px;height:1080px;display:block}}
  .holo{{position:absolute;color:{O["vif"]};font-family:"Literata",Georgia,serif;
    font-variant-numeric:tabular-nums;font-weight:600;letter-spacing:-.02em;line-height:1}}
  .holo .n{{display:block;font-size:168px;text-shadow:0 0 28px {O["vif"]}66,0 0 70px {O["vif"]}33}}
  .holo .n small{{font-size:96px;font-weight:500}}
  .holo .l{{display:block;font-family:"Roboto Mono",ui-monospace,Menlo,monospace;font-size:28px;
    letter-spacing:.16em;text-transform:uppercase;margin-bottom:14px;opacity:.92}}
  .holo .s{{display:block;font-family:"Roboto Mono",ui-monospace,Menlo,monospace;font-size:20px;
    letter-spacing:.06em;margin-top:10px;opacity:.7}}
  .faisceau{{position:absolute;width:{LARGEUR_FAISCEAU}%;pointer-events:none;
    background:linear-gradient(to top,{O["vif"]}66,{O["vif"]}1f 55%,transparent);
    clip-path:polygon(46% 100%,54% 100%,100% 0,0 0);filter:blur(2px)}}
</style>
<div id="scene">
  <img id="plate" src="affiche-{outil_id}-plaque.png" alt="">
  <div class="faisceau" style="left:{FAISCEAU['g']['x']}%;top:{FAISCEAU['g']['y']}%;height:{FAISCEAU['g']['h']}%"></div>
  <div class="faisceau" style="left:{FAISCEAU['d']['x']}%;top:{FAISCEAU['d']['y']}%;height:{FAISCEAU['d']['h']}%"></div>
  <div class="holo" style="left:{POS['g']['x']}%;top:{POS['g']['y']}%">
    <span class="l">recall, at the frontier</span>
    <span class="n">{chiffre_a}<small>%</small></span>
    <span class="s">{palier} &#183; threshold {seuil} &#183; n={a['n']}</span>
  </div>
  <div class="holo" style="left:{POS['d']['x']}%;top:{POS['d']['y']}%">
    <span class="l">false alerts, same cell</span>
    <span class="n">{chiffre_b}<small>%</small></span>
    <span class="s">wilson [{b['bas'] * 100:.0f}&#8211;{b['haut'] * 100:.0f}] &#183; n={b['n']}</span>
  </div>
</div>
</html>"""
page = ICI / f"affiche-{outil_id}.html"
page.write_text(html, encoding="utf-8")

brut = plaque.parent / f"affiche-{outil_id}-1920.png"
subprocess.run(["node", str(CAPTURE), f"http://127.0.0.1:8812/etats/affiche-{outil_id}.html",
                "1920", "1080", "-", str(brut)], check=True, capture_output=True)
dst = SRC / "rendus" / f"affiche-{outil_id}.jpg"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(brut),
                "-vf", "scale=1280:720:flags=lanczos,noise=alls=5:allf=u", "-q:v", "3", str(dst)],
               check=True)
plaque_web.unlink()
print(f"{dst} : {chiffre_a} % recall / {chiffre_b} % false alerts at {palier}@{seuil}, "
      f"seal {R['empreinte']} ({dst.stat().st_size} o)")
