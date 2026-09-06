#!/usr/bin/env python3
"""L'OFFRE, direction E1 choisie le 4 septembre : les colonnes de nuit.

Trois colonnes aux filets fins, sans cartes, chaque montant en corps d'affiche
(les références collectées avant de dessiner : Linear pour les colonnes,
Vercel pour les prix géants, rangées dans le skill design-arslane). L'ordre
est l'argument : l'évaluation d'abord, la campagne, la licence au-dessus.

CHAQUE CHIFFRE EST SOURCÉ : l'évaluation vient de LICENCES.md du dépôt public,
la campagne et la licence de LICENCE-COMMERCIALE.md (décisions des 25 et
27 août : 12 000 $ fixe ; 30 000 $/an, 30 %% à la signature, solde net 60,
plafond de renouvellement au plus bas de CPI-U et 5 %%). Aucun palier
intermédiaire n'est documenté ; aucun n'est affiché.
"""
import pathlib

BASE = pathlib.Path(__file__).parent
from outil import SCEAU_ROUTING, OUTILS
SCEAU = SCEAU_ROUTING   # lu dans le relevé scellé du vert, jamais tapé (8/09)
# la barre du site (10/09) : les cinq instruments dans l'ordre du rideau, lus dans OUTILS, jamais tapés
NAV = "".join(f'\n    <a href="{o["page_hero"]}">{o["nom"]}</a>' for o in OUTILS.values())
DEPOT_URL = "https://github.com/ArslaneSempai-ui/cascade-routing"

