from sigmaepsilon.mesh.cells import Q8 as PolyCell
from sigmaepsilon.mesh.utils.numint import (
    Gauss_Legendre_Quad_9,
    Gauss_Legendre_Quad_4,
)

from ..data import FiniteElement, MembraneFiniteElement
from .mindlin import MindlinPlateFiniteElement
from ..material import MembraneMaterial, MindlinPlateMaterial, MindlinShellMaterial


__all__ = ["Q8_M", "Q8_P_MR", "Q8_S_MR"]


class Q8_M(MembraneFiniteElement):
    """
    Finite element class to handle 4-noded biquadratic quadrilateral membranes.
    """

    label = "Q8_M"
    standalone = True

    Geometry = PolyCell.Geometry

    class Material(MembraneMaterial):
        qrule = "full"
        quadrature = {
            "full": Gauss_Legendre_Quad_9(),
            "selective": {(0, 1): "full", (2,): "reduced"},
            "reduced": Gauss_Legendre_Quad_4(),
            "stiffness": "full",
        }


class Q8_P_MR(MindlinPlateFiniteElement):
    """
    Finite element class to handle 4-noded biquadratic quadrilateral Mindlin-Reissner plates.
    """

    label = "Q8_P_MR"
    Geometry = PolyCell.Geometry

    class Material(MindlinPlateMaterial):
        qrule = "selective"
        quadrature = {
            "full": Gauss_Legendre_Quad_9(),
            "selective": {(0, 1, 2): "full", (3, 4): "reduced"},
            "reduced": Gauss_Legendre_Quad_4(),
            "stiffness": "selective",
        }


class Q8_S_MR(FiniteElement):
    """
    Finite element class to handle 4-noded biquadratic quadrilateral Mindlin-Reissner shells.
    """

    label = "Q8_S_MR"
    Geometry = PolyCell.Geometry

    class Material(MindlinShellMaterial):
        quadrature = {
            "full": Gauss_Legendre_Quad_9(),
            "selective": {(0, 1, 3, 4, 5): "full", (2, 6, 7): "reduced"},
            "reduced": Gauss_Legendre_Quad_4(),
            "stiffness": "selective",
        }
