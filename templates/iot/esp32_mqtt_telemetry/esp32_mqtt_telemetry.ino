#include <WiFi.h>
#include <PubSubClient.h>

const char *ssid = "your-ssid";
const char *password = "your-password";
const char *mqttHost = "broker.hivemq.com";

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);
uint32_t lastPublish = 0;

void ensureWifi() {
  if (WiFi.status() == WL_CONNECTED) return;
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
  }
}

void ensureMqtt() {
  mqtt.setServer(mqttHost, 1883);
  while (!mqtt.connected()) {
    mqtt.connect("esp32-telemetry-demo");
  }
}

void setup() {
  Serial.begin(115200);
  ensureWifi();
  ensureMqtt();
}

void loop() {
  ensureWifi();
  ensureMqtt();
  mqtt.loop();

  const uint32_t now = millis();
  if (now - lastPublish < 2000) {
    return;
  }
  lastPublish = now;

  mqtt.publish("demo/telemetry/temp", "24.6");
  Serial.println("published telemetry");
}
