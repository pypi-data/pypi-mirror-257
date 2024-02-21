from typing import Optional, Union, Tuple

import numpy as np
from numpy import ndarray
from numba import njit, prange


from .preproc import (
    assert_min_diagonals_bulk,
    _pull_submatrix,
    _pull_subvector,
    _push_submatrix,
    _push_subvector,
)

__cache = True


__all__=["condensate_bulk"]


@njit(nogil=True, parallel=True, cache=__cache)
def _condensate_Kf_bulk(
    K: ndarray, f: ndarray, fixity: ndarray
) -> Tuple[ndarray, ndarray]:
    """
    Returns the condensed coefficient matrices representing constraints
    on the internal forces of the elements (eg. hinges).

    Currently this solution is only able to handle two states, being totally free
    and being fully constrained. The fixity values are expected to be numbers between
    0 and 1, where dofs with a factor > 0.5 are assumed to be the constrained ones.

    Parameters
    ----------
    K: numpy.ndarray
        3d float array, the stiffness matrices of several elements of the same kind.
    factors: numpy.ndarray
        2d boolean array of connectivity factors for each dof of several elements.

    Returns
    -------
    numpy.ndarray
        The condensed stiffness matrices with the same shape as `K`.
    numpy.ndarray
        The condensed load vectors with the same shape as `f`.
    """
    nE = K.shape[0]
    K_out = np.zeros_like(K)
    f_out = np.zeros_like(f)
    for iE in prange(nE):
        b = np.where(fixity[iE])[0]
        i = np.where(~fixity[iE])[0]
        # stiffness matrix
        Kbb = _pull_submatrix(K[iE], b, b)
        Kbi = _pull_submatrix(K[iE], b, i)
        Kib = _pull_submatrix(K[iE], i, b)
        Kii = _pull_submatrix(K[iE], i, i)
        Kii_inv = np.linalg.inv(Kii)
        Kbb -= Kbi @ Kii_inv @ Kib
        _push_submatrix(K_out[iE], Kbb, b, b)
        # load vector
        fb = _pull_subvector(f[iE], b)
        fi = _pull_subvector(f[iE], i)
        fb -= Kbi @ Kii_inv @ fi
        _push_subvector(f_out[iE], fb, b)
    return K_out, f_out


@njit(nogil=True, parallel=True, cache=__cache)
def _condensate_M_bulk(M: ndarray, fixity: ndarray) -> ndarray:
    """
    Returns the condensed coefficient matrices representing constraints
    on the internal forces of the elements (eg. hinges).

    Parameters
    ----------
    M : numpy.ndarray
        3d float array, the mass matrices of several elements of the same kind.
    fixity: numpy.ndarray
        2d float boolean of connectivity factors for each dof of several elements.

    Returns
    -------
    numpy.ndarray
        The condensed mass matrices with the same shape as `M`.
    """
    nE = M.shape[0]
    M_out = np.zeros_like(M)
    for iE in prange(nE):
        b = np.where(fixity[iE])[0]
        i = np.where(~fixity[iE])[0]
        Mbb = _pull_submatrix(M[iE], b, b)
        Mbi = _pull_submatrix(M[iE], b, i)
        Mib = _pull_submatrix(M[iE], i, b)
        Mii = _pull_submatrix(M[iE], i, i)
        Mbb -= Mbi @ np.linalg.inv(Mii) @ Mib
        _push_submatrix(M_out[iE], Mbb, b, b)
    return M_out


def condensate_bulk(
    fixity: ndarray,
    K: ndarray,
    f: ndarray,
    M: Optional[Union[ndarray, None]] = None,
    assertmin: bool = True,
) -> Tuple[ndarray, ndarray, Union[ndarray, None]]:
    """
    Applies static condensation to account for cell fixity.

    References
    ----------
    .. [1] Duan Jin, Li-Yun-gui "About the Finite Element
        Analysis for Beam-Hinged Frame," Advances in Engineering
        Research, vol. 143, pp. 231-235, 2017.
    """    
    nE, nNE, nDOF = fixity.shape
    fixity = fixity.reshape(nE, nNE * nDOF)

    nEVAB_full = nNE * nDOF - 0.001
    cond = np.sum(fixity, axis=1) < nEVAB_full
    i = np.where(cond)[0]
    K[i], f[i] = _condensate_Kf_bulk(K[i], f[i], fixity[i])
    
    if assertmin:
        assert_min_diagonals_bulk(K, 1e-12)
    
    if M is not None:
        M[i] = _condensate_M_bulk(M[i], fixity[i])
        
        if assertmin:
            assert_min_diagonals_bulk(M, 1e-12)
    
    return K, f, M
