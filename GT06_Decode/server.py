#!/usr/bin/env python
import socket, threading
import sqlite3
from datetime import datetime
import binascii
import re
import time

TCP_PORT = 4001
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
           
def GetCrc16(Data):
   crc16tab = (
   0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD, 0x6536, 0x74BF, 
   0x8C48, 0x9DC1, 0xAF5A, 0xBED3, 0xCA6C, 0xDBE5, 0xE97E, 0xF8F7, 
   0x1081, 0x0108, 0x3393, 0x221A, 0x56A5, 0x472C, 0x75B7, 0x643E, 
   0x9CC9, 0x8D40, 0xBFDB, 0xAE52, 0xDAED, 0xCB64, 0xF9FF, 0xE876, 
   0x2102, 0x308B, 0x0210, 0x1399, 0x6726, 0x76AF, 0x4434, 0x55BD, 
   0xAD4A, 0xBCC3, 0x8E58, 0x9FD1, 0xEB6E, 0xFAE7, 0xC87C, 0xD9F5, 
   0x3183, 0x200A, 0x1291, 0x0318, 0x77A7, 0x662E, 0x54B5, 0x453C, 
   0xBDCB, 0xAC42, 0x9ED9, 0x8F50, 0xFBEF, 0xEA66, 0xD8FD, 0xC974, 
   0x4204, 0x538D, 0x6116, 0x709F, 0x0420, 0x15A9, 0x2732, 0x36BB, 
   0xCE4C, 0xDFC5, 0xED5E, 0xFCD7, 0x8868, 0x99E1, 0xAB7A, 0xBAF3, 
   0x5285, 0x430C, 0x7197, 0x601E, 0x14A1, 0x0528, 0x37B3, 0x263A, 
   0xDECD, 0xCF44, 0xFDDF, 0xEC56, 0x98E9, 0x8960, 0xBBFB, 0xAA72, 
   0x6306, 0x728F, 0x4014, 0x519D, 0x2522, 0x34AB, 0x0630, 0x17B9, 
   0xEF4E, 0xFEC7, 0xCC5C, 0xDDD5, 0xA96A, 0xB8E3, 0x8A78, 0x9BF1, 
   0x7387, 0x620E, 0x5095, 0x411C, 0x35A3, 0x242A, 0x16B1, 0x0738, 
   0xFFCF, 0xEE46, 0xDCDD, 0xCD54, 0xB9EB, 0xA862, 0x9AF9, 0x8B70, 
   0x8408, 0x9581, 0xA71A, 0xB693, 0xC22C, 0xD3A5, 0xE13E, 0xF0B7, 
   0x0840, 0x19C9, 0x2B52, 0x3ADB, 0x4E64, 0x5FED, 0x6D76, 0x7CFF, 
   0x9489, 0x8500, 0xB79B, 0xA612, 0xD2AD, 0xC324, 0xF1BF, 0xE036, 
   0x18C1, 0x0948, 0x3BD3, 0x2A5A, 0x5EE5, 0x4F6C, 0x7DF7, 0x6C7E, 
   0xA50A, 0xB483, 0x8618, 0x9791, 0xE32E, 0xF2A7, 0xC03C, 0xD1B5, 
   0x2942, 0x38CB, 0x0A50, 0x1BD9, 0x6F66, 0x7EEF, 0x4C74, 0x5DFD, 
   0xB58B, 0xA402, 0x9699, 0x8710, 0xF3AF, 0xE226, 0xD0BD, 0xC134, 
   0x39C3, 0x284A, 0x1AD1, 0x0B58, 0x7FE7, 0x6E6E, 0x5CF5, 0x4D7C, 
   0xC60C, 0xD785, 0xE51E, 0xF497, 0x8028, 0x91A1, 0xA33A, 0xB2B3, 
   0x4A44, 0x5BCD, 0x6956, 0x78DF, 0x0C60, 0x1DE9, 0x2F72, 0x3EFB, 
   0xD68D, 0xC704, 0xF59F, 0xE416, 0x90A9, 0x8120, 0xB3BB, 0xA232, 
   0x5AC5, 0x4B4C, 0x79D7, 0x685E, 0x1CE1, 0x0D68, 0x3FF3, 0x2E7A, 
   0xE70E, 0xF687, 0xC41C, 0xD595, 0xA12A, 0xB0A3, 0x8238, 0x93B1, 
   0x6B46, 0x7ACF, 0x4854, 0x59DD, 0x2D62, 0x3CEB, 0x0E70, 0x1FF9, 
   0xF78F, 0xE606, 0xD49D, 0xC514, 0xB1AB, 0xA022, 0x92B9, 0x8330, 
   0x7BC7, 0x6A4E, 0x58D5, 0x495C, 0x3DE3, 0x2C6A, 0x1EF1, 0x0F78, 
   )
   # Codigo C.
   #   fcs = int("FFFF",16)
   #   i = 0
   #   while i < len(Data):
   #      intNumber = 0xFFFF
   #      intNumber = int((Data[i+1] << 8)) + int((Data[i]))
   #      print intNumber
   #      crc16tabIndex = (fcs ^ intNumber) & int("FF",16)
   #      fcs = (fcs >> 8) ^ crc16tab[crc16tabIndex]
   #      i = i + 2
   #   return fcs^0xffff
   
   fcs = 0xffff #// initialization
   i = 0
   nLength = len(Data)
   while(nLength>1):
         fcs = (fcs >> 8) ^ crc16tab[(fcs ^ Data[i-1]) & 0xff]
         nLength-=1
         i+=1
   return ~fcs #// negated
   
