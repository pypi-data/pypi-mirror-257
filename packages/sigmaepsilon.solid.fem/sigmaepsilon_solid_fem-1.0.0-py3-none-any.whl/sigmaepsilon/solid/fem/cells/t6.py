import numpy as np
from numpy import ndarray

from sigmaepsilon.mesh.cells import T6
from sigmaepsilon.mesh.utils.numint import (
    Gauss_Legendre_Tri_1,
    Gauss_Legendre_Tri_3a,
    Gauss_Legendre_Tri_3b,
)

from ..data import MembraneFiniteElement
from ..material import MembraneMaterial


__all__ = ["T6_M"]


class T6_M(MembraneFiniteElement):
    """
    Linear strain triangle aka. LST developed by Fraeijs de Veubeke and Argyris
    :cite:p:`VeubekeLST1965, arcyris_1965`.
    """

    label = "T6_M"

    class Geometry(T6.Geometry):
        shape_function_evaluator: None
        shape_function_matrix_evaluator: None
        shape_function_derivative_evaluator: None
        monomial_evaluator: None
        quadrature = {
            "full": Gauss_Legendre_Tri_3a(center=np.array([1 / 3, 1 / 3])),
            "geometry": "full",
        }

        @classmethod
        def master_coordinates(cls) -> ndarray:
            """
            Returns local coordinates of the cell.

            Returns
            -------
            numpy.ndarray
            """
            return np.array(
                [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [0.5, 0.0], [0.5, 0.5], [0.0, 0.5]]
            )

        @classmethod
        def master_center(cls) -> ndarray:
            """
            Returns the local coordinates of the center of the cell.

            Returns
            -------
            numpy.ndarray
            """
            return np.array([[1 / 3, 1 / 3]])

    class Material(MembraneMaterial):
        quadrature = {
            "full": Gauss_Legendre_Tri_3a(center=np.array([1 / 3, 1 / 3])),
            "full2": Gauss_Legendre_Tri_3b(center=np.array([1 / 3, 1 / 3])),
            "selective": {(0, 1): "full", (2,): "reduced"},
            "reduced": Gauss_Legendre_Tri_1(center=np.array([1 / 3, 1 / 3])),
            "stiffness": "full",
        }
