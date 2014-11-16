#!/bin/bash

echo "Iniciar Utemper"

# opcion de luz de la pantalla.
echo 252 > /sys/class/gpio/export

#iniciamos ficheros.
mkdir -p /var/utemp/
echo "-1" > /tmp/rele.var
echo "-1" > /tmp/temp.var
echo "-1" > /tmp/ldr.var
echo "1" > /tmp/file_watchdog.txt
echo "30" > /tmp/time_espera.var
echo -e "0\n0\n0\n0" >/tmp/wifi.var

# poner permisos.

chmod 777 /tmp/rele.var
chmod 777 /tmp/temp.var
chmod 777 /tmp/ldr.var
chmod 777 /tmp/time_espera.var
chmod 777 ./rele

# mkidr dir
mkdir -p config/
mkdir -p config/send/

#logs
mkdir -p /var/utemp/

echo $(date  +"%F_%T")";1;Start Utemper.sh: Iniciamos ficheros">>/var/utemp/logs.log
chmod 777 /var/utemp/logs.log

# desabilitamos swap:
sudo swapoff --all
sudo rm /var/swap

# convertirmos ficheros a linux.
cd /home/pi/utemper/
dos2unix *

# cerramos antiguos programas:
killall start_read_temp.sh 2>/dev/null
killall start_read_ldr.sh 2>/dev/null
killall start_rele.sh 2>/dev/null
killall utemper.py 2>/dev/null
killall connect_wifi.py 2>/dev/null

# Iniciamos programas.
sleep 10

bash /home/pi/utemper/start_read_ldr.sh &
bash /home/pi/utemper/start_rele.sh &
#bash /home/pi/utemper/start_wifi_conect.sh &
sleep 2

bash /home/pi/utemper/start_watchdog.sh &
sudo python utemper.py
