#!/bin/bash

echo -e "\tIniciar start_read_temp.sh"

count=1
while [ $count -le 15 ]
do
  python read_temp.py 
  x=$(( $x + 1 ))
  sleep 30
  echo $(date  +"%F_%T")";4;start_read_temp.sh;salida inesperada de read_temp.py KO">>/var/utemp/logs.log
done

echo $(date  +"%F_%T")";5;start_read_temp.sh;max errores KO">>/var/utemp/logs.log
echo $(date  +"%F_%T")";5;start_read_temp.sh;Rebbot OK">>/var/utemp/logs.log
sleep 60

reboot
