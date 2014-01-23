# coding: utf-8
#!/usr/bin/python

# Xively Temperatura SoC Python script by @AlexCorvis84
# Agradecimientos: www.geekytheory.com

import os, sys
import csv
import xively
import datetime
import pygal
import time
from pygal.style import CleanStyle

class calssReport:
    # Variables personales
    FEED_ID=""
    API_KEY=""
    
    NameFileTemp= "/home/pi/calefa/Reg_temp.csv"
    
    def __init__(self):
        self.inicio=0
        self.old_time=0
        self.oldValores=["",-1,-1,-1]
        
        api = xively.XivelyAPIClient(calssReport.API_KEY)
        self.feed = api.feeds.get(calssReport.FEED_ID)
        self.inicio=1
            


    def suceso(self,valores):
        if ( time.time()-self.old_time>900) or (valores!=self.oldValores):
            # Save values.
            print "suceso report entramos."
            
            self.old_time=time.time()
            self.oldValores = valores            
            
            self.SendDataxively(valores)
            self.SaveFileValues(valores)
 
    def SendDataxively(self,valores):
        if (self.inicio==1):
             #guardar valores.
            now = datetime.datetime.utcnow()
            self.feed.datastreams = [
            xively.Datastream(id='Temperatura', current_value=valores[0], at=now),
            xively.Datastream(id='horarios', current_value=valores[2], at=now),
            xively.Datastream(id='humedad', current_value=valores[1], at=now),
            xively.Datastream(id='Activado', current_value=valores[3], at=now),
            ]
            self.feed.update()
            print "suceso Report: Se ha actulizado los valores."
            
            
    def SaveFileValues(self,valores): 
      # open files.
      sys.stderr.write( "SaveFileValues: Save Value " + str(valores)  )
      try:
          f = open(calssReport.NameFileTemp,"a")
      except IOError, (strerror):
          sys.stderr.write( "SaveFileValues: I/O error: %s\n" % (strerror))
          return
          
      cvsOutput = csv.writer(f, dialect='excel', delimiter=';', quotechar='"')
      cvsOutput.writerow([ time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), valores[0],valores[1],valores[2],valores[3] ])
      
      #close the opened files
      sys.stderr.write( "SaveFileValues: Closing the Source file... ")
      try:
          f.close()
      except IOError, (strerror):
          sys.stderr.write( "SaveFileValues: I/O error: %s\n" % (strerror))
          return
"""
      
    def CreateGrafic (tdata, hdata):
      # all data graph
      line_chart = pygal.DateY(style=CleanStyle, width=1200,order_min=-1,x_title='Time',x_labels_major_every=6,x_label_rotation=20)
      line_chart.title = 'Temperature & Humidity'
      line_chart.add('Temperature *C', tdata)
      line_chart.add('Humidity %', hdata, secondary=True) 
      line_chart.render_to_file('/tmp/temp-hum.svg')


    def ReadTempValue ():
      # open files.
      sys.stderr.write( "SaveTempValue: Save Value of temp: %s " %text )
      try:
          f = open(calssReport.NameFileTemp,"r")
      except IOError, (strerror):
          sys.stderr.write( "SaveTempValue: I/O error: %s\n" % (strerror))
          return

      for line in f.readlines():
          line = re.sub( r"\n", r"", line)
          line = line.split("|")
          matrixtTemp.append([line[0],line[1]])
          matrixtHume.append((line[0],line[3]))
          
      #close the opened files
      sys.stderr.write( "SaveTempValue: Closing the Source file... ")
      try:
          f.close()
      except IOError, (strerror):
          sys.stderr.write( "SaveTempValue: I/O error: %s\n" % (strerror))
          return
                
                

    from datetime import datetime, timedelta
    datey = pygal.DateY(x_label_rotation=20)
    datey.add("Visits", [
        (datetime(2013, 1, 2), 300),
        (datetime(2013, 1, 12), 412),
        (datetime(2013, 2, 2), 823),
        (datetime(2013, 2, 22), 672)
    ])
    datey.render()
    
    
    
    from aa import DHT_Temp
    temp=DHT_Temp()
    
"""
