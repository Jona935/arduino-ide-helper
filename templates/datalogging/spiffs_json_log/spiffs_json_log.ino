#include <SPIFFS.h>

void setup() {
  Serial.begin(115200);
  SPIFFS.begin(true);
  File file = SPIFFS.open("/log.txt", FILE_APPEND);
  file.println("{\"boot\":true}");
  file.close();
}

void loop() {
}
