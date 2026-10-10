import math
import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk,
)
from matplotlib.figure import Figure

from core.core import generar_senales


class InterfazSistema:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema discreto estable")
        self.root.geometry("1100x700")
        self.root.minsize(850, 550)

        self.valores = {
            "k": tk.StringVar(value="1"),
            "a": tk.StringVar(value="1"),
            "b": tk.StringVar(value="-0.05"),
            "d": tk.StringVar(value="0.02"),
            "num_puntos": tk.StringVar(value="200"),
        }

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._crear_controles()
        self._crear_graficas()

    def _crear_controles(self):
        controles = ttk.LabelFrame(
            self.root, text="Constantes del sistema", padding=12
        )
        controles.grid(
            row=0, column=0, padx=(12, 6), pady=12, sticky=tk.NSEW
        )
        controles.columnconfigure(0, weight=1)
        campos = (
            ("k", "k"),
            ("a", "a"),
            ("b", "b"),
            ("d", "d"),
            ("num_puntos", "Número de puntos"),
        )
        for fila, (clave, etiqueta) in enumerate(campos):
            ttk.Label(controles, text=etiqueta).grid(
                row=fila * 2, column=0, padx=4, pady=(8, 2), sticky=tk.W
            )
            ttk.Entry(controles, textvariable=self.valores[clave], width=16).grid(
                row=fila * 2 + 1, column=0, padx=4, sticky=tk.EW
            )

        ttk.Button(
            controles, text="Generar gráficas", command=self.generar_graficas
        ).grid(
            row=len(campos) * 2,
            column=0,
            padx=4,
            pady=(16, 4),
            sticky=tk.EW,
        )

    def _crear_graficas(self):
        contenedor = ttk.Frame(self.root, padding=(6, 12, 12, 12))
        contenedor.grid(row=0, column=1, sticky=tk.NSEW)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure((0, 1), weight=1)

        self.ejes = []
        for fila, titulo in enumerate(
            ("Gráfica de la señal de entrada", "Gráfica de la señal de salida")
        ):
            panel = ttk.LabelFrame(contenedor, text=titulo, padding=6)
            panel.grid(
                row=fila,
                column=0,
                pady=(0, 8) if fila == 0 else (0, 0),
                sticky=tk.NSEW,
            )

            figura = Figure(figsize=(7, 3), dpi=100)
            eje = figura.add_subplot(111)
            eje.set_xlabel("n")
            eje.set_ylabel("Amplitud")
            eje.grid(True, alpha=0.3)

            canvas = FigureCanvasTkAgg(figura, master=panel)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(canvas, panel, pack_toolbar=False)
            toolbar.update()
            toolbar.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.draw()
            self.ejes.append((eje, canvas))

        self.generar_graficas()

    def generar_graficas(self):
        try:
            k = float(self.valores["k"].get())
            a = float(self.valores["a"].get())
            b = float(self.valores["b"].get())
            d = float(self.valores["d"].get())
            num_puntos = int(self.valores["num_puntos"].get())
            if not all(math.isfinite(valor) for valor in (k, a, b, d)):
                raise ValueError("Los valores k, a, b y d deben ser números finitos.")
            entrada, salida = generar_senales(k, a, b, d, num_puntos)
        except (ValueError, OverflowError) as error:
            messagebox.showerror("Valores no válidos", str(error), parent=self.root)
            return

        muestras = np.arange(num_puntos)
        for (eje, canvas), senal, titulo in zip(
            self.ejes,
            (entrada, salida),
            ("Señal de entrada x[n]", "Señal de salida y[n]"),
        ):
            eje.clear()
            eje.stem(muestras, senal)
            eje.set_title(titulo)
            eje.set_xlabel("n")
            eje.set_ylabel("Amplitud")
            eje.grid(True, alpha=0.3)
            canvas.draw_idle()


def iniciar_interfaz():
    root = tk.Tk()
    InterfazSistema(root)
    root.mainloop()
