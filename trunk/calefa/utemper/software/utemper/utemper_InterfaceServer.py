#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    maxTimeSendFromServer = 360

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
                self.update_file()

            if (gv.upload_config) and (self.download_config == False) :
                self.upload_files()

            self.checkmaxTimeSendStatus()

            self.lastTimeInterfaceServer = time.time()

    def reset(self):
        self.maxTimeSendStatus = 5
        self.lastTimeSendStatus =  0
        self.maxTimeSendFromServer = 360
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
             self.maxTimeSendStatus = 360

         if (self.maxTimeSendFromServer < self.maxTimeSendStatus):
             self.maxTimeSendStatus = self.maxTimeSendFromServer

         if (maxTimeSend != self.maxTimeSendStatus):
             clog().log(3, "Nuevo tiempo Max to send estado: %d" %self.maxTimeSendStatus) 

    def send_estatus(self):
        text="http://www.utemper.net/movil/recive_status.php?id=" + str(gv.number_equipo)
        text+= "&temp="+str(gv.temperatura)
        text+= "&rele="+str(gv.rele)
        try:
            response = urllib2.urlopen(text)
            gv.internet = 1
            clog().log(1, "Enviado el estado a: %s" %(text))
            self.check_response_send_status(response.read())
            self.lastSendRele = gv.rele
        except:
            gv.internet = 0
            clog().log(3, "Imposible poder enviar el estado a: %s" %text)
            return False
        return True

    def check_response_send_status(self, lines):
        lastTime =  self.maxTimeSendStatus;

        for line in lines:
            line = line.replace("\n", "")
            if (line.lower() == "update:read"):
                self.download_config = True
            elif (line.lower() == "segsendstatus:5"):
                self.maxTimeSendFromServer = 5
            elif (line.lower() == "segsendstatus:60"):
                self.maxTimeSendFromServer = 60
            elif (line.lower() == "segsendstatus:600"):
                self.maxTimeSendFromServer = 600
    
    def update_file(self):
        try:
            #clog().log(2," update_file Download from server http://www.utemper.net/movil/update_file_config.php ... ")
            #text2="http://www.utemper.net/movil/update_file_config.php"
            #data = urllib.urlencode({"operacion":"2utemper" , "id":str(gv.number_equipo)})

            clog().log(2," update_file from server to local file....")
            text = "sshpass -f /var/utemp/------.txt rsync -av --remove-source-files --timeout=8  ------@utemper.net:/tmp/* /home/pi/utemper/config/."
            result = subprocess.call(text, sell = True)
            if result ==0:
                gv.lastTimeChageSomething = time.time()
                download_config = False
        except:
            clog().log(0," Imposible send status to http://www.utemper.net/movil/update_file_config.php ... ")
    
    def upload_files(self):
        try:
            dirs = os.listdir(self.folder_send_files)
        except:
            clog().log(5,"upload_files: ERROR! Imposible read fonder: %s" %self.folder_send_files)
            gv.upload_config =False
            return
			
        if os.listdir(self.folder_send_files) == []: 
            text =  "sshpass -f /var/utemp/----.txt rsync  -av --remove-source-files --timeout=15  /home/pi/utemper/config/send/* -------@utemper.net:/tmp/."
            result = subprocess.call(text, shell = True)
            if result ==0:
                gv.lastTimeChageSomething = time.time()

            gv.lastTimeChageSomething = time.time()