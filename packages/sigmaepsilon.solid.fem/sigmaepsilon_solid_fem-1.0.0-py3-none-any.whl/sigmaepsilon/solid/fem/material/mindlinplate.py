from numpy import ndarray

from .surface import FiniteElementSurfaceMaterial
from .utils.mindlinplate import (
    strain_displacement_matrix,
    HMH,
)

__all__ = ["MindlinPlateMaterial"]


class MindlinPlateMaterial(FiniteElementSurfaceMaterial):
    """
    A linear material model for Mindlin-Reissner plates.
    """

    displacement_variables = ("UZ", "ROTX", "ROTY")
    strain_variables = ("kxx", "kyy", "kxy" "exz", "eyz")
    number_of_displacement_variables = 3
    number_of_material_variables = 5

    @classmethod
    def strain_displacement_matrix(
        cls,
        *_,
        shp: ndarray,
        dshp: ndarray,
        jac: ndarray,
        **__,
    ) -> ndarray:
        """
        Calculates the strain displacement matrix.

        Parameters
        ----------
        shp: numpy.ndarray
            Shape functions evaluated at some points. Default is None.
        jac: numpy.ndarray
            The jacobian matrix as a float array of shape (nE, nP, 1, 1), evaluated for
            each point in each cell. Default is None.
        dshp: numpy.ndarray
            The shape function derivatives of the master element as a float array of
            shape (nP, nNE, nDOF=6, 3), evaluated at a 'nP' number of points.
            Default is None.
        """
        return strain_displacement_matrix(shp, dshp, jac)

    @classmethod
    def HMH(cls, stresses: ndarray) -> ndarray:
        """
        Evaluates the Huber-Mises-Hencky stress.
        """
        return HMH(stresses)
