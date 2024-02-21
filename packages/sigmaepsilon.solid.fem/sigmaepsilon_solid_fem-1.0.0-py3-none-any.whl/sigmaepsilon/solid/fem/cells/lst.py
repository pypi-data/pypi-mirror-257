from sigmaepsilon.mesh.cells import T6 as PolyCell
from sigmaepsilon.mesh.utils.numint import (
    Gauss_Legendre_Tri_1,
    Gauss_Legendre_Tri_3a,
    Gauss_Legendre_Tri_3b,
)

from ..data import FiniteElement, MembraneFiniteElement
from .mindlin import MindlinPlateFiniteElement
from ..material import MembraneMaterial, MindlinPlateMaterial, MindlinShellMaterial


__all__ = ["LST_M", "LST_P_MR", "LST_S_MR"]


class LST_M(MembraneFiniteElement):
    """
    Linear strain triangle aka. LST developed by Fraeijs de Veubeke and Argyris
    :cite:p:`VeubekeLST1965, arcyris_1965`.
    """

    label = "LST_M"

    Geometry = PolyCell.Geometry

    class Material(MembraneMaterial):
        quadrature = {
            "full": Gauss_Legendre_Tri_3a(),
            "full2": Gauss_Legendre_Tri_3b(),
            "selective": {(0, 1): "full", (2,): "reduced"},
            "reduced": Gauss_Legendre_Tri_1(),
            "stiffness": "full",
        }


class LST_P_MR(MindlinPlateFiniteElement):
    label = "LST_P_MR"

    Geometry = PolyCell.Geometry

    class Material(MindlinPlateMaterial):
        quadrature = {
            "full": Gauss_Legendre_Tri_3a(),
            "full2": Gauss_Legendre_Tri_3b(),
            "selective": {(0, 1, 2): "full", (3, 4): "reduced"},
            "reduced": Gauss_Legendre_Tri_1(),
            "stiffness": "full",
        }


class LST_S_MR(FiniteElement):
    label = "LST_S_MR"

    Geometry = PolyCell.Geometry

    class Material(MindlinShellMaterial):
        quadrature = {
            "full": Gauss_Legendre_Tri_3a(),
            "full2": Gauss_Legendre_Tri_3b(),
            "selective": {(0, 1, 3, 4, 5): "full", (2, 6, 7): "reduced"},
            "reduced": Gauss_Legendre_Tri_1(),
            "stiffness": "full",
        }
