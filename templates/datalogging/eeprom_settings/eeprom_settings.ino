#include <EEPROM.h>

struct Settings {
  float setpoint;
  uint8_t mode;
};

Settings settings{42.0f, 1};

void setup() {
  Serial.begin(115200);
  EEPROM.begin(sizeof(Settings));
  EEPROM.get(0, settings);
  if (isnan(settings.setpoint)) {
    settings = {42.0f, 1};
    EEPROM.put(0, settings);
    EEPROM.commit();
  }
}

void loop() {
}
