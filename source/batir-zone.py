#!/usr/bin/env python3
"""Six façons de traiter la zone sous la ligne verte, menu compris.

CE QU'ARSLANE A DEMANDÉ LE 29 AOÛT
  · « l'écriture sous le design 3d est mauvaise » ;
  · « pour les infos sous la ligne verte tu pourrais faire différents menus sur plusieurs
    maquettes pour qu'on puisse voir la différence ? »

CE QUI NE BOUGE PAS
L'en-tête, le titre sur toute la hauteur du vert, l'objet seul à droite, le pied et ses
six annexes. Seule la zone sous le vert change, menu compris : c'est la seule chose à
juger, donc la seule qui varie.

LA LÉGENDE DE L'OBJET, REFAITE
Elle était trois lignes de gris alignées à droite, en drapeau, flottant sous une ombre
sans rien pour la porter. Trois défauts, pas un : l'alignement à droite sur trois lignes
donne un bord gauche déchiqueté et l'œil n'a plus où commencer ; le bloc n'a ni filet ni
support, donc il flotte ; et il disait deux choses là où une légende en dit une.
Elle devient ce qu'elle aurait dû être depuis le début : la légende d'une figure de
rapport, « FIGURE 1, … », dans la MÊME petite capitale que « TABLE 1 » sous le tableau,
alignée à gauche, posée sur un filet. La page est un rapport ; ses figures se légendent
comme celles d'un rapport.

LES SIX DIRECTIONS, ET CE QUE CHACUNE APPORTE
  A la table étendue     chaque chiffre porte SA limite dans le tableau, en quatrième
                         colonne, au lieu d'une note qu'on lit après
  B le diptyque          les chiffres à gauche, ce qu'ils ne prouvent pas à droite, à
                         poids égal : c'est l'argument du produit, pas une réserve
  C le menu en colonne   les cinq constats sous l'objet, dans la zone aujourd'hui morte ;
                         le menu est à côté de ce qui reste, la lecture à côté de ce qui change
  D les cartes           chaque constat porte la question à laquelle il répond, donc on
                         choisit en sachant ce qu'on va lire
  E la phrase-chiffre    le tableau se replie, une seule phrase porte les deux taux :
                         l'écran assène, le détail est à un clic et non supprimé
  F la bande             trois chiffres en rangée, dans le registre de tableau de bord que
                         la banque connaît — mais avec l'intervalle DESSINÉ sous chacun,
                         qui est précisément ce qu'un vrai tableau de bord cache
"""
import importlib.util
import pathlib

BASE = pathlib.Path(__file__).parent

# On charge l'écran arrêté au lieu de le recopier : ce qui est validé ne doit exister
# qu'à un seul endroit, sinon les six maquettes dérivent de l'original sans qu'on le voie.
_spec = importlib.util.spec_from_file_location("bn", BASE / "batir-nav.py")
bn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bn)

X = bn.X
ECRANS = bn.ECRANS

# Ce que chaque constat demande. Aucun chiffre : les mesures des écrans 02 à 05 sont en
# cours de vérification dans le dépôt, et un chiffre non retrouvé ne s'affiche pas.
QUESTIONS = {
    "01": "Which rate do you act on?",
    "02": "Can a cheaper reader hold?",
    "03": "Is a blank worth more than a wrong value?",
    "04": "What did we refuse to publish?",
    "05": "What runs, and for how long?",
}

LEGENDE_TXT = ("Figure 1, one stack per reader and per field. The empty row is the human "
               "operator, never sampled field by field.")

