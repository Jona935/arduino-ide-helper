# Arduino IDE Helper Repo

Repositorio portable para asistir agentes de codigo con proyectos Arduino usando `arduino-cli`.

Ahora incluye instalador por `npm`, para que se use mas como un paquete real:

- Codex: instala el plugin en tu home
- Claude Code: copia `CLAUDE.md` al proyecto que elijas
- OpenCode: copia `OPENCODE.md` al proyecto que elijas
- Todos: comparten la CLI de Python `tools/arduino_helper.py`

## Capacidades

- Instalar librerias Arduino
- Instalar plataformas y placas
- Revisar proyectos `.ino`
- Compilar sketches cuando se conoce el `FQBN`

## Instalacion con npm

Sin instalar globalmente:

```bash
npx github:Jona935/arduino-ide-helper install codex
```

```bash
npx github:Jona935/arduino-ide-helper install claude --project .
```

```bash
npx github:Jona935/arduino-ide-helper install opencode --project .
```

Instalacion global:

```bash
npm install -g github:Jona935/arduino-ide-helper
arduino-ide-helper doctor
arduino-ide-helper install codex
```

Instalar todo de una vez:

```bash
arduino-ide-helper install all --project .
```

Sobrescribir archivos existentes:

```bash
arduino-ide-helper install claude --project . --force
```

## Estructura

- `plugins/arduino-ide-helper/`: plugin de Codex
- `bin/arduino-ide-helper.cjs`: instalador npm
- `tools/arduino_helper.py`: herramienta compartida para cualquier agente
- `AGENTS.md`: instrucciones generales para agentes
- `CLAUDE.md`: adaptacion para Claude Code
- `OPENCODE.md`: adaptacion para OpenCode

## Uso rapido

```powershell
python .\tools\arduino_helper.py install-library ArduinoJson
```

```powershell
python .\tools\arduino_helper.py install-platform esp32:esp32
```

```powershell
python .\tools\arduino_helper.py check-project "C:\ruta\mi-sketch" --fqbn arduino:avr:uno
```

## Requisitos

- Node.js 18 o superior para el instalador npm
- Python 3.10 o superior
- `arduino-cli` en `PATH`, o `ARDUINO_CLI_PATH`
- Alternativamente, Arduino IDE 2.x instalado

## Nota

El plugin de Codex sigue existiendo y usa la misma idea funcional, pero este repo ya no depende solo de Codex.
