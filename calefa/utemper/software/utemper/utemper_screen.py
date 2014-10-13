#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pygame
import os
from pygame.locals import *
from utemper_public import *
import utemper_screen_image

class cScreen:
    
    pantalla = 0
    screen_number = 0
    carpeta_img = "img/dia/"
    letra_color = (0,0,0)
    Letra_top = None
    lastTimeRefes = time.time() + 5
    cUtemperSceenImagen=None
	
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
            
            self.refrescar_screen()
        except:
            clog().log(4,"Imposible iniciar la pantalla")
            self.pantalla=0

    def suceso(self):
        if(self.pantalla==1):
            # Check el estado del mouse!!!!
            self.check_screen()
            if (time.time()-self.lastTimeRefes > 60 ):
                self.lastTimeRefes = time.time()
                self.refrescar_screen()  
    
    def reset(self):
        self.refrescar_screen()

    def check_screen(self):
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                 pos = pygame.mouse.get_pos()
                 print pygame.mouse.get_pos()
                 clog().log(1,"BOTON press screen %d x %d  y." %(pos[0], pos[1]))
                 if(self.pantalla==0):
                       return 0
                 if self.screen_number == 0:
                       self.boton_screen_0(pos)
                 elif self.screen_number == 1:
                       self.boton_screen_1(pos)
                 elif self.screen_number == 2:
                       self.boton_screen_2(pos)
                 else:
                       self.boton_screen_0(pos)
                 self.refrescar_screen()
                 gv.lastTimeChageSomething = time.time()

    def refrescar_screen(self):
        self.lastTimeRefes = time.time()
        if(self.pantalla==0):
            return 0
        if self.screen_number == 0:
            self.refrescar_screen_0()
        elif self.screen_number == 1:
            self.refrescar_screen_1()
        elif self.screen_number == 2:
            self.refrescar_screen_2()
        else:
            elf.refrescar_screen_0()
            
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
        self.screen.blit(fondo_up, (0, -7))
        #dia y hora:
        string=time.strftime("%d-%b %I:%M%p", time.localtime())
        mytext = self.Letra_top.render(string, False, self.letra_color).convert_alpha()
        posX= gv.screen_widht -(mytext.get_size()[0] + 15)
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
        posY = (gv.screen_height/2)- (mytext.get_size()[1]/2) +42
        self.screen.blit(mytext, (posX ,posY))
        # se muestran lo cambios en pantalla
        pygame.display.flip()
        clog().log(1,"Refrescar screen 0 OK")

    def refrescar_screen_1(self):

        # cargamos el fondo
        fichero_fondo = self.carpeta_img+"fondo/change_temp.jpg"
        fondo = self.cUtemperSceenImagen.getImagen(fichero_fondo)
        self.screen.blit(fondo, (0, 0))

        #estado Calefa
        fichero_icono = self.carpeta_img+"iconos/boton_"+str(gv.estadoCalefa)+".png"
        icon = self.cUtemperSceenImagen.getImagen(fichero_icono)
        posX = (gv.screen_widht/2) - (icon.get_size()[0]/2)
        self.screen.blit(icon, (posX,20))
         
        #temp
        string="%.1f" %gv.temperatura_max
        mytext = self.Letra_temp2.render(string, False, self.letra_color).convert_alpha()
        posX = (gv.screen_widht/2) - (mytext.get_size()[0]/2)
        posY = (gv.screen_height/2)- (mytext.get_size()[1]/2)
        self.screen.blit(mytext, (posX ,posY))
         
        # se muestran lo cambios en pantalla
        pygame.display.flip()
        clog().log(1,"Refrescar screen 1 OK")

    def refrescar_screen_2(self):

        # cargamos el fondo
        fichero_fondo = self.carpeta_img+"fondo/change_temp.jpg"
        fondo = pygame.image.load(fichero_fondo).convert()
        self.screen.blit(fondo, (0, 0))

        #text
        mytext = self..Letra_top.render("Seleciona el modo.", False, self.letra_color).convert_alpha()
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
        clog().log(1,"Refrescar screen 2 OK")

    def boton_screen_0 (self, pos):
        # Entrar menu
        self.screen_number = 1
        
    def boton_screen_1(self, pos):
        # subir boton         # pos[0] x 
                              # pos[1] y
        if ( pos[1] < 60):  # cambiar configuracion.
             self.screen_number = 2
        elif (pos[0] < 100) and (60 < pos[1] < 160):  # bajo temp
             self.changeTemp(gv.temperatura_max+0.5)
        elif (pos[0] > 180) and (60 < pos[1] < 160):  # subir temp
             self.changeTemp(gv.temperatura_max-0.5)
        elif (pos[0] < 80) and ( pos[1] > 170):  # volver
             self.screen_number = 0
             if(self.saveConfigurcion == True):
                cread_config().update_config_file("temperatura",str(gv.temperatura_max))
                self.saveConfigurcion == False
                gv.reset_class = 1

    def boton_screen_2(self, pos):
        # boton         # pos[0] x 
                        # pos[1] y
        if (80 < pos[0] < 130) and (50 < pos[1] < 95):  # estado 0
             gv.estadoCalefa = 0
             cread_config().update_config_file("estado_caldera",str(gv.estadoCalefa))
             gv.reset_class = 1
        elif (80 < pos[0] < 130) and (95 < pos[1] < 150):  # estado 1
             gv.estadoCalefa = 1
             cread_config().update_config_file("estado_caldera",str(gv.estadoCalefa))
             gv.reset_class = 1
        elif (80 < pos[0] < 130) and (150 < pos[1] < 180):  # estado 2
             gv.estadoCalefa = 2
             cread_config().update_config_file("estado_caldera",str(gv.estadoCalefa))
             gv.reset_class = 1
        self.screen_number = 1


    def changeTemp(self, new_temp):
        if (15 < new_temp <35):
             gv.temperatura_max = new_temp
             self.saveConfigurcion = True
