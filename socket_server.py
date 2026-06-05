# socket_server.py - Servidor TCP local independiente de Flask

import socket
import threading
import json
import config

class SocketServer:
    """
    Servidor TCP en 127.0.0.1:9000.
    Responde con un resumen JSON del estado del sistema a cada cliente conectado.
    """

    def __init__(self, data_store, analyzer):
        self.data_store = data_store
        self.analyzer   = analyzer
        self._hilo      = None
        self._activo    = False

    def iniciar(self):
        self._activo = True
        self._hilo = threading.Thread(target=self._loop, name="SocketServer", daemon=True)
        self._hilo.start()
        print(f"[SocketServer] Escuchando en {config.SOCKET_HOST}:{config.SOCKET_PORT}")

    def detener(self):
        self._activo = False

    def _loop(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((config.SOCKET_HOST, config.SOCKET_PORT))
            srv.listen(5)
            srv.settimeout(1.0)
            while self._activo:
                try:
                    conn, addr = srv.accept()
                    threading.Thread(target=self._atender_cliente,
                                     args=(conn, addr), daemon=True).start()
                except socket.timeout:
                    continue

    def _atender_cliente(self, conn, addr):
        try:
            datos   = self.data_store.obtener_copia()
            stats   = self.analyzer.analizar(datos)
            resumen = {
                "ultimo_adc":     stats["ultimo_adc"],
                "ultimo_voltaje": stats["ultimo_voltaje"],
                "promedio":       stats["promedio"],
                "minimo":         stats["minimo"],
                "maximo":         stats["maximo"],
                "desv_std":       stats["desv_std"],
                "muestras":       stats["n"],
                "estado":         stats["estado"],
            }
            mensaje = json.dumps(resumen, ensure_ascii=False) + "\n"
            conn.sendall(mensaje.encode("utf-8"))
        finally:
            conn.close()
