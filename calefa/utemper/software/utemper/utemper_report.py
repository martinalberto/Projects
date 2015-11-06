#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xively
import datetime
import time
import utemper_report_grovestreams
from utemper_public import *

class calssReport:

    old_time = 0
    time_lastUpdate    = 0
    oldValores=[-1,-1,-1,-1]
    inicio = 0
    # Variables personales
    xively_id = "-1"
    xively_key = "-1"
    FEED_ID="1844265561"
    API_KEY="3QTvK8CwHnYoJmHsp2OiVdrwE1NEkGX9YmenXwu4Fgz9iAhj"
    
    def __init__(self):
        self.xively_id = cread_config().read_config("xively_id")
        self.xively_key = cread_config().read_config("xively_key")
        self.Init_xively()
        self.Grovestreams = utemper_report_grovestreams.calssReport_Grovestreams()
        
    def Init_xively(self):
        if gv.internet!= 1:
            log(3, "No hay Internet. Imposible Iniciar reportes xively.")
            return False
        if ((self.xively_id == "-1") or (self.xively_key == "-1")):
            log(0, "No hay configuracion xively.")
            return False
        try:
            api = xively.XivelyAPIClient(self.xively_key)
            self.feed = api.feeds.get(self.xively_id)
            self.inicio=1
            log(2, "inicializar Report xively OK.")
            return True
        except:
            self.inicio=0
            log(3, "Imposible poder Iniciar xively Reportes.")
            return False
            
    def suceso(self):
        valores = [gv.temperatura, gv.rele, gv.tiempo_temp, gv.luzValor, gv.temperatura_max]
        Tiempo = time.time()
        if (self.inicio != 1): # No inicializado.
            if(Tiempo - self.old_time>300) and (gv.internet == 1):
                self.old_time=Tiempo
                log(1,"Intentamos self.Init_xively()")
                if self.Init_xively():
                    log(1,"Class Report KO ->  OK Bien !")
        # Si Inicializado.
        else:
            if(time.time() - self.old_time>100) and (gv.internet == 1): # cada 100 seg se envia el estado.
                if((Tiempo -self.old_time>300) or (valores!=self.oldValores)):                    
                    if (self.SendDataxively(valores)):# send values.
                        self.old_time=Tiempo
                        self.oldValores = valores
                        
        self.Grovestreams.suceso()
        
    def SendDataxively(self, valores):
        if (self.inicio != 1):
            log(5,"Intentamos enviar reportes Sin Inicialiar. ERROR!")
            return
        try:
            #guardar valores.
            now = datetime.datetime.utcnow()
            self.feed.datastreams = [
            xively.Datastream(id='Temperatura', current_value=valores[0], at=now),
            xively.Datastream(id='Activado', current_value=valores[1], at=now),
            xively.Datastream(id='TemperaturaExt', current_value=valores[2], at=now),
            xively.Datastream(id='Luz', current_value=valores[3], at=now),
            xively.Datastream(id='TemperaturaMax', current_value=valores[4], at=now),
            ]
            self.feed.update()
            log(1, "suceso Report: Se ha actulizado los valores.")

        except:
            gv.inicio = 0
            log(3, "Imposible poder enviar reporte xively")
            return False
        return True