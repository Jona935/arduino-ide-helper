#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;
uint32_t lastSample = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.initialize();
}

void loop() {
  if (millis() - lastSample < 50) return;
  lastSample = millis();
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);
  Serial.print("ax:");
  Serial.print(ax);
  Serial.print(",ay:");
  Serial.print(ay);
  Serial.print(",az:");
  Serial.println(az);
}
