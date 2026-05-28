import csv
import os
import time
from datetime import datetime
import serial

PUERTO = "COM4"
BAUDIOS = 115200
ARCHIVO_CSV = "datos_potenciometro.csv"

def inicializar_csv(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["timestamp_pc", "lectura_cruda", "voltaje", "porcentaje"])

def main():
    conexion = None
    inicializar_csv(ARCHIVO_CSV)
    print("Intentando abrir el puerto serial...")
    try:
        conexion = serial.Serial(PUERTO, BAUDIOS, timeout=1)
        time.sleep(2)
        print(f"Conexion establecida con {PUERTO} a {BAUDIOS} baudios.")
        print("Presiona Ctrl + C para detener la captura.\n")
        while True:
            linea = conexion.readline().decode("utf-8", errors="ignore").strip()
            if not linea:
                continue
            if "ESP32 listo" in linea:
                print(f"[INFO] {linea}")
                continue
            print(f"[RECIBIDO] {linea}")
            partes = linea.split(",")
            if len(partes) != 3:
                print("[ADVERTENCIA] Linea con formato inesperado. Se omite.")
                continue
            try:
                lectura_cruda = int(partes[0])
                voltaje = float(partes[1])
                porcentaje = float(partes[2])
            except ValueError as error:
                print(f"[ADVERTENCIA] No se pudo convertir la linea: {error}")
                continue
            timestamp_pc = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                with open(ARCHIVO_CSV, mode="a", newline="", encoding="utf-8") as archivo:
                    escritor = csv.writer(archivo)
                    escritor.writerow([timestamp_pc, lectura_cruda, voltaje, porcentaje])
            except PermissionError as error:
                print(f"[ERROR] No se pudo escribir el CSV: {error}")
                time.sleep(1)
    except serial.SerialException as error:
        print(f"[ERROR] Problema con el puerto serial: {error}")
    except KeyboardInterrupt:
        print("\nCaptura finalizada por el usuario.")
    finally:
        if conexion is not None and conexion.is_open:
            conexion.close()
            print("Puerto serial cerrado correctamente.")

if __name__ == "__main__":
    main()