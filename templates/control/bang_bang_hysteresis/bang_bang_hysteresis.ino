constexpr float kLow = 24.0f;
constexpr float kHigh = 26.0f;
bool relayOn = false;

float readValue() {
  return 25.0f + sin(millis() / 4000.0f);
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  const float value = readValue();
  if (!relayOn && value < kLow) relayOn = true;
  if (relayOn && value > kHigh) relayOn = false;

  Serial.print("value:");
  Serial.print(value);
  Serial.print(",relay:");
  Serial.println(relayOn ? 1 : 0);
  delay(100);
}
