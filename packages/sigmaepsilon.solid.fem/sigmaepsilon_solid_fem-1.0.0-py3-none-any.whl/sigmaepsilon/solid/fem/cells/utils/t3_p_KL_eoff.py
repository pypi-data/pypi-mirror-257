import numpy as np
from numpy import ndarray
from numba import njit, prange

from sigmaepsilon.mesh.utils.tri import loc_to_nat_tri, loc_to_glob_tri, area_tri

__cache = True


# fmt: off
@njit(nogil=True, cache=__cache)
def _lumping_matrix(ec: ndarray) -> ndarray:
    (x1, x2, x3), (y1, y2, y3) = ec[:, 0], ec[:, 1]
    x21, x13, x32 = x2 - x1, x1 - x3, x3 - x2
    y21, y13, y32 = y2 - y1, y1 - y3, y3 - y2
    return 0.5 * np.array(
        [
            [0.0, 0.0, 0.0],
            [0.0, x32, y32],
            [y32, 0.0, x32],
            [0.0, 0.0, 0.0],
            [0.0, x13, y13],
            [y13, 0.0, x13],
            [0.0, 0.0, 0.0],
            [0.0, x21, y21],
            [y21, 0.0, x21],
        ],
        dtype=ec.dtype,
    )
   

@njit(nogil=True, cache=__cache)
def _Hc(ec: ndarray) -> ndarray:
    (x1, x2, x3), (y1, y2, y3) = ec[:, 0], ec[:, 1]
    x21, x13, x32 = x2 - x1, x1 - x3, x3 - x2
    y21, y13, y32 = y2 - y1, y1 - y3, y3 - y2
    return np.array(
        [
            [
                12.0, -6*y21+9*y32, 6*x21-9*x32, 12.0, -6*y32-15*y13, 6*x32-15*x13,
                -24.0, -3*y13+3*y32, 3*x13-3*x32
            ],
            [
                -24.0, -3*y21+3*y13, 3*x21-3*x13, 12.0, -6*y32+9*y13, 6*x32-9*x13,
                12.0, -6*y13-5*y21, 6*x13+15*x21
            ],
            [
                12.0, -6*y21-15*y32, 6*x21+15*x32, -24.0, -3*y32+3*y21, 3*x32+3*x21,
                12.0, -6*y13+9*y21, 6*x13-9*x21
            ],
        ],
        dtype=ec.dtype
    ) / 108


@njit(nogil=True, cache=__cache)
def _Hh(ec: ndarray) -> ndarray:
    (x1, x2, x3), (y1, y2, y3) = ec[:, 0], ec[:, 1]
    x21, x13, x32 = x2 - x1, x1 - x3, x3 - x2
    y21, y13, y32 = y2 - y1, y1 - y3, y3 - y2
    return np.array(
        [
            [-12.0, y32-6*y21, -x32+6*x21, 12.0, y13-6*y21, -x13+6*x21, 0.0, y21, -x21],
            [0.0, y32, -x32, -12.0, y13-6*y32, -x13+6*x32, 12.0, y21-6*y32, -x21+6*x32],
            [12.0, y32-6*y13, -x32+6*x13, 0.0, y13, -x13, -12.0, y21-6*y13, -x21+6*x13]
        ],
        dtype=ec.dtype
    ) / 54


