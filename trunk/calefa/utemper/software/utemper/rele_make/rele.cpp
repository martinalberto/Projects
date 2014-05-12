/*

 'codesend' hacked from 'send' by @justy
 
 - The provided rc_switch 'send' command uses the form systemCode, unitCode, command
   which is not suitable for our purposes.  Instead, we call 
   send(code, length); // where length is always 24 and code is simply the code
   we find using the RF_sniffer.ino Arduino sketch.

 Usage: ./codesend decimalcode
 (Use RF_Sniffer.ino to check that RF signals are being produced by the RPi's transmitter)
 */

#include "RCSwitch.h"
#include <stdlib.h>
#include <stdio.h>
     

int rele= 1;
int tiempo_espera=0;

int read_rele(void){
   FILE * fp;
   int temp_valor=-1;
    // open 
   fp = fopen("/tmp/rele.var", "r");
   if (fp == NULL)
   {
       printf("ERROR al abrir el fichero: /tmp/rele.var");
       return 0;
    }
    
    //read
    
    if (fscanf (fp, "%u", &temp_valor)!=1)
    {
        printf("ERROR al leer el fichero: /tmp/rele.var");
       return 0;
    }
    // close
    
    if( fclose(fp) )
    {
      printf( "Error: fichero /tmp/rele.var NO CERRADO\n" );
      return -1;
   }
    
    if (temp_valor == -1)
   {
       printf( "Valor no inicalizado /tmp/rele.var\n" );
       delay(20000);
      return 0;
   }
   else if (0<temp_valor>1)
   {
       printf ("Valor no se entiende no se sabe que es >1 o <0");
       return 0;
   }
   else
    rele = int(temp_valor) ;  // OK
   return 1;
}

int read_espera(void){
    FILE * fp;
    int temp_valor=-1;
    // open 
    fp = fopen("/tmp/time_espera.var", "r");
    if (fp == NULL)
    {
       printf("ERROR al abrir el fichero: /tmp/time_espera.var");
       return 0;
    }   
    //read
    
    if (fscanf (fp, "%u", &temp_valor)!=1)
    {
        printf("ERROR al leer el fichero: /tmp/time_espera.var");
       return 0;
    }
    // close    
    if( fclose(fp) )
    {
      printf( "Error: fichero /tmp/time_espera.var NO CERRADO\n" );
      return -1;
    }
    
    if (temp_valor == -1)
    {
       printf( "Valor no inicalizado /tmp/time_espera.var\n" );
       delay(20000);
      return 0;
    }
    else if (0<temp_valor>99)
    {
       printf ("Valor no se entiende no se sabe que es >1 o <0");
       return 0;
    }
    else
        tiempo_espera= temp_valor ;  // OK
   return 1;
}

int send433(RCSwitch mySwitch, int code)
{

    
}
int main(int argc, char *argv[]) {
    
        // This pin is not the first pin on the RPi GPIO header!
    // Consult https://projects.drogon.net/raspberry-pi/wiringpi/pins/
    // for more information.
    
    // INT
    int PIN_433 = 0;
    int PIN_RELE =22;
    
    
    int code= 0;
    int errores=0;
    int last_value=0;
    int result=-1;
    
    if (wiringPiSetup () == -1) return 1;
	printf("sending code[%i]\n", code);
	RCSwitch mySwitch = RCSwitch();
	mySwitch.enableTransmit(PIN_433);
    
     pinMode (PIN_RELE, OUTPUT) ;
     digitalWrite (PIN_RELE, 0);
    
    while (errores<20)
    {
        
        result = read_rele();
        if (result==-1 )
        {
             printf ("ERRoR Grave salimos ");
             return 1;
        }
        else if (result!=1)
        {
            errores++;
            delay(200);
        }
        else
        {
            printf ("OK!!!!!! \n");
       
            
            result = read_espera();
            if (result==-1 )
            {
                 printf ("ERRoR Grave salimos ");
                 return 1;
            }
            else if (result!=1)
            {
                errores++;
                delay(200);
            }
            else
            {
                if (last_value!= rele)
                {
                    digitalWrite (PIN_RELE, rele);
                    last_value =rele;
                }
                
                code = (rele*100)+tiempo_espera;
                mySwitch.send(code, 24);

            }
        }
     delay(200);
    }
    
	return 0;

}
