#!/bin/bash

echo -e "\tIniciar start_atchdog.sh"

count=1
while [ $count -le 15 ]
do
  sleep 180
  # si el programa esta arrancado lo cerramos.
  if [ ! -f /tmp/file_watchdog.txt ]; then
    echo $(date  +"%F_%T")";5;ERROR  /tmp/file_watchdog.txt no existe Reboot! KO"
    echo $(date  +"%F_%T")";5;ERROR  /tmp/file_watchdog.txt no existe Reboot! KO">>/var/utemp/logs.log
    reboot
  fi
  rm -f /tmp/file_watchdog.txt
done

echo $(date  +"%F_%T")";1; Fin de start_atchdog.sh END"
echo $(date  +"%F_%T")";1; Fin de start_atchdog.sh END">>/var/utemp/logs.log