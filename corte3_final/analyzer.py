# analyzer.py - Análisis de datos con pandas y numpy

import pandas as pd
import numpy as np
import config

class Analyzer:
    """Calcula estadísticas sobre las lecturas del potenciómetro."""

    def analizar(self, datos):
        """
        Recibe una lista de dicts {tiempo_ms, adc, voltaje}.
        Devuelve un dict con las estadísticas calculadas.
        """
        if not datos:
            return self._resultado_vacio()

        df = pd.DataFrame(datos)

        voltajes = df["voltaje"].to_numpy(dtype=float)

        n           = len(voltajes)
        ultimo_adc  = int(df["adc"].iloc[-1])
        ultimo_v    = float(df["voltaje"].iloc[-1])
        promedio    = float(np.mean(voltajes))
        minimo      = float(np.min(voltajes))
        maximo      = float(np.max(voltajes))
        desv_std    = float(np.std(voltajes))

        # Promedio móvil (ventana configurable)
        serie = pd.Series(voltajes)
        promedio_movil = serie.rolling(window=config.VENTANA_MOVIL, min_periods=1).mean().tolist()

        # Clasificación por umbral
        estado = self._clasificar(ultimo_v)

        return {
            "n":              n,
            "ultimo_adc":     ultimo_adc,
            "ultimo_voltaje": round(ultimo_v, 3),
            "promedio":       round(promedio, 3),
            "minimo":         round(minimo, 3),
            "maximo":         round(maximo, 3),
            "desv_std":       round(desv_std, 3),
            "promedio_movil": [round(v, 3) for v in promedio_movil],
            "tiempos_ms":     df["tiempo_ms"].tolist(),
            "voltajes":       voltajes.tolist(),
            "adc_vals":       df["adc"].tolist(),
            "estado":         estado,
        }

    def _clasificar(self, voltaje):
        if voltaje < config.UMBRAL_BAJO:
            return "BAJO"
        elif voltaje > config.UMBRAL_ALTO:
            return "ALTO"
        return "NORMAL"

    def _resultado_vacio(self):
        return {
            "n": 0, "ultimo_adc": 0, "ultimo_voltaje": 0.0,
            "promedio": 0.0, "minimo": 0.0, "maximo": 0.0,
            "desv_std": 0.0, "promedio_movil": [], "tiempos_ms": [],
            "voltajes": [], "adc_vals": [], "estado": "SIN DATOS",
        }
