from sigmaepsilon.mesh.cells import QuadraticLine as PolyCell
from sigmaepsilon.mesh.utils.numint import Gauss_Legendre_Line_Grid

from .bernoulli import BernoulliBase
from ..material import BernoulliBeamMaterial
from .gen.b3 import (
    shape_function_values_bulk,
    shape_function_derivatives_bulk,
    shape_function_derivatives_multi_L,
)

__all__ = ["Bernoulli3"]


class Bernoulli3(BernoulliBase):
    """
    Finite element class to handle 3-noded Bernoulli beams.
    """

    label = "Bernoulli3"

    class Geometry(PolyCell.Geometry):
        ...

    class Material(BernoulliBeamMaterial):
        shape_function_evaluator = shape_function_values_bulk
        shape_function_derivative_evaluator = shape_function_derivatives_bulk
        dshpfnc_geom = shape_function_derivatives_multi_L  # FIXME not necessary

        quadrature = {
            "full": Gauss_Legendre_Line_Grid(6),
            "stiffness": "full",
            "mass": Gauss_Legendre_Line_Grid(8),
        }
