# OpenCode Setup

Este repo puede usarse desde OpenCode siguiendo una convencion simple: delega todo el trabajo de Arduino a la CLI compartida.

## Entrada recomendada

```bash
python tools/arduino_helper.py <comando> ...
```

## Comandos utiles

```bash
python tools/arduino_helper.py install-library ArduinoJson
python tools/arduino_helper.py install-platform esp32:esp32
python tools/arduino_helper.py check-project ./mi-sketch --fqbn arduino:avr:uno
```

## Reglas

- Usa `check-project` para una revision rapida de estructura e includes.
- Usa `--fqbn` cuando quieras compilacion real.
- Si falta `arduino-cli`, usa `ARDUINO_CLI_PATH` o instala Arduino IDE 2.x.
