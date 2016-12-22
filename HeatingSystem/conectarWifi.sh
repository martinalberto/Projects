#!/bin/sh

sleep 40

ifconfig eth0 192.168.0.222 netmask 255.255.255.0 broadcast 192.168.0.1 2>/dev/null


if ping -c 1 8.8.8.8
then
  echo "Hay Conexion a internet"
else
  echo "No hay conexion a internet:"
  killall wpa_supplicant
  ifconfig wlan0 down
  ifconfig wlan0 up
  # configurar wpa_supplicant con aplicacion destop.
  wpa_supplicant -c/etc/wpa_supplicant/wpa_supplicant.conf -iwlan0 -B
  sleep 60
  dhclient -4 wlan0 -v 
  ##ifconfig wlan0 
fi
