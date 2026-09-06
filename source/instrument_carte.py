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


# ═══════════════════════════════════════════════════════════════════════════════════════════
# THE TWO INSTRUMENTS WITHOUT A THRESHOLD GRID, same language (Arslane, 9/09 : « oui, les deux
# comme ça ») : one chart, one line you drag, what holds lights up, a side panel reads the thing
# under the pointer.
#   VERT : every routing of the fields over the tiers (7^5 = 16 807, the ones optimise
#          enumerates) as a cloud of cost x accuracy, the frontier drawn, the BUDGET a vertical
#          line you drag ; the best routing under it lights up and the panel names it field by
#          field ; hovering a frontier point reads its routing, clicking it composes it.
#   ONYX : the questions' seals on a time axis (days since measured), the declared RHYTHM a
#          vertical line you drag (a what-if, said as such) ; a seal past it would lose « fresh »
#          and the --next lines say so ; the panel reads the five sealed verdicts of the
#          question under the pointer.
# ═══════════════════════════════════════════════════════════════════════════════════════════

CSS_VERT = '''
  /* the vert names its colours differently : aliased so the shared chart rules apply */
  :root{--accent-titre:var(--vert-titre);--accent-vif:var(--vert-vif);--accent-clair:var(--vert-clair);
    --sur-vert:#e8e6df;--sur-vert-pale:#9a988f;--sur:#e8e6df;--sur-pale:#9a988f}
  .reserves{background:var(--nuit-b);color:var(--sur-vert);border-top:1px solid #1e1e23}
  .reserves p{color:var(--sur-vert-pale)} .reserves b,.reserves code{color:var(--sur-vert)}
  .vos-t{color:var(--vert-vif)}
  .term{background:linear-gradient(163deg,#141417,#0e0e11);box-shadow:none}
  .ouvrir{color:var(--vert-clair);border-color:color-mix(in srgb,var(--vert-vif) 55%,transparent)}
  .ouvrir:hover{background:var(--vert-vif);color:var(--nuit-c);border-color:var(--vert-vif)}
  .pan .plancher b{font-size:12.5px}          /* the field → tier list, not a big figure */
  .carte .nuage circle{fill:#26262c}
  .carte .front{fill:none;stroke:#6a6a72;stroke-width:1.2}
  .carte .pt-front circle{fill:var(--nuit-c);stroke:#8a8a92;stroke-width:1.2}
  .carte .pt-front.tenu circle{fill:var(--tenu);stroke:var(--tenu)}
  .carte .pt-front.vise circle{fill:var(--accent-vif);stroke:var(--accent-clair);stroke-width:2}
  .carte .repere circle{fill:none;stroke:var(--accent-clair);stroke-width:1.5;stroke-dasharray:2 2}
  .carte .repere text{fill:var(--sur-pale);font-size:10.5px}
  .carte .choix-t{fill:var(--accent-clair);font-size:11px}
  .carte .ligne-l{stroke:var(--accent-clair);stroke-width:1.5;cursor:ew-resize}
  .carte .ligne-prise{fill:transparent;cursor:ew-resize}
  .carte .ligne-poignee{fill:var(--nuit-c);stroke:var(--accent-clair);stroke-width:2;cursor:ew-resize}
  .carte .ligne-t{fill:var(--accent-clair);font-size:11px;text-anchor:middle}
  .carte .abscisse{fill:var(--sur-pale);font-size:10.5px;text-anchor:middle}
'''

