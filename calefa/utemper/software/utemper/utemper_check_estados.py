#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, urllib2, time
import xml.etree.ElementTree as ET
import socket
import os.path
from uuid import getnode as get_mac
from utemper_public import *

class cCheck_estados:
    flie_config_wifi = "/tmp/wifi.var"
    lastTimeNoche=0

    lastTimeSend=0

    lastTimeDownloadConfig=0
    download_config = False

    lastTimeCheckInternet=0    
    lastTimeReadWifiStatus =0
    lastTimeModifyWifiStatus =0

    def __init__(self):
        default_timeout = 5
        socket.setdefaulttimeout(default_timeout)
        gv.number_equipo = get_mac()
        self.read_wifi_estado()
         
    def suceso (self):
        # check noche:
        if (time.time()-self.lastTimeNoche>900):
            self.checkNoche()
            self.lastTimeNoche = time.time()
            
        if (time.time()-self.lastTimeCheckInternet>180):
            # enviar estado del equipo.
            clog().log(0, "suceso check estados: leemos el estado Internet" )
            self.check_intenernet()
            self.lastTimeCheckInternet = time.time()
            
        if (time.time()-self.lastTimeReadWifiStatus>5):
            clog().log(0, "suceso check estados: leemos el estado Wifi" )
            result = self.read_wifi_estado()
            self.lastTimeReadWifiStatus = time.time()

        if (time.time()-self.lastTimeSend>self.lastTimeDownloadConfig) and (gv.internet == 1):
            # enviar estado del equipo.
            self.send_estatus()
            self.lastTimeSend = time.time()

        if (time.time()-self.lastTimeDownloadConfig>2) and (self.download_config) and (gv.internet == 1):
            self.update_file()
            self.lastTimeDownloadConfig = time.time()

        if (time.time()-self.lastTimeUploadConfig>3) and (gv.upload_config) and (self.download_config == False) and (gv.internet == 1):
            self.upload_file()
            self.lastTimeUploadConfig = time.time()

    def reset(self):
        self.lastTimeDownloadConfig = 5
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
            if (os.path.getmtime(self.flie_config_wifi) != self.lastTimeModifyWifiStatus):
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
            clog().log(4, "Imposible poder leer el estado del wifi del fichero wifi.var" )
            gv.wifi_estado = 0
            gv.wifi_ip = ""
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
        clog().log(1, "Enviado el estado a: %s" %(text))
        self.check_response_send_status(response.read())
    #except:
    #    gv.internet = 0
    #    clog().log(3, "Imposible poder enviar el estado a: %s" %text)

    def update_file(self):
        try:
            clog().log(2," update_file from server http://www.utemper.net/movil/update_file_config.php ... ")
            text2="http://www.utemper.net/movil/update_file_config.php"
            data = urllib.urlencode({"operacion":"2utemper" , "id":str(gv.number_equipo)})

            clog().log(2," update_file from server to local file....")
            configData = urllib2.urlopen(text2,  data=data).read()
            cread_config().write_config_file(configData)
            download_config = False
        except:
            clog().log(0," Imposible send status to http://www.utemper.net/movil/update_file_config.php ... ")

    def check_response_send_status(self, lines):
        lastTime =  self.lastTimeDownloadConfig;

        for line in lines:
            line = line.replace("\n", "")
            if (line.lower() == "update:read"):
                self.download_config = True
            elif (line.lower() == "segsendstatus:5"):
                lastTime = 5
            elif (line.lower() == "segsendstatus:60"):
                lastTime = 60
            elif (line.lower() == "segsendstatus:600"):
                lastTime = 60
        if (lastTime < self.lastTimeDownloadConfig):
            self.lastTimeDownloadConfig = lastTime