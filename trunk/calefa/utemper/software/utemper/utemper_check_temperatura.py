#!/usr/bin/env python

import sys
import time, datetime, os
import RPi.GPIO as GPIO
from utemper_public import *

class cCheck_temperatura:
    lastTimeCheckCalefa=0
    RELE_FILE="/tmp/rele.var"
    FOLER_PROGRA = "config/"
    tiempo_rele = 0
    dia_horarios = 0
    horarios=[]
    Pin_RELE=0
    def __init__(self):
        # read config value:
        gv.temperatura_max = float (cread_config().read_config("temperatura"))
        if(gv.temperatura_max == -1):
            log(5, "ERROR INIT : Imposible leer valor Temperatura Max suponemos 18.") 
            gv.temperatura_max = 18.0
        gv.estadoCalefa = int (cread_config().read_config("estado_caldera"))
        if(gv.temperatura_max == -1):
            log(5, "ERROR INIT : Imposible leer valor estado_caldera suponemos 0.") 
            gv.estadoCalefa = 0
        self.Pin_RELE = int (cread_config().read_config("Pin_RELE"))
        if(self.Pin_RELE == -1):
            log(5, "ERROR INIT : Imposible leer valor 'Pin_RELE' suponemos 3.") 
            self.Pin_RELE = 3
        self.leer_ficheroHorarios()
        self.checkEstado()
        
        #Rele Config.
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Pin_RELE, GPIO.OUT)
        GPIO.output(self.Pin_RELE, GPIO.LOW)
        
        self.actualiza_rele(gv.rele)
        log(1, "Init Check Temperatura OK") 

    def suceso(self):
        # check  programacion del la calefacion:
        if (time.time()-self.lastTimeCheckCalefa>5):
            if (self.dia_horarios != time.localtime().tm_wday):
                self.leer_ficheroHorarios()
            self.checkEstado()
            self.lastTimeCheckCalefa = time.time()
 
    def reset(self):
        self.__init__()
        
    def checkEstado(self):
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
                log(3, "checkEstado: mal estado de index en leer estado %d " %(index) )
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
		
        if valor == 1: # fix valor si hay error.
            valor_pin = GPIO.HIGH
        else:
            valor_pin = GPIO.LOW            
        GPIO.output(self.Pin_RELE, valor_pin)
        if GPIO.input(self.Pin_RELE) != valor_pin:
            log(5, "ERROR RELE: Imposible actualizar RELE el pin: " + str(self.Pin_RELE) + " al valor: " + str(valor))
            return
        gv.lastTimeChageSomething = time.time()
        gv.rele = valor
        log(2, "Actulizado valor del rele a -%d- " %(valor) )
        
    def leer_ficheroHorarios(self):
        fichero = str(time.localtime().tm_wday +1) + ".txt"
        try:
            log(1, "Leer la temperatura del fichero %s..." %(self.FOLER_PROGRA + fichero))
            iFile = file(self.FOLER_PROGRA +fichero, 'r')
            line = iFile.readline()
            line = line.replace("\n", "")
            iFile.close()        
            self.horarios = line.split(';')
            self.dia_horarios = time.localtime().tm_wday
        except:
            log(5, "imposible leer fichero %s" %(self.FOLER_PROGRA +fichero) )