from numba import njit, prange
from numpy import ndarray

__cache = True


@njit(nogil=True, cache=__cache)
def _gauss_approximator(N: ndarray, values_source: ndarray, out: ndarray) -> ndarray:
    # N: (nP x nG)
    # values_source: (nE, nG, nSTRE, nRHS)
    # out: (nE, nP, nSTRE, nRHS)
    nE, _, nSTRE, nRHS = values_source.shape
    for iE in prange(nE):
        for iRHS in prange(nRHS):
            for iSTRE in prange(nSTRE):
                out[iE, :, iSTRE, iRHS] = N @ values_source[iE, :, iSTRE, iRHS]
