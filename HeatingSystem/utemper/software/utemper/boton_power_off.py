
from time import sleep
import os
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN)
 
while True:
        if ( GPIO.input(15) == 0 ):
			sleep(2);
			if ( GPIO.input(15) == 0 ):
				os.system(' echo "boton pulsado apagamos todo el sistema" | wall')
				sleep(0.2)
				os.system('shutdown -h now')
			else:
				os.system("echo 'boton pulsado cerramos programas bash y python.'  | wall")
				sleep(0.2)
				os.system('pkill bash')
				os.system('killall bash')
				os.system('killall python')
				os.system('pkill rele')
				os.system('pkill bash')
        sleep(0.2);