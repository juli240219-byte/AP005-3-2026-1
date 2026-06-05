import os
from datetime import datetime
from flask import Flask, render_template
import pandas as pd
from pandas.errors import EmptyDataError
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ARCHIVO_CSV = "datos_potenciometro.csv"
CARPETA_STATIC = "static"
RUTA_GRAFICA = os.path.join(CARPETA_STATIC, "grafica_potenciometro.png")

app = Flask(__name__)

def cargar_datos():
    if not os.path.exists(ARCHIVO_CSV):
        return pd.DataFrame()
    try:
        df = pd.read_csv(ARCHIVO_CSV, parse_dates=["timestamp_pc"])
        if df.empty:
            return pd.DataFrame()
        df["lectura_cruda"] = pd.to_numeric(df["lectura_cruda"], errors="coerce")
        df["voltaje"] = pd.to_numeric(df["voltaje"], errors="coerce")
        df["porcentaje"] = pd.to_numeric(df["porcentaje"], errors="coerce")
        df = df.dropna().reset_index(drop=True)
        return df
    except EmptyDataError:
        return pd.DataFrame()
    except KeyError as error:
        print(f"[ERROR] Falta una columna en el CSV: {error}")
        return pd.DataFrame()
    except Exception as error:
        print(f"[ERROR] No se pudo cargar el CSV: {error}")
        return pd.DataFrame()

def generar_grafica(df):
    os.makedirs(CARPETA_STATIC, exist_ok=True)
    try:
        if df.empty:
            plt.figure(figsize=(10, 4))
            plt.text(0.5, 0.5, "Aun no hay datos para graficar",
                     ha="center", va="center", fontsize=14)
            plt.axis("off")
            plt.tight_layout()
            plt.savefig(RUTA_GRAFICA)
            plt.close()
            return
        df_grafica = df.tail(100).copy()
        plt.figure(figsize=(12, 5))
        plt.plot(df_grafica["timestamp_pc"], df_grafica["lectura_cruda"], marker="o")
        plt.title("Lecturas recientes del potenciometro")
        plt.xlabel("Tiempo")
        plt.ylabel("Lectura ADC (0 a 4095)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(RUTA_GRAFICA)
        plt.close()
    except Exception as error:
        print(f"[ERROR] No se pudo generar la grafica: {error}")

def construir_resumen(df):
    if df.empty:
        return {
            "total_muestras": 0,
            "ultima_lectura": "Sin datos",
            "ultimo_voltaje": "Sin datos",
            "ultimo_porcentaje": "Sin datos",
            "promedio": "Sin datos",
            "minimo": "Sin datos",
            "maximo": "Sin datos",
        }
    ultima = df.iloc[-1]
    return {
        "total_muestras": int(len(df)),
        "ultima_lectura": int(ultima["lectura_cruda"]),
        "ultimo_voltaje": round(float(ultima["voltaje"]), 3),
        "ultimo_porcentaje": round(float(ultima["porcentaje"]), 1),
        "promedio": round(float(df["lectura_cruda"].mean()), 2),
        "minimo": int(df["lectura_cruda"].min()),
        "maximo": int(df["lectura_cruda"].max()),
    }

@app.route("/")
def inicio():
    try:
        df = cargar_datos()
        generar_grafica(df)
        resumen = construir_resumen(df)
        if df.empty:
            tabla_html = "<p>No hay datos todavia.</p>"
        else:
            tabla_html = (
                df.tail(10)
                .copy()
                .to_html(classes="tabla-datos", index=False, border=0)
            )
        actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return render_template(
            "index.html",
            resumen=resumen,
            tabla_html=tabla_html,
            actualizacion=actualizacion
        )
    except Exception as error:
        return f"""
        <html><head><title>Error</title></head>
        <body><h1>Error interno</h1><p>{error}</p></body>
        </html>""", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)