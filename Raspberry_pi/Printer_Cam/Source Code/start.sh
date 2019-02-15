#!/bin/bash

sudo swapoff --all
sudo rm /var/swap
cd /home/pi/Python-Thermal-Printer
/usr/bin/python2.7 Printercam.py 1>/tmp/Test.log 2>&1 
echo "Error Utemper: Reiniciamos..."
echo "Esperamos 200 seg."
sleep 200
sudo shutdown -r -F now

 
