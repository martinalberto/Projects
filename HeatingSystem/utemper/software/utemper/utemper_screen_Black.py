#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from subprocess import call
from utemper_public import *

class cScreenBlack:

    ConfScreenBlack = 0
    InitOk = False
    lastTimePowerONScreen = time.time()
    lastStatusScreen = -1 # 1 = Encendido 0 = apagado.
    botonScreen_OFF = 0
    
    def __init__(self):
        try:
            # Encendemos la pantalla:
            self.ScreenON()
            self.ConfScreenBlack = int(cread_config().read_config("PantallNegra"))
            if(self.ConfScreenBlack == -1):
                log(4,"Error: Imposible leer 'PantallNegra' Conf: Simepre encendida!")
                self.InitOk= False
                return
            if not (os.path.isfile("/sys/class/gpio/gpio252/value")):
                log(4,"INIT Error: fichero /sys/class/gpio/gpio252/value no existe no finccona pantalla negra.")                
                self.InitOk= False
                return
            self.InitOk= True
            self.suceso()
            log(1,"iniciar la pantalla Negra OK")
        except:
            log(4,"Imposible iniciar Pantalla Negra")
            self.InitOk= False
         
    def suceso(self):
        if not (self.InitOk):
            return
        if (self.botonScreen_OFF == 1 ):
            return # Boton Pulsado. NO hacemos caso de los estados.
            
        elif(self.ConfScreenBlack == 0): # siempre encendido.
            self.ScreenON()
            
        elif (self.ConfScreenBlack == 1) and (gv.noche==0): # encendido de día. y es de dia
            self.ScreenON()
            
        elif (self.ConfScreenBlack == 1) and (gv.noche==1): # encendido de día. y es de Noche # puede apagarse.
            if (time.time()-self.lastTimePowerONScreen > 200 ):
                self.ScreenOFF() # Apagamos.
                
        elif (self.ConfScreenBlack == 2):
            if (time.time()-self.lastTimePowerONScreen > 200 ):
                self.ScreenOFF() # Apagamos.
        else:
            log(5,"Error: ConfScreenBlack con estado Imposible %d", self.ConfScreenBlack)
            self.InitOk= False
            
    def reset(self):
        log(2,"reset cScreenBlack...")
        NewConfScreenBlack = int(cread_config().read_config("PantallNegra"))
        if(self.ConfScreenBlack != NewConfScreenBlack):
            self.__init__() # La configuracion ha cambiado Iniciamos todo de nuevo.
            
        if (gv.reset_class == 1): # Encedemos la pantalla.
            log(2,"gv.reset_class == 1: ENCENDEMOS LA PANTALLA.")
            self.lastStatusScreen = -1# Se resetea si o si.
            return self.ScreenON()
        return False

    def ScreenON(self):
        if (self.lastStatusScreen != 1):
            log(1,"Encendemos la pantalla ON")
            reslut = os.system("echo '1' > /sys/class/gpio/gpio252/value")
            self.lastStatusScreen = 1
            self.botonScreen_OFF  = 0
            self.lastTimePowerONScreen = time.time()
            return True
        return False

    def ScreenOFF(self):
        if (self.InitOk):
            if (self.lastStatusScreen != 0):
                log(1,"Apagamos la pantalla OFF")
                reslut = os.system("echo '0' > /sys/class/gpio/gpio252/value")
                self.lastStatusScreen = 0
        else:
            log(3,"Pantalla negra NO inicalizacida NO se apaga.")
    
    def IsScreenON(self):
        if (self.lastStatusScreen == 1):
            return True
        else:
            return False

    def BotonScreenOFF(self):
        self.botonScreen_OFF = 1
        log(1,"BotonScreenOFF: Han pulsado a BotonScreenOFF.")
        self.ScreenOFF()