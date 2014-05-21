#!/usr/bin/env python

import sys
import time, os
from utemper_public import *

class cCheck_temperatura:
	lastTimeNoche=0
	CONF_FILE="config/utemper.conf"

	def __init__(self):
		# read config value:
		gv.temperatura_max = int (cread_config().read_config("temperatura"))
		gv.estadoCalefa = int (cread_config().read_config("estado_caldera"))
		self.checkTemperatura()
		self.actualiza_rele(gv.rele)

	def suceso(self):
		# check noche:
                if (time.time()-self.lastTimeNoche>6):
                        self.checkTemperatura()
                        self.lastTimeNoche = time.time()

	def checkTemperatura(self):
		
		if(gv.estadoCalefa == 0):
			# estado Apagado.
			if (gv.rele !=0):
				self.actualiza_rele(0)

		elif(gv.estadoCalefa == 1):
			#estado  Encendido.

			if ((gv.temperatura - 0.1) < gv.temperatura_max) and (gv.rele==0):
				# temperatura menor y rele apagado.
				self.actualiza_rele(1)

			elif ((gv.temperatura + 0.1) > gv.temperatura_max) and (gv.rele==1):
                                # temperatura mayor y rele encedido.
                                actualiza_rele(0)

		elif (gv.estadoCalefa == 2):
			# estado programado
			pass
			
	def actualiza_rele(self, valor):
		pass