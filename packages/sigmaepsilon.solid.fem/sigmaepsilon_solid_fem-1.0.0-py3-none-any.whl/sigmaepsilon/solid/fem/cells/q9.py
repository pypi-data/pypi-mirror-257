from sigmaepsilon.mesh.cells import Q9 as PolyCell
from sigmaepsilon.mesh.utils.numint import (
    Gauss_Legendre_Quad_9,
    Gauss_Legendre_Quad_4,
)

from ..data import FiniteElement, MembraneFiniteElement
from .mindlin import MindlinPlateFiniteElement
from ..material import MembraneMaterial, MindlinPlateMaterial, MindlinShellMaterial

__all__ = ["Q9_M", "Q9_P_MR", "Q9_S_MR"]


class Q9_M(MembraneFiniteElement):
    """
    Finite element class to handle 4-noded biquadratic quadrilateral membranes.
    """

    label = "Q9_M"
    Geometry = PolyCell.Geometry

    class Material(MembraneMaterial):
        quadrature = {
            "full": Gauss_Legendre_Quad_9,
            "selective": {(0, 1): "full", (2,): "reduced"},
            "reduced": Gauss_Legendre_Quad_4,
            "stiffness": "full",
        }


class Q9_P_MR(MindlinPlateFiniteElement):
    """
    Finite element class to handle 4-noded biquadratic quadrilateral Mindlin-Reissner plates.
    """

    label = "Q9_P_MR"
    Geometry = PolyCell.Geometry

    class Material(MindlinPlateMaterial):
        quadrature = {
            "full": Gauss_Legendre_Quad_9,
            "selective": {(0, 1, 2): "full", (3, 4): "reduced"},
            "reduced": Gauss_Legendre_Quad_4,
            "stiffness": "selective",
        }


class Q9_S_MR(FiniteElement):
    """
    Finite element class to handle 4-noded biquadratic quadrilateral Mindlin-Reissner shells.
    """

    label = "Q9_S_MR"
    Geometry = PolyCell.Geometry

    class Material(MindlinShellMaterial):
        quadrature = {
            "full": Gauss_Legendre_Quad_9,
            "selective": {(0, 1, 3, 4, 5): "full", (2, 6, 7): "reduced"},
            "reduced": Gauss_Legendre_Quad_4,
            "stiffness": "selective",
        }
