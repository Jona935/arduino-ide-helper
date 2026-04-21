struct PidState {
  float kp;
  float ki;
  float kd;
  float integral;
  float previousError;
};

constexpr float kSetpointC = 42.0f;
constexpr uint32_t kControlIntervalMs = 200;

PidState pid{2.0f, 0.4f, 0.1f, 0.0f, 0.0f};
uint32_t lastControlMs = 0;

float readTemperatureC() {
  const float simulated = 30.0f + 5.0f * sin(millis() / 3000.0f);
  return simulated;
}

float updatePid(PidState &state, float setpoint, float measurement, float dtSeconds) {
  const float error = setpoint - measurement;
  state.integral += error * dtSeconds;
  const float derivative = (error - state.previousError) / dtSeconds;
  state.previousError = error;

  float output = state.kp * error + state.ki * state.integral + state.kd * derivative;
  if (output < 0.0f) output = 0.0f;
  if (output > 255.0f) output = 255.0f;
  return output;
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  const uint32_t now = millis();
  if (now - lastControlMs < kControlIntervalMs) {
    return;
  }

  const float dtSeconds = (now - lastControlMs) / 1000.0f;
  lastControlMs = now;

  const float measuredTemp = readTemperatureC();
  const float controlOutput = updatePid(pid, kSetpointC, measuredTemp, dtSeconds);

  Serial.print("temp:");
  Serial.print(measuredTemp);
  Serial.print(',');
  Serial.print("setpoint:");
  Serial.print(kSetpointC);
  Serial.print(',');
  Serial.print("output:");
  Serial.println(controlOutput);
}
