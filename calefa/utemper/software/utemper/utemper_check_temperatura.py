#!/usr/bin/env python

import sys
import time, os

class cCheck_temperatura:

	CONF_FILE="config/utemper.conf"

	def __init__():
		# read config value:
		leer_conf_temp()
		checkTemperatura()
		actualiza_rele(gv.rele)

	def leer_conf_temp():
                try:
                        f = file(self.CONF_FILE, 'r')
                        lines = f.readlines()
                        f.close()
                        for line in lines:
				result = scanf(lines, "%d:%s:%f", segActualizacion, nombre, valor)
                                if (result==3) and (nombre = "temperatura" ):
                             		gv.temperatura_max= valor
   	
                except:
                        clog().log(3,"Imposible leer config 'temp'")
                        return 0

	
	def suceso():
		# check noche:
                if (time.time()-self.lastTimeNoche>6):
                        checkTemperatura()
                        self.lastTimeNoche = time.time()

	def checkTemperatura():
		
		if(gv.estadoCalefa == 0):
			# estado Apagado.
			if (gv.rele !=0):
				actualiza_rele(0)

		elif(gv.estadoCalefa == 1):
			#estado  Encendido.

			if ((gv.temperatura - 0.1) < gv.temperatura_max) and (gv.rele==0):
				# temperatura menor y rele apagado.
				actualzia_rele(1)

			elif ((gv.temperatura + 0.1) > gv.temperatura_max) and (gv.rele==1):
                                # temperatura mayor y rele encedido.
                                actualzia_rele(0)

		elif (gv.estadoCalefa == 2):
			# estado programado
