from typing import Union, Optional

from numpy import ndarray
import numpy as np

from sigmaepsilon.math.linalg import ReferenceFrame
from sigmaepsilon.solid.material import ElasticityTensor, LinearElasticMaterial

from ..typing import FiniteElementProtocol
from .abstract import FiniteElementMaterial
from .utils.solid3d import (
    strain_displacement_matrix,
    HMH_3d_bulk_multi,
)

__all__ = ["Solid3dMaterial"]


class Solid3dMaterial(FiniteElementMaterial):
    """
    A linear material model for 3d solids.
    """

    displacement_variables = ("UX", "UY", "UZ")
    strain_variables = ("exx", "eyy", "ezz", "eyz", "exz", "exy")
    number_of_displacement_variables = 3
    number_of_material_variables = 6

    @classmethod
    def strain_displacement_matrix(
        cls,
        parent: FiniteElementProtocol,
        x: Optional[ndarray] = None,
        *,
        dshp: Optional[ndarray] = None,
        jac: Optional[ndarray] = None,
        **_,
    ) -> ndarray:
        """
        Calculates the strain displacement matrix for solids.

        Parameters
        ----------
        x: numpy.ndarray, Optional
            Locations of evaluation points. Either 'x' or
            both 'dshp' and 'jac' must be provided.
        parent: CellDataProtocol
            The parent celldata instance.
        dshp: numpy.ndarray, Optional
            Shape function derivatives evaluated at some points.
            Only required if 'x' is not provided.
        jac: numpy.ndarray
            Jacobian matrices evaluated at some points.
            Only required if 'x' is not provided.

        Returns
        -------
        numpy.ndarray
            An array of shape (nE, nP, nSTRE, nTOTV), where nE, nP
            nSTRE and nTOTV are the number of elements, evaulation
            points, stress components and total DOFs per element.
        """
        if dshp is None and x is not None:
            dshp = parent.Geometry.shape_function_derivatives(x)
        if jac is None:
            jac = parent.jacobian_matrix(dshp=dshp)
        return strain_displacement_matrix(dshp, jac)

    @classmethod
    def HMH(cls, stresses: ndarray) -> ndarray:
        """
        Evaluates the Huber-Mises-Hencky stress at multiple points
        of multiple cells.

        Parameters
        ----------
        stresses: numpy.ndarray, Optional
            Array of shape (nE, nP, nSTRE), where nE, nP and nSTRE
            are the number of elements, evaulation points and stress
            components. The stresses are expected in the order
            s11, s22, s33, s23, s13, s12.

        Returns
        -------
        numpy.ndarray
            An array of shape (nE, nP), where nE and nP are the
            number of elements and evaulation points.
        """
        return HMH_3d_bulk_multi(stresses)

    @classmethod
    def elastic_material_stiffness_matrix(
        cls,
        parent: FiniteElementProtocol,
        target: Optional[Union[str, ReferenceFrame]] = "local",
    ) -> ndarray:
        """
        Returns the elastic stiffness matrix in the desired frame.

        Parameters
        ----------
        parent: CellDataProtocol
            The parent celldata instance.
        target: ReferenceFrame, Optional
            A target frame in which the result should be returned.
            If it is a string, only "local" and "global" are accepted at
            the moment. Default is "local".
        """
        if isinstance(target, str) and target == "local":
            return parent.material_stiffness

        if isinstance(target, str):
            assert target == "global"
            target = parent.container.source().frame
        else:
            if not isinstance(target, ReferenceFrame):
                raise TypeError("'target' should be an instance of ReferenceFrame")

        source = ReferenceFrame(parent.frames)
        tensor = ElasticityTensor(
            parent.material_stiffness, frame=source, tensorial=False
        )
        return tensor.contracted_components(target=target)

    @classmethod
    def utilization(
        cls,
        parent: FiniteElementProtocol,
        *_,
        strains: Optional[Union[ndarray, None]] = None,
        stresses: Optional[Union[ndarray, None]] = None,
        squeeze: Optional[bool] = True,
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
        strains: numpy.ndarray, Optional
            1d or 2d array of strains such that the strains run along the last axis.
            The shape of this array determines the shape of the output in a straightforward
            manner.

        Note
        ----
        The returned result treats layers as iterables even if the case of one single layer.
        This shows in the shapes of output arrays and you will quickly find the logic behind it
        with minimal experimentation.
        """
        material = parent.material

        if not isinstance(material, LinearElasticMaterial):
            raise NotImplementedError

        result = material.utilization(
            strains=strains,
            stresses=stresses,
        )

        return result if not squeeze else np.squeeze(result)

    @classmethod
    def stresses(
        cls,
        parent: FiniteElementProtocol,
        *_,
        strains: Optional[Union[ndarray, None]] = None,
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
        squeeze: bool, Optional
            Whether to squeeze the reusulting array or not. Default is `True`.
        """
        material = parent.material

        if not isinstance(material, LinearElasticMaterial):
            raise NotImplementedError

        result = material.calculate_stresses(
            strains=strains,
        )

        return result if not squeeze else np.squeeze(result)
