from typing import Iterable, ClassVar, Optional, Protocol, runtime_checkable

from numpy import ndarray

__all__ = ["MaterialProtocol"]


@runtime_checkable
class MaterialProtocol(Protocol):
    """
    Protocol for Material classes.
    """

    displacement_variables: ClassVar[Iterable[str]]
    strain_variables: ClassVar[Iterable[str]]
    number_of_material_variables: ClassVar[int]
    number_of_displacement_variables: ClassVar[int]
    quadrature: ClassVar[dict]
    dofmap: ClassVar[Optional[Iterable[int]]] = None

    @classmethod
    def shape_function_values(cls) -> ndarray:
        """Evaluates the shape functions."""
        ...

    @classmethod
    def shape_function_matrix(cls) -> ndarray:
        """Evaluates the shape functions."""
        ...

    @classmethod
    def shape_function_derivatives(cls) -> ndarray:
        """Evaluates the shape function derivatives."""
        ...

    @classmethod
    def strain_displacement_matrix(cls) -> ndarray:
        """
        Calculates the strain displacement matrix.
        """
        ...

    @classmethod
    def elastic_material_stiffness_matrix(cls) -> ndarray:
        """
        Returns the elastic stiffness matrix.
        """
        ...

    @classmethod
    def utilization(cls) -> ndarray:
        """
        Calculates and returns utilizations.
        """
        ...
        
    @classmethod
    def stresses(cls) -> ndarray:
        """
        Calculates and returns material stresses.
        """
        ...
