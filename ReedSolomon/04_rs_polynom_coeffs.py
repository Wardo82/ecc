"""

"""
import itertools
import numpy as np
import numpy.polynomial as poly
import random

from utils import build_vandermonde

# The alphabet are integers.
# The size k of the message word m is 4.
k = 4
# We want to 2 redundant symbols, so the code word has length n of 6.
n = 6
# The polynomial p(x) is always evaluated for the following values of x: (−1,0,1,2,3,4). Note that there are as many values xi as there are symbols in a code word.
r = [1,2]

def encode(message, r):
    k = len(message)
    n = k + len(r)

    # 1) Los simbolos del mensaje son valores y de un polinomio p(x) de grado k-1 evaluado en x. Queremos encontrar p(x)
    p = poly.Polynomial(message) # p(x)
    print(f"Polinomio del mensaje: {p}")

    # 2) Creamos el 'polinomio generador' g(x) a partir de los valores acordades de redundancia
    g = poly.Polynomial(1)
    for val in r:
        aux_pol = poly.Polynomial([-val, 1]) # -xi + x -> (x-xi)
        g = g * aux_pol
    print(f"Polinomio generador: {g}")

    # 3) Efectuamos p(x) * x**(n-k) / g(x) para encontrar el cociente y el residuo
    x_nk = np.zeros(n-k+1)
    x_nk[-1] = 1 
    quo, rem = divmod(p * poly.Polynomial(x_nk), g)
    print(f"Cociente: {quo} - Resto: {rem}")

    # 4) Definimos el codigo s(x) como p(x) * x**(n-k) - r
    s = (p * poly.Polynomial(x_nk)) - rem
    return s

message = [2, 3, -5, 1]
codeword = encode(message, r)
print(f"Mensaje: {message} -> Codigo: {codeword.coef}")
print(f"Evaluando s(x) en r: {codeword(r)}\n")

print("Corrigiendo errores:")
# Para corregir hasta s errores, necesitamos al menos 2s simbolos de redundancia (extra).
def decode_and_correct(codeword, r, k):
    """
    
    """
    n = len(codeword)

    # 1) Encontramos las sindromes
    s = codeword(r)
    print(f"Sindromes {s}")
    if not any(s):
        return codeword[:k] # No hay error, retorna los primeros k simbolos

    # 2) Si hay error, hay que probar, para cada coeficiente, cual es el erroneo. Esto se hace creando una ecuacion de una incognita (el coeficiente)
    print(f"Codigo recibido s(x): {codeword}")
    for i in range(n):
        values = []

        # Construye un polinomio modificado con posicion i como incognita
        # s(r) = alpha*r^i + (resto del polinomio) = 0 (en los valores r)
        # Buscamos alpha = -(resto del polinomio) / x^i
        for x_val in r: # Para cada valor de reduncancia a evaluar

            # Calcula el resto del polinomio
            total = 0
            for j, coef in enumerate(codeword.coef):
                if j == i:
                    continue
                total += coef * (x_val ** j)

            # Ecuacion: alpha * x^i + total = 0
            if x_val ** i == 0:
                continue

            alpha = -total / (x_val ** i)
            values.append(alpha)
    
        # Si todas las ecuaciones estan de acuerdo, hemos conseguido el error
        if len(values) == len(r) and np.allclose(values, values[0]):
            print(f"Coeficiente corrupto en posicion {i}, valor corregido: {values[0]}")

            corrected = codeword.coef.copy()
            corrected[i] = values[0]

            # Message is first k symbols
            return corrected[n-k:]

    return codeword

codeword.coef[2] = -4 # Introduce un error en el tercer simbolo 
message_rx = decode_and_correct(codeword, r, k)
print(f"Codigo recibido: {codeword} - Mensaje corregido: {message_rx}")
exact_match = all(a == b for a, b in zip(message_rx, message))
assert(exact_match)