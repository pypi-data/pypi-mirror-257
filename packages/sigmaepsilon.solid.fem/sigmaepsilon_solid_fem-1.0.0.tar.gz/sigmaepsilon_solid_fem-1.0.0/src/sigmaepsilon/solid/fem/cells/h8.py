from sigmaepsilon.mesh.cells import H8 as PolyCell
from sigmaepsilon.mesh.utils.numint import Gauss_Legendre_Hex_Grid

from ..data import VolumeFiniteElement
from ..material import Solid3dMaterial

__all__ = ["H8"]


class H8(VolumeFiniteElement):
    """
    Finite element class to handle 8-noded trilinear hexahedrons.
    """

    label = "H8"

    Geometry = PolyCell.Geometry

    class Material(Solid3dMaterial):
        quadrature = {
            "full": Gauss_Legendre_Hex_Grid(2, 2, 2),
            "selective": {(0, 1, 2): "full", (3, 4, 5): "reduced"},
            "reduced": Gauss_Legendre_Hex_Grid(1, 1, 1),
            "stiffness": "selective",
        }
