# Project Router

Esta guia define como debe decidir el agente que hacer cuando el usuario le pide cualquier proyecto relacionado con Arduino, ESP32, ESP8266 o RP2040.

## Regla general

No responder solo con comandos. Primero clasifica el pedido, luego decide placa, arquitectura, dependencias, calculos y firmware.

## Escenarios principales

### 1. "Quiero hacer X proyecto"

El agente debe:

1. inferir el tipo de proyecto:
   - sensor/medicion
   - control
   - IoT
   - robotica/motores
   - datalogging
   - interfaz/pantalla
   - simulacion/calculo
2. proponer la placa mas adecuada
3. listar sensores, actuadores y modulos necesarios
4. advertir compatibilidad electrica
5. proponer arquitectura de firmware
6. generar codigo inicial de alta calidad

### 2. "Quiero saber que placa usar"

El agente debe comparar al menos:

- Arduino Uno/Nano si importa simplicidad
- ESP32 si importa WiFi/Bluetooth/potencia
- ESP8266 si importa WiFi barato
- RP2040 si importa PIO, costo o ADC/dual core basico

Evaluar segun:

- cantidad de pines
- conectividad
- RAM/Flash
- precision ADC
- voltaje logico
- consumo
- costo

### 3. "Ayudame con setup"

El agente debe:

- detectar FQBN
- instalar core y librerias
- revisar puertos
- preparar compilacion
- sugerir pinout inicial

### 4. "Necesito simular esta ecuacion en Arduino"

El agente debe:

- convertir la ecuacion a forma discreta si hace falta
- razonar sobre precision numerica
- recomendar `float` o aproximacion fija si aplica
- estimar frecuencia de muestreo
- generar sketch con trazas para Serial Plotter

### 5. "Quiero codigo para sensor/driver especifico"

El agente debe:

- consultar la base de componentes en `docs/components/`
- seleccionar plantilla base en `templates/`
- adaptar pines, libreria, calibracion y telemetria

### 6. "Quiero depurar un proyecto existente"

El agente debe:

- correr `check-project`
- correr `fix-deps`
- revisar includes, warnings, arquitectura y bloqueos
- si hay FQBN, compilar
- si hay telemetria, proponer formato de depuracion o plot

## Salida esperada por tipo de solicitud

- Idea/proyecto: recomendacion de hardware + firmware base
- Seleccion de placa: comparativa concreta
- Setup: comandos y pasos exactos
- Sensor/driver: wiring + librerias + sketch
- Control/calculo: formulas + discretizacion + sketch
- Depuracion: hallazgos + cambios sugeridos + compilacion
