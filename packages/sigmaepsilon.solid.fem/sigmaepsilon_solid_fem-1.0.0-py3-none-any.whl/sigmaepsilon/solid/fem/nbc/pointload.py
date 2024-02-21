from typing import Iterable, Optional, Union
from collections import defaultdict

import numpy as np
from numpy import ndarray

from sigmaepsilon.math.linalg import Vector, ReferenceFrame
from sigmaepsilon.math import atleast2d
from sigmaepsilon.mesh.utils.space import index_of_closest_point

from .base import FemNaturalBoundaryCondition
from ..dofmap import DOF
from ..data.mesh import FemMesh


__all__ = ["PointLoad"]


class PointLoad(FemNaturalBoundaryCondition):
    """
    A point load at a node. The object calculates the equivalent
    nodal representation.
    
    Parameters
    ----------
    values: dict
        Dictionary to define the prescribed values.
        Valid keys are 'FX', 'FY', 'FZ', 'MX', 'MY', 'MZ'.
    x: Iterable, Optional
        An iterable expressing the point of application.
        Use it if you don't know the index of the point of application
        in advance. Default is None.
    i: Iterable[int] or int, Optional
        The index of the point of application.
        Default is -1.
    frame: numpy.ndarray or ReferenceFrame, Optional
        The Reference frame in which the provided components are understood.
        If not specified, the default is the global frame.
    """

    def __init__(
        self,
        values: dict,
        x: Optional[Union[Iterable, None]] = None,
        i: Optional[int] = -1,
        frame: Optional[Union[ReferenceFrame, None]] = None,
    ):
        self._values = values
        self._x = x
        self._i = i
        self._frame = frame
        
        if isinstance(frame, ndarray):
            self._frame = ReferenceFrame(frame)

    def _has_point_defined(self) -> bool:
        return self._x is not None

    def _has_index_defined(self) -> bool:
        return self._i > -1

    @property
    def frame(self) -> ReferenceFrame:
        """
        Returns the frame in which the components of the load vector
        is understood.
        """
        if self._frame is not None:
            return self._frame
        return ReferenceFrame(dim=3)

    def values(self, target: Optional[Union[ReferenceFrame, None]] = None) -> dict:
        """
        Returns the provided values of the load.
        """
        frame = self.frame
        values = defaultdict(lambda: 0.0)
        values.update(self._values)
        v3 = Vector([values[k] for k in ["FX", "FY", "FZ"]], frame=frame)
        af = v3.show(target=target).tolist()
        v3 = Vector([values[k] for k in ["MX", "MY", "MZ"]], frame=frame)
        am = v3.show(target=target).tolist()
        return np.array(af + am)

    def x(self, mesh: Optional[Union[FemMesh, None]] = None) -> ndarray:
        """
        Returns the point of application as a NumPy array.
        """
        if self._x is not None:
            return self._x
        elif mesh is not None:
            coords = mesh.coords()
            x = atleast2d(self.x, front=True)
            i = index_of_closest_point(coords, x)[0]
            return coords[i, :]
        else:
            raise NotImplementedError(
                "The point of application is not defined and no mesh is provided."
            )

    def index(self, mesh: Optional[Union[FemMesh, None]] = None) -> int:
        """
        Returns the index of the node where the load is applied.
        """
        if self._has_index_defined() > 0:
            return self._i
        else:
            coords = mesh.coords()
            x = atleast2d(self.x(mesh), front=True)
            i = index_of_closest_point(coords, x)[0]
            return i

    def assemble(
        self, mesh: FemMesh, out: Optional[Union[ndarray, None]] = None
    ) -> ndarray:
        """
        Returns the equivalent nodal representation.
        """
        index = self.index(mesh)
        nDOF = len(mesh.displacement_variables)
        nN = len(mesh.pointdata)

        if out is None:
            out = np.zeros((nN, nDOF), dtype=float)
        else:
            if not isinstance(out, ndarray):
                raise TypeError("out ought to be a NumPy array")
            if not out.shape == (nN, nDOF):
                raise ValueError("out has the wrong shape")

        target_frame = mesh.frame
        values = self.values(target_frame)

        dofmap = DOF.dofmap(
            mesh.displacement_variables, ["UX", "UY", "UZ", "ROTX", "ROTY", "ROTZ"]
        )
        out[index, :] += [values[i] for i in dofmap]

        return out
