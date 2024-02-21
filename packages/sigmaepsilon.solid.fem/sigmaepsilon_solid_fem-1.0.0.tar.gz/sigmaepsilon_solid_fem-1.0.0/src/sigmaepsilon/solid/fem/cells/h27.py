from sigmaepsilon.mesh.cells import H27 as PolyCell
from sigmaepsilon.mesh.utils.numint import Gauss_Legendre_Hex_Grid

from ..data import VolumeFiniteElement
from ..material import Solid3dMaterial

__all__ = ["H27"]


class H27(VolumeFiniteElement):
    """
    Finite element class to handle 27-noded triquadratic hexahedrons.
    """

    label = "H27"

    Geometry = PolyCell.Geometry

    class Material(Solid3dMaterial):
        quadrature = {
            "full": Gauss_Legendre_Hex_Grid(3, 3, 3),
            "selective": {(0, 1, 2): "full", (3, 4, 5): "reduced"},
            "reduced": Gauss_Legendre_Hex_Grid(2, 2, 2),
            "stiffness": "full",
        }