ZONE_CSS = """
  /* ── LA LÉGENDE DE L'OBJET, REFAITE ──────────────────────────────────────────
     Alignée à gauche (trois lignes en drapeau à droite n'ont pas de bord où commencer),
     posée sur un filet qui la porte, et libellée comme la légende d'une figure de
     rapport, dans la même capitale que « TABLE 1 ». */
  .legende{display:block;margin:1.05rem 0 0 auto;max-width:34ch;text-align:left;
           border-top:1px solid var(--filet-clair);padding-top:.5rem;
           margin-right:calc(4vw + clamp(1.2rem,3.4vw,3.2rem));
           font:400 13px/1.5 var(--sans);color:var(--pale)}
  .legende .no{display:block;font:600 10.5px/1.3 var(--sans);letter-spacing:.12em;
               text-transform:uppercase;color:var(--demi);margin-bottom:.2rem}
  /* Variante C : la colonne de droite sert au menu, la légende repasse à gauche. */
  .zone-c .legende{display:none}
  .leg-gauche{margin:.15rem 0 0;max-width:52ch;font:400 12.5px/1.5 var(--sans);
              color:var(--pale)}
  .leg-gauche b{color:var(--demi);font-weight:600;letter-spacing:.1em;
                text-transform:uppercase;font-size:10.5px;margin-right:.45rem}
  /* D n'a plus de paragraphe et gagne cinq cartes : sa légende tient sur une ligne. */
  .zone-d .leg-gauche{margin-top:.1rem;font-size:12px}

  /* ── LE MENU. Socle commun aux six ; chaque variante le reprend à sa façon. ── */
  /* MESURÉ : .pied portait deja margin-top:auto. Deux marges automatiques dans la meme
     colonne se PARTAGENT l'espace libre — le menu flottait au milieu de la page avec un
     trou dessous. Le pied rend la sienne ; le menu prend tout et le pied le suit. */
  .menu{position:relative;z-index:5;margin-top:auto}
  .zone-a .pied,.zone-b .pied,.zone-d .pied,.zone-e .pied,.zone-f .pied{margin-top:0}
  .menu .lien{all:unset;cursor:pointer;display:block}
  .menu .lien:focus-visible{outline:none;
    box-shadow:0 0 0 2px var(--papier-haut),0 0 0 4.5px var(--nuit-b)}
  .menu .no{font:500 12px/1 var(--mono);letter-spacing:.05em;color:var(--filet)}
  .menu .ti{font:400 15px/1.35 var(--texte);color:var(--demi)}
  .menu [aria-current="true"] .no{color:var(--vert-titre)}
  .menu [aria-current="true"] .ti{color:var(--encre);font-weight:600}

  /* ── A · LA TABLE ÉTENDUE ────────────────────────────────────────────────────
     Une quatrième colonne : ce que le chiffre NE dit pas, sur sa propre ligne. La
     limite cesse d'être une note qu'on lit après le tableau. */
  /* MESURÉ : en pleine largeur, la quatrieme colonne passait sous l'objet et sous la
     legende. Le tableau s'arrete au bord gauche de l'objet : 54rem, mesure a 1440. */
  .zone-a .bas{max-width:none}
  /* MESURÉ DEUX FOIS : « 54rem » etait juste a 1440 et faux partout ailleurs, parce que
     le bord gauche de l'objet suit la fenetre (100vw + 4vw - min(40vw,600px)) et pas une
     constante. La largeur du tableau se calcule maintenant AVEC les memes variables que
     l'objet : elle ne peut plus le croiser. */
  .zone-a .tab{max-width:calc(104vw - min(40vw,600px)
               - 2 * clamp(1.2rem,3.4vw,3.2rem) - 1.5rem)}
  .zone-a .tab td{padding-top:.28rem;padding-bottom:.28rem}
  .zone-a .tab td.lim{font:400 12.5px/1.4 var(--sans);color:var(--pale);text-align:left;
                      white-space:normal;width:15rem;padding-left:1.3rem;
                      font-variant-numeric:normal}
  .zone-a .tab thead th.lim{text-align:left;padding-left:1.4rem}
  .zone-a .agir{margin-top:.2rem}
  .zone-a .menu{display:grid;grid-template-columns:repeat(5,1fr);
                border-top:1px solid var(--filet-clair);margin-bottom:.5rem}
  .zone-a .menu .lien{display:flex;gap:.55rem;align-items:baseline;
                      padding:.62rem .8rem .58rem 0;border-top:2.5px solid transparent;
                      margin-top:-1.5px}
  .zone-a .menu [aria-current="true"]{border-top-color:var(--vert-titre)}
  .zone-a .menu .lien:hover{border-top-color:var(--filet)}

  /* ── B · LE DIPTYQUE ─────────────────────────────────────────────────────────
     Les deux taux à gauche, en grand ; ce qu'ils ne prouvent pas à droite, dans un
     encadré de même poids. Chez Cascade la réserve EST le produit. */
  /* MESURÉ, DEUX FAUTES. Le placement automatique avait mis la reserve a GAUCHE et les
     deux chiffres a droite, sous l'objet. Et la colonne de droite, alignee en haut,
     tombait de toute facon sur l'objet. Les colonnes sont maintenant nommees, et la
     reserve s'aligne sur le BAS : elle passe donc sous l'objet par construction, dans la
     zone qui etait morte. */
  /* MESURÉ TROIS FOIS. Nommer les colonnes a bien remis la reserve a droite, mais
     « aligne sur le bas de la grille » ne suffit pas : la hauteur de la grille vient des
     chiffres, pas de l'objet, et la reserve remontait de 18 px sur lui a TOUTES les
     tailles. Elle s'accroche donc a l'objet lui-meme, comme le menu de C. */
  .zone-b .bas{max-width:min(56%,44rem)}
  .zone-b .legende{display:none}
  .zone-b .paire{display:flex;gap:clamp(1.4rem,3.5vw,3.2rem);flex-wrap:wrap}
  .zone-b .chif{min-width:11rem}
  .zone-b .chif .v{display:block;font:600 clamp(2.1rem,3.4vw,3rem)/1 var(--texte);
                   letter-spacing:-.02em;font-variant-numeric:tabular-nums}
  .zone-b .chif.deux .v{color:var(--vert-titre)}
  .zone-b .chif .q{display:block;margin:.3rem 0 .35rem;font:400 14.5px/1.4 var(--sans);
                   color:var(--demi);max-width:22ch}
  .zone-b .chif .mou{max-width:15rem}
  .zone-b .note{position:absolute;z-index:5;
                right:clamp(1.2rem,3.4vw,3.2rem);width:min(36%,24rem);
                top:calc(clamp(4.4rem,9vh,7rem) + 0.81 * min(40vw,600px) + 1.2rem);
                border-left:2px solid var(--vert-titre);padding:.15rem 0 .15rem .9rem}
  .zone-b .note h2{margin:0 0 .35rem;font:600 10.5px/1.3 var(--sans);letter-spacing:.12em;
                   text-transform:uppercase;color:var(--pale)}
  .zone-b .note p{margin:0 0 .5rem;font:400 14.5px/1.5 var(--sans);color:var(--demi)}
  .zone-b .note p:last-child{margin-bottom:0}
  .zone-b .note b{color:var(--encre);font-weight:600}

  .zone-b .menu{display:flex;justify-content:flex-end;gap:clamp(.8rem,2vw,1.9rem);
                flex-wrap:wrap;border-top:1px solid var(--filet-clair);
                padding-top:.6rem;margin-bottom:.45rem}
  .zone-b .menu .lien{display:flex;gap:.5rem;align-items:baseline;padding:.25rem 0}
  .zone-b .menu [aria-current="true"] .ti{box-shadow:0 1.5px 0 var(--vert-titre)}
  .zone-b .menu .lien:hover .ti{box-shadow:0 1.5px 0 var(--filet)}

  /* ── C · LE MENU EN COLONNE ──────────────────────────────────────────────────
     Les cinq constats descendent dans la colonne de droite, sous l'objet, là où il n'y
     avait rien. Ils s'alignent sur le BAS de la zone : c'est la seule façon de garantir
     qu'ils passent sous l'objet sans écrire sa hauteur en dur quelque part. */
  /* MESURÉ : aligne sur le bas d'une grille, le menu remontait sur l'objet des que la
     fenetre baissait — la hauteur de la grille vient du tableau, pas de l'objet. Il
     s'accroche donc a l'OBJET lui-meme, avec les memes variables que lui : haut de
     l'objet + sa hauteur (le rendu fait 0,81 fois sa largeur, mesure). C'est le seul
     ancrage qui ne se demente pas quand la fenetre change. */
  .zone-c .bas{max-width:min(56%,44rem)}
  .zone-c .gauche{display:flex;flex-direction:column;gap:clamp(.4rem,1.1vh,.75rem);
                  align-items:flex-start}
  .zone-c .leg-gauche{margin-top:0;font-size:12px}
  .zone-c .sous{font-size:15.5px}
  .zone-c .menu .ti{font-size:14.5px}
  .zone-c .tab td{padding-top:.28rem;padding-bottom:.28rem}
  .zone-c .menu{position:absolute;z-index:5;margin:0;
                right:clamp(1.2rem,3.4vw,3.2rem);width:min(36%,25rem);
                top:calc(clamp(4.4rem,9vh,7rem) + 0.81 * min(40vw,600px) + 1.2rem);
                display:flex;flex-direction:column;
                border-top:1px solid var(--filet-clair)}
  .zone-c .menu .lien{display:flex;gap:.7rem;align-items:baseline;
                      padding:.42rem .3rem .42rem .7rem;
                      border-bottom:1px solid var(--filet-clair);
                      border-left:2px solid transparent;margin-left:-.7rem}
  .zone-c .menu .lien:last-child{border-bottom:none}
  .zone-c .menu [aria-current="true"]{border-left-color:var(--vert-titre);
                                      background:rgba(35,84,63,.07)}
  .zone-c .menu .lien:hover{border-left-color:var(--filet)}

  /* ── D · LES CARTES ──────────────────────────────────────────────────────────
     Chaque constat porte la question à laquelle il répond. On choisit en sachant ce
     qu'on va lire, au lieu de cliquer un titre. */
  /* MESURÉ : vingt pixels de trop, et le pied s'en trouvait coupé. Ils sont rendus par
     les rangées du tableau et l'écart sous les cartes, pas par le texte lu. */
  .zone-d .menu{display:grid;grid-template-columns:repeat(5,1fr);
                gap:clamp(.4rem,1vw,.75rem);margin-bottom:.3rem}
  .zone-d .tab td{padding-top:.24rem;padding-bottom:.24rem}
  .zone-d .bas{gap:clamp(.4rem,1.1vh,.7rem)}
  .zone-d .menu .lien{border:1px solid var(--filet-clair);padding:.5rem .6rem .55rem;
                      background:linear-gradient(168deg,rgba(255,252,244,.55),
                                 rgba(255,252,244,.14));
                      transition:border-color .16s ease,transform .16s var(--montee),
                                 box-shadow .16s ease}
  .zone-d .menu .lien:hover{border-color:var(--filet);transform:translateY(-1px);
                            box-shadow:0 4px 12px rgba(20,37,30,.12)}
  .zone-d .menu .ti{display:block;margin:.1rem 0 .2rem;font-size:14px;line-height:1.2}
  .zone-d .menu .qu{display:block;font:400 12px/1.35 var(--sans);color:var(--pale);
                    display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
                    overflow:hidden}
  /* MESURÉ, ET LA PREMIERE CORRECTION ETAIT LA MAUVAISE : brider la largeur du menu a
     bien ecarte la legende, mais cinq cartes de 145 px ne tiennent plus leur texte et
     l'ecran a debordE de 65 px au lieu de 49. Les cartes reprennent donc la pleine
     largeur — elles vivent tout en bas, la ou l'objet n'est plus — et c'est la PROSE
     qui part : les cinq questions du menu disent deja ce que le paragraphe repetait.
     La variante D est celle ou le menu porte l'information, l'ecran au-dessus peut
     donc en porter moins. */
  .zone-d .menu [aria-current="true"]{border-color:var(--vert-titre);
    box-shadow:inset 0 2.5px 0 var(--vert-titre)}

  /* ── E · LA PHRASE-CHIFFRE ───────────────────────────────────────────────────
     Le tableau se replie. Une phrase porte les deux taux en grand, et le détail reste
     accessible : replié n'est pas supprimé. Le groupe de boutons est à angles vifs,
     comme tout le reste de la page — un groupe arrondi jurerait. */
  .zone-e .phrase{margin:0;max-width:38ch;font:400 clamp(1.3rem,2.35vw,2.05rem)/1.32
                  var(--texte);color:var(--encre);letter-spacing:-.008em}
  .zone-e .phrase b{font-weight:600;font-variant-numeric:tabular-nums}
  .zone-e .phrase .un{color:var(--encre)} .zone-e .phrase .de{color:var(--vert-titre)}
  .zone-e details{margin:0;max-width:46rem}
  .zone-e summary{cursor:pointer;list-style:none;display:inline-flex;gap:.5rem;
                  align-items:center;padding:.35rem .1rem;
                  font:600 11px/1.4 var(--sans);letter-spacing:.12em;
                  text-transform:uppercase;color:var(--pale);
                  border-bottom:1px solid var(--filet-clair)}
  .zone-e summary::-webkit-details-marker{display:none}
  .zone-e summary:hover{color:var(--encre);border-bottom-color:var(--filet)}
  .zone-e summary .cr{font:400 13px/1 var(--sans);transition:transform .2s var(--montee)}
  .zone-e details[open] summary .cr{transform:rotate(90deg)}
  .zone-e details .tab{margin-top:.7rem}
  .zone-e .menu{display:flex;border:1px solid var(--filet);align-self:flex-start;
                margin-bottom:.5rem;background:rgba(255,252,244,.45)}
  .zone-e .menu .lien{display:flex;gap:.5rem;align-items:baseline;padding:.55rem .95rem;
                      border-right:1px solid var(--filet-clair)}
  .zone-e .menu .lien:last-child{border-right:none}
  .zone-e .menu .lien:hover{background:rgba(255,252,244,.7)}
  .zone-e .menu [aria-current="true"]{background:var(--nuit-a)}
  .zone-e .menu [aria-current="true"] .no{color:var(--vert-vif)}
  .zone-e .menu [aria-current="true"] .ti{color:var(--sur-vert)}

  /* ── F · LA BANDE ────────────────────────────────────────────────────────────
     Le registre du tableau de bord, que la banque lit tous les jours — et sous chaque
     chiffre, l'intervalle dessiné, qui est exactement ce qu'un tableau de bord ne
     montre jamais. L'écran se sert de la forme qu'il critique. */
  .zone-f .bas{max-width:none}
  .zone-f .bande{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
                 gap:0;border-top:1.6px solid var(--encre);
                 border-bottom:1px solid var(--filet-clair);max-width:52rem}
  .zone-f .cel{padding:.65rem 1.1rem .7rem 0;border-right:1px solid var(--filet-clair)}
  .zone-f .cel:last-child{border-right:none;padding-right:0}
  .zone-f .cel:not(:first-child){padding-left:1.1rem}
  .zone-f .cel .et{display:block;font:600 10.5px/1.3 var(--sans);letter-spacing:.1em;
                   text-transform:uppercase;color:var(--pale)}
  .zone-f .cel .v{display:block;margin:.2rem 0 .1rem;
                  font:600 clamp(1.6rem,2.5vw,2.15rem)/1 var(--texte);
                  font-variant-numeric:tabular-nums;letter-spacing:-.02em}
  .zone-f .cel.cle .v{color:var(--vert-titre)}
  .zone-f .cel .q{display:block;font:400 12.5px/1.4 var(--sans);color:var(--pale);
                  max-width:26ch;margin-bottom:.15rem}
  .zone-f .menu{display:flex;align-items:center;gap:0;margin-bottom:.5rem;
                border-top:1px solid var(--filet-clair);padding-top:.75rem}
  .zone-f .menu .lien{display:flex;gap:.55rem;align-items:baseline;padding:.2rem .9rem;
                      position:relative}
  .zone-f .menu .lien:first-child{padding-left:0}
  /* Le filet continu passait DERRIERE les mots et se lisait comme un barre. Les pastilles
     suffisent a dire l'ordre ; le filet du haut suffit a dire que c'est une rangee. */
  .zone-f .menu .pt{display:inline-block;width:7px;height:7px;
                    background:var(--filet-clair);margin-right:.15rem}
  .zone-f .menu [aria-current="true"] .pt{background:var(--vert-titre)}
  .zone-f .menu .lien:hover .pt{background:var(--filet)}

  /* MESURÉ : ancré sous l'objet, le menu de C descend avec lui — et à 1440x760 il
     rejoignait le pied. Ses cinq lignes se resserrent quand la fenêtre est basse. */
  @media (max-height:840px){
    .zone-c .menu .lien{padding:.3rem .3rem .3rem .7rem}
    .zone-c .menu .ti{font-size:14px}
    .zone-b .note p{font-size:13.5px;line-height:1.45}
  }

  /* MESURÉ : a 1152 la place restante entre la marge et l'objet tombe a 635 px. Quatre
     colonnes s'y empilent sur trois lignes chacune et l'ecran deborde de 118 px. La
     quatrieme colonne — celle qui fait tout l'interet de A — se retire sous 1280 : la
     variante montre ce qu'elle a a montrer au-dessus, et ne ment pas en dessous. */
  @media (max-width:1280px){
    .zone-a .tab td.lim,.zone-a .tab thead th.lim{display:none}
  }
  /* MESURÉ : a 1152 les cinq cartes de D montent a 52 px de trop et le menu sort de
     l'ecran. La question se retire ; le numero et le titre restent. La variante montre
     ce qu'elle a a montrer au-dessus de 1200, et se tait proprement en dessous. */
  @media (max-width:1200px){
    .zone-d .menu .qu{display:none}
  }

  @media (max-width:1080px){
    .legende,.leg-gauche{display:none}
    .zone-a .tab td.lim,.zone-a .tab thead th.lim{display:none}
    .zone-b .bas,.zone-c .bas{grid-template-columns:1fr}
    .zone-b .note{grid-row:auto;margin-top:.8rem}
    .zone-c .menu{align-self:stretch;margin-top:1rem}
    .zone-d .menu,.zone-a .menu{grid-template-columns:1fr 1fr}
    .zone-e .menu{flex-wrap:wrap}
    .zone-f .bande{grid-template-columns:1fr}
    .zone-f .cel{border-right:none;border-bottom:1px solid var(--filet-clair);
                 padding-left:0}
  }
"""


