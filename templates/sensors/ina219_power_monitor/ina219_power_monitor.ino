#include <Wire.h>
#include <Adafruit_INA219.h>

Adafruit_INA219 ina219;
constexpr uint32_t kSampleMs = 500;
uint32_t lastSample = 0;

void setup() {
  Serial.begin(115200);
  if (!ina219.begin()) {
    Serial.println("INA219 not found");
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

  const float busV = ina219.getBusVoltage_V();
  const float currentMa = ina219.getCurrent_mA();
  const float powerMw = ina219.getPower_mW();

  Serial.print("busV:");
  Serial.print(busV);
  Serial.print(",currentmA:");
  Serial.print(currentMa);
  Serial.print(",powermW:");
  Serial.println(powerMw);
}
