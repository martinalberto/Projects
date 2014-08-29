#!/usr/bin/env python

import urllib, time
import xml.etree.ElementTree as ET
import socket
from uuid import getnode as get_mac
from utemper_public import *

class cCheck_estados:
    lastTimeNoche=0
    
    def __init__(self):
        default_timeout = 5
        socket.setdefaulttimeout(default_timeout)
        gv.number_equipo = get_mac()
         
    def suceso (self):
        # check noche:
        if (time.time()-self.lastTimeNoche>600):
            self.checkNoche()
            self.lastTimeNoche = time.time()
            
            # enviar estado del equipo.
            self.send_estatus()
            
    def checkNoche(self):
        gv.hora_init_dia
        ahora= time.strptime( time.strftime("%I:%M %p", time.localtime()), "%I:%M %p")
        if (gv.hora_init_dia < ahora < gv.hora_init_noche):
            gv.noche=0 # dia
        else:   gv.noche=1 # noche
    
    def read_wifi_estado (self):
        # read
        try:
            f = open("/tmp/crear_wifi.var")
            lines = f.readlines()
            f.close()
            if int(lines[2]) == 1:
                gv.internet = 1
            gv.wifi_estado=int(lines[0]) + int(lines[1]) +int(lines[2])
            gv.wifi_ip=lines[3].replace("\n", "")
            
        except:
            clog().log(4, "Imposible poder leer el estado del wifi del fichero wifi.var" )
            gv.wifi_estado= 0
            gv.wifi_ip = ""
            gv.wifi_error=1
            
    def send_estatus(self):
        text="ticsismtemas.com/utemper/send.php?num=" + str(gv.number_equipo)
        text+= "&temp="+str(gv.temperatura)
        text+= "&rele="+str(gv.rele)
        try:
            response = urllib2.urlopen('text')
            gv.wifi_error=0
        except:
            gv.wifi_error=1
