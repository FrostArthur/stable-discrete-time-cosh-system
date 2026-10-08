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

## Implementación en Python

El núcleo calcula la salida muestra por muestra usando la ecuación en diferencias:

$$y(n)=2c\,y(n-1)-e^{2b}y(n-2)+\frac{a}{k}\left[x(n)-(1+c)x(n-1)+cx(n-2)\right]$$

donde $c=e^b\cosh(d)$. Se asumen condiciones iniciales nulas y la entrada escalón
$x(n)=k\mu(n)$ comienza en $n=0$. La implementación comprueba que el sistema sea
estable ($b<-|d|$), que $k\ne0$ y que se generen al menos 100 muestras.

La aplicación ofrece una interfaz gráfica para ingresar `k`, `a`, `b`, `d` y el
número de puntos. Al generar las señales, muestra la entrada y la salida como
señales discretas en dos gráficas independientes. Los parámetros iniciales son
`k=1`, `a=1`, `b=-0.05`, `d=0.02` y `200` puntos.

## Estructura del repositorio

```
.
├── core/core.py     # ecuación en diferencias y generación de señales
├── gui/interface.py # gráficas de entrada y salida
├── main.py          # punto de entrada de la aplicación
├── .gitignore
└── README.md
```

## Ejecución

```bash
pip install numpy matplotlib
python main.py
```

La interfaz valida las mismas condiciones que el núcleo: `k` distinto de cero,
al menos 100 puntos y estabilidad (`b < -|d|`).
