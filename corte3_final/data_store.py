# data_store.py - Almacenamiento en memoria y escritura en CSV

import csv
import threading
import os
import config

class DataStore:
    """Almacena las lecturas en memoria y las persiste en un CSV."""

    def __init__(self):
        self._lock = threading.Lock()
        self._datos = []           # Lista de dicts {tiempo_ms, adc, voltaje}
        self._inicializar_csv()

    def _inicializar_csv(self):
        os.makedirs(os.path.dirname(config.CSV_PATH), exist_ok=True)
        if not os.path.exists(config.CSV_PATH):
            with open(config.CSV_PATH, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=config.CSV_HEADERS)
                writer.writeheader()

    def agregar(self, tiempo_ms, adc, voltaje):
        fila = {"tiempo_ms": tiempo_ms, "adc": adc, "voltaje": round(voltaje, 3)}
        with self._lock:
            self._datos.append(fila)
            self._escribir_fila(fila)

    def _escribir_fila(self, fila):
        with open(config.CSV_PATH, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=config.CSV_HEADERS)
            writer.writerow(fila)

    def obtener_copia(self):
        """Devuelve una copia segura de todos los datos actuales."""
        with self._lock:
            return list(self._datos)

    def ultima_lectura(self):
        with self._lock:
            return self._datos[-1] if self._datos else None

    def total_muestras(self):
        with self._lock:
            return len(self._datos)
