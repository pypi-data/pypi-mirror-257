from typing import Tuple
from abc import abstractmethod
from numpy import ndarray
from scipy.sparse import coo_matrix as coo

from ..data.mesh import FemMesh


class FemNaturalBoundaryCondition:
    """
    Base class for Neumann boundary conditions.
    """

    @abstractmethod
    def assemble(self, mesh: FemMesh) -> Tuple[coo, ndarray]:
        """
        The implementation ought to return a load vector as a 1d NumPy array.
        """
        ...
