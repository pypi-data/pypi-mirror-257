import numpy as np
from numpy import ndarray
from numpy.linalg import inv
from numba import njit, prange

from sigmaepsilon.mesh.utils.tri import loc_to_glob_tri

__cache = True

# fmt: off
@njit(nogil=True, cache=__cache)
def displacement_pattern_vector(p: ndarray) -> None:
    """
    Evaluates the matrix N at one point.
    """
    x, y = p[:2]
    return np.array(
        [
            [1.0, x, y, x**2, x * y, y**2, x**3, x**2 * y + x * y**2, y**3],
            [0.0, 0.0, 1.0, 0.0, x, 2.0 * y, 0.0, x**2 + 2.0 * x * y, 3.0 * y**2],
            [0.0, -1.0, 0.0, -2.0 * x, -y, 0.0, -3.0 * x**2, -2.0 * x * y - y**2, 0.0],
        ],
        dtype=p.dtype,
    )


@njit(nogil=True, cache=__cache)
def displacement_pattern_vector_rc(p: ndarray) -> None:
    """
    Evaluates the matrix Nrc at one point.
    """
    x, y = p[:2]
    return np.array(
        [
            [1.0, x, y, x**2, x * y, y**2],
            [0.0, 0.0, 1.0, 0.0, x, 2.0 * y],
            [0.0, -1.0, 0.0, -2.0 * x, -y, 0.0],
        ],
        dtype=p.dtype,
    )


@njit(nogil=True, cache=__cache)
def displacement_pattern_vector_h(p: ndarray) -> None:
    """
    Evaluates the matrix Nh at one point.
    """
    x, y = p[:2]
    return np.array(
        [
            [x**3, x**2 * y + x * y**2, y**3],
            [0.0, x**2 + 2.0 * x * y, 3.0 * y**2],
            [-3 * x**2, -2.0 * x * y - y**2, 0.0],
        ],
        dtype=p.dtype,
    )
# fmt: on


@njit(nogil=True, parallel=True, cache=__cache)
def nodal_displacement_pattern_vector(ec: ndarray) -> ndarray:
    """
    Evaluates the matrix G for one cell.
    """
    nNE, nDOF = 3, 3
    res = np.zeros((9, 9), dtype=ec.dtype)
    for iNE in prange(nNE):
        _i = iNE * nDOF
        i_ = (iNE + 1) * nDOF
        res[_i:i_, :] = displacement_pattern_vector(ec[iNE])
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def nodal_displacement_pattern_vector_bulk(
    ec: ndarray, invert: bool = False
) -> ndarray:
    """
    Evaluates the matrix G for several cells, or the H matrix if `invert` is `True`.
    """
    nE = ec.shape[0]
    res = np.zeros((nE, 9, 9), dtype=ec.dtype)
    for iE in prange(nE):
        res[iE, :, :] = nodal_displacement_pattern_vector(ec[iE])
        if invert:
            res[iE, :, :] = inv(res[iE, :, :])
    return res


@njit(nogil=True, cache=__cache)
def strain_displacement_pattern_matrix_rc(out: ndarray) -> None:
    out[:, :] = np.array(
        [
            [0.0, 0.0, 0.0, -2.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, -2.0],
            [0.0, 0.0, 0.0, 0.0, -2.0, 0.0],
        ],
        dtype=out.dtype,
    )


@njit(nogil=True, cache=__cache)
def strain_displacement_pattern_matrix_c(out: ndarray) -> None:
    out[:, :] = np.array(
        [
            [-2.0, 0.0, 0.0],
            [0.0, 0.0, -2.0],
            [0.0, -2.0, 0.0],
        ],
        dtype=out.dtype,
    )


@njit(nogil=True, cache=__cache)
def strain_displacement_pattern_matrix_h(p: ndarray, out: ndarray) -> None:
    x, y = p[:2]
    out[:, :] = np.array(
        [
            [-6 * x, -2 * y, 0.0],
            [0.0, -2 * x, -6 * y],
            [0.0, -4 * (x + y), 0.0],
        ],
        dtype=out.dtype,
    )


@njit(nogil=True, parallel=True, cache=__cache)
def shape_function_matrix_bulk(ec: ndarray, H: ndarray, x_loc: ndarray) -> ndarray:
    nE = ec.shape[0]
    nP = x_loc.shape[0]
    res = np.zeros((nE, nP, 3, 9), dtype=ec.dtype)
    for iE in prange(nE):
        for iP in prange(nP):
            x_glob = loc_to_glob_tri(x_loc[iP], ec[iE])
            N = displacement_pattern_vector(x_glob)
            res[iE, iP, :, :] = N @ H[iE]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def strain_displacement_matrix_bulk(
    ec: ndarray, Hc: ndarray, Hh: ndarray, x_loc: ndarray
) -> ndarray:
    nE = ec.shape[0]
    nP = x_loc.shape[0]
    dNc = np.zeros((3, 3), dtype=ec.dtype)
    strain_displacement_pattern_matrix_c(dNc)
    res = np.zeros((nE, nP, 3, 9), dtype=ec.dtype)
    for iE in prange(nE):
        for iP in prange(nP):
            x_glob = loc_to_glob_tri(x_loc[iP], ec[iE])
            dNh = np.zeros((3, 3), dtype=ec.dtype)
            strain_displacement_pattern_matrix_h(x_glob, dNh)
            res[iE, iP, :, :] = dNc @ Hc[iE] + dNh @ Hh[iE]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def elastic_stiffness_matrix_bulk(
    ec: ndarray,
    D: ndarray,
    Hrc: ndarray,
    Hh: ndarray,
    qp: ndarray,
    qw: ndarray,
    djac: ndarray,
) -> ndarray:
    nE, nG = ec.shape[0], qp.shape[0]
    dtype = ec.dtype
    dNrc = np.zeros((3, 6), dtype=dtype)
    strain_displacement_pattern_matrix_rc(dNrc)
    res = np.zeros((nE, 9, 9), dtype=dtype)
    for iE in prange(nE):
        for iG in range(nG):
            weight = qw[iG] * djac[iE, iG]
            # basic stiffness
            res[iE, :, :] += (Hrc[iE].T @ dNrc.T @ D[iE] @ dNrc @ Hrc[iE]) * weight
            # higher order stiffness
            p = loc_to_glob_tri(qp[iG], ec[iE])
            dNh = np.zeros((3, 3), dtype=dtype)
            strain_displacement_pattern_matrix_h(p, dNh)
            res[iE, :, :] += (Hh[iE].T @ dNh.T @ D[iE] @ dNh @ Hh[iE]) * weight
    return res
