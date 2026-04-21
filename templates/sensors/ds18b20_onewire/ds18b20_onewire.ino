#include <OneWire.h>
#include <DallasTemperature.h>

constexpr int kBusPin = 2;
OneWire oneWire(kBusPin);
DallasTemperature sensors(&oneWire);
uint32_t lastSample = 0;

void setup() {
  Serial.begin(115200);
  sensors.begin();
}

void loop() {
  if (millis() - lastSample < 1000) return;
  lastSample = millis();
  sensors.requestTemperatures();
  Serial.print("temp:");
  Serial.println(sensors.getTempCByIndex(0));
}
