#include <HX711.h>

constexpr int kDout = 3;
constexpr int kSck = 2;
HX711 scale;

void setup() {
  Serial.begin(115200);
  scale.begin(kDout, kSck);
  scale.set_scale();
  scale.tare();
}

void loop() {
  if (scale.is_ready()) {
    Serial.print("weight_raw:");
    Serial.println(scale.get_units(5));
  }
  delay(200);
}
