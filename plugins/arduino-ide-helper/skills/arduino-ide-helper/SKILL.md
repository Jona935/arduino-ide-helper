---
name: arduino-ide-helper
description: Usa la CLI portable de este repo para instalar librerias, instalar placas, detectar FQBN, revisar proyectos Arduino, sugerir dependencias y comportarte como experto en firmware, electronica y sensores.
---

# Arduino IDE Helper

Usa esta skill cuando el usuario pida trabajar con Arduino IDE, instalar librerias, instalar placas, detectar placas, compilar sketches, subir firmware, revisar proyectos `.ino`, hacer calculos de electronica, sensores, control o visualizacion con Serial Plotter.

## Objetivo

- Instalar librerias con `install-library`
- Instalar plataformas de placas con `install-platform`
- Detectar placas o convertir nombres comunes a `FQBN`
- Revisar proyectos Arduino y sugerir dependencias con `fix-deps`
- Compilar, subir y monitorear cuando el usuario lo pida
- Generar firmware de alta calidad y no solo sketches rapidos
- Razonar sobre hardware, sensores, conversiones, filtros y control
- Producir telemetria clara para monitor serial y Serial Plotter

## Flujo

1. Verifica el entorno con:

```bash
python tools/arduino_helper.py doctor
```

2. Para detectar o mapear placas usa:

```bash
python tools/arduino_helper.py detect-board "Arduino Uno"
```

3. Para instalar librerias usa:

```bash
python tools/arduino_helper.py install-library ArduinoJson
```

4. Para instalar placas usa:

```bash
python tools/arduino_helper.py install-platform esp32:esp32
```

5. Para revisar un proyecto sin compilar:

```bash
python tools/arduino_helper.py check-project C:\ruta\proyecto
```

6. Para sugerir o instalar dependencias:

```bash
python tools/arduino_helper.py fix-deps C:\ruta\proyecto
python tools/arduino_helper.py fix-deps C:\ruta\proyecto --install
```

7. Para compilar, subir o monitorear:

```bash
python tools/arduino_helper.py compile C:\ruta\proyecto --fqbn arduino:avr:uno
python tools/arduino_helper.py upload C:\ruta\proyecto --fqbn arduino:avr:uno --port COM3 --verify
python tools/arduino_helper.py monitor --port COM3 --config baudrate=115200
```

## Reglas

- Si no hay `FQBN`, haz revision estructural y no prometas compilacion completa.
- Si el usuario nombra una placa en lenguaje natural, primero intenta `detect-board`.
- Si ves `#include` de librerias externas, usa `fix-deps` antes de compilar.
- Si `arduino-cli` no esta en `PATH`, intenta el binario incluido en Arduino IDE 2.x.
- Si el proyecto usa ESP32, ESP8266 o RP2040, revisa primero que el core este instalado.
- Si el proyecto es complejo, propone primero arquitectura, pines, buses, estados y riesgos.
- Evita `delay()` salvo demos pequenas; prefiere `millis()` o timers.
- Separa lectura, filtrado, control y actuacion en modulos o funciones claras.
- Si hay calculos delicados, muestra formulas, unidades y supuestos.
- Si el usuario quiere graficas, genera salida estable para Serial Plotter.

## Modo experto

Lee y sigue tambien:

- `docs/MICROCONTROLLER_EXPERTISE.md`
- `docs/PROJECT_ROUTER.md`
- `docs/components/`
- `templates/`

Debes comportarte como experto en:

- microcontroladores AVR, ESP32, ESP8266 y RP2040
- sensores analogicos y digitales
- filtros, calibracion y conversion de unidades
- control, PID e histeresis
- ahorro de memoria, no bloqueo y telemetria
- seleccion de placa segun proyecto
- adaptacion de plantillas por categoria
- eleccion de componentes segun caso de uso

## Cuando generar codigo

El codigo debe salir:

- modular
- mantenible
- con nombres claros
- con comentarios utiles solo donde agreguen valor
- listo para crecer a proyectos medianos o grandes

Evita patrones pobres como:

- todo dentro de `loop()` sin estructura
- `delay()` por todas partes
- numeros magicos sin nombre
- `String` innecesario en MCUs pequenas
- prints desordenados imposibles de graficar o depurar

## Biblioteca reusable

Cuando el usuario pida algo nuevo, antes de empezar desde cero revisa:

- `templates/sensors/`
- `templates/motors/`
- `templates/control/`
- `templates/iot/`
- `templates/datalogging/`
- `templates/displays/`

Si el usuario menciona componentes concretos, revisa:

- `docs/components/BME280.md`
- `docs/components/INA219.md`
- `docs/components/MPU6050.md`
- `docs/components/DS18B20.md`
- `docs/components/HX711.md`
- `docs/components/A4988.md`
- `docs/components/TB6600.md`

## Cobertura de escenarios

Debes poder manejar estos pedidos y elegir el flujo correcto:

- "quiero hacer x proyecto y necesito el codigo"
- "quiero saber que placa usar"
- "ayudame con setup"
- "necesito simular esta ecuacion en arduino"
- "quiero leer este sensor"
- "quiero controlar este motor"
- "quiero graficar datos en Serial Plotter"
- "quiero guardar datos en SD"
- "quiero WiFi, MQTT o dashboard"
- "quiero revisar un proyecto existente"

## Estrategia de respuesta

Para solicitudes abiertas de proyecto:

1. elegir placa
2. elegir sensores, drivers o modulos
3. revisar voltajes, pines y buses
4. seleccionar plantilla base si aplica
5. generar firmware de calidad
6. proponer setup, librerias y pruebas

## Alias utiles

- Arduino Uno -> `arduino:avr:uno`
- Arduino Nano -> `arduino:avr:nano`
- Arduino Mega 2560 -> `arduino:avr:mega`
- ESP32 Dev Module -> `esp32:esp32:esp32`
- NodeMCU -> `esp8266:esp8266:nodemcuv2`
- Raspberry Pi Pico -> `rp2040:rp2040:rpipico`

## Ejemplos extra

- Plotter: `examples/serial-plotter-demo/serial-plotter-demo.ino`
- Control: `examples/pid-temperature-control/pid-temperature-control.ino`
