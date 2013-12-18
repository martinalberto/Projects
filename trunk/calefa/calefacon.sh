#!/bin/bash
LOG_FILE=/var/log/calefa.log



is_alive_ping()
{
  ping -c 1 $1 > /dev/null
  if [ $? -eq 0 ] ; then
     echo "there are internt conection.."| tee -a ${LOG_FILE}
     return 
  else
     echo "No ay internet probamos otra vez en 60 seg"| tee -a ${LOG_FILE}
     sleep 60
     ping -c 1 $1 > /dev/null
     if [ $? -eq 0 ] ; then
        echo "there are internt conection.."
        return 
     else
        echo "No ay internet probamos otra vez en 180 seg"| tee -a ${LOG_FILE}
        sleep 180
        ping -c 1 $1 > /dev/null
        if [ $? -eq 0 ] ; then
           echo "there are internt conection.."
           return 
        else
          echo "No ay internet Reiniciamos equipo."| tee -a ${LOG_FILE}
          reboot
        fi
     fi
  fi
}

send_Mail()
{
    if test `find "/var/log/sendmail.log" -mmin +600`
    then
        echo "Intenta mandar mail con menos de 10 min."| tee -a ${LOG_FILE}
        echo "Se rechecha mail."| tee -a ${LOG_FILE}
        return
    fi
    
    /usr/sbin/sendmail -v !!!! MAIL !!!!!!! < ${LOG_FILE} 1>/dev/null 2>>${LOG_FILE}
    if [ $? -eq 0 ] ; then
       rm /var/log/calefa.log
       rm /var/log/sendmail.log
       date >/var/log/sendmail.log
    fi
}

Start_esto()
{
    
    echo "Start Raspberry pi..." | tee -a ${LOG_FILE}
    python /home/pi/calefa/StartCalefa.py
    
    sleep 60

    date | tee -a ${LOG_FILE}
    hostname ticsistemas.com 1>> ${LOG_FILE} 2>&1
}



# INIT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


Start_esto


# Check status and send mails.
is_alive_ping 8.8.8.8 | tee -a ${LOG_FILE}
ifconfig | grep "addr"| tee -a ${LOG_FILE}
echo "Demeg Errors: " | tee -a ${LOG_FILE}
dmesg -n1 | tee -a ${LOG_FILE}
dmesg | grep -i error | tee -a ${LOG_FILE}
send_Mail




#start program.!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
while true
do
    echo "#start program.calefacon.py... " | tee -a ${LOG_FILE}  
    python /home/pi/calefa/calefacon.py 2>&1 | tee -a ${LOG_FILE}  
    echo "Server 'calefacon.py' crashed with exit code $?.  Respawning.." >&2 | tee -a ${LOG_FILE}
    sleep 30
    
    is_alive_ping 8.8.8.8 | tee -a ${LOG_FILE}
    
    send_Mail
done

