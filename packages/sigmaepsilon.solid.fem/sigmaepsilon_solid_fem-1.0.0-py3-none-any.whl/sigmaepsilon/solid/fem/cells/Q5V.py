from sigmaepsilon.mesh.cells import Q9
from sigmaepsilon.mesh.utils.numint import (
    Gauss_Legendre_Quad_9,
    Gauss_Legendre_Quad_4,
)

from ..data import MembraneFiniteElement
from ..material import MembraneMaterial


__all__ = ["Q5V_M"]


class Q5V_M(MembraneFiniteElement):
    """
    Finite element class to handle 4-noded biquadratic quadrilateral membranes.
    """

    label = "Q5V_M"
    standalone = True

    Geometry = Q9.Geometry

    class Material(MembraneMaterial):
        qrule = "full"
        quadrature = {
            "full": Gauss_Legendre_Quad_9(),
            "selective": {(0, 1): "full", (2,): "reduced"},
            "reduced": Gauss_Legendre_Quad_4(),
            "stiffness": "full",
        }