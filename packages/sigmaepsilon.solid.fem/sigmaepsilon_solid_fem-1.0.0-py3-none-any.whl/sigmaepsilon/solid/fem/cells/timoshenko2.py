from sigmaepsilon.mesh.cells import L2 as PolyCell
from sigmaepsilon.mesh.utils.numint import Gauss_Legendre_Line_Grid

from .timoshenko import TimoshenkoBase
from ..material import TimoshenkoBeamMaterial

__all__ = ["Timoshenko2"]


class Timoshenko2(TimoshenkoBase):
    """
    Finite element class to handle 2-noded Timoshenko-Ehrenfest beams.
    """

    label = "Timoshenko2"

    class Geometry(PolyCell.Geometry):
        ...

    class Material(TimoshenkoBeamMaterial):
        quadrature = {
            "full": Gauss_Legendre_Line_Grid(2),
            "selective": {(0, 3, 4, 5): "full", (1, 2): "reduced"},
            "reduced": Gauss_Legendre_Line_Grid(1),
            "mass": Gauss_Legendre_Line_Grid(2),
            "stiffness": "reduced",
        }
