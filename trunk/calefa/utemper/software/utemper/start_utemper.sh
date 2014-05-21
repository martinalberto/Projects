#!/bin/bash

echo "Iniciar Utemper"

#iniciamos ficheros.
mkdir -p /var/utemp/
echo "-1" > /tmp/rele.var
echo "-1" > /tmp/temp.var
echo "-1" > /tmp/ldr.var
echo "0" > /tmp/time_espera.var
# poner permisos.

chmod 777 /tmp/rele.var
chmod 777 /tmp/temp.var
chmod 777 /tmp/ldr.var
chmod 777 /tmp/time_espera.var

# mkidr dir
mkdir -p config/
mkdir -p config/server/
mkdir -p config/send/

#logs
mkdir -p /var/utemp/

echo $(date  +"%F_%T")";1;INI1;Iniciamos ficheros">>/var/utemp/logs.log
chmod 777 /var/utemp/logs.log

# Iniciamos programas.
sleep 10

#bash /home/pi/utemper/start_read_temp.sh &
#bash /home/pi/utemper/start_read_ldr.sh &
#bash /home/pi/utemper/start_rele.sh &
sleep 2


