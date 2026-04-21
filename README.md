# Arduino IDE Helper Repo

Repositorio portable para asistir agentes de codigo con proyectos Arduino usando `arduino-cli`.

Funciona en tres capas:

- Codex: plugin local en `plugins/arduino-ide-helper/`
- Claude Code: instrucciones en `CLAUDE.md`
- OpenCode: instrucciones en `OPENCODE.md`

La pieza compartida entre todos es la CLI de Python:

- `tools/arduino_helper.py`

## Capacidades

- Instalar librerias Arduino
- Instalar plataformas y placas
- Revisar proyectos `.ino`
- Compilar sketches cuando se conoce el `FQBN`

## Estructura

- `plugins/arduino-ide-helper/`: plugin de Codex
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

- Python 3.10 o superior
- `arduino-cli` en `PATH`, o `ARDUINO_CLI_PATH`
- Alternativamente, Arduino IDE 2.x instalado

## Publicarlo como repo

1. Inicializa git en esta carpeta.
2. Haz tu primer commit.
3. Sube el contenido a GitHub, GitLab o tu forge preferido.

## Nota

El plugin de Codex sigue existiendo y usa la misma idea funcional, pero este repo ya no depende solo de Codex.