@njit(nogil=True, cache=__cache)
def _H(ec: ndarray) -> ndarray:
    (x1, x2, x3), (y1, y2, y3) = ec[:, 0], ec[:, 1]
    x21, x13, x32 = x2 - x1, x1 - x3, x3 - x2
    y21, y13, y32 = y2 - y1, y1 - y3, y3 - y2
    return np.array(
        [
            [
                60.0, -10*y13+6*y21, 10*x13-6*x21, -36.0, 2*y21-6*y32, -2*x21+6*x32, 
                12.0, 2*y32+6*y13, -2*x32-6*x13
            ],
            [
                12.0, 2*y13 + 6*y21, -2*x13-6*x21, 60.0, -10*y21+6*y32, 10*x21-6*x32,
                -36.0, 2*y32 - 6*y13, -2*x32+6*x13
            ],
            [
                -36.0, 2*y13-6*y21, -2*x13+6*x21, 12.0, 2*y21+6*y32, -2*x21-6*x32,
                60.0, -10*y32+6*y13, 10*x32-6*x13
            ],
            [
                12.0, -6*y21+9*y32, 6*x21-9*x32, 12.0, -6*y32-15*y13, 6*x32-15*x13,
                -24.0, -3*y13+3*y32, 3*x13-3*x32
            ],
            [
                -24.0, -3*y21+3*y13, 3*x21-3*x13, 12.0, -6*y32+9*y13, 6*x32-9*x13,
                12.0, -6*y13-5*y21, 6*x13+15*x21
            ],
            [
                12.0, -6*y21-15*y32, 6*x21+15*x32, -24.0, -3*y32+3*y21, 3*x32+3*x21,
                12.0, -6*y13+9*y21, 6*x13-9*x21
            ],
            [
                -24.0, 2*(y32-6*y21), 2*(-x32+6*x21), 24.0, 2*(y13-6*y21), 
                2*(-x13+6*x21), 0.0, 2*y21, -2*x21
            ],
            [
                0.0, 2*y32, -2*x32, -24.0, 2*(y13-6*y32), 2*(-x13+6*x32), 24.0, 
                2*(y21-6*y32), 2*(-x21+6*x32)
            ],
            [
                24.0, 2*(y32-6*y13), 2*(-x32+6*x13), 0.0, 2*y13, -2*x13, -24.0, 
                2*(y21-6*y13), 2*(-x21+6*x13)
            ]
        ],
        dtype=ec.dtype
    ) / 108


@njit(nogil=True, cache=__cache)
def _Bh(ec: ndarray) -> ndarray:
    (x1, x2, x3), (y1, y2, y3) = ec[:, 0], ec[:, 1]
    A = area_tri(ec)
    lam = 1 / np.sqrt(A)
    xi1 = lam * x1
    xi2 = lam * x2
    xi3 = lam * x3
    eta1 = lam * y1
    eta2 = lam * y2
    eta3 = lam * y3
    c = 3 / 2
    a1 = -c * lam * eta3
    a2 = -c * lam * eta1
    a3 = -c * lam * eta2
    b1 = c * lam * xi3
    b2 = c * lam * xi1
    b3 = c * lam * xi2
    return 6 * np.array(
        [
            [a1**2, a2**2, a3**2],
            [b1**2, b2**2, b3**2],
            [2 * a1 * b1, 2 * a2 * b2, 2 * a3 * b3],
        ],
        dtype=ec.dtype,
    )
    

