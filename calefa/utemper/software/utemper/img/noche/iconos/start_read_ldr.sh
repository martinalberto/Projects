#!/bin/bash

echo -e "\tIniciar start_read_ldr.sh"

count=1
while [ $count -le 15 ]
do

  killall read_ldr.py 2>/dev/null 
  
  python read_ldr.py 
  #x=$(( $x + 1 )) # NUNCA TERMINA!!!!!
  sleep 30
  echo $(date  +"%F_%T")";4;start_read_ldr.sh;salida inesperada de read_ldr.py KO">>/var/utemp/logs.log
done

echo $(date  +"%F_%T")";5;start_read_ldr.sh;max errores KO">>/var/utemp/logs.log
echo $(date  +"%F_%T")";5;start_read_ldr.sh;Rebbot OK">>/var/utemp/logs.log
sleep 60

reboot
