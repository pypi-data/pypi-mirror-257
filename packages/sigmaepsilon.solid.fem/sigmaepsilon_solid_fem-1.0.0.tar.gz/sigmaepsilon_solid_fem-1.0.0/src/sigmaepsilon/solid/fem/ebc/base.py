from typing import Tuple
from abc import abstractmethod

from numpy import ndarray
from scipy.sparse import coo_matrix as coo

from ..data.mesh import FemMesh


__all__ = ["FemEssentialBoundaryCondition"]


class FemEssentialBoundaryCondition:
    """
    Base class for Dirichlet boundary conditions accounted for
    using Courant-type penalization.
    """

    @abstractmethod
    def assemble(self, mesh: FemMesh) -> Tuple[coo, ndarray]:
        """
        The implementation ought to return a penalty matrix
        either in dense or sparse format.
        """
        ...