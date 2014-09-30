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
	cutemper_Check_estados = utemper_check_estados.cCheck_estados()
	cutemper_Check_temperatura = utemper_check_temperatura.cCheck_temperatura()
	
	clog().log(1,"##### Init Utemper OK ####")
	
	# bucle
	while(salir):
		cutemper_tiempo.suceso()
		#clog().log(1," cutemper_tiempo OK")
		cutemper_screen.suceso()
		#clog().log(1," cutemper_Check_estados OK")
		cutemper_Check_estados.suceso()
		#clog().log(1," cutemper_Check_estados OK")
		cutemper_Check_temperatura.suceso()
		#clog().log(1," cutemper_Check_temperatura OK")

		#salir=0
		time.sleep(0.3)
		
		if (gv.reset_class==1):
			clog().log(2,"RESET utemper....")
			cutemper_tiempo.reset()
			cutemper_screen.reset()
			cutemper_Check_estados.reset()
			cutemper_Check_temperatura.reset()
			clog().log(2,"RESET utemper OK")
			gv.reset_class = 0
	# exit
	clog().log(1,"Salimos del Utemper OK")
	
def fin_program():
	print "Saliendo de Utemper."
	clog().log(1,"##### Cerrando Utemper OK ####")
	
if __name__ == "__main__":
    main()