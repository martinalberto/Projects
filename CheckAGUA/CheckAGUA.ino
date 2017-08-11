
#include <FS.h>                   //this needs to be first, or it all crashes and burns...
#include <ESP8266WiFi.h>          //ESP8266 Core WiFi Library (you most likely already have this in your sketch)
#include <ESP8266HTTPClient.h>

#include <DNSServer.h>            //Local DNS Server used for redirecting all requests to the configuration portal
#include <ESP8266WebServer.h>     //Local WebServer used to serve the configuration portal
#include "WiFiManager.h"          //https://github.com/tzapu/WiFiManager WiFi Configuration Magic


WiFiManager wifiManager;
char host [] ="http://martinalberto.es/*************"; /// pagina donde avisa de la Alerta Lluvia.

#define LED_BLUE  2
#define LED_RED  LED_BUILTIN

//##################################################################- 
void setup() {
  // put your setup code here, to run once:
  wifiManager.setTimeout(120);
  wifiManager.setAPCallback(configModeCallback);
  
  Serial.begin(115200);
  
  pinMode(LED_BLUE, OUTPUT);     // Initialize the LED_BUILTIN pin as an output
  digitalWrite(LED_BLUE, LOW);  // Turn the LED off by making the voltage HIGH
  
  delay(100);
  Serial.println("\n Starting Check AGUA V1.01.");
  
}
//##################################################################- 

//##################################################################- 
void loop() {
  uint16_t value = 0;
  uint32_t rtcData;
  if (ESP.rtcUserMemoryRead(0, (uint32_t*) &rtcData, sizeof(rtcData))) {     
      if (rtcData == -32000){
      // Encendido. -> Enviar.
         Serial.println("\n ENVIAR!");
         Enviar();
      }
  }  

  rtcData = -32000;
  if (!ESP.rtcUserMemoryWrite(0, (uint32_t*) &rtcData, sizeof(rtcData))) {
      /// Error -> Enviar.
      Serial.println("\nError Save: ENVIAR!");
      Enviar();
  }
  
  /// A dormir.
   Serial.println("Going into deep sleep for 120 seg");
   delay(50);
  //delay(10000); // 10 seg Despierto.
   ESP.deepSleep( 120 * 1000000);
}

void Enviar (void)
{
    HTTPClient http;
    int httpCode =0;
    if(!wifiManager.autoConnect()) {
        Serial.println("failed to connect and hit timeout");
        delay(2000);
        Serial.println("Going into deep sleep for 1 Hour"); 
        delay(100);
        //delay(10000); // 60 min Despierto.
        ESP.deepSleep( 1800 * 1000000 * 2 );
    }
    Serial.println("connected...yeey :)");


  /// CONECTAMOS-> 
   if (!http.begin(host)) //HTTP
  {
    Serial.println("connection failed");
    return;
  }
    // start connection and send HTTP header
    httpCode = http.GET();

    // httpCode will be negative on error
    if(httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] GET... code: %d \n", httpCode);

        // file found at server
        if(httpCode == HTTP_CODE_OK) {
            String payload = http.getString();
            Serial.println(payload);
            Serial.println();
        }
    } else {
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
   Serial.println("closing connection");
   http.end();
   /// A dormir.
   Serial.println("Going into deep sleep for 1 Hour");
   delay(100);
  //delay(10000); // 30 min Despierto.
   ESP.deepSleep( 1800 * 1000000 * 2);
}

void configModeCallback (WiFiManager *myWiFiManager) {
  pinMode(LED_RED, OUTPUT);     // Initialize the LED_BUILTIN pin as an output
  digitalWrite(LED_RED, LOW);  // Turn the LED on by making the voltage LOW
  digitalWrite(LED_BLUE, HIGH);  // Turn the LED off by making the voltage HIGH
  
  Serial.println("Entered config mode");
  Serial.println(WiFi.softAPIP());
  Serial.println(myWiFiManager->getConfigPortalSSID());
}

