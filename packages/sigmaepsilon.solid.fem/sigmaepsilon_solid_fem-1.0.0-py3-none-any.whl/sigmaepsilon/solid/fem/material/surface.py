from typing import Iterable, Optional, Union, Tuple
from numbers import Number

from numpy import ndarray

from sigmaepsilon.solid.material.surface.surface import SurfaceSection

from .abstract import FiniteElementMaterial
from ..typing import FiniteElementProtocol

__all__ = ["FiniteElementSurfaceMaterial"]


class FiniteElementSurfaceMaterial(FiniteElementMaterial):
    """
    Base class for finite element materials for surfaces.
    """

    @classmethod
    def utilization(
        cls,
        parent: FiniteElementProtocol,
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
        A function that returns a positive number. If the value is 1.0, it means that the material
        is at peak performance and any further increase in the loads is very likely to lead to failure
        of the material.

        The implementation should be able to cover the case if the input 'strains' is a 2d array.
        In that case, the strain values are expected to run along the last axis, hence the i-th
        item would be accessed as `strains[i]` and it would return a tuple of numbers, one for
        every strain component involved in the formulation of the material law.

        Parameters
        ----------
        strains: numpy.ndarray, Optional
            1d or 2d array of strains such that the strains run along the last axis.
            The shape of this array determines the shape of the output in a straightforward
            manner.
        stresses: numpy.ndarray, Optional
            1d or 2d NumPy array. Default is None
        z: float or None, Optional
            The signed normal distance from the reference surface of the body.
            If `None`, values for all points are returned, grouped by layers (see later).
            Use it in combination with the 'rng' parameter.
        rng: Tuple[Number, Number], Optional
            An interval that puts the value of 'z' to perspective. Otherwise specified, the
            value for the parameter 'z' is expected in the range [-1, 1].

        Note
        ----
        The returned result treats layers as iterables even if the case of one single layer.
        This shows in the shapes of output arrays and you will quickly find the logic behind it
        with minimal experimentation.
        """
        material = parent.material

        if not isinstance(material, SurfaceSection):
            raise NotImplementedError

        return material.utilization(
            strains=strains,
            stresses=stresses,
            z=z,
            rng=rng,
            squeeze=squeeze,
            ppl=ppl,
        )

    @classmethod
    def stresses(
        cls,
        parent: FiniteElementProtocol,
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
            1d or 2d NumPy array. Default is None
        z: Iterable[Number], Optional
            Points of evaluation. Default is None.
        rng: Iterable[Number], Optional
            The range in which 'z' is to be understood. Default is (-1, 1).
        squeeze: bool, Optional
            Whether to squeeze the reusulting array or not. Default is `True`.
        ppl: int, Optional
            Point per layer. Default is None.
        """
        material = parent.material

        if not isinstance(material, SurfaceSection):
            raise NotImplementedError

        return material.calculate_stresses(
            strains=strains,
            stresses=stresses,
            z=z,
            rng=rng,
            squeeze=squeeze,
            ppl=ppl,
        )
