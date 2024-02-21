from enum import Enum
from typing import Iterable, List, Optional


from .utils.fem import element_dofmap_bulk


class DOF(Enum):
    """
    An enumeration class to handle degrees of freedom. It acceprs several keys
    for the same DOF to help dissolve ambiguities between different notations.

    Examples
    --------
    >>> from sigmaepsilon.solid.fem.dofmap import DOF
    >>> DOF['UXX']
    <DOF.ROTX: 3>
    >>> DOF.UXX
    <DOF.ROTX: 3>
    >>> DOF.UXX.value
    3
    >>> DOF.UXX.name
    'ROTX'
    >>> DOF(3).name
    'ROTX'

    The keys 'UX', 'U1' and 'U' all refer to the same thing:

    >>> DOF.dofmap(['U', 'UX', 'U1'])
    [0, 0, 0]

    Similarly, the rotation around X can be referenced using
    multiple keys (for rotations, a total of 7 versions are available):

    >>> DOF.dofmap(['ROTX', 'UXX', 'UYZ', 'U32', 'U23'])
    [3, 3, 3, 3, 3]

    >>> {d.name: d.value for d in DOF}
    {'UX': 0, 'UY': 1, 'UZ': 2, 'ROTX': 3, 'ROTY': 4, 'ROTZ': 5}

    To map one set of DOFs to another:

    >>> DOF.dofmap(['W', 'ROTX', 'ROTY'], ['UZ', 'V', 'ROTY', 'U32'])
    [0, 3, 2]

    To get all the items as a dictionary (with their default names):

    >>> DOF.items()
    {'UX': 0, 'UY': 1, 'UZ': 2, 'ROTX': 3, 'ROTY': 4, 'ROTZ': 5}
    """

    UX = U1 = U = 0  # displacement in X direction
    UY = U2 = V = 1  # displacement in Y direction
    UZ = U3 = W = 2  # displacement in Z direction
    ROTX = UXX = UYZ = UZY = U11 = U23 = U32 = 3  # rotation around X
    ROTY = UYY = UXZ = UZX = U22 = U13 = U31 = 4  # rotation around Y
    ROTZ = UZZ = UXY = UYX = U33 = U12 = U21 = 5  # rotation around Z

    @classmethod
    def dofmap(
        cls, dofs: Iterable[str], host: Optional[Iterable[str]] = None
    ) -> List[int]:
        """
        Returns indices of dofs in a global dof system.

        Parameters
        ----------
        dofs: Iterable[str]
            An iterable of strings.
        host: Iterable[str]
            An iterable of dofs. This represents a global, or hosting
            dof system. If not provided, it is assumed that the host
            has all dofs of the class, in the same order.

        Examples
        --------
        >>> from sigmaepsilon.solid.fem.dofmap import DOF
        >>> DOF.dofmap(['UX', 'U', 'UXX'])
        [0, 0, 3]
        >>> DOF.dofmap(['W', 'ROTX', 'ROTY'])
        [2, 3, 4]
        >>> DOF.dofmap(['W', 'ROTX', 'ROTY'], ['W', 'UX', 'ROTY', 'U32'])
        [0, 3, 2]
        """
        if host:
            host_map = DOF.dofmap(host)
            return [host_map.index(dof) for dof in DOF.dofmap(dofs)]
        else:
            return [cls[d].value for d in dofs]

    @classmethod
    def items(cls) -> dict:
        """
        Returns the items of the class as a dictionary.

        Notes
        -----
        The items appear in the dictionary with their default names.

        Examples
        --------
        >>> from sigmaepsilon.solid.fem.dofmap import DOF
        >>> DOF.items()
        {'UX': 0, 'UY': 1, 'UZ': 2, 'ROTX': 3, 'ROTY': 4, 'ROTZ': 5}
        """
        return {d.name: d.value for d in DOF}

    def element_dofmap(self, nDOF: int, nNODE: int) -> List[int]:
        """
        Returns the element dof map for the DOF.

        Parameters
        ----------
        nDOF: int
            The number of displacement variables.
        nNODE: int
            The number of nodes.

        Examples
        --------
        >>> from sigmaepsilon.solid.fem.dofmap import DOF
        >>> DOF.UX.element_dofmap(3, 2)
        [0, 1, 2]
        >>> DOF.ROTX.element_dofmap(3, 2)
        [3, 4, 5]
        """
        return element_dofmap_bulk(self.value, nDOF, nNODE)