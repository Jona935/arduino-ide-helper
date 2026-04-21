# Arduino IDE Helper

Plugin local de Codex para trabajar con proyectos Arduino usando `arduino-cli`.

## Que hace

- Instala librerias Arduino
- Instala plataformas y paquetes de placas
- Revisa proyectos `.ino`
- Compila sketches cuando se proporciona un `FQBN`
- Comparte una CLI portable con Claude Code y OpenCode
- Sugiere dependencias a partir de los `#include`
- Ayuda a mapear nombres comunes de placas a `FQBN`

## Scripts incluidos

- `scripts/install-library.ps1`
- `scripts/install-board-platform.ps1`
- `scripts/check-project.ps1`

## CLI compartida

Este plugin forma parte de un repo portable. La herramienta comun para otros agentes esta en:

- `../../tools/arduino_helper.py`

## Ejemplos

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-library.ps1 -LibraryName "ArduinoJson"
```

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-board-platform.ps1 -Platform "esp32:esp32"
```

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check-project.ps1 -ProjectPath "C:\ruta\mi-sketch" -Fqbn "arduino:avr:uno"
```

```powershell
python ..\..\tools\arduino_helper.py fix-deps "C:\ruta\mi-sketch" --install --fqbn "arduino:avr:uno"
```

## Requisitos

- Python 3.10 o superior
- `arduino-cli` en `PATH`, o Arduino IDE 2.x instalado
- Opcionalmente, definir `ARDUINO_CLI_PATH` si el binario esta en otra ruta
