from numba import njit, prange
import numpy as np
from numpy import ndarray

__cache = True


@njit(nogil=True, parallel=True, cache=__cache)
def strain_displacement_matrix_bulk2(B: ndarray, djac: ndarray, w: ndarray):
    nE, nG, nSTRE, nTOTV = B.shape
    res = np.zeros((nE, nSTRE, nTOTV), dtype=B.dtype)
    for iG in range(nG):
        for iE in prange(nE):
            res[iE] += B[iE, iG] * djac[iE, iG] * w[iG]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def unit_strain_load_vector_bulk(D: ndarray, B: ndarray):
    nE, nSTRE, nTOTV = B.shape
    res = np.zeros((nE, nTOTV, nSTRE), dtype=D.dtype)
    for iE in prange(nE):
        res[iE] = B[iE].T @ D[iE]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def strain_load_vector_bulk(BTD: ndarray, strains: ndarray):
    nE, nTOTV, nSTRE = BTD.shape
    nE, nRHS, nSTRE = strains.shape
    res = np.zeros((nE, nTOTV, nRHS), dtype=BTD.dtype)
    for iE in prange(nE):
        for iRHS in prange(nRHS):
            res[iE, :, iRHS] = BTD[iE] @ strains[iE, iRHS, :]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def stiffness_matrix_bulk2(D: ndarray, B: ndarray, djac: ndarray, w: ndarray):
    nE, nG = djac.shape
    nTOTV = B.shape[-1]
    res = np.zeros((nE, nTOTV, nTOTV), dtype=D.dtype)
    for iG in range(nG):
        for iE in prange(nE):
            res[iE] += B[iE, iG].T @ D[iE] @ B[iE, iG] * djac[iE, iG] * w[iG]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def stiffness_matrix_bulk2_i(
    D: ndarray, B: ndarray, djac: ndarray, w: ndarray, inds: ndarray, out: ndarray
) -> ndarray:
    nE, nG = djac.shape
    nX = inds.shape[0]
    for iG in range(nG):
        for iE in prange(nE):
            K_iE = B[iE, iG].T @ D[iE] @ B[iE, iG] * djac[iE, iG] * w[iG]
            for i in prange(nX):
                for j in prange(nX):
                    out[iE, inds[i], inds[j]] += K_iE[i, j]
    return out


@njit(nogil=True, parallel=True, cache=__cache)
def mass_matrix_bulk(
    N: ndarray, dens: ndarray, weights: ndarray, djac: ndarray, w: ndarray
):
    """
    Evaluates the mass matrix of several elements from evaluations at the
    Gauss points of the elements. The densities are assumed to be constant
    over the elements, and be represented by the 1d float numpy array 'dens'.

    Parameters
    ----------
    N: 4d numpy float array
        Evaluations of the shape function matrix according to the type of
        the element for every cell and Gauss point.
    dens: 1d numpy float array
        1d float array of densities of several elements.
    weights: 1d numpy float array
        Array of weighting factors for the cells (eg. areas, volumes) with
        the same shape as 'dens'.
    w: 1d numpy float array
        Weights of the Gauss points
    djac: 2d numpy float array
        Jacobi determinants for every element and Gauss point.

    nE: number of elements
    nG: number of Gauss points
    nNE: number of nodes per element
    nDOF: number of dofs per node
    """
    nE, nG = djac.shape
    nTOTV = N.shape[-1]
    res = np.zeros((nE, nTOTV, nTOTV), dtype=N.dtype)
    for iG in range(nG):
        for iE in prange(nE):
            res[iE] += (
                dens[iE] * weights[iE] * N[iE, iG].T @ N[iE, iG] * djac[iE, iG] * w[iG]
            )
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def compliance_bulk(K_bulk: ndarray, dofsol1d: ndarray, gnum: ndarray) -> ndarray:
    """
    Returns the total compliance of the structure, that is
        u.T @ K @ u
    """
    nE, nTOTV, _ = K_bulk.shape
    res = np.zeros(nE, dtype=K_bulk.dtype)
    for iE in prange(nE):
        for i in prange(nTOTV):
            for j in prange(nTOTV):
                res[iE] += (
                    K_bulk[iE, i, j] * dofsol1d[gnum[iE, i]] * dofsol1d[gnum[iE, j]]
                )
    return res


@njit(nogil=True, cache=__cache)
def elastic_strain_energy_bulk(
    K_bulk: ndarray, dofsol1d: ndarray, gnum: ndarray
) -> ndarray:
    """
    Returns the total elastic strain energy of the structure, that is
        0.5 * u.T @ K @ u
    """
    return compliance_bulk(K_bulk, dofsol1d, gnum) / 2


@njit(nogil=True, parallel=True, cache=__cache)
def approx_dof_solution(dofsol1d: ndarray, gnum: ndarray, shpmat: ndarray) -> ndarray:
    nDOFN, nTOTV = shpmat.shape
    res = np.zeros((nDOFN), dtype=dofsol1d.dtype)
    for j in prange(nDOFN):
        for k in prange(nTOTV):
            res[j] += shpmat[j, k] * dofsol1d[gnum[k]]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def approx_dof_solution_bulk(
    dofsol1d: ndarray, gnum: ndarray, shpmat: ndarray
) -> ndarray:
    nE = len(gnum)
    nDOFN, nTOTV = shpmat.shape
    res = np.zeros((nE, nDOFN), dtype=dofsol1d.dtype)
    for i in prange(nE):
        for j in prange(nDOFN):
            for k in prange(nTOTV):
                res[i, j] += shpmat[j, k] * dofsol1d[gnum[i, k]]
    return res


