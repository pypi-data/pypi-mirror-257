from typing import Callable, Tuple

import numpy as np
from numpy import ndarray

from sigmaepsilon.mesh.utils.tri import glob_to_nat_tri, loc_to_glob_tri, nat_to_loc_tri
from sigmaepsilon.mesh.utils import cells_coords


def numerical_integration_points(
    base: Callable, mc: ndarray, subtopo: ndarray
) -> Tuple[ndarray]:
    p, w = base()
    nP = len(p)
    nSE = len(subtopo)
    p_super, w_super = [], []
    for iSE in range(nSE):
        imc = mc[subtopo[iSE]]
        for iP in range(nP):
            p_super.append(loc_to_glob_tri(p[iP], imc))
            w_super.append(w[iP])
    return np.array(p_super, dtype=float), np.array(w_super, dtype=float)


def sublocations_of_points(
    x: ndarray,
    mc: ndarray,
    subtopo: ndarray,
    ftol: float = 1e-12,
    regular: bool = False,
) -> Tuple[ndarray, ndarray]:
    nP = len(x)
    nSE = len(subtopo)  # number of subelements
    mec = cells_coords(mc, subtopo)  # (nSE, nSNE, 2)
    subloc = []

    if regular:
        submap = np.repeat(np.arange(nSE), divmod(nP, nSE)[0])
        subloc = []
        for iP in range(nP):
            iSE = submap[iP]
            nat = glob_to_nat_tri(x[iP], mec[iSE])
            subloc.append(nat_to_loc_tri(nat))
    else:
        submap = np.zeros((nP,), dtype=int)
        subloc = []
        for iP in range(nP):
            for iSE in range(nSE):
                nat = glob_to_nat_tri(x[iP], mec[iSE])
                c1 = np.all(nat > (-ftol))
                c2 = np.all(nat < (1 + ftol))
                if c1 and c2:
                    submap[iP] = iSE
                    subloc.append(nat_to_loc_tri(nat))
                    break

    return submap, np.array(subloc).astype(float)


def dofmap_of_subtriangles(subtopo: ndarray, nDOF: int) -> ndarray:
    subdofmap = []
    for tri in subtopo:
        sdm = np.array([list(range((i * nDOF), (i + 1) * nDOF)) for i in tri]).flatten()
        subdofmap.append(sdm)
    subdofmap = np.array(subdofmap).astype(int)
    return subdofmap
