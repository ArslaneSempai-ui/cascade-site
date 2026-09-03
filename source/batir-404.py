#!/usr/bin/env python3
"""LA 404 DESSINÉE : le petit robot, calme, et rien à mesurer ici.

Elle tourne APRÈS batir-annexe dans l'assembleur et remplace sa 404 de
plomberie : même phrase d'honnêteté (rien ici n'a été mesuré, scellé ni
publié), mais l'écran appartient au monde du site : nuit, le robot de la fin
du film en petit, trois portes de sortie. L'assembleur lui pose le <base>
pour que ses liens se résolvent depuis la racine quel que soit le chemin raté.
"""
import pathlib

BASE = pathlib.Path(__file__).parent
SCEAU = "1151f5a1cfaae0c0"

CSS = '''
  :root{--nuit-a:#1b3229;--nuit-b:#14251e;--nuit-c:#0e1a15;--sur-vert:#e4ecdf;
    --sur-vert-pale:#a9bdaf;--vert-vif:#57b184;--vert-clair:#a5f7cb;
    --texte:"Literata",Georgia,serif;--mono:"Roboto Mono",ui-monospace,Menlo,monospace;
    --sans:ui-sans-serif,-apple-system,"Helvetica Neue",sans-serif;
    --montee:cubic-bezier(.16,.84,.32,1)}
  *{box-sizing:border-box;margin:0}
  body{min-height:100vh;display:flex;flex-direction:column;align-items:center;
    justify-content:center;gap:8px;padding:40px 24px;text-align:center;
    background:radial-gradient(120% 100% at 50% -10%,var(--nuit-a),var(--nuit-b) 55%,var(--nuit-c));
    color:var(--sur-vert);font-family:var(--texte);line-height:1.55}
  ::selection{background:var(--vert-vif);color:var(--nuit-c)}
  a{color:inherit;text-underline-offset:4px}
  :focus-visible{outline:3px solid var(--vert-vif);outline-offset:3px;border-radius:2px}
  .code{font-family:var(--mono);font-size:12px;letter-spacing:.22em;color:var(--vert-vif)}
  .robot{width:min(300px,60vw);margin:10px 0 4px}
  .robot img{width:100%;border-radius:14px;box-shadow:0 30px 80px rgba(0,0,0,.55)}
  h1{font-size:clamp(28px,4.4vw,46px);font-weight:600;letter-spacing:-.02em;line-height:1.08;
    text-wrap:balance;max-width:18ch}
  p{font-size:15.5px;color:var(--sur-vert-pale);max-width:52ch;text-wrap:balance}
  .portes{display:flex;gap:10px;margin-top:22px;flex-wrap:wrap;justify-content:center}
  .porte{font-family:var(--texte);font-size:14.5px;font-weight:600;color:var(--vert-clair);
    text-decoration:none;border:1px solid color-mix(in srgb,var(--vert-vif) 45%,transparent);
    border-radius:9px;padding:11px 18px;transition:background .2s,color .2s,border-color .2s}
  .porte:hover{background:var(--vert-vif);color:var(--nuit-c);border-color:var(--vert-vif)}
  .sceau{margin-top:26px;font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;
    color:color-mix(in srgb,var(--sur-vert-pale) 70%,transparent)}
'''

PAGE = f'''<!doctype html><html lang="en">
<meta charset="utf-8"><title>Cascade, nothing measured here</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<meta name="description" content="This address was never measured, never sealed, never published.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M0 0h16L0 16z' fill='%2314251e'/%3E%3Cpath d='M16 0v16H0z' fill='%2323543f'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<link rel="stylesheet" href="fontes/roboto-mono.css">
<style>{CSS}</style>
<span class="code">404</span>
<div class="robot"><img src="rendus/robot-p6.jpg"
  alt="The small Cascade robot, alone on the night ground, with nothing to present"></div>
<h1>Nothing measured here.</h1>
<p>Whatever this address promised was never measured, never sealed, never published:
  the address is wrong, or the page has moved.</p>
<nav class="portes" aria-label="Ways out">
  <a class="porte" href="HERO.html">The question &#8594;</a>
  <a class="porte" href="INSTRUMENT.html">The instrument &#8594;</a>
  <a class="porte" href="CONTACT.html">Say a figure is missing &#8594;</a>
</nav>
<span class="sceau">seal {SCEAU} &#183; measured, then frozen</span>
'''

assert "—" not in PAGE
(BASE / "404.html").write_text(PAGE, encoding="utf-8")
print(f"404.html {len(PAGE) / 1e3:.0f} ko")
