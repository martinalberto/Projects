#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import os
from pygame.locals import *
from utemper_public import *
import utemper_screen_image

class cScreen_4:
    carpeta_img = "img/dia/"
    letra_color = (0,0,0)
    cUtemperSceenImagen=None
    screen = None
    
    def __init__(self, screen):
        self.screen = screen
        try:
            self.cUtemperSceenImagen = utemper_screen_image.cScreenImeges()

        except:
            log(4,"Imposible iniciar la pantalla 1 ")
            self.pantalla=0

    def refrescar_screen(self):
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

        #botones.
        fichero_fondo = self.carpeta_img+"fondo/configPanel.png"
        fondo = self.cUtemperSceenImagen.getImagen(fichero_fondo)
        self.screen.blit(fondo, (0, 0))

        # se muestran lo cambios en pantalla
        pygame.display.flip()
        log(1,"Refrescar screen 4 OK")

    def boton_screen (self, pos):
        # Entrar menu
        self.screen_number = 1
        
