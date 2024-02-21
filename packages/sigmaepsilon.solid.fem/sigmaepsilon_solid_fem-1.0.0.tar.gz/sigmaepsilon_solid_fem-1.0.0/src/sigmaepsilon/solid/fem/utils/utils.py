from typing import Callable

from numpy import ndarray
import numpy as np

from sigmaepsilon.math import atleastnd

from ..typing import (
    FiniteElementProtocol as FEP,
    FemDataProtocol as FDP,
    PointDataProtocol as PDP,
)
from .fem import (
    element_dofmap_bulk,
    expand_shape_function_matrix_bulk,
)


def flatten_pd(default=True):
    def decorator(fnc: Callable):
        def inner(*args, flatten: bool = default, **kwargs):
            if flatten:
                x = fnc(*args, **kwargs)
                if len(x.shape) == 2:
                    return x.flatten()
                else:
                    nN, nDOFN, nRHS = x.shape
                    return x.reshape((nN * nDOFN, nRHS))
            else:
                return fnc(*args, **kwargs)

        inner.__doc__ = fnc.__doc__
        return inner

    return decorator


def expand_shape_function_matrix(data: FEP[FDP, PDP], N: ndarray) -> ndarray:
    constant_metric = len(N.shape) == 3
    N = atleastnd(N, 4, front=True)
    nNODE = data.Geometry.number_of_nodes
    nDOFN_mesh = data.container.number_of_displacement_variables
    dofmap = data.Material.dofmap
    if len(dofmap) < nDOFN_mesh:
        # the model has more dofs than the element
        nE, nP, nX = N.shape[:3]
        nTOTV = nDOFN_mesh * nNODE
        # nE, nP, nX, nDOF * nNE
        N_ = np.zeros((nE, nP, nX, nTOTV), dtype=float)
        dofmap = element_dofmap_bulk(dofmap, nDOFN_mesh, nNODE)
        N = expand_shape_function_matrix_bulk(N, N_, dofmap)
    return N[0] if constant_metric else N
