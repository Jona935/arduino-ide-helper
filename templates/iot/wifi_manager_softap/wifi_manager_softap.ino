#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_AP);
  WiFi.softAP("ArduinoSetup", "12345678");
  Serial.println(WiFi.softAPIP());
}

void loop() {
}
