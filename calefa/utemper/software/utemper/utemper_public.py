#!/usr/bin/env python

import sys
import time, os
import shutil
import os.path

# -----------
# Constantes
# -----------


LOGS_DEBUG_LEVEL= -1
LOGS_FILE= "/var/utemp/logs.log"
# gris \033[91m
LOGS_COLORES= ['\033[94m','\033[0m',  '\033[92m', '\033[93m','\033[91m','\033[93m']
LOGS_ENDC ='\033[0m'
def log(nivel, text):
    if (nivel<LOGS_DEBUG_LEVEL):
        return 0
    frame= sys._getframe(1)
    text_file= time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()) + ";"+ str(nivel) + ";"
    text_file+= frame.f_code.co_filename.split('/')[-1] + ":" + str(frame.f_lineno) +" "+ text
    print (LOGS_COLORES[nivel] + text_file + LOGS_ENDC)
    sys.stdout.flush()

    # save into file.
    try:
        File = file(LOGS_FILE, 'a')
        File.write(text_file+"\n")
        File.close()
    except:
        print("Imposible escribir en File: " +LOGS_FILE )

class cread_config(object):

    CONFIG_FILE_LOCAL= "config/utemper.conf"
    CONFIG_FILE_SEND= "config/send/utemper.conf"

    def read_config (self, nombre_config):
        # read file local
        (tiempo_local, valor_local) = self.read_config_file(self.CONFIG_FILE_LOCAL,nombre_config )
        log(1, "Leida el valor -%s- para la config -%s- " %(valor_local, nombre_config) )
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
            log(4, "Imposible poder leer la configuracion -%s- del fichero %s " %(nombre_config, file) )

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
            log(4, "Imposible poder escribir la nueva configuracion en fichero %s " %( self.CONFIG_FILE_LOCAL) )
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
            log(4, "Imposible poder leer la configuracion -%s- del fichero %s " %(nombre_config, self.CONFIG_FILE_LOCAL) )
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
            log(5, "Imposible GUARDAR leer la configuracion del fichero %s " %self.CONFIG_FILE_LOCAL )
            return

        # copy to send data.
        try:
            shutil.copy2(self.CONFIG_FILE_LOCAL, self.CONFIG_FILE_SEND)
            log(0, "Configuracion copiada a  %s " %self.CONFIG_FILE_SEND )
        except:
            log(5, "Imposible copiar de %s  a %s" %(self.CONFIG_FILE_LOCAL, self.CONFIG_FILE_SEND) )
            gv.upload_config = False
            return

        log(2, "Configuracion Actualizada fichero  %s " %self.CONFIG_FILE_LOCAL )
        gv.upload_config = True
        gv.lastTimeChageSomething = time.time()
        return 1

class gv(object):

    # number equipo.
    number_equipo =0

    # el tiempo
    tiempo_OK = False
    tiempo_temp=-1
    tiempo_code=3200
    tiempo_estado=""
    tiempo_titulo=""
    hora_init_dia = time.strptime( "08:00 am", "%I:%M %p")
    hora_init_noche = time.strptime( "07:00 pm", "%I:%M %p")
    tiempo_speed = 0.0
    tiempo_City = "Error"

    # temperatura.
    temperatura=30
    temperatura_max = 50
    temperatura_error=1

    # prog Calefa.
    estadoCalefa = 0
    estadoCalefa_NextProg = 0

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

    # sensor de luz
    luz_OK =  False
    luzValor = 0

    #Scan Macs IP.
    scanIp_OK = False
    scanIp_EnCasa = False
