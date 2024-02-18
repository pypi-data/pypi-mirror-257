import numpy as np

def householder_reflection(v):
    """Create a Householder reflection matrix."""
    u = v / (v[0] + np.copysign(np.linalg.norm(v), v[0]))
    u[0] = 1
    H = np.eye(len(v)) - (2 / np.dot(u, u)) * np.outer(u, u)
    return H