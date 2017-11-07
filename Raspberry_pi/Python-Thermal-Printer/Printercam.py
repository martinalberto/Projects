#!/usr/bin/python

# Main script for Adafruit Internet of Things Printer 2.  Monitors button
# for taps and holds, performs periodic actions (Twitter polling by default)
# and daily actions (Sudoku and weather by default).
# Written by Adafruit Industries.  MIT license.
#
# MUST BE RUN AS ROOT (due to GPIO access)
#
# Required software includes Adafruit_Thermal, Python Imaging and PySerial
# libraries. Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import RPi.GPIO as GPIO

LedFlash = 10

LedRojo = 17
LedAzul = 3
LedVerde = 2
buttonPin = 24 

size = 512, 384


def photo_callback(tipo):
   num =  str(int(random.random()*100000))
   
   #Camara:
   camera = picamera.PiCamera()
   camera.resolution = (512, 384)
   camera.brightness = 60
   #camera.rotation = 90
   camera.framerate = 15
   #camera.contrast = 70
   camera.exposure_mode ="auto"
   camera.awb_mode = "auto"
   #camera.awb_mode='fluorescent'
   if (tipo == 1):
    camera.image_effect = 'colorbalance'
    print ("colorbalance")
   else:
	 camera.image_effect = 'watercolor'
    
   GPIO.output(LedFlash, 1)
   camera.capture("../ImgCapture/image"+num+".bmp")
   GPIO.output(LedFlash, 0)
   
   camera.close()
   
   printer.wake() # Despertamos!
   
   imagen = Image.open("../ImgCapture/image"+num+".bmp")
   if (len(imagen.histogram())<400):
      setLed(True, False, False)
      printer.print("Error Campture Foto.")
      time.sleep(4)
      return
   # Cambiamos tamano
   imagen = imagen.resize(size, Image.ANTIALIAS)
   imagen = imagen.convert('L', dither=0)
   imagen = to_pil(cca.max_white(from_pil(imagen))) # https://github.com/shunsukeaihara/colorcorrect
   imagen.save("../ImgCorrect/image"+num+".bmp")
   # Convertimos en blancos y negros.
   imagen = imagen.convert('1', dither=1)
   # Giramos
   imagen = imagen.transpose(2)
   imagen.save("../ImgPrint/image"+num+".bmp")
   
   #Imprimimos!!
   printer.feed(1)
   printer.printImage(imagen, True)
   printer.feed(3)
   
def setLed ( LRojo, LVerde, LAzul):

   GPIO.output(LedRojo, not(LRojo))
   GPIO.output(LedVerde, not(LVerde))
   GPIO.output(LedAzul, not(LAzul))

#######################################################################
#              1.- Inicio.
#######################################################################
GPIO.setmode(GPIO.BCM)
GPIO.setup(LedRojo, GPIO.OUT) ## GPIO 2 como salida
GPIO.setup(LedAzul, GPIO.OUT) ## GPIO 3 como salida
GPIO.setup(LedVerde, GPIO.OUT) ## GPIO 4 como salida
GPIO.setup(LedFlash, GPIO.OUT) 

GPIO.setup(buttonPin, GPIO.IN) ## GPIO como Entrada

#Start:
setLed(True, False, False)

import picamera
from Adafruit_Thermal import *
import subprocess, time, socket, os
import time 
import random
from PIL import Image
import colorcorrect.algorithm as cca
from colorcorrect.util import from_pil, to_pil

#Impresora:
printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
time.sleep(0.5)
try:
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.connect(('8.8.8.8', 0))
   printer.print('Mi IP es ' + s.getsockname()[0])
   printer.feed(2)
except:
   printer.feed(1)
   
printer.sleep()

########################################################################
#             2.- Bucle.
########################################################################

while(1):

   # Wait change   
   time.sleep(0.2)
   #check botton.
   if( GPIO.input(buttonPin) ==1 ):
      setLed(False, False, False)
      timeStart = time.time()
      while(1):
         time.sleep(0.1)
         if( GPIO.input(buttonPin) ==0 ):
            setLed(False, False, True)
            if (time.time()- timeStart > 7):
                  print ("Apagamos...")
                  setLed(True, False, False)
                  try:
                     printer.print("Bye, bye")
                     printer.feed(3)
                  except:
                     print("Error goodbye")
                  subprocess.call("sync")
                  subprocess.call(["sudo","shutdown", "-h", "now"])
                  
            elif (time.time()- timeStart > 3):
                  print ("Foto...")
                  photo_callback(2)
            elif (time.time()- timeStart > 0.4):
                  print ("Foto...")
                  photo_callback(1)
                  
            setLed(False, False, False)    
            break
                     
   # Change Color.
   print 
   if (time.time()%2 > 1):
      setLed(False, False, False)
   else:
      setLed(False, True, False)

