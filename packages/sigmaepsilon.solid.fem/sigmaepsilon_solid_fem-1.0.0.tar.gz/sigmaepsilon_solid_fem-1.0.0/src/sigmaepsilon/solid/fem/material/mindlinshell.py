from numpy import ndarray

from .abstract import FiniteElementMaterial
from .utils.mindlinshell import (
    strain_displacement_matrix,
    HMH,
)

__all__ = ["MindlinShellMaterial"]


class MindlinShellMaterial(FiniteElementMaterial):
    """
    A linear material model for Mindlin-Reissner shells.
    """

    displacement_variables = ("UX", "UY", "UZ", "ROTX", "ROTY", "ROTZ")
    strain_variables = ("exx", "eyy", "ezz", "eyz", "exz", "kxx", "kyy", "kxy")
    number_of_displacement_variables = 6
    number_of_material_variables = 8

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
        shp: ndarray, Optional
            Shape functions evaluated at some points. Default is None.
        jac: ndarray, Optional
            The jacobian matrix as a float array of shape (nE, nP, 1, 1), evaluated for
            each point in each cell. Default is None.
        dshp: ndarray, Optional
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
