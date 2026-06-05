# web_app.py - Servidor web con Flask

from flask import Flask, render_template, jsonify
import threading
import config

app = Flask(__name__)

# Referencias inyectadas desde main.py
_data_store       = None
_analyzer         = None
_plotter          = None
_thingspeak_client = None

def configurar(data_store, analyzer, plotter, thingspeak_client):
    global _data_store, _analyzer, _plotter, _thingspeak_client
    _data_store        = data_store
    _analyzer          = analyzer
    _plotter           = plotter
    _thingspeak_client = thingspeak_client

@app.route("/")
def index():
    datos  = _data_store.obtener_copia()
    stats  = _analyzer.analizar(datos)
    _plotter.generar_todas(stats)
    ts_info = {
        "ultimo_envio":  _thingspeak_client.ultimo_envio,
        "ultimo_estado": _thingspeak_client.ultimo_estado,
    }
    return render_template("index.html", stats=stats, ts=ts_info)

@app.route("/api/estado")
def api_estado():
    """Endpoint JSON para consultas programáticas."""
    datos = _data_store.obtener_copia()
    stats = _analyzer.analizar(datos)
    return jsonify({k: v for k, v in stats.items()
                    if k not in ("voltajes", "adc_vals", "tiempos_ms", "promedio_movil")})

def iniciar(debug=False):
    hilo = threading.Thread(
        target=lambda: app.run(host=config.FLASK_HOST, port=config.FLASK_PORT,
                               debug=debug, use_reloader=False),
        name="Flask", daemon=True
    )
    hilo.start()
    print(f"[Flask] Servidor en http://{config.FLASK_HOST}:{config.FLASK_PORT}")
