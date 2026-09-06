"""THE LIVE CHART of the instrument pages that carry a matcher x threshold grid (screening,
monitoring, scoring). Chosen by Arslane on 9/09/2026 from a board of directions (« B3, une seule
carte », the animated one): the whole page in black, the tool's colour only in strokes and glows;
one chart, one curve per tier over a LINEAR threshold axis, the recall of each shown cell as a
point; ONE floor line you drag across the chart (the slider stays for the keyboard and follows);
what holds the floor at the Wilson LOWER BOUND lights up green and the held zone is tinted; the
hovered cell draws its interval and is read in a fixed side panel; the other half of the record
(authored / synthetic) stays as a dotted ghost when you switch. The grid table stays in the DOM,
painted by the same figures, for keyboard users and readers without a pointer.

The three builders are line-for-line copies of each other; this module holds what they share so
the chart is written once. Every figure comes from the tool's JSON; nothing is typed here."""

# ── the black page : overrides appended after each builder's own CSS ─────────────────────────
CSS_NOIR = '''
  /* THE BLACK PAGE (Arslane, 9/09) : the tool's night becomes near-black, its colour stays in
     strokes, figures and glows ; the parchment section turns black with paper ink, the clone
     terminal too. The variables are re-declared so every rule below inherits the change. */
  :root{--nuit-a:#1a1a1f;--nuit-b:#0e0e11;--nuit-c:#08080a;
    --papier:#0e0e11;--papier-haut:#121215;--encre:#e8e6df;--demi:#a5a39a;--pale:#8f8d84;
    --filet-clair:#2c2c33;--sur:#e8e6df;--sur-pale:#9a988f;--tenu:#7fd4a0}
  .tete{background:radial-gradient(120% 100% at 50% -20%,color-mix(in srgb,var(--accent-titre) 38%,#0e0e11),var(--nuit-b) 70%)}
  /* the lede : one wide line or two, never a three-line block (Arslane : « un bloc moche ») */
  .lede{max-width:none;text-wrap:pretty}
  .terminal{background:linear-gradient(180deg,#131316,#0b0b0d 120px);
    border-color:color-mix(in srgb,var(--accent-vif) 26%,transparent)}
  .terminal::after{background:none}
  .tm-barre{background:linear-gradient(180deg,#17171b,#101013)}
  .basse{border-top:1px solid #1e1e23}
  .basse li::before{background:var(--accent-vif)}
  .clone{background:linear-gradient(163deg,#141417,#0e0e11);box-shadow:none}
  .pied{border-top:1px solid #1e1e23}
  /* the robot keeps leaning over the RIGHT edge of the window, left of the panel's column
     (on the left it sat on the title and the lede, seen on the 9/09 capture) */
  /* the robot leans over the RIGHT edge of the window and is CUT by it (z below the terminal),
     looking down at the chart (pose « regarde », Arslane 9/09 : « faut que le robot regarde
     l'outil et qu'il soit crop correctement avec les bords de l'outil ») */
  .fen-robot{position:relative}
  /* over the window's right edge the robot sat on the title (the panel took the width) : it
     leans over the PANEL's card, at the far right, and looks left, at the chart */
  .pan-col{position:relative}
  .rb{right:-24px;left:auto;width:340px;top:-262px;z-index:2;
    filter:drop-shadow(0 26px 44px rgba(0,0,0,.85)) brightness(.92)}
  @media (max-width:980px){.rb{display:none}}
  /* as wide as the robot allows (three lines at 1440), never the old 52ch block */
  .lede{max-width:min(100%,800px);font-size:clamp(15px,1.15vw,16.5px)}

  /* THE LIVE CHART : the window becomes window + side panel ; the table stays for the keyboard */
  .dessus{width:min(100%,1180px)}
  .poste-grille{display:grid;grid-template-columns:1fr 272px;gap:22px;align-items:start}
  @media (max-width:980px){.poste-grille{grid-template-columns:1fr}.pan{position:static}}
  html.js .t-scroll{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
  .carte{display:block;width:100%;height:auto;font-family:var(--mono);touch-action:none;
    user-select:none;-webkit-user-select:none;cursor:crosshair;margin:2px 0 10px}
  .carte .grille-h{stroke:#1c1c21;stroke-width:1}
  .carte .ordonnee{fill:var(--sur-pale);font-size:10px;text-anchor:end}
  .carte .seuil{fill:var(--sur-pale);font-size:10.5px;text-anchor:middle}
  .carte .seuil.axe{fill:var(--accent-clair)}
  .carte .zone-tenue{fill:var(--tenu);opacity:.06}
  .carte .courbe{fill:none;stroke:#3a3a42;stroke-width:1.4}
  .carte .courbe.axe{stroke:var(--sur);stroke-width:2}
  .carte .fantome{fill:none;stroke:var(--accent-vif);stroke-width:1;stroke-dasharray:3 3;opacity:.55}
  .carte .fantome-pt{fill:none;stroke:var(--accent-vif);stroke-width:1;opacity:.55}
  .carte .pt circle{fill:var(--nuit-c);stroke:#4a4a52;stroke-width:1.5}
  .carte .pt text{fill:var(--sur-pale);font-size:10.5px;text-anchor:middle}
  .carte .pt.tenu circle{fill:var(--tenu);stroke:var(--tenu)}
  .carte .pt.axe circle{stroke:var(--sur)} .carte .pt.axe text{fill:var(--sur)}
  .carte .pt.vise circle{fill:var(--accent-vif);stroke:var(--accent-clair);stroke-width:2}
  .carte .pt.vise text{fill:var(--accent-clair);font-size:13px;font-weight:500}
  .carte .pt.presse circle{stroke:var(--accent-clair);stroke-width:2.5}
  .carte .choix circle{fill:none;stroke:var(--accent-vif);stroke-width:2.5}
  .carte .choix text{fill:var(--accent-clair);font-size:10.5px;text-anchor:middle}
  .carte .intervalle{stroke:var(--accent-clair);stroke-width:2;opacity:.9}
  .carte .viseur{stroke:var(--accent-vif);stroke-width:1;opacity:.7}
  .carte .plancher-l{stroke:var(--accent-clair);stroke-width:1.5;cursor:ns-resize}
  .carte .plancher-prise{fill:transparent;cursor:ns-resize}
  .carte .plancher-poignee{fill:var(--nuit-c);stroke:var(--accent-clair);stroke-width:2;cursor:ns-resize}
  .carte .plancher-t{fill:var(--accent-clair);font-size:11px;text-anchor:end}
  .carte .legende text{font-size:11px;fill:var(--sur-pale)} .carte .legende text.axe{fill:var(--sur)}
  .carte .legende text.fantome-t{fill:var(--accent-vif);opacity:.8}
  /* under 700 px the chart keeps a readable width and scrolls sideways, as the grid did */
  .carte-boite{overflow-x:auto;margin:0 -6px;padding:0 6px}
  @media (max-width:700px){.carte{min-width:640px}}
  .carte-aide{font-family:var(--mono);font-size:11.5px;color:var(--sur-pale);margin:0 0 12px}
  .carte-aide b{color:var(--tenu);font-weight:500}

  .pan{position:sticky;top:20px;z-index:3;border:1px solid #232328;border-left:2px solid var(--accent-vif);
    border-radius:10px;background:#101013;padding:16px 18px 18px;font-family:var(--mono);min-height:300px}
  .pan .qui{font-size:11px;color:var(--sur-pale);letter-spacing:.08em;text-transform:uppercase}
  .pan .nom{font-family:var(--texte);font-size:23px;margin:6px 0 14px;color:var(--sur);line-height:1.15}
  .pan .nom small{color:var(--sur-pale);font-size:14px}
  .pan .gros{font-size:34px;line-height:1;color:var(--sur);margin:2px 0 4px}
  .pan .gros small{font-size:14px;color:var(--sur-pale)}
  .pan .leg{font-size:11.5px;color:var(--sur-pale);margin-bottom:14px;line-height:1.5}
  .pan .plancher{font-size:12px;padding-top:12px;border-top:1px solid #2c2c33;line-height:1.6;color:var(--sur-pale)}
  .pan .plancher b{color:var(--accent-clair);font-size:19px;font-weight:500}
  .pan .tenu{color:var(--tenu)} .pan .pas{color:var(--accent-clair)}
  @media (prefers-reduced-motion:reduce){.caret{animation:none}}
'''


