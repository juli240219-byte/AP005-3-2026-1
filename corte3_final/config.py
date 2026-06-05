# config.py - Parámetros generales del sistema de monitoreo

# ── Puerto serial ─────────────────────────────────────────────────────────────
SERIAL_PORT = "COM4"   # Linux. En Windows usar "COM3", "COM4", etc.
SERIAL_BAUDRATE = 115200
SERIAL_TIMEOUT = 2             # Segundos de espera por lectura

# ── Archivo CSV ───────────────────────────────────────────────────────────────
CSV_PATH = "data/lecturas.csv"
CSV_HEADERS = ["tiempo_ms", "adc", "voltaje"]

# ── Análisis / umbrales (potenciómetro 0–3.3 V) ───────────────────────────────
UMBRAL_BAJO  = 1.1   # Voltaje por debajo de este valor → BAJO
UMBRAL_ALTO  = 2.2   # Voltaje por encima de este valor → ALTO
VENTANA_MOVIL = 20   # Número de muestras para el promedio móvil

# ── Servidor socket TCP ───────────────────────────────────────────────────────
SOCKET_HOST = "127.0.0.1"
SOCKET_PORT = 9000

# ── Flask ─────────────────────────────────────────────────────────────────────
FLASK_HOST = "127.0.0.1"
FLASK_PORT = 5000

# ── ThingSpeak ────────────────────────────────────────────────────────────────
# IMPORTANTE: no publiques tu Write API Key en repositorios públicos.
# Coloca la clave real en una variable de entorno o en un archivo .env no versionado.
import os
THINGSPEAK_WRITE_KEY = os.environ.get("THINGSPEAK_KEY", "TU_WRITE_API_KEY_AQUI")
THINGSPEAK_URL = "https://api.thingspeak.com/update"
THINGSPEAK_INTERVALO = 15      # Segundos entre envíos a ThingSpeak
