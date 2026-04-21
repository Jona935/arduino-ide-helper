constexpr int kStepPin = 2;
constexpr int kDirPin = 3;
uint32_t lastStepUs = 0;

void setup() {
  pinMode(kStepPin, OUTPUT);
  pinMode(kDirPin, OUTPUT);
  digitalWrite(kDirPin, HIGH);
}

void loop() {
  if (micros() - lastStepUs < 1000) return;
  lastStepUs = micros();
  digitalWrite(kStepPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(kStepPin, LOW);
}
