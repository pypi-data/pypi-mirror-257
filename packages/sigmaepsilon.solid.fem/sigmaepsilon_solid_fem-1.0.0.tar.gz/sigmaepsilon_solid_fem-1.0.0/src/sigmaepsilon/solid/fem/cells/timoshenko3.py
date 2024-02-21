from sigmaepsilon.mesh.cells import L3 as PolyCell
from sigmaepsilon.mesh.utils.numint import Gauss_Legendre_Line_Grid

from .timoshenko import TimoshenkoBase
from ..material import TimoshenkoBeamMaterial

__all__ = ["Timoshenko3"]


class Timoshenko3(TimoshenkoBase):
    """
    Finite element class to handle 3-noded Timoshenko-Ehrenfest beams.
    """

    label = "Timoshenko3"

    class Geometry(PolyCell.Geometry):
        ...

    class Material(TimoshenkoBeamMaterial):
        quadrature = {
            "full": Gauss_Legendre_Line_Grid(3),
            "selective": {(0, 3, 4, 5): "full", (1, 2): "reduced"},
            "reduced": Gauss_Legendre_Line_Grid(2),
            "mass": Gauss_Legendre_Line_Grid(3),
            "stiffness": "reduced",
        }
