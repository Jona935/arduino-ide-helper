# Arduino IDE Helper Instructions

Este repositorio esta pensado para agentes de codigo que necesiten ayudar con Arduino.

## Cuando usarlo

Usalo cuando el usuario pida alguna de estas tareas:

- instalar una libreria Arduino
- instalar una plataforma o core de placas
- revisar un sketch o proyecto `.ino`
- compilar un proyecto Arduino con `FQBN`

## Herramienta principal

Prefiere siempre la CLI compartida:

```bash
python tools/arduino_helper.py <comando> ...
```

## Instalacion recomendada

Si este repo aun no esta integrado al entorno del agente:

```bash
npx github:Jona935/arduino-ide-helper install codex
```

```bash
npx github:Jona935/arduino-ide-helper install claude --project .
```

```bash
npx github:Jona935/arduino-ide-helper install opencode --project .
```

## Comandos

- `install-library <nombre> [--version <version>]`
- `install-platform <platform>`
- `list-libraries [--all]`
- `list-platforms [--all]`
- `list-boards [--watch]`
- `detect-board [nombre-de-placa]`
- `check-project <ruta> [--fqbn <fqbn>]`
- `fix-deps <ruta> [--install] [--fqbn <fqbn>]`
- `compile <ruta> --fqbn <fqbn>`
- `upload <ruta> --fqbn <fqbn> --port <puerto>`
- `monitor --port <puerto> [--config baudrate=115200]`

## Comportamiento esperado

- Detecta `arduino-cli` automaticamente.
- Si no esta en `PATH`, intenta usar el empaquetado con Arduino IDE 2.x.
- Antes de instalar librerias o plataformas, actualiza indices.
- Si no hay `FQBN`, haz una revision estructural del proyecto y dilo claramente.
- Si el usuario nombra una placa en lenguaje natural, intenta mapearla a `FQBN`.
- Si el proyecto tiene includes externos, corre `fix-deps` antes de compilar.

## Ejemplos de FQBN

- Arduino Uno -> `arduino:avr:uno`
- Arduino Mega 2560 -> `arduino:avr:mega`
- ESP32 Dev Module -> `esp32:esp32:esp32`
- Raspberry Pi Pico -> `rp2040:rp2040:rpipico`
