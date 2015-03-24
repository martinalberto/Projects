#!/usr/bin/env python

#import RPi.GPIO as GPIO

import time, os


import utemper_tiempo
from utemper_public import *
import utemper_screen
import utemper_check_estados
import utemper_InterfaceServer
import utemper_check_temperatura
import utemper_report
import utemper_Scan_Ips
import utemper_ldr

#import utemper_wifi
		
def main():
	
	salir=1
	
	# Init Clases.
	cutemper_tiempo = utemper_tiempo.eltiempo()
	cutemper_screen = utemper_screen.cScreen()
	cutemper_Check_estados = utemper_check_estados.cCheck_estados()
	cutemper_Check_temperatura = utemper_check_temperatura.cCheck_temperatura()
	cinterfaceServer = utemper_InterfaceServer.cInterfaceServer()
	cutemper_report = utemper_report.calssReport()
	cutemper_ldr = utemper_ldr.cUtemperLdr()
	cutemper_Scan_Ips =  utemper_Scan_Ips.cUtemperCheckIp()
	log(1,"##### Init Utemper OK ####")
	# bucle
	while(salir):
		cutemper_tiempo.suceso()
		#log(1," cutemper_tiempo OK")
		cutemper_Check_estados.suceso()
		#log(1," cutemper_Check_estados OK")
		cutemper_Check_temperatura.suceso()
		#log(1," cutemper_Check_temperatura OK")
		cinterfaceServer.suceso()
		cutemper_report.suceso()
		cutemper_screen.suceso()
		cutemper_ldr.suceso()
		cutemper_Scan_Ips.suceso()
		#log(1," cutemper_screen OK")
		#salir=0
		time.sleep(0.3)
		if (gv.reset_class!=0):
			log(2,"RESET utemper Clase %d...." %gv.reset_class)
			cutemper_tiempo.reset()
			cutemper_screen.reset()
			cinterfaceServer.reset()
			cutemper_Check_estados.reset()
			cutemper_Check_temperatura.reset()
			log(2,"RESET utemper OK")
			gv.reset_class = 0
	# exit
	log(1,"Salimos del Utemper OK")
	
def fin_program():
	log(1,"##### Cerrando Utemper OK ####")
	
if __name__ == "__main__":
    main()
