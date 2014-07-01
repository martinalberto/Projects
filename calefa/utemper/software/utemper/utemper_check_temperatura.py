#!/usr/bin/env python

import sys
import time, os
from utemper_public import *

class cCheck_temperatura:
    lastTimeNoche=0
    RELE_FILE="/tmp/rele.var"
    FOLER_PROGRA = "programacion/"
    tiempo_rele = 0
    horarios=[]
    def __init__(self):
        # read config value:
        gv.temperatura_max = int (cread_config().read_config("temperatura"))
        gv.estadoCalefa = int (cread_config().read_config("estado_caldera"))
        self.checkestadotemperatura()
        self.actualiza_rele(gv.rele)

    def suceso(self):
        # check noche:
        if (time.time()-self.lastTimeNoche>6):
            self.checkestadotemperatura()
            self.lastTimeNoche = time.time()

    def checkestadotemperatura(self):
        
        if(gv.estadoCalefa == 0):
            # estado Apagado.
            if (gv.rele !=0):
                self.actualiza_rele(0)

        elif(gv.estadoCalefa == 1):
            #estado  Encendido.
            self.check_temperatura()

        elif (gv.estadoCalefa == 2):
            # estado programado
            hora=time.localtime()
            index = hora.tm_hour + (hora.tm_min/15)
            if (self.horarios[index]!="0"):
                self.check_temperatura()
                
    def check_temperatura(self):
        if ((gv.temperatura - 0.1) < gv.temperatura_max) and (gv.rele==0):
                # temperatura menor y rele apagado.
                self.actualiza_rele(1)

        elif ((gv.temperatura + 0.1) > gv.temperatura_max) and (gv.rele==1):
                # temperatura mayor y rele encendido.
                self.actualiza_rele(0)
                
    def actualiza_rele(self, valor):
        File = file(self.RELE_FILE, 'w')
        File.write(str(valor))
        File.close()
        gv.rele
        clog().log(1, "actulizado valor del rele a -%d- " %(valor) )
        
    def leer_temperatura(self):
        fichero = str(datetime.datetime.date.fromtimestamp(time.localtime()).weekday()+1) + ".txt"
        File = file(self.FOLER_PROGRA +fichero, 'r')
        line = f.readline()
        line = line.replace("\n", "")
        File.close()        
        self.horarios = line.split(';')
        
            
