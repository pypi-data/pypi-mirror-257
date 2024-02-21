from typing import TypeVar, Generic

from numpy import ndarray
import numpy as np

from sigmaepsilon.mesh.cells import Q9
from sigmaepsilon.mesh.utils.numint import (
    Gauss_Legendre_Quad_9,
    Gauss_Legendre_Quad_4,
)
from sigmaepsilon.math.linalg.sparse.jaggedarray import JaggedArray

from ..typing import (
    FemDataProtocol,
    PointDataProtocol,
)
from ..data import MembraneFiniteElement
from ..material import MembraneMaterial
from .utils.q5 import (
    stiffness_matrix_T2,
    nodal_data_T2,
    approximation_matrix_T2_bulk,
    nodal_approximation_matrix_T2_bulk,
)
from ..utils.fem import topo_to_gnum

__all__ = ["Q5_M_Veubeke"]

FD = TypeVar("FD", bound=FemDataProtocol)
PD = TypeVar("PD", bound=PointDataProtocol)


class Q5_M_Veubeke(Generic[FD, PD], MembraneFiniteElement[FD, PD]):
    """
    A nonconform membrane superelement consisting of 4 Veubeke triangles.

    The specialty of the element is that it only has connectors on the edges
    of the cell. As a result, elements of this class are nonconforming and
    shoulf not be used for production stress analysis, but perform surprisingly
    well among some unexpected circumstances in topology optimization.

    The class has 9 geometrical nodes, only 5 of which is active in the sense of work.

    The element only supports very basic calculations and is mainly for experimental work.

    Refe
    -----
    The element requires nodal distribution factors to be calculated.
    """

    label = "Q5_Veubeke_M"
    standalone = True
    mask = [False, False, False, False, True, True, True, True, True]

    class Geometry(Q9.Geometry):
        ...

    class Material(MembraneMaterial):
        quadrature = {
            "full": Gauss_Legendre_Quad_9(),
            "selective": {(0, 1): "full", (2,): "reduced"},
            "reduced": Gauss_Legendre_Quad_4(),
            "stiffness": "full",
        }

    def _elastic_stiffness_matrix_(
        self, *, transform: bool = True, **kwargs
    ) -> ndarray:
        ec = kwargs.get("_ec", self.local_coordinates())
        D = self.material_stiffness
        K = stiffness_matrix_T2(D, ec)
        return self._transform_coeff_matrix_(K) if transform else K

    def _strain_load_vector_(self, values: ndarray = None) -> ndarray:
        # FIXME : returns a zero, but shape-correct array
        nE, _, nRHS = values.shape
        nNE = 5  # self.Geometry.number_of_nodes
        nDOF = self.Material.number_of_displacement_variables
        nodal_loads = np.zeros((nE, nNE * nDOF, nRHS))
        return nodal_loads  # (nE, nTOTV, nRHS)

    def global_dof_numbering(self, *_, **kwargs) -> JaggedArray:
        topo = kwargs.get("topo", self.topology().to_numpy())
        nDOFN = self.container.number_of_displacement_variables
        data = topo_to_gnum(topo[:, 4:], nDOFN)
        return JaggedArray(data)

    def redistribute_passive_data(self, data: ndarray, key: str) -> None:
        super().distribute_nodal_data(data, key)
        if key == "loads":
            celldata = self._wrapped["loads"].to_numpy()
            self._wrapped["loads"] = nodal_data_T2(celldata)

    def approximation_matrix(self, *args, **kwargs) -> ndarray:
        return approximation_matrix_T2_bulk(self.ndf.to_numpy())

    def nodal_approximation_matrix(self, *args, **kwargs) -> ndarray:
        return nodal_approximation_matrix_T2_bulk(self.ndf.to_numpy())
