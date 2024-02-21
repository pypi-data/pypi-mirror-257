from typing import Iterable, Union, Tuple, Optional

import numpy as np
from numpy import ndarray
from scipy.sparse import coo_matrix as coo

from sigmaepsilon.mesh.space import PointCloud
from sigmaepsilon.mesh.data import PolyCell

from .base import FemEssentialBoundaryCondition
from ..data.mesh import FemMesh
from ..dofmap import DOF
from ..constants import DEFAULT_DIRICHLET_PENALTY
from ..utils.ebc import (
    link_points_to_body,
    _body_to_body_stiffness_data_,
)


__all__ = ["BodyToBody"]


class BodyToBody(FemEssentialBoundaryCondition):
    """
    Constrains the dofs of two touching bodies by gluing them together.

    Parameters
    ----------
    source: PolyCell, Optional
        The source body. It is optional at creation, but must be set at some point.
    target: PolyCell, Optional
        The target body. It is optional at creation, but must be set at some point.
    dofs: Iterable, Optinal
        An iterable of the constrained global degrees of freedom. It not specified,
        all degrees of freedom are constrained.
    penalty: float, Optional
        The penalty value.
    lazy: bool, Optional
        Default is True.
    tol: float, Optional
        Floating point tolerance for detecting point in polygons. Default is 1e-12.
    k: int, Optional
        The number of neighbours.

    Notes
    -----
    The two bodies must have a common surface.
    """

    def __init__(
        self,
        source: Optional[Union[PolyCell, None]] = None,
        target: Optional[Union[PolyCell, None]] = None,
        dofs: Optional[Union[Iterable, None]] = None,
        penalty: Optional[float] = DEFAULT_DIRICHLET_PENALTY,
        lazy: Optional[bool] = True,
        tol: Optional[float] = 1e-12,
        k: Optional[int] = 4,
        touching: Optional[bool] = False,
        factors: Optional[Union[ndarray, None]] = None,
        indices: Optional[Union[ndarray, None]] = None,
    ):
        if source and target:
            #assert source.Geometry.number_of_spatial_dimensions == 3, "Source must be a 3 dimensional body!"
            #assert target.Geometry.number_of_spatial_dimensions == 3, "Source must be a 3 dimensional body!"
            assert (
                source.container.source() is target.container.source()
            ), "The source and the target must belong to the same pointcloud!"
            assert (
                source.container.source() is source.container.root
            ), "The mesh must be brought to a standard form!"
            #assert isinstance(
            #    target.__class__.monomsfnc, Callable
            #), "The class is not equipped with the tools for this operation."
        self.source = source
        self.target = target
        self.penalty = penalty
        self.lazy = lazy
        self.k = k
        self.tol = tol
        self.touching = touching
        self.factors = factors
        self.indices = indices

        if isinstance(dofs, Iterable):
            self.dofmap = DOF.dofmap(dofs)
        else:
            self.dofmap = None

    def assemble(self, mesh: FemMesh) -> Tuple[coo, ndarray]:
        if (self.factors is None) or (self.indices is None):
            S: PolyCell = self.source
            T: PolyCell = self.target

            assert (
                S.container.root == mesh
            ), "The input mesh must be the root of both the source and the target."
            assert (
                T.container.root == mesh
            ), "The input mesh must be the root of both the source and the target."

            if self.touching:
                coords, topo_source_surface = S.extract_surface(detach=False)
                source_indices = np.unique(topo_source_surface)
            else:
                coords = S.source_coords()
                source_indices = S.unique_indices()

            source_coords = coords[source_indices]
            factors, indices = link_points_to_body(
                PointCloud(source_coords, inds=source_indices),
                T,
                self.lazy,
                self.tol,
                self.k,
            )
        else:
            factors, indices = self.factors, self.indices

        nDOF = mesh.number_of_displacement_variables
        nN = len(mesh.pointdata)
        N = nDOF * nN
        if self.dofmap is None:
            dmap = np.arange(nDOF)
        else:
            dmap = self.dofmap
        dmap = np.array(dmap, dtype=int)

        factors, indices = _body_to_body_stiffness_data_(factors, indices, dmap, nDOF)
        fdata = factors.flatten()
        frows = np.repeat(np.arange(factors.shape[0]), factors.shape[1])
        fcols = indices.flatten()
        factors = coo((fdata, (frows, fcols)), shape=(factors.shape[0], N))

        Kp = self.penalty * (factors.T @ factors)
        fp = np.zeros(N, dtype=float)
        Kp.eliminate_zeros()
        return Kp, fp