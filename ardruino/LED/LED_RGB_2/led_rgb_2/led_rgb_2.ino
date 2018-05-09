
#include "Lib_RGB.h"
#define num_led_total 3



/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  This example code is in the public domain.
*/

// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
#define num_led_total 3

#define _30MIN 180000//0
#define _60MIN 3600000

#define RED   0
#define GREEN 1
#define BLUE  2

int pin_led[num_led_total * 3];
int luz_led[num_led_total * 3] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
unsigned int Num_led_Manual = 2;
unsigned int Num_led_pwm = 1;
int Colores[num_led_total] = {0, 0, 100};


// the setup routine runs once when you press reset:
void setup() {
  setup_Manual();
  setup_PWM();
  Serial.begin(9600);
  Serial.println("Waiting for  R50 B50 G50");
  Set_Valor_LED_final();
  /// Texto
  Serial.println( "Luz RGB Cambiando:");
  Serial.println( "0 -> 30 min de Azul a Verde.");
  Serial.println( "30 -> 60 min de Verde a Rojo.");
  Serial.println( "60 -> 90 min de Rojo a RojoAzul.");
  Serial.println( "90 -> 120 min de RojoAzul a RojoVerde");
  Serial.println( "120 -> 180 min de RojoVerde a Blanco");
}

void setup_Manual()
{

  pin_led[0] = 14; // r
  pin_led[1] = 15; // g
  pin_led[2] = 16; // b
  pin_led[3] = 19; // r
  pin_led[4] = 17; // g
  pin_led[5] = 18; // b
  pinMode(pin_led[0], OUTPUT);
  pinMode(pin_led[1], OUTPUT);
  pinMode(pin_led[2], OUTPUT);
  pinMode(pin_led[3], OUTPUT);
  pinMode(pin_led[4], OUTPUT);
  pinMode(pin_led[5], OUTPUT);
  digitalWrite(pin_led[0], HIGH);
  digitalWrite(pin_led[1], HIGH);
  digitalWrite(pin_led[2], HIGH);
  digitalWrite(pin_led[3], HIGH);
  digitalWrite(pin_led[4], HIGH);
  digitalWrite(pin_led[5], HIGH);

}
void setup_PWM()
{
  pin_led[0 + 6] = 3; // r
  pin_led[1 + 6] = 5; // g
  pin_led[2 + 6] = 6; // b
  // initialize the digital pin as an output.
  pinMode(pin_led[0 + 6], OUTPUT);
  pinMode(pin_led[1 + 6], OUTPUT);
  pinMode(pin_led[2 + 6], OUTPUT);
  digitalWrite(pin_led[0 + 6], HIGH);
  digitalWrite(pin_led[1 + 6], HIGH);
  digitalWrite(pin_led[2 + 6], HIGH);
}
// the loop routine runs over and over again forever:
void loop() {
  Control();
  Control_Led_Manual();
  Control_Led_PWM();
  delay(1);
}

void Actualiza_Luminosidad(int num_color, int valor)
{
  /// Init Check.
  if (valor < 0) {
    Serial.print( "Error: Actualiza_Luminosidad, Color:");
    Serial.print( num_color, DEC);
    Serial.print(" Valor: ");
    Serial.println( valor, DEC);
    return;
  }
  Colores[num_color] = valor;
  Actualiza_Luminosidad_Manual(num_color, valor);
  Actualiza_Luminosidad_PWM(num_color, valor);
}
void Actualiza_Luminosidad_Manual(int num_color, int valor)
{
  int i = 0;
  // 99 -> 100
  valor = valor + 1;
  luz_led[num_color] = valor / 10 ;
  /*Serial.print("  Luz mANUAL[");
    Serial.print( num_color, DEC);
    Serial.print("] = ");
    Serial.println( luz_led[num_color + i * 3], DEC);*/
  luz_led[num_color + 3] = valor / 10 ;
  /*Serial.print("  Luz mANUAL[");
    Serial.print( num_color + 3, DEC);
    Serial.print("] = ");
    Serial.println( luz_led[num_color + i * 3], DEC);*/
}

