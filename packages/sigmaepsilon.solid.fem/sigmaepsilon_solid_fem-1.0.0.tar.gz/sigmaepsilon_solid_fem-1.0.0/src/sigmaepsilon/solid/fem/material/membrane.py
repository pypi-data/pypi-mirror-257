from abc import abstractclassmethod

from numpy import ndarray

from .surface import FiniteElementSurfaceMaterial
from .utils.membrane import strain_displacement_matrix

__all__ = [
    "MembraneMaterial",
    "DrillingMembraneMaterial",
    "FictiveDrillingMembraneMaterial",
]


class MembraneMaterial(FiniteElementSurfaceMaterial):
    """
    A linear material model for membranes.
    """

    displacement_variables = ("UX", "UY")
    strain_variables = ("exx", "exy", "eyy")
    number_of_displacement_variables = 2
    number_of_material_variables = 3

    @classmethod
    def strain_displacement_matrix(
        cls,
        *_,
        dshp: ndarray,
        jac: ndarray,
        **__,
    ) -> ndarray:
        """
        Calculates the strain displacement matrix.

        Parameters
        ----------
        jac: ndarray, Optional
            The jacobian matrix as a float array of shape (nE, nP, 2, 2), evaluated for
            each point in each cell. Default is None.
        dshp: ndarray, Optional
            The shape function derivatives of the master element as a float array of
            shape (nE, nP, nS=3, nX), evaluated at a 'nP' number of points, for an 'nE'
            number of elements, 'nS' number of strain components and 'nX' number of total
            displacement variables.
            Default is None.
        """
        return strain_displacement_matrix(dshp, jac)


class DrillingMembraneMaterial(MembraneMaterial):
    """
    A linear material model for membranes with drilling degrees of freedom.
    """

    displacement_variables = ("UX", "UY", "ROTZ")
    strain_variables = ("exx", "exy", "eyy")
    number_of_displacement_variables = 3
    number_of_material_variables = 3

    @abstractclassmethod
    def strain_displacement_matrix(cls) -> ndarray:
        ...


class FictiveDrillingMembraneMaterial(MembraneMaterial):
    """
    A linear material model for membranes with fictitious drilling degrees of freedom.
    """

    displacement_variables = ("UX", "UY", "ROTZ")
    strain_variables = ("exx", "exy", "eyy")
    number_of_displacement_variables = 3
    number_of_material_variables = 3

    @classmethod
    def strain_displacement_matrix(
        cls,
        *_,
        dshp: ndarray,
        jac: ndarray,
        **__,
    ) -> ndarray:
        """
        Calculates the strain displacement matrix.

        Parameters
        ----------
        jac: ndarray, Optional
            The jacobian matrix as a float array of shape (nE, nP, 2, 2), evaluated for
            each point in each cell. Default is None.
        dshp: ndarray, Optional
            The shape function derivatives of the master element as a float array of
            shape (nE, nP, nS=3, nX), evaluated at a 'nP' number of points, for an 'nE'
            number of elements, 'nS' number of strain components and 'nX' number of total
            displacement variables.
            Default is None.
        """
        return strain_displacement_matrix(dshp, jac, 3)
    