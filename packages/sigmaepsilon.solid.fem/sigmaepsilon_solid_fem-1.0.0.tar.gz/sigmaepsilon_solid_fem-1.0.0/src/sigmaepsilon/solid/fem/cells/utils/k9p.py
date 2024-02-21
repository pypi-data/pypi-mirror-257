import numpy as np
from numpy import ndarray
from numba import njit, prange

__cache = True

# fmt: off
@njit(nogil=True, cache=__cache)
def monoms(X: ndarray) -> ndarray:
    x, y = X
    return np.array([
        1, x, y, x**2, x*y, y**2, x**3, x**2*y, x*y**2, y**3, x**4, x**3*y, 
        x**2*y**2, x*y**3, y**4, x**5, x**4*y, x**3*y**2, x**2*y**3, x*y**4, 
        y**5, x**5*y, x**4*y**2, x**2*y**4, x*y**5, x**5*y**2, x**2*y**5
        ], dtype=X.dtype
    )


@njit(nogil=True, cache=__cache)
def monoms_diff_1(X: ndarray) -> ndarray:
    x, y = X
    return np.array([
        [
            0, 1, 0, 2*x, y, 0, 3*x**2, 2*x*y, y**2, 0, 4*x**3, 3*x**2*y, 
            2*x*y**2, y**3, 0, 5*x**4, 4*x**3*y, 3*x**2*y**2, 2*x*y**3, y**4, 
            0, 5*x**4*y, 4*x**3*y**2, 2*x*y**4, y**5, 5*x**4*y**2, 2*x*y**5
        ],
        [
            0, 0, 1, 0, x, 2*y, 0, x**2, 2*x*y, 3*y**2, 0, x**3, 2*x**2*y, 3*x*y**2, 
            4*y**3, 0, x**4, 2*x**3*y, 3*x**2*y**2, 4*x*y**3, 5*y**4, x**5, 2*x**4*y, 
            4*x**2*y**3, 5*x*y**4, 2*x**5*y, 5*x**2*y**4
        ]
        ], dtype=X.dtype
    )
    

@njit(nogil=True, cache=__cache)
def monoms_diff_2(X: ndarray) -> ndarray:
    x, y = X
    return np.array([
        [
            0, 0, 0, 2, 0, 0, 6*x, 2*y, 0, 0, 12*x**2, 6*x*y, 2*y**2, 0, 0, 20*x**3, 
            12*x**2*y, 6*x*y**2, 2*y**3, 0, 0, 20*x**3*y, 12*x**2*y**2, 2*y**4, 0, 
            20*x**3*y**2, 2*y**5
        ],
        [
            0, 0, 0, 0, 0, 2, 0, 0, 2*x, 6*y, 0, 0, 2*x**2, 6*x*y, 12*y**2, 0, 0, 
            2*x**3, 6*x**2*y, 12*x*y**2, 20*y**3, 0, 2*x**4, 12*x**2*y**2, 20*x*y**3, 
            2*x**5, 20*x**2*y**3
        ],
        [
            0, 0, 0, 0, 1, 0, 0, 2*x, 2*y, 0, 0, 3*x**2, 4*x*y, 3*y**2, 0, 0, 4*x**3, 
            6*x**2*y, 6*x*y**2, 4*y**3, 0, 5*x**4, 8*x**3*y, 8*x*y**3, 5*y**4, 10*x**4*y, 
            10*x*y**4    
        ]
        ], dtype=X.dtype
    )
    

@njit(nogil=True, cache=__cache)
def monoms_diff_3(X: ndarray) -> ndarray:
    x, y = X
    return np.array([
        [
            0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 24*x, 6*y, 0, 0, 0, 60*x**2, 24*x*y, 6*y**2, 
            0, 0, 0, 60*x**2*y, 24*x*y**2, 0, 0, 60*x**2*y**2, 0
        ],
        [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6*x, 24*y, 0, 0, 0, 6*x**2, 24*x*y, 
            60*y**2, 0, 0, 24*x**2*y, 60*x*y**2, 0, 60*x**2*y**2
        ],
        [
            0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 4*x, 6*y, 0, 0, 0, 6*x**2, 12*x*y, 
            12*y**2, 0, 0, 8*x**3, 24*x*y**2, 20*y**3, 10*x**4, 40*x*y**3  
        ],
        [
            0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 6*x, 4*y, 0, 0, 0, 12*x**2, 12*x*y, 
            6*y**2, 0, 0, 20*x**3, 24*x**2*y, 8*y**3, 0, 40*x**3*y, 10*y**4
        ]
        ], dtype=X.dtype
    )
# fmt: on


@njit(nogil=True, cache=__cache)
def monoms_disp(X: ndarray) -> ndarray:
    res = np.zeros((3, 27), dtype=X.dtype)
    md1 = monoms_diff_1(X)
    res[0, :] = monoms(X)
    res[1, :] = md1[1, :]
    res[2, :] = -md1[0, :]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def shape_function_coefficients(ec: ndarray) -> ndarray:
    nNE, nDOF = ec.shape[0], 3
    N = nNE * nDOF
    coeff_matrix = np.zeros((N, N), dtype=ec.dtype)
    for iNE in prange(nNE):
        r0 = iNE * nDOF
        r1 = (iNE + 1) * nDOF
        coeff_matrix[r0:r1, :] = monoms_disp(ec[iNE])
    return np.linalg.inv(coeff_matrix)


