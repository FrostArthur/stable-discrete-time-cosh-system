import math
import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from core.core import generar_senales


class InterfazSistema:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema discreto estable")
        self.root.geometry("1100x700")
        self.root.minsize(800, 550)

        self.valores = {
            "k": tk.StringVar(value="1"),
            "a": tk.StringVar(value="1"),
            "b": tk.StringVar(value="-0.05"),
            "d": tk.StringVar(value="0.02"),
            "num_puntos": tk.StringVar(value="200"),
        }

        self._crear_controles()
        self._crear_graficas()

    def _crear_controles(self):
        controles = ttk.Frame(self.root, padding=12)
        controles.pack(fill=tk.X)

        campos = (
            ("k", "k"),
            ("a", "a"),
            ("b", "b"),
            ("d", "d"),
            ("num_puntos", "Número de puntos"),
        )
        for columna, (clave, etiqueta) in enumerate(campos):
            ttk.Label(controles, text=etiqueta).grid(
                row=0, column=columna, padx=6, pady=(0, 4), sticky=tk.W
            )
            ttk.Entry(controles, textvariable=self.valores[clave], width=16).grid(
                row=1, column=columna, padx=6, sticky=tk.EW
            )
            controles.columnconfigure(columna, weight=1)

        ttk.Button(
            controles, text="Generar gráficas", command=self.generar_graficas
        ).grid(row=1, column=len(campos), padx=(12, 6), sticky=tk.EW)

    def _crear_graficas(self):
        contenedor = ttk.Frame(self.root, padding=(12, 0, 12, 12))
        contenedor.pack(fill=tk.BOTH, expand=True)
        contenedor.columnconfigure((0, 1), weight=1)
        contenedor.rowconfigure(0, weight=1)

        self.ejes = []
        for columna, titulo in enumerate(("Señal de entrada", "Señal de salida")):
            panel = ttk.LabelFrame(contenedor, text=titulo, padding=6)
            panel.grid(row=0, column=columna, padx=6, sticky=tk.NSEW)

            figura = Figure(figsize=(5, 4), dpi=100)
            eje = figura.add_subplot(111)
            eje.set_xlabel("n")
            eje.set_ylabel("Amplitud")
            eje.grid(True, alpha=0.3)

            canvas = FigureCanvasTkAgg(figura, master=panel)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
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
