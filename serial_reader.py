# serial_reader.py - Lectura continua del puerto serial UART

import serial
import threading
import time
import config

class SerialReader:
    """Lee líneas del ESP32 por UART y las pone en una cola de datos."""

    def __init__(self, data_store):
        self.data_store = data_store
        self._hilo = None
        self._activo = False
        self._ser = None
        self.conectado = False

    def iniciar(self):
        """Inicia el hilo de lectura serial."""
        self._activo = True
        self._hilo = threading.Thread(target=self._leer_loop, name="SerialReader", daemon=True)
        self._hilo.start()
        print(f"[SerialReader] Hilo iniciado → {config.SERIAL_PORT} @ {config.SERIAL_BAUDRATE}")

    def detener(self):
        self._activo = False
        if self._ser and self._ser.is_open:
            self._ser.close()

    def _leer_loop(self):
        while self._activo:
            try:
                self._ser = serial.Serial(config.SERIAL_PORT, config.SERIAL_BAUDRATE,
                                          timeout=config.SERIAL_TIMEOUT)
                self.conectado = True
                print("[SerialReader] Puerto serial abierto.")
                while self._activo:
                    linea = self._ser.readline().decode("utf-8", errors="ignore").strip()
                    if linea:
                        self._procesar_linea(linea)
            except serial.SerialException as e:
                self.conectado = False
                print(f"[SerialReader] Error serial: {e}. Reintentando en 3 s…")
                time.sleep(3)
            finally:
                if self._ser and self._ser.is_open:
                    self._ser.close()

    def _procesar_linea(self, linea):
        """Valida y parsea la línea 'tiempo_ms,adc,voltaje'."""
        try:
            partes = linea.split(",")
            if len(partes) < 3:
                return
            tiempo_ms = int(partes[0])
            adc       = int(partes[1])
            voltaje   = float(partes[2])
            if not (0 <= adc <= 4095):
                return
            self.data_store.agregar(tiempo_ms, adc, voltaje)
        except (ValueError, IndexError):
            pass  # Línea malformada; se ignora
