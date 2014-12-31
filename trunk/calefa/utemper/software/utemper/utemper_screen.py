#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pygame
import os
import subprocess
from pygame.locals import *
from utemper_public import *
import utemper_screen_image
import utemper_screen_0
import utemper_screen_1
import utemper_screen_2
import utemper_screen_4
import utemper_screen_5
import utemper_screen_Black

class cScreen:
    
    pantalla = 0
    screen = None
    screen_number = 0
    carpeta_img = "img/dia/"
    letra_color = (0,0,0)
    lastTimeRefes = time.time()
    lastTimeSeg = time.time()
    cUtemperSceenImagen=None
    cScreenBlack =  None
    last_values= [0, 0, 0, 0, 0, 0] # noche, rele, temperatura, wifi, sensor_temp
    
    saveConfigurcion = False
    
    def __init__(self):
        try:
            # iniciamos la pantalla.
            os.putenv('SDL_VIDEODRIVER', 'fbcon')
            os.putenv('SDL_FBDEV'      , '/dev/fb1')
            os.putenv('SDL_MOUSEDRV' , 'TSLIB')
            os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')
            pygame.init()
            #screen = pygame.display.set_mode((gv.screen_widht, gv.screen_widht))
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            pygame.display.set_caption("utemper")
            pygame.mouse.set_visible(False)
            
            # info
            gv.screen_widht  = pygame.display.Info().current_w
            gv.screen_height  = pygame.display.Info().current_h

            self.cUtemperSceenImagen = utemper_screen_image.cScreenImeges()
            self.cUtemperSceen0 = utemper_screen_0.cScreen_0(self.screen)
            self.cUtemperSceen1 = utemper_screen_1.cScreen_1(self.screen)
            self.cUtemperSceen2 = utemper_screen_2.cScreen_2(self.screen)
            self.cUtemperSceen4 = utemper_screen_4.cScreen_4(self.screen)
            self.cUtemperSceen5 = utemper_screen_5.cScreen_5(self.screen)
            self.cScreenBlack = utemper_screen_Black.cScreenBlack()
            
            self.pantalla=1

            log(1,"iniciar la pantalla  OK")
        except:
            log(4,"Imposible iniciar la pantalla KOO")
            self.pantalla=0
        self.refrescar_screen()                
    def suceso(self):
        if(self.pantalla==1):
            # Check el estado del mouse!!!!
            self.check_screen()
            if (time.time() - self.lastTimeSeg > 1 ): # se ha de cheqear cada SEG
                self.cScreenBlack.suceso()
                self.lastTimeSeg = time.time()
                if (self.lastTimeSeg - self.lastTimeRefes > 60 ):
                    self.refrescar_screen()
                elif ([gv.noche, gv.rele, round(gv.temperatura, 0), gv.wifi_estado, gv.temperatura_error, gv.estadoCalefa] != self.last_values):
                    self.refrescar_screen() 
    
    def reset(self):
        if(self.pantalla==1):
            self.cScreenBlack.reset()
            self.refrescar_screen()

    def check_screen(self):
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):                
                 self.cScreenBlack.ScreenON()
                 pos = pygame.mouse.get_pos()
                 log(1,"BOTON press screen %d x %d  y." %(pos[0], pos[1]))
                 if(self.pantalla==0):
                       return 0
                 if self.screen_number == 0:
                       self.boton_screen_0(pos)
                 elif self.screen_number == 1:
                       self.boton_screen_1(pos)
                 elif self.screen_number == 2:
                       self.boton_screen_2(pos)
                 elif self.screen_number == 4:
                       self.boton_screen_4(pos)
                 elif self.screen_number == 5:
                       self.boton_screen_5(pos)
                 else:
                       self.boton_screen_0(pos)
                 self.refrescar_screen()
                 gv.lastTimeChageSomething = time.time()

    def refrescar_screen(self):
        if(self.pantalla==0):
            return 0
        if(self.cScreenBlack.IsScreenON() == False): # si no esta encendida no se refresca.
            return 0
        self.last_values = [gv.noche, gv.rele, round(gv.temperatura, 0), gv.wifi_estado, gv.temperatura_error, gv.estadoCalefa]
        self.lastTimeRefes = time.time()
        if(self.pantalla==0):
            return 0
        if self.screen_number == 0:
            self.cUtemperSceen0.refrescar_screen()
        elif self.screen_number == 1:
            self.cUtemperSceen1.refrescar_screen()
        elif self.screen_number == 2:
            self.cUtemperSceen2.refrescar_screen()
        elif self.screen_number == 4:
            self.cUtemperSceen4.refrescar_screen()
        elif self.screen_number == 5:
            self.cUtemperSceen5.refrescar_screen()
        else:
            self.cUtemperSceen0.refrescar_screen()

    def boton_screen_0 (self, pos):
        # Entrar menu
        self.screen_number = 1
        
    def boton_screen_1(self, pos):
        # subir boton         # pos[0] x 
                              # pos[1] y
        if ( pos[1] < 50):  # cambiar configuracion.
             self.screen_number = 2
        elif (pos[0] < 100) and (60 < pos[1] < 160):  # bajo temp
             self.changeTemp(gv.temperatura_max+0.5)
        elif (pos[0] > 180) and (60 < pos[1] < 160):  # subir temp
             self.changeTemp(gv.temperatura_max-0.5)
        elif (pos[0] > 240) and ( pos[1] > 170):  # Config
             self.screen_number = 4
        elif (pos[0] < 80) and ( pos[1] > 170):  # volver
             self.screen_number = 0
             if(self.saveConfigurcion == True):
                cread_config().update_config_file("temperatura",str(gv.temperatura_max))
                self.saveConfigurcion == False
                gv.reset_class = 1

    def boton_screen_2(self, pos):
        # boton         # pos[0] x 
                        # pos[1] y
        if (80 < pos[0] < 250) and (50 < pos[1] < 95):  # estado 0
             gv.estadoCalefa = 0
             cread_config().update_config_file("estado_caldera",str(gv.estadoCalefa))
             gv.reset_class = 1
        elif (80 < pos[0] < 250) and (95 < pos[1] < 150):  # estado 1
             gv.estadoCalefa = 1
             cread_config().update_config_file("estado_caldera",str(gv.estadoCalefa))
             gv.reset_class = 1
        elif (80 < pos[0] < 250) and (150 < pos[1] < 180):  # estado 2
             gv.estadoCalefa = 2
             cread_config().update_config_file("estado_caldera",str(gv.estadoCalefa))
             gv.reset_class = 1
        self.screen_number = 0
        
    def boton_screen_4(self, pos):
        # boton         # pos[0] x 
                        # pos[1] y
        if (pos[0] < 100) and (pos[1] < 200):  # Info
            self.screen_number = 5
        elif (100 < pos[0] < 212) and (pos[1] < 200):  # Apagar
            log(1,"Apagando el equipo....")
            fichero_fondo = self.carpeta_img+"fondo/power_off.jpg"
            fondo = self.cUtemperSceenImagen.getImagen(fichero_fondo)
            self.screen.blit(fondo, (0, 0))
            pygame.display.flip()
            os.remove(LOGS_FILE)
            subprocess.call(["shutdown", "-h", "-F", "now"])
            exit(0)
        if (pos[0] > 212) and (pos[1] < 200):  # sleep Screen
            log(1,"Sleep Pantalla el equipo....")
            self.cScreenBlack.BotonScreenOFF()
            self.screen_number = 5
        elif (pos[0] < 100) and ( pos[1] > 220):  # Volver
             self.screen_number = 0

    def boton_screen_5(self, pos):
        # boton         # pos[0] x 
                        # pos[1] y
        self.screen_number = 0
             
    def changeTemp(self, new_temp):
        if (15 < new_temp <35):
             gv.temperatura_max = new_temp
             self.saveConfigurcion = True