@njit(nogil=True, cache=__cache)
def element_dof_solution(dofsol1d: ndarray, gnum: ndarray) -> ndarray:
    return dofsol1d[gnum]


@njit(nogil=True, parallel=True, cache=__cache)
def element_dof_solution_bulk(dofsol1d: ndarray, gnum: ndarray) -> ndarray:
    nE, nEVAB = gnum.shape
    res = np.zeros((nE, nEVAB), dtype=dofsol1d.dtype)
    for i in prange(nE):
        res[i, :] = dofsol1d[gnum[i, :]]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def element_dof_solution_bulk_multi(dofsol: ndarray, gnum: ndarray) -> ndarray:
    nRHS = dofsol.shape[-1]
    nE, nEVAB = gnum.shape
    res = np.zeros((nRHS, nE, nEVAB), dtype=dofsol.dtype)
    for i in prange(nE):
        for j in prange(nRHS):
            res[j, i, :] = dofsol[gnum[i, :], j]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def avg_nodal_data_bulk(data: ndarray, topo: ndarray) -> ndarray:
    nE, nNE, nD = data.shape
    nP = np.max(topo) + 1
    res = np.zeros((nP, nD), dtype=data.dtype)
    count = np.zeros((nP), dtype=topo.dtype)
    for iE in prange(nE):
        for jNE in prange(nNE):
            res[topo[iE, jNE]] += data[iE, jNE]
            count[topo[iE, jNE]] += 1
    for iP in prange(nP):
        res[iP] = res[iP] / count[iP]
    return res


@njit(nogil=True, parallel=True, fastmath=True, cache=__cache)
def body_load_vector_bulk_cm(
    values: ndarray, N: ndarray, djac: ndarray, w: ndarray
) -> ndarray:
    """
    Integrates the body loads for constant metric elements to give an equivalent
    nodal load vector.

    This implementation is general in the context of Lagrange elements.

    Input values are assumed to be evaluated at multiple (nG) Gauss points of
    multiple (nE) cells.

    Parameters
    ----------
    values: numpy.ndarray
        A 3d float array of body loads of shape (nE, nRHS, nNE * nDOF)
        for several elements and load cases.
    N: numpy.ndarray
        A float array of shape (nG, nDOF, nDOF * nNODE), being the shape
        function matrix evaluated at a nG number of Gauss points for the
        master cell of the block.
    djac: numpy.ndarray
        A float array of shape (nE, nG), being jacobian determinants
        evaluated at the Gauss points of several cells.
    w: numpy.ndarray
        1d float array of weights for an nG number of Gauss points,
        with a shape of (nG,).

    Returns
    -------
    numpy.ndarray
        3d float array of shape (nE, nNE * nDOF, nRHS).
    """
    nE, nRHS, nEVAB = values.shape
    nG = N.shape[0]
    res = np.zeros((nE, nEVAB, nRHS), dtype=values.dtype)
    for iG in range(nG):
        NTN = N[iG].T @ N[iG]
        for iRHS in prange(nRHS):
            for iE in prange(nE):
                res[iE, :, iRHS] += NTN @ values[iE, iRHS, :] * djac[iE, iG] * w[iG]
    return res


@njit(nogil=True, parallel=True, fastmath=True, cache=__cache)
def body_load_vector_bulk_vm(
    values: ndarray, N: ndarray, djac: ndarray, w: ndarray
) -> ndarray:
    """
    Integrates the body loads for variable metric elements to give an equivalent
    nodal load vector.

    Input values are assumed to be evaluated at multiple (nG) Gauss points of
    multiple (nE) cells.

    Parameters
    ----------
    values: numpy.ndarray
        A 3d float array of body loads of shape (nE, nRHS, nNE * nDOF)
        for several elements and load cases.
    N: numpy.ndarray
        A float array of shape (nE, nG, nDOF, nDOF * nNODE), being the shape
        function matrix evaluated at a nG number of Gauss points of several
        cells.
    djac: numpy.ndarray
        A float array of shape (nE, nG), being jacobian determinants
        evaluated at the Gauss points of several cells.
    w: numpy.ndarray
        1d float array of weights for an nG number of Gauss points,
        with a shape of (nG,).

    Returns
    -------
    numpy.ndarray
        3d float array of shape (nE, nNE * nDOF, nRHS).
    """
    nE, nRHS, nEVAB = values.shape
    nG = N.shape[1]
    res = np.zeros((nE, nEVAB, nRHS), dtype=values.dtype)
    for iE in prange(nE):
        for iG in range(nG):
            NTN = N[iE, iG].T @ N[iE, iG]
            for iRHS in range(nRHS):
                res[iE, :, iRHS] += NTN @ values[iE, iRHS, :] * djac[iE, iG] * w[iG]
    return res
