#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, urllib2, time
import xml.etree.ElementTree as ET
import socket
import os, os.path, subprocess
from uuid import getnode as get_mac
from utemper_public import *

class cCheck_estados:
    flie_config_wifi = "/tmp/wifi.var"
    file_watchdog =  "/tmp/file_watchdog.txt"
    lastTimeNoche=0
    
    lastTimeCheckInternet=0    
    lastTimeReadWifiStatus =0
    lastTimeModifyWifiStatus =0
    lastTimePerroGuardian = 0

    def __init__(self):
        default_timeout = 5
        socket.setdefaulttimeout(default_timeout)
        gv.number_equipo = 222222#get_mac()
        self.read_wifi_estado()
         
    def suceso (self):
        # check noche:
        if (time.time()-self.lastTimeNoche>900):
            self.checkNoche()
            self.lastTimeNoche = time.time()
            
        if (time.time()-self.lastTimeCheckInternet>180):
            # enviar estado del equipo.
            log(0, "suceso check estados: leemos el estado del Internet" )
            self.check_intenernet()
            self.lastTimeCheckInternet = time.time()
            
        if (time.time()-self.lastTimeReadWifiStatus>5):            
            self.read_wifi_estado()
            self.lastTimeReadWifiStatus = time.time()

        if (time.time()-self.lastTimePerroGuardian>60):            
            self.ActualizaWatchdog()
            self.lastTimePerroGuardian = time.time()
            
    def reset(self):
        self.checkNoche()
        self.read_wifi_estado()

    def checkNoche(self):
        ahora= time.strptime( time.strftime("%I:%M %p", time.localtime()), "%I:%M %p")
        if (gv.hora_init_dia < ahora < gv.hora_init_noche):
            if gv.noche!=0:
                gv.noche=0 # dia
                gv.reset_class = 2
                log(2, "Cambiamos a dia. Reseteamos.")
        else:
            if gv.noche!=1:
                gv.noche=1 # noche
                gv.reset_class = 2
                log(2, "Cambiamos a noche. Reseteamos.")

    def check_intenernet(self):
        # check internet.
        ip_ping = "8.8.8.8"
        result = os.system("ping -c 1 -w 1 %s >/dev/null" %ip_ping)
        if (result== 0):
            gv.internet=1
        else:
            gv.internet=0
         
    def read_wifi_estado(self):
        # read
        try:
            if (os.path.getmtime(self.flie_config_wifi) != self.lastTimeModifyWifiStatus):
                log(1, "suceso check estados: leemos el estado Wifi" )
                f = open(self.flie_config_wifi)
                lines = f.readlines()
                f.close()
                if int(lines[2]) == 1:
                    gv.internet = 1
                gv.wifi_estado=int(lines[0]) + int(lines[1]) +int(lines[2])
                gv.wifi_ip=lines[3].replace("\n", "")
                self.lastTimeModifyWifiStatus = os.path.getmtime(self.flie_config_wifi)
                return 1
            else:
                return 0

        except:
            log(4, "Imposible poder leer el estado del wifi del fichero wifi.var" )
            gv.wifi_estado = 0
            gv.wifi_ip = ""
            return 0

    def ActualizaWatchdog(self):
        try:
            log(0, "Actualizamos perro guardian: " + self.file_watchdog)
            f = open(self.file_watchdog,'w')
            lines = f.write("1")
            f.close()
        except:
            log(5, "Imposibleactulizar perro guardian: reboot!!" )
            subprocess.call("reboot")
            exit()