void Actualiza_Luminosidad_PWM(int num_color, int valor)
{
  int i = 0;
  for (i = Num_led_Manual; i < num_led_total; i++)
  {
    luz_led[num_color + i * 3] = 255 - (valor * 255 / 100) ;
    /*Serial.print("  Luz PWM [");
      Serial.print( num_color, DEC);
      Serial.print("] = ");
      Serial.println( luz_led[num_color + i * 3], DEC);*/
  }

}
void Control_Led_Manual(void)
{
  static unsigned long time[6] = {0, 0, 0, 0, 0, 0};
  static char status_led[6] = {1, 1, 1, 1, 1, 1};
  static unsigned int num_led = 0;

  if ( (luz_led[num_led] == 0 && status_led[num_led] != 0) || (luz_led[num_led] == 10 && status_led[num_led] == 0) ) //
  {
    //
  }
  else
  {
    if ( millis() >= time[num_led])
    {
      if (status_led[num_led] == 0) // ENCENDIDO
      {
        digitalWrite(pin_led[num_led], HIGH );  // tcambiamos estado del led
        time[num_led] = millis() + 10 - luz_led[num_led];
        status_led[num_led] = 1;
        /*Serial.print("  Luz [");
          Serial.print( num_led, DEC);
          Serial.print("] = High en ");
          Serial.println( millis(), DEC);
          Serial.print("] = High pin ");
          Serial.println( pin_led[num_led], DEC);*/
      }
      else if (status_led[num_led] == 1) // APAGADO
      {
        digitalWrite(pin_led[num_led], LOW );  // tcambiamos estado del led
        time[num_led] = millis() + luz_led[num_led];
        status_led[num_led] = 0;
        /*Serial.print("  Luz [");
          Serial.print( num_led, DEC);
          Serial.print("] = Apagado en ");
          Serial.println( millis(), DEC);
          Serial.print("] = LOW pin ");
          Serial.println( pin_led[num_led], DEC);*/
      }
      else
      {
        Serial.print("  Error status_led[");
        Serial.print( num_led, DEC);
        Serial.print("] =  ");
        Serial.println( status_led[num_led], DEC);
      }
      /*Serial.print("  SI salta");
        Serial.print( status_led[num_led], DEC);
        Serial.print(", actual  ");
        Serial.println( millis(), DEC);*/
    }
    else
    {
      /* Serial.print("  NO salta");
        Serial.print( status_led[num_led], DEC);
        Serial.print(", actual  ");
        Serial.println( millis(), DEC);*/
    }
  }
  num_led++;
  if (num_led > 5)
    num_led = 0;
}

void Control_Led_PWM(void )
{
  static unsigned char num_led = Num_led_Manual * 3;
  static char count = 0;

  if (count == 0)
  {
    count = 21;
    analogWrite(pin_led[num_led], luz_led[num_led]);

    num_led++ ;
    if (num_led >= 9)
      num_led = 6;
  }
  count--;
}

void Control(void)
{
  static unsigned long lastTime;
  static int estado = 0;
  int value;

  if ((millis() - lastTime) < 18000) /// 1 Cambio cada 18000 milisec.
    return;
    
  lastTime = millis();
  Serial.print( "Cambio Led.");
  Serial.println( lastTime, DEC);

  if (estado == 0)
  {
    value = Colores[GREEN] + 1;
    Actualiza_Luminosidad(GREEN, value);
    value = Colores[BLUE] - 1;
    Actualiza_Luminosidad(BLUE, value);
    if (value == 0) {
      estado ++;
      Serial.print( "Cambio Estado!!!.");
      Serial.println( estado, DEC);
    }
  }
  else if (estado == 1) // 30 -> 60 min
  {
    value = Colores[RED] + 1;
    Actualiza_Luminosidad(RED, value);
    value = Colores[GREEN] - 1;
    Actualiza_Luminosidad(GREEN, value);
    if (value == 0) {
      estado ++;
      Serial.print( "Cambio Estado!!!.");
      Serial.println( estado, DEC);
    }
  }
  else if (estado == 2) // 60 ->  90 Min
  {
    /// SIEMPRE ROJO!!!!
    value = Colores[BLUE] + 1;
    Actualiza_Luminosidad(BLUE, value);
    if (value == 100) {
      estado ++;
      Serial.print( "Cambio Estado!!!.");
      Serial.println( estado, DEC);
    }
  }
  else if (estado == 3)// 90 ->  120 Min
  {
    value = Colores[BLUE] - 1;
    Actualiza_Luminosidad(BLUE, value);
    value = Colores[GREEN] + 1;
    Actualiza_Luminosidad(GREEN, value);
    if (value == 100) {
      estado ++;
      Serial.print( "Cambio Estado!!!.");
      Serial.println( estado, DEC);
    }
  }
  else if (estado == 4)// 120 ->  180 Min
  {
    value = Colores[BLUE] + 1;
    Actualiza_Luminosidad(BLUE, value);
    if (value == 100) {
      estado ++;
      Serial.print( "Cambio Estado!!!.");
      Serial.println( estado, DEC);
    }
  }
}

// ###################################################




