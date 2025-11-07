from __future__ import annotations
"""
UI mínima con Tkinter: ventana grande con gráfico a la izquierda (Matplotlib)
 y panel scrolleable a la derecha que lista las particiones mientras se "simula".

Uso:
    PYTHONPATH=src python -m src.ui.sim_points --n 5 --sleep 0.05

Opciones útiles:
    --dark / --no-dark            Fondo negro / blanco
    --rotation 90                 Rotación del polígono
    --point-size 60               Tamaño del punto
    --label-offset 0.08           Desplazamiento radial de etiquetas

De momento solo dibuja los puntos (sin bloques) y va agregando las particiones
como texto en el panel derecho, a modo de vista previa de la simulación.
Más adelante se integrará el dibujado de bloques por partición.
"""
import argparse
import tkinter as tk
from tkinter import scrolledtext
import time
from typing import List

import matplotlib
matplotlib.use("TkAgg")  # backend para integrar con Tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from combinatoria.rgs import rgs_all, rgs_to_blocks
from visual.puntos import layout_regular_ngon, draw_points, style_axes, auto_radius


class SimApp(tk.Tk):
    def __init__(self, n: int, sleep: float, dark: bool,
                 rotation: float, point_size: float, label_offset: float) -> None:
        super().__init__()
        self.title(f"Simulación de puntos y lista de particiones (n={n})")
        # Ventana grande
        self.geometry("1200x800")

        # --- LEFT: Figure ---
        fig, ax = plt.subplots(figsize=(7.5, 7.5))
        self.fig = fig
        self.ax = ax

        # fondo / estilo
        style_axes(self.ax, dark=dark)

        # puntos
        radius = auto_radius(n)
        self.positions = layout_regular_ngon(n, radius=radius, rotation_deg=rotation)
        draw_points(
            self.ax,
            self.positions,
            labels=True,
            point_size=point_size,
            label_offset_factor=label_offset,
            point_color=("white" if dark else "black"),
            label_color=("white" if dark else "black"),
        )
        self.ax.set_title(f"{n} puntos — polígono regular", color=("white" if dark else "black"))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- RIGHT: Scrolled Text ---
        self.panel = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40)
        # Estilo oscuro/claro
        if dark:
            self.panel.configure(bg="#111", fg="#f5f5f5", insertbackground="#f5f5f5")
        self.panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        # Datos de simulación
        self.n = n
        self.sleep = max(0.0, sleep)
        self.dark = dark

        # Arranca el streaming de particiones al iniciar
        self.after(200, self.stream_partitions)

                # --- BOTÓN DE CIERRE MANUAL ---
        btn_close = tk.Button(self, text="Cerrar", command=self.destroy)
        btn_close.pack(side=tk.BOTTOM, pady=8)


    def stream_partitions(self) -> None:
        """Recorre todas las particiones y las imprime en el panel derecho.
        (Por ahora, no actualiza el dibujo por partición; solo la lista textual.)
        """
        counter = 0
        for blocks in rgs_all(self.n, yield_blocks=True):
            counter += 1
            text = f"{counter:>5}: " + " | ".join("{" + ",".join(map(str, b)) + "}" for b in blocks)
            self.panel.insert(tk.END, text + "\n")
            self.panel.see(tk.END)  # autoscroll
            self.update()            # refresca UI
            if self.sleep > 0:
                time.sleep(self.sleep)

        # Al terminar, enfoca el final
        self.panel.insert(tk.END, "\nFin del listado.\n")
        self.panel.see(tk.END)


def main() -> None:
    ap = argparse.ArgumentParser(description="Simulador: puntos + panel scrolleable de particiones")
    ap.add_argument("--n", type=int, required=True, help="Tamaño del conjunto {1..n}")
    ap.add_argument("--sleep", type=float, default=0.02, help="Pausa en segundos entre líneas")
    ap.add_argument("--dark", action=argparse.BooleanOptionalAction, default=True, help="Tema oscuro")
    ap.add_argument("--rotation", type=float, default=90.0, help="Rotación inicial en grados")
    ap.add_argument("--point-size", type=float, default=70.0, help="Tamaño de marcador de punto")
    ap.add_argument("--label-offset", type=float, default=0.08, help="Offset radial de etiquetas (fracción del radio)")
    args = ap.parse_args()

    app = SimApp(
        n=args.n,
        sleep=args.sleep,
        dark=args.dark,
        rotation=args.rotation,
        point_size=args.point_size,
        label_offset=args.label_offset,
    )
    app.mainloop()


if __name__ == "__main__":
    main()
