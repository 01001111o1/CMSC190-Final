"""
ACM_Generation.py: File to generate a 2x2 Arnold's Cat Map for a given image size N
"""
import numpy as np
from sympy import factorint
from numpy.random import randint

"""
Function to generate a random 2x2 matrix whose determinant is coprime to the image size

Parameters:

    1. N : Positive integer denoting the size of the image

Output: 
    
    1. M : 2x2 unrestricted arnold's cat map matrix
    2. det : determinant of M
    3. period : positive integer denoting the minimal period of M

"""
def generate_ACM_Matrix(N: int) -> tuple[np.ndarray, float, int]:

    factor_dict: dict[int, int] = factorint(N)
    p, k = list(factor_dict.keys()), list(factor_dict.values())
    r: int = len(p)

    n, m, a, b, c, d, barn, bara, barb = [np.zeros(r) for _ in range(9)]
    
    A: list[np.ndarray] = [None] * r

    for i in range(r):
        
        pk = p[i] ** k[i]

        n[i] = N / pk

        for j in range(1, pk):
            if n[i] * j % pk == 1:
                barn[i] = j
                break

        m[i] = randint(1, pk)
        while m[i] % p[i] == 0:
            m[i] = randint(1, pk)

        a[i] = randint(1, pk)
        if a[i] % p[i] > 0:
            for j in range(1, pk):
                if a[i] * j % pk == 1:
                    bara[i] = j
                    break
            b[i] = randint(0, pk)
            c[i] = randint(0, pk)
            d[i] = (bara[i] * (b[i] * c[i] + m[i])) % pk
        else:
            b[i] = randint(1, pk)
            while b[i] % p[i] == 0:
                b[i] = randint(1, pk)
            for j in range(1, pk):
                if b[i] * j % pk == 1:
                    barb[i] = j
                    break
            d[i] = randint(0, pk) 
            c[i] = (barb[i] * (a[i] * d[i] - m[i])) % pk
        A[i] = np.array([[a[i], b[i]], [c[i], d[i]]])

    M: np.ndarray = np.zeros((2, 2))
    for i in range(r):
        M += n[i] * barn[i] * A[i]

    M %= N
    det: float = np.linalg.det(M) % N

    B: np.ndarray = np.eye(2)
    counter: int = 1
    while True:
        B = np.dot(B, M) % N
        if np.array_equal(B, np.eye(2)):
            period: int = counter
            break
        else:
            counter += 1

    return M, det, period