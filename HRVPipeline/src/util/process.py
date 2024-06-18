import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


def baseline_als(data, smooth, symmetry, niter=10):
    L = len(data)
    D = sparse.csc_matrix(np.diff(np.eye(L), 2))
    w = np.ones(L)
    for i in range(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + smooth * D.dot(D.transpose())
        z = spsolve(Z, w * data)
        w = symmetry * (data > z) + (1 - symmetry) * (data < z)
    return z


def baseline_flat(y, lam, p, niter=10):
    L = len(y)
    D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2))
    w = np.ones(L)
    for i in range(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w * y)
        w = p * (y > z) + (1 - p) * (y < z)
    return z
