#!/usr/bin/python
import gspread
import subprocess, time, Image, socket
from Adafruit_Thermal import *
import random
import time



printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

printer.printImage(Image.open('gfx/hello.png'), True)
printer.feed(1)
subprocess.call("./timetemp.py")

# Show IP address (if network is available)
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))
	printer.println('My IP address is ' + s.getsockname()[0])
except:
	printer.boldOn()
	printer.println('Network is unreachable.')
	printer.boldOff()

printer.inverseOn()
printer.setSize('L')
printer.println("     INGLES    ")
printer.setSize('S')
printer.inverseOff()

# Google Docs account email, password, and spreadsheet name.
GDOCS_EMAIL            = 'martinalberto@gmail.com'
GDOCS_PASSWORD         = 'Martin13'
GDOCS_SPREADSHEET_NAME = 'palabras_ingles'

def login_open_sheet(email, password, spreadsheet):
	"""Connect to Google Docs spreadsheet and return the first worksheet."""
	try:
		gc = gspread.login(email, password)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except:
		#printer.println("Unable to login and get spreadsheet.  Check email, password, spreadsheet name.") 
		sys.exit(1)

# Login if necessary.
worksheet = login_open_sheet(GDOCS_EMAIL, GDOCS_PASSWORD, GDOCS_SPREADSHEET_NAME)

list_of_lists = worksheet.get_all_values()
i=1
lista=[]
for value in list_of_lists:
   lista.append([value[0],value[1], value[2], value[3],i])
   i+=1

#ordenar por veces:
lista.sort( key=lambda veces: veces[2])
lista = lista[:30]
random.shuffle(lista)
print lista


#print List Ingles.
result = []
for i in range(0,9):
	printer.println(lista[i][0].encode('ascii', 'ignore'))
	result.append(lista[i][1].encode('ascii', 'ignore'))
	worksheet.update_cell(lista[i][4], 3, int(lista[i][2])+1)
	
result.append("\n")
	
#print List spaon
for i in range(10,19):
	printer.println(lista[i][1].encode('ascii', 'ignore'))
	result.append(lista[i][0].encode('ascii', 'ignore'))
	worksheet.update_cell(lista[i][4], 3, int(lista[i][2])+1 )
	
printer.justify('L')
# print reslt
printer.println("********************************")
printer.println("")

for i in range(len(result)):
	printer.print_(result[i])
	printer.print_(" | ")
	
printer.feed(1)
printer.printImage(Image.open('gfx/goodbye.png'), True)
time.sleep(20)
printer.feed(3)
subprocess.call("sync")
subprocess.call(["shutdown", "-h", "now"])