CSS = '''
  :root{--noir:#0e0e11;--noir-b:#08080a;--noir-c:#121215;--filet:#26262c;--sur:#e8e6df;--sur-pale:#9a988f;
    --vert-titre:#23543f;--vert-vif:#57b184;--vert-clair:#a5f7cb;--papier:#dbd7c5;--encre:#1b1d18;
    --texte:"Literata",Georgia,serif;--mono:"Roboto Mono",ui-monospace,Menlo,monospace;--montee:cubic-bezier(.16,.84,.32,1)}
  *{box-sizing:border-box;margin:0}
  html{scroll-behavior:smooth;caret-color:var(--vert-vif);scrollbar-color:var(--vert-titre) var(--noir-b)}
  @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
  body{background:var(--noir);color:var(--sur);font-family:var(--texte);line-height:1.6;overflow-x:hidden;position:relative}
  ::selection{background:var(--vert-vif);color:var(--noir-b)}
  a{text-underline-offset:4px;color:inherit}
  .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
  :focus-visible{outline:3px solid var(--vert-vif);outline-offset:3px;border-radius:2px}
  .colonne{max-width:1180px;margin:0 auto;padding:0 48px;position:relative;z-index:2}
  /* the ground : a fine grid, and the light that follows the pointer (10/09, « effets de souris ») */
  .grille{position:fixed;inset:0;z-index:0;pointer-events:none;
    background-image:linear-gradient(color-mix(in srgb,var(--sur) 4%,transparent) 1px,transparent 1px),
      linear-gradient(90deg,color-mix(in srgb,var(--sur) 4%,transparent) 1px,transparent 1px);background-size:64px 64px;
    mask-image:radial-gradient(ellipse 70% 60% at 50% 20%,#000 30%,transparent 100%)}
  .lumiere{position:fixed;left:0;top:0;width:800px;height:800px;border-radius:50%;z-index:1;pointer-events:none;
    background:radial-gradient(circle,color-mix(in srgb,var(--vert-vif) 18%,transparent),transparent 62%);will-change:transform;filter:blur(10px)}
  html:not(.js) .lumiere{display:none}

  .barre{position:absolute;inset:0 0 auto 0;z-index:40;display:flex;align-items:center;gap:28px;padding:14px 32px}
  .marque{font-weight:700;font-size:19px;letter-spacing:.01em;text-decoration:none;color:var(--sur)}
  .barre nav{display:flex;gap:16px;margin-left:auto}
  .barre nav a{font-size:14.5px;text-decoration:none;color:var(--sur-pale);padding:13px 6px}
  .barre nav a:hover{color:var(--sur);text-decoration:underline;text-decoration-color:var(--vert-vif);text-decoration-thickness:1.5px}
  .barre nav a[aria-current]{color:var(--sur)}
  .sceau{font-family:var(--mono);font-size:11px;color:var(--sur-pale);letter-spacing:.04em}

  .tete{padding:150px 0 20px}
  .h1{font-size:clamp(38px,5vw,66px);font-weight:600;letter-spacing:-.02em;line-height:1.04;text-wrap:balance}
  .lede{font-size:clamp(15px,1.3vw,18.5px);color:var(--sur-pale);max-width:72ch;line-height:1.65;margin-top:18px;text-wrap:balance}
  .lede b{color:var(--sur)}

  /* the three offers : cards that light where the cursor is ; the buttons pinned at the foot, one line */
  .cols{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px;margin:150px 0 10px;align-items:stretch}
  .col{position:relative;display:flex;flex-direction:column;padding:126px 30px 26px;border-radius:16px;background:var(--noir-c);
    border:1px solid var(--filet);--mx:50%;--my:0%;transition:transform .35s var(--montee),border-color .3s}
  .col::before{content:"";position:absolute;inset:0;border-radius:16px;pointer-events:none;opacity:0;transition:opacity .35s;
    background:radial-gradient(460px circle at var(--mx) var(--my),color-mix(in srgb,var(--vert-vif) 14%,transparent),transparent 62%)}
  .col::after{content:"";position:absolute;inset:-1px;border-radius:17px;pointer-events:none;padding:1px;opacity:0;transition:opacity .35s;
    background:radial-gradient(340px circle at var(--mx) var(--my),var(--vert-clair),transparent 70%);
    -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude}
  .col:hover{transform:translateY(-4px)}
  .col:hover::before,.col:hover::after{opacity:1}
  .col.haute{border-color:color-mix(in srgb,var(--vert-vif) 45%,var(--filet))}
  .col.haute::after{opacity:.35}
  .col-robot{position:absolute;top:-96px;left:50%;height:190px;width:auto;transform:translateX(-50%);pointer-events:none;
    filter:drop-shadow(0 26px 40px rgba(0,0,0,.7));transition:transform .4s var(--montee)}
  .col.haute .col-robot{height:214px;top:-116px}
  .c-t{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--sur-pale)}
  .c-prix{font-weight:600;font-size:clamp(40px,4.4vw,64px);letter-spacing:-.02em;line-height:1.05;margin:14px 0 4px;font-variant-numeric:lining-nums tabular-nums}
  .c-prix small{font-size:.32em;font-weight:400;color:var(--sur-pale);letter-spacing:0;white-space:nowrap}
  .col.haute .c-prix{color:var(--vert-clair);text-shadow:0 0 26px color-mix(in srgb,var(--vert-vif) 40%,transparent)}
  .c-qui{font-size:14px;color:var(--sur-pale);min-height:3em;line-height:1.55;border-bottom:1px solid var(--filet);padding-bottom:16px;margin-bottom:16px}
  .c-plus{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:color-mix(in srgb,var(--sur-pale) 70%,transparent);margin-bottom:8px}
  .c-liste{list-style:none;padding:0;display:flex;flex-direction:column;gap:9px;font-size:13.5px;color:var(--sur-pale)}
  .c-liste li{padding-left:22px;position:relative;line-height:1.5}
  .c-liste li::before{content:"";position:absolute;left:0;top:.5em;width:12px;height:7px;border-left:2px solid var(--vert-vif);border-bottom:2px solid var(--vert-vif);transform:rotate(-45deg)}
  .c-liste b{color:var(--sur)}
  .cta{display:block;text-decoration:none;margin-top:auto;padding-top:26px;font-family:var(--texte);font-size:16px;font-weight:600;color:var(--vert-clair)}
  .cta .b{display:inline-flex;align-items:baseline;gap:12px;padding:13px 24px;border-radius:10px;border:1px solid color-mix(in srgb,var(--vert-vif) 45%,transparent);transition:background .2s,color .2s,border-color .2s}
  .cta:hover .b{background:var(--vert-vif);color:var(--noir-b);border-color:var(--vert-vif)}
  .col.haute .cta .b{background:var(--vert-vif);color:var(--noir-b);border-color:var(--vert-vif)}
  .cta .fl{transition:transform .2s var(--montee)}
  .cta:hover .fl{transform:translateX(4px)}
  .c-fin{font-family:var(--mono);font-size:10.5px;letter-spacing:.05em;color:color-mix(in srgb,var(--sur-pale) 70%,transparent);margin-top:14px;line-height:1.7;min-height:3.4em}

  /* the days : three lanes to scale, the papers on their lane at their date, one line reads the day */
  .jours{padding:80px 0 30px}
  .jours-t{font-size:clamp(24px,2.4vw,32px);font-weight:600;letter-spacing:-.01em;line-height:1.15}
  .jours-l{font-size:17px;color:var(--sur-pale);line-height:1.6;margin-top:8px;max-width:none}
  .axe-boite{margin-top:34px;border:1px solid var(--filet);border-radius:16px;background:var(--noir-c);padding:36px 40px 30px;position:relative;overflow:hidden}
  .axe-defile{overflow-x:auto;overflow-y:hidden}
  .axe{position:relative;height:364px;--y:324px;min-width:820px;user-select:none;cursor:ew-resize;touch-action:pan-y}
  .regle{position:absolute;left:0;right:0;top:var(--y);height:2px;background:var(--filet)}
  .regle i{position:absolute;left:0;top:0;height:2px;width:calc(130/150*100%);background:linear-gradient(90deg,var(--vert-vif),var(--vert-clair))}
  .graduations span{position:absolute;left:calc(var(--d)/150*100%);top:calc(var(--y) + 10px);transform:translateX(-50%);font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;color:var(--sur-pale);text-align:center;line-height:1.4;white-space:nowrap}
  .graduations span i{display:block;width:1px;height:10px;background:var(--sur-pale);margin:-14px auto 4px}
  .graduations .coupure i{height:18px;width:12px;background:none;border-left:2px solid var(--sur-pale);border-right:2px solid var(--sur-pale);transform:skewX(-30deg);margin-top:-18px}
  .graduations span[style*="--d:0"]{transform:none;text-align:left}.graduations span[style*="--d:0"] i{margin-left:0}
  .graduations span[style*="--d:150"]{transform:translateX(-100%);text-align:right}.graduations span[style*="--d:150"] i{margin-right:0}
  .curseur{position:absolute;top:0;left:calc(12/150*100%);width:2px;height:calc(var(--y) + 8px);background:var(--vert-clair);transform:translateX(-50%);box-shadow:0 0 14px var(--vert-vif);z-index:5}
  .curseur::after{content:"";position:absolute;left:50%;bottom:-6px;width:12px;height:12px;border-radius:50%;background:var(--vert-clair);transform:translateX(-50%)}
  .curseur span{position:absolute;top:2px;left:10px;font-family:var(--mono);font-size:11px;letter-spacing:.1em;color:var(--vert-clair);white-space:nowrap;background:var(--noir-c);padding:2px 6px;border-radius:4px}
  html:not(.js) .curseur{display:none}
  .voies{position:absolute;left:0;right:0;top:34px}
  .voie{position:absolute;left:0;right:0;top:calc(var(--t)*92px);height:84px;border-bottom:1px solid color-mix(in srgb,var(--filet) 70%,transparent);transition:background .3s}
  .voie:hover{background:color-mix(in srgb,var(--vert-vif) 5%,transparent)}
  .v-nom{position:absolute;left:0;top:6px;font-family:var(--texte);font-size:15px;font-weight:600;color:var(--sur);z-index:2}
  .voie[data-l="eval"] .v-nom{left:112px}
  .barre-v{position:absolute;left:calc(var(--a)/150*100%);width:calc((var(--b) - var(--a))/150*100%);top:60px;height:6px;border-radius:3px;background:color-mix(in srgb,var(--vert-vif) 50%,transparent)}
  .barre-v.pointille{background:repeating-linear-gradient(90deg,color-mix(in srgb,var(--vert-vif) 50%,transparent) 0 6px,transparent 6px 10px)}
  .v-robot{position:absolute;left:-4px;top:-22px;height:98px;width:auto;filter:drop-shadow(0 16px 26px rgba(0,0,0,.65));z-index:1}
  .anneau{position:absolute;left:calc(30/150*100%);top:26px;width:40px;height:40px;transform:translateX(-50%);z-index:2}
  .anneau svg{width:40px;height:40px;transform:rotate(-90deg)}
  .anneau circle{fill:var(--noir-c);stroke:var(--filet);stroke-width:4}
  .anneau .plein{fill:none;stroke:var(--vert-clair);stroke-dasharray:100.5;stroke-dashoffset:100.5;transition:stroke-dashoffset .2s}
  html:not(.js) .anneau .plein{stroke-dashoffset:0}
  .pap{position:absolute;left:calc(var(--d)/150*100%);top:12px;transform:translateX(var(--tx));width:150px;background:linear-gradient(165deg,#f2edda,#ded8c3);color:var(--encre);border-radius:3px;
    padding:7px 9px;box-shadow:0 12px 24px rgba(0,0,0,.55);display:flex;flex-direction:column;gap:2px;opacity:.5;transition:opacity .3s}
  .pap.vu,html:not(.js) .pap{opacity:1}
  .pap>span{font-family:var(--mono);font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:#55523f;border-bottom:1px solid #9d9a83;padding-bottom:3px}
  .pap b{font-size:12px;font-weight:600;line-height:1.2}
  .voie[data-l="eval"] .pap{top:14px}
  .etat{font-size:18px;line-height:1.5;color:var(--sur);margin:22px auto 0;max-width:80ch;text-align:center;text-wrap:balance;min-height:2.6em}
  .etat b{color:var(--vert-clair);font-weight:600}
  .commande-jour{display:flex;justify-content:center;gap:12px;align-items:center;margin-top:14px;font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:var(--sur-pale)}
  .commande-jour button{font:inherit;letter-spacing:inherit;color:var(--vert-clair);background:none;border:1px solid color-mix(in srgb,var(--vert-vif) 45%,transparent);border-radius:8px;padding:8px 14px;cursor:pointer}
  .commande-jour button:hover{background:var(--vert-vif);color:var(--noir-b)}
  html:not(.js) .commande-jour{display:none}
  /* the closing paragraph runs the whole width of the column : never piled on the left (Arslane, 11/09) */
  .note-fin{font-size:17px;line-height:1.65;color:var(--sur-pale);max-width:none;margin:34px 0 90px;text-wrap:pretty}
  .note-fin a{color:var(--sur);text-decoration:none;border-bottom:1px solid color-mix(in srgb,var(--vert-clair) 50%,transparent)}
  .note-fin b{color:var(--sur);font-weight:600}

  .pied{background:var(--noir-b);color:var(--sur);padding:52px 0;position:relative;z-index:2;border-top:1px solid var(--filet)}
  .pied .colonne{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:baseline}
  .pied-p{font-size:clamp(17px,1.8vw,23px);font-weight:600}
  .pied-p em{font-style:italic;color:var(--vert-clair)}
  .pied .sceau{color:var(--sur-pale)}

  @media (max-width:1080px){
    .colonne{padding:0 22px}
    .barre{padding:12px 18px;gap:14px}
    .barre nav{display:none}
    .tete{padding-top:100px}
    .cols{grid-template-columns:1fr;gap:110px;margin-top:130px}
    .axe-boite{padding:24px 18px}
  }
  @media (prefers-reduced-motion:reduce){
    *{transition-duration:.01ms!important;animation-duration:.01ms!important}.lumiere{display:none}}
'''

