from functools import partial

from sigmaepsilon.math.numint import gauss_points
from sigmaepsilon.mesh.cells import Q9

from .kirchhoffplate import KirchhoffPlateElement
from ..material import KirchhoffPlateMaterial
from .utils.k9p import (
    strain_displacement_matrix_bulk_multi_k9p,
    shape_function_matrix_bulk_multi_k9p,
    calculate_shear_forces_k9p,
    approximate_internal_forces_UM,
)

__all__ = ["Q9_P_KL"]


class Q9_P_KL(KirchhoffPlateElement):
    """
    Finite element class to handle 4-noded bilinear quadrilateral
    Kirchhoff-Love plates.
    """

    label = "Q9_P_KL"

    Geometry = Q9.Geometry
    
    class Material(KirchhoffPlateMaterial):
        shape_function_matrix_evaluator = shape_function_matrix_bulk_multi_k9p
        strain_displacement_matrix_evaluator = strain_displacement_matrix_bulk_multi_k9p
        shear_force_calculator = calculate_shear_forces_k9p
        internal_force_calculator = approximate_internal_forces_UM
        quadrature = {
            "full": partial(gauss_points, 5, 5),
            "stiffness": "full",
        }
