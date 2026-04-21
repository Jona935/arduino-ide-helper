# Arduino IDE Helper Repo

[![npm-style installer](https://img.shields.io/badge/install-npx%20github:Jona935%2Farduino--ide--helper-0f766e)](https://github.com/Jona935/arduino-ide-helper)
[![arduino-cli](https://img.shields.io/badge/arduino--cli-supported-2563eb)](https://arduino.github.io/arduino-cli/)
[![agents](https://img.shields.io/badge/agents-Codex%20%7C%20Claude%20Code%20%7C%20OpenCode-111827)](https://github.com/Jona935/arduino-ide-helper)

Repositorio portable para asistir agentes de codigo con proyectos Arduino usando `arduino-cli`.

## Que resuelve

- instala librerias Arduino
- instala plataformas y cores
- detecta placas y ayuda a mapear nombres comunes a `FQBN`
- revisa sketches `.ino`
- sugiere dependencias leyendo `#include`
- compila, sube y monitorea placas
- se integra con Codex, Claude Code y OpenCode

## Instalacion con npm

Sin instalar globalmente:

```bash
npx github:Jona935/arduino-ide-helper install codex
npx github:Jona935/arduino-ide-helper install claude --project .
npx github:Jona935/arduino-ide-helper install opencode --project .
```

Instalacion global:

```bash
npm install -g github:Jona935/arduino-ide-helper
arduino-ide-helper doctor
arduino-ide-helper install all --project .
```

## Quick Start

Verifica el entorno:

```bash
arduino-ide-helper doctor
```

Detecta una placa o resuelve su `FQBN`:

```bash
python tools/arduino_helper.py detect-board "Arduino Uno"
python tools/arduino_helper.py detect-board "ESP32 Dev Module"
```

Revisa un proyecto y detecta includes:

```bash
python tools/arduino_helper.py check-project ./examples/esp32-web-status
```

Sugiere o instala dependencias:

```bash
python tools/arduino_helper.py fix-deps ./examples/esp32-web-status
python tools/arduino_helper.py fix-deps ./examples/esp32-web-status --install
```

Compila:

```bash
python tools/arduino_helper.py compile ./examples/uno-blink --fqbn arduino:avr:uno
python tools/arduino_helper.py compile ./examples/rpi-pico-sensor --fqbn rp2040:rp2040:rpipico
```

Sube a una placa:

```bash
python tools/arduino_helper.py upload ./examples/uno-blink --fqbn arduino:avr:uno --port COM3 --verify
```

Abre monitor serial:

```bash
python tools/arduino_helper.py monitor --port COM3 --config baudrate=115200
```

## Comandos disponibles

- `install-library <nombre> [--version <version>]`
- `install-platform <platform>`
- `list-libraries [--all]`
- `list-platforms [--all]`
- `list-boards [--watch]`
- `detect-board [nombre-de-placa]`
- `check-project <ruta> [--fqbn <fqbn>]`
- `fix-deps <ruta> [--install] [--fqbn <fqbn>]`
- `compile <ruta> --fqbn <fqbn> [--output-dir <ruta>]`
- `upload <ruta> --fqbn <fqbn> --port <puerto> [--verify]`
- `monitor --port <puerto> [--fqbn <fqbn>] [--config baudrate=115200]`
- `doctor`

## Alias de placas incluidos

- Arduino Uno -> `arduino:avr:uno`
- Arduino Nano -> `arduino:avr:nano`
- Arduino Mega 2560 -> `arduino:avr:mega`
- Arduino Leonardo -> `arduino:avr:leonardo`
- ESP32 Dev Module -> `esp32:esp32:esp32`
- NodeMCU -> `esp8266:esp8266:nodemcuv2`
- Raspberry Pi Pico -> `rp2040:rp2040:rpipico`

## Ejemplos reales

- `examples/uno-blink/uno-blink.ino`
- `examples/esp32-web-status/esp32-web-status.ino`
- `examples/rpi-pico-sensor/rpi-pico-sensor.ino`

## Integraciones

- Codex: plugin local en `plugins/arduino-ide-helper/`
- Claude Code: instrucciones en `CLAUDE.md`
- OpenCode: instrucciones en `OPENCODE.md`
- Todos: comparten `tools/arduino_helper.py`

## Calidad

- pruebas basicas con `python -m unittest discover -s tests -v`
- instalador npm con `bin/arduino-ide-helper.cjs`
- ejemplos incluidos para Uno, ESP32 y Raspberry Pi Pico

## Requisitos

- Node.js 18 o superior para el instalador npm
- Python 3.10 o superior para la CLI portable
- `arduino-cli` en `PATH`, `ARDUINO_CLI_PATH`, o Arduino IDE 2.x instalado

## Publicacion

El repo ya esta listo para iterar. Los siguientes pasos recomendados para hacerlo mas visible son:

- agregar topics de GitHub
- publicar un release `v0.3.0`
- añadir screenshots o GIFs
- validar la CLI en macOS y Linux