JS = r'''<script>
(function(){
  const reduit = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const l = document.querySelector('.lumiere'); let tx = innerWidth * .6, ty = 320, x = tx, y = ty;
  addEventListener('pointermove', e => { tx = e.clientX; ty = e.clientY; }, {passive: true});
  if (!reduit) (function pas(){ x += (tx - x) * .07; y += (ty - y) * .07; l.style.transform = 'translate(' + (x - 400) + 'px,' + (y - 400) + 'px)'; requestAnimationFrame(pas); })();
  document.querySelectorAll('.col').forEach(c => { const r = c.querySelector('.col-robot');
    c.addEventListener('pointermove', e => { const b = c.getBoundingClientRect(); const px = (e.clientX - b.left) / b.width, py = (e.clientY - b.top) / b.height;
      c.style.setProperty('--mx', (px * 100) + '%'); c.style.setProperty('--my', (py * 100) + '%');
      if (r && !reduit) r.style.transform = 'translateX(-50%) translateY(-10px) rotate(' + ((px - .5) * 8) + 'deg)'; });
    c.addEventListener('pointerleave', () => { if (r) r.style.transform = ''; }); });
  const fmt = n => '$' + n.toLocaleString('en-US');
  const io = new IntersectionObserver(es => es.forEach(en => { if (!en.isIntersecting) return; io.unobserve(en.target);
    const txt = en.target.childNodes[0]; const m = /\$([\d,]+)/.exec(txt.textContent); if (!m) return;
    const fin = parseInt(m[1].replace(/,/g, ''), 10); if (!fin || reduit) return; const t0 = performance.now(), d = 1100;
    (function tick(t){ const p = Math.min(1, (t - t0) / d), e = 1 - Math.pow(1 - p, 3); txt.textContent = fmt(Math.round(fin * e)); if (p < 1) requestAnimationFrame(tick); })(t0);
  }), {threshold: .4});
  document.querySelectorAll('.c-prix').forEach(c => io.observe(c));
  // the days : the axis, the cursor, the lanes, one line that reads the day
  const axe = document.getElementById('axe'), cur = document.getElementById('curseur'), lab = document.getElementById('jour'), etat = document.getElementById('etat');
  if (!axe) return;
  const LIC = 30000, PART = 0.30, CAMP = 12000;        // the documented terms ; the amounts below are computed, never typed
  const ECHELLE = 150, versJour = u => u <= 130 ? Math.round(u) : Math.round(130 + (u - 130) / 20 * 235);
  let u = 12, actif = false;
  const poser = v => { u = Math.max(0, Math.min(ECHELLE, v)); cur.style.left = (u / ECHELLE * 100) + '%'; const j = versJour(u);
    lab.textContent = 'Day ' + j; cur.setAttribute('aria-valuenow', j);
    document.querySelectorAll('.pap').forEach(p => { const d = parseFloat(p.style.getPropertyValue('--d')); p.classList.toggle('vu', u >= d - 0.5); });
    const pl = document.querySelector('.anneau .plein'); if (pl) pl.style.strokeDashoffset = 100.5 * (1 - Math.min(30, j) / 30);
    let s;
    if (j <= 30) s = '<b>Day ' + j + ' of the thirty.</b> The counter runs at your desk and results stay internal. No data has reached us, and nothing is owed.';
    else if (j < 45) s = '<b>Day ' + j + '.</b> The thirty days have run. Nothing is owed until you sign; your legal team can read the papers now.';
    else if (j < 105) s = '<b>Day ' + j + '.</b> Signed ' + (j - 45 === 0 ? 'today' : (j - 45) + ' days ago') + '. Campaign: the invoice (' + fmt(CAMP) + ', fixed) is settled and the sealed report is at your desk. Licence: 30% paid (' + fmt(LIC * PART) + '); the balance (' + fmt(LIC * (1 - PART)) + ') falls due in ' + (105 - j) + ' days.';
    else if (j < 365) s = '<b>Day ' + j + '.</b> The balance is settled. The licence year runs on all five instruments, updates included, with recertification on fresh records over the period you declare.';
    else s = '<b>The twelfth month.</b> Renewal capped at the lower of CPI-U and 5% above this year.';
    etat.innerHTML = s; };
  const depuis = e => { const b = axe.getBoundingClientRect(); return (e.clientX - b.left) / b.width * ECHELLE; };
  axe.addEventListener('pointerdown', e => { actif = true; axe.setPointerCapture(e.pointerId); poser(depuis(e)); });
  axe.addEventListener('pointermove', e => { if (actif) poser(depuis(e)); });
  axe.addEventListener('pointerup', () => actif = false); axe.addEventListener('pointercancel', () => actif = false);
  cur.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { poser(u + 2); e.preventDefault(); } if (e.key === 'ArrowLeft') { poser(u - 2); e.preventDefault(); } });
  document.getElementById('courir').addEventListener('click', () => { if (reduit) { poser(ECHELLE); return; }
    const t0 = performance.now(), d = 6000; actif = false; (function pas(t){ const p = Math.min(1, (t - t0) / d); poser(p * ECHELLE); if (p < 1 && !actif) requestAnimationFrame(pas); })(t0); });
  poser(u);
})();
</script>
'''

