#!/usr/bin/env python

import sys
import time, os
import shutil
import os.path

# -----------
# Constantes
# -----------
 
class clog:
    DEBUG_LEVEL= -1
    LOGS_FILE= "/var/utemp/logs.log"
    # gris \033[91m
    COLORES= ['\033[94m','\033[0m',  '\033[92m', '\033[93m','\033[91m','\033[93m']
    ENDC ='\033[0m'
    def log(self, nivel, text):
        if (nivel<self.DEBUG_LEVEL):
            return 0            
        frame= sys._getframe(1)
        text_file= time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()) + ";"+ str(nivel) + ";"
        text_file+= "UTEMPER;"+ frame.f_code.co_filename.split('/')[-1] + ":" + str(frame.f_lineno) +" "+ text
        print self.COLORES[nivel] + text_file + self.ENDC
        sys.stdout.flush()
        
        
        return 
        
        # save into file.
        File = file(self.LOGS_FILE, 'a')
        File.write(text_file)
        File.close()

class cread_config(object):

    CONFIG_FILE_LOCAL= "config/utemper.conf"
    CONFIG_FILE_SEND= "config/send/utemper.conf"
    
    def read_config (self, nombre_config):
        # read file local
        (tiempo_local, valor_local) = self.read_config_file(self.CONFIG_FILE_LOCAL,nombre_config )
        clog().log(1, "Leida el valor -%s- para la config -%s- " %(valor_local, nombre_config) )
        return valor_local
	
    def read_config_file (self, file, nombre_config):
        lines=[""]
        encontrado = False
        tiempo = 0 
        nombre=""
        valor="-1"
        
        # read
        try:
            f = open(file)
            lines = f.readlines()
            f.close()
        except:
            clog().log(4, "Imposible poder leer la configuracion -%s- del fichero %s " %(nombre_config, file) )
            
        # check.
        for line in lines:
            if (len(line.split(':'))==3):
                line = line.replace("\n", "")
                (stiempo, nombre, valor) = line.split(':')
                tiempo = int(stiempo)
                if (nombre.lower() == nombre_config.lower()):
                    encontrado = True
                    return (tiempo, valor)                
        return (0, "-1")

    def write_config_file (self,  data):
        # write
        try:
            f = open(self.CONFIG_FILE_LOCAL, "w")
            lines = f.writelines(data)
            f.close()
        except:
            clog().log(4, "Imposible poder escribir la nueva configuracion en fichero %s " %( self.CONFIG_FILE_LOCAL) )
            return 0
        gv.lastTimeChageSomething = time.time()
        return 1
		
    def update_config_file (self, nombre_config , valor_new):
        encontrado =False
        lines =[]
        tiempo_new = long(time.time())
        new_line = str(tiempo_new) + ":" + nombre_config + ":" + valor_new + "\n"

        # read
        try:
            f = open(self.CONFIG_FILE_LOCAL)
            lines = f.readlines()
            f.close()
        except:
            clog().log(4, "Imposible poder leer la configuracion -%s- del fichero %s " %(nombre_config, self.CONFIG_FILE_LOCAL) )
            return

        # process
        new_lines =[]
        for linen in lines:
            if (len(linen.split(':'))==3):
                line = linen.replace("\n", "")
                (stiempo, nombre, valor) = line.split(':')
                if (nombre.lower() == nombre_config.lower()):
                    new_lines.append(new_line)
                    encontrado = True
                else:
                    new_lines.append(linen)
            else:
                new_lines.append(linen)
        if (encontrado ==False):
            new_lines.lappend (new_line)
            
        # save
        try:
            f = open(self.CONFIG_FILE_LOCAL, "w")
            f.writelines(new_lines)
            f.close()
        except:
            clog().log(5, "Imposible GUARDAR leer la configuracion del fichero %s " %self.CONFIG_FILE_LOCAL )
            return 

        # copy to send data.
        try:
            shutil.copy2(self.CONFIG_FILE_LOCAL, self.CONFIG_FILE_SEND)
            clog().log(0, "Configuracion copiada a  %s " %self.CONFIG_FILE_SEND )
        except:
            clog().log(5, "Imposible copiar de %s  a %s" %(self.CONFIG_FILE_LOCAL, self.CONFIG_FILE_SEND) )
            gv.upload_config = False
            return

        clog().log(2, "Configuracion Actualizada fichero  %s " %self.CONFIG_FILE_LOCAL )
        gv.upload_config = True
        gv.lastTimeChageSomething = time.time()
        return 1
        
class gv(object):
    
    # number equipo.
    number_equipo =0
    
    # el tiempo
    tiempo_temp=-1
    tiempo_code=3200
    tiempo_estado=""
    tiempo_titulo=""
    hora_init_dia = time.strptime( "08:00 am", "%I:%M %p")
    hora_init_noche = time.strptime( "07:00 pm", "%I:%M %p")

    # temperatura.
    temperatura=30
    temperatura_max = 50
    temperatura_error=1

    #dia noche:
    noche=0
    
    # rele
    rele=0
    tiempo_espera=0
    
    #internet y wifi
    internet=0
    wifi_estado = 0
    wifi_ip = ""
    
    # screen
    screen_widht = 320
    screen_height = 240

    # reset todas las clases.
    reset_class = 0

    #config:
    upload_config = True
    lastTimeChageSomething = 0 