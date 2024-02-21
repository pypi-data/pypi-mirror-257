from sigmaepsilon.core.meta import ABCMeta_Weak

from .femdata import FemDataProtocol


__all__ = ["ABCMeta_FemMesh"]


class ABCMeta_FemMesh(ABCMeta_Weak):
    """
    Meta class for PointData and CellData classes.

    It merges attribute maps with those of the parent classes.

    """

    def __init__(self, name, bases, namespace, *args, **kwargs):
        super().__init__(name, bases, namespace, *args, **kwargs)

    def __new__(metaclass, name, bases, namespace, *args, **kwargs):
        cls: FemDataProtocol = super().__new__(
            metaclass, name, bases, namespace, *args, **kwargs
        )
        if hasattr(cls, "displacement_variables"):
            cls.number_of_displacement_variables = len(cls.displacement_variables)
        return cls


class ABC_FemMesh(metaclass=ABCMeta_FemMesh):
    """Helper class that provides a standard way to create an ABC using
    inheritance.
    """

    __slots__ = ()
