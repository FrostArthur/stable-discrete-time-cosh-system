# Sistema discreto estable con salida y(n) = a·e^(bn)·cosh(dn)·μ(n)

## Objetivo

Diseñar e implementar en Python (o Matlab) un sistema discreto LTI **estable** que, para una
entrada escalón x(n) = k·μ(n) de mínimo 100 puntos, genere la salida

$$y(n) = a\,e^{bn}\cosh(dn)\,\mu(n)$$

y graficar la señal de entrada y la de salida para verificar su funcionamiento.

## Desarrollo matemático

### 1. Transformadas Z de entrada y salida

Entrada:

$$X(z) = \mathcal{Z}[k\mu(n)] = \frac{kz}{z-1}$$

Se reescribe el coseno hiperbólico como suma de exponenciales:

$$y(n) = \frac{a}{2}\left[e^{(b+d)n} + e^{(b-d)n}\right]\mu(n)$$

Con $p_1 = e^{b+d}$ y $p_2 = e^{b-d}$, y usando $\mathcal{Z}[e^{an}\mu(n)] = \frac{z}{z-e^{a}}$:

$$Y(z) = \frac{a}{2}\left[\frac{z}{z-p_1} + \frac{z}{z-p_2}\right]$$

### 2. Función de transferencia

$$H(z) = \frac{Y(z)}{X(z)} = \frac{a}{2k}\,\frac{(z-1)(2z-p_1-p_2)}{(z-p_1)(z-p_2)}$$

Como $p_1+p_2 = 2e^{b}\cosh(d)$ y $p_1p_2 = e^{2b}$, y definiendo $c = e^{b}\cosh(d)$:

$$H(z) = \frac{a}{k}\,\frac{(z-1)(z-c)}{z^2 - 2c\,z + e^{2b}}
= \frac{a}{k}\,\frac{1-(1+c)z^{-1}+c\,z^{-2}}{1-2c\,z^{-1}+e^{2b}z^{-2}}$$

### 3. Ecuación en diferencias (sistema de orden 2)

$$y(n) - 2c\,y(n-1) + e^{2b}\,y(n-2) = \frac{a}{k}\Big[x(n) - (1+c)\,x(n-1) + c\,x(n-2)\Big]$$

con $c = e^{b}\cosh(d)$.

### 4. Estabilidad

Polos: $\rho_1 = e^{b+d}$, $\rho_2 = e^{b-d}$.

Criterio: el sistema es estable si $|\rho_i| < 1$, es decir

$$b + |d| < 0 \quad\Longleftrightarrow\quad b < -|d|$$

### 5. Verificación

Condiciones iniciales: $y(0) = \frac{a}{k}\,x(0) = a$, que coincide con
$a\,e^{0}\cosh(0) = a$.

## Implementación (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter

k, a, b, d = 2.0, 3.0, -0.05, 0.03   # estable: b < -|d|
N = 150                               # >= 100 puntos
n = np.arange(N)
x = k * np.ones(N)                    # x(n) = k·μ(n)

c   = np.exp(b) * np.cosh(d)
num = (a / k) * np.array([1, -(1 + c), c])
den = np.array([1, -2 * c, np.exp(2 * b)])

y = lfilter(num, den, x)                       # salida del sistema
y_teo = a * np.exp(b * n) * np.cosh(d * n)     # salida esperada
assert np.allclose(y, y_teo)

plt.stem(n, x, linefmt="C0-", markerfmt="C0o", label="x(n)")
plt.stem(n, y, linefmt="C3-", markerfmt="C3o", label="y(n)")
plt.xlabel("n"); plt.legend(); plt.grid(True); plt.show()
```

## Estructura del repositorio

```
.
├── lab2.py          # implementación del sistema
├── lab2.m           # (opcional) versión Matlab
├── informe/         # informe estilo IEEE
├── .gitignore
└── README.md
```

## Ejecución

```bash
pip install numpy scipy matplotlib
python lab2.py
```
