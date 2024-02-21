from typing import Union, Iterable, Optional, ClassVar, Callable

import numpy as np
from numpy import ndarray

from sigmaepsilon.math import atleast1d
from sigmaepsilon.math.utils import to_range_1d

from ..typing import FiniteElementProtocol
from .abstract import FiniteElementMaterial
from .utils.bernoulli import strain_displacement_matrix_bulk
from ..utils.cells.bernoulli import (
    shape_function_matrix_Bernoulli_bulk,
    global_shape_function_derivatives_Bernoulli_bulk as gdshpB,
)

__all__ = ["BernoulliBeamMaterial"]


class BernoulliBeamMaterial(FiniteElementMaterial):
    """
    A linear material model for Euler-Bernoulli beams.
    """

    displacement_variables = ("UX", "UY", "UZ", "ROTX", "ROTY", "ROTZ")
    strain_variables = ("exx", "kxx", "kyy", "kzz")
    number_of_displacement_variables = 6
    number_of_material_variables = 4

    shape_function_evaluator: ClassVar[Optional[Callable]] = None
    shape_function_derivative_evaluator: ClassVar[Optional[Callable]] = None

    @classmethod
    def shape_function_values(
        cls,
        parent: FiniteElementProtocol,
        pcoords: Union[float, Iterable[float]],
        *_,
        rng: Optional[Union[Iterable, None]] = None,
        lengths: Optional[Union[Iterable[float], None]] = None,
        **__,
    ) -> ndarray:
        """
        Evaluates the shape functions at the points specified by 'pcoords'.

        Parameters
        ----------
        parent: FiniteElement
            The parent celldata instance.
        pcoords: float or Iterable[float]
            Locations of the evaluation points.
        rng: Iterable, Optional
            The range in which the locations ought to be understood,
            typically [0, 1] or [-1, 1]. Default is [0, 1].
        lengths: Iterable, Optional
            The lengths of the beams in the block. Default is None.

        Returns
        -------
        numpy.ndarray
            The returned array has a shape of (nP, nNE=2, nDOF=6), where nP,
            nNE and nDOF stand for the number of evaluation points, nodes
            per element and number of degrees of freedom, respectively.
        """
        rng = np.array([-1, 1]) if rng is None else np.array(rng)
        pcoords = atleast1d(np.array(pcoords))
        pcoords = to_range_1d(pcoords, source=rng, target=[-1, 1])
        lengths = parent.measures() if lengths is None else lengths
        return cls.shape_function_evaluator(pcoords, lengths).astype(float)

    @classmethod
    def shape_function_matrix(
        cls,
        parent: FiniteElementProtocol,
        pcoords: Union[float, Iterable[float]] = None,
        *_,
        rng: Iterable = None,
        lengths: Iterable[float] = None,
        **__,
    ) -> ndarray:
        """
        Evaluates the shape function matrix at the points specified by 'pcoords'.

        Parameters
        ----------
        parent: FiniteElement
            The parent celldata instance.
        pcoords: float or Iterable
            Locations of the evaluation points.
        rng: Iterable, Optional
            The range in which the locations ought to be understood,
            typically [0, 1] or [-1, 1]. Default is [0, 1].

        Other Parameters
        ----------------
        These parameters are for advanced users and can be omitted.
        They are here only to avoid repeated evaulation of common quantities.

        lengths: Iterable, Optional
            The lengths of the beams in the block. Default is None.

        Returns
        -------
        numpy.ndarray
            The returned array has a shape of (nE, nP, nDOF, nDOF * nNE), where nE, nP,
            nNE and nDOF stand for the number of elements, evaluation points, nodes
            per element and number of degrees of freedom respectively.

        Notes
        -----
        The returned array is always 4 dimensional, even if there is only one
        evaluation point.
        """
        pcoords = atleast1d(np.array(pcoords))
        rng = np.array([-1.0, 1.0]) if rng is None else np.array(rng)
        pcoords = to_range_1d(pcoords, source=rng, target=[-1, 1])
        lengths = parent.measures() if lengths is None else lengths
        dshp = cls.shape_function_derivative_evaluator(pcoords, lengths)
        ecoords = parent.local_coordinates()
        jac = parent.jacobian_matrix(dshp=dshp, ecoords=ecoords)
        shp = cls.shape_function_values(parent, pcoords, rng=rng)
        gdshp = cls.shape_function_derivatives(parent, jac=jac, dshp=dshp)
        return shape_function_matrix_Bernoulli_bulk(shp, gdshp).astype(float)

    @classmethod
    def shape_function_derivatives(
        cls,
        parent: FiniteElementProtocol,
        pcoords: Union[float, Iterable[float]] = None,
        *_,
        rng: Iterable = None,
        jac: ndarray = None,
        dshp: ndarray = None,
        lengths: Iterable[float] = None,
        **__,
    ) -> ndarray:
        """
        Evaluates the shape function derivatives (up to third) at the points specified
        by 'pcoords'. The function either returns the derivatives on the master or the actual
        element, depending on the inputs.

        Valid combination of inputs are:

            * 'pcoords' and optionally 'jac' : this can be used to calculate the derivatives
              in both the global ('jac' is provided) and the master frame ('jac' is not provided).

            * 'dshp' and 'jac' : this combination can only be used to return the derivatives
              wrt. to the global frame.

        Parameters
        ----------
        parent: FiniteElement
            The parent celldata instance.
        pcoords: float or Iterable, Optional
            Locations of the evaluation points. Default is None.
        rng: Iterable, Optional
            The range in which the locations ought to be understood,
            typically [0, 1] or [-1, 1]. Only if 'pcoords' is provided.
            Default is [0, 1].
        lengths: Iterable, Optional
            The lengths of the beams in the block. Default is None.
        jac: Iterable, Optional
            The jacobian matrix as a float array of shape (nE, nP, 1, 1), evaluated for
            each point in each cell. Default is None.
        dshp: Iterable, Optional
            The shape function derivatives of the master element as a float array of
            shape (nP, nNE, nDOF=6, 3), evaluated at a 'nP' number of points.
            Default is None.

        Returns
        -------
        numpy.ndarray
            The returned array has a shape of (nE, nP, nNE=2, nDOF=6, 3), where nE, nP, nNE and
            nDOF stand for the number of elements, evaluation points, nodes per element and number
            of degrees of freedom, respectively. Number 3 refers to first, second and third
            derivatives.

        Notes
        -----
        The returned array is always 5 dimensional, independeltly from the number of cells or
        evaluation points.
        """
        if pcoords is not None:
            lengths = parent.measures() if lengths is None else lengths
            # calculate derivatives wrt. the parametric coordinates in the range [-1, 1]
            pcoords = atleast1d(np.array(pcoords))
            rng = np.array([-1.0, 1.0]) if rng is None else np.array(rng)
            pcoords = to_range_1d(pcoords, source=rng, target=[-1.0, 1.0])
            dshp = cls.shape_function_derivative_evaluator(pcoords, lengths)
            if jac is None:
                # return derivatives wrt. the master frame
                return dshp.astype(float)
            else:
                # return derivatives wrt. the global frame
                return gdshpB(dshp, jac).astype(float)
        elif dshp is not None and jac is not None:
            # return derivatives wrt. the local frame
            return gdshpB(dshp, jac).astype(float)

    @classmethod
    def strain_displacement_matrix(
        cls,
        parent: FiniteElementProtocol,
        x: Optional[Union[float, Iterable[float]]] = None,
        *,
        rng: Optional[Iterable] = None,
        jac: Optional[ndarray] = None,
        dshp: Optional[ndarray] = None,
        **_,
    ) -> ndarray:
        """
        Calculates the strain displacement matrix.

        Parameters
        ----------
        parent: FiniteElement
            The parent celldata instance.
        x: float or Iterable, Optional
            Locations of the evaluation points. Default is None.
        rng: Iterable, Optional
            The range in which the locations ought to be understood,
            typically [0, 1] or [-1, 1]. Only if 'x' is provided.
            Default is [0, 1].
        jac: numpy.ndarray, Optional
            The jacobian matrix as a float array of shape (nE, nP, 1, 1), evaluated for
            each point in each cell. Default is None.
        dshp: numpy.ndarray, Optional
            The shape function derivatives of the master element as a float array of
            shape (nP, nNE, nDOF=6, 3), evaluated at a 'nP' number of points.
            Default is None.
        """
        rng = np.array([-1, 1]) if rng is None else np.array(rng)
        gdshp = cls.shape_function_derivatives(parent, x, rng=rng, jac=jac, dshp=dshp)
        return strain_displacement_matrix_bulk(gdshp)
