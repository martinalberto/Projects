#!/usr/bin/python
from __future__ import print_function
from wifi import Cell, Scheme

from utemper_public import *

class  cwifi (object):
	conexion = ""
	def __init__(self):	
		# get all cells from the air
		try:
			cread_config_1=cread_config()
			gv.wifissid = cread_config_1.read_config("wifi_ssid")
			gv.wificode = cread_config_1.read_config("wifi_code")
		except:
			gv.wifi = 0
	
	def connect (self):
		# buscamos el ssid:
		cell = Cell.where("wlan0", lambda cell: cell.ssid.lower() == gv.wifissidc.lower())
		if ( cell ==[]):
			clog().log(5, "Imposible Encontrar la wifissid  %s " %gv.wifissid )
			gv.wifi_connect = 0
			return 0
		
		if (Scheme.find("wlan0", gv.wifissid) == None ):
			# se guarda:
			scheme = Scheme.for_cell("wlan0",gv.wifissid, cell[0], gv.wificode )			
			scheme.save()
			
		# conectamos.		
		scheme = Scheme.find("wlan0", gv.wifissid)
		try:
			 self.conexion = scheme.activate()
		except:
			clog().log(5, "Imposible conecar a  la red  %s " %gv.wifissid )

	def check_wifi(self):
	# por terminar.
	
		pass
