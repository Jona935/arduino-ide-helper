---
name: arduino-ide-helper
description: Usa arduino-cli para instalar librerias, instalar plataformas de placas y revisar proyectos Arduino desde Codex.
---

# Arduino IDE Helper

Usa esta skill cuando el usuario pida trabajar con Arduino IDE, instalar librerias, instalar placas, compilar sketches o revisar proyectos `.ino`.

## Objetivo

- Instalar librerias con `arduino-cli lib install`
- Instalar plataformas de placas con `arduino-cli core install`
- Revisar proyectos Arduino y, cuando haya `FQBN`, compilarlos

## Flujo

1. Verifica si existe `arduino-cli` usando el script `scripts\\arduino-cli-common.ps1`.
2. Para instalar librerias usa:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-library.ps1 -LibraryName "ArduinoJson"
```

3. Para instalar placas usa:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-board-platform.ps1 -Platform "esp32:esp32"
```

4. Para revisar un proyecto usa:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check-project.ps1 -ProjectPath "C:\ruta\proyecto" -Fqbn "arduino:avr:uno"
```

## Notas

- Si `arduino-cli` no esta en `PATH`, intenta usar el binario incluido en Arduino IDE 2.x para Windows.
- Si no hay `FQBN`, revisa estructura, archivos `.ino` e includes, pero no prometas compilacion completa.
- Antes de instalar placas o librerias, actualiza indices.
- Si el usuario menciona una placa por nombre comun, ayuda a convertirla a FQBN. Ejemplos:
  - Arduino Uno -> `arduino:avr:uno`
  - ESP32 Dev Module -> `esp32:esp32:esp32`
  - Raspberry Pi Pico -> `rp2040:rp2040:rpipico`
