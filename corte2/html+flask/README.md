# Proyecto IoT ESP32 - Monitoreo de Potenciometro

## Requisitos
- Python 3
- Arduino IDE
- ESP32 + potenciometro

## Instalacion
1. Clonar el repositorio:
   git clone https://github.com/juli240219-byte/AP005-3-2026-1.git

2. Instalar librerias:
   pip install pyserial pandas matplotlib flask

## Conexion del potenciometro
- Extremo 1        a 3.3V
- Terminal central a D34
- Extremo 2        a GND

## Cargar el ESP32
- Abrir Arduino IDE
- Cargar el archivo esp32_potenciometro.ino
- Seleccionar el puerto COM correcto

## Ejecucion
1. Abrir terminal 1 y ejecutar:
   python serial_a_csv.py

2. Abrir terminal 2 y ejecutar:
   python app.py

3. Abrir el navegador en:
   http://127.0.0.1:5000

## Nota importante
- Cambiar el puerto COM en serial_a_csv.py segun el PC usado
- Cerrar el Monitor Serie de Arduino antes de ejecutar serial_a_csv.py