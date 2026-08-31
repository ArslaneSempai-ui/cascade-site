#!/usr/bin/env python3
"""Le bloc des deux taux, six présentations des MÊMES chiffres.

CE QU'ARSLANE A JUGÉ LE 31 AOÛT : « les écritures en dessous ne sont pas symétriques
et c'est un peu pauvrement fait ». Vrai : la moustache est écrasée contre sa note,
trois corps se battent (chiffre, flèche, notes), et les notes tombent au fer sans
gabarit commun.

LES CHIFFRES NE CHANGENT PAS : 94,4 (moyenne des cinq taux), 76,7 (par dossier,
92 sur 120, Wilson 68,3-83,3), l'écart 17,7. Seule la PRÉSENTATION varie.

LA VALEUR DE CHACUNE, ÉCRITE AVANT DE DESSINER
  F1  la phrase        les chiffres vivent DANS une phrase composée en grand :
                       zéro appareil, c'est du langage. L'annotation en une seule
                       ligne de petites capitales dessous.
  F2  le socle         les deux chiffres posés sur UNE règle de base commune, les
                       notes suspendues dessous, centrées sous leur chiffre ; l'écart
                       est une COTE de dessin technique au-dessus. La symétrie est
                       structurelle, pas réglée.
  F3  le miroir        deux colonnes strictement égales, tout centré dans chacune ;
                       l'écart en ligne centrée sous les deux. La plus calme.
  F4  la hiérarchie    LE taux qui compte en très grand, l'autre réduit à une ligne
                       d'amorce au-dessus : la composition dit laquelle des deux
                       valeurs part au dossier. La plus éditoriale.
  F5  l'instrument     UNE échelle dessinée de 60 à 100 porte les deux taux : le
                       94,4 pointé dessus, le 76,7 avec son intervalle, l'écart en
                       plage teintée entre les deux. La comparaison devient spatiale,
                       et l'intervalle a enfin la place qu'il mérite.
  F6  le registre      deux lignes de livre de comptes : chiffre à droite dans une
                       colonne fixe, note en regard, le solde en bas sous un filet
                       gras. Le registre est la langue maternelle d'une banque.
"""
import importlib.util
import pathlib

BASE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("bn", BASE / "batir-nav.py")
bn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bn)

COMMUN = """
  *{box-sizing:border-box}
  html{background:#dbd7c5}
  body{margin:0;padding:2.2rem 2.6rem;width:840px;color:#1b1d18;
       font:400 16px/1.5 "Literata",Georgia,serif;-webkit-font-smoothing:antialiased;
       background:linear-gradient(168deg,#e2ddcb,#dbd7c5 70%)}
  :root{--encre:#1b1d18;--demi:#4a4739;--pale:#55523f;--filet:#9d9a83;
        --filet-clair:#bab7a0;--vert:#23543f;
        --sans:ui-sans-serif,-apple-system,"Helvetica Neue",sans-serif}
  .cap{font:600 11px/1.4 var(--sans);letter-spacing:.14em;text-transform:uppercase;
       color:var(--pale)}
"""

# L'échelle commune 60-100, la même que partout ailleurs sur le site.
def pc(v):
    return round((v - 60) / 40 * 100, 2)


F1 = ("""
  .ph{max-width:34ch;font:400 2.05rem/1.34 "Literata",Georgia,serif;margin:0;
      letter-spacing:-.012em}
  .ph b{font-weight:600;font-variant-numeric:tabular-nums}
  .ph .de{color:var(--vert)}
  .ligne-cap{display:flex;gap:1.6rem;margin-top:1.1rem}
""", """
  <p class="ph">Your dashboard says <b>94.4%</b>. Your desk says
    <b class="de">76.7%</b>: all five fields right on the same file, 92&nbsp;of&nbsp;120.</p>
  <div class="ligne-cap"><span class="cap">The gap, 17.7 points</span>
    <span class="cap">Wilson 95%: 68.3 to 83.3</span></div>
""")

