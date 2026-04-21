constexpr int kStepPin = 2;
constexpr int kDirPin = 3;
constexpr uint32_t kPulseUs = 400;
constexpr uint32_t kIntervalUs = 1200;

uint32_t lastStepUs = 0;
bool stepState = false;

void setup() {
  pinMode(kStepPin, OUTPUT);
  pinMode(kDirPin, OUTPUT);
  digitalWrite(kDirPin, HIGH);
}

void loop() {
  const uint32_t nowUs = micros();
  if (nowUs - lastStepUs < kIntervalUs) {
    return;
  }
  lastStepUs = nowUs;

  stepState = !stepState;
  digitalWrite(kStepPin, stepState ? HIGH : LOW);
}
