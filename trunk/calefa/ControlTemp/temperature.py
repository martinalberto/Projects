#!/usr/bin/python

import subprocess
import re
import time
import datetime
import pygal
import gspread
import os, sys

# ===========================================================================
# Read Temp
# ===========================================================================
class ClassTemp:
    
    def __init__(self):
      self.incio=1
      self.temp=0
      self.hume=0
      self.lastTimeRead=0
      self.dateRead = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
      try:
            self.ReadTemp()
      except:
            print "Error: no se pude leer la temperatura"
            self.incio=0
            return
      self.lastTimeRead=time.time()
      
    def SucesoTemp (self):
       if (time.time()-self.lastTimeRead>190):
           self.ReadTemp()
           self.lastTimeRead=time.time()
           
       return (self.GetData())
       
    def GetData(self):
       return ([self.dateRead, self.temp, self.hume])
       
    def ReadTemp(self):
      print "leemos la temp"
      # Run the DHT program to get the humidity and temperature readings!
      if self.incio==0:
            return False
      
      output = subprocess.check_output(["Adafruit_DHT", "11", "8"]);
      print output
      matches = re.search("Temp =\s+([0-9.]+)", output)
      if (not matches):
            time.sleep(3)
            return False
      self.temp = float(matches.group(1))
      
      # search for humidity printout
      matches = re.search("Hum =\s+([0-9.]+)", output)
      if (not matches):
            time.sleep(3)
            return False
      self.hume = float(matches.group(1))
      
      # save date.
      self.dateRead= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
      print self.dateRead
      print "Temperature: %.1f C" % self.temp
      print "Humidity:    %.1f %%" % self.hume
      
      return True

