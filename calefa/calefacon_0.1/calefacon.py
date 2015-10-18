#!/usr/bin/python

#Google.
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom
import getopt
import sys, os
import string
import time, datetime
from time import sleep

#Rele.
import RPi.GPIO as GPIO
errores_rele=0


RELE1 = 18
RELE2 = 7
STATUSLED=16

#espera entre busqueda y  busqueda. seg
WAIT_TIME=600

text_event=""

def Start_Google():
       global cal_client
       
       print "Start  Google API...."
       cal_client = gdata.calendar.client.CalendarClient(source='Google-Calendar_Python_Sample-1.0')
       cal_client.ClientLogin("!!!!!!!MAIL !!!!!!!!",  "!!!!!!!!!!!PASS !!!!!!!!!", cal_client.source)
       sys.stderr.write("Start  Google API [OK]\n")

def googleCa():
       global cal_client
       global text_event
       
       rc=GPIO.LOW
       text_event=""
       
       query = gdata.calendar.client.CalendarEventQuery()
       query.start_min = time.strftime("%Y-%m-%dT%H:%M:%S.000+01:00", time.localtime())
       query.start_max = time.strftime("%Y-%m-%dT%H:%M:%S.000+01:00", time.localtime(time.time()+300))
       # los siguientes 300 seg.
       

       #print query.start_min
       #print query.start_max
       feed = cal_client.GetCalendarEventFeed(q=query)
       
       #print 'Events on Primary Calendar: %s' % (feed.title.text)
       for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
        for a_when in an_event.when:
            rc=GPIO.HIGH
            try:
                utText_event = "Event: '" + str(an_event.title.text) +"' Entre " + str(a_when.start) + " y " + str(a_when.end)
                text_event= utText_event.encode("ascii","ignore")
            except:
                text_event="Nuevo evento: EROOR nombre.!!" 
                sys.stderr.write("Nuevo evento: EROOR nombre.!!\n")

       return rc

def empezar_rele():     
     print "empezar_rele...."
     GPIO.setmode(GPIO.BCM)
     GPIO.setup(RELE1, GPIO.OUT)
     GPIO.setup(RELE2, GPIO.OUT)
     GPIO.setup(STATUSLED, GPIO.OUT)
     
     GPIO.output(RELE1, GPIO.HIGH)
     GPIO.output(RELE2, GPIO.HIGH)
     GPIO.output(STATUSLED, GPIO.LOW)
     print "empezar_rele %d y %d [OK]" %(RELE1, RELE2)
     print "Estado incial All GPIO.HIGH" 
     sys.stderr.write("empezar_rele %d y %d [OK]  todos a GPIO.HIGH\n" %(RELE1, RELE2))


def cambiarRele(Estado):
     global errores_rele
     try:
        GPIO.output(RELE2, Estado)
        GPIO.output(STATUSLED, Estado)
        errores_rele=0
     except:
        print"ERRROR!!! No se puede.num_Rele"
        sys.stderr.write( "ERRROR!!! No se puede.num_Rele\n" )
        errores_rele+=1
        sleep (33)
        #if (errores_rele> 3):
        #  sys.stderr.write("ERROR: Max numero de erorres reiniciamos:! ")
        #  os.system("reboot")

def startLog():
    sys.stderr.write('-------------------------------------------\n')
    sys.stderr.write('%s Started Log\n' %(datetime.datetime.now()) )
    
def main():
     global text_event
     global WAIT_TIME
     
     old_estado = 3
     old_time= 0
     
     #int
     startLog()
     empezar_rele()
     Start_Google()
     while (1):

          estado= googleCa()
          cambiarRele(estado)

          if (estado != old_estado):
               print "IMP: cambiio de estado: antes: %d ahora: %d" %(old_estado, estado)
               sys.stderr.write( "IMP: %s : cambiio de estado: antes: %d ahora: %d\n" %(datetime.datetime.now(), old_estado, estado))
               try:
                  sys.stderr.write(text_event)
                  text_send="curl http://www.XXXXXXXXXXXXX.com/calefa_alb.php?q=IMP_cambioEstado_%d_%d\n" %(old_estado, estado)
                  sys.stderr.write(text_send)
                  os.system(text_send)
               except:
                  sys.stderr.write( "Nuevo evento ERROR al impriirlo.\n")
                  sys.stderr.write("%s Nuevo evento ERRO al impriirlo.\n" %(datetime.datetime.now()) )
                  
               old_estado = estado 
               old_time =  time.time()
                  
          #control del led status.
          for x in range(0, WAIT_TIME):
               GPIO.output(STATUSLED, GPIO.HIGH)
               GPIO.output(STATUSLED, GPIO.LOW)
               sleep((0.5-(estado*0.3)))
               GPIO.output(STATUSLED, GPIO.LOW)
               GPIO.output(STATUSLED, GPIO.HIGH)
               sleep((0.5-(estado*0.3)))
          try:
                  text_send="curl http://www.XXXXXXXXXXXXX.com/calefa_alb.php?a=estado_%d\n" %(estado)
                  sys.stderr.write(text_send)
                  os.system(text_send)
          except: 
                  sys.stderr.write( "Error: %s calefa_alb.php?a=estado_% !!!!\n" %(datetime.datetime.now()) )

          if (estado==GPIO.HIGH) and (time.time()-old_time>7200):
               print "Mucho tiempo encendido: apagamos 30 seg."
               sys.stderr.write("%s Mucho tiempo encendido: apagamos 30 seg.\n" %(datetime.datetime.now()))
               cambiarRele(GPIO.LOW)
               sleep (30)
               cambiarRele(estado)
               old_time= time.time()
               
if __name__ == '__main__':
  main()
