#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "your-ssid";
const char* password = "your-password";
ESP8266WebServer server(80);

void setup() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
  }

  server.on("/ping", []() {
    server.send(200, "application/json", "{\"ok\":true}");
  });
  server.begin();
}

void loop() {
  server.handleClient();
}
