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

class cScreen:
    
    pantalla = 0
    screen = None
    screen_number = 0
    carpeta_img = "img/dia/"
    letra_color = (0,0,0)
    Letra_top = None
    Letra_temp1 = None
    Letra_temp2 = None
    lastTimeRefes = time.time() + 5
    lastTimePowerONScreen = time.time()
    cUtemperSceenImagen=None
    backlightpath = "/sys/class/gpio/gpio252"

    last_values= [0, 0, 0, 0, 0] # noche, rele, temperatura, wifi, sensor_temp
    
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

            # inicializamos las letras.
            self.Letra_top = pygame.font.Font("font/stag-sans-light-webfont.ttf", 20)
            self.Letra_temp1 = pygame.font.Font("font/Interstate-Black.ttf", 50)
            self.Letra_temp2 = pygame.font.Font("font/Interstate-Black.ttf", 40)
            self.pantalla=1
            
            # info
            gv.screen_widht  = pygame.display.Info().current_w
            gv.screen_height  = pygame.display.Info().current_h

            self.cUtemperSceenImagen = utemper_screen_image.cScreenImeges()
            self.cUtemperSceen0 = utemper_screen_0.cScreen_0()
            self.cUtemperSceen1 = utemper_screen_1.cScreen_1()
            self.cUtemperSceen2 = utemper_screen_2.cScreen_2()
            self.cUtemperSceen4 = utemper_screen_4.cScreen_4()
            self.cUtemperSceen5 = utemper_screen_5.cScreen_5()
            self.refrescar_screen()
        except:
            log(4,"Imposible iniciar la pantalla")
            self.pantalla=0
            
        # Check if GPIO252 has already been set up  // INICIAR Apagar Pantalla.
        self.backlightenabled = False
        if not exists(self.backlightpath):
            try:
                with open("/sys/class/gpio/export", "w") as bfile:
                    bfile.write("252")

            except:
                log(4,"Imposible Iniciar Apagar Pantalla")

        # Set the direction
        try:
            with open("/sys/class/gpio/gpio252/direction", "w") as bfile:
                bfile.write("out")
                self.backlightenabled = True
        except:
                log(4,"Imposible Iniciar Apagar Pantalla")
            
    def suceso(self):
        if(self.pantalla==1):
            # Check el estado del mouse!!!!
            self.check_screen()
            if (time.time()-self.lastTimeRefes > 60 ):
                self.refrescar_screen()
            elif (time.time()-self.lastTimePowerONScreen > 300 ) and (gv.noche == 1) and (self.screen_number!= 3):
                self.screen_number = 3  # pantalla negra.
                self.Backlight(0)
            elif ([gv.noche, gv.rele, round(gv.temperatura, 0), gv.wifi_estado, gv.temperatura_error] != self.last_values)and (self.screen_number!= 3):
                self.refrescar_screen() 
    
    def reset(self):
        self.Backlight(1)
        self.lastTimePowerONScreen= time.time()
        self.refrescar_screen()

    def check_screen(self):
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                 pos = pygame.mouse.get_pos()
                 print pygame.mouse.get_pos()
                 log(1,"BOTON press screen %d x %d  y." %(pos[0], pos[1]))
                 if(self.pantalla==0):
                       return 0
                 if self.screen_number == 0:
                       self.boton_screen_0(pos)
                 elif self.screen_number == 1:
                       self.boton_screen_1(pos)
                 elif self.screen_number == 2:
                       self.boton_screen_2(pos)
                 elif self.screen_number == 3:
                       self.boton_screen_3(pos)
                 elif self.screen_number == 4:
                       self.boton_screen_4(pos)
                 elif self.screen_number == 5:
                       self.boton_screen_5(pos)
                 else:
                       self.boton_screen_0(pos) 
                 self.refrescar_screen()
                 gv.lastTimeChageSomething = time.time()
                 self.lastTimePowerONScreen = time.time()

    def refrescar_screen(self):
        self.last_values = [gv.noche, gv.rele, round(gv.temperatura, 0), gv.wifi_estado, gv.temperatura_error]
        self.lastTimeRefes = time.time()
        if(self.pantalla==0):
            return 0
        if self.screen_number == 0:
            self.cUtemperSceen0.refrescar_screen()
          #  self.refrescar_screen_0()
        elif self.screen_number == 1:
            self.cUtemperSceen1.refrescar_screen()
        #    self.refrescar_screen_1()
        elif self.screen_number == 2:
            self.cUtemperSceen2.refrescar_screen()
        #    self.refrescar_screen_2()
        elif self.screen_number == 3:
            self.cUtemperSceen3.refrescar_screen()
        elif self.screen_number == 4:
            self.cUtemperSceen4.refrescar_screen()
        elif self.screen_number == 5:
            self.cUtemperSceen5.refrescar_screen()
        else:
            self.refrescar_screen_0()
            
    def refrescar_screen_0(self):
        if (gv.noche==1):
            self.carpeta_img="img/noche/"
            self.letra_color=(255,255,255)
        else:
            self.carpeta_img="img/dia/"
            self.letra_color=(0,0,0)
            
        # cargamos el fondo
        fichero_fondo = self.carpeta_img+"fondo/"+str(gv.tiempo_code)+".jpg"
        fondo = self.cUtemperSceenImagen.getImagen(fichero_fondo)
        self.screen.blit(fondo, (0, 0))
        fichero_up =  self.carpeta_img+"fondo_up.png"
        fondo_up = self.cUtemperSceenImagen.getImagen(fichero_up)
        self.screen.blit(fondo_up, (0, -15))
        #dia y hora:
        string=time.strftime("%d-%b %I:%M %p", time.localtime())
        mytext = self.Letra_top.render(string, False, self.letra_color).convert_alpha()
        posX= gv.screen_widht -(mytext.get_size()[0] + 7)
        self.screen.blit(mytext, (posX, 10))
        
        #iconos top:
        #wifi
        posX = 10
        fichero_icono = self.carpeta_img+"iconos/wifi_"+str(gv.wifi_estado)+".png"
        icon = self.cUtemperSceenImagen.getImagen(fichero_icono)
        self.screen.blit(icon, (posX,10))
        
        #sensor temperatura
        posX +=(icon.get_size()[0] + 10)
        if (gv.temperatura_error ==1):            
            fichero_icono = self.carpeta_img+"iconos/temp_KO.png"
        else:
            fichero_icono = self.carpeta_img+"iconos/temp_OK.png"
        icon = self.cUtemperSceenImagen.getImagen(fichero_icono)
        self.screen.blit(icon, (posX,10))

        #caldera.
        if (gv.rele ==1):            
            fichero_icono = self.carpeta_img+"iconos/fire_ON.png"
        else:
            fichero_icono = self.carpeta_img+"iconos/fire_OFF.png"
        icon = self.cUtemperSceenImagen.getImagen(fichero_icono)
        posX = gv.screen_widht - icon.get_size()[0] - 7
        posY = gv.screen_height - (icon.get_size()[1]) -7
        self.screen.blit(icon, (posX,posY))
        
        # temperaturas:
        string="%d.C" %gv.tiempo_temp
        mytext = self.Letra_temp2.render(string, False, self.letra_color).convert_alpha()
        posY = (gv.screen_height/2)- (mytext.get_size()[1]/2) +30
        self.screen.blit(mytext, (20 ,posY))
        
        string="%.1fC" %gv.temperatura
        mytext = self.Letra_temp1.render(string, False, self.letra_color).convert_alpha()
        posX = gv.screen_widht - mytext.get_size()[0] - 30
        posY = (gv.screen_height/2)- (mytext.get_size()[1]/2) +5
        self.screen.blit(mytext, (posX ,posY))
        # se muestran lo cambios en pantalla
        pygame.display.flip()
        log(1,"Refrescar screen 0 OK")

    def refrescar_screen_1(self):

        # cargamos el fondo
        fichero_fondo = self.carpeta_img+"fondo/change_temp.jpg"
        fondo = self.cUtemperSceenImagen.getImagen(fichero_fondo)
        self.screen.blit(fondo, (0, 0))

        #estado Calefa
        fichero_icono = self.carpeta_img+"iconos/boton_"+str(gv.estadoCalefa)+".png"
        icon = self.cUtemperSceenImagen.getImagen(fichero_icono)
        posX = (gv.screen_widht/2) - (icon.get_size()[0]/2)
        self.screen.blit(icon, (posX,15))
         
        #temp
        string="%.1f" %gv.temperatura_max
        mytext = self.Letra_temp2.render(string, False, self.letra_color).convert_alpha()
        posX = (gv.screen_widht/2) - (mytext.get_size()[0]/2)
        posY = (gv.screen_height/2)- (mytext.get_size()[1]/2)
        self.screen.blit(mytext, (posX ,posY))
         
        # se muestran lo cambios en pantalla
        pygame.display.flip()
        log(1,"Refrescar screen 1 OK")

    def refrescar_screen_2(self):

        # cargamos el fondo
        fichero_fondo = self.carpeta_img+"fondo/change_temp.jpg"
        fondo = self.cUtemperSceenImagen.getImagen(fichero_fondo)
        self.screen.blit(fondo, (0, 0))

        #text
        mytext = self.Letra_top.render("Seleciona el modo.", False, self.letra_color).convert_alpha()
        posX = (gv.screen_widht/2) - (mytext.get_size()[0]/2)
        self.screen.blit(mytext, (posX ,15))
        
        #botones.
        icon = self.cUtemperSceenImagen.getImagen(self.carpeta_img+"iconos/boton_0.png")
        posX = (gv.screen_widht/2) - (icon.get_size()[0]/2)
        self.screen.blit(icon, (posX,55))

        icon = self.cUtemperSceenImagen.getImagen(self.carpeta_img+"iconos/boton_1.png")
        posX = (gv.screen_widht/2) - (icon.get_size()[0]/2)
        self.screen.blit(icon, (posX,100))

        icon = self.cUtemperSceenImagen.getImagen(self.carpeta_img+"iconos/boton_2.png")
        posX = (gv.screen_widht/2) - (icon.get_size()[0]/2)
        self.screen.blit(icon, (posX,155))

        # se muestran lo cambios en pantalla
        pygame.display.flip()
        log(1,"Refrescar screen 2 OK")

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
        self.screen_number = 1

    def boton_screen_3(self, pos):
        # boton         # pos[0] x 
                        # pos[1] y
        self.Backlight(1)
        self.screen_number = 0
		
    def boton_screen_4(self, pos):
        # boton         # pos[0] x 
                        # pos[1] y
        if (pos[0] < 100) and (pos[1] < 200):  # Info
            self.screen_number = 5
        elif (100 <pos[0] > 212) and (pos[1] < 200):  # Apagar
			fichero_fondo = self.carpeta_img+"fondo/power_off.jpg"
			fondo = self.cUtemperSceenImagen.getImagen(fichero_fondo)
			self.screen.blit(fondo, (0, 0))
			pygame.display.flip()
			subprocess.call(["shutdown", "-h", "3"])
			time.sleep(2)
        elif (pos[0] < 100) and ( pos[1] > 220):  # Volver
             self.screen_number = 1

    def boton_screen_5(self, pos):
        # boton         # pos[0] x 
                        # pos[1] y
        self.screen_number = 0
			 
    def changeTemp(self, new_temp):
        if (15 < new_temp <35):
             gv.temperatura_max = new_temp
             self.saveConfigurcion = True

    def Backlight(self, light):
        '''Turns the PiTFT backlight on or off.
        Usage:
         Backlight(True) - turns light on
         Backlight(False) - turns light off
        '''
        if self.backlightenabled:
            try:
                with open("/sys/class/gpio/gpio252/value", "w") as bfile:
                    bfile.write("%d" % (bool(light)))
            except:
                log(4,"Imposible cambiar black light Screen.")