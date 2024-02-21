from typing import Union, TypeVar

import numpy as np
from numpy import ndarray

from sigmaepsilon.math.linalg import ReferenceFrame

from .surfaceelement import SurfaceFiniteElement
from ..typing import (
    FemDataProtocol,
    PointDataProtocol,
)

__all__ = ["PlateFiniteElement"]


FD = TypeVar("FD", bound=FemDataProtocol)
PD = TypeVar("PD", bound=PointDataProtocol)


class PlateFiniteElement(SurfaceFiniteElement[FD, PD]):
    standalone = True

    def direction_cosine_matrix(
        self,
        *_,
        source: Union[ndarray, str, ReferenceFrame] = None,
        target: Union[ndarray, str, ReferenceFrame] = None,
        N: int = None,
        **__,
    ) -> ndarray:
        """
        Returns the DCM matrix for all elements in the block.

        Parameters
        ----------
        source: Union[ndarray, str, ReferenceFrame], Optional
            A source frame. The string 'global' refers to the global
            frame of the mesh. Default is None.
        target: Union[ndarray, str, ReferenceFrame], Optional
            A target frame. The string 'global' refers to the global
            frame of the mesh. Default is None.
        N: int, Optional
            Number of points. If not specified, the number of nodes is inferred from
            the class of the instance the function is called upon. Default is None.

        Returns
        -------
        numpy.ndarray
            The dcm matrix for linear transformations from source to target.
        """
        dcm = super().direction_cosine_matrix(
            source=source, target=target, N=N, _ndof=6
        )
        nNE = self.Geometry.number_of_nodes if N is None else N
        inds = np.array(
            [[i * 3 + 2, i * 3 + 3, i * 3 + 4] for i in range(nNE)]
        ).flatten()
        return np.ascontiguousarray(dcm[:, inds, :][:, :, inds])
