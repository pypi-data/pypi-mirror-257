from typing import TypeVar, Generic, Iterable, Optional, Union, Tuple
from numbers import Number

from numpy import ndarray, arange
import numpy as np
import xarray as xr

from .finiteelement import FiniteElement
from ..typing import (
    FemDataProtocol,
    PointDataProtocol,
)

__all__ = ["SurfaceFiniteElement"]


FD = TypeVar("FD", bound=FemDataProtocol)
PD = TypeVar("PD", bound=PointDataProtocol)


class SurfaceFiniteElement(Generic[FD, PD], FiniteElement[FD, PD]):
    """
    Base class for surface finite elements.
    """

    def material_stresses(
        self,
        *_,
        strains: Optional[Union[ndarray, None]] = None,
        stresses: Optional[Union[ndarray, None]] = None,
        z: Optional[Union[Number, Iterable[Number], None]] = None,
        rng: Optional[Tuple[Number, Number]] = (-1.0, 1.0),
        squeeze: Optional[bool] = True,
        ppl: Optional[Union[int, None]] = None,
        **__,
    ) -> ndarray:
        """
        Calculates material stresses for input internal forces or strains
        and returns it as a NumPy array.

        Either strains or stresses must be provided.

        If the points of evaluation are not explivitly specified with the parameter 'z',
        results are calculated at a default number of points per every layer.

        Parameters
        ----------
        strains: numpy.ndarray, Optional
            1d or 2d NumPy array. Default is None.
        stresses: numpy.ndarray, Optional
            1d or 2d NumPy array. Default is None.
        z: Iterable[Number], Optional
            Points of evaluation. Default is None.
        rng: Iterable[Number], Optional
            The range in which 'z' is to be understood. Default is (-1, 1).
        squeeze: bool, Optional
            Whether to squeeze the reusulting array or not. Default is `True`.
        ppl: int, Optional
            Point per layer. Default is None.
        """
        return self.Material.stresses(
            self,
            strains=strains,
            stresses=stresses,
            z=z,
            rng=rng,
            squeeze=squeeze,
            ppl=ppl,
        )

    def utilization(
        self,
        *_,
        cells: Optional[Union[int, Iterable[int], None]] = None,
        rng: Optional[Tuple[Number, Number]] = (-1.0, 1.0),
        points: Optional[Union[float, Iterable, None]] = None,
        z: Optional[Union[Number, Iterable[Number], None]] = None,
        ppl: Optional[Union[int, None]] = None,
        dtype: type = xr.DataArray,
        **__,
    ) -> Union[xr.DataArray, ndarray]:
        """
        Calculates and returns utilizations. If the value is 1.0, it means that the material
        is at peak performance and any further increase in the loads is very likely to lead to failure
        of the material.

        Parameters
        ----------
        points: float or Iterable[float], Optional
            Points of evaluation. If provided, it is assumed that the given values
            are wrt. the range [0, 1], unless specified otherwise with the 'rng'
            parameter. If not provided, results are returned for the nodes of the
            selected elements. Default is None.
        cells: int or Iterable[int], Optional
            Indices of cells. If not provided, results are returned for all cells.
            Default is None.
        z: float or None, Optional
            The signed normal distance from the reference surface of the body.
            If `None`, values for all points are returned, grouped by layers (see later).
            Use it in combination with the 'rng' parameter.
        rng: Tuple[Number, Number], Optional
            An interval that puts the value of 'z' to perspective. Otherwise specified, the
            value for the parameter 'z' is expected in the range [-1, 1].
        ppl: int, Optional
            Point per layer. Default is None.
        """
        strains_fem = self.strains(cells=cells, points=points, flatten=False)
        num_cells, num_points, num_components, num_loads = strains_fem.shape
        strains_fem = np.moveaxis(strains_fem, -2, -1)
        strains_fem = strains_fem.reshape(
            num_cells * num_points * num_loads, num_components
        )

        # result = np.ones((strains_fem.shape[0], len(z)), dtype=float)
        result = self.Material.utilization(
            self,
            strains=strains_fem,
            z=z,
            rng=rng,
            squeeze=False,
            ppl=ppl,
        ).values

        if z is None:
            assert len(result.shape) == 3
            _, num_layers, num_point_per_layer = result.shape
            result = result.reshape(
                num_cells, num_points, num_loads, num_layers, num_point_per_layer
            )
            result = np.moveaxis(result, 2, -1)
            coords = [
                arange(num_cells),
                arange(num_points),
                arange(num_layers),
                arange(num_point_per_layer),
                arange(num_loads),
            ]
            dims = ["index", "ppc", "layer", "ppl", "case"]
        else:
            assert len(result.shape) == 2
            _, num_z = result.shape
            result = result.reshape(num_cells, num_points, num_loads, num_z)
            result = np.moveaxis(result, 2, -1)
            coords = [
                arange(num_cells),
                arange(num_points),
                arange(num_z),
                arange(num_loads),
            ]
            dims = ["index", "ppc", "ppz", "case"]

        if dtype == xr.DataArray:
            return xr.DataArray(result, coords=coords, dims=dims)
        elif dtype == ndarray:
            return result
        else:
            raise NotImplementedError(f"Invalid type: {dtype}")
