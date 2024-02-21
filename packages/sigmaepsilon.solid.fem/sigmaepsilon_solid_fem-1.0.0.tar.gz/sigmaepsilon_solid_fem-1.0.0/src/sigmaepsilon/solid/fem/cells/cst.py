from sigmaepsilon.mesh.cells import T3 as PolyCell
from sigmaepsilon.mesh.utils.numint import Gauss_Legendre_Tri_1

from ..data import FiniteElement, MembraneFiniteElement, PlateFiniteElement
from ..material import MembraneMaterial, MindlinPlateMaterial, MindlinShellMaterial


__all__ = ["CST_M", "CST_P_MR", "CST_S_MR"]


class CST_M(MembraneFiniteElement):
    """
    The constant-strain triangle a.k.a., CST triangle, Turner triangle or
    linear triangle for membranes. Developed as a plane stress element by
    John Turner, Ray Clough and Harold Martin in 1952-53 [1], published in 1956 [2].

    Notes
    -----
    The element has poor performance and is represented for historycal reasons.
    Don't use it in a production enviroment, unless your mesh is extremely dense.

    References
    ----------
    .. [1] R. W. Clough, The finite element method - a personal view of its original
       formulation, in From Finite Elements to the Troll Platform - the Ivar Holand
       70th Anniversary Volume, ed. by K. Bell, Tapir, Trondheim, Norway, 89-100, 1994.
    .. [2] M. J. Turner, R. W. Clough, H. C. Martin, and L. J. Topp, Stiffness and
       deflection analysis of complex structures, J. Aero. Sco., 23, pp. 805-824, 1956.
    """

    label = "CST_M"
    standalone = True

    class Geometry(PolyCell.Geometry):
        ...

    class Material(MembraneMaterial):
        quadrature = {
            "full": Gauss_Legendre_Tri_1,
            "geometry": "full",
            "stiffness": "full",
        }


class CST_P_MR(PlateFiniteElement):
    label = "CST_P_MR"
    standalone = True

    class Geometry(PolyCell.Geometry):
        ...

    class Material(MindlinPlateMaterial):
        quadrature = {
            "full": Gauss_Legendre_Tri_1,
            "geometry": "full",
            "stiffness": "full",
        }


class CST_S_MR(FiniteElement):
    label = "CST_S_MR"

    class Geometry(PolyCell.Geometry):
        ...

    class Material(MindlinShellMaterial):
        quadrature = {
            "full": Gauss_Legendre_Tri_1,
            "geometry": "full",
            "stiffness": "full",
        }
