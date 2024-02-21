import numpy as np
from numpy import ndarray
from numba import njit, prange

from sigmaepsilon.mesh.utils.cells.t3 import shp_T3
from sigmaepsilon.mesh.utils.tri import loc_to_nat_tri, loc_to_glob_tri


__cache = True


@njit(nogil=True, cache=__cache)
def strain_coefficient_matrix_all84(ec: ndarray) -> ndarray:
    res = np.zeros((5, 9), dtype=ec.dtype)
    (x1, x2, x3), (y1, y2, y3) = ec[:, 0], ec[:, 1]
    x12, x21, x13, x31, x23, x32 = (
        x1 - x2,
        x2 - x1,
        x1 - x3,
        x3 - x1,
        x2 - x3,
        x3 - x2,
    )
    y12, y21, y13, y31, y23, y32 = (
        y1 - y2,
        y2 - y1,
        y1 - y3,
        y3 - y1,
        y2 - y3,
        y3 - y2,
    )
    A2 = y21 * x13 - x21 * y13

    res[0, 0] = y23
    res[0, 2] = 0.5 * y1 * y23
    res[0, 3] = y31
    res[0, 5] = 0.5 * y2 * y31
    res[0, 6] = y12
    res[0, 8] = 0.5 * y3 * y12

    res[1, 2] = -0.5 * y23
    res[1, 5] = -0.5 * y31
    res[1, 8] = -0.5 * y12

    res[2, 1] = x32
    res[2, 2] = 0.5 * x1 * x23
    res[2, 4] = x13
    res[2, 5] = 0.5 * x2 * x31
    res[2, 7] = x21
    res[2, 8] = 0.5 * x3 * x12

    res[3, 2] = -0.5 * x23
    res[3, 5] = -0.5 * x31
    res[3, 8] = -0.5 * x12

    res[4, 0] = x32
    res[4, 1] = y23
    res[4, 2] = 0.5 * (x1 * y32 + y1 * x32)
    res[4, 3] = x13
    res[4, 4] = y31
    res[4, 5] = 0.5 * (x2 * y13 + y2 * x13)
    res[4, 6] = x21
    res[4, 7] = y12
    res[4, 8] = 0.5 * (x3 * y21 + y3 * x21)

    res /= A2

    return res


@njit(nogil=True, parallel=True, cache=__cache)
def strain_displacement_matrix_bulk_multi_all84(
    points: ndarray, ec: ndarray, out: ndarray, inds: ndarray
) -> ndarray:
    # res (nE, nP, nSTRE, nTOTV)
    nE = ec.shape[0]
    nP = points.shape[0]
    ftype = points.dtype
    nI = len(inds)
    for iE in prange(nE):
        C = strain_coefficient_matrix_all84(ec[iE])
        for iP in prange(nP):
            x, y = loc_to_glob_tri(points[iP], ec[iE])
            B = np.array(
                [
                    [1.0, y, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, x, 0.0],
                    [0.0, -x, 0.0, -y, 1.0],
                ],
                dtype=ftype,
            )
            BC = B @ C
            for iI in prange(nI):
                out[iE, iP, :, inds[iI]] += BC[:, iI]
    return out


@njit(nogil=True, parallel=True, cache=__cache)
def shape_function_matrix_bulk_multi_all84(
    points: ndarray, ec: ndarray, out: ndarray, inds: ndarray
) -> ndarray:
    """
    `points` are expected in the master domain.
    """
    nE = ec.shape[0]
    nP = points.shape[0]
    for iE in prange(nE):
        for iP in prange(nP):
            A1, A2, A3 = loc_to_nat_tri(points[iP])

            (x1, x2, x3), (y1, y2, y3) = ec[iE, :, 0], ec[iE, :, 1]
            x12, x31, x23 = (
                x1 - x2,
                x3 - x1,
                x2 - x3,
            )
            y12, y31, y23 = (
                y1 - y2,
                y3 - y1,
                y2 - y3,
            )

            l12 = np.sqrt(x12**2 + y12**2)
            l23 = np.sqrt(x23**2 + y23**2)
            l31 = np.sqrt(x31**2 + y31**2)
            S12 = x12 / l12
            S23 = x23 / l23
            S31 = x31 / l31
            C12 = -y12 / l12
            C23 = -y23 / l23
            C31 = -y31 / l31

            out[iE, iP, 0, inds[0]] = A1
            out[iE, iP, 0, inds[3]] = A2
            out[iE, iP, 0, inds[6]] = A3
            out[iE, iP, 0, inds[2]] = 0.5 * (l31 * C31 * A1 * A3 - l12 * C12 * A1 * A2)
            out[iE, iP, 0, inds[5]] = 0.5 * (l12 * C12 * A1 * A2 - l23 * C23 * A2 * A3)
            out[iE, iP, 0, inds[8]] = 0.5 * (l23 * C23 * A2 * A3 - l31 * C31 * A1 * A3)

            out[iE, iP, 1, inds[1]] = A1
            out[iE, iP, 1, inds[4]] = A2
            out[iE, iP, 1, inds[7]] = A3
            out[iE, iP, 1, inds[2]] = 0.5 * (l31 * S31 * A1 * A3 - l12 * S12 * A1 * A2)
            out[iE, iP, 1, inds[5]] = 0.5 * (l12 * S12 * A1 * A2 - l23 * S23 * A2 * A3)
            out[iE, iP, 1, inds[8]] = 0.5 * (l23 * S23 * A2 * A3 - l31 * S31 * A1 * A3)

            shp = shp_T3(points[iP])
            out[iE, iP, 2, inds[2]] = shp[0]
            out[iE, iP, 2, inds[5]] = shp[1]
            out[iE, iP, 2, inds[8]] = shp[2]
    return out
