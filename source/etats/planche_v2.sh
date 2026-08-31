#!/bin/bash
# Planche v2 : les six objets sur crème, rangée du haut ; références 3dicons en bas.
set -e
E="/private/tmp/claude-501/-Users-arslanechr-Downloads-atlas-final-en-fr/9eaa6456-ea12-48c5-bd77-6279f40c9def/scratchpad/maquette-cascade/etats"
cd "$E"
CREME="0xf2ede2"

for o in cadenas balance cle stylo dossier podium; do
  ffmpeg -y -loglevel error -f lavfi -i "color=$CREME:s=700x700" -i /tmp/v2-$o/img-000.png \
    -filter_complex "[0][1]overlay=0:0,format=rgb24" -frames:v 1 /tmp/pv2-$o.png
done

ffmpeg -y -loglevel error \
  -i /tmp/pv2-cadenas.png -i /tmp/pv2-balance.png -i /tmp/pv2-cle.png \
  -i /tmp/pv2-stylo.png -i /tmp/pv2-dossier.png -i /tmp/pv2-podium.png \
  -filter_complex "[0][1][2]hstack=3[h1];[3][4][5]hstack=3[h2];[h1][h2]vstack=2,format=rgb24" \
  /tmp/planche-v2.png

# la rangée de références (lock/key/mail/link/dollar) pour la comparaison
ffmpeg -y -loglevel error \
  -i refs/s-lock-p.png -i refs/s-key-p.png -i refs/s-mail-p.png -i refs/s-link-p.png -i refs/s-dollar-p.png \
  -filter_complex "[0][1][2][3][4]hstack=5,pad=2100:ih:0:0:0x1a1a1a,format=rgb24" /tmp/refs-row.png

ffmpeg -y -loglevel error -i /tmp/planche-v2.png -i /tmp/refs-row.png \
  -filter_complex "[0]scale=2100:-1[a];[a][1]vstack=2,format=rgb24" /tmp/planche-v2-vs-refs.png

echo "planche : /tmp/planche-v2.png ; comparaison : /tmp/planche-v2-vs-refs.png"