def SaveData(LatitudeF, LongitudF):
   fichero = "/home/ubuntu/GPS-data/gps-" + datetime.now().strftime("%Y-%m-%d") + ".sqlite"
   timestamp =  datetime.now().strftime("%y%m%d%H%M%S")
   gps_time  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   base = sqlite3.connect(fichero)
   c = base.cursor()
   c.execute('CREATE TABLE IF NOT EXISTS pos (id numeric PRIMARY KEY ,imei int,hora text, lat REAL, log REAL)')
   c.execute( "INSERT INTO pos (id,imei, hora, lat, log) VALUES ('"+ timestamp+"','22222','"+gps_time+"', '"+str(LatitudeF)+"', '"+ str(LongitudF)+"')")
   base.commit()
   base.close()
 
class ClientThread(threading.Thread):

    def __init__(self,ip,port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        print "[+] New thread started for "+ip+":"+str(port)


    def run(self):
        data = "dummydata"
        count =0
        clientsock.settimeout(60.0)
        while len(data):
            try:
               data = clientsock.recv(BUFFER_SIZE)
               print str(datetime.now())+" Received data:", data.encode("hex")
               self.DecodeData(bytearray(data))
               count = 0
            except:
               #time Out.
               response = bytearray([0x78 ,0x78 ,0x16 ,0x80 ,0x10 ,0x00 ,0x01 ,0xA9 ,0x67 ,0x44 ,0x57 ,0x58 ,0x58 ,0x2C ,0x30 ,0x30 ,0x30 ,0x30 ,0x30 ,0x30 ,0x23 ,0x00 ,0xA0 ,0x06 ,0x2D ,0x0D ,0x0A])         
               print  "-> TimeOut: Send responseCMD:"
               print binascii.hexlify(response)
               data = "AA"
               count +=1
               if (count >10):
                 print "-> Count > 10 sin respuesta. -> Close Connect."
                 clientsock.close()
                 return 
               try:
                 clientsock.send(response)
               except:
                 data = ""
                 print "-> Error Send Data -> Close Connect."
                 clientsock.close()
        print "[-] Client disconnected..."


    def DecodeData(self, data):
      if(len(data)==0):
         return
      if ((data[0] != 0x78) or (data[1] != 0x78)):
         return
      
      if(data[3] == 0x01):
         print "-> Trama Login."
      # Login:
         response = bytearray()
         response.append(0x78)
         response.append(0x78)
         response.append(0x05)
         response.append(0x01)
         response.append(data[12])
         response.append(data[13])
         Crc = GetCrc16(response)
         response.append((Crc& (0xff00))>>8)
         response.append(Crc& (0x00ff))
         response.append(0x0D)
         response.append(0x0A)
         print  "Send response:"
         print binascii.hexlify(response)
         clientsock.send(response)
         
         time.sleep(1)
         response = bytearray([0x78 ,0x78 ,0x16 ,0x80 ,0x10 ,0x00 ,0x01 ,0xA9 ,0x67 ,0x44 ,0x57 ,0x58 ,0x58 ,0x2C ,0x30 ,0x30 ,0x30 ,0x30 ,0x30 ,0x30 ,0x23 ,0x00 ,0xA0 ,0x06 ,0x2D ,0x0D ,0x0A])         
         print  "-> login: Send responseCMD:"
         print binascii.hexlify(response)
         clientsock.send(response)
         
      if(data[3] == 0x15) :
      # String data: 
        print "-> Trama String."
        strRsp = str(data)
        if (len(data) > 100):
            strRsp = str(data[9:-18])
        print str(strRsp)
        LatitudeF = 0.0
        LongitudF = 0.0
        m = re.search('LAT:N(.+?),', strRsp)
        if m:
           LatitudeF =  float(m.group(1))
        m = re.search('LON:W(.+?),', strRsp)
        if m:
           LongitudF =  float(m.group(1)) * -1
        print " Latitude: " + str(LatitudeF) + " Longitud: " + str(LongitudF)
        SaveData(LatitudeF, LongitudF)
      
      if((data[3] == 0x12) or(data[3] == 0x16)):
         print "-> Trama Dato."
         # posicion:
         satelites = (data[10] &(0x0f))
         if(satelites <= 3):
            print "pocos satelites."
            return
         LatitudeI =  (data[11]<< 24)  + (data[12]<< 16) + (data[13]<< 8) + data[14]
         LatitudeF = float(LatitudeI) / 30000.0
         LatitudeF /= 60.0
         LongitudI =  (data[15]<< 24)  + (data[16]<< 16) + (data[17]<< 8) + data[18]
         LongitudF = float(LongitudI) / 30000.0
         LongitudF /= -60.0 # en espana esta en el norte.
         
         print "Sat: "+ str(satelites) + " Latitude: " + str(LatitudeF) + " Longitud: " + str(LongitudF)
         SaveData(LatitudeF, LongitudF)
        
host = "0.0.0.0"
port = 4001

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,TCP_PORT))
threads = []


while True:
    tcpsock.listen(10)
    print "\nListening for incoming connections..."
    (clientsock, (ip, port)) = tcpsock.accept()
    clientsock.settimeout(600)
    newthread = ClientThread(ip, port)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
          
    
