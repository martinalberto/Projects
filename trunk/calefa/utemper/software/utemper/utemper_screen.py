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
            pygame.display.set_caption("tutorial pygame parte 2")
            pygame.mouse.set_visible(False)

            # inicializamos las letras.
            self.Letra_top = pygame.font.Font("font/stag-sans-light-webfont.ttf", 20)
            self.Letra_temp1 = pygame.font.Font("font/stag-sans-light-webfont.ttf", 50)
            self.Letra_temp2 = pygame.font.Font("font/stag-sans-light-webfont.ttf", 40)
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
        self.screen.blit(fondo_up, (0, 0))
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
        if (gv.temperatura ==1):            
            fichero_icono = self.carpeta_img+"iconos/temp_OK.png"
        else:
            fichero_icono = self.carpeta_img+"iconos/temp_KO.png"
        icon = pygame.image.load(fichero_icono).convert_alpha() 
        self.screen.blit(icon, (posX,10))

        # temperaturas:
        string="%dºC" %gv.tiempo_temp
        mytext = self.Letra_temp2.render(string, False, self.letra_color).convert_alpha()
        posY = (gv.screen_height/2)- (mytext.get_size()[1]/2) +40
        self.screen.blit(mytext, (20 ,posY))
        
        string="%dºC" %gv.temperatura
        mytext = self.Letra_temp1.render(string, False, self.letra_color).convert_alpha()
        posX = gv.screen_widht - mytext.get_size()[0] + 35
        posY = (gv.screen_height/2)- (mytext.get_size()[1]/2) +50
        self.screen.blit(mytext, (posX ,posY))
        # se muestran lo cambios en pantalla
        pygame.display.flip()
        clog().log(1,"Refrescar screen 0 OK")

