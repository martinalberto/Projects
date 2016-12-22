#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from utemper_public import *

class cScreenImeges:
    imagenes=[]

    def getImagen(self, ruta):
        for imagen in self.imagenes:
            if (ruta == imagen[0]):
                return imagen[1]

        # no esta guardado
        try:
            if (ruta[-3:] == "png"):
               icon = pygame.image.load(ruta).convert_alpha()
            else:
               icon = pygame.image.load(ruta).convert()
        except:
               log(4,"Imposible cargar imagen. %s" %(ruta))
               return pygame.Surface((0,0))
        self.imagenes.append([ruta,icon])
        return icon