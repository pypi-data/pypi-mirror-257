from sigmaepsilon.mesh.cells import TET10 as PolyCell
from sigmaepsilon.mesh.utils.numint import (
    Gauss_Legendre_Tet_1,
    Gauss_Legendre_Tet_4,
)

from ..data import VolumeFiniteElement
from ..material import Solid3dMaterial

__all__ = ["TET10"]


class TET10(VolumeFiniteElement):
    """
    Finite element class to handle 4-noded trilinear tetrahedra.
    """

    label = "TET10"

    class Geometry(PolyCell.Geometry):
        ...

    class Material(Solid3dMaterial):
        quadrature = {
            "full": Gauss_Legendre_Tet_4(),
            "selective": {(0, 1, 2): "full", (3, 4, 5): "reduced"},
            "reduced": Gauss_Legendre_Tet_1(),
            "stiffness": "full",
        }
