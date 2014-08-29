#!/usr/bin/env python

#import RPi.GPIO as GPIO

import time, os


import utemper_tiempo
from utemper_public import *
import utemper_screen
import utemper_check_estados
import utemper_check_temperatura

#import utemper_wifi
		
def main():
	
	salir=1
	
	# Init Clases.
	cutemper_tiempo = utemper_tiempo.eltiempo()
	cutemper_screen = utemper_screen.cScreen()
	cutemper_cCheck_estados = utemper_check_estados.cCheck_estados()
	cutemper_cCheck_temperatura = utemper_check_temperatura.cCheck_temperatura()
	
	clog().log(1,"##### Init Utemper OK ####")
	
	# bucle
	while(salir):
		cutemper_tiempo.suceso()
		#clog().log(1," cutemper_tiempo OK")
		cutemper_screen.suceso()
		#clog().log(1," cutemper_cCheck_estados OK")
		cutemper_cCheck_estados.suceso()
		#clog().log(1," cutemper_cCheck_estados OK")
		cutemper_cCheck_temperatura.suceso()
		#clog().log(1," cutemper_cCheck_temperatura OK")

		#salir=0
		time.sleep(0.3)
	# exit
	clog().log(1,"Salimos del Utemper OK")
	
def fin_program():
	print "asd"

if __name__ == "__main__":
    main()
