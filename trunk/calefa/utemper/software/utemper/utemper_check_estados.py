#!/usr/bin/env python

import urllib, urllib2, time
import xml.etree.ElementTree as ET
import socket
from uuid import getnode as get_mac
from utemper_public import *

class cCheck_estados:
    lastTimeNoche=0
    lastTimeSend=0
    lastTimeCheckInternet=0
    lastTimeReadWifiStatus =0
    
    def __init__(self):
        default_timeout = 5
        socket.setdefaulttimeout(default_timeout)
        gv.number_equipo = get_mac()
        self.read_wifi_estado()
         
    def suceso (self):
        # check noche:
        if (time.time()-self.lastTimeNoche>600):
            self.checkNoche()
            self.lastTimeNoche = time.time()

        if (time.time()-self.lastTimeSend>180) and (gv.internet == 1):
            # enviar estado del equipo.
            self.send_estatus()
            self.lastTimeSend = time.time()
            
        if (time.time()-self.lastTimeCheckInternet>180):
            # enviar estado del equipo.
            clog().log(0, "suceso check estados: leemos el estado Internet" )
            self.check_intenernet()
            self.lastTimeCheckInternet = time.time()
            
        if (time.time()-self.lastTimeReadWifiStatus>30):
            clog().log(0, "suceso check estados: leemos el estado Wifi" )
            result = self.read_wifi_estado()
            if (result ==1):
                self.lastTimeReadWifiStatus = time.time()
            else:
                self.lastTimeReadWifiStatus = time.time() - 26 # chequeamos cada 5 seg si no hay wifi.
            
    def reset(self):
        self.checkNoche()
        self.send_estatus()
        
    def checkNoche(self):
        gv.hora_init_dia
        ahora= time.strptime( time.strftime("%I:%M %p", time.localtime()), "%I:%M %p")
        if (gv.hora_init_dia < ahora < gv.hora_init_noche):
            gv.noche=0 # dia
        else:
            gv.noche=1 # noche
     
    def check_intenernet(self):
        # check internet.
        ip_ping = "8.8.8.8"
        result = os.system("ping -c 1 -w 1 %s >/dev/null" %ip_ping)
        if (result== 0):
            gv.internet=1
        else:
            gv.internet=0
         
    def read_wifi_estado (self):
        # read
        try:
            f = open("/tmp/wifi.var")
            lines = f.readlines()
            f.close()
            if int(lines[2]) == 1:
                gv.internet = 1
            gv.wifi_estado=int(lines[0]) + int(lines[1]) +int(lines[2])
            gv.wifi_ip=lines[3].replace("\n", "")
            return 1
        except:
            clog().log(4, "Imposible poder leer el estado del wifi del fichero wifi.var" )
            gv.wifi_estado = 0
            gv.wifi_ip = ""
            gv.internet=0
            return 0
            
    def send_estatus(self):
        if (gv.internet != 1):
            return
        text="http://www.utemper.net/movil/recive_status.php?id=" + str(gv.number_equipo)
        text+= "&temp="+str(gv.temperatura)
        text+= "&rele="+str(gv.rele)
	#try:
        response = urllib2.urlopen(text)
        gv.internet = 1
        clog().log(1, "Enviado el estado a: %s" %text)		
        if (response.read()=="READ"):
            #update file.
            self.update_file()
	#except:
    #    gv.internet = 0
    #    clog().log(3, "Imposible poder enviar el estado a: %s" %text)
	
    def update_file(self):
        clog().log(2," update_file from server http://www.utemper.net/movil/update_file_config.php ... ")
        text2="http://www.utemper.net/movil/update_file_config.php"
        data = urllib.urlencode({"operacion":"2utemper" , "id":str(gv.number_equipo)})
		
        clog().log(2," update_file from server to local file....")
        configData = urllib2.urlopen(text2,  data=data).read()
        cread_config().write_config_file(configData)
