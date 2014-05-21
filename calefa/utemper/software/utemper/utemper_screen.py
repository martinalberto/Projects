#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pygame
from pygame.locals import *
from utemper_public import *

class cScreen:
    
    screen = 0
    suceso_estado = 0
    screen_number = 0
    carpeta_img = "img/dia/"
    letra_color = (0,0,0)
    Letra_top = None

    def __init__(self):
        try:
            
            # iniciamos la pantalla.
            pygame.init()
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("tutorial pygame parte 2")
            
            # inicializamos las letras.
            Letra_top = pygame.font.Font("font/stag-sans-light-webfont.ttf", 20)
            self.screen=1
        except:
            clog().log(4,"Imposible iniciar la pantalla")
            self.screen=0
        self.refrescar_screen()
        
    def suceso(self):
        if(self.screen==1):
            if (self.suceso_estado== 0  ):
                self.suceso_estado+=1
                self.check_screen()  
            elif self.suceso_estado== 1:
                self.suceso_estado+=1
                if (time.time()-self.lastTimeRefesf>5) and (self.lastTemp!=[temperatura, tiempo_temp]):
                    self.refrescar_screen()  
            elif (self.suceso_estado== 2  ):
                self.suceso_estado+=1
            else:
                self.suceso_estado=0
    
    def refrescar_screen(self):
        if(self.screen==0):
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
        
        fichero_up =  self.carpeta_img+"fondo_up.png"
        fondo_up = pygame.image.load(fichero_up).convert_alpha()
        
        #dia y hora:
        string=time.strftime("%d-%b-%Y %H:%M", time.localtime())
        mytext = myfont.render(string, False, self.letra_color).convert_alpha()
        posX= SCREEN_WIDTH -(mytext.get_size()[0] + 15)
        screen.blit(mytext, (posX, 10))
        
        #iconos top:
        posX = 10
        fichero_icono = self.carpeta_img+"/iconos/wifi_"+str(estado_wifi)+".png"
        icon = pygame.image.load(fichero_icono).convert_alpha() 
        screen.blit(wifi_icon, (posX,10))
        
        posX +=(mytext.get_size()[0] + 10)
        fichero_icono = self.carpeta_img+"/iconos/temp_"+str(estado_temp)+".png"
        icon = pygame.image.load(fichero_icono).convert_alpha() 
        screen.blit(wifi_icon, (posX,10))

        # temperaturas:
        

        # se muestran lo cambios en pantalla
        pygame.display.flip()

