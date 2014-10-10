#!/usr/bin/env python

import urllib, time
import glob, os
import xml.etree.ElementTree as ET

from utemper_public import *

class eltiempo:
	# tiempo
	tiempo = False
	WOEID=0
	CONF_FILE= "config/utemper.conf"
	WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'	
	lastTimeTiempo=0
	
	#temp:
	
	temp = False
	lastTimeTemp=0
	
	def __init__(self):
		clog().log(1,"init int_tiempo OK")
		if self.int_tiempo()==1:
			self.tiempo=True
		
		if self.int_temp()==1:
			self.temp=True
			clog().log(1,"init read temperatura OK")
		else:
			self.temp=False
			clog().log(1,"init read temperatura KO")
		
	def int_tiempo(self):		
		self.WOEID = int(cread_config().read_config("WOEID"))
		if self.WOEID ==-1:
			return 0
		self.leer_tiempo()
		return 1
		
	def int_temp(self):
		try:
			os.system('modprobe w1-gpio')
			os.system('modprobe w1-therm')
			base_dir = '/sys/bus/w1/devices/'
			device_folder = glob.glob(base_dir + '10*')[0]
			self.device_file = device_folder + '/w1_slave'
			return 1
		except:
			clog().log(3,("Imposible modprobe w1-gpio y w1-therm "))
			return 0
			
	def suceso(self):
		#leer tiempo

		if (time.time()-self.lastTimeTiempo>900) and (self.tiempo):
			self.lastTimeTiempo=time.time()
			self.leer_tiempo()
			
		#leer temperatura
		if (time.time()-self.lastTimeTemp>6) and (self.temp):
			self.lastTimeTemp=time.time()
			result = self.leer_temperatura()
			if result==1:
			    gv.temperatura_error=0
			else:
			    gv.temperatura_error=1
	
	def reset(self):
		self.__init__()
		
	def leer_tiempo(self):
		if self.WOEID<=0:
			clog().log(4,("Error al leer tiempo WOEID <0 "))
			return 0
		try:
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
			clog().log(0," leer_tiempo  OK")
			return 1
		except:
			clog().log(3,"Imposible poder acceder al tiempo.")
			return 0
			
	def leer_temperatura(self):
		clog().log(1,"leer_temperatura...")
		temp_c=0
		count = 0
		try:		
			lines = self.read_temp_raw()
			while lines[0].strip()[-3:] != 'YES':
				time.sleep(0.2)
				lines = self.read_temp_raw()
				count += 1
				clog().log(1,"count ++")
				if (count>4):
					clog().log(3,("Imposible leer temperatura count > 4"))
					break
			equals_pos = lines[1].find('t=')
			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				#temp_f = temp_c * 9.0 / 5.0 + 32.0
				if (temp_c>2 and temp_c<40):
					gv.temperatura = temp_c
					return 1
			return 0
		except:
			clog().log(3,("Imposible leer temperatura "))
			return 0

		
	def read_temp_raw(self):
		f = open(self.device_file, 'r')
		lines = f.readlines()
		f.close()
		return lines
