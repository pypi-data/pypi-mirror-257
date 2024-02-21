from typing import ClassVar, Callable, Iterable

import numpy as np
from numpy import ndarray

from sigmaepsilon.math import atleast2d

from .abstract import FiniteElementMaterial
from ..typing import FiniteElementProtocol

__all__ = ["KirchhoffPlateMaterial"]


class KirchhoffPlateMaterial(FiniteElementMaterial):
    """
    A linear material model for Mindlin-Reissner plates.
    """

    displacement_variables = ("UZ", "ROTX", "ROTY")
    strain_variables = ("kxx", "kyy", "kxy")
    number_of_displacement_variables = 3
    number_of_material_variables = 3

    shape_function_matrix_evaluator: ClassVar[Callable]
    strain_displacement_matrix_evaluator: ClassVar[Callable]
    shear_force_calculator: ClassVar[Callable]
    internal_force_calculator: ClassVar[Callable]

    switches = {"postproc-mode": "KL"}

    @classmethod
    def strain_displacement_matrix(
        cls,
        parent: FiniteElementProtocol,
        x: Iterable[float],
        *_,
        **__,
    ) -> ndarray:
        """
        Calculates the strain displacement matrix.

        Parameters
        ----------
        parent: CellDataProtocol
            The parent celldata instance.
        x: Iterable[float]
            Locations of one or more evaluation points in the master domain.

        Returns
        -------
        numpy.ndarray
            4d float array of shape (nE, nP, nSTRE=3, nNE*nDOF=12).
        """
        x = atleast2d(np.array(x), front=True)
        ec = parent.local_coordinates()
        points = parent.loc_to_glob(x, ec)  # (nE, nP, nD)
        return cls.strain_displacement_matrix_evaluator(points, ec)

    @classmethod
    def shape_function_matrix(
        cls,
        parent: FiniteElementProtocol,
        x: Iterable[float],
        *_,
        **__,
    ) -> ndarray:
        """
        Evaluates the shape function matrix at one or more points.

        Parameters
        ----------
        parent: FiniteElement
            The parent celldata instance.
        x: Iterable[float]
            Locations of one or more evaluation points in the master domain.

        Returns
        -------
        numpy.ndarray
            4d float array of shape (nE, nP, nDOF=3, nNE*nDOF=12).
        """
        x = atleast2d(np.array(x), front=True)
        ec = parent.local_coordinates()
        points = parent.loc_to_glob(x, ec)  # (nE, nP, nD)
        return cls.shape_function_matrix_evaluator(points, ec)