def menu_html(variante, courant="01"):
    """Le menu des cinq constats. Ce sont des LIENS, pas des boutons : un constat a une
    adresse, il s'envoie par courriel et s'ouvre dans un onglet. La forme change d'une
    variante à l'autre, la nature non."""
    items = []
    for no, titre in ECRANS:
        cur = ' aria-current="true"' if no == courant else ""
        if variante == "d":
            items.append(
                f'<a class="lien" href="#{no}"{cur}><span class="no">{no}</span>'
                f'<span class="ti">{titre}</span>'
                f'<span class="qu">{QUESTIONS[no]}</span></a>')
        elif variante == "f":
            items.append(
                f'<a class="lien" href="#{no}"{cur}>'
                f'<span class="pt" aria-hidden="true"></span>'
                f'<span class="no">{no}</span><span class="ti">{titre}</span></a>')
        else:
            items.append(
                f'<a class="lien" href="#{no}"{cur}><span class="no">{no}</span>'
                f'<span class="ti">{titre}</span></a>')
    return ('<nav class="menu" aria-label="Findings">' + "".join(items) + "</nav>")


def moustache(kind):
    """Les mêmes moustaches que le tableau, à la même échelle. Une échelle par figure
    rendrait la comparaison fausse tout en la rendant jolie."""
    if kind == "vide":
        return (f'<svg class="mou" viewBox="0 0 210 26" role="img" '
                f'aria-label="No interval: a mean of rates is not a proportion.">'
                f'<line class="ax" x1="6" y1="13" x2="204" y2="13"></line>'
                f'<text class="vide" x="105" y="17" text-anchor="middle">no interval</text>'
                f'<circle class="pt" cx="{X(94.4)}" cy="13" r="3.4"></circle></svg>')
    return (f'<svg class="mou" viewBox="0 0 210 26" role="img" '
            f'aria-label="Wilson 95% interval from 68.3 to 83.3 percent.">'
            f'<line class="ax" x1="6" y1="13" x2="204" y2="13"></line>'
            f'<path class="br" d="M{X(68.3)} 6 L{X(68.3)} 20 M{X(68.3)} 13 L{X(83.3)} 13 '
            f'M{X(83.3)} 6 L{X(83.3)} 20"></path>'
            f'<circle class="pt" cx="{X(76.7)}" cy="13" r="3.4"></circle>'
            f'<text class="g" x="{X(68.3)}" y="25" text-anchor="middle">68.3</text>'
            f'<text class="g" x="{X(83.3)}" y="25" text-anchor="middle">83.3</text></svg>')


