from __future__ import annotations

import math

import numpy as np


def generate_signals(
    a: float = 1.0,
    b: float = -0.05,
    d: float = 0.02,
    k: float = 1.0,
    num_samples: int = 200,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate x[n] = k*u[n] and its output using the difference equation.

    The system is stable when both poles exp(b + d) and exp(b - d) lie
    inside the unit circle, equivalently b < -abs(d).
    """
    parameters = (a, b, d, k)
    if not all(math.isfinite(value) for value in parameters):
        raise ValueError("a, b, d, and k must be finite real numbers.")
    if k == 0:
        raise ValueError("k must be nonzero to define the transfer function.")
    if b >= -abs(d):
        raise ValueError("The system is not stable: b must be less than -abs(d).")
    if isinstance(num_samples, bool) or not isinstance(num_samples, int):
        raise TypeError("num_samples must be an integer.")
    if num_samples < 100:
        raise ValueError("num_samples must be at least 100.")

    n = np.arange(num_samples)
    input_signal = np.full(num_samples, k, dtype=float)
    output_signal = np.zeros(num_samples, dtype=float)

    pole_1 = math.exp(b + d)
    pole_2 = math.exp(b - d)
    c = (pole_1 + pole_2) / 2
    pole_product = math.exp(2 * b)
    gain = a / k

    for index in range(num_samples):
        x_n = input_signal[index]
        x_n_minus_1 = input_signal[index - 1] if index >= 1 else 0.0
        x_n_minus_2 = input_signal[index - 2] if index >= 2 else 0.0
        y_n_minus_1 = output_signal[index - 1] if index >= 1 else 0.0
        y_n_minus_2 = output_signal[index - 2] if index >= 2 else 0.0

        output_signal[index] = (
            2 * c * y_n_minus_1
            - pole_product * y_n_minus_2
            + gain
            * (x_n - (1 + c) * x_n_minus_1 + c * x_n_minus_2)
        )

    return n, input_signal, output_signal