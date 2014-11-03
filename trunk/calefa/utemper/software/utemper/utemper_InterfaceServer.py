#!/usr/bin/env python

import urllib, urllib2, time
import xml.etree.ElementTree as ET
import socket
import os, os.path
import subprocess
from uuid import getnode as get_mac
from utemper_public import *

class cInterfaceServer:
    folder_send_files =  "config/send/"

    maxTimeSendStatus = 5
    maxTimeSendFromServer = 200

    lastTimeInterfaceServer = 0
    lastTimeSendStatus=0

    lastSendRele = -1
    download_config = False
    
    def __init__(self):
        default_timeout = 3
        socket.setdefaulttimeout(default_timeout)

    def suceso (self):
        if  (time.time()-self.lastTimeInterfaceServer > 3) and (gv.internet == 1):

            if (time.time()-self.lastTimeSendStatus>self.maxTimeSendStatus) or (gv.rele != self.lastSendRele):
                # enviar estado del equipo.
                if (self.send_estatus()):
                    self.lastTimeSendStatus = time.time()

            if (self.download_config):
                self.download_files()

            if (gv.upload_config) and (self.download_config == False) :
                self.upload_files()

            self.checkmaxTimeSendStatus()

            self.lastTimeInterfaceServer = time.time()

    def reset(self):
        self.maxTimeSendStatus = 5
        self.lastTimeSendStatus =  0
        self.maxTimeSendFromServer = 200
        lastSendRele = -1
         
    def checkmaxTimeSendStatus(self):
         maxTimeSend = self.maxTimeSendStatus
         if (time.time() - gv.lastTimeChageSomething <30):
             self.maxTimeSendStatus = 5 
         elif (time.time() - gv.lastTimeChageSomething <90):
             self.maxTimeSendStatus = 30
         elif (time.time() - gv.lastTimeChageSomething <180):
             self.maxTimeSendStatus = 90
         else:
             self.maxTimeSendStatus = 200

         if (self.maxTimeSendFromServer < self.maxTimeSendStatus):
             self.maxTimeSendStatus = self.maxTimeSendFromServer

         if (maxTimeSend != self.maxTimeSendStatus):
             log(3, "Nuevo tiempo Max to send estado: %d" %self.maxTimeSendStatus) 

    def send_estatus(self):
        text="http://www.utemper.net/movil/recive_status.php?id=" + str(gv.number_equipo)
        text+= "&temp="+str(gv.temperatura)
        text+= "&rele="+str(gv.rele)
        try:
            response = urllib2.urlopen(text)
            gv.internet = 1
            log(1, "Enviado el estado a: %s" %(text))
            self.check_response_send_status(response.read())
            self.lastSendRele = gv.rele
        except:
            gv.internet = 0
            log(3, "Imposible poder enviar el estado a: %s" %text)
            return False
        return True

    def check_response_send_status(self, lines):
        try:
            lines = lines.split("\n")
        except:
            log(3, "check_response_send_status imposible leer texto")
            return

        for line in lines:
            if (line.lower() == "update:read"):
                self.download_config = True
            elif (line.lower() == "segsendstatus:5"):
                self.maxTimeSendFromServer = 5
            elif (line.lower() == "segsendstatus:60"):
                self.maxTimeSendFromServer = 60
            elif (line.lower() == "segsendstatus:600"):
                self.maxTimeSendFromServer = 300
    
    def download_files(self):
        try:
            log(2," download_files from server to local file....")
            text = "sshpass -f /var/utemp/pass.txt rsync -av --remove-source-files --timeout=8  ubuntu@utemper.net:/var/www/utemper/movil/text/" + str(gv.number_equipo) + "/send/* config/."
            result = subprocess.call(text, shell = True)
			
            if result ==0:
                gv.lastTimeChageSomething = time.time()
                self.download_config = False
                log(2, "download_files desde utemper.net OK")
                gv.reset_class = 1
            else:
                log(3, "download_files desde utemper.net ERROR!")
                self.lastTimeInterfaceServer += 2 # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        except:
            log(0," Imposible send status to http://www.utemper.net/movil/download_files_config.php ... ")
    
    def upload_files(self):
        try:
            os.listdir(self.folder_send_files)
        except:
            log(5,"upload_files: ERROR! Imposible read fonder: %s" %self.folder_send_files)
            gv.upload_config =False
            return
 
        if len(os.listdir(self.folder_send_files))!=0: 
            text =  "sshpass -f /var/utemp/pass.txt rsync  -av --remove-source-files --timeout=8  config/send/* ubuntu@utemper.net:/var/www/utemper/movil/text/" + str(gv.number_equipo) + "/."
            log(2," upload_files from local to server file....")
            result = subprocess.call(text, shell = True)
            if result ==0:
                gv.lastTimeChageSomething = time.time()
                log(2, "download_files A utemper.net OK")
            else:
                log(3, "download_files A utemper.net ERROR!")
            gv.lastTimeChageSomething = time.time()
