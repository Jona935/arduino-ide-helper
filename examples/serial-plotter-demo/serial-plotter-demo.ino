constexpr uint32_t kSampleIntervalMs = 100;

float phase = 0.0f;
uint32_t lastSampleMs = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  const uint32_t now = millis();
  if (now - lastSampleMs < kSampleIntervalMs) {
    return;
  }

  lastSampleMs = now;
  phase += 0.15f;

  const float rawSignal = 512.0f + 200.0f * sin(phase);
  const float filteredSignal = 512.0f + 180.0f * sin(phase - 0.2f);
  const float setpoint = 600.0f;

  Serial.print("raw:");
  Serial.print(rawSignal);
  Serial.print(',');
  Serial.print("filtered:");
  Serial.print(filteredSignal);
  Serial.print(',');
  Serial.print("setpoint:");
  Serial.println(setpoint);
}