# ── A · la table gagne une colonne « ce que ce chiffre ne dit pas » ───────────
TAB_A = f"""<table class="tab">
        <caption>Table 1, the two rates over the same 120 case files</caption>
        <thead><tr><th>Figure</th><th>95% interval</th><th>Value</th>
          <th class="lim">What it cannot tell you</th></tr></thead>
        <tbody>
          <tr aria-selected="false">
            <th><button class="sel" type="button">Mean of five field rates
              <small>not a proportion, so none can be computed</small></button></th>
            <td class="f">{moustache("vide")}</td>
            <td>94.4%</td>
            <td class="lim">Whether one file was right end to end.</td></tr>
          <tr aria-selected="false">
            <th><button class="sel" type="button">Per-file rate, 92 of 120
              <small>all five fields right on the same file</small></button></th>
            <td class="f">{moustache("wilson")}</td>
            <td>76.7%</td>
            <td class="lim">Where inside 68.3 and 83.3 the true rate sits.</td></tr>
          <tr class="cle" aria-selected="false">
            <th><button class="sel" type="button">Difference
              <small>over the same 120 case files</small></button></th>
            <td class="f"><svg class="mou" viewBox="0 0 210 26" role="img"
                 aria-label="A gap of 17.7 points between the two rates.">
              <path class="br" d="M{X(76.7)} 8 L{X(76.7)} 18 M{X(76.7)} 13 L{X(94.4)} 13
                M{X(94.4)} 8 L{X(94.4)} 18"></path>
              <text class="g" x="{(X(76.7) + X(94.4)) / 2:.1f}" y="25"
                text-anchor="middle">17.7 points</text></svg></td>
            <td>17.7</td>
            <td class="lim">Which one to act on. That is a decision.</td></tr>
        </tbody></table>"""

