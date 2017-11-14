#!/usr/bin/env python

#import RPi.GPIO as GPIO
import os, os.path
from utemper_public import *

class cUtemperLdr:

    lastTimeReadLdr = 0
    FILE_LDR = "/tmp/ldr.var"

    def __init__(self):
        gv.luz_OK = 0
        gv.luzValor =0
        log(0, "Init LDR OK")

    def suceso (self):
        if  (time.time()-self.lastTimeReadLdr > 30) :
            self.lastTimeReadLdr = time.time()
            result = os.path.isfile(self.FILE_LDR)
            if (result!= True):
                return
            try:
                file = open(self.FILE_LDR, "r")
                valor = file.readline()
                file.close()
                gv.luzValor = float(valor)
                if (gv.luzValor > 0):
                    gv.luz_OK = 1
                    log(0, "Hay valor LDR: "+ str(gv.luzValor))
                else:
                    log(0, "valor LDR: "+ str(gv.luzValor) +" MAL.")
            except:
                gv.luz_OK = 0
                log(3, "Error al leer el fichero: "+ self.FILE_LDR)
                self.lastTimeReadLdr = time.time()+60