F2 = ("""
  .socle{position:relative;width:640px;padding-top:3rem}
  .cote{position:absolute;top:0;left:25%;width:50%;text-align:center}
  .cote .cap{color:var(--demi)}
  .cote svg{display:block;width:100%;height:12px;margin-top:.3rem}
  .paire{display:grid;grid-template-columns:1fr 1fr;border-bottom:1.5px solid var(--encre)}
  .col{text-align:center;padding-bottom:.55rem}
  .col .cap{display:block;margin-bottom:.45rem}
  .gv{font:600 3.1rem/1 "Literata",Georgia,serif;letter-spacing:-.03em;
      font-variant-numeric:tabular-nums}
  .col.de .gv{color:var(--vert)}
  .dessous{display:grid;grid-template-columns:1fr 1fr}
  .dessous p{margin:.6rem auto 0;max-width:24ch;text-align:center;
             font:400 13px/1.5 var(--sans);color:var(--demi)}
  .dessous .int{display:block;margin-top:.25rem;font-size:12px;color:var(--pale)}
""", f"""
  <div class="socle">
    <div class="cote"><span class="cap">17.7 points, the gap</span>
      <svg viewBox="0 0 100 12" preserveAspectRatio="none">
        <path d="M1 1 L1 11 M1 6 L99 6 M99 1 L99 11" stroke="#55523f"
          stroke-width="1.4" fill="none" vector-effect="non-scaling-stroke"></path></svg>
    </div>
    <div class="paire">
      <div class="col"><span class="cap">On the dashboard</span>
        <span class="gv">94.4%</span></div>
      <div class="col de"><span class="cap">On your desk</span>
        <span class="gv">76.7%</span></div>
    </div>
    <div class="dessous">
      <p>Mean of five field rates. Not a proportion, so no interval exists.</p>
      <p>All five fields right on the same file, 92 of 120.
        <span class="int">Wilson 95%: 68.3 to 83.3</span></p>
    </div>
  </div>
""")

F3 = ("""
  .mir{display:grid;grid-template-columns:1fr 1fr;column-gap:3rem;width:620px}
  .col{text-align:center;display:flex;flex-direction:column;align-items:center;gap:.4rem}
  .gv{font:600 3rem/1 "Literata",Georgia,serif;letter-spacing:-.03em;
      font-variant-numeric:tabular-nums}
  .col.de .gv{color:var(--vert)}
  .mou{width:200px;height:24px}
  .mou line{stroke:#bab7a0}
  .mou .br{stroke:#1b1d18;stroke-width:1.4;fill:none}
  .mou .pt{fill:#23543f}
  .mou text{font:500 10px var(--sans);fill:#55523f}
  .mou .vide{font-style:italic;fill:#55523f}
  .col p{margin:0;max-width:24ch;font:400 13px/1.5 var(--sans);color:var(--demi)}
  .ecart{grid-column:1 / -1;text-align:center;margin-top:1.2rem}
""", f"""
  <div class="mir">
    <div class="col"><span class="cap">On the dashboard</span>
      <span class="gv">94.4%</span>
      <svg class="mou" viewBox="0 0 200 24"><line x1="4" y1="11" x2="196" y2="11"></line>
        <text class="vide" x="100" y="15" text-anchor="middle">no interval exists</text>
        <circle class="pt" cx="{pc(94.4) * 1.92 + 4:.0f}" cy="11" r="3" fill="#1b1d18"></circle></svg>
      <p>Mean of five field rates, not a proportion.</p></div>
    <div class="col de"><span class="cap">On your desk</span>
      <span class="gv">76.7%</span>
      <svg class="mou" viewBox="0 0 200 24"><line x1="4" y1="11" x2="196" y2="11"></line>
        <path class="br" d="M{pc(68.3) * 1.92 + 4:.0f} 5 L{pc(68.3) * 1.92 + 4:.0f} 17
          M{pc(68.3) * 1.92 + 4:.0f} 11 L{pc(83.3) * 1.92 + 4:.0f} 11
          M{pc(83.3) * 1.92 + 4:.0f} 5 L{pc(83.3) * 1.92 + 4:.0f} 17"></path>
        <circle class="pt" cx="{pc(76.7) * 1.92 + 4:.0f}" cy="11" r="3"></circle>
        <text x="{pc(68.3) * 1.92 + 4:.0f}" y="23" text-anchor="middle">68.3</text>
        <text x="{pc(83.3) * 1.92 + 4:.0f}" y="23" text-anchor="middle">83.3</text></svg>
      <p>All five fields right on the same file, 92 of 120.</p></div>
    <span class="ecart cap">The gap over the same files: 17.7 points</span>
  </div>
""")

