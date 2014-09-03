#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pygame
from pygame.locals import *
from utemper_public import *

class cScreen:
    
    pantalla = 0
    suceso_estado = 0
    screen_number = 0
    carpeta_img = "img/dia/"
    letra_color = (0,0,0)
    Letra_top = None
    lastTimeRefes =0
    
    def __init__(self):
        #try:
            
            # iniciamos la pantalla.
            os.putenv('SDL_VIDEODRIVER', 'fbcon')
            os.putenv('SDL_FBDEV'      , '/dev/fb1')
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
            
            self.refrescar_screen()
        #except:
            #clog().log(4,"Imposible iniciar la pantalla")
            #self.pantalla=0

        
    def suceso(self):
        if(self.pantalla==1):
            if (self.suceso_estado== 0  ):
                self.suceso_estado+=1
                
                # Check el estado del mouse!!!!
                #self.check_screen()
            elif self.suceso_estado== 1:
                self.suceso_estado+=1
                if (time.time()-self.lastTimeRefes > 60 ):
                    self.lastTimeRefes = time.time()
                    self.refrescar_screen()  
            elif (self.suceso_estado== 2  ):
                self.suceso_estado+=1
            else:
                self.suceso_estado=0
    
    def reset():
        self.refrescar_screen()

    def check_screen(self):        
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                 pos = pygame.mouse.get_pos()
                 clog().log(1,"BOTON press screen %d x %d  y." %(pos[0], pos[1]))
                 if(self.pantalla==0):
                       return 0
                 if self.screen_number == 0:
                       self.boton_screen_0(pos)
                 elif self.screen_number == 1:
                       self.boton_screen_1(pos)
                 else:
                       self.boton_screen_0(pos)

    def refrescar_screen(self):
        if(self.pantalla==0):
			return 0
        if self.screen_number == 0:
			self.refrescar_screen_0()
        elif self.screen_number == 1:
			self.refrescar_screen_0()
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
        fondo = pygame.image.load(fichero_fondo).convert()
        self.screen.blit(fondo, (0, 0))
        fichero_up =  self.carpeta_img+"fondo_up.png"
        fondo_up = pygame.image.load(fichero_up).convert_alpha()
        self.screen.blit(fondo_up, (0, -7))
        #dia y hora:
        string=time.strftime("%d-%b-%Y %H:%M", time.localtime())
        mytext = self.Letra_top.render(string, False, self.letra_color).convert_alpha()
        posX= gv.screen_widht -(mytext.get_size()[0] + 15)
        self.screen.blit(mytext, (posX, 10))
        
        #iconos top:
        #wifi
        posX = 10
        fichero_icono = self.carpeta_img+"iconos/wifi_"+str(gv.wifi_estado)+".png"
        icon = pygame.image.load(fichero_icono).convert_alpha() 
        self.screen.blit(icon, (posX,10))
        
        #sensor temperatura
        posX +=(icon.get_size()[0] + 10)
        if (gv.temperatura_error ==1):            
            fichero_icono = self.carpeta_img+"iconos/temp_KO.png"
        else:
            fichero_icono = self.carpeta_img+"iconos/temp_OK.png"
        icon = pygame.image.load(fichero_icono).convert_alpha() 
        self.screen.blit(icon, (posX,10))

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
        fondo = pygame.image.load(fichero_fondo).convert()
        self.screen.blit(fondo, (0, 0))

        #iconos
        posX = 10
        fichero_icono = self.carpeta_img+"iconos/subir_temp.png"
        icon = pygame.image.load(fichero_icono).convert_alpha()
        self.screen.blit(icon, (20,100))
        fichero_icono = self.carpeta_img+"iconos/bajar_temp.png"
        icon = pygame.image.load(fichero_icono).convert_alpha()
        self.screen.blit(icon, (120,100))

        fichero_icono = self.carpeta_img+"iconos/boton_config.png"
        icon = pygame.image.load(fichero_icono).convert_alpha()
        posX = gv.screen_widht - icon.get_size()[0] - 5
        posY = (gv.screen_height) - (icon.get_size()[1]/2) -5
        self.screen.blit(icon, (posX,posY))

        fichero_icono = self.carpeta_img+"iconos/boton_volver.png"
        icon = pygame.image.load(fichero_icono).convert_alpha()
        posY = (gv.screen_height) - (icon.get_size()[1]/2) -5
        self.screen.blit(icon, (15,posY))

 
    def botton_screen_1 (self, pos):
        # subir boton 
        if (pos[0] < (gv.screen_widht/2)-10) and (pos[1] < 120):
			print ""                 