CSS_ONYX = '''
  .carte .piste{stroke:#232328;stroke-width:1}
  .carte .nomq{fill:var(--sur-pale);font-size:12px} .carte .nomq.axe{fill:var(--accent-clair)}
  .carte .pierre circle{fill:var(--nuit-c);stroke:var(--sur);stroke-width:2}
  .carte .pierre.tenu circle{fill:var(--tenu);stroke:var(--tenu)}
  .carte .pierre.pas circle{fill:var(--nuit-c);stroke:var(--accent-clair);stroke-width:2;stroke-dasharray:3 2}
  .carte .pierre text{fill:var(--sur);font-size:10.5px;text-anchor:middle}
  .carte .pierre.vise circle{stroke:var(--accent-clair);stroke-width:3.5}
  .carte .rythme{stroke:#2c2c33;stroke-width:1;stroke-dasharray:2 4}
  .carte .abscisse{fill:var(--sur-pale);font-size:10.5px;text-anchor:middle}
  .carte .ligne-l{stroke:var(--accent-clair);stroke-width:1.5;cursor:ew-resize}
  .carte .ligne-prise{fill:transparent;cursor:ew-resize}
  .carte .ligne-poignee{fill:var(--nuit-c);stroke:var(--accent-clair);stroke-width:2;cursor:ew-resize}
  .carte .ligne-t{fill:var(--accent-clair);font-size:11px;text-anchor:middle}
  .pan .verdicts{font-size:12px;line-height:1.7;color:var(--sur-pale);padding-top:12px;border-top:1px solid #2c2c33}
  .pan .verdicts b{color:var(--sur);font-weight:500}
'''

CARTE_VERT_HTML = '''<p class="carte-aide">every dot is one routing of the five fields, priced and scored from the sealed bricks ; the line through the bright dots is the frontier no routing beats · <b>pull the budget line</b> (or the slider below), the best routing under it lights up · hover a frontier dot to read it, click it to compose it</p>
          <div class="carte-boite"><svg class="carte" id="carte" viewBox="0 0 900 400" role="img" aria-label="Every routing as cost against accuracy, the frontier, and the budget as a line"><g id="carte-nuage"></g><g id="carte-vif"></g></svg></div>'''

PANNEAU_VERT_HTML = '''<aside class="pan" id="pan" aria-live="polite">
        <div class="qui">the routing under the pointer</div>
        <div class="nom" id="pan-nom"></div>
        <div class="gros" id="pan-g1"></div><div class="leg" id="pan-l1"></div>
        <div class="gros" id="pan-g2"></div><div class="leg" id="pan-l2"></div>
        <div class="plancher" id="pan-plancher"></div>
      </aside>'''

CARTE_ONYX_HTML = '''<p class="carte-aide">each stone is one question's sealed record, placed at its age in days · <b>pull the rhythm line</b> to ask what a shorter or longer rhythm would change : a stone past it would lose its « fresh » control, and the --next lines say so · hover a stone to read its five verdicts</p>
          <div class="carte-boite"><svg class="carte" id="carte" viewBox="0 0 900 300" role="img" aria-label="The questions' seals on a time axis, with the declared rhythm as a line"></svg></div>'''

PANNEAU_ONYX_HTML = '''<aside class="pan" id="pan" aria-live="polite">
        <div class="qui">the question under the pointer</div>
        <div class="nom" id="pan-nom">hover a stone</div>
        <div class="gros" id="pan-g1"></div><div class="leg" id="pan-l1"></div>
        <div class="verdicts" id="pan-verdicts"></div>
      </aside>'''


