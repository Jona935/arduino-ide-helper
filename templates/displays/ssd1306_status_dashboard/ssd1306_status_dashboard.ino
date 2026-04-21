#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);
uint32_t lastFrame = 0;

void setup() {
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    while (true) {
    }
  }
}

void loop() {
  const uint32_t now = millis();
  if (now - lastFrame < 250) {
    return;
  }
  lastFrame = now;

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("System OK");
  display.print("Millis: ");
  display.println(now);
  display.display();
}
