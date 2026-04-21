#include <OneWire.h>
#include <DallasTemperature.h>

constexpr int kOneWireBus = 2;
OneWire oneWire(kOneWireBus);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  sensors.begin();
}

void loop() {
  sensors.requestTemperatures();
  Serial.println(sensors.getTempCByIndex(0));
  delay(2000);
}
