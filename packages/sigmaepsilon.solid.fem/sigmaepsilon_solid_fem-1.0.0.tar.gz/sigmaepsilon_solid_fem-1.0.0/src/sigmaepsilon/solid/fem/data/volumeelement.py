from typing import TypeVar, Generic, Iterable, Optional, Union

from numpy import ndarray, arange
import numpy as np
import xarray as xr

from .finiteelement import FiniteElement
from ..typing import (
    FemDataProtocol,
    PointDataProtocol,
)

__all__ = ["VolumeFiniteElement"]


FD = TypeVar("FD", bound=FemDataProtocol)
PD = TypeVar("PD", bound=PointDataProtocol)


class VolumeFiniteElement(Generic[FD, PD], FiniteElement[FD, PD]):
    """
    Base class for surface finite elements.
    """

    def material_stresses(
        self,
        *_,
        strains: Optional[Union[ndarray, None]] = None,
        stresses: Optional[Union[ndarray, None]] = None,
        squeeze: Optional[bool] = True,
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
        squeeze: bool, Optional
            Whether to squeeze the reusulting array or not. Default is `True`.
        """
        return self.Material.stresses(
            self,
            strains=strains,
            stresses=stresses,
            squeeze=squeeze,
        )

    def utilization(
        self,
        *_,
        cells: Optional[Union[int, Iterable[int], None]] = None,
        points: Optional[Union[float, Iterable, None]] = None,
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
        """
        strains_fem = self.strains(cells=cells, points=points, flatten=False)
        num_cells, num_points, num_components, num_loads = strains_fem.shape
        strains_fem = np.moveaxis(strains_fem, -2, -1)
        strains_fem = strains_fem.reshape(
            num_cells * num_points * num_loads, num_components
        )
        
        result = self.Material.utilization(
            self,
            strains=strains_fem,
            squeeze=False,
        ).values
        
        result = result.reshape(num_cells, num_points, num_loads)
        
        if dtype == xr.DataArray:
            coords = [
                arange(num_cells),
                arange(num_points),
                arange(num_loads),
            ]
            dims = ["index", "point", "case"]
            return xr.DataArray(result, coords=coords, dims=dims)
        elif dtype == ndarray:
            return result
        else:
            raise NotImplementedError(f"Invalid type: {dtype}")
    