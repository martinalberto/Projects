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
#include <time.h>

// INT
int PIN_433 = 0;
int PIN_RELE =8; // cuidado usamos la libreira  wiringpi
	
int rele= 0;
int tiempo_espera=10;

int log (int nivel,char *text )
{

	
}

int read_rele(void){
   FILE * fp;
   int temp_valor=-1;
    // open 
   fp = fopen("/tmp/rele.var", "r");
   if (fp == NULL)
   {
       printf("ERROR al abrir el fichero: /tmp/rele.var\n");
       return 0;
    }
    
    //read
    
    if (fscanf (fp, "%u", &temp_valor)!=1)
    {
        printf("ERROR al leer el fichero: /tmp/rele.var\n");
       return 0;
    }
    // close
    
    if( fclose(fp) )
    {
      printf( "Error: fichero /tmp/rele.var NO CERRADO\n" );
      exit(1);
   }
    
    if (temp_valor == -1)
   {
       printf( "Valor no inicalizado /tmp/rele.var\n" );
       delay(20000);
      return 0;
   }
   else if (0<temp_valor>1)
   {
       printf ("Valor no se entiende no se sabe que es >1 o <0\n");
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
       printf("ERROR al abrir el fichero: /tmp/time_espera.var\n");
       return 0;
    }   
    //read
    
    if (fscanf (fp, "%u", &temp_valor)!=1)
    {
        printf("ERROR al leer el fichero: /tmp/time_espera.var\n");
       return 0;
    }
    // close    
    if( fclose(fp) )
    {
      printf( "Error: fichero /tmp/time_espera.var NO CERRADO\n" );
      exit(1);
    }
    
    if (temp_valor == -1)
    {
       printf( "Valor no inicalizado /tmp/time_espera.var\n" );
       delay(20000);
      return 0;
    }
    else if (0<temp_valor>99)
    {
       printf ("Valor no se entiende no se sabe que es >1 o <0\n");
       return 0;
    }
    else
        tiempo_espera= temp_valor ;  // OK
   return 1;
}

int main(int argc, char *argv[]) {
    
        // This pin is not the first pin on the RPi GPIO header!
    // Consult https://projects.drogon.net/raspberry-pi/wiringpi/pins/
    // for more information.
    
    int code= 0;
    int errores=0;
    int result1=-1;
    int result2=-1;
	time_t lasttime=0;
	
    printf ("inicializamos\n");
    if (wiringPiSetup () == -1) return 1;
	printf("sending code[%i]\n", code);
	RCSwitch mySwitch = RCSwitch();
	mySwitch.enableTransmit(PIN_433);
    
     pinMode (PIN_RELE, OUTPUT) ;
     digitalWrite (PIN_RELE, 0);
    printf ("empezamos\n");
	fflush(stdout);
	
    while (errores<20000)
    {
        if (time(NULL) - lasttime > 2)
		{
			lasttime = time(NULL);
			// leer valor del relé
			result1 = read_rele();
			fflush(stdout);

			// leer valor del tiempo.
			result2 = read_espera();
			fflush(stdout);
			if ((result1!=1)||(result2!=1))
			{
				errores++;
				delay(2000);
			}
			else
			{
				errores=0;
			}
				// Enviamos los valores.
			digitalWrite (PIN_RELE, rele);

		}
		
		// Enviamos los valores.
		code = (rele*100)+tiempo_espera;
		mySwitch.send(code, 24);
		fflush(stdout);
     delay(400);
    }
    
	return 0;

}
