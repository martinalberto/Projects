#!/usr/bin/env python

from utemper_public import * 
import RPi.GPIO as GPIO, time, os

PIN_DEFAULT = 2# Read RC timing using pin #2  
    # pin default.
	# it is the same the 0 in rev:1

FILE = "/tmp/ldr.var"

def RCtime (RCpin):
        global lastvalue
        reading = 0
        GPIO.setup(RCpin, GPIO.OUT)
        GPIO.output(RCpin, GPIO.LOW)
        time.sleep(0.2)
 
        GPIO.setup(RCpin, GPIO.IN)
        # This takes about 1 millisecond per loop cycle
        while (GPIO.input(RCpin) == GPIO.LOW):
                reading += 1
                if (reading>50000): # posible error hardware.
					break
        return reading
		
		
#Init del programa.
lastValue_Write = -1
lastvalues = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

valor=0
errores=1

#================================ INIT ============================
log(1,"Init read_ldr.py")
DEBUG = 1
GPIO.setmode(GPIO.BCM)

pinLdr = int(cread_config().read_config("Pin_LDR"))
if pinLdr < 1:
	log(4,"imposible leer 'Pin_LDR' en conf file: se supene default pi : "+str(PIN_DEFAULT) )
	pinLdr = PIN_DEFAULT
else:
	log(1,"lectura del pin: "+str(pinLdr)+ ". para la fotocelula.")
	
# ================================ BUCLE ==========================
while True:
		
		#Ciclo 1.
		lastvalues.pop(0)
		lastvalues.append(RCtime(pinLdr))
		
		valor= sum(lastvalues) / float(len(lastvalues))
		
		print ("Valor LDR: %f" %(valor))

		#save:
		if (valor>0 and valor<49000) and (lastValue_Write != valor):
			try:
				file = open(FILE, "w")
				file.write(str(valor))
				file.close()
				errores=1
				lastValue_Write = valor
			except:
				os.system('echo $(date  +"%F_%T")";4;READ_LDR;Impisible guardar valor en /tmp/ldr.var">>/var/utemp/logs.log')
				errores+=1
		else:
			errores+=1
			
		if (errores>10):
			os.system('echo $(date  +"%F_%T")";5;READ_LDR;Errores max KO">>/var/utemp/logs.log')
			os.system('echo $(date  +"%F_%T")";5;READ_LDR;Reboot">>/var/utemp/logs.log')
			if (os.path.isfile(FILE) ):
				os.remove(FILE)
			time.sleep(120)
			errores=1
        
		#sleep
		time.sleep(5*errores)
