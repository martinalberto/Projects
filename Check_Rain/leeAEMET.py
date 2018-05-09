import time, os
import urllib2
import csv
import re

import logging
import telegram
from telegram.error import NetworkError, Unauthorized

try:
   print "Start leeAEMET_telegram.py..."
   # 1.- Descargamos el fiechero. -> This Case Media de Rioseco
   response = urllib2.urlopen('http://www.aemet.es/es/eltiempo/observacion/ultimosdatos_2604B_resumenes-diarios-anteriores.csv?k=cle&l=2604B&datos=det&w=2&f=tmax&x=')
   data = response.read()

   File = file("/tmp/temp_file.csv", 'w')
   File.write(data)
   File.close()

   # 2.- Leemos el fichero.
   File = open("/tmp/temp_file.csv", 'rt')
   reader= csv.reader(File)
   for row in reader:
      if(reader.line_num == 5):
          if ((len(row[6]) ==0) and (len(row[0]) !=0)): # Error de la AEMET en sus estacion.
            print "Tamano lluvia 0."
            exit()
          lluvia = float(row[6]) 
          dia = row[0]
          break

   File.close()

   # 3.- Comprobamos.
   if(lluvia == 0):
      exit()
      
   #Enviamos!
   dia = re.sub(r"20..", '', dia)
   texto = "El dia " + dia + "llovio en Rioseco: " + str(lluvia) + "L"
   
   bot = telegram.Bot("*******************************")# Repmplazar por BOT-ID
   
   #Yo
   bot.send_message (*********, texto) # Repmplazar por Chat-ID
   print texto
   
except Exception,e: 
   bot.send_message ((*********,, "ERROR: Bot Check lluvia.")# Repmplazar por Chat-ID
   print str(e)
