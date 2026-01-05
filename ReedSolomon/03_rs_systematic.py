"""
En este script queremos explorar codigos sistematicos de Reed-Solomon, donde al mensaje se le anaden los simbolos redundantes.
En otras palabras: Codificar m=(2,3,-5,1) en algo como c=(2,3,-5,1,r4,r5).

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
x = [-1, 0, 1, 2, 3, 4]

def encode(message, x):
    n = len(x)
    k = len(message)

    # 1) Los simbolos del mensaje son valores y de un polinomio p(x) de grado k-1 evaluado en x. Queremos encontrar p(x)
    A = build_vandermonde(x[0:k])
    coeffs = np.linalg.solve(A, message)
    p = poly.Polynomial(coeffs) # p(x)
    #2) Evaluate p(x) on the new redundant simbols
    r = p(x[k:])
    codeword = [*message, *r]
    return codeword

message = [2, 3, -5, 1]
codeword = encode(message, x)
print(f"Mensaje: {message} -> Codigo: {codeword}")