BAS_A = f"""<div class="bas">
    <p class="sous">{bn.SOUS}</p>
    {TAB_A}
    {bn.AGIR}
  </div>"""

# ── B · le diptyque : les chiffres, et ce qu'ils ne prouvent pas ──────────────
BAS_B = f"""<div class="bas">
    <div class="paire">
      <div class="chif"><span class="v">94.4%</span>
        <span class="q">Mean of five field rates</span>
        {moustache("vide")}</div>
      <div class="chif deux"><span class="v">76.7%</span>
        <span class="q">Files where all five fields are right together, 92 of 120</span>
        {moustache("wilson")}</div>
    </div>
    {bn.AGIR}
  </div>
  <div class="note">
    <h2>What this does not prove</h2>
    <p>Both rates are computed correctly. <b>Neither one is wrong.</b> They answer
      different questions, and only one of them is the question at your desk.</p>
    <p>120 files is what we ran. The true per-file rate sits somewhere between
      <b>68.3</b> and <b>83.3</b>, and no amount of presentation narrows that.</p>
  </div>"""

# ── C · le menu descend dans la colonne de droite ─────────────────────────────
BAS_C = f"""<div class="bas">
    <div class="gauche">
      <p class="sous">{bn.SOUS}</p>
      {bn.TABLEAU}
      {bn.AGIR}
      <p class="leg-gauche"><b>Figure 1</b><br>One stack per reader and per field. The
        empty row is the human operator, never sampled field by field.</p>
    </div>
  </div>
  {menu_html("c")}"""

