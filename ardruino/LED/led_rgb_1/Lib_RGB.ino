#include <Arduino.h>
#include "Arduino.h"
#include "Lib_RGB.h"
#include <EEPROM.h>



int luz_led_Fin[num_led_total*3]={50,50,50,50,50,50,50,50,50};

int Set_Valor_LED_final( void  )
{	

	char i=0;
					Serial.print(". led[");
			Serial.print( 0, DEC);
			Serial.print("] = ");
			Serial.print( luz_led[0], DEC);
			Serial.print(". led[");
			Serial.print( 1, DEC);
			Serial.print("] = ");
			Serial.print( luz_led[1], DEC);
			Serial.print(". led[");
			Serial.print( 2, DEC);
			Serial.print("] = ");
			Serial.print( luz_led[2], DEC);
			Serial.print(". led[");
			Serial.print( 3, DEC);
			Serial.print("] = ");
			Serial.print( luz_led[3], DEC);
			Serial.print(". led[");
			Serial.print( 5, DEC);
			Serial.print("] = ");
			Serial.print( luz_led[5], DEC);
			Serial.print(". led[");
			Serial.print(6, DEC);
			Serial.print("] = ");
			Serial.print( luz_led[6], DEC);
			Serial.print(". led[");
			Serial.print( 7, DEC);
			Serial.print("] = ");
			Serial.print( luz_led[7], DEC);
			Serial.print(". led[");
			Serial.print(8, DEC);
			Serial.print("] = ");
			Serial.println( luz_led[8], DEC);		
			
	for (i=0;i<9;i++)
		luz_led_Fin[i]=luz_led[i];

	Inicia_Led();

      Serial.println(" ___________________ Set_Valor_LED_final");

}

void Inicia_Led(void)
{
		//led Manual
		luz_led[0]=0;//led 1
		luz_led[1]=0;//led 1
		luz_led[2]=0;//led 1
		luz_led[3]=0;//led 2
		luz_led[4]=0;//led 3
		luz_led[5]=0;//led 4
		// led PWM
		luz_led[6] =255 ;
		luz_led[7] =255 ;
		luz_led[8] =255 ;	
	return ;
}

int SucesoLibCambiaLed(void)
{
    static char i=0;
    char rc;

	switch (i){
	case 0:
                // translate to setup()
		//Set_Valor_LED_final();
		i++;
		break;
	case 1:
		i++;
		break;
	case 2:
		i=SucesoLibCambiaLed2();
		break;
	case 3:
		rc=Aumenta_LED();
		if (rc==1)
		{
			i=4;
		}	
		break;
	case 4:
		i=CompruebaFin();
		break;
	case 5:// Fin
		return 1;
		break;
	default:
		return 1;
		break;
    }
	return 0;
}

char SucesoLibCambiaLed2(void)
{
	static long int time=0;
	char rc=1;// volver a estado anterior 
		if (millis()>time)
		{
			rc=3; // sube valor.
			time= millis()+500;
		}
		return rc;
}
int Aumenta_LED(void)
{
   static char Led=0, TipoLed=0;
   char rc=3;
   
	switch(TipoLed)
	{
		case 0:// led Normal
			
			luz_led[Led]+=1;
			if (luz_led[Led]>luz_led_Fin[Led])
				luz_led[Led]=luz_led_Fin[Led];
                                Led++;		
			if (Led>=6)
                {
					TipoLed++;
				}
			break;
		case 1:// led PWM
			luz_led[Led]-=(25);
			if (luz_led[Led]<=luz_led_Fin[Led])
				luz_led[Led]=luz_led_Fin[Led];
			Led++;
		
			if (Led>=9)
                        {
				   
				TipoLed=0;
				Led=0;
				return 1;
                        }
			break;
		default:
		        break;
	}

	return 0;
}
char CompruebaFin(void)
{
	char i;
	for (i=0; i<6; i++)
	{
		if (luz_led[i]<luz_led_Fin[i])
                {
			return 1;
                }
	}
	for (i=6; i<9; i++)
	{
		if (luz_led[i]>luz_led_Fin[i])
			return 1;
	}
	return 5;
}