@njit(nogil=True, parallel=True, cache=__cache)
def shape_function_matrix_bulk(ec: ndarray, x_loc: ndarray) -> ndarray:
    nE = ec.shape[0]
    nP = x_loc.shape[0]
    res = np.zeros((nE, nP, 3, 9), dtype=ec.dtype)
    for iE in prange(nE):
        (x1, x2, x3), (y1, y2, y3) = ec[iE, :, 0], ec[iE, :, 1]
        A = area_tri(ec[iE])
        lam = 1 / np.sqrt(A)
        xi1 = lam * x1
        xi2 = lam * x2
        xi3 = lam * x3
        eta1 = lam * y1
        eta2 = lam * y2
        eta3 = lam * y3
        c = 3 / 2
        a1 = -c * lam * eta3
        a2 = -c * lam * eta1
        a3 = -c * lam * eta2
        b1 = c * lam * xi3
        b2 = c * lam * xi1
        b3 = c * lam * xi2
        for iP in prange(nP):
            A1, A2, A3 = loc_to_nat_tri(x_loc[iP])
            A12 = A1 - A2
            A23 = A2 - A3
            A31 = A3 - A1
            x_glob = loc_to_glob_tri(x_loc[iP], ec[iE])
            xi = lam * x_glob[0]
            eta = lam * x_glob[1]
            N = np.array(
                [
                    [
                        1.0 + A1 - A2, 1.0 + A2 - A3, 1.0 + A3 - A1, 
                        (A1 - A2)**2, (A2 - A3)**2, (A3 - A1)**2,
                        (A1 - A2)**3, (A2 - A3)**3, (A3 - A1)**3
                    ],
                    [
                        0.0, lam, 0.0, 2.0*lam*xi, lam*eta, 0.0, 
                        3.0*a1*A12**2, 3.0*a2*A23**2, 3.0*a3*A31**2
                    ],
                    [
                        0.0, 0.0, lam, 0.0, lam*xi, 2.0*lam*eta,
                        3.0*b1*A12**2, 3.0*b2*A23**2, 3.0*b3*A31**2
                    ],
                ], 
                dtype=ec.dtype
            )
            res[iE, iP, :, :] = N @ _H(ec[iE])
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def strain_displacement_matrix_bulk(ec: ndarray, x_loc: ndarray) -> ndarray:
    nE = ec.shape[0]
    nP = x_loc.shape[0]
    c = 3 / 2
    res = np.zeros((nE, nP, 3, 9), dtype=ec.dtype)
    for iE in prange(nE):
        (x1, x2, x3), (y1, y2, y3) = ec[iE, :, 0], ec[iE, :, 1]
        A = area_tri(ec[iE])
        lam = 1 / np.sqrt(A)
        lam2 = lam**2
        xi1 = lam * x1
        xi2 = lam * x2
        xi3 = lam * x3
        eta1 = lam * y1
        eta2 = lam * y2
        eta3 = lam * y3
        a1 = -c * lam * eta3
        a2 = -c * lam * eta1
        a3 = -c * lam * eta2
        b1 = c * lam * xi3
        b2 = c * lam * xi1
        b3 = c * lam * xi2
        dNc = 2.0 * np.array(
            [
                [lam2, 0.0, 0.0],
                [0.0, 0.0, lam2],
                [0.0, lam2, 0.0],
            ], 
            dtype=ec.dtype
        )
        for iP in prange(nP):
            A1, A2, A3 = loc_to_nat_tri(x_loc[iP])
            A12 = A1 - A2
            A23 = A2 - A3
            A31 = A3 - A1
            dNh = 2.0 * np.array(
                [
                    [3.0*a1**2*A12, 3.0*a2**2*A23, 3.0*a3**2*A31],
                    [3.0*b1**2*A12, 3.0*b2**2*A23, 3.0*b3**2*A31],
                    [6.0*a1*b1*A12, 6.0*a2*b2*A23, 6.0*a3*b3*A31],
                ], 
                dtype=ec.dtype
            )
            res[iE, iP, :, :] = -dNc @ _Hc(ec[iE]) - dNh @ _Hh(ec[iE])
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def basic_elastic_stiffness_matrix_bulk(ec: ndarray, D: ndarray, out: ndarray) -> None:
    nE = ec.shape[0]
    for iE in prange(nE):
        A = area_tri(ec[iE])
        L = _lumping_matrix(ec[iE])
        out[iE] += (L @ D[iE] @ L.T) / A


@njit(nogil=True, parallel=True, cache=__cache)
def higher_order_elastic_stiffness_matrix_bulk(
    ec: ndarray, D: ndarray, out: ndarray, beta:float=0.5
) -> None:
    """
    A default value of 0.5 is adopted for the scaling parameter 'beta', 
    to account for bad element ratios.
    """
    nE = ec.shape[0]
    J = np.array(
        [
            [2.0, -1.0, -1.0], 
            [-1.0, 2.0, -1.0], 
            [-1.0, -1.0, 2.0]
        ], 
        dtype=ec.dtype
    ) / 12
    for iE in prange(nE):
        A = area_tri(ec[iE])
        Hh = _Hh(ec[iE])
        Bh = _Bh(ec[iE])
        out[iE] += beta * (Hh.T @ (A * (Bh.T @ D[iE] @ Bh) * J) @ Hh)
# fmt: on
