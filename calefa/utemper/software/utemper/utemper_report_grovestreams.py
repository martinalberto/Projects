#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import httplib
import StringIO
import gzip
import xively
import datetime
import time
from utemper_public import *

class calssReport_Grovestreams:
    old_time = 0
    time_lastUpdate = 0
    oldValores=[-1,-1,-1,-1]
 
   def __init__(self):
        #GroveStreams Settings
        self.api_key = "8fd02458-1eb1-38c9-8056-ad660b25efe0"
        
        #Optionally compress the JSON feed body to decrease network bandwidth
        self.compress = True
        self.url = '/api/feed'
        
        #Connect to the server
        self.conn = httplib.HTTPConnection('www.grovestreams.com')

   def suceso(self):
      Tiempo = time.time()
      if(time.time() - self.old_time>200) and (gv.internet == 1): # cada 200 seg se envia el estado.
         valores = [gv.temperatura, gv.rele, gv.tiempo_temp, gv.luzValor, gv.temperatura_max]
         if((Tiempo -self.old_time>300) or (valores!=self.oldValores)):
         
            self.component_id = str(gv.number_equipo)
            if (self.SendData(valores)):# send values.
               self.old_time=Tiempo
               self.oldValores = valores
    

   def compressBuf(buf):
       #This method is used to compress a string
       zbuf = StringIO.StringIO()
       zfile = gzip.GzipFile(mode = 'wb',  fileobj = zbuf, compresslevel = 9)
       zfile.write(buf)
       zfile.close()
       return zbuf.getvalue()
       
   def SendData(self, valores):
   
        temperature_val = random.randrange(-10, 40)
        humidity_val = random.randrange(0, 100)
       
        #Assemble feed as a JSON string (Let the GS servers set the sample time)
        samples = []
        samples.append({ 'compId' : self.component_id, 'streamId' : 'temp', 'data' : valores[0] })
        samples.append({ 'compId' : self.component_id, 'streamId' : 'rele', 'data' : valores[1] })
        samples.append({ 'compId' : self.component_id, 'streamId' : 'tempExt', 'data' : valores[2] })
        samples.append({ 'compId' : self.component_id, 'streamId' : 'Luz', 'data' : valores[3] })
        samples.append({ 'compId' : self.component_id, 'streamId' : 'Gente', 'data' : valores[4] })
        
        #Uncomment below to include the sample time - milliseconds since epoch
        #now = datetime.datetime.now()
        #sample_time = int(time.mktime(now.timetuple())) * 1000
        #samples = []
        #samples.append({ 'compId': component_id, 'streamId' : 'temperature', 'data' : temperature_val, 'time' : sample_time })
        #samples.append({ 'compId': component_id, 'streamId' : 'humidity', 'data' : humidity_val, 'time' : sample_time  })
       
        json_encoded = json.dumps(samples);
       
        try:           
            if self.compress:
                #Compress the JSON HTTP body
                body = self.compressBuf(json_encoded)
 
                print(
               log(0,'SendData: Compressed feed ' + str(100*len(body) / len(json_encoded)) + '%')
                headers = {"Content-Encoding" : "gzip" , "Connection" : "close",
                           "Content-type" : "application/json", "Cookie" : "api_key="+self.api_key}
               
                #GS limits feed calls to one per 10 seconds per outward facing router IP address
                #Use the ip_addr and headers assignment below to work around this
                # limit by setting the below to this device's IP address
                #ip_addr = "192.168.1.72"
                #headers = {"Content-Encoding" : "gzip" , "Connection" : "close", "Content-type" : "application/json", "X-Forwarded-For" : ip_addr, "Cookie" : "api_key="+api_key}
               
            else:
                #No Compression
                body = json_encoded
                headers = {"Connection" : "close", "Content-type" : "application/json",
                           "Cookie" : "api_key="+self.api_key}
 
                #GS limits calls to 10 per second per outward facing router IP address
                #Use the ip_addr and headers assignment below to work around this
                # limit by setting the below to this device's IP address
                #ip_addr = "192.168.1.72"
                #headers = {"Connection" : "close", "Content-type" : "application/json", "X-Forwarded-For" : ip_addr, "Cookie" : "api_key="+api_key}
               
            log(1,'Uploading Report to: ' + self.url)
           
            #Upload the feed to GroveStreams
            self.conn.request("PUT", self.url, body, headers)
             
            #Check for errors
            response = self.conn.getresponse()
            status = response.status
           
            if status != 200 and status != 201:
                try:
                    if (response.reason != None):
                        log(3,'HTTP Failure Reason: ' + response.reason + ' body: ' + response.read())
                    else:
                        log(3,'HTTP Failure Body: ' + response.read())
                except Exception:
                    log(3,'HTTP Failure Status: %d' % (status) )
       
        except Exception as e:
            log(4,'HTTP Failure: ' + str(e))
       
        finally:
            if self.conn != None:
                self.conn.close()
