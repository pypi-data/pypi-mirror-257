from typing import Iterable, ClassVar, Optional, Union

from numpy import ndarray

from sigmaepsilon.core.meta import ABCMeta_Weak
from sigmaepsilon.math.linalg import ReferenceFrame

from ..typing import FiniteElementProtocol

__all__ = ["FiniteElementMaterial"]


class ABC_FemMaterial(metaclass=ABCMeta_Weak):
    """
    Helper class that provides a standard way to create an ABC using
    inheritance.
    """

    __slots__ = ()


class FiniteElementMaterial(ABC_FemMaterial):
    """
    A base class that implement the MaterialProtocol for finite elements.
    """

    displacement_variables: ClassVar[Iterable[str]]
    strain_variables: ClassVar[Iterable[str]]
    number_of_material_variables: ClassVar[int]
    number_of_displacement_variables: ClassVar[int]
    quadrature: ClassVar[Optional[dict]]
    qrule: ClassVar[str]
    dofmap: ClassVar[Optional[Iterable[int]]] = None

    @classmethod
    def shape_function_values(
        cls,
        parent: FiniteElementProtocol,
        x: Union[float, Iterable[float]],
        *,
        rng: Iterable = None,
    ) -> ndarray:
        return parent.Geometry.shape_function_values(x, rng=rng)

    @classmethod
    def shape_function_matrix(
        cls,
        parent: FiniteElementProtocol,
        x: Union[float, Iterable[float]],
        *,
        rng: Optional[Union[Iterable, None]] = None,
        N: Optional[Union[int, None]] = None,
    ) -> ndarray:
        if not N:
            N = cls.number_of_displacement_variables
        return parent.Geometry.shape_function_matrix(x, rng=rng, N=N)

    @classmethod
    def shape_function_derivatives(
        cls,
        parent: FiniteElementProtocol,
        x: Union[float, Iterable[float]],
        *,
        jac: ndarray = None,
        dshp: ndarray = None,
        rng: Iterable = None,
    ) -> ndarray:
        return parent.Geometry.shape_function_derivatives(
            x, jac=jac, dshp=dshp, rng=rng
        )

    @classmethod
    def elastic_material_stiffness_matrix(
        cls,
        parent: FiniteElementProtocol,
        *_,
        target: Optional[Union[str, ReferenceFrame]] = "local",
        **__,
    ) -> ndarray:
        """
        Returns the elastic stiffness matrix in the desired frame.

        Parameters
        ----------
        parent: FiniteElementProtocol
            The parent celldata instance.
        target: ReferenceFrame, Optional
            A target frame in which the result should be returned.
            If it is a string, only "local" and "global" are accepted at
            the moment. Default is "local".
        """
        if isinstance(target, str) and target == "local":
            return parent.material_stiffness
        else:
            raise NotImplementedError(
                "If a target frame is specified, it must be 'local'."
            )
            
    @classmethod
    def utilization(cls) -> ndarray:
        """
        Calculates utilization.
        """
        raise NotImplementedError
    
    @classmethod
    def stresses(cls) -> ndarray:
        """
        Calculates material strains.
        """
        raise NotImplementedError