JS_VERT = '''
  /* THE LIVE CHART OF THE VERT : the cloud of routings, the frontier, the budget line you drag. */
  const carte = $("#carte"), nuageG = $("#carte-nuage"), vifG = $("#carte-vif");
  const CW = 900, CH = 400, CL = 56, CR = 30, CT = 26, CB = 34;
  const xl = (cout) => CL + Math.log10(Math.max(cout * 100, 1)) / 5 * (CW - CL - CR);   /* $ per 100k, log 1..100k */
  const yl = (just) => (CH - CB) - just / 100 * (CH - CB - CT);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  let viseV = null;                          /* the frontier point under the pointer */
  const budgetDe = () => Math.pow(10, parseFloat(curseur.value)) / 100;
  /* the cloud, drawn ONCE : every routing, thinned to one in three (the eye cannot tell) */
  (() => {
    let h = ""; let i = 0;
    const marche = (k, r, cout, just) => {
      if (k === F.length) { if (i++ % 3 === 0) h += '<circle cx="' + xl(cout).toFixed(0) + '" cy="' + yl(just / F.length).toFixed(0) + '" r="1.2"/>'; return; }
      for (const t of T) marche(k + 1, r, cout + D.price[t][F[k]], just + D.acc[t][F[k]]);
    };
    marche(0, {}, 0, 0);
    nuageG.innerHTML = '<g class="nuage">' + h + "</g>";
  })();
  const memeR = (a, b) => F.every((f) => a[f] === b[f]);
  function dessinerV() {
    const budget = budgetDe();
    let h = "";
    for (const v of [0, 25, 50, 75, 100]) h += '<line class="grille-h" x1="' + CL + '" x2="' + (CW - CR) + '" y1="' + yl(v) + '" y2="' + yl(v) + '"/><text class="ordonnee" x="' + (CL - 8) + '" y="' + (yl(v) + 4) + '">' + v + '</text>';
    ["$1", "$10", "$100", "$1k", "$10k", "$100k"].forEach((lab, k) => { h += '<text class="abscisse" x="' + (CL + k / 5 * (CW - CL - CR)).toFixed(0) + '" y="' + (CH - 8) + '">' + lab + '</text>'; });
    h += '<rect class="zone-tenue" x="' + CL + '" y="' + CT + '" width="' + Math.max(0, xl(budget) - CL).toFixed(0) + '" height="' + (CH - CB - CT) + '"/>';
    h += '<polyline class="front" points="' + frontiere.map((p) => xl(p.cout).toFixed(0) + "," + yl(p.just).toFixed(0)).join(" ") + '"/>';
    let best = null;
    for (const p of frontiere) { if (p.cout <= budget) best = p; else break; }
    for (const p of frontiere) {
      const k = "pt-front" + (p.cout <= budget ? " tenu" : "") + (viseV === p ? " vise" : "");
      h += '<g class="' + k + '"><circle cx="' + xl(p.cout).toFixed(0) + '" cy="' + yl(p.just).toFixed(0) + '" r="' + (viseV === p ? 5 : 3.2) + '"/></g>';
    }
    const pub = lire(D.publie.routage), vis = lire(D.vise.routage);
    for (const [c, nom] of [[pub, "published \\u00b7 " + fmtC(pub.cout)], [vis, "file-aimed \\u00b7 " + fmtC(vis.cout)]]) {
      h += '<g class="repere"><circle cx="' + xl(c.cout).toFixed(0) + '" cy="' + yl(c.just).toFixed(0) + '" r="7"/><text x="' + (xl(c.cout) + 11).toFixed(0) + '" y="' + (yl(c.just) + 16).toFixed(0) + '">' + nom + '</text></g>';
    }
    /* the routing composed right now (the grid, the chips, or the budget) : a ring */
    const cur = lire(routage);
    h += '<g class="choix"><circle cx="' + xl(cur.cout).toFixed(0) + '" cy="' + yl(cur.just).toFixed(0) + '" r="9"/><text class="choix-t" x="' + (xl(cur.cout) + 13).toFixed(0) + '" y="' + (yl(cur.just) - 8).toFixed(0) + '">your routing \\u00b7 ' + cur.just.toFixed(1) + " % at " + fmtC(cur.cout) + '</text></g>';
    const xb = xl(budget);
    h += '<rect class="ligne-prise" x="' + (xb - 9).toFixed(0) + '" y="' + CT + '" width="18" height="' + (CH - CB - CT) + '"/>'
       + '<line class="ligne-l" x1="' + xb.toFixed(0) + '" x2="' + xb.toFixed(0) + '" y1="' + CT + '" y2="' + (CH - CB) + '"/>'
       + '<rect class="ligne-poignee" x="' + (xb - 7).toFixed(0) + '" y="' + (CT - 8) + '" width="14" height="14" rx="3"/>'
       + '<text class="ligne-t" x="' + xb.toFixed(0) + '" y="' + (CT - 12) + '">budget ' + fmtC(budget) + ' /100k docs</text>';
    vifG.innerHTML = h;
  }
  function peindrePanneauV() {
    const p = viseV || { r: routage, ...lire(routage) };
    const pub = lire(D.publie.routage);
    $("#pan-nom").innerHTML = viseV ? "a frontier routing" : (memeR(routage, D.publie.routage) ? "the published routing" : memeR(routage, D.vise.routage) ? "the file-aimed routing" : "your routing");
    $("#pan-g1").innerHTML = p.just.toFixed(1) + "<small>%</small>";
    $("#pan-l1").textContent = "per-field mean accuracy, no interval (the tool\\u2019s own figure)";
    $("#pan-g2").textContent = fmtC(p.cout);
    $("#pan-l2").textContent = "per 100 000 documents, assumed prices";
    const dj = p.just - pub.just, dc = (p.cout - pub.cout) * 100;
    $("#pan-plancher").innerHTML = F.map((f) => esc(f) + " \\u2192 <b>" + esc(p.r[f]) + "</b>").join("<br>")
      + "<br><span class=\\"" + (memeR(p.r, D.publie.routage) ? "tenu" : "pas") + "\\">" + (memeR(p.r, D.publie.routage) ? "this is the published routing" : "vs published " + (dj >= 0 ? "+" : "\\u2212") + Math.abs(dj).toFixed(1) + " pt, " + (dc >= 0 ? "+" : "\\u2212") + "$" + Math.abs(dc).toFixed(0)) + "</span>";
  }
  const pointV = (ev) => {
    const r = carte.getBoundingClientRect();
    const x = (ev.clientX - r.left) / r.width * CW, y = (ev.clientY - r.top) / r.height * CH;
    let best = null, d0 = 1e9;
    for (const p of frontiere) { const d = Math.hypot(xl(p.cout) - x, yl(p.just) - y); if (d < d0) { d0 = d; best = p; } }
    return d0 < 24 ? best : null;
  };
  let tireV = false;
  carte.addEventListener("pointerdown", (ev) => {
    const r = carte.getBoundingClientRect();
    const x = (ev.clientX - r.left) / r.width * CW;
    if (Math.abs(x - xl(budgetDe())) < 12 || ev.target.classList.contains("ligne-poignee")) { tireV = true; try { carte.setPointerCapture(ev.pointerId); } catch (e) {} ev.preventDefault(); }
  });
  carte.addEventListener("pointermove", (ev) => {
    if (tireV) {
      const r = carte.getBoundingClientRect();
      const x = (ev.clientX - r.left) / r.width * CW;
      const v = Math.min(5, Math.max(0, (x - CL) / (CW - CL - CR) * 5));
      curseur.value = v.toFixed(2); curseur.dispatchEvent(new Event("input")); return;
    }
    const p = pointV(ev);
    if (p !== viseV) { viseV = p; dessinerV(); peindrePanneauV(); }
  });
  carte.addEventListener("pointerup", () => { tireV = false; });
  carte.addEventListener("pointerleave", () => { if (!tireV) { viseV = null; dessinerV(); peindrePanneauV(); } });
  carte.addEventListener("click", (ev) => { if (tireV) return; const p = pointV(ev); if (p) { routage = { ...p.r }; peindre(); } });
'''