# ── D · les cartes portent la question de chaque constat ──────────────────────
BAS_D = f"""<div class="bas">
    {bn.TABLEAU}
    {bn.AGIR}
  </div>"""

# ── E · la phrase-chiffre, le tableau replié ──────────────────────────────────
BAS_E = f"""<div class="bas">
    <p class="phrase">Your dashboard says <b class="un">94.4%</b>. Your desk says
      <b class="de">76.7%</b>: the share of files where all five fields are right
      together, 92 of 120.</p>
    <details>
      <summary><span class="cr" aria-hidden="true">&#9656;</span>See the table</summary>
      {bn.TABLEAU}
    </details>
    {bn.AGIR}
  </div>"""

# ── F · la bande de chiffres, avec l'intervalle sous chacun ───────────────────
BAS_F = f"""<div class="bas">
    <div class="bande">
      <div class="cel"><span class="et">On the dashboard</span>
        <span class="v">94.4%</span>
        <span class="q">Mean of five field rates</span>
        {moustache("vide")}</div>
      <div class="cel cle"><span class="et">On your desk</span>
        <span class="v">76.7%</span>
        <span class="q">All five fields right on the same file, 92 of 120</span>
        {moustache("wilson")}</div>
      <div class="cel"><span class="et">The gap</span>
        <span class="v">17.7</span>
        <span class="q">Points, over the same 120 case files</span>
        <svg class="mou" viewBox="0 0 210 26" role="img"
             aria-label="A gap of 17.7 points between the two rates.">
          <path class="br" d="M{X(76.7)} 8 L{X(76.7)} 18 M{X(76.7)} 13 L{X(94.4)} 13
            M{X(94.4)} 8 L{X(94.4)} 18"></path>
          <text class="g" x="{(X(76.7) + X(94.4)) / 2:.1f}" y="25"
            text-anchor="middle">17.7 points</text></svg></div>
    </div>
    {bn.AGIR}
  </div>"""

