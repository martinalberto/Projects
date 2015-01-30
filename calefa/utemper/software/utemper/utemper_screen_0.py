#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, datetime
import pygame
import os
from pygame.locals import *
from utemper_public import *
import utemper_screen_image

class cScreen_0:
    pantalla=0
    carpeta_img = "img/dia/"
    letra_color = (0,0,0)
    Sombra_Color = (120,120,120)
    Letra_top = None
    Letra_temp1 = None
    Letra_temp2 = None
    cUtemperSceenImagen=None
    screen = None
    
    def __init__(self, screen):
        self.screen = screen
        try:
            # inicializamos las letras.
            self.Letra_top = pygame.font.Font("font/stag-sans-light-webfont.ttf", 20)
            self.Letra_temp1 = pygame.font.Font("font/Interstate-Black.ttf", 50)
            self.Letra_temp2 = pygame.font.Font("font/Interstate-Black.ttf", 40)

            self.cUtemperSceenImagen = utemper_screen_image.cScreenImeges()
            self.pantalla=1
        except:
            log(4,"Imposible iniciar la pantalla 0 ")
            self.pantalla=0

    def refrescar_screen(self):
        if (self.pantalla==0):
            log(3," Pantalla inactiva: Imposible refrescar la pantalla 0 ")
            return
        if (gv.noche==1):
            self.carpeta_img="img/noche/"
            self.letra_color=(255,255,255)
            self.Sombra_Color = (120,120,120)
        else:
            self.carpeta_img="img/dia/"
            self.letra_color=(0,0,0)
            self.Sombra_Color = (130,130,130)
            
        # cargamos el fondo
        fichero_fondo = self.carpeta_img+"fondo/"+str(gv.tiempo_code)+".jpg"
        log(0," Pantalla 0: fondo: "+ fichero_fondo)
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
        if (gv.estadoCalefa == 0):
            fichero_icono = self.carpeta_img+"iconos/apagado_label.png"
            icon = self.cUtemperSceenImagen.getImagen(fichero_icono)
            posX = gv.screen_widht - icon.get_size()[0] - 4
            posY = gv.screen_height - icon.get_size()[1] -4
            self.screen.blit(icon, (posX,posY))
        elif (gv.estadoCalefa == 1) and (gv.rele ==1): # solo cuando esta encendido.            
            fichero_icono = self.carpeta_img+"iconos/fire_ON.png"
            icon = self.cUtemperSceenImagen.getImagen(fichero_icono)
            posX = gv.screen_widht - icon.get_size()[0] - 7
            posY = gv.screen_height - icon.get_size()[1] -7
            self.screen.blit(icon, (posX,posY))
        elif (gv.estadoCalefa == 2):
            if (gv.estadoCalefa_NextProg == -1):
                fichero_icono = self.carpeta_img+"iconos/programado_label.png"
                icon = self.cUtemperSceenImagen.getImagen(fichero_icono)
                posX = gv.screen_widht - icon.get_size()[0] - 4
                posY = gv.screen_height - icon.get_size()[1] -4
                self.screen.blit(icon, (posX,posY))            
            elif (gv.estadoCalefa_NextProg - time.time() < 60):
                if (gv.rele ==1):            
                    fichero_icono = self.carpeta_img+"iconos/fire_ON_prog.png"
                else:
                    fichero_icono = self.carpeta_img+"iconos/fire_OFF_prog.png"
                icon = self.cUtemperSceenImagen.getImagen(fichero_icono)
                posX = gv.screen_widht - icon.get_size()[0] - 7
                posY = gv.screen_height - icon.get_size()[1] -7
                self.screen.blit(icon, (posX,posY))
            else:
                string = "Prog a las %s " %(time.strftime("%I:%M %p", time.localtime(abs(gv.estadoCalefa_NextProg))))
                string +=  "(%s)" %(time.strftime(str(datetime.timedelta(seconds =round(gv.estadoCalefa_NextProg - time.time())))))
                mytext = self.Letra_top.render(string , False, self.letra_color).convert_alpha()
                mytext_sombra = self.Letra_top.render(string , False, self.Sombra_Color).convert_alpha()
                posX = gv.screen_widht - mytext.get_size()[0] - 7
                posY = gv.screen_height - mytext.get_size()[1] -7
                self.screen.blit(mytext_sombra, (posX+1,posY+1))
                self.screen.blit(mytext, (posX,posY))
        
        # temperaturas:
        if (gv.tiempo_OK ): # temperatura Imposible.
            string="%d.C" %gv.tiempo_temp
            mytext_sombra = self.Letra_temp2.render(string, False, self.Sombra_Color).convert_alpha()
            mytext = self.Letra_temp2.render(string, False, self.letra_color).convert_alpha()
            posY = (gv.screen_height/2)- (mytext.get_size()[1]/2) +30
            self.screen.blit(mytext_sombra, (20+2 ,posY+2))
            self.screen.blit(mytext, (20 ,posY))
        
        string="%.1fC" %gv.temperatura
        mytext_sombra = self.Letra_temp1.render(string, False, self.Sombra_Color).convert_alpha()
        mytext = self.Letra_temp1.render(string, False, self.letra_color).convert_alpha()
        posX = gv.screen_widht - mytext.get_size()[0] - 30
        posY = (gv.screen_height/2)- (mytext.get_size()[1]/2) +5
        self.screen.blit(mytext_sombra, (posX+2 ,posY+2))
        self.screen.blit(mytext, (posX ,posY))
        
        # se muestran lo cambios en pantalla
        pygame.display.flip()
        log(1,"Refrescar screen 0 OK")


    def boton_screen (self, pos):
        # Entrar menu
        self.screen_number = 1
        
