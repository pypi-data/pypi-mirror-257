from typing import Generic, TypeVar, ClassVar, Iterable, Protocol, Union

from sigmaepsilon.mesh.typing import PolyDataProtocol


__all__ = ["FemDataProtocol"]


PD = TypeVar("PD")
CD = TypeVar("CD")


class FemDataProtocol(PolyDataProtocol[PD, CD], Generic[PD, CD], Protocol):
    """Protocol for finite element meshes"""

    displacement_variables: ClassVar[Iterable[str]]
    number_of_displacement_variables: ClassVar[Union[int, None]] = None
    
    @property
    def number_of_load_cases(self) -> int:
        """Ought to return the number of load cases"""
        ...
