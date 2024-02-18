import numpy as np
from .household import householder_reflection  


def qr_decomposition(A):
    """Perform QR decomposition of matrix A using Householder reflections."""
    m, n = A.shape
    Q = np.eye(m)
    R = A.copy()

    for j in range(n):
        # Create the Householder reflection matrix for column j
        x = R[j:, j]
        H = np.eye(m)
        H[j:, j:] = householder_reflection(x)
        R = np.dot(H, R)
        Q = np.dot(Q, H.T)

    return Q, R

