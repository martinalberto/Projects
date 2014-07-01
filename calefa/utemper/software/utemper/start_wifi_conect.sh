#!/bin/bash

echo -e "\tIniciar start_connect_wifi.sh"

count=1
while [ $count -le 15 ]
do
  python connect_wifi.py 
  x=$(( $x + 1 ))
  sleep 30
  echo $(date  +"%F_%T")";4;connect_wifi.sh;salida inesperada de read_temp.py KO">>/var/utemp/logs.log
done

echo $(date  +"%F_%T")";5;connect_wifi.sh;max errores KO">>/var/utemp/logs.log
echo $(date  +"%F_%T")";5;connect_wifi.sh;Rebbot OK">>/var/utemp/logs.log
sleep 60

reboot
