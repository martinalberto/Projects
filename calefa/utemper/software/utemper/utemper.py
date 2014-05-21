#!/usr/bin/env python

#import RPi.GPIO as GPIO

import time, os


import utemper_tiempo
from utemper_public import *
import utemper_screen
#import utemper_wifi
		
def main():
	
	salir=1
	
	# Init Clases.
	cutemper_tiempo = utemper_tiempo.eltiempo()
	cutemper_screen = utemper_screen.cScreen()
	clog().log(1,"Init Utemper OK")
	
	# bucle
	while(salir):
		cutemper_tiempo.suceso()
		
		print gv.tiempo_temp
		print gv.tiempo_code
		salir=0
		
	# exit
	clog().log(1,"Salimos del Utemper OK")
	
def fin_program():
	print "asd"

if __name__ == "__main__":
    main()