PAGE = f'''<!doctype html><html lang="en">
<meta charset="utf-8"><title>Cascade &#183; pricing</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta property="og:type" content="website">
<meta property="og:title" content="Cascade: what an engagement buys">
<meta property="og:description" content="Evaluate free for thirty days on your own records. Then one sealed measurement campaign at a fixed price, or the annual licence. Nothing here asks for trust before measurement.">
<meta property="og:url" content="https://cascade-routing.com/engagement.html">
<meta property="og:image" content="https://cascade-routing.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="description" content="Evaluate free for thirty days on your own records. Then one sealed measurement campaign at a fixed price, or the annual licence. Nothing here asks for trust before measurement.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M0 0h16L0 16z' fill='%2314251e'/%3E%3Cpath d='M16 0v16H0z' fill='%2323543f'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<link rel="stylesheet" href="fontes/roboto-mono.css">
<script>document.documentElement.classList.add("js")</script>
<style>{CSS}</style>
<div class="grille" aria-hidden="true"></div><div class="lumiere" aria-hidden="true"></div>
<header class="barre">
  <a class="marque" href="ACCUEIL.html">CASCADE</a>
  <nav aria-label="Site">{NAV}
    <a href="ENGAGEMENT.html" aria-current="page">Pricing</a>
    <a href="CONTACT.html">Contact</a>
  </nav>
  <span class="sceau">measured, then frozen</span>
</header>

<main>
<section class="tete"><div class="colonne">
  <h1 class="h1">What an engagement buys.</h1>
  <p class="lede"><b>Test any of the five instruments for thirty days on your own records.</b><br>
    Run one sealed campaign when you are ready. Then license it for the year, when the results
    make the case.</p>
</div></section>

<section aria-label="The three steps"><div class="colonne">
  <div class="cols">
    <div class="col">
      <img class="col-robot" src="rendus/robot-salut.webp" alt="">
      <p class="c-t">the evaluation</p>
      <p class="c-prix">$0<small> &#183; 30 days</small></p>
      <p class="c-qui">For deciding. Your records, your machine, nothing to sign.</p>
      <ul class="c-liste">
        <li>The whole tool, <b>on your own records</b></li>
        <li>One plan, each Cascade tool: <b>Routing</b>, <b>Screening</b>, <b>Monitoring</b> and <b>Scoring</b> alike, and the <b>Dossier</b> that reads them</li>
        <li>Counter starts at first use, instead of at download</li>
        <li>Results stay internal, no production</li>
      </ul>
      <a class="cta" href="{DEPOT_URL}"><span class="b">Clone and run <span class="fl" aria-hidden="true">&#8594;</span></span></a>
      <p class="c-fin">granted in the public licence itself</p>
    </div>
    <div class="col">
      <img class="col-robot" src="rendus/robot-penche.webp" alt="">
      <p class="c-t">the campaign</p>
      <p class="c-prix">$12,000<small> fixed</small></p>
      <p class="c-qui">For the file your reviewers will open. One campaign, one deliverable.</p>
      <p class="c-plus">everything in the evaluation, plus</p>
      <ul class="c-liste">
        <li><b>What suffices, tool by tool</b>: field by field on Routing, matcher and threshold on Screening, scenario and threshold on Monitoring, factor and threshold on Scoring; the Dossier binds the four</li>
        <li>Intervals, refusals under twenty observations</li>
        <li>A <b>sealed, signed report</b> your audit team verifies without us</li>
        <li>Your data stays with you; we do not read it</li>
      </ul>
      <a class="cta" href="CONTACT.html"><span class="b">Start with a message <span class="fl" aria-hidden="true">&#8594;</span></span></a>
      <p class="c-fin">one campaign &#183; one sealed deliverable</p>
    </div>
    <div class="col haute">
      <img class="col-robot" src="rendus/robot-vert-tient.webp" alt="">
      <p class="c-t">the licence</p>
      <p class="c-prix">$30,000<small> a year</small></p>
      <p class="c-qui">For running it as yours. Commercial use, updates included.</p>
      <p class="c-plus">everything in the campaign, plus</p>
      <ul class="c-liste">
        <li>Commercial use for your own business</li>
        <li>The same licence covers <b>each Cascade tool</b>: Routing, Screening, Monitoring, Scoring, one paper</li>
        <li>And the <b>Dossier</b>: the cross-tool piece your regulator reads, sealed, verified without us</li>
        <li>The <b>licensed component</b>, kept unpublished</li>
        <li>Updates included for each paid term</li>
        <li><b>Recertify</b> on fresh records, re-sealed, on the validity period you declare</li>
        <li>One legal entity signs; affiliates named, instead of assumed</li>
      </ul>
      <a class="cta" href="CONTACT.html"><span class="b">Talk terms <span class="fl" aria-hidden="true">&#8594;</span></span></a>
      <p class="c-fin">30% on signature &#183; net 60 &#183; renewal capped at the lower of CPI&#8209;U and 5%</p>
    </div>
  </div>
</div></section>

<section class="jours" aria-label="The days"><div class="colonne">
  <p class="jours-t">The days.</p>
  <p class="jours-l">Thirty days to decide, on your own records. Then a signature, sixty days to the balance, and the year.</p>
  <div class="axe-boite"><div class="axe-defile">
    <div class="axe" id="axe">
      <div class="voies">
        <div class="voie" style="--t:0" data-l="eval"><span class="v-nom">The evaluation</span>
          <i class="barre-v" style="--a:0;--b:30"></i>
          <img class="v-robot" src="rendus/robot-salut.webp" alt="">
          <span class="anneau" aria-hidden="true"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="16"/><circle cx="20" cy="20" r="16" class="plein"/></svg></span>
          <span class="pap" style="--d:30;--tx:34px"><span>thirty days</span><b>granted in the public licence</b></span>
        </div>
        <div class="voie" style="--t:1" data-l="camp"><span class="v-nom">The campaign</span>
          <i class="barre-v pointille" style="--a:45;--b:76"></i>
          <span class="pap" style="--d:45;--tx:0"><span>engagement letter</span><b>$12,000 fixed</b></span>
          <span class="pap" style="--d:76;--tx:12px"><span>sealed report</span><b>at your desk, verified without us</b></span>
        </div>
        <div class="voie" style="--t:2" data-l="lic"><span class="v-nom">The licence</span>
          <i class="barre-v" style="--a:45;--b:150"></i>
          <span class="pap" style="--d:45;--tx:0"><span>commercial licence</span><b>30% on signature</b></span>
          <span class="pap" style="--d:105;--tx:-50%"><span>balance</span><b>net 60 days</b></span>
          <span class="pap" style="--d:150;--tx:-100%"><span>the twelfth month</span><b>renewal capped, the lower of CPI-U and 5%</b></span>
        </div>
      </div>
      <div class="graduations">
        <span style="--d:0"><i></i>Day 0<br>first use</span><span style="--d:30"><i></i>Day 30</span><span style="--d:45"><i></i>Signature</span>
        <span style="--d:105"><i></i>+ 60 days</span><span class="coupure" style="--d:130"><i></i></span><span style="--d:150"><i></i>Twelfth month</span>
      </div>
      <div class="regle"><i></i></div>
      <div class="curseur" id="curseur" role="slider" aria-valuemin="0" aria-valuemax="365" aria-valuenow="12" tabindex="0" aria-label="Day"><span id="jour">Day 12</span></div>
    </div>
  </div>
    <p class="etat" id="etat">Thirty days on your records before anything is signed; what is bought afterwards is delivered at your desk and verified there, without us.</p>
    <div class="commande-jour"><span>drag the day, or</span><button type="button" id="courir">run the year</button></div>
  </div>
  <p class="note-fin">One person answers, at <a href="mailto:contact@cascade-routing.com">contact@cascade-routing.com</a>; nothing is signed during the thirty days, and your vendor onboarding can run while they pass. <b>What none of this certifies:</b> the report proves what was measured and no more, external publication of engagement results is excluded from the first day, and the full terms are on <a href="ANNEXE-TERMS.html">the terms page</a>, in the same words the paper uses.</p>
</div></section>
</main>

<footer class="pied"><div class="colonne">
  <p class="pied-p">Your records stay on your machine, and <em>no data leaves the network.</em></p>
  <span class="sceau">content hash {SCEAU} &#183; measured, then frozen</span>
</div></footer>
{JS}
'''

assert "—" not in PAGE, "un cadratin s'est glissé dans la page"
(BASE / "ENGAGEMENT.html").write_text(PAGE, encoding="utf-8")
print(f"ENGAGEMENT.html {len(PAGE) / 1e3:.0f} ko")
