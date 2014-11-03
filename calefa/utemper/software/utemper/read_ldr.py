#!/usr/bin/env python
 
# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier verions
# are not fast enough!
 
import RPi.GPIO as GPIO, time, os

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

lastvalue1 = 0
lastvalue2 = 0
lastvalue3 = 0
valor=0
errores=1

PIN = 2# Read RC timing using pin #2
	# it is the same the 0 in rev:1

		 
os.system('echo $(date  +"%F_%T")";0;READ_LDR;Init read_ldr.py">>/var/utemp/logs.log')
DEBUG = 1
GPIO.setmode(GPIO.BCM)


while True:
		
		#Ciclo 1.
		lastvalue1 = RCtime(PIN)
		lastvalue2 = RCtime(PIN)
		lastvalue3 = RCtime(PIN)
		valor= (lastvalue1 + lastvalue2 + lastvalue3)/3
		
		print ("Valores: %d, %d %d = %d", (lastvalue1, lastvalue2, lastvalue3, valor))
		
		#save:
		if (valor>0 and valor<49000):
			try:
				file = open("/tmp/ldr.var", "w")
				file.write(str(valor))
				file.close()
				errores=1
			except:
				os.system('echo $(date  +"%F_%T")";4;READ_LDR;Impisible guardar valor en /tmp/ldr.var">>/var/utemp/logs.log')
				errores+=1
		else:
			errores+=1
			
		if (errores>10):
			os.system('echo $(date  +"%F_%T")";5;READ_LDR;Errores max KO">>/var/utemp/logs.log')
			os.system('echo $(date  +"%F_%T")";5;READ_LDR;Reboot">>/var/utemp/logs.log')
			time.sleep(90)
			exit(1)
        
		#sleep
		time.sleep(5*errores)
