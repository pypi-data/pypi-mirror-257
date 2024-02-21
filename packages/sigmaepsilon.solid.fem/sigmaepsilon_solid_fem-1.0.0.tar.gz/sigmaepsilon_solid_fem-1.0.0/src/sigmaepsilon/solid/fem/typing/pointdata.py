from typing import Protocol

from numpy import ndarray

from sigmaepsilon.mesh.typing import PointDataProtocol as PDP

__all__ = ["PointDataProtocol"]


class PointDataProtocol(PDP, Protocol):
    @property
    def dofsol(self) -> ndarray:
        """Ought to return dof solution."""
        ...

    @property
    def loads(self) -> ndarray:
        """Ought to return nodal loads."""
        ...

    @property
    def forces(self) -> ndarray:
        """Ought to return nodal forces."""
        ...

    @property
    def fixity(self) -> ndarray:
        """Ought to return nodal fixity."""
        ...

    @property
    def mass(self) -> ndarray:
        """Ought to return nodal masses."""
        ...
