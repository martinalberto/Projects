#!/usr/bin/python
import getopt
import sys, os
import string
import time, datetime
from time import sleep

import temperature
import report
import TiemposCalendar

#Rele and led.
import RPi.GPIO as GPIO

class ClassRele:
    RELE = 7
    def __init__(self):
        self.statusRele=GPIO.HIGH
        self.lastTime=0
        self.errores_rele=0
        
        print "empezar_rele...."
        GPIO.setup(ClassRele.RELE, GPIO.OUT)
        GPIO.output(ClassRele.RELE, GPIO.HIGH)
        sys.stderr.write("empezar_rele %d [OK] todos a GPIO.HIGH\n" %(ClassRele.RELE))

    def suceso(self, Estado):
        if (Estado!=self.statusRele):  
            self.statusRele=Estado
            try:
                GPIO.output(ClassRele.RELE, Estado)
                errores_rele=0
            except:
                sys.stderr.write( "ERRROR!!! No se puede.num_Rele\n" )
                errores_rele+=1
                sleep (33)
                
    
class ClassLed:
    STATUSLED=16 
    
    def __init__(self):      
        self.statusLed=GPIO.LOW
        self.lastTime=time.time()
        GPIO.setup(ClassLed.STATUSLED, GPIO.OUT)
        GPIO.output(ClassLed.STATUSLED, GPIO.LOW)
        
    def suceso(self, Estado):
    
        if (self.statusLed == GPIO.LOW) and  (time.time()-self.lastTime>(1.1-(0.4*Estado))) :
               GPIO.output(ClassLed.STATUSLED, GPIO.LOW)
               GPIO.output(ClassLed.STATUSLED, GPIO.HIGH)               
               #saveValues:
               self.old_time=time.time()
               self.statusLed = GPIO.HIGH
               
        elif (self.statusLed == GPIO.HIGH) and  (time.time()-self.lastTime>(1.1-(0.4*Estado))) :
               GPIO.output(ClassLed.STATUSLED, GPIO.HIGH)
               GPIO.output(ClassLed.STATUSLED, GPIO.LOW)               
               #saveValues:
               self.old_time=time.time()
               self.statusLed = GPIO.LOW


def startLog():
    sys.stderr.write('-------------------------------------------\n')
    sys.stderr.write('%s Started Log\n' %(datetime.datetime.now()) )

def main():
    
    salir=1

    #init.    
    startLog()

    GPIO.setmode(GPIO.BCM)
    rele=ClassRele()
    led=ClassLed()
    DHT_Temp = temperature.ClassTemp()
    horarios = TiemposCalendar.classHorrarios()
    ReportTemp = report.calssReport()
    
    sys.stderr.write('%s Started bucle.\n' )
    while (salir):
        #loop.
                
        ValueTemp = DHT_Temp.SucesoTemp()
        ahora = horarios.suceso()
        
        if (ValueTemp[1] < ahora):
            encendido = 1
        else:
            encendido = 0
        
        led.suceso(encendido)
        rele.suceso(encendido)
        
        ReportTemp.suceso([ValueTemp[1], ValueTemp[2],ahora,encendido ])
        
        sleep(0.3)

if __name__ == '__main__':
  main()
