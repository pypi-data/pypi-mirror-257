from typing import Callable, Iterable, Union

import numpy as np
from numpy import ndarray

from sigmaepsilon.math.linalg import generalized_inverse
from sigmaepsilon.mesh.cellapproximator import LagrangianCellApproximator
from sigmaepsilon.mesh.typing import GeometryProtocol

from .utils.cells.approximator import _gauss_approximator


__all__ = ["LagrangianCellGaussApproximator"]


def _approximator(
    cls: GeometryProtocol,
    *,
    x_source: Iterable = None,
    shp_source_inverse: Iterable = None,
    values_source: Iterable = None,
    x_target: Iterable = None,
    **__
) -> Union[float, ndarray]:
    if shp_source_inverse is None:
        assert isinstance(x_source, Iterable)
        shp_source = cls.shape_function_values(x_source)  # (nP_source, nNE)
        shp_source_inverse = generalized_inverse(shp_source)

    if not isinstance(values_source, ndarray):
        values_source = np.array(values_source)

    shp_target = cls.shape_function_values(x_target)  # (nP_target, nNE)

    nE, _, nSTRE, nRHS = values_source.shape
    nP = shp_target.shape[0]
    result = np.zeros((nE, nP, nSTRE, nRHS))
    # FIXME swap axes for better performance
    _gauss_approximator(shp_target @ shp_source_inverse, values_source, result)
    return result


class LagrangianCellGaussApproximator(LagrangianCellApproximator):
    """
    An approximator for Lagrangian cells to approximate gauss cell data.
    """

    approximator_function: Callable = _approximator
