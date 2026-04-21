#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

Adafruit_BME280 bme;
constexpr uint32_t kSampleMs = 1000;
uint32_t lastSample = 0;

void setup() {
  Serial.begin(115200);
  if (!bme.begin(0x76)) {
    Serial.println("BME280 not found");
    while (true) {
    }
  }
}

void loop() {
  const uint32_t now = millis();
  if (now - lastSample < kSampleMs) {
    return;
  }
  lastSample = now;

  const float tempC = bme.readTemperature();
  const float humidity = bme.readHumidity();
  const float pressureHpa = bme.readPressure() / 100.0f;

  Serial.print("temp:");
  Serial.print(tempC);
  Serial.print(",hum:");
  Serial.print(humidity);
  Serial.print(",pres:");
  Serial.println(pressureHpa);
}
