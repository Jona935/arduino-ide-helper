# Claude Code Setup

Usa este repo como helper de Arduino desde Claude Code.

## Regla principal

Para instalar librerias, instalar placas o revisar sketches, ejecuta la herramienta compartida:

```bash
python tools/arduino_helper.py <comando> ...
```

## Tareas comunes

Instalar libreria:

```bash
python tools/arduino_helper.py install-library ArduinoJson
```

Instalar plataforma:

```bash
python tools/arduino_helper.py install-platform esp32:esp32
```

Revisar proyecto:

```bash
python tools/arduino_helper.py check-project /ruta/al/proyecto --fqbn arduino:avr:uno
```

## Pautas

- Si no conoces el `FQBN`, pide o infiere el modelo de placa antes de prometer compilacion.
- Si falla la deteccion de `arduino-cli`, prueba con `ARDUINO_CLI_PATH`.
- Reporta includes detectados y el resultado de compilacion.
