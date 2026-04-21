constexpr int kTrigPin = 9;
constexpr int kEchoPin = 10;
uint32_t lastSample = 0;

float readDistanceCm() {
  digitalWrite(kTrigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(kTrigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(kTrigPin, LOW);
  const unsigned long duration = pulseIn(kEchoPin, HIGH, 30000);
  return duration * 0.0343f / 2.0f;
}

void setup() {
  Serial.begin(115200);
  pinMode(kTrigPin, OUTPUT);
  pinMode(kEchoPin, INPUT);
}

void loop() {
  if (millis() - lastSample < 250) return;
  lastSample = millis();
  Serial.print("distance_cm:");
  Serial.println(readDistanceCm());
}
