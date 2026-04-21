constexpr float kAlpha = 0.15f;
float filtered = 0.0f;
uint32_t lastSample = 0;

float readSignal() {
  return 512.0f + 100.0f * sin(millis() / 700.0f);
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  if (millis() - lastSample < 50) return;
  lastSample = millis();
  const float raw = readSignal();
  filtered = filtered + kAlpha * (raw - filtered);
  Serial.print("raw:");
  Serial.print(raw);
  Serial.print(",filtered:");
  Serial.println(filtered);
}
