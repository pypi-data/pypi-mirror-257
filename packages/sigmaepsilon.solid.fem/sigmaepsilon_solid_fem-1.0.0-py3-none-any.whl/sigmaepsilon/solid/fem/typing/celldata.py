from typing import TypeVar, Generic, Protocol

from numpy import ndarray

from sigmaepsilon.mesh.typing import PolyCellProtocol

from .femdata import FemDataProtocol
from .pointdata import PointDataProtocol

__all__ = ["CellDataProtocol"]

FemDataLike = TypeVar(
    "FemDataLike", bound=FemDataProtocol[PointDataProtocol, "CellDataProtocol"]
)
PointDataLike = TypeVar("PointDataLike", bound=PointDataProtocol)


class CellDataProtocol(
    PolyCellProtocol[FemDataLike, PointDataLike],
    Generic[FemDataLike, PointDataLike],
    Protocol,
):
    @property
    def has_mass_matrix(self) -> bool:
        ...
        
    @property
    def has_fixity(self) -> bool:
        ...
    
    @property
    def material_stiffness(self) -> ndarray:
        """Ought to return material stiffness matrices the cells."""
        ...

    @property
    def density(self) -> ndarray:
        """Returns densities of the cells as an 1d array."""
        ...

    @property
    def nodal_loads(self) -> ndarray:
        """Returns the nodal loads of the cells."""
        ...

    @property
    def elastic_stiffness_matrix(self) -> ndarray:
        """Returns the elastic stiffness matrices of the cells."""
        ...

    @elastic_stiffness_matrix.setter
    def elastic_stiffness_matrix(self, value: ndarray) -> None:
        """Sets the elastic stiffness matrices of the cells."""
        ...
        
    @property
    def mass_matrix(self) -> ndarray:
        """Returns the mass matrices of the cells."""
        ...
        
    @mass_matrix.setter
    def mass_matrix(self, value: ndarray) -> None:
        """Sets the mass matrices of the cells."""
        ...
        
    @property
    def fixity(self) -> ndarray:
        """Returns the fixity of the cells."""
        ...

    @fixity.setter
    def fixity(self, value: ndarray) -> None:
        """
        Sets the fixity of the cells.
        """
        ...
