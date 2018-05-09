#include <EEPROM.h>
#include "Lib_RGB.h"
#define num_led_total 3
int luz_led[num_led_total * 3] = {0, 0, 0, 0, 0, 0, 0, 0, 0};


/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  This example code is in the public domain.
*/

// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
#define num_led_total 3
#define RANDOM_VALUE 50
int pin_led[num_led_total * 3];
//int luz_led[num_led_total*3];
int Num_led_Manual = 2;
int Num_led_pwm = 1;

//save values
char Save_values = 0;
int Color_led[3] = {0, 0, 0};

// the setup routine runs once when you press reset:
void setup() {
  setup_Manual();
  setup_PWM();
  Serial.begin(9600);
  Serial.println("Waiting for  R50 B50 G50");
  ReadMemory();
  Set_Valor_LED_final();
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

  //digitalWrite(pin_led[1], HIGH);   // turn the LED on (HIGH is the voltage level)
  //delay(20);               // wait for a second
  // digitalWrite(pin_led_r, LOW);    // turn the LED off by making the voltage LOW
  //  delay(200-cont);               // wait for a second
  Control();
  Control_Led_Manual();
  Control_Led_PWM();
}

void Actualiza_Luminosidad(int num_color, int valor)
{
  Color_led[num_color] = valor;
  Save_values = 1;
  Actualiza_Luminosidad_Manual(num_color, valor);
  Actualiza_Luminosidad_PWM(num_color, valor);
}
void Actualiza_Luminosidad_Manual(int num_color, int valor)
{
  int i = 0;
  // 99 -> 100
  valor = valor + 1;
  /// -> LED 0.
  luz_led[num_color] = valor / 10 ;
  Serial.print("  Luz mANUAL[");
  Serial.print( num_color, DEC);
  Serial.print("] = ");
  Serial.println( luz_led[num_color + i * 3], DEC);
  /// -> LED 2.
  luz_led[num_color + 3] = valor / 10 ;
  Serial.print("  Luz mANUAL[");
  Serial.print( num_color + 3, DEC);
  Serial.print("] = ");
  Serial.println( luz_led[num_color + i * 3], DEC);
}
void Actualiza_Luminosidad_PWM(int num_color, int valor)
{
  int i = 0;

  for (i = Num_led_Manual; i < num_led_total; i++)
  {
    /// -> LED 1.
    luz_led[num_color + i * 3] = 255 - (valor * 255 / 100) ;
       Serial.print("  Luz PWM [");
      Serial.print( num_color, DEC);
      Serial.print("] = ");
      Serial.println( luz_led[num_color+i*3], DEC);
  }

}
void Control_Led_Manual(void )
{
  static long int time[6] = {0, 0, 0, 0, 0, 0};
  static char status_led[6] = {1, 1, 1, 1, 1, 1};
  static int num_led = 0;

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
  static char num_led = Num_led_Manual * 3;
  static int luz_led_old[num_led_total * 3] = { -1, -1, -1};
  //static char Max_cont=(3*(Num_led_Manual+Num_led_pwm));
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
  static char status_Control = 3;
  static char Max_status_Control = 5;
  char rc;
  switch (status_Control) {
    case 0:
      //Control Serial.
      ControlSerial();
      status_Control = 200; // default
      return;
    case 1:
      //None
      status_Control--;
      return;
    case 2:
      WriteMemory();
      status_Control--;
      return;
    case 3:
      //None
      status_Control--;
      return;
    case 4:
      rc = SucesoLibCambiaLed();
      if (rc == 1)
        Max_status_Control = 3;
      status_Control--;
      return;
    case 5:
      //None
      status_Control--;
      return;
    default:
      status_Control = Max_status_Control;
      return;
  }

}
void ControlSerial (void)
{
  char c = 0;
  static int led_select = 0;
  static int valor = 0;
  // check if data has been sent from the computer:
  if (Serial.available()) {
    // read the most recent byte (which will be from 0 to 255):
    c = Serial.read();
    if (c == 'a') {
      Set_Valor_LED_final();
    }
    else if (c == 'f')
    {
      ReadMemory();
    }
    else if (c == 'r')
    {
      led_select = 0;
      Actualiza_Luminosidad(0, 0);
      valor = 0;
      Serial.print("  led_select=0:");
    }
    else if (c == 'g')
    {
      led_select = 1;
      Actualiza_Luminosidad(led_select, 0);
      valor = 0;
      Serial.print("  led_select=1:");
    }
    else if (c == 'b')
    {
      led_select = 2;
      Actualiza_Luminosidad(led_select, 0);
      valor = 0;
      Serial.print("  led_select=2:");
    }
    else if ( c >= '0' && c <= '9') {
      valor = (10 * valor) + ((int)c - (int)'0') ; // convert digits to a number
      Actualiza_Luminosidad(led_select, valor);
    }
    else
    {
      Serial.print(" Error letra incorrecta: ");
      Serial.print(c);
    }

  }
}

void ReadMemory(void)
{
  byte i = 0, value = 0;

  for (i = 0; i < 3; i++)
  {
    Serial.print("  ReadMemory OK");
    value = EEPROM.read(i + RANDOM_VALUE);
    Actualiza_Luminosidad(i, value);
  }
  Save_values = 0;
}

void WriteMemory(void)
{
  byte j = 0;
  static unsigned int i = 25000;

  if (Save_values == 0)
    return;
  else
  {
    if (i != 0)
    {
      i--;
      return ;
    }
    else
    {
      Serial.print("  WriteMemory OK");
      for (j = 0; j < 3; j++)
      {
        EEPROM.write(j + RANDOM_VALUE, Color_led[j]);
      }
      i = 25000;
      Save_values = 0;
    }
  }
}
