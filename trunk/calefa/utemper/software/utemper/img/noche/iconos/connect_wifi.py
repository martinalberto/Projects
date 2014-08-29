#!/usr/bin/python
from __future__ import print_function
from wifi import Cell, Scheme
import os
import os.path

from utemper_public import *

######################################################
############## que pasa si se cambia la clave wifi.
######################################################

# Init.
FILE_RED_WIFI ="/tmp/crear_wifi.var"
FILE_WIFI =  "/tmp/wifi.var"
wifissid ="prueba"
wificode="prueba"

estado = 0

wifi=0
conectado=0
internet=0
ip=""

# last valores guarda
wifi_old=0
conectado_old=0
internet_old=0
ip_old=""

save_resultados (wifi, conectado, internet, ip )

# loop
errores=0
salir = 0
cread_config_Class = cread_config()
while not(salir):
    if estado==0:
        # leer configuracion
        try:
            wifissid = cread_config_Class.read_config("wifi_ssid")
            wificode = cread_config_Class.read_config("wifi_code")
            wait = 0.1
            conectado=0
            internet=0
            estado = 1
            clog().log(0, "configuracion leida.")
        except:
            # error.
            clog().log(5, "Imposible leer la configuracion"  )
            wifi = 0
            conectado=0
            internet=0
            estado = 0
            wait= 10
            
    elif estado ==1:    
        # buscamos el ssid:
        try:
            cell = Cell.where("wlan0", lambda cell: cell.ssid.lower() == wifissid.lower())
            if ( cell ==[]):
                # error.
                log(3, "Imposible Encontrar la wifissid  %s " %wifissid )
                wifi = 1
                estado = 0
                wait = 7
            else:
                clog().log(0, "red -%s- encontrada."%wifissid)
                wifi = 1
                wait = 0.1
                estado = 2
        except:
            clog().log(5, "Imposible leer redes wifi error de wlan0"  )
            wifi = 0
            conectado=0
            internet=0
            estado = 0
            wait= 10
            
    elif estado ==2:
        if (Scheme.find("wlan0", wifissid) == None ):
            # se guarda:
            try:
                scheme = Scheme.for_cell("wlan0",wifissid, cell[0], wificode )
                scheme.save()
                clog().log(0, "red -%s- guardada."%wifissid)
                wifi = 1
                estado = 3
                wait= 0.1
            except:
                try:
                    scheme.delete()
                except:
                    pass
                clog().log(3, "Imposible guardar la wifissid  %s " %wifissid )
                scheme.delete()
                wifi = 0
                conectado=0
                internet=0
                estado = 0
                wait= 10
        else:
            wifi = 1
            estado = 3
            wait= 0.5
            
    elif estado ==3:
        # conectamos.        
        scheme = Scheme.for_cell("wlan0",wifissid, cell[0], wificode )
        try:
            conexion = scheme.activate()
            ip = conexion.ip_address
            clog().log(3, "conectado  %s con -%s- ip" %(wifissid, ip) )
            wifi = 1
            conectado=1
            estado = 4
            wait = 2
        except:
            clog().log(3, "Imposible connectar a  la red  %s " %wifissid )
            conectado=0
            internet=0
            estado = 0
            wait = 20
            
    elif estado ==4:
        # check internet.
        result = os.system("ping -c 1 -w 1 -I wlan0 %s >/dev/null" %ip)
        if (result== 0):
            errores = 0
            wifi = 1
            conectado=1
            internet=1
            estado = 4
            wait = 30
        else:
            clog().log(3, "Imposible hacer ping en la wlan0 a 8.8.8.8" )
            errores+=1
            internet=0
            estado = 4
            wait = 2
            if errores >3:
                estado = 0
                wait = 10
                
    #########################################################
    if ((wifi, conectado, internet, ip ) !=(wifi_old, conectado_old, internet_old, ip_old ) ):
        wifi_old = wifi
        conectado_old = conectado
        internet_old = internet
        ip_old = ip
        save_resultados (wifi, conectado, internet, ip )
        
    time.sleep(wait)
    
    if os.path.isfile(FILE_RED_WIFI):
        salir = 0
        
def save_resultados (wifi, conectado, internet, ip ):
    file = open(FILE_WIFI, "w")
    file.write(str(wifi)+"\n")
    file.write(str(conectado)+"\n")
    file.write(str(internet)+"\n")
    file.write(str(ip)+"\n")
    file.close()