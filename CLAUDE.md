# Claude Code Setup

Usa este repo como helper de Arduino desde Claude Code.

## Instalacion

```bash
npx github:Jona935/arduino-ide-helper install claude --project .
```

## Regla principal

Para instalar librerias, instalar placas o revisar sketches, ejecuta la herramienta compartida:

```bash
python tools/arduino_helper.py <comando> ...
```

Ademas, para proyectos abiertos o complejos, consulta:

```text
docs/MICROCONTROLLER_EXPERTISE.md
docs/PROJECT_ROUTER.md
docs/components/
templates/
```

## Tareas comunes

Detectar placa o FQBN:

```bash
python tools/arduino_helper.py detect-board "Arduino Uno"
```

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

Revisar dependencias:

```bash
python tools/arduino_helper.py fix-deps /ruta/al/proyecto --install --fqbn arduino:avr:uno
```

## Pautas

- Si no conoces el `FQBN`, pide o infiere el modelo de placa antes de prometer compilacion.
- Si falla la deteccion de `arduino-cli`, prueba con `ARDUINO_CLI_PATH`.
- Reporta includes detectados y el resultado de compilacion.
- Si ves includes externos, corre `fix-deps` antes de compilar.
- Si el usuario pide ayuda amplia, elige placa, setup y plantilla base antes de escribir firmware.
