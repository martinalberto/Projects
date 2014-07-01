#!/bin/bash

echo -e "\tIniciar start_rele.sh"

count=1
while [ $count -le 15 ]
do

  # si el programa esta arrancado lo cerramos.
  killall rele 2>/dev/null 

  /home/pi/utemper/rele
  x=$(( $x + 1 ))
  sleep 30
  echo $(date  +"%F_%T")";4;start_rele.sh;salida inesperada de rele KO">>/var/utemp/logs.log
done

echo $(date  +"%F_%T")";5;start_rele.sh;max errores KO">>/var/utemp/logs.log
echo $(date  +"%F_%T")";5;start_rele.sh;Rebbot OK">>/var/utemp/logs.log
sleep 60

reboot
