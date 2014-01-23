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
import string, re
import time, datetime


class classHorrarios:

    def __init__(self):
       print "Start  Google API...."
       self.cal_client = gdata.calendar.client.CalendarClient(source='Google-Calendar_Python_Sample-1.0')
       self.cal_client.ClientLogin("MAIL",  "CONTRASENA", self.cal_client.source)
       sys.stderr.write("Start  Google API [OK]\n")
       self.old_time=0
       self.oldStatus=5 # grados.
       
    def suceso(self):
        
        if ( time.time()-self.old_time>300) :
            print "suceso Calendar ReadGoogleNow entramos."
            # Save values.
            self.old_time=time.time()
            rc = self.ReadGoogleNow()
            self.oldStatus=rc
            
        return (self.oldStatus)
            
    def ReadGoogleNow(self):
       rc=0
       query = gdata.calendar.client.CalendarEventQuery()
       query.start_min = time.strftime("%Y-%m-%dT%H:%M:%S.000+01:00", time.localtime())
       query.start_max = time.strftime("%Y-%m-%dT%H:%M:%S.000+01:00", time.localtime(time.time()+300))
       # los siguientes 300 seg.
       

       #print query.start_min
       #print query.start_max
       feed = self.cal_client.GetCalendarEventFeed(q=query)
       
       #print 'Events on Primary Calendar: %s' % (feed.title.text)
       for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
        for a_when in an_event.when:
            print"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            try:
                utText_event = "Event: '" + str(an_event.title.text) +"' Entre " + str(a_when.start) + " y " + str(a_when.end)
                text_event= utText_event.encode("ascii","ignore")
            except:
                text_event="Nuevo evento: EROOR nombre.!!" 
                sys.stderr.write("Nuevo evento: EROOR nombre.!!\n")
                
            try:
                temp = re.sub( r"\,", r".", str(an_event.title.text))
                print "temp: leida " + temp
                rc =float(temp)# grados.
            except:
                rc = 99# grados.
       return rc
