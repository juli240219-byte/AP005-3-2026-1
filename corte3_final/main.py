# main.py - Punto de entrada del sistema de monitoreo analógico
# Programación Aplicada 2025-3

import time
import sys

from config            import FLASK_HOST, FLASK_PORT, SOCKET_HOST, SOCKET_PORT
from data_store        import DataStore
from serial_reader     import SerialReader
from analyzer          import Analyzer
from plotter           import Plotter
from socket_server     import SocketServer
from thingspeak_client import ThingSpeakClient
import web_app

def main():
    print("=" * 55)
    print("  Sistema de Monitoreo Analógico - ESP32 + Python 3")
    print("=" * 55)

    # 1. Instanciar módulos
    data_store  = DataStore()
    analyzer    = Analyzer()
    plotter     = Plotter()

    # 2. Configurar e iniciar Flask (hilo propio dentro de web_app)
    web_app.configurar(data_store, analyzer, plotter,
                       thingspeak_client=None)   # se actualiza abajo

    # 3. Iniciar ThingSpeak (hilo periódico)
    ts_client = ThingSpeakClient(data_store, analyzer)
    ts_client.iniciar()

    # 4. Ahora sí inyectar el cliente ThingSpeak en Flask
    web_app._thingspeak_client = ts_client

    # 5. Iniciar servidor socket TCP (hilo propio)
    socket_srv = SocketServer(data_store, analyzer)
    socket_srv.iniciar()

    # 6. Iniciar lectura serial (hilo propio)
    serial_rdr = SerialReader(data_store)
    serial_rdr.iniciar()

    # 7. Iniciar Flask
    web_app.iniciar(debug=False)

    print(f"\nSistema activo:")
    print(f"  Página web  →  http://{FLASK_HOST}:{FLASK_PORT}")
    print(f"  Socket TCP  →  {SOCKET_HOST}:{SOCKET_PORT}")
    print(f"  Para probar el socket:  python3 -c \"import socket,json; s=socket.create_connection(('{SOCKET_HOST}',{SOCKET_PORT})); print(s.recv(4096).decode()); s.close()\"")
    print("  Ctrl+C para salir.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[main] Cerrando sistema…")
        serial_rdr.detener()
        socket_srv.detener()
        ts_client.detener()
        sys.exit(0)

if __name__ == "__main__":
    main()
