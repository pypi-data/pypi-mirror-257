from sigmaepsilon.mesh.cells import Q4 as PolyCell
from sigmaepsilon.mesh.utils.numint import (
    Gauss_Legendre_Quad_1,
    Gauss_Legendre_Quad_4,
)

from ..data import (
    FiniteElement,
    MembraneFiniteElement,
    FictiveDrillingMembraneFiniteElement,
)
from .mindlin import MindlinPlateFiniteElement
from ..material import (
    MembraneMaterial,
    FictiveDrillingMembraneMaterial,
    MindlinPlateMaterial,
    MindlinShellMaterial,
)

__all__ = ["Q4_M", "Q4_FDM", "Q4_P_MR", "Q4_S_MR"]


class Q4_M(MembraneFiniteElement):
    """
    Finite element class to handle 4-noded bilinear quadrilateral membranes.
    """

    label = "Q4_M"

    Geometry = PolyCell.Geometry

    class Material(MembraneMaterial):
        quadrature = {
            "full": Gauss_Legendre_Quad_4(),
            "selective": {(0, 1): "full", (2,): "reduced"},
            "reduced": Gauss_Legendre_Quad_1(),
            "stiffness": "full",
        }


class Q4_FDM(FictiveDrillingMembraneFiniteElement):
    """
    Finite element class to handle 4-noded bilinear quadrilateral membranes.
    """

    label = "Q4_FM"

    Geometry = PolyCell.Geometry

    class Material(FictiveDrillingMembraneMaterial):
        quadrature = {
            "full": Gauss_Legendre_Quad_4(),
            "selective": {(0, 1): "full", (2,): "reduced"},
            "reduced": Gauss_Legendre_Quad_1(),
            "stiffness": "full",
        }


class Q4_P_MR(MindlinPlateFiniteElement):
    """
    Finite element class to handle 4-noded bilinear quadrilateral Uflyand-Mindlin plates.
    """

    label = "Q4_P_MR"

    Geometry = PolyCell.Geometry

    class Material(MindlinPlateMaterial):
        quadrature = {
            "full": Gauss_Legendre_Quad_4(),
            "selective": {(0, 1, 2): "full", (3, 4): "reduced"},
            "reduced": Gauss_Legendre_Quad_1(),
            "stiffness": "selective",
        }


class Q4_S_MR(FiniteElement):
    """
    Finite element class to handle 4-noded bilinear quadrilateral Uflyand-Mindlin shells.
    """

    label = "Q4_S_MR"

    Geometry = PolyCell.Geometry

    class Material(MindlinShellMaterial):
        quadrature = {
            "full": Gauss_Legendre_Quad_4(),
            "selective": {(0, 1, 3, 4, 5): "full", (2, 6, 7): "reduced"},
            "reduced": Gauss_Legendre_Quad_1(),
            "stiffness": "selective",
        }
