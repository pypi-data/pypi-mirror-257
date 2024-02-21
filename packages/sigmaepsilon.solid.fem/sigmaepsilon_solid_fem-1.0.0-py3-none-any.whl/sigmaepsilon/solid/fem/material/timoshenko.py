from typing import Union, Iterable, Optional

import numpy as np
from numpy import ndarray

from sigmaepsilon.math.utils import to_range_1d

from ..typing import CellDataProtocol
from .abstract import FiniteElementMaterial
from .utils.timoshenko import strain_displacement_matrix_bulk

__all__ = ["TimoshenkoBeamMaterial"]


class TimoshenkoBeamMaterial(FiniteElementMaterial):
    """
    A linear material model for Timoshenko-Ehrenfest beams.
    """

    displacement_variables = ("UX", "UY", "UZ", "ROTX", "ROTY", "ROTZ")
    strain_variables = ("exx", "exy", "exz", "kxx", "kyy", "kzz")
    number_of_displacement_variables = 6
    number_of_material_variables = 6

    @classmethod
    def strain_displacement_matrix(
        cls,
        parent: CellDataProtocol,
        x: Optional[Union[float, Iterable[float], None]] = None,
        *_,
        rng: Optional[Union[Iterable, None]] = None,
        jac: Optional[Union[ndarray, None]] = None,
        shp: Optional[Union[ndarray, None]] = None,
        dshp: Optional[Union[ndarray, None]] = None,
        **__,
    ) -> ndarray:
        """
        Calculates the strain displacement matrix.

        Parameters
        ----------
        parent: CellDataProtocol
            The parent celldata instance.
        x: float or Iterable, Optional
            Locations of the evaluation points. Default is None.
        rng: Iterable, Optional
            The range in which the locations ought to be understood,
            typically [0, 1] or [-1, 1]. Only if 'x' is provided.
            Default is [0, 1].
        jac: ndarray, Optional
            The jacobian matrix as a float array of shape (nE, nP, 1, 1), evaluated for
            each point in each cell. Default is None.
        shp: ndarray, Optional
            Shape functions evaluated at some points. Default is None.
        dshp: ndarray, Optional
            The shape function derivatives of the master element as a float array of
            shape (nP, nNE, nDOF=6, 3), evaluated at a 'nP' number of points.
            Default is None.
        """
        rng = np.array([-1, 1]) if rng is None else np.array(rng)
        if x is not None:
            _rng = [-1, 1]
            x = to_range_1d(x, source=rng, target=_rng).flatten()
            rng = _rng
        if shp is None and x is not None:
            shp = parent.Geometry.shape_function_values(x, rng=rng)
        gdshp = parent.Geometry.shape_function_derivatives(
            x, rng=rng, jac=jac, dshp=dshp
        )
        return strain_displacement_matrix_bulk(shp, gdshp)
