from numba import njit, prange
import numpy as np
from numpy import ndarray

__cache = True


@njit(nogil=True, parallel=True, cache=__cache)
def strain_displacement_matrix(shp: ndarray, gdshp: ndarray) -> ndarray:
    """
    Returns the matrix expressing the relationship of generalized strains
    and generalized displacements of a Bernoulli beam element. The order
    of strain components is
        0 : strain along x (exx)
        1 : engineering shear strain xy (exy)
        2 : engineering shear strain xz (exz)
        3 : curvature around x (cxx)
        4 : curvature around y (cyy)
        5 : curvature around z (czz)

    Parameters
    ----------
    shp: numpy.ndarray
        Shape function values for every node (nNE) as a 1d float
        array (nNE,) evaluated at a point of integration.
    gdshp: numpy.ndarray
        First derivatives for every node (nNE) as a 2d float array
        (nNE, 1) evaluated at a point of integration.

    Returns
    -------
    numpy.ndarray
        Approximation coefficients for every generalized strain and every
        shape function as a 2d float array of shape (nSTRE=6, nNE * nDOF=6).
    """
    nNE = gdshp.shape[0]
    B = np.zeros((6, nNE * 6), dtype=gdshp.dtype)
    for i in prange(nNE):
        di = i * 6
        # exx
        B[0, 0 + di] = gdshp[i, 0]
        # exy
        B[1, 1 + di] = gdshp[i, 0]
        B[1, 5 + di] = -shp[i]
        # exz
        B[2, 2 + di] = gdshp[i, 0]
        B[2, 4 + di] = shp[i]
        # cxx
        B[3, 3 + di] = gdshp[i, 0]
        # cyy
        B[4, 4 + di] = gdshp[i, 0]
        # czz
        B[5, 5 + di] = gdshp[i, 0]
    return B


@njit(nogil=True, parallel=True, cache=__cache)
def strain_displacement_matrix_bulk(shp: ndarray, gdshp: ndarray) -> ndarray:
    """
    Calculates the strain-displacement matrix for several elements.

    Parameters
    ----------
    shp: numpy.ndarray
        2d float array of shape (nP, nNE).
    gdshp: numpy.ndarray
        4d float array of shape (nE, nP, nNE, 1).

    Returns
    -------
    numpy.ndarray
        4d float array of shape (nE, nP, nSTRE=6, nNE * nDOF=6).
    """
    nE, nP, nNE = gdshp.shape[:3]
    B = np.zeros((nE, nP, 6, nNE * 6), dtype=gdshp.dtype)
    for iE in prange(nE):
        for iP in prange(nP):
            B[iE, iP] = strain_displacement_matrix(shp[iP], gdshp[iE, iP])
    return B
