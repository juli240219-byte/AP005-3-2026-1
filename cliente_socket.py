# =====================================================
# cliente_socket.py - Cliente de prueba del servidor TCP
# Uso: python cliente_socket.py
# =====================================================

import socket
import config

def consultar_servidor():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((config.SOCKET_HOST, config.SOCKET_PORT))
            datos = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                datos += chunk
        print("Respuesta del servidor:")
        print(datos.decode("utf-8"))
    except ConnectionRefusedError:
        print(f"No se pudo conectar a {config.SOCKET_HOST}:{config.SOCKET_PORT}")
        print("Asegúrate de que main.py está corriendo.")

if __name__ == "__main__":
    consultar_servidor()