@njit(nogil=True, parallel=True, cache=__cache)
def strain_displacement_matrix(x: ndarray, shp_coeffs: ndarray) -> ndarray:
    nNE, nDOF, nSTRE = 9, 3, 3
    res = np.zeros((nSTRE, nNE * nDOF), dtype=x.dtype)
    gdshp2 = monoms_diff_2(x) @ shp_coeffs
    res[0, :] = -gdshp2[0, :]
    res[1, :] = -gdshp2[1, :]
    res[2, :] = -2 * gdshp2[2, :]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def strain_displacement_matrix_bulk_multi_k9p(x: ndarray, ec: ndarray) -> ndarray:
    nE, nP = x.shape[:2]
    nSTRE, nTOTV = (3, 27)
    res = np.zeros((nE, nP, nSTRE, nTOTV), dtype=x.dtype)
    for iE in prange(nE):
        shp_coeffs = shape_function_coefficients(ec[iE])
        for iP in prange(nP):
            res[iE, iP] = strain_displacement_matrix(x[iE, iP], shp_coeffs)
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def shape_function_matrix_bulk_multi_k9p(x: ndarray, ec: ndarray) -> ndarray:
    nE, nP = x.shape[:2]
    res = np.zeros((nE, nP, 3, 27), dtype=x.dtype)
    for iE in prange(nE):
        shp_coeffs = shape_function_coefficients(ec[iE])
        for iP in prange(nP):
            res[iE, iP] = monoms_disp(x[iE, iP]) @ shp_coeffs
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def calculate_shear_forces_k9p(
    loads: ndarray, dofsol: ndarray, D: ndarray, x: ndarray, ec: ndarray, out: ndarray
) -> None:
    nE, nRHS, nP = out.shape[:3]
    for iE in prange(nE):
        D11, D12, D16 = D[iE, 0, :]
        D22 = D[iE, 1, 1]
        D26 = D[iE, 1, 2]
        D66 = D[iE, 2, 2]
        shp_coeffs = shape_function_coefficients(ec[iE])
        for iP in prange(nP):
            gdshp3 = monoms_diff_3(x[iE, iP]) @ shp_coeffs
            for iRHS in prange(nRHS):
                pxx = loads[iE, iRHS, iP, 1]
                pyy = loads[iE, iRHS, iP, 2]
                dxxx = gdshp3[0, :] @ dofsol[iE, iRHS]
                dyyy = gdshp3[1, :] @ dofsol[iE, iRHS]
                dxyy = gdshp3[2, :] @ dofsol[iE, iRHS]
                dyxx = gdshp3[3, :] @ dofsol[iE, iRHS]
                out[iE, iRHS, iP, 3] = (
                    -(D11 * dxxx + (D12 + 2 * D66) * dxyy + 3 * D16 * dyxx + D26 * dyyy)
                    + pyy
                )
                out[iE, iRHS, iP, 4] = (
                    -(D16 * dxxx + (D12 + 2 * D66) * dyxx + 3 * D26 * dxyy + D22 * dyyy)
                    - pxx
                )


@njit(nogil=True, parallel=True, cache=__cache)
def approximate_internal_forces_UM(
    loads: ndarray,
    forces: ndarray,
    shp: ndarray,
    dshp: ndarray,
    jac: ndarray,
) -> ndarray:
    nE, nRHS = forces.shape[:2]
    nP, nN = dshp.shape[:2]
    res = np.zeros((nE, nRHS, nP, 5), dtype=forces.dtype)
    for iE in prange(nE):
        for iP in prange(nP):
            gdshp = dshp[iP] @ np.linalg.inv(jac[iE, iP])
            for iRHS in prange(nRHS):
                for iN in range(nN):
                    # moments
                    res[iE, iRHS, iP, 0] += forces[iE, iRHS, iN, 0] * shp[iP, iN]
                    res[iE, iRHS, iP, 1] += forces[iE, iRHS, iN, 1] * shp[iP, iN]
                    res[iE, iRHS, iP, 2] += forces[iE, iRHS, iN, 2] * shp[iP, iN]
                    # vx
                    res[iE, iRHS, iP, 3] += (
                        forces[iE, iRHS, iN, 0] * gdshp[iN, 0]
                        + forces[iE, iRHS, iN, 2] * gdshp[iN, 1]
                        + loads[iE, iRHS, iN, 1] * shp[iP, iN]
                    )
                    # vy
                    res[iE, iRHS, iP, 4] += (
                        forces[iE, iRHS, iN, 1] * gdshp[iN, 1]
                        + forces[iE, iRHS, iN, 2] * gdshp[iN, 0]
                        - loads[iE, iRHS, iN, 2] * shp[iP, iN]
                    )
    return res
