import numpy as np
import math

#La ecuación en diferencias a aplicar es: 
#   (a/k)*[x[n] - (exp(b)*cosh(d)+1)*x[n-1] + exp(b)*cosh(d)*x[n-2]] + 2*exp(b)*cosh(d)*y[n-1] - exp(2*b)*y[n-2]

def generar_senales(k, a, b, d, num_puntos: int = 100):
    #Al menos 100 puntos
    if num_puntos < 100:
        raise ValueError("Se requieren al menos 100 puntos")
    #k no puede ser 0 porque se dividiria por 0
    if k == 0:
        raise ValueError("k no puede ser 0")
    #Criterio de estabilidad:
    if b >= -abs(d):
        raise ValueError("El sistema no es estable: se requiere b < -|d|")
    
    #Señal de entrada
    senal_entrada = np.full(num_puntos, k, dtype=float)
    
    #c = exp(b)*cosh(d)
    c = math.exp(b)*math.cosh(d)
    
    #f = a / k
    f = a / k
    
    #expo2 = exp(2b)
    expo2 = math.exp(2*b)
    
    senal_salida = np.zeros(num_puntos, dtype=float)

    for i in range(num_puntos):
        x_n = senal_entrada[i]
        x_n_1 = senal_entrada[i - 1] if i >= 1 else 0.0
        x_n_2 = senal_entrada[i - 2] if i >= 2 else 0.0
        y_n_1 = senal_salida[i - 1] if i >= 1 else 0.0
        y_n_2 = senal_salida[i - 2] if i >= 2 else 0.0
            
        senal_salida[i] = f*(x_n - (c+1)*x_n_1 + c*x_n_2) + 2*c*y_n_1 - expo2*y_n_2

    return senal_entrada, senal_salida
    
