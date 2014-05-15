#!/bin/bash

echo "Iniciar Utemper"

#iniciamos ficheros.
mkdir -p /var/utemp/
echo "-1" > /tmp/rele.var
echo "-1" > /tmp/temp.var
echo "-1" > /tmp/lrd.var
echo "0" > /tmp/time_espera.var
# poner permisos.

chmod 777 /tmp/rele.var
chmod 777 /tmp/temp.var
chmod 777 /tmp/lrd.var
chmod 777 /tmp/time_espera.var

#logs
mkdir -p /var/utemp/
echo $(date  +"%F_%T")";1;INI1;Iniciamos ficheros">>/var/utemp/logs.log
chmod 777 /var/utemp/logs.log

# Iniciamos programas.

start_read_temp.sh
sleep 2