def carte_html(x_titre, y_titre):
    """The chart and its side panel, empty : the JS draws both from the embedded record."""
    return f'''<p class="carte-aide">every point is one cell of the record : hover it to read it, click it to keep it, <b>pull the floor line</b> (or the slider below) and what holds the lower bound lights up</p>
          <div class="carte-boite"><svg class="carte" id="carte" viewBox="0 0 900 400" role="img" aria-label="{y_titre} of every tier at every {x_titre} of the public record, with the recall floor as a line"></svg></div>'''


PANNEAU_HTML = '''<aside class="pan" id="pan" aria-live="polite">
        <div class="qui">the cell under the pointer</div>
        <div class="nom" id="pan-nom">hover a point</div>
        <div class="gros" id="pan-g1"></div><div class="leg" id="pan-l1"></div>
        <div class="gros" id="pan-g2"></div><div class="leg" id="pan-l2"></div>
        <div class="plancher" id="pan-plancher"></div>
      </aside>'''


def js_carte(mot_x, mot_y, mot_fp):
    """The drawing and the hand. `mot_x` names the axis (threshold), `mot_y` the first figure
    (recall), `mot_fp` the second (false alerts), in the tool's own words."""
    return '''
  /* THE LIVE CHART : one curve per tier over a linear ''' + mot_x + ''' axis, the floor as a line you drag. */
  const carte = $("#carte");
  const NS = "http://www.w3.org/2000/svg";
  const CW = 900, CH = 400, CL = 56, CR = 118, CT = 22, CB = 34;
  const XMIN = Math.min(...D.seuilsMontres), XMAX = Math.max(...D.seuilsMontres);
  const cx = (s) => CL + (s - XMIN) / (XMAX - XMIN) * (CW - CL - CR);
  const cy = (t) => (CH - CB) - t * (CH - CB - CT);
  const pcv = (x) => { const s = (x * 100).toFixed(1); return s.endsWith(".0") ? s.slice(0, -2) : s; };
  let vise = null;                       // {p, s} under the pointer, or the pressed cell
  let plancher = D.recommandee.plancher; // the floor, shared with the slider
  const autre = () => (moitie === "authored" ? "synthetic" : "authored");
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

  function dessiner() {
    const g = D[moitie].grille, g2 = D[autre()].grille;
    const presse = cells.find((x) => x.getAttribute("aria-pressed") === "true");
    const cible = vise || (presse ? { p: presse.dataset.p, s: presse.dataset.s } : null);
    let h = "";
    for (const v of [0, .25, .5, .75, 1]) h += '<line class="grille-h" x1="' + CL + '" x2="' + (CW - CR) + '" y1="' + cy(v) + '" y2="' + cy(v) + '"/><text class="ordonnee" x="' + (CL - 8) + '" y="' + (cy(v) + 4) + '">' + Math.round(v * 100) + '</text>';
    h += '<rect class="zone-tenue" x="' + CL + '" y="' + CT + '" width="' + (CW - CL - CR) + '" height="' + Math.max(0, cy(plancher) - CT) + '"/>';
    for (const [p, ligne] of Object.entries(g2)) {
      h += '<polyline class="fantome" points="' + MONTRES.map((s) => cx(+s) + "," + cy(ligne[s].rappel.taux)).join(" ") + '"/>';
      for (const s of MONTRES) h += '<circle class="fantome-pt" cx="' + cx(+s) + '" cy="' + cy(ligne[s].rappel.taux) + '" r="2.5"/>';
    }
    for (const [p, ligne] of Object.entries(g)) {
      const axe = cible && cible.p === p;
      h += '<polyline class="courbe' + (axe ? " axe" : "") + '" points="' + MONTRES.map((s) => cx(+s) + "," + cy(ligne[s].rappel.taux)).join(" ") + '"/>';
    }
    /* the labels of the hovered COLUMN sit left of their point and are pushed apart when two
       curves cross the column at the same height (48.3 over 46.7 on the 9/09 capture) */
    const colonne = [];
    if (cible) {
      for (const [p, ligne] of Object.entries(g)) if (p !== cible.p) colonne.push([cy(ligne[cible.s].rappel.taux), p]);
      colonne.sort((a, b) => a[0] - b[0]);
      let dernier = -99;
      for (const e of colonne) { e[2] = Math.max(e[0], dernier + 12); dernier = e[2]; }
      const depasse = dernier - (CH - CB - 6);          /* zeros stacked under the axis : slide up */
      if (depasse > 0) for (const e of colonne) e[2] -= depasse;
    }
    const yLabel = Object.fromEntries(colonne.map(([y0, p, y]) => [p, y]));
    for (const [p, ligne] of Object.entries(g)) {
      for (const s of MONTRES) {
        const c = ligne[s], t = c.rappel.taux, x = cx(+s), y = cy(t);
        const estVise = cible && cible.p === p && cible.s === s;
        const axe = cible && (cible.p === p || cible.s === s);
        let k = "pt" + (estVise ? " vise" : axe ? " axe" : "") + (c.rappel.bas >= plancher ? " tenu" : "");
        if (presse && presse.dataset.p === p && presse.dataset.s === s) k += " presse";
        let label = "";
        if (estVise || (cible && cible.p === p)) label = '<text x="' + x + '" y="' + (y - 9) + '">' + pcv(t) + '</text>';
        else if (axe) label = '<text x="' + (x - 8) + '" y="' + (yLabel[p] + 4) + '" style="text-anchor:end">' + pcv(t) + '</text>';
        h += '<g class="' + k + '" data-p="' + esc(p) + '" data-s="' + s + '"><circle cx="' + x + '" cy="' + y + '" r="' + (estVise ? 5 : 3) + '"/>' + label + '</g>';
        if (estVise) h += '<line class="intervalle" x1="' + x + '" x2="' + x + '" y1="' + cy(c.rappel.haut) + '" y2="' + cy(c.rappel.bas) + '"/>';
      }
    }
    /* the tool's own pick at this floor, on the authored half and all 51 thresholds : a ring at its true ''' + mot_x + ''' */
    const choix = retenir(plancher);
    if (choix && moitie === "authored" && choix.seuil >= XMIN && choix.seuil <= XMAX) {
      h += '<g class="choix"><circle cx="' + cx(choix.seuil) + '" cy="' + cy(choix.rappel.taux) + '" r="8"/><text x="' + (cx(choix.seuil) + 13) + '" y="' + (cy(choix.rappel.taux) + 4) + '" style="text-anchor:start">the tool\\u2019s pick \\u00b7 ' + esc(choix.palier) + " at " + choix.seuil.toFixed(2) + '</text></g>';
    }
    if (cible) h += '<line class="viseur" x1="' + cx(+cible.s) + '" x2="' + cx(+cible.s) + '" y1="' + CT + '" y2="' + (CH - CB) + '"/>';
    const yf = cy(plancher);
    h += '<rect class="plancher-prise" x="' + CL + '" y="' + (yf - 9) + '" width="' + (CW - CL - CR) + '" height="18"/>'
       + '<line class="plancher-l" x1="' + CL + '" x2="' + (CW - CR) + '" y1="' + yf + '" y2="' + yf + '"/>'
       + '<rect class="plancher-poignee" x="' + (CW - CR - 7) + '" y="' + (yf - 7) + '" width="14" height="14" rx="3"/>'
       + '<text class="plancher-t" x="' + (CW - CR - 12) + '" y="' + (yf - 6) + '">floor ' + plancher.toFixed(2) + '</text>';
    for (const s of MONTRES) h += '<text class="seuil' + (cible && cible.s === s ? " axe" : "") + '" x="' + cx(+s) + '" y="' + (CH - 8) + '">' + s + '</text>';
    /* the names at the right end of their curve, pushed apart when curves end on the same value */
    const fins = Object.entries(g).map(([p, ligne]) => [cy(ligne[MONTRES[MONTRES.length - 1]].rappel.taux), p]).sort((a, b) => a[0] - b[0]);
    let dernier = -99; const ys = [];
    for (const [y0, p] of fins) { const y = Math.max(y0, dernier + 13); dernier = y; ys.push(y); }
    /* curves that end at zero pushed the stack under the axis (monitoring, 9/09) : it slides back up */
    const depasse = dernier - (CH - CB - 4);
    fins.forEach(([y0, p], i) => {
      const y = ys[i] - Math.max(0, depasse);
      h += '<g class="legende"><text x="' + (CW - CR + 8) + '" y="' + (y + 4) + '" class="' + (cible && cible.p === p ? "axe" : "") + '">' + esc(p) + '</text></g>';
    });
    h += '<g class="legende"><text class="fantome-t" x="' + (CW - CR + 8) + '" y="' + (CT + 8) + '">dotted: ' + autre() + '</text></g>';
    carte.innerHTML = h;
  }

  function peindrePanneau() {
    const presse = cells.find((x) => x.getAttribute("aria-pressed") === "true");
    const cible = vise || (presse ? { p: presse.dataset.p, s: presse.dataset.s } : null);
    if (!cible) { $("#pan-nom").textContent = "hover a point"; ["#pan-g1", "#pan-l1", "#pan-g2", "#pan-l2"].forEach((id) => { $(id).textContent = ""; }); }
    else {
      const c = D[moitie].grille[cible.p][cible.s];
      $("#pan-nom").innerHTML = esc(cible.p) + " <small>at " + cible.s + "</small>";
      $("#pan-g1").innerHTML = pcv(c.rappel.taux) + "<small>%</small>";
      $("#pan-l1").textContent = "''' + mot_y + ''', interval " + iv(c.rappel) + ", " + c.rappel.succes + " of " + c.rappel.n;
      $("#pan-g2").innerHTML = pcv(c.fauxPositifs.taux) + "<small>%</small>";
      $("#pan-l2").textContent = "''' + mot_fp + ''', interval " + iv(c.fauxPositifs) + ", " + c.fauxPositifs.succes + " of " + c.fauxPositifs.n;
    }
    const tenues = MONTRES.reduce((n, s) => n + Object.values(D[moitie].grille).filter((l) => l[s].rappel.bas >= plancher).length, 0);
    const total = Object.keys(D[moitie].grille).length * MONTRES.length;
    const c = cible ? D[moitie].grille[cible.p][cible.s] : null;
    $("#pan-plancher").innerHTML = "floor <b>" + plancher.toFixed(2) + "</b> \\u00b7 " + tenues + " of " + total + " shown cells hold the lower bound"
      + (c ? " \\u00b7 this one <span class=\\"" + (c.rappel.bas >= plancher ? "tenu" : "pas") + "\\">" + (c.rappel.bas >= plancher ? "holds" : "does not hold") + "</span> (" + Math.round(c.rappel.bas * 100) + " %)" : "");
  }

  /* the hand : hover the nearest point of the column, click to keep it, pull the floor */
  const pointDe = (ev) => {
    const r = carte.getBoundingClientRect();
    const x = (ev.clientX - r.left) / r.width * CW, y = (ev.clientY - r.top) / r.height * CH;
    let best = null, d0 = 1e9;
    for (const [p, ligne] of Object.entries(D[moitie].grille)) for (const s of MONTRES) {
      const d = Math.hypot(cx(+s) - x, cy(ligne[s].rappel.taux) - y);
      if (d < d0) { d0 = d; best = { p, s }; }
    }
    return d0 < 28 ? best : null;
  };
  let tire = false;
  carte.addEventListener("pointerdown", (ev) => {
    const r = carte.getBoundingClientRect();
    const y = (ev.clientY - r.top) / r.height * CH;
    if (Math.abs(y - cy(plancher)) < 12 || ev.target.classList.contains("plancher-poignee")) { tire = true; carte.setPointerCapture(ev.pointerId); ev.preventDefault(); }
  });
  carte.addEventListener("pointermove", (ev) => {
    if (tire) {
      const r = carte.getBoundingClientRect();
      const y = (ev.clientY - r.top) / r.height * CH;
      const v = Math.min(1, Math.max(0.5, ((CH - CB) - y) / (CH - CB - CT)));
      plancher = Math.round(v * 100) / 100; curseur.value = plancher; rejouer(); return;
    }
    const pt = pointDe(ev);
    if ((pt && (!vise || pt.p !== vise.p || pt.s !== vise.s)) || (!pt && vise)) { vise = pt; dessiner(); peindrePanneau(); }
  });
  carte.addEventListener("pointerup", () => { tire = false; });
  carte.addEventListener("pointerleave", () => { if (!tire) { vise = null; dessiner(); peindrePanneau(); } });
  carte.addEventListener("click", (ev) => {
    if (tire) return;
    const pt = pointDe(ev);
    if (!pt) return;
    const c = cells.find((x) => x.dataset.p === pt.p && x.dataset.s === pt.s);
    if (c) lire(c);
  });
'''