F4 = ("""
  .amorce{margin:0 0 .5rem;font:italic 400 16.5px/1.5 "Literata",Georgia,serif;
          color:var(--demi)}
  .amorce b{font-style:normal;font-weight:600;color:var(--encre);
            font-variant-numeric:tabular-nums}
  .grand{font:600 5.4rem/1 "Literata",Georgia,serif;letter-spacing:-.035em;
         color:var(--vert);font-variant-numeric:tabular-nums;display:block}
  .mou{width:340px;height:30px;display:block;margin-top:.5rem}
  .mou line{stroke:#bab7a0}
  .mou .br{stroke:#1b1d18;stroke-width:1.5;fill:none}
  .mou .pt{fill:#23543f}
  .mou text{font:500 10.5px var(--sans);fill:#55523f}
  .dessous{margin:.6rem 0 0;font:400 13.5px/1.5 var(--sans);color:var(--demi);
           max-width:44ch}
  .dessous .cap{display:block;margin-top:.5rem}
""", f"""
  <p class="amorce">Your dashboard says <b>94.4%</b>, the mean of five field rates.
    The number that gets filed is this one:</p>
  <span class="grand">76.7%</span>
  <svg class="mou" viewBox="0 0 340 30"><line x1="4" y1="13" x2="336" y2="13"></line>
    <path class="br" d="M{pc(68.3) * 3.32 + 4:.0f} 6 L{pc(68.3) * 3.32 + 4:.0f} 20
      M{pc(68.3) * 3.32 + 4:.0f} 13 L{pc(83.3) * 3.32 + 4:.0f} 13
      M{pc(83.3) * 3.32 + 4:.0f} 6 L{pc(83.3) * 3.32 + 4:.0f} 20"></path>
    <circle class="pt" cx="{pc(76.7) * 3.32 + 4:.0f}" cy="13" r="3.4"></circle>
    <text x="{pc(68.3) * 3.32 + 4:.0f}" y="29" text-anchor="middle">68.3</text>
    <text x="{pc(83.3) * 3.32 + 4:.0f}" y="29" text-anchor="middle">83.3</text></svg>
  <p class="dessous">All five fields right on the same file, 92 of 120 case files.
    <span class="cap">17.7 points below the dashboard, over the same files</span></p>
""")

