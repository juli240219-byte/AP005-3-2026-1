# plotter.py - Generación de gráficas con matplotlib

import matplotlib
matplotlib.use("Agg")          # Backend sin GUI (necesario con Flask)
import matplotlib.pyplot as plt
import os

RUTA_PLOTS = "static/plots"

class Plotter:
    """Genera y guarda las tres gráficas obligatorias."""

    def __init__(self):
        os.makedirs(RUTA_PLOTS, exist_ok=True)
        # Estilo visual
        plt.rcParams.update({
            "figure.facecolor": "#0f1117",
            "axes.facecolor":   "#1a1d27",
            "axes.edgecolor":   "#3a3f5c",
            "axes.labelcolor":  "#c9d1d9",
            "xtick.color":      "#8b949e",
            "ytick.color":      "#8b949e",
            "text.color":       "#c9d1d9",
            "grid.color":       "#21262d",
            "grid.linestyle":   "--",
            "grid.alpha":       0.6,
        })

    def generar_todas(self, stats):
        if stats["n"] < 2:
            return
        self.grafica_tiempo(stats)
        self.histograma(stats)
        self.promedio_movil(stats)

    # ── 1. Señal en el tiempo ──────────────────────────────────────────────────
    def grafica_tiempo(self, stats):
        fig, ax = plt.subplots(figsize=(9, 4))
        tiempos = [t / 1000 for t in stats["tiempos_ms"]]   # ms → s
        ax.plot(tiempos, stats["voltajes"], color="#58a6ff", linewidth=1.2, label="Voltaje (V)")
        ax.axhline(1.1, color="#f85149", linestyle="--", linewidth=0.8, label="Umbral BAJO (1.1 V)")
        ax.axhline(2.2, color="#3fb950", linestyle="--", linewidth=0.8, label="Umbral ALTO (2.2 V)")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Voltaje (V)")
        ax.set_title("Señal del potenciómetro en el tiempo")
        ax.legend(fontsize=8)
        ax.grid(True)
        fig.tight_layout()
        fig.savefig(f"{RUTA_PLOTS}/sensor_tiempo.png", dpi=100)
        plt.close(fig)

    # ── 2. Histograma ─────────────────────────────────────────────────────────
    def histograma(self, stats):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(stats["voltajes"], bins=30, color="#58a6ff", edgecolor="#1a1d27", alpha=0.85)
        ax.axvline(stats["promedio"], color="#f0883e", linestyle="--", linewidth=1.2,
                   label=f"Promedio: {stats['promedio']} V")
        ax.set_xlabel("Voltaje (V)")
        ax.set_ylabel("Frecuencia")
        ax.set_title("Distribución de voltajes (histograma)")
        ax.legend(fontsize=8)
        ax.grid(True)
        fig.tight_layout()
        fig.savefig(f"{RUTA_PLOTS}/histograma.png", dpi=100)
        plt.close(fig)

    # ── 3. Promedio móvil ─────────────────────────────────────────────────────
    def promedio_movil(self, stats):
        fig, ax = plt.subplots(figsize=(9, 4))
        tiempos = [t / 1000 for t in stats["tiempos_ms"]]
        ax.plot(tiempos, stats["voltajes"],       color="#58a6ff", linewidth=0.8,
                alpha=0.5, label="Voltaje bruto")
        ax.plot(tiempos, stats["promedio_movil"], color="#f0883e", linewidth=1.6,
                label=f"Promedio móvil (ventana={len(tiempos) if len(tiempos) < 20 else 20})")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Voltaje (V)")
        ax.set_title("Promedio móvil de la señal")
        ax.legend(fontsize=8)
        ax.grid(True)
        fig.tight_layout()
        fig.savefig(f"{RUTA_PLOTS}/promedio_movil.png", dpi=100)
        plt.close(fig)
