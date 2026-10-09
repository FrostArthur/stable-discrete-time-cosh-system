# Sistema discreto LTI estable con respuesta al escalón y(n) = a·eᵇⁿ·cosh(dn)·μ(n)

Diseño e implementación en Python de un sistema discreto lineal e invariante en el tiempo (LTI) **estable** que, ante una entrada escalón $x(n) = k\,\mu(n)$ de al menos 100 muestras, produce exactamente la salida

$$y(n) = a\,e^{bn}\cosh(dn)\,\mu(n)$$

La aplicación incluye una interfaz gráfica (Tkinter + Matplotlib) para variar los parámetros y visualizar la entrada y la salida.

## Contenido

- [Características](#características)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Parámetros](#parámetros)
- [Desarrollo matemático](#desarrollo-matemático)
- [Implementación](#implementación)
- [Uso como librería](#uso-como-librería)
- [Verificación](#verificación)
- [Validaciones y errores](#validaciones-y-errores)
- [Estructura del repositorio](#estructura-del-repositorio)

## Características

- Sistema de orden 2 obtenido analíticamente a partir de la salida deseada.
- Cálculo muestra por muestra mediante la ecuación en diferencias, con condiciones iniciales nulas.
- Validación de parámetros: `k ≠ 0`, mínimo 100 muestras y estabilidad (`b < -|d|`).
- Interfaz gráfica con dos gráficas independientes (entrada y salida) en formato discreto (`stem`).
- Núcleo de cálculo separado de la interfaz, reutilizable sin GUI.

## Instalación y ejecución

Requisitos: Python 3.8 o superior.

```bash
pip install numpy matplotlib
python main.py
```

> **Nota:** Tkinter viene incluido con Python en Windows y macOS. En Linux puede requerir instalarlo aparte, por ejemplo `sudo apt install python3-tk`.

Al abrir la aplicación se generan automáticamente las gráficas con los valores por defecto. Para cambiarlos, edita los campos y pulsa **Generar gráficas**.

## Parámetros

| Parámetro    | Descripción                                   | Restricción        | Valor por defecto |
|--------------|-----------------------------------------------|--------------------|-------------------|
| `k`          | Amplitud del escalón de entrada               | `k ≠ 0`            | `1`               |
| `a`          | Amplitud de la señal de salida                | cualquier real     | `1`               |
| `b`          | Factor de decaimiento exponencial             | `b < -|d|`         | `-0.05`           |
| `d`          | Parámetro del coseno hiperbólico              | `b < -|d|`         | `0.02`            |
| `num_puntos` | Número de muestras a generar                  | entero `≥ 100`     | `200`             |

## Desarrollo matemático

### 1. Transformadas Z de entrada y salida

Entrada:

$$X(z) = \mathcal{Z}[k\mu(n)] = \frac{kz}{z-1}$$

El coseno hiperbólico se reescribe como suma de exponenciales:

$$y(n) = \frac{a}{2}\left[e^{(b+d)n} + e^{(b-d)n}\right]\mu(n)$$

Con $p_1 = e^{b+d}$ y $p_2 = e^{b-d}$, y usando $\mathcal{Z}[e^{\alpha n}\mu(n)] = \dfrac{z}{z-e^{\alpha}}$:

$$Y(z) = \frac{a}{2}\left[\frac{z}{z-p_1} + \frac{z}{z-p_2}\right]$$

### 2. Función de transferencia

$$H(z) = \frac{Y(z)}{X(z)} = \frac{a}{2k}\,\frac{(z-1)(2z-p_1-p_2)}{(z-p_1)(z-p_2)}$$

Como $p_1+p_2 = 2e^{b}\cosh(d)$ y $p_1p_2 = e^{2b}$, definiendo

$$c = e^{b}\cosh(d)$$

se obtiene:

$$H(z) = \frac{a}{k}\,\frac{(z-1)(z-c)}{z^2 - 2c\,z + e^{2b}}
= \frac{a}{k}\,\frac{1-(1+c)z^{-1}+c\,z^{-2}}{1-2c\,z^{-1}+e^{2b}z^{-2}}$$

### 3. Ecuación en diferencias (orden 2)

$$y(n) - 2c\,y(n-1) + e^{2b}\,y(n-2) = \frac{a}{k}\Big[x(n) - (1+c)\,x(n-1) + c\,x(n-2)\Big]$$

o, despejando la salida actual:

$$y(n)=2c\,y(n-1)-e^{2b}\,y(n-2)+\frac{a}{k}\Big[x(n)-(1+c)\,x(n-1)+c\,x(n-2)\Big]$$

### 4. Estabilidad

Los polos de $H(z)$ son $\rho_1 = e^{b+d}$ y $\rho_2 = e^{b-d}$. El sistema es estable (BIBO) si ambos están dentro del círculo unidad:

$$|\rho_i| < 1 \iff b + |d| < 0 \iff b < -|d|$$

Los ceros están en $z = 1$ y $z = c$. El cero en $z=1$ cancela el polo del escalón, por lo que la salida decae a cero en lugar de crecer.

### 5. Verificación analítica

Con condiciones iniciales nulas y $x(0)=k$:

$$y(0) = \frac{a}{k}\,x(0) = a,$$

que coincide con $a\,e^{0}\cosh(0) = a$.

## Implementación

La función `generar_senales(k, a, b, d, num_puntos)` de `core/core.py`:

1. Valida los parámetros (ver [Validaciones y errores](#validaciones-y-errores)).
2. Construye la entrada $x(n)=k$ para $n = 0,\dots,N-1$.
3. Precalcula las constantes $c = e^{b}\cosh(d)$, $a/k$ y $e^{2b}$.
4. Recorre las muestras aplicando la ecuación en diferencias, tomando como cero las muestras previas a $n=0$.
5. Devuelve la tupla `(senal_entrada, senal_salida)` como arreglos de NumPy.

La interfaz (`gui/interface.py`) llama a esta función, captura los errores de validación y los muestra en un cuadro de diálogo.

## Uso como librería

```python
from core.core import generar_senales

entrada, salida = generar_senales(k=1, a=1, b=-0.05, d=0.02, num_puntos=200)
```

## Verificación

Para comprobar que la salida del sistema coincide con la expresión teórica:

```python
import numpy as np
from core.core import generar_senales

k, a, b, d, N = 2.0, 3.0, -0.1, 0.05, 200
_, y = generar_senales(k, a, b, d, N)

n = np.arange(N)
y_teorica = a * np.exp(b * n) * np.cosh(d * n)

print(np.allclose(y, y_teorica))  # True
```

Observa que la salida **no depende de `k`**: el factor $a/k$ de la función de transferencia compensa la amplitud del escalón.

## Validaciones y errores

La interfaz y el núcleo comprueban las mismas condiciones y lanzan `ValueError` si no se cumplen:

| Condición                 | Error                                                |
|---------------------------|------------------------------------------------------|
| `num_puntos < 100`        | Se requieren al menos 100 puntos                     |
| `k == 0`                  | `k` no puede ser 0 (división por cero en `a/k`)      |
| `b >= -abs(d)`            | El sistema no es estable: se requiere `b < -|d|`     |
| Valores no numéricos o no finitos | Mensaje de valores no válidos en la interfaz |

## Estructura del repositorio

```
.
├── core/core.py     # ecuación en diferencias y generación de señales
├── gui/interface.py # interfaz gráfica con las gráficas de entrada y salida
├── main.py          # punto de entrada de la aplicación
├── .gitignore
└── README.md
```
