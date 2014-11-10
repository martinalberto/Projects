#!/usr/bin/env python

import sys
import time, datetime, os
from utemper_public import *

class cCheck_temperatura:
    lastTimeCheckCalefa=0
    RELE_FILE="/tmp/rele.var"
    FOLER_PROGRA = "config/"
    tiempo_rele = 0
    dia_horarios = 0
    horarios=[]
    def __init__(self):
        # read config value:
        gv.temperatura_max = float (cread_config().read_config("temperatura"))
        gv.estadoCalefa = int (cread_config().read_config("estado_caldera"))
        self.leer_ficheroHorarios()
        self.checkEstadoCheckCalefacion()
        self.actualiza_rele(gv.rele)

    def suceso(self):
        # check  programacion del la calefacion:
        if (time.time()-self.lastTimeCheckCalefa>10):
            self.checkEstadoCheckCalefacion()
            self.lastTimeCheckCalefa = time.time()
            if (self.dia_horarios != time.localtime().tm_wday):
                self.leer_ficheroHorarios()
 
    def reset(self):
        self.__init__()
        
    def checkEstadoCheckCalefacion(self):
        if(gv.estadoCalefa == 0):
            # estado Apagado.
            if (gv.rele !=0):
                self.actualiza_rele(0)

        elif(gv.estadoCalefa == 1):
            #estado  Encendido.
            self.check_temperatura()

        elif (gv.estadoCalefa == 2):
            # estado programado
            self.check_next_prog()

            hora=time.localtime()
            index = (hora.tm_hour*4) + (hora.tm_min/15)
            if 0 < index >=len(self.horarios):
                log(3, "checkEstadoCheckCalefacion: mal estado de index en leer estado %d " %(index) )
                return
            if (self.horarios[index]!="0"):
                self.check_temperatura()
            else:
                if (gv.rele !=0):
                   self.actualiza_rele(0)

    def check_next_prog(self):
        # estado programado
        segundos = time.time()
        hora=time.localtime()
        index = (hora.tm_hour*4) + (hora.tm_min/15)
        if 0 < index >=len(self.horarios):
            log(3, "check_next_prog: mal estado de index en leer estado %d " %(index) )
            return
        for i in range(index, len(self.horarios)-1):
            if (self.horarios[i]!="0"):
                gv.estadoCalefa_NextProg = segundos
                return
            else:
                 segundos += 900
        gv.estadoCalefa_NextProg = -1
 
    def check_temperatura(self):
        log(0, "Temperatura: %.2f Temperatura_Max %.2f " %(gv.temperatura , gv.temperatura_max ))
        if ((gv.temperatura + 0.2) < gv.temperatura_max) and (gv.rele==0):
                # temperatura menor y rele apagado.
                self.actualiza_rele(1)

        elif ((gv.temperatura - 0.2) > gv.temperatura_max) and (gv.rele==1):
                # temperatura mayor y rele encendido.
                self.actualiza_rele(0)
                
    def actualiza_rele(self, valor):
        iFile = file(self.RELE_FILE, 'w')
        iFile.write(str(valor))
        iFile.close()
        gv.lastTimeChageSomething = time.time()
        gv.rele = valor
        log(2, "Actulizado valor del rele a -%d- " %(valor) )
        
    def leer_ficheroHorarios(self):
        fichero = str(time.localtime().tm_wday +1) + ".txt"
        try:
            log(1, "Leer la temperatura del fichero %s..." %(self.FOLER_PROGRA +fichero) )
            iFile = file(self.FOLER_PROGRA +fichero, 'r')
            line = iFile.readline()
            line = line.replace("\n", "")
            iFile.close()        
            self.horarios = line.split(';')
            self.dia_horarios = time.localtime().tm_wday
        except:
            log(5, "imposible leer fichero %s" %(self.FOLER_PROGRA +fichero) )