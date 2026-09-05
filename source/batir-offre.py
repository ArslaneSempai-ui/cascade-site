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
SCEAU = "1151f5a1cfaae0c0"
DEPOT_URL = "https://github.com/ArslaneSempai-ui/cascade-routing"

CSS = '''
  :root{--papier:#dbd7c5;--papier-haut:#e2ddcb;--papier-bas:#cdccb9;--encre:#1b1d18;
    --demi:#4a4739;--pale:#55523f;--filet:#9d9a83;
    --nuit-a:#1b3229;--nuit-b:#14251e;--nuit-c:#0e1a15;--sur-vert:#e4ecdf;--sur-vert-pale:#a9bdaf;
    --vert-titre:#23543f;--vert-vif:#57b184;--vert-clair:#a5f7cb;
    --texte:"Literata",Georgia,serif;--mono:"Roboto Mono",ui-monospace,Menlo,monospace;
    --sans:ui-sans-serif,-apple-system,"Helvetica Neue",sans-serif;
    --montee:cubic-bezier(.16,.84,.32,1)}
  *{box-sizing:border-box;margin:0}
  html{scroll-behavior:smooth;caret-color:var(--vert-vif);
    scrollbar-color:var(--vert-titre) var(--nuit-c)}
  @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
  body{background:var(--nuit-b);color:var(--sur-vert);font-family:var(--texte);line-height:1.6}
  ::selection{background:var(--vert-vif);color:var(--nuit-c)}
  a{text-underline-offset:4px;color:inherit}
  .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
  :focus-visible{outline:3px solid var(--vert-vif);outline-offset:3px;border-radius:2px}
  .colonne{max-width:1180px;margin:0 auto;padding:0 48px}

  .barre{position:absolute;inset:0 0 auto 0;z-index:40;display:flex;align-items:center;gap:28px;
    padding:14px 32px}
  .marque{font-weight:700;font-size:19px;letter-spacing:.01em;text-decoration:none;color:var(--sur-vert)}
  .barre nav{display:flex;gap:16px;margin-left:auto}
  .barre nav a{font-size:14.5px;text-decoration:none;color:var(--sur-vert-pale);padding:13px 6px}
  .barre nav a:hover{color:var(--sur-vert);text-decoration:underline;
    text-decoration-color:var(--vert-vif);text-decoration-thickness:1.5px}
  .barre nav a[aria-current]{color:var(--sur-vert)}
  .sceau{font-family:var(--mono);font-size:11px;color:var(--sur-vert-pale);letter-spacing:.04em}

  .tete{padding:150px 0 20px;
    background:radial-gradient(120% 100% at 50% -20%,#0f231b,var(--nuit-b) 70%)}
  .h1{font-size:clamp(38px,5vw,66px);font-weight:600;letter-spacing:-.02em;line-height:1.04;
    text-wrap:balance}
  .lede{font-size:clamp(15px,1.3vw,18.5px);color:var(--sur-vert-pale);max-width:72ch;
    line-height:1.65;margin-top:18px;text-wrap:balance}
  .lede b{color:var(--sur-vert)}

  /* ── les trois colonnes aux filets ── */
  .cols{display:grid;grid-template-columns:1fr 1fr 1fr;margin:54px 0 10px}
  .col{padding:8px 34px 10px;border-left:1px solid color-mix(in srgb,var(--sur-vert-pale) 18%,transparent)}
  .col:first-child{border-left:0;padding-left:0}
  .c-t{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
    color:var(--sur-vert-pale)}
  .c-prix{font-weight:600;font-size:clamp(40px,4.4vw,64px);letter-spacing:-.02em;line-height:1.05;
    margin:14px 0 4px;font-variant-numeric:lining-nums tabular-nums}
  .c-prix small{font-size:.32em;font-weight:400;color:var(--sur-vert-pale);letter-spacing:0;white-space:nowrap}
  .col.haute .c-prix{color:var(--vert-clair);
    text-shadow:0 0 26px color-mix(in srgb,var(--vert-vif) 40%,transparent)}
  .c-qui{font-size:14px;color:var(--sur-vert-pale);min-height:3em;line-height:1.55;
    border-bottom:1px solid color-mix(in srgb,var(--sur-vert-pale) 18%,transparent);
    padding-bottom:16px;margin-bottom:16px}
  .c-plus{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
    color:color-mix(in srgb,var(--sur-vert-pale) 70%,transparent);margin-bottom:8px}
  .c-liste{list-style:none;padding:0;display:flex;flex-direction:column;gap:9px;
    font-size:13.5px;color:var(--sur-vert-pale);min-height:196px}
  .c-liste li{padding-left:22px;position:relative;line-height:1.5}
  .c-liste li::before{content:"";position:absolute;left:0;top:.5em;width:12px;height:7px;
    border-left:2px solid var(--vert-vif);border-bottom:2px solid var(--vert-vif);
    transform:rotate(-45deg)}
  .c-liste b{color:var(--sur-vert)}
  .cta{display:inline-flex;align-items:baseline;gap:12px;text-decoration:none;margin-top:22px;
    font-family:var(--texte);font-size:16px;font-weight:600;padding:13px 24px;border-radius:10px;
    color:var(--vert-clair);border:1px solid color-mix(in srgb,var(--vert-vif) 45%,transparent);
    transition:background .2s,color .2s,border-color .2s,box-shadow .2s}
  .cta .fl{font-family:var(--sans);transition:transform .2s var(--montee)}
  .cta:hover{background:var(--vert-vif);color:var(--nuit-c);border-color:var(--vert-vif)}
  .cta:hover .fl{transform:translateX(4px)}
  .col.haute .cta{background:var(--vert-vif);color:var(--nuit-c);border-color:var(--vert-vif)}
  .col.haute .cta:hover{box-shadow:0 14px 36px color-mix(in srgb,var(--vert-vif) 32%,transparent)}
  .c-fin{font-family:var(--mono);font-size:10.5px;letter-spacing:.05em;
    color:color-mix(in srgb,var(--sur-vert-pale) 70%,transparent);margin-top:14px;line-height:1.7}

  /* ── le chemin d'achat ── */
  .chemin{padding:54px 0 30px}
  .h2{font-size:clamp(26px,2.8vw,38px);font-weight:600;letter-spacing:-.015em;
    line-height:1.1;text-wrap:balance;margin-bottom:22px}
  .pas{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
  .p-un{border-top:3px solid var(--vert-vif);padding-top:12px}
  .p-no{font-family:var(--mono);font-size:11px;letter-spacing:.12em;color:var(--vert-vif)}
  .p-t{display:block;font-size:18px;font-weight:600;margin:4px 0 6px}
  .p-d{font-size:13.5px;color:var(--sur-vert-pale);line-height:1.55}
  .p-d a{color:var(--vert-clair);font-weight:600}

  /* ── le refus, puis l'appel ── */
  .refus{padding:34px 0 80px}
  .refus-carte{border:1px solid color-mix(in srgb,var(--sur-vert-pale) 22%,transparent);
    border-radius:12px;padding:20px 24px;display:flex;gap:24px;align-items:center;flex-wrap:wrap}
  .refus-carte p{flex:1;min-width:320px;font-size:14.5px;color:var(--sur-vert-pale);line-height:1.6}
  .refus-carte b{color:var(--sur-vert)}

  .pied{background:var(--nuit-c);color:var(--sur-vert);padding:52px 0}
  .pied .colonne{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:baseline}
  .pied-p{font-size:clamp(17px,1.8vw,23px);font-weight:600}
  .pied-p em{font-style:italic;color:var(--vert-clair)}
  .pied .sceau{color:var(--sur-vert-pale)}

  @media (max-width:1080px){
    .colonne{padding:0 22px}
    .barre{padding:12px 18px;gap:14px}
    .barre nav{display:none}
    .tete{padding-top:100px}
    .cols{grid-template-columns:1fr}
    .col{border-left:0;padding:22px 0;
      border-top:1px solid color-mix(in srgb,var(--sur-vert-pale) 18%,transparent)}
    .col:first-child{border-top:0}
    .c-liste{min-height:0}
    .pas{grid-template-columns:1fr 1fr}
  }
  @media (prefers-reduced-motion:reduce){
    *{transition-duration:.01ms!important;animation-duration:.01ms!important}}
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
<header class="barre">
  <a class="marque" href="HERO.html">CASCADE</a>
  <nav aria-label="Site">
    <a href="INSTRUMENT.html">Instrument</a>
    <a href="ENGAGEMENT.html" aria-current="page">Pricing</a>
    <a href="ANNEXE-METHODE.html">Method</a>
    <a href="ANNEXE-SECURITE.html">Security</a>
    <a href="ANNEXE-QUESTIONS.html">Questions</a>
    <a href="CONTACT.html">Contact</a>
  </nav>
  <span class="sceau">seal {SCEAU} &#183; measured, then frozen</span>
</header>

<main>
<section class="tete"><div class="colonne">
  <h1 class="h1">What an engagement buys.</h1>
  <p class="lede"><b>Proof before commitment.</b><br>Test the instrument free on your own records.
    Run one sealed campaign when you are ready. Then license it for the year, when the results
    make the case.</p>
</div></section>

<section aria-label="The three steps"><div class="colonne">
  <div class="cols">
    <div class="col">
      <p class="c-t">the evaluation</p>
      <p class="c-prix">$0<small> &#183; 30 days</small></p>
      <p class="c-qui">For deciding. Your records, your machine, nothing to sign.</p>
      <ul class="c-liste">
        <li>The whole tool, <b>on your own records</b></li>
        <li>Counter starts at first use, not download</li>
        <li>Results stay internal, no production</li>
        <li>No document leaves your network</li>
      </ul>
      <a class="cta" href="{DEPOT_URL}">Clone and run <span class="fl" aria-hidden="true">&#8594;</span></a>
      <p class="c-fin">granted in the public licence itself</p>
    </div>
    <div class="col">
      <p class="c-t">the campaign</p>
      <p class="c-prix">$12,000<small> fixed</small></p>
      <p class="c-qui">For the file your reviewers will open. One campaign, one deliverable.</p>
      <p class="c-plus">everything in the evaluation, plus</p>
      <ul class="c-liste">
        <li><b>Which tier suffices</b>, field by field</li>
        <li>Intervals, refusals under twenty observations</li>
        <li>A <b>sealed, signed report</b> your audit team verifies without us</li>
        <li>We never access your data</li>
      </ul>
      <a class="cta" href="CONTACT.html">Start with a message <span class="fl" aria-hidden="true">&#8594;</span></a>
      <p class="c-fin">one campaign &#183; one sealed deliverable</p>
    </div>
    <div class="col haute">
      <p class="c-t">the licence</p>
      <p class="c-prix">$30,000<small> a year</small></p>
      <p class="c-qui">For running it as yours. Commercial use, updates included.</p>
      <p class="c-plus">everything in the campaign, plus</p>
      <ul class="c-liste">
        <li>Commercial use for your own business</li>
        <li>The <b>licensed component</b>, not published</li>
        <li>Updates included for every paid term</li>
        <li><b>Recertify</b> on fresh records, re-sealed, on the rhythm you declare</li>
        <li>One legal entity signs; affiliates named, not assumed</li>
      </ul>
      <a class="cta" href="CONTACT.html">Talk terms <span class="fl" aria-hidden="true">&#8594;</span></a>
      <p class="c-fin">30% on signature &#183; net 60 &#183; renewal capped at the lower of CPI&#8209;U and 5%</p>
    </div>
  </div>
</div></section>

<section class="chemin"><div class="colonne">
  <h2 class="h2">How buying works.</h2>
  <div class="pas">
    <div class="p-un"><span class="p-no">01</span><span class="p-t">Write</span>
      <p class="p-d"><a href="mailto:contact@cascade-routing.com">contact@cascade-routing.com</a>,
        or open an issue on the public repository. Name the figure you care about.</p></div>
    <div class="p-un"><span class="p-no">02</span><span class="p-t">Evaluate</span>
      <p class="p-d">Thirty days on your records, at your desk. Nothing to install on our side,
        because there is no our side.</p></div>
    <div class="p-un"><span class="p-no">03</span><span class="p-t">Sign</span>
      <p class="p-d">An engagement letter for the campaign, or the commercial licence for the year.
        The paper names what it does not certify.</p></div>
    <div class="p-un"><span class="p-no">04</span><span class="p-t">Wire</span>
      <p class="p-d">An invoice, settled by bank transfer. The licence takes 30% on signature,
        the balance net 60; the campaign is one fixed price.</p></div>
  </div>
</div></section>

<section class="refus"><div class="colonne">
  <div class="refus-carte">
    <p><b>What none of this certifies.</b> The report proves what was measured and, in its own
      words, nothing more; the burden stays on the measurement. External publication of engagement
      results is excluded from day one. The full terms are on
      <a href="ANNEXE-TERMS.html">the terms page</a>, in the same words the paper uses.</p>
    <a class="cta" href="CONTACT.html">Contact us <span class="fl" aria-hidden="true">&#8594;</span></a>
  </div>
</div></section>
</main>

<footer class="pied"><div class="colonne">
  <p class="pied-p">On your records, on your machine. <em>Nothing leaves the network.</em></p>
  <span class="sceau">seal {SCEAU} &#183; measured, then frozen</span>
</div></footer>
'''

assert "—" not in PAGE, "un cadratin s'est glissé dans la page"
(BASE / "ENGAGEMENT.html").write_text(PAGE, encoding="utf-8")
print(f"ENGAGEMENT.html {len(PAGE) / 1e3:.0f} ko")