VARIANTES = [
    ("A", "table-etendue", BAS_A, "a", "Cascade, extended table"),
    ("B", "diptyque", BAS_B, "b", "Cascade, finding and reserve"),
    ("C", "menu-colonne", BAS_C, "c", "Cascade, side column menu"),
    ("D", "cartes", BAS_D, "d", "Cascade, question cards"),
    ("E", "phrase", BAS_E, "e", "Cascade, the sentence"),
    ("F", "bande", BAS_F, "f", "Cascade, the strip"),
]

LEG_FIG = (f'<figcaption class="legende"><span class="no">Figure 1</span>'
           f'{LEGENDE_TXT.split(", ", 1)[1]}</figcaption>')

for lettre, nom, bas, cle, titre in VARIANTES:
    fichier = f"Z{lettre}-{nom}.html"
    menu = "" if cle == "c" else menu_html(cle)
    (BASE / fichier).write_text(f"""<!doctype html>
<meta charset="utf-8"><title>{titre}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%2314251e'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fontes/literata.css">
<script>document.documentElement.classList.add("js")</script>
<style>{bn.COMMUN}{ZONE_CSS}</style>
<div class="ecran zone-{cle}">
  <div class="tete"><b>CASCADE</b><span>routing audit, KYC extraction</span>
    <span class="d">report 64bdacf, measured once and frozen</span></div>
  <span class="oeil">Finding 01, two rates over one desk</span>
  <div class="haut"><h1>{bn.TITRE}</h1></div>
  <figure class="plaque">
      {bn.POSES}
    {LEG_FIG}
  </figure>
  <span class="socle-ombre"></span>
{bas}
  {menu}
  {bn.PIED}
</div>
{bn.SCRIPT}
""", encoding="utf-8")
    print(f"  {fichier}")
