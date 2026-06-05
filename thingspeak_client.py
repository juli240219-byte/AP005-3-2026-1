# thingspeak_client.py - Envío periódico de datos a ThingSpeak

import requests
import threading
import time
import config

# Mapa de estado → valor numérico para ThingSpeak field4
ESTADO_NUM = {"BAJO": 0, "NORMAL": 1, "ALTO": 2, "SIN DATOS": -1}

class ThingSpeakClient:
    """Envía datos al canal de ThingSpeak cada THINGSPEAK_INTERVALO segundos."""

    def __init__(self, data_store, analyzer):
        self.data_store    = data_store
        self.analyzer      = analyzer
        self._hilo         = None
        self._activo       = False
        self.ultimo_envio  = "Nunca"
        self.ultimo_estado = "—"

    def iniciar(self):
        self._activo = True
        self._hilo = threading.Thread(target=self._loop, name="ThingSpeak", daemon=True)
        self._hilo.start()
        print(f"[ThingSpeak] Hilo iniciado (intervalo: {config.THINGSPEAK_INTERVALO} s)")

    def detener(self):
        self._activo = False

    def _loop(self):
        while self._activo:
            self._enviar()
            time.sleep(config.THINGSPEAK_INTERVALO)

    def _enviar(self):
        datos = self.data_store.obtener_copia()
        stats = self.analyzer.analizar(datos)
        if stats["n"] == 0:
            return

        payload = {
            "api_key": config.THINGSPEAK_WRITE_KEY,
            "field1":  stats["ultimo_adc"],
            "field2":  stats["ultimo_voltaje"],
            "field3":  round(stats["promedio_movil"][-1], 3) if stats["promedio_movil"] else 0,
            "field4":  ESTADO_NUM.get(stats["estado"], -1),
        }
        try:
            r = requests.post(config.THINGSPEAK_URL, data=payload, timeout=10)
            if r.status_code == 200 and r.text != "0":
                self.ultimo_estado = f"OK (entrada {r.text.strip()})"
            else:
                self.ultimo_estado = f"Error HTTP {r.status_code}"
            self.ultimo_envio = time.strftime("%H:%M:%S")
        except requests.RequestException as e:
            self.ultimo_estado = f"Fallo: {e}"
        print(f"[ThingSpeak] {self.ultimo_envio} → {self.ultimo_estado}")
