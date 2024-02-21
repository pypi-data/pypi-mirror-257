from typing import Iterable, Union, Tuple, Optional

import numpy as np
from numpy import ndarray, concatenate as conc
from scipy.sparse import coo_matrix as coo

from sigmaepsilon.mesh.space import PointCloud
from sigmaepsilon.mesh.data import PolyCell

from .base import FemEssentialBoundaryCondition
from ..data.mesh import FemMesh
from ..dofmap import DOF
from ..constants import DEFAULT_DIRICHLET_PENALTY
from ..utils.ebc import link_points_to_points


__all__ = ["NodeToNode"]


class NodeToNode(FemEssentialBoundaryCondition):
    """
    Constrains relative motion of nodes.

    Parameters
    ----------
    imap: Union[dict, ndarray, list]
        An iterable describing pairs of nodes.
    penalty: float, Optional
        Penalty value for Courant-type penalization.
        Default is `~sigmaepsilon.solid.fem.constants.DEFAULT_DIRICHLET_PENALTY`.
    dofs: Iterable, Optinal
        An iterable of the constrained degrees of freedom. It not specified, all
        degrees of freedom are constrained.
    source: PointCloud, Optional
        The source pointcloud. Only if 'imap' is not provided.
    target: PointCloud, Optional
        The target pointcloud. Only if 'imap' is not provided.

    Example
    -------
    The following lines tie together all DOFs of nodes 1 with node 2 and node 3 with 4.
    The large penalty value means that the tied nodes should have the same displacements.

    >>> from sigmaepsilon.solid.fem import NodeToNode
    >>> n2n = NodeToNode([[1, 2], [3, 4]], penalty=1e12)

    To tie only DOFs 'UX' and 'ROTZ':

    >>> n2n = NodeToNode([[1, 2], [3, 4]], dofs=['UX', 'ROTZ'], penalty=1e12)
    """

    def __init__(
        self,
        imap: Union[dict, ndarray, list] = None,
        *,
        source: Optional[Union[PolyCell, None]] = None,
        target: Optional[Union[PolyCell, None]] = None,
        dofs: Optional[Union[Iterable, None]] = None,
        penalty: Optional[float] = DEFAULT_DIRICHLET_PENALTY,
    ):
        if imap is None:
            if isinstance(source, PointCloud) and isinstance(target, PointCloud):
                imap = link_points_to_points(source, target)
        self.imap = imap
        self.penalty = penalty
        if isinstance(dofs, Iterable):
            self.dofmap = DOF.dofmap(dofs)
        else:
            self.dofmap = None

    def assemble(self, mesh: FemMesh) -> Tuple[coo, ndarray]:
        """
        Returns the penalty stiffness matrix and the penalty load matrix.
        """
        imap = None
        if isinstance(self.imap, dict):
            imap = np.stack([list(self.imap.keys()), list(self.imap.values())], axis=1)
        else:
            imap = np.array(self.imap).astype(int)
        nI = len(imap)

        nDOF = mesh.number_of_displacement_variables
        nN = len(mesh.pointdata)
        N = nDOF * nN

        if self.dofmap is None:
            dmap = np.arange(nDOF)
        else:
            dmap = self.dofmap
        dmap = np.array(dmap, dtype=int)

        nF = nI * len(dmap)
        fdata = np.tile([1, -1], nF)
        frows = np.repeat(np.arange(nF), 2)
        i_source = conc([dmap + (i_ * nDOF) for i_ in imap[:, 0]])
        i_target = conc([dmap + (i_ * nDOF) for i_ in imap[:, 1]])
        fcols = np.stack([i_source, i_target], axis=1).flatten()
        factors = coo((fdata, (frows, fcols)), shape=(nF, N))

        Kp = self.penalty * (factors.T @ factors)
        fp = np.zeros(N, dtype=float)
        Kp.eliminate_zeros()
        return Kp, fp