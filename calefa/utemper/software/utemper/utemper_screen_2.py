#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import os
from pygame.locals import *
from utemper_public import *
import utemper_screen_image

class cScreen_2:
    pantalla=0
    carpeta_img = "img/dia/"
    letra_color = (0,0,0)
    cUtemperSceenImagen=None
    screen = None
    
    def __init__(self, screen):
        self.screen = screen
        try:
            self.cUtemperSceenImagen = utemper_screen_image.cScreenImeges()
            self.Letra = pygame.font.Font("font/stag-sans-light-webfont.ttf", 20)
            self.pantalla=1
        except:
            log(4,"Imposible iniciar la pantalla 2 ")
            self.pantalla=0

    def refrescar_screen(self):
        if (self.pantalla==0):
            log(3," Pantalla inactiva: Imposible refrescar la pantalla 2 ")
            return
        if (gv.noche==1):
            self.carpeta_img="img/noche/"
            self.letra_color=(255,255,255)
        else:
            self.carpeta_img="img/dia/"
            self.letra_color=(0,0,0)
            
        # cargamos el fondo
        fichero_fondo = self.carpeta_img+"fondo/config_fondo.jpg"
        fondo = self.cUtemperSceenImagen.getImagen(fichero_fondo)
        self.screen.blit(fondo, (0, 0))

        #text
        mytext = self.Letra.render("Seleciona el modo.", False, self.letra_color).convert_alpha()
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

    def boton_screen (self, pos):
        # Entrar menu
        self.screen_number = 1
        