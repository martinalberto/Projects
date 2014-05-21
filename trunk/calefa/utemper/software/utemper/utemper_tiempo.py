#!/usr/bin/env python

import urllib, time
import xml.etree.ElementTree as ET

from utemper_public import *



class eltiempo:
	# tiempo
	tiempo = False
	WOEID=0
	CONF_FILE="config/utemper.conf"
	WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'	
	lastTimeTiempo=0
	
	#temp:
	temp = False
	READ_TEMP_FILE = "/tmp/temp.var"
	lastTimeTemp=0
	
	def __init__(self):
		clog().log(1,"init int_tiempo OK")
		if self.int_tiempo()==1:
			self.tiempo=True
		clog().log(1,"init read temperatura OK")
		if self.int_temp()==1:
			self.temp=True
			
	def int_tiempo(self):		
		self.WOEID = int(cread_config().read_config("WOEID"))
		if self.WOEID ==-1:
			return 0
		self.leer_tiempo()
		return 1
		
	def int_temp(self):
		try:
			f = file(self.READ_TEMP_FILE, 'r')
			gv.temperatura = float(f.readlines())
			f.close()
		except:
			clog().log(3,("Imposible leer temperatura del fichero "+ self.READ_TEMP_FILE))
			return 0			
		return 1

	def suceso(self):
		#leer tiempo
		if (time.time()-self.lastTimeTiempo>4000) and (self.tiempo):
			self.lastTimeTiempo=time.time()
			self.leer_tiempo()
			
		#leer temperatura
		if (time.time()-self.lastTimeTemp>5) and (self.temp):
			self.lastTimeTemp=time.time()
			self.leer_temperatura()
			
	def leer_tiempo(self):
		if self.WOEID<=0:
			clog().log(4,("Error al leer tiempo WOEID <0 "))
			return 0
		#try:
			clog().log(1,("init leer_tiempo... "))
			data = urllib.urlopen('http://weather.yahooapis.com/forecastrss?u=c&w=' + str(self.WOEID)).read()
			rss = ET.fromstring(data)
			ycondition = rss.find('channel/item/{%s}condition' % self.WEATHER_NS)
			gv.tiempo_temp = int(ycondition.get('temp'))
			gv.tiempo_code = int(ycondition.get('code'))
			gv.tiempo_estado = rss.findtext('text')
			gv.tiempo_titulo = rss.findtext('channel/title')
		
			# dia y noche.
			ycondition = rss.find('channel/{%s}astronomy' % self.WEATHER_NS)
			gv.hora_init_dia = time.strptime(ycondition.get('sunrise'), "%I:%M %p")
			gv.hora_init_noche = time.strptime(ycondition.get('sunset'), "%I:%M %p")
			return 1
		#except:
			clog().log(3,"Imposible poder acceder al tiempo.")
			return 0
			
	def leer_temperatura(self):
		clog().log(0,"leer_temperatura...")
		try:
			f = file(self.READ_TEMP_FILE, 'r')
			gv.temperatura = float(f.readlines())
			f.close()
		except:
			clog().log(3,("Imposible leer temperatura del fichero "+ self.READ_TEMP_FILE))
			return 0			
		return 1
