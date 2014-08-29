import os
import glob
import time

#Init del programa.
os.system('echo $(date  +"%F_%T")";0;READ_TEMP;Init read_temp.py">>/var/utemp/logs.log')

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

os.system('echo $(date  +"%F_%T")";0;READ_TEMP;modulos  w1-gpio y w1-therm OK">>/var/utemp/logs.log')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '10*')[0]
device_file = device_folder + '/w1_slave'

os.system('echo $(date  +"%F_%T")";0;READ_TEMP;encontrados device_file OK">>/var/utemp/logs.log')

errores = 1

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        #temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

#bucle
while True:
        temp = read_temp()
        time.sleep(5*errores)
        
        if (temp>2 and temp<40):
			try:
				file = open("/tmp/temp.var", "w")
				file.write(str(temp))
				file.close()
				errores=1
			except:
				os.system('echo $(date  +"%F_%T")";4;READ_TEMP;Impisible guardar valor en /tmp/temp.var">>/var/utemp/logs.log')
				errores+=1
        else:
			errores+=1
			
        if (errores>7):
            os.system('echo $(date  +"%F_%T")";5;READ_TEMP;Errores max KO">>/var/utemp/logs.log')
            os.system('echo $(date  +"%F_%T")";5;READ_TEMP;Exit">>/var/utemp/logs.log')
            time.sleep(90)
            exit(1)
            
