#!/usr/bin/python
from __future__ import print_function
from wifi import Cell, Scheme
import os
import os.path
import subprocess

from utemper_public import *
        
def save_resultados (wifi, conectado, internet, ip ):
    file = open(FILE_WIFI, "w")
    file.write(str(wifi)+"\n")
    file.write(str(conectado)+"\n")
    file.write(str(internet)+"\n")
    file.write(str(ip)+"\n")
    file.close()

######################################################
############## que pasa si se cambia la clave wifi.
######################################################

# Init.
FILE_RED_WIFI ="/tmp/crear_wifi.var"
FILE_WIFI =  "/tmp/wifi.var"
wifissid ="prueba"
wificode="prueba"

estado = -1

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
    if estado== -1:
        # Init. borramos las redes antuguas.
        try:
            log(2, "====== Init Connect wifi =======")
            wifissid = cread_config_Class.read_config("wifi_ssid")
            wificode = cread_config_Class.read_config("wifi_code")
            wait = 0.1
            conectado=0
            internet=0
            estado = 0            
            try:
                scheme = Scheme.find("wlan0", wifissid)
                if (scheme != None ):
                    scheme.delete()
                    log(0, "scheme borrado.")
            except:
                scheme = None
        except:
            # error.
            log(5, "Imposible leer la configuracion"  )
            wifi = 0
            conectado=0
            internet=0
            estado = 0
            wait= 10
    elif estado==0:
        # leer configuracion
        try:
            subprocess.call(["ifconfig", "wlan0", "up"])			
            subprocess.call(["killall", "dhclient"])
            wifissid = cread_config_Class.read_config("wifi_ssid")
            wificode = cread_config_Class.read_config("wifi_code")
            wait = 0.1
            conectado=0
            internet=0
            estado = 1
            log(1, "Reset ifconfig y dhclient")
            log(0, "configuracion leida.")
        except:
            # error.
            log(5, "Imposible leer la configuracion"  )
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
                estado = 1
                wait = 10
            else:
                log(0, "red -%s- encontrada."%wifissid)
                wifi = 1
                wait = 0.1
                estado = 2
        except:
            log(5, "Imposible leer redes wifi error de wlan0"  )
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
                log(0, "red -%s- guardada."%wifissid)
                wifi = 1
                estado = 3
                wait= 0.1
                errores = 0
            except:
                try:
                    scheme.delete()
                except:
                    pass
                log(3, "Imposible guardar la wifissid  %s " %wifissid )
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
        try:
            scheme = Scheme.for_cell("wlan0",wifissid, cell[0], wificode )
            conexion = scheme.activate()
            ip = conexion.ip_address
            log(2, "conectado con %s" %wifissid)
            wifi = 1
            conectado=1
            estado = 4
            wait = 1
        except:
            log(3, "Imposible conectar a la red  %s " %wifissid )
            conectado=0
            internet=0
            estado = 1
            wait = 20
           
    elif estado ==4:
        # dhcp.
        try:
            result = subprocess.call(["dhclient", "wlan0"])
            if (result == 0):
               conexion = scheme.activate()
               ip = conexion.ip_address
               log(2, "DHCP con -%s- ip" %ip )
               wifi = 1
               conectado=1
               estado = 5
               wait = 30
               errores = 0
            else:
               wait = 5 #intentamos conectar otra vez.
               errores+=1
               estado = 3 
               log(3, "DHCP Error: %d" %result )
               if errores >3:
                   conectado=0
                   internet=0
                   estado = 0
                   estado = 0 # empezamos otra vez.
                   wait = 10
        except:
            log(3, "Imposible DHCP a  la red  %s " %wifissid )
            conectado=0
            internet=0
            estado = 0
            wait = 20
    elif estado ==5:
        # check internet.
        result = os.system("ping -c 1 -w 1 -I wlan0 %s >/dev/null" %('8.8.8.8'))
        if (result== 0):
            errores = 0
            wifi = 1
            conectado=1
            internet=1
            estado = 5
            wait = 120
        else:
            log(3, "Imposible hacer ping en la wlan0 a 8.8.8.8" )
            errores+=1
            internet=0
            estado = 5
            wait = 2
            if errores >3:
                estado = 0
                wait = 10
                subprocess.call(["ifconfig", "wlan0", "down"])
                log(4, "Max errores: wlan0 Down." )
    else:
            #estado imposible
            log(5, "Estado imposible del Wifi connect estado : %d" %estado )
            wifi = 0
            conectado=0
            internet=0
            estado = 0
            wait= 10
    #########################################################
    if ((wifi, conectado, internet, ip ) !=(wifi_old, conectado_old, internet_old, ip_old ) ):
        wifi_old = wifi
        conectado_old = conectado
        internet_old = internet
        ip_old = ip
        save_resultados(wifi, conectado, internet, ip )
        
    time.sleep(wait)
    
    if os.path.isfile(FILE_RED_WIFI):
        salir = 0
