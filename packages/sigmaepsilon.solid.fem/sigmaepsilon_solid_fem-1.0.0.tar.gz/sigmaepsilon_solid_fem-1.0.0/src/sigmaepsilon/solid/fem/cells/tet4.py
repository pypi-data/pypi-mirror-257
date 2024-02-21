from sigmaepsilon.mesh.cells import TET4 as PolyCell
from sigmaepsilon.mesh.utils.numint import Gauss_Legendre_Tet_1

from ..data import VolumeFiniteElement
from ..material import Solid3dMaterial

__all__ = ["TET4"]


class TET4(VolumeFiniteElement):
    """
    Finite element class to handle 4-noded trilinear tetrahedra.
    """

    label = "TET4"

    Geometry = PolyCell.Geometry

    class Material(Solid3dMaterial):
        quadrature = {
            "full": Gauss_Legendre_Tet_1,
            "geometry": "full",
            "stiffness": "full",
        }
