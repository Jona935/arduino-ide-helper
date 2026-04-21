#include <SPI.h>
#include <SD.h>

constexpr int kChipSelect = 10;
uint32_t lastWrite = 0;

void setup() {
  Serial.begin(115200);
  if (!SD.begin(kChipSelect)) {
    Serial.println("SD init failed");
    while (true) {
    }
  }
}

void loop() {
  const uint32_t now = millis();
  if (now - lastWrite < 1000) {
    return;
  }
  lastWrite = now;

  File file = SD.open("log.csv", FILE_WRITE);
  if (!file) {
    Serial.println("open failed");
    return;
  }

  file.print(now);
  file.print(',');
  file.println(analogRead(A0));
  file.close();
}
