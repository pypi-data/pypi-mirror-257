from typing import Iterable, Any, Optional

import numpy as np

from sigmaepsilon.deepdict import DeepDict

from ..data.mesh import FemMesh
from .base import FemNaturalBoundaryCondition


__all__ = ["FemLoad"]


class FemLoad(DeepDict):
    """
    A class to handle load groups.

    Examples
    --------
    >>> from sigmaepsilon.solid.fem import FemLoad, PointLoad
    >>> loads = FemLoad(
    >>>     group1 = FemLoad(
    >>>         case1 = PointLoad(...),
    >>>         case2 = [PointLoad(...), PointLoad(...)],
    >>>     ),
    >>>     group2 = FemLoad(
    >>>         case1 = PointLoad(...),
    >>>         case2 = PointLoad(...),
    >>>     ),
    >>> )

    You can modify the cooperativity of the load cases in a group

    >>> loads['group1'].cooperative = True

    Since the FemLoad is a subclass of DeepDict,
    a case is accessible as

    >>> loads['group1', 'case1']

    If you want to protect the object from the accidental
    creation of nested subdirectories, you can lock the layout
    by typing

    >>> loads.lock()
    """

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], Iterable):
            args = args[0]
        
        _kwargs = dict()
        for k, v in kwargs.items():
            if isinstance(v, FemLoad):
                _kwargs[k] = v
            elif isinstance(v, FemNaturalBoundaryCondition):
                _kwargs[k] = FemLoad(v)
            elif isinstance(v, Iterable):
                assert all(list(map(lambda x: isinstance(x, FemNaturalBoundaryCondition), v)))
                _kwargs[k] = FemLoad(*v)
        
        if len(args) > 0:
            assert len(_kwargs) == 0
            
        if len(kwargs) > 0:
            assert len(args) == 0
        
        super().__init__(**_kwargs)
        self._cooperative = False
        self._cases = args
        self._index = None
        
    @property
    def cases(self) -> Iterable[FemNaturalBoundaryCondition]:
        """
        Returns the load cases.
        """
        return self._cases
    
    @property
    def index(self) -> int:
        """
        Returns the index of the load group in the RHS column vector.
        """
        return self._index
    
    @property
    def cooperative(self) -> bool:
        """
        Returns `True` if the load cases of this group can interact.
        """
        return self._cooperative

    @cooperative.setter
    def cooperative(self, value: bool):
        """
        Sets the cooperativity of the cases in the group.
        """
        self._cooperative = value

    def blocks(
        self,
        *,
        inclusive: Optional[bool] = False,
        blocktype: Optional[Any] = None,
        deep: Optional[bool] = True,
    ) -> Iterable["FemLoad"]:
        """
        Returns a generator object that yields all the subgroups.

        Parameters
        ----------
        inclusive: bool, Optional
            If True, returns the object the call is made upon.
            Default is False.
        blocktype: Any, Optional
            The type of the load groups to return. Default is None, that
            returns all types.
        deep: bool, Optional
            If True, all deep groups are returned separately. Default is True.

        Yields
        ------
        FemLoad
        """
        dtype = FemLoad if blocktype is None else blocktype
        return self.containers(inclusive=inclusive, dtype=dtype, deep=deep)
    
    def assemble(self, mesh: FemMesh) -> None:
        """
        Assembles the load vectors of the load cases.
        """
        nDOF = len(mesh.displacement_variables)
        nN = len(mesh.pointdata)
        blocks_with_cases = list(filter(lambda b: len(b.cases) > 0, self.blocks()))
        nRHS = len(blocks_with_cases)
        loads = np.zeros((nN, nDOF, nRHS), dtype=float)
        
        for i, block in enumerate(blocks_with_cases):
            block._index = i
            for case in block.cases:
                case.assemble(mesh, out=loads[:, :, i])
                
        mesh.pd.loads = np.squeeze(loads)