JS_ONYX = '''
  /* THE LIVE CHART OF THE ONYX : the seals on the clock, the rhythm line you drag (a what-if). */
  const carte = $("#carte");
  const CW = 900, CH = 300, CL = 100, CR = 40, CT = 30, CB = 34, XMAX = 180;
  const noms = Object.keys(D.questions).filter((q) => D.questions[q].present);
  const HR = (CH - CT - CB) / Math.max(1, noms.length);
  const xd = (d) => CL + Math.min(d, XMAX) / XMAX * (CW - CL - CR);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  let rythme = D.reglages.rythmeJours, viseQ = null;
  const frais = (q) => D.questions[q].joursDepuis <= rythme;
  function dessinerO() {
    let h = '<rect class="zone-tenue" x="' + CL + '" y="' + CT + '" width="' + (xd(rythme) - CL).toFixed(0) + '" height="' + (CH - CT - CB) + '"/>';
    for (let k = 0; k <= XMAX; k += 30) h += '<text class="abscisse" x="' + xd(k).toFixed(0) + '" y="' + (CH - 8) + '">' + k + ' d</text><line class="rythme" x1="' + xd(k).toFixed(0) + '" x2="' + xd(k).toFixed(0) + '" y1="' + CT + '" y2="' + (CH - CB) + '"/>';
    noms.forEach((q, i) => {
      const y = CT + (i + .5) * HR, d = D.questions[q].joursDepuis;
      h += '<text class="nomq' + (q === viseQ ? " axe" : "") + '" x="0" y="' + (y + 4).toFixed(0) + '">' + esc(q) + '</text><line class="piste" x1="' + CL + '" x2="' + (CW - CR) + '" y1="' + y.toFixed(0) + '" y2="' + y.toFixed(0) + '"/>';
      h += '<g class="pierre ' + (frais(q) ? "tenu" : "pas") + (q === viseQ ? " vise" : "") + '"><circle cx="' + xd(d).toFixed(0) + '" cy="' + y.toFixed(0) + '" r="7"/><text x="' + xd(d).toFixed(0) + '" y="' + (y - 13).toFixed(0) + '">' + d + ' d \\u00b7 ' + esc(D.questions[q].etat) + '</text></g>';
    });
    const xs = xd(rythme);
    h += '<rect class="ligne-prise" x="' + (xs - 9).toFixed(0) + '" y="' + CT + '" width="18" height="' + (CH - CT - CB) + '"/>'
       + '<line class="ligne-l" x1="' + xs.toFixed(0) + '" x2="' + xs.toFixed(0) + '" y1="' + CT + '" y2="' + (CH - CB) + '"/>'
       + '<rect class="ligne-poignee" x="' + (xs - 7).toFixed(0) + '" y="' + (CT - 8) + '" width="14" height="14" rx="3"/>'
       + '<text class="ligne-t" x="' + xs.toFixed(0) + '" y="' + (CT - 12) + '">' + (rythme === D.reglages.rythmeJours ? "declared rhythm " + rythme + " days" : "if the rhythm were " + rythme + " days (declared: " + D.reglages.rythmeJours + ")") + '</text>';
    carte.innerHTML = h;
  }
  function peindrePanneauO() {
    if (!viseQ) { $("#pan-nom").textContent = "hover a stone"; $("#pan-g1").textContent = ""; $("#pan-l1").textContent = ""; $("#pan-verdicts").innerHTML = "<b>" + noms.filter(frais).length + "</b> of " + noms.length + " fresh within " + rythme + " days" + (rythme === D.reglages.rythmeJours ? "" : " (what-if : the sealed verdicts below keep the declared rhythm)"); return; }
    const d = D.questions[viseQ];
    $("#pan-nom").innerHTML = esc(viseQ) + " <small>" + esc(d.etat) + "</small>";
    $("#pan-g1").innerHTML = d.joursDepuis + "<small> days</small>";
    $("#pan-l1").textContent = "since its record was measured \\u00b7 seal " + String(d.sceau).slice(0, 8) + "\\u2026 \\u00b7 " + String(d.fichier).slice(0, 36);
    $("#pan-verdicts").innerHTML = (d.verdicts || []).map((v) => esc(v.controle) + " <b class=\\"" + (v.tenu ? "tenu" : "pas") + "\\">" + (v.tenu ? "held" : "not held") + "</b>").join("<br>")
      + "<br><span class=\\"" + (frais(viseQ) ? "tenu" : "pas") + "\\">" + (frais(viseQ) ? "fresh within " + rythme + " days" : "would fall out of a " + rythme + "-day rhythm") + "</span>";
  }
  function suivantesO() {
    const lignes = [];
    for (const [q, d] of Object.entries(D.questions)) {
      if (!d.present) { lignes.push("<b>" + esc(q) + "</b>: no public record yet \\u00b7 nothing judged"); continue; }
      const tenu = Object.fromEntries((d.verdicts || []).map((v) => [v.controle, v.tenu]));
      const suivant = ORDRE.find((c) => !(c in tenu) || !tenu[c]);
      const jours = typeof d.joursDepuis === "number" ? " \\u00b7 measured " + d.joursDepuis + " day(s) ago" : "";
      const echeance = typeof d.joursDepuis === "number" ? (d.joursDepuis <= rythme ? " \\u00b7 due in " + (rythme - d.joursDepuis) + " day(s)" : " \\u00b7 <b>past a " + rythme + "-day rhythm</b>") : "";
      if (suivant === undefined) lignes.push("<b>" + esc(q) + "</b>: every control held" + jours + echeance);
      else { const v = verdictDe(q, suivant); lignes.push("<b>" + esc(q) + "</b>: state reached <b>" + esc(d.etat) + "</b>" + jours + " \\u00b7 next, <b>" + esc(suivant) + "</b>: " + (v ? esc(v.detail) : "not judged by the record")); }
    }
    $("#g-suivant").innerHTML = lignes.join("<br>") + (rythme === D.reglages.rythmeJours ? "" : "<br><span class=\\"tm-l\\">what-if at " + rythme + " days ; the dossier's declared rhythm is " + D.reglages.rythmeJours + "</span>");
  }
  const pierreDe = (ev) => {
    const r = carte.getBoundingClientRect();
    const x = (ev.clientX - r.left) / r.width * CW, y = (ev.clientY - r.top) / r.height * CH;
    let best = null, d0 = 1e9;
    noms.forEach((q, i) => { const d = Math.hypot(xd(D.questions[q].joursDepuis) - x, CT + (i + .5) * HR - y); if (d < d0) { d0 = d; best = q; } });
    return d0 < 22 ? best : null;
  };
  let tireO = false;
  carte.addEventListener("pointerdown", (ev) => {
    const r = carte.getBoundingClientRect();
    const x = (ev.clientX - r.left) / r.width * CW;
    if (Math.abs(x - xd(rythme)) < 12 || ev.target.classList.contains("ligne-poignee")) { tireO = true; try { carte.setPointerCapture(ev.pointerId); } catch (e) {} ev.preventDefault(); }
  });
  carte.addEventListener("pointermove", (ev) => {
    if (tireO) {
      const r = carte.getBoundingClientRect();
      const x = (ev.clientX - r.left) / r.width * CW;
      rythme = Math.round(Math.min(XMAX, Math.max(1, (x - CL) / (CW - CL - CR) * XMAX)));
      dessinerO(); peindrePanneauO(); suivantesO(); return;
    }
    const q = pierreDe(ev);
    if (q !== viseQ) { viseQ = q; dessinerO(); peindrePanneauO(); }
  });
  carte.addEventListener("pointerup", () => { tireO = false; });
  carte.addEventListener("pointerleave", () => { if (!tireO) { viseQ = null; dessinerO(); peindrePanneauO(); } });
  carte.addEventListener("dblclick", () => { rythme = D.reglages.rythmeJours; dessinerO(); peindrePanneauO(); suivantesO(); });
  carte.addEventListener("click", (ev) => { if (tireO) return; const q = pierreDe(ev); if (!q) return; const cel = cells.find((x) => x.dataset.q === q && x.dataset.c === "fresh") || cells.find((x) => x.dataset.q === q); if (cel) lire(cel); });
  dessinerO(); peindrePanneauO(); suivantesO();
'''
