from numpy import ndarray
import numpy as np
from numba import njit, prange


__cache = True


@njit(nogil=True, cache=__cache)
def dof_transformation_matrix_Q8_Cook(ec: ndarray) -> ndarray:
    res = np.zeros((16, 12), dtype=ec.dtype)

    (x1, x2, x3, x4), (y1, y2, y3, y4) = ec[:4, 0], ec[:4, 1]

    x12, x41, x23, x34 = (
        x1 - x2,
        x4 - x1,
        x2 - x3,
        x3 - x4,
    )
    y12, y41, y23, y34 = (
        y1 - y2,
        y4 - y1,
        y2 - y3,
        y3 - y4,
    )

    l12 = np.sqrt(x12 ** 2 + y12 ** 2)
    l23 = np.sqrt(x23 ** 2 + y23 ** 2)
    l34 = np.sqrt(x34 ** 2 + y34 ** 2)
    l41 = np.sqrt(x41 ** 2 + y41 ** 2)

    S12 = (x1 - x2) / l12
    S23 = (x2 - x3) / l23
    S41 = (x3 - x1) / l41
    S34 = (x3 - x4) / l34
    C12 = (y2 - y1) / l12
    C23 = (y3 - y2) / l23
    C41 = (y1 - y3) / l41
    C34 = (y4 - y3) / l34

    res[0, 0] = 1.0
    res[1, 1] = 1.0
    res[2, 3] = 1.0
    res[3, 4] = 1.0
    res[4, 6] = 1.0
    res[5, 7] = 1.0
    res[6, 9] = 1.0
    res[7, 10] = 1.0

    res[8, 0] = 0.5
    res[8, 3] = 0.5
    res[8, 5] = l12 * C12 / 8
    res[8, 2] = -res[8, 5]

    res[9, 1] = 0.5
    res[9, 4] = 0.5
    res[9, 5] = l12 * S12 / 8
    res[9, 2] = -res[9, 5]

    res[10, 3] = 0.5
    res[10, 6] = 0.5
    res[10, 8] = l23 * C23 / 8
    res[10, 5] = -res[10, 8]

    res[11, 4] = 0.5
    res[11, 7] = 0.5
    res[11, 8] = l23 * S23 / 8
    res[11, 5] = -res[11, 8]

    res[12, 6] = 0.5
    res[12, 9] = 0.5
    res[12, 11] = l34 * C34 / 8
    res[12, 8] = -res[12, 11]

    res[13, 7] = 0.5
    res[13, 10] = 0.5
    res[13, 11] = l34 * S34 / 8
    res[13, 8] = -res[13, 11]

    res[14, 9] = 0.5
    res[14, 0] = 0.5
    res[14, 2] = l41 * C41 / 8
    res[14, 11] = -res[14, 2]

    res[15, 10] = 0.5
    res[15, 1] = 0.5
    res[15, 2] = l41 * S41 / 8
    res[15, 11] = -res[15, 2]

    return res


@njit(nogil=True, parallel=True, cache=__cache)
def tr_strain_displacement_matrices(B: ndarray, ec: ndarray) -> ndarray:
    nE, nG, nSTRE = B.shape[:3]
    res = np.zeros((nE, nG, nSTRE, 12), dtype=B.dtype)
    for iE in prange(nE):
        T = dof_transformation_matrix_Q8_Cook(ec[iE])
        for iG in prange(nG):
            for iS in prange(nSTRE):
                res[iE, iG, iS] = B[iE, iG, iS] @ T
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def tr_shape_function_matrices(N: ndarray, ec: ndarray) -> ndarray:
    nE = ec.shape[0]
    nG, nDOF = N.shape[:2]
    res = np.zeros((nE, nG, 3, 12), dtype=N.dtype)
    for iE in prange(nE):
        T = dof_transformation_matrix_Q8_Cook(ec[iE])
        for iG in prange(nG):
            for iDOF in prange(nDOF):
                res[iE, iG, iDOF] = N[iG, iDOF] @ T
    res[:, :, 2, 2] = 0.25
    res[:, :, 2, 5] = 0.25
    res[:, :, 2, 8] = 0.25
    res[:, :, 2, 11] = 0.25
    return res
