#!/usr/bin/env python

import urllib2, time
import glob, os
import xml.etree.ElementTree as ET

from utemper_public import *

class eltiempo:
	# tiempo
	WOEID=0
	CONF_FILE= "config/utemper.conf"
	WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'	
	lastTimeTiempo = 0
	
	#temp:	
	temp = False
	lastTimeTemp = 0
	sensorTemp = None
	
	def __init__(self):
		if self.int_tiempo()==1:
			log(1,"init int_tiempo OK")
			
		if self.int_temp()==1:
			self.temp=True
			log(1,"init read temperatura OK")
		else:
			self.temp=False
			log(1,"init read temperatura KO")
		
	def int_tiempo(self):
		self.WOEID = int(cread_config().read_config("WOEID"))
		if self.WOEID ==-1:
			gv.tiempo_OK = False
			return 0
		self.leer_tiempo()
		return 1
		
	def int_temp(self):
		try:
			from w1thermsensor import W1ThermSensor
			time.sleep(0.5)
			self.sensorTemp = W1ThermSensor()
			return 1
		except:
			log(3,("Imposible W1ThermSensor"))
			return 0
			
	def suceso(self):
		#leer tiempo

		if (time.time()-self.lastTimeTiempo>900) and (gv.tiempo_OK):
			self.lastTimeTiempo=time.time()
			self.leer_tiempo()
		elif (time.time()-self.lastTimeTiempo>300) and (gv.tiempo_OK == False):
			self.lastTimeTiempo=time.time()
			if self.int_tiempo()==1:
				log(1,"Read tiempo KO ->  OK Bien ")
				
		#leer temperatura
		if (time.time()-self.lastTimeTemp>30) and (self.temp):
			self.lastTimeTemp=time.time()
			result = self.leer_temperatura()
			if result==1:
			    gv.temperatura_error=0
			else:
			    gv.temperatura_error=1
		elif (time.time()-self.lastTimeTemp>300) and (self.temp== False):
			self.lastTimeTemp=time.time()
			if self.int_temp()==1:
				self.temp=True
				log(1,"Conseguimos iniciar read temperatura OK")
				
	def reset(self):
		self.__init__()
		
	def leer_tiempo(self):
		if self.WOEID<=0:
			log(4,("Error al leer tiempo WOEID <0 "))
			gv.tiempo_OK = False
			return 0
		try:
			log(1,("init leer_tiempo... "))
			data = urllib2.urlopen('http://weather.yahooapis.com/forecastrss?u=c&w=' + str(self.WOEID), timeout = 2).read()
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
			
			# wind speed
			ycondition = rss.find('channel/{%s}wind' % self.WEATHER_NS)
			gv.tiempo_speed = float(ycondition.get('speed'))
			
			# city 
			ycondition = rss.find('channel/{%s}location' % self.WEATHER_NS)
			gv.tiempo_City = ycondition.get('city')
			
			log(0," leer_tiempo  OK")
			gv.tiempo_OK = True
			return 1
		except:
			log(3,"Imposible poder acceder al tiempo.")
			gv.tiempo_OK = False
			return 0
			
	def leer_temperatura(self):
		log(0,"leer_temperatura...")
		temp_c=0
		count = 0
		try:
			temp_c = self.sensorTemp.get_temperature()
			if (temp_c>2 and temp_c<40):
					gv.temperatura = round(temp_c, 2)
					return 1
			return 0
		except:
			log(3,("Imposible leer temperatura "))
			return 0

	def read_temp_raw(self):
		f = open(self.device_file, 'r')
		lines = f.readlines()
		f.close()
		return lines
