from functools import partial

from sigmaepsilon.math.numint import gauss_points
from sigmaepsilon.mesh.cells import Q4

from .kirchhoffplate import KirchhoffPlateElement
from ..material import KirchhoffPlateMaterial
from .utils.k4p import (
    strain_displacement_matrix_bulk_multi_k4p,
    shape_function_matrix_bulk_multi_k4p,
    calculate_shear_forces_k4p,
    approximate_internal_forces_UM,
)

__all__ = ["Q4_P_KL"]


class Q4_P_KL(KirchhoffPlateElement):
    """
    Finite element class to handle 4-noded bilinear quadrilateral
    Kirchhoff-Love plates.
    """

    label = "Q4_P_KL"

    Geometry = Q4.Geometry
    
    class Material(KirchhoffPlateMaterial):
        shape_function_matrix_evaluator = shape_function_matrix_bulk_multi_k4p
        strain_displacement_matrix_evaluator = strain_displacement_matrix_bulk_multi_k4p
        shear_force_calculator = calculate_shear_forces_k4p
        internal_force_calculator = approximate_internal_forces_UM
        quadrature = {
            "full": partial(gauss_points, 2, 2),
            "stiffness": "full",
        }
