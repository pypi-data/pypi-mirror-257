from numba import njit, prange
import numpy as np
from numpy import ndarray

__cache = True


@njit(nogil=True, parallel=True, cache=__cache)
def strain_displacement_matrix(dshp: ndarray, jac: ndarray, nDOF: int = 2) -> ndarray:
    nE = jac.shape[0]
    nP, nN = dshp.shape[:2]
    nTOTV = nN * nDOF
    nSTRE = 3
    B = np.zeros((nE, nP, nSTRE, nTOTV), dtype=dshp.dtype)
    for iE in prange(nE):
        for iP in prange(nP):
            gdshp = dshp[iP] @ np.linalg.inv(jac[iE, iP]).T
            for i in prange(nN):
                B[iE, iP, 0, 0 + i * nDOF] = gdshp[i, 0]
                B[iE, iP, 1, 1 + i * nDOF] = gdshp[i, 1]
                B[iE, iP, 2, 0 + i * nDOF] = gdshp[i, 1]
                B[iE, iP, 2, 1 + i * nDOF] = gdshp[i, 0]
    return B
