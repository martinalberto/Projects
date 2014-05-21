#!/usr/bin/env python

import sys
import time, os
import os.path
import shutil

# -----------
# Constantes
# -----------
 
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
 

class clog:
	DEBUG_LEVEL=1
	LOGS_FILE= "/var/utemp/logs.log"
	
	def log(self, nivel, text):
		if (nivel<self.DEBUG_LEVEL):
			return 0			
		frame= sys._getframe(1)
		text_file= time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()) + ";"+ str(nivel) + ";"
		text_file+= "UTEMPER;"+ frame.f_code.co_filename.split('/')[-1] + ":" + str(frame.f_lineno) +" "+ text
		print text_file
		sys.stdout.flush()
		
		# save into file.
		File = file(self.LOGS_FILE, 'a')
		File.write(text_file)
		File.close()

class cread_config(object):

	CONFIG_FILE_LOCAL= "config/utemper.conf"
	CONFIG_FILE_REMOTE= "config/server/utemper.conf"
	CONFIG_FILE_SEND= "config/send/utemper.conf"
	
	def read_config (self, nombre_config):
		# read file local
		(tiempo_local, valor_local) = self.read_config_file(self.CONFIG_FILE_LOCAL,nombre_config )
		
		if (os.path.isfile(self.CONFIG_FILE_REMOTE)):
			(tiempo_remote, valor_remote) = self.read_config_file(self.CONFIG_FILE_REMOTE,nombre_config )
			if (tiempo_remote<tiempo_local):
				self.update_config_file(self.CONFIG_FILE_REMOTE, tiempo_local, nombre_config , valor_local)
				shutil.copy2(self.CONFIG_FILE_REMOTE, self.CONFIG_FILE_SEND)
				
			elif (tiempo_remote>tiempo_local):
				self.update_config_file(self.CONFIG_FILE_LOCAL, tiempo_remote, nombre_config , valor_remote)
				valor_local = valor_remote
				
		return valor_local
	def read_config_file (self, file, nombre_config):
		lines=[""]
		tiempo = 0
		valor = "-1"
		# read file 1
		try:
			f = open(file)
			lines = f.readlines()
			f.close()
		except:
			clog().log(4, "Imposible poder leer la configuracion -%s- del fichero %s " %(nombre_config, file) )
			
		for line in lines:
			if len(line.split(':')):
				(tiempo,config,valor)=line.split(':')
				if config.lower() == nombre_config.lower():
					return {int(tiempo), valor}
		return {tiempo, valor}
		
	def update_config_file (self, file, tiempo_new, nombre_config , valor_new):
		encontrado =False
		lines =[]
		new_line = str(tiempo_new) + ":" + nombre_config + ":" + valor_new + "\n"

		# read
		try:
			f = open(file)
			lines = f.readlines()
			f.close()
		except:
			clog().log(4, "Imposible poder leer la configuracion -%s- del fichero %s " %(nombre_config, file) )
			
		# process
		for numline in range(lines):
			if len(lines[numline].split(':')):
				(tiempo,config,valor)=lines[numline].split(':')
				if config.lower() == nombre_config.lower():
					lines[numline] = new_line
					encontrado = True					
		if (encontrado ==False):
			lines.lappend (new_line)
			
		# save
		try:
			f = open(file, "w")
			lines = f.writelines(lines)
			f.close()
		except:
			clog().log(5, "Imposible GUARDAR leer la configuracion del fichero %s " %file )
		return 1
		
class gv(object):
    
    # el tiempo
    tiempo_temp=-1
    tiempo_code=-1
    tiempo_estado=""
    tiempo_titulo=""
    hora_init_dia = time.strptime( "08:00 am", "%I:%M %p")
    hora_init_noche = time.strptime( "07:00 pm", "%I:%M %p")

    # temperatura.
    temperatura=22
    temperatura_max = 44

    #dia noche:
    noche=0
