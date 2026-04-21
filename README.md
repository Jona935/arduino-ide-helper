# Arduino IDE Helper Repo

[![install](https://img.shields.io/badge/install-npx%20github:Jona935%2Farduino--ide--helper-0f766e)](https://github.com/Jona935/arduino-ide-helper)
[![embedded](https://img.shields.io/badge/focus-microcontrollers-1f2937)](https://github.com/Jona935/arduino-ide-helper)
[![firmware](https://img.shields.io/badge/firmware-professional-2563eb)](https://github.com/Jona935/arduino-ide-helper)

Repositorio portable para convertir agentes de codigo en asistentes serios para Arduino, ESP32, ESP8266 y RP2040.

## Lo que hace ahora

No solo instala y compila. Tambien puede ayudar a:

- elegir placa para un proyecto
- proponer setup completo
- generar firmware Arduino o ESP de buena calidad
- razonar sobre electronica, sensores, motores y control
- simular ecuaciones discretizadas
- preparar salida para Serial Plotter
- revisar y reparar proyectos existentes
- reutilizar plantillas profesionales por categoria
- consultar una base de conocimiento por componente

## Instalacion con npm

```bash
npx github:Jona935/arduino-ide-helper install codex
npx github:Jona935/arduino-ide-helper install claude --project .
npx github:Jona935/arduino-ide-helper install opencode --project .
```

O global:

```bash
npm install -g github:Jona935/arduino-ide-helper
arduino-ide-helper doctor
arduino-ide-helper install all --project .
```

## Despues de instalar, que puede hacer la IA

Ejemplos de pedidos que ya deberia cubrir:

- "quiero hacer un sistema de riego automatico y necesito el codigo de arduino"
- "quiero un medidor de bateria con INA219 y grafica en plotter"
- "quiero saber que placa usar para una estacion meteorologica con WiFi"
- "ayudame con setup para ESP32 y MQTT"
- "necesito simular esta ecuacion diferencial en Arduino"
- "quiero leer un BME280 y guardar CSV en SD"
- "quiero controlar un motor paso a paso con A4988"
- "quiero revisar este proyecto viejo y hacerlo compilar"

## Biblioteca de plantillas

Plantillas listas para adaptar:

- `templates/sensors/`
- `templates/motors/`
- `templates/control/`
- `templates/iot/`
- `templates/datalogging/`
- `templates/displays/`

Incluye ejemplos como:

- BME280 por I2C
- monitor de potencia con INA219
- stepper no bloqueante con A4988
- control PID para heater
- telemetria MQTT en ESP32
- logger CSV en SD
- dashboard SSD1306

## Base de conocimiento por componente

Documentacion inicial incluida en:

- `docs/components/BME280.md`
- `docs/components/INA219.md`
- `docs/components/MPU6050.md`
- `docs/components/DS18B20.md`
- `docs/components/HX711.md`
- `docs/components/A4988.md`
- `docs/components/TB6600.md`

## Capa de inteligencia

El comportamiento experto se apoya en:

- `docs/MICROCONTROLLER_EXPERTISE.md`
- `docs/PROJECT_ROUTER.md`

Eso hace que el agente sepa como reaccionar ante casi cualquier solicitud:

- idea abierta de proyecto
- seleccion de placa
- setup
- calculos
- sensores
- motores
- IoT
- datalogging
- displays
- depuracion

## Herramientas

- instalador npm con arte ASCII y animacion ligera
- CLI portable en `tools/arduino_helper.py`
- plugin para Codex en `plugins/arduino-ide-helper/`
- guias para Claude Code y OpenCode

## Calidad

- pruebas basicas con `python -m unittest discover -s tests -v`
- ejemplos para Uno, ESP32, RP2040, PID y Serial Plotter
- skill enfocada en firmware mantenible y criterios de electronica

## Requisitos

- Node.js 18 o superior
- Python 3.10 o superior
- `arduino-cli` o Arduino IDE 2.x
