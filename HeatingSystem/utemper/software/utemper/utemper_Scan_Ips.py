#!/usr/bin/env python

#import RPi.GPIO as GPIO
import os, os.path
import re
import shutil
import subprocess
from utemper_public import *

class cUtemperCheckIp:

    lastTimeScan = 0
    lastValues=list()
    status =0
    modeSaveConfig = 0
    vSubprocess = None
    FILE_CONF_LIST = "config/list_Mac.txt"
    FILE_TMP_LIST = "/tmp/ip_scan_list.txt"
    FILE_CONF_LIST_SEND = "config/send/list_Mac.txt"
    
    def __init__(self):
        self.status = 0
        self.lastValues[:]= []
        self.lastValues.append(False)
        self.lastValues.append(False)
        self.lastValues.append(False)
        subprocess.call(["killall", "arp"])
        subprocess.call(["killall", "fping"])
        log(0, "Init Scan IPs")
		
    def suceso (self):
        if self.status == 0:
            #wait time for start.
            if  (time.time()-self.lastTimeScan > 90) and (gv.internet== 1):
                self.lastTimeScan = time.time()
                self.status = 1

        elif self.status == 1:
            # Check.
            self.status = 2
            if(os.path.isfile(self.FILE_CONF_LIST)!= True):
                log(3,"Warning Don't exist file: " + self.FILE_CONF_LIST)
                self.status = 5

        elif self.status == 2:
            # Execute.
            if (len(gv.wifi_ip) > 0):
               log(0,"Empezamos a Escanear IPs")
               subNetwork =re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}', gv.wifi_ip).group(0) 
               log (2, "bash + scan_ips.sh " + subNetwork + self.FILE_TMP_LIST)
               self.vSubprocess = subprocess.Popen(["bash", "scan_ips.sh", subNetwork, self.FILE_TMP_LIST])
               self.lastTimeScan = time.time()
               self.status =3
            else:
              self.status = 5 #Error.
              
        elif self.status == 3:
            #wait
            if (self.vSubprocess !=None):
               self.status = 4 # OK -> Vamos.
        
            if  (time.time()-self.lastTimeScan > 300):
                #Error
                log(3,"Error: tiempo maximo scan_ips.sh ")
                self.status = 5
                self.vSubprocess.kill()
                self.lastTimeScan = time.time()

        elif self.status == 4:
            # Check Diff.
            result =0
            self.status =0
            self.lastTimeScan = time.time()
            time.sleep(1)
            if(os.path.isfile(self.FILE_TMP_LIST)!= True):
                log(3,"Error: Fichero "+self.FILE_TMP_LIST+" No existe. ")
                self.status = 5
                return
                
            result  = subprocess.call("diff -i -B -w "+self.FILE_CONF_LIST+" "+self.FILE_TMP_LIST+" | grep '>'", shell = True) # 1: ERROR, 0: OK.
            log(0,"diff -i -B -w "+self.FILE_CONF_LIST+" "+self.FILE_TMP_LIST+" | grep '>'|wc -l result: " + str(result))
            gv.scanIp_OK = True
            if (result == 0):
                self.checkChange(True) # Hay gente
            else:
                self.checkChange(False)  # NO hay nadie.

            if (self.modeSaveConfig == 1):
                self.status  = 6 # save config.
                
        elif self.status == 5:
            # ERROR!
            gv.scanIp_OK = False
            if  (time.time()-self.lastTimeScan > 180) and (gv.wifi_estado>2):
                self.lastTimeScan = time.time()
                self.status = 0
                log(1,"Error: Esperados 3 min. Se intenta otra vez.")
        
        elif self.status == 6:
            # Save config.
            self.status = 0
            log(2,"Valores actuales de MAC guardados como NO en casa.")
            log(2,"Copiados desde "+self.FILE_TMP_LIST +" a "+self.FILE_CONF_LIST )
            shutil.copy(self.FILE_TMP_LIST, self.FILE_CONF_LIST)
            shutil.copy(self.FILE_TMP_LIST, self.FILE_CONF_LIST_SEND) # Send File to Central

            cread_config().update_config_file("Save_Mac_NoPerson","0")
            gv.reset_class = 1
            self.modeSaveConfig = 0;

                
    def reset(self):
        self.modeSaveConfig = int (cread_config().read_config("Save_Mac_NoPerson"))
        self.__init__()

    def checkChange (self, NewValue):
        self.lastValues.pop(0)
        self.lastValues.append(NewValue)
        
        if(NewValue == True):
            log(0,"Hay gente en Casa.")
            gv.scanIp_EnCasa = True

        elif (True in self.lastValues):
            log(0,"Hay gente en Casa.")
            gv.scanIp_EnCasa = True

        else:
            log(0,"NADIE gente en Casa.")
            gv.scanIp_EnCasa = False
