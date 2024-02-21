import numpy as np
from numpy import ndarray
from numpy.linalg import inv
from numba import njit, prange

__cache = True


@njit(nogil=True, cache=__cache)
def displacement_pattern_vector(p: ndarray, mode: int = 0) -> None:
    """
    Evaluates the matrix N at one point.
    """
    x, y = p[:2]
    if mode == 0:
        return np.array(
            [
                [1.0, 0.0, -y, x, 0, y, x * y, 0],
                [0.0, 1.0, x, 0.0, y, x, 0, x * y],
            ],
            dtype=p.dtype,
        )
    else:
        return np.array(
            [
                [1.0, 0.0, -y, x, 0, y, x * y, -0.5 * y ** 2],
                [0.0, 1.0, x, 0.0, y, x, -0.5 * x ** 2, x * y],
            ],
            dtype=p.dtype,
        )


@njit(nogil=True, parallel=True, cache=__cache)
def nodal_displacement_pattern_vector(ec: ndarray, mode: int = 0) -> ndarray:
    """
    Evaluates the matrix G for one cell.
    """
    nNE, nDOF = 4, 2
    res = np.zeros((8, 8), dtype=ec.dtype)
    for iNE in prange(nNE):
        _i = iNE * nDOF
        i_ = (iNE + 1) * nDOF
        res[_i:i_, :] = displacement_pattern_vector(ec[iNE], mode)
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def nodal_displacement_pattern_vector_bulk(
    ec: ndarray, mode: int = 0, invert: bool = False
) -> ndarray:
    """
    Evaluates the matrix G for several cells, or the H matrix if `invert` is `True`.
    """
    nE = ec.shape[0]
    res = np.zeros((nE, 8, 8), dtype=ec.dtype)
    for iE in prange(nE):
        res[iE, :, :] = nodal_displacement_pattern_vector(ec[iE], mode)
        if invert:
            res[iE, :, :] = inv(res[iE, :, :])
    return res


@njit(nogil=True, cache=__cache)
def strain_displacement_pattern_matrix_rc(out: ndarray) -> None:
    out[:, :] = np.array(
        [
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 2.0],
        ],
        dtype=out.dtype,
    )


@njit(nogil=True, cache=__cache)
def strain_displacement_pattern_matrix_c(out: ndarray) -> None:
    out[:, :] = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 2.0],
        ],
        dtype=out.dtype,
    )


@njit(nogil=True, cache=__cache)
def strain_displacement_pattern_matrix_h(
    p: ndarray, out: ndarray, mode: int = 0
) -> None:
    x, y = p[:2]
    if mode == 0:
        out[:, :] = np.array(
            [
                [y, 0.0],
                [0.0, x],
                [x, y],
            ],
            dtype=out.dtype,
        )
    else:
        out[:, :] = np.array(
            [
                [y, 0.0],
                [0.0, x],
                [0.0, 0.0],
            ],
            dtype=out.dtype,
        )


@njit(nogil=True, parallel=True, cache=__cache)
def shape_function_matrix_bulk(H: ndarray, x_glob: ndarray, mode: int = 0) -> ndarray:
    nE, nP = x_glob.shape[:2]
    res = np.zeros((nE, nP, 2, 8), dtype=x_glob.dtype)
    for iE in prange(nE):
        for iP in prange(nP):
            N = displacement_pattern_vector(x_glob[iE, iP], mode)
            res[iE, iP, :, :] = N @ H[iE]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def strain_displacement_matrix_bulk(
    ec: ndarray, Hc: ndarray, Hh: ndarray, x_glob: ndarray, mode: int = 0
) -> ndarray:
    nE, nP = x_glob.shape[:2]
    dNc = np.zeros((2, 3), dtype=x_glob.dtype)
    strain_displacement_pattern_matrix_c(dNc)
    res = np.zeros((nE, nP, 2, 8), dtype=ec.dtype)
    for iE in prange(nE):
        for iP in prange(nP):
            dNh = np.zeros((2, 2), dtype=ec.dtype)
            strain_displacement_pattern_matrix_h(x_glob[iE, iP], dNh, mode)
            res[iE, iP, :, :] = dNc @ Hc[iE] + dNh @ Hh[iE]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def elastic_stiffness_matrix_bulk(
    x_glob: ndarray,
    D: ndarray,
    Hrc: ndarray,
    Hh: ndarray,
    qw: ndarray,
    djac: ndarray,
    mode: int = 0,
) -> ndarray:
    nE, nG = x_glob.shape[:2]
    dtype = x_glob.dtype
    dNrc = np.zeros((3, 6), dtype=dtype)
    strain_displacement_pattern_matrix_rc(dNrc)
    res = np.zeros((nE, 8, 8), dtype=dtype)
    for iE in prange(nE):
        for iG in range(nG):
            weight = qw[iG] * djac[iE, iG]
            # basic stiffness
            res[iE, :, :] += (Hrc[iE].T @ dNrc.T @ D[iE] @ dNrc @ Hrc[iE]) * weight
            # higher order stiffnessű
            dNh = np.zeros((3, 2), dtype=dtype)
            strain_displacement_pattern_matrix_h(x_glob[iE, iG], dNh, mode)
            res[iE, :, :] += (Hh[iE].T @ dNh.T @ D[iE] @ dNh @ Hh[iE]) * weight
    return res