F5 = ("""
  .inst{width:660px}
  .inst .cap{display:block;margin-bottom:2.6rem}
  .porte{position:relative;height:168px}
  .axe{position:absolute;left:0;right:0;top:78px;height:1.5px;background:var(--encre)}
  .grads{position:absolute;left:0;right:0;top:79.5px;height:5px;
         background:repeating-linear-gradient(90deg,#bab7a0 0 1px,transparent 1px 5%)}
  .reps{position:absolute;left:0;right:0;top:86px;height:14px;display:block}
  .reps text{font:500 10px var(--sans);fill:var(--pale)}
  .plage{position:absolute;top:72px;height:14px;background:rgba(35,84,63,.16)}
  .pt{position:absolute;top:78.75px;width:9px;height:9px;border-radius:50%;
      transform:translate(-50%,-50%)}
  .pt.a{background:var(--encre)}
  .pt.b{background:var(--vert)}
  .wil{position:absolute;top:72px;height:13px;border-left:1.5px solid var(--vert);
       border-right:1.5px solid var(--vert)}
  .wil i{position:absolute;left:0;right:0;top:6px;height:1.5px;background:var(--vert);
         display:block}
  .drapeau{position:absolute;transform:translateX(-50%);text-align:center;width:190px}
  .drapeau .gv{font:600 1.9rem/1 "Literata",Georgia,serif;letter-spacing:-.02em;
               font-variant-numeric:tabular-nums;display:block}
  .drapeau p{margin:.15rem 0 0;font:400 12px/1.4 var(--sans);color:var(--demi)}
  .d-a{top:0;width:170px}
  .d-b{top:104px}
  .d-b .gv{color:var(--vert)}
  .ecart-l{position:absolute;top:58px;transform:translateX(-50%);
           font:600 10.5px/1 var(--sans);letter-spacing:.13em;text-transform:uppercase;
           color:var(--vert)}
""", f"""
  <div class="inst"><span class="cap">The two rates, on the same drawn scale</span>
    <div class="porte">
      <span class="plage" style="left:{pc(76.7)}%;width:{pc(94.4) - pc(76.7)}%"></span>
      <span class="axe"></span><span class="grads"></span>
      <svg class="reps" viewBox="0 0 660 14">
        <text x="0" y="11">60</text>
        <text x="165" y="11" text-anchor="middle">70</text>
        <text x="330" y="11" text-anchor="middle">80</text>
        <text x="495" y="11" text-anchor="middle">90</text>
        <text x="660" y="11" text-anchor="end">100</text></svg>
      <span class="wil" style="left:{pc(68.3)}%;width:{pc(83.3) - pc(68.3)}%"><i></i></span>
      <span class="pt a" style="left:{pc(94.4)}%"></span>
      <span class="pt b" style="left:{pc(76.7)}%"></span>
      <span class="ecart-l" style="left:{(pc(94.4) + pc(76.7)) / 2}%">17.7 points</span>
      <div class="drapeau d-a" style="left:{pc(94.4)}%"><span class="gv">94.4%</span>
        <p>The dashboard mean, no interval.</p></div>
      <div class="drapeau d-b" style="left:{pc(76.7)}%"><span class="gv">76.7%</span>
        <p>On your desk: all five fields right on the same file, 92 of 120.
           Wilson 95%: 68.3 to 83.3.</p></div>
    </div>
  </div>
""")

F6 = ("""
  .reg{width:560px;border-top:1.5px solid var(--encre)}
  .li{display:grid;grid-template-columns:9.5rem 1fr;align-items:baseline;
      column-gap:1.6rem;padding:.65rem 0;border-bottom:1px solid var(--filet-clair)}
  .gv{font:600 2.3rem/1 "Literata",Georgia,serif;letter-spacing:-.025em;
      font-variant-numeric:tabular-nums;text-align:right}
  .li.de .gv{color:var(--vert)}
  .li p{margin:0;font:italic 400 14.5px/1.5 "Literata",Georgia,serif;color:var(--demi)}
  .li p .int{font-style:normal;font:400 12px/1.4 var(--sans);color:var(--pale);
             display:block;margin-top:.1rem}
  .li.solde{border-bottom:none;border-top:1.5px solid var(--encre);margin-top:-1px}
  .li.solde .gv{font-size:1.7rem}
  .li.solde p{font-style:normal;font:600 11px/1.4 var(--sans);letter-spacing:.14em;
              text-transform:uppercase;color:var(--pale)}
""", """
  <div class="reg">
    <div class="li"><span class="gv">94.4%</span>
      <p>Mean of five field rates, on the dashboard. Not a proportion, so no
        interval exists.</p></div>
    <div class="li de"><span class="gv">76.7%</span>
      <p>All five fields right on the same file, 92 of 120.
        <span class="int">Wilson 95%: 68.3 to 83.3</span></p></div>
    <div class="li solde"><span class="gv">17.7</span>
      <p>Points between the two, over the same files</p></div>
  </div>
""")

VARIANTES = [("F1", "phrase", *F1), ("F2", "socle", *F2), ("F3", "miroir", *F3),
             ("F4", "hierarchie", *F4), ("F5", "instrument", *F5),
             ("F6", "registre", *F6)]

for code, nom, css, html in VARIANTES:
    (BASE / f"{code}-{nom}.html").write_text(f"""<!doctype html>
<meta charset="utf-8"><title>Figures {code}</title>
<link rel="stylesheet" href="fontes/literata.css">
<style>{COMMUN}{css}</style>
{html}
""", encoding="utf-8")
    print(f"  {code}-{nom}.html")
