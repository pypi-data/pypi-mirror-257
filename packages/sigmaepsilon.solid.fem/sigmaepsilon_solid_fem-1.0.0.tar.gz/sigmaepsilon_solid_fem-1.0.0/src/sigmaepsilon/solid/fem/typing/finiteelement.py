from typing import ClassVar, TypeVar, Generic, Protocol, Union

from numpy import ndarray
import xarray as xr

from sigmaepsilon.solid.material import MaterialLike, StiffnessLike

from .femdata import FemDataProtocol
from .pointdata import PointDataProtocol
from .material import MaterialProtocol
from .celldata import CellDataProtocol

__all__ = ["FiniteElementProtocol"]

FemDataLike = TypeVar(
    "FemDataLike", bound=FemDataProtocol[PointDataProtocol, "FiniteElementProtocol"]
)
PointDataLike = TypeVar("PointDataLike", bound=PointDataProtocol)


class FiniteElementProtocol(
    CellDataProtocol[FemDataLike, PointDataLike],
    Generic[FemDataLike, PointDataLike],
    Protocol,
):
    Material: ClassVar[MaterialProtocol]
    standalone: ClassVar[bool]

    @property
    def material(self) -> Union[MaterialLike, StiffnessLike, ndarray]:
        ...

    def masses(self) -> ndarray:
        """Ought to return the masses of the cells as an 1d float array."""
        ...

    def mass(self) -> float:
        """Ought to return the mass of the cells as a float."""
        ...

    def internal_forces(self) -> float:
        """Ought to return the mass of the cells as a float."""
        ...

    def utilization(self) -> Union[xr.DataArray, ndarray]:
        """
        Ought to return one utilization value for every load case, cell and point
        of evaluation.
        """
        ...

    def maximum_utilization(self) -> Union[xr.DataArray, ndarray]:
        """Ought to return one utilization value for every load case."""
        ...
