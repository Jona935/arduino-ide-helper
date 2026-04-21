#include <Servo.h>

Servo servo;
int angle = 0;
int direction = 1;
uint32_t lastMove = 0;

void setup() {
  servo.attach(9);
}

void loop() {
  if (millis() - lastMove < 20) return;
  lastMove = millis();
  angle += direction;
  if (angle >= 180 || angle <= 0) direction = -direction;
  servo.write(angle);
}
