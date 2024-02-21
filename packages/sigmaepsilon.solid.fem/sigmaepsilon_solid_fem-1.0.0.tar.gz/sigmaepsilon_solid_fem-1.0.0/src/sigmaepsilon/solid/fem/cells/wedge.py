from sigmaepsilon.mesh.cells import W6 as Wedge6, W18 as Wedge18
from sigmaepsilon.mesh.utils.numint import (
    Gauss_Legendre_Wedge_3x2,
    Gauss_Legendre_Wedge_3x3,
)

from ..data import VolumeFiniteElement
from ..material import Solid3dMaterial

__all__ = ["W6", "W18"]


class W6(VolumeFiniteElement):
    """
    Finite element class to handle 6-noded trilinear isoparametric wedges.
    """

    label = "W6"

    Geometry = Wedge6.Geometry

    class Material(Solid3dMaterial):
        quadrature = {
            "full": Gauss_Legendre_Wedge_3x2,
            "geometry": "full",
            "stiffness": "full",
        }


class W18(VolumeFiniteElement):
    """
    Finite element class to handle 18-noded biquadratic-quadratic isoparametric wedges.
    """

    label = "W18"

    Geometry = Wedge18.Geometry

    class Material(Solid3dMaterial):
        quadrature = {
            "full": Gauss_Legendre_Wedge_3x3,
            "geometry": "full",
            "stiffness": "full",
        }
