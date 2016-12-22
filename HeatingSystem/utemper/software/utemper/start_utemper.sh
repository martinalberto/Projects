#!/bin/bash

echo "Iniciar Utemper"

# opcion de luz de la pantalla.
echo 252 > /sys/class/gpio/export
sudo sh -c "echo 'out' > /sys/class/gpio/gpio252/direction"
sudo sh -c "echo '1' > /sys/class/gpio/gpio252/value"

#apagamos rele:
echo "3" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio3/direction
echo "0" > /sys/class/gpio/gpio3/value

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
chmod +x  ./utemper.py

# mkidr dir
mkdir -p config/
mkdir -p config/send/

#logs
mkdir -p /var/utemp/
echo $(date  +"%F_%T")";1;===================================================">>/var/utemp/logs.log
echo $(date  +"%F_%T")";1;       Iniciamos ficheros UTEMPER ">>/var/utemp/logs.log
echo $(date  +"%F_%T")";1;===================================================">>/var/utemp/logs.log
chmod 777 /var/utemp/logs.log

# desabilitamos swap:
sudo swapoff --all
sudo dphys-swapfile swapoff
sudo rm /var/swap

# convertirmos ficheros a linux.
cd /home/pi/utemper/
dos2unix * 2>/dev/null
dos2unix config/* 2>/dev/null

# cerramos antiguos programas:
killall start_read_temp.sh 2>/dev/null
killall start_read_ldr.sh 2>/dev/null
killall start_rele.sh 2>/dev/null
killall utemper.py 2>/dev/null
killall connect_wifi.py 2>/dev/null
killall utemper.py 2>/dev/null
# Iniciamos programas.

bash /home/pi/utemper/start_wifi_conect.sh &

bash /home/pi/utemper/start_read_ldr.sh &
#bash /home/pi/utemper/start_watchdog.sh &
sudo ./utemper.py
 
echo "Error Utemper: Reiniciamos..."
echo "Esperamos 200 seg."
sleep 200
#sudo shutdown -r -F now
