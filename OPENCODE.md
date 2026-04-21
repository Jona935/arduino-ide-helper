# OpenCode Setup

Este repo puede usarse desde OpenCode siguiendo una convencion simple: delega todo el trabajo de Arduino a la CLI compartida.

Para criterio tecnico y cobertura de escenarios, consulta tambien:

- `docs/MICROCONTROLLER_EXPERTISE.md`
- `docs/PROJECT_ROUTER.md`
- `docs/components/`
- `templates/`

## Instalacion

```bash
npx github:Jona935/arduino-ide-helper install opencode --project .
```

## Entrada recomendada

```bash
python tools/arduino_helper.py <comando> ...
```

## Comandos utiles

```bash
python tools/arduino_helper.py install-library ArduinoJson
python tools/arduino_helper.py install-platform esp32:esp32
python tools/arduino_helper.py detect-board "ESP32 Dev Module"
python tools/arduino_helper.py check-project ./mi-sketch --fqbn arduino:avr:uno
python tools/arduino_helper.py fix-deps ./mi-sketch --install --fqbn arduino:avr:uno
```

## Reglas

- Usa `check-project` para una revision rapida de estructura e includes.
- Usa `fix-deps` si detectas librerias externas.
- Usa `--fqbn` cuando quieras compilacion real.
- Si falta `arduino-cli`, usa `ARDUINO_CLI_PATH` o instala Arduino IDE 2.x.
- Si el usuario pide proyecto nuevo, selecciona placa y plantilla antes de generar codigo.
