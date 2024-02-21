from typing import Union, TypeVar, Generic, Optional

import numpy as np
from numpy import ndarray

from sigmaepsilon.math.linalg import ReferenceFrame

from .surfaceelement import SurfaceFiniteElement
from ..typing import (
    FemDataProtocol,
    PointDataProtocol,
)
from ..utils import calculate_fictitious_membrane_stiffness_bulk

__all__ = [
    "MembraneFiniteElement",
    "DrillingMembraneFiniteElement",
    "FictiveDrillingMembraneFiniteElement",
]


FD = TypeVar("FD", bound=FemDataProtocol)
PD = TypeVar("PD", bound=PointDataProtocol)


class MembraneFiniteElement(Generic[FD, PD], SurfaceFiniteElement[FD, PD]):
    standalone = True

    def direction_cosine_matrix(
        self,
        *_,
        source: Optional[Union[ndarray, str, ReferenceFrame, None]] = None,
        target: Optional[Union[ndarray, str, ReferenceFrame, None]] = None,
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
            source=source, target=target, N=N, _ndof=3
        )
        nNE = self.Geometry.number_of_nodes if N is None else N
        inds = np.array([[i * 3, i * 3 + 1] for i in range(nNE)]).flatten()
        return np.ascontiguousarray(dcm[:, inds, :][:, :, inds])


class DrillingMembraneFiniteElement(SurfaceFiniteElement[FD, PD]):
    standalone = True

    def direction_cosine_matrix(
        self,
        *_,
        source: Optional[Union[ndarray, str, ReferenceFrame, None]] = None,
        target: Optional[Union[ndarray, str, ReferenceFrame, None]] = None,
        N: Optional[Union[int, None]] = None,
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
        inds = np.array([[i * 6, i * 6 + 1, i * 6 + 5] for i in range(nNE)]).flatten()
        return np.ascontiguousarray(dcm[:, inds, :][:, :, inds])


class FictiveDrillingMembraneFiniteElement(DrillingMembraneFiniteElement):
    """
    Base class for membrane finite elements with fictitious drilling stiffness.
    The value of the fictitious stiffness is governed by the class attribute `alpha`
    and calculated as the product of `alpha` and the average of the diagonal stiffness
    values. The default value for the parameter `alpha` is `1e-8`.

    The fictitious stiffnesses hardly influence the analysis results, but are mandatory
    in some modelling problems where flat surfaces meet at flat angles.
    """

    alpha = 1e-8

    def __elastic_stiffness_matrix__(self, *args) -> ndarray:
        K = super().__elastic_stiffness_matrix__(*args)
        nNE = self.Geometry.number_of_nodes
        nDOF = self.Material.number_of_displacement_variables
        alpha = self.__class__.alpha
        calculate_fictitious_membrane_stiffness_bulk(K, nNE, nDOF, alpha)
        return K
