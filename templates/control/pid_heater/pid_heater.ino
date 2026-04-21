struct Pid {
  float kp;
  float ki;
  float kd;
  float integral;
  float previousError;
};

Pid pid{3.0f, 0.2f, 0.05f, 0.0f, 0.0f};
constexpr float kSetpoint = 55.0f;
constexpr uint32_t kSampleMs = 200;
uint32_t lastSample = 0;

float readTemperature() {
  return 35.0f + 4.0f * sin(millis() / 4000.0f);
}

float updatePid(Pid &controller, float setpoint, float measurement, float dt) {
  const float error = setpoint - measurement;
  controller.integral += error * dt;
  const float derivative = (error - controller.previousError) / dt;
  controller.previousError = error;
  float output = controller.kp * error + controller.ki * controller.integral + controller.kd * derivative;
  if (output < 0.0f) output = 0.0f;
  if (output > 255.0f) output = 255.0f;
  return output;
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  const uint32_t now = millis();
  if (now - lastSample < kSampleMs) {
    return;
  }
  const float dt = (now - lastSample) / 1000.0f;
  lastSample = now;

  const float temp = readTemperature();
  const float output = updatePid(pid, kSetpoint, temp, dt);

  Serial.print("temp:");
  Serial.print(temp);
  Serial.print(",setpoint:");
  Serial.print(kSetpoint);
  Serial.print(",output:");
  Serial.println(output);
}
