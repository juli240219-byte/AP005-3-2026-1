# Sistema de Monitoreo Analógico — ESP32 + Python 3

**Programación Aplicada 2025-3**

## Descripción
Sistema completo de adquisición y visualización de datos analógicos. Un ESP32 lee un potenciómetro mediante ADC y envía las mediciones por UART. Python las recibe, almacena en CSV, analiza con pandas/numpy, genera gráficas y las muestra en una página web local con Flask. Además, un servidor socket TCP independiente entrega resúmenes del sistema y un hilo envía datos periódicamente a ThingSpeak.

## Flujo del dato
```
Potenciómetro → ESP32 (ADC GPIO34) → UART → Python → CSV
   → pandas/numpy → matplotlib → Flask/HTML → ThingSpeak
```

## Hardware
| Elemento | Detalle |
|---|---|
| Microcontrolador | ESP32 (cualquier variante con ADC1) |
| Sensor | Potenciómetro 10 kΩ |
| Pin ADC | GPIO34 — ADC1_CH6 (solo entrada) |
| Baudrate | 115200 bps |

### Conexión del potenciómetro
```
3.3V  ──── Pin 1 (extremo) del potenciómetro
GND   ──── Pin 3 (extremo) del potenciómetro
GPIO34 ─── Pin 2 (cursor/wiper) del potenciómetro
```

## Formato UART
Cada línea enviada por el ESP32:
```
tiempo_ms,adc,voltaje
1250,1843,1.49
```

## Estructura del proyecto
```
proyecto_final_python_esp32/
├── esp32_potenciometro.ino  # Firmware ESP32
├── main.py                  # Punto de entrada; coordina todos los módulos
├── config.py                # Parámetros globales (puerto, umbrales, claves)
├── serial_reader.py         # Hilo: lectura UART continua
├── data_store.py            # Almacén en memoria + escritura CSV
├── analyzer.py              # Estadísticas con pandas y numpy
├── plotter.py               # Gráficas con matplotlib
├── socket_server.py         # Servidor TCP local (puerto 9000)
├── thingspeak_client.py     # Hilo: envío periódico a ThingSpeak
├── web_app.py               # Flask + rutas HTML y JSON
├── data/lecturas.csv        # Datos capturados
├── static/plots/            # Gráficas PNG generadas
├── templates/index.html     # Página web
└── requirements.txt
```

## Instalación (Ubuntu)
```bash
sudo apt update && sudo apt install python3-pip
pip3 install -r requirements.txt
# Agregar usuario al grupo dialout para acceso al puerto serial:
sudo usermod -aG dialout $USER
# Reiniciar sesión o ejecutar: newgrp dialout
```

## Configurar ThingSpeak
```bash
export THINGSPEAK_KEY="tu_write_api_key_real"
```
O edita `config.py` localmente (nunca subas la clave al repositorio).

## Ejecución
```bash
cd proyecto_final_python_esp32
python3 main.py
```

## Acceso
- Página web → http://127.0.0.1:5000
- API JSON   → http://127.0.0.1:5000/api/estado

## Probar el servidor socket
```bash
python3 -c "import socket, json; s=socket.create_connection(('127.0.0.1',9000)); print(json.loads(s.recv(4096))); s.close()"
# o con netcat:
nc 127.0.0.1 9000
```

## Hilos del sistema
| Hilo | Responsabilidad |
|---|---|
| SerialReader | Lectura continua del puerto UART |
| SocketServer | Atiende conexiones TCP en puerto 9000 |
| ThingSpeak | Envía datos cada 15 s |
| Flask | Sirve la página web |

## Umbrales del potenciómetro
| Estado | Condición |
|---|---|
| BAJO | Voltaje < 1.1 V |
| NORMAL | 1.1 V ≤ Voltaje ≤ 2.2 V |
| ALTO | Voltaje > 2.2 V |

## Seguridad
- La Write API Key de ThingSpeak **no** debe publicarse en el repositorio.
- Usa variables de entorno o un archivo `.env` excluido con `.gitignore`.
