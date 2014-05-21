#!/usr/bin/env python

import urllib, time
import xml.etree.ElementTree as ET

from utemper_public import *

class cCheck_estados:
	lastTimeNoche=0

	def __init__(self):
		pass
	
	def suceso (self):
		# check noche:
		if (time.time()-self.lastTimeNoche>600):
			self.checkNoche()
			self.lastTimeNoche = time.time()

	def checkNoche(self):		
		gv.hora_init_dia
		ahora= time.strptime( time.strftime("%I:%M %p", time.localtime()), "%I:%M %p")
		if (gv.hora_init_dia < ahora < gv.hora_init_noche):
			gv.noche=0 # dia
		else:   gv.noche=1 # noche

