# poner hora equipos #

poner hora equipos


# Details #

poner en hora un equipo:

sudo date -s "$(wget -S  "http://www.google.com/" 2>&1 | grep -E '<sup>[[:space:]]*[dD]ate:' | sed 's/</sup>[[:space:]]**[dD](dD.md)ate:[[:space:]]**//' | head -1l | awk '{print $1, $3, $2,  $5 ,"GMT", $4 }' | sed 's/,//')"

guardar la hora en la maquina:

hwclock --systohc

check:

hwclock --show