from sigmaepsilon.mesh.typing.abcpolycell import ABCMeta_PolyCell
from sigmaepsilon.mesh.typing import GeometryProtocol

from .finiteelement import FiniteElementProtocol as FEP
from .pointdata import PointDataProtocol as PDP
from .femdata import FemDataProtocol as FDP
from .material import MaterialProtocol

__all__ = ["ABC_FemCell"]


class ABCMeta_FemCell(ABCMeta_PolyCell):
    """
    Meta class for PointData and CellData classes.

    It merges attribute maps with those of the parent classes.
    """

    def __init__(self, name, bases, namespace, *args, **kwargs):
        super().__init__(name, bases, namespace, *args, **kwargs)

    def __new__(metaclass, name, bases, namespace, *args, **kwargs):
        cls: FEP[FDP, PDP] = super().__new__(
            metaclass, name, bases, namespace, *args, **kwargs
        )

        implements_material_protocol = False
        if namespace.get("Material", None):
            if not isinstance(cls.Material, MaterialProtocol):
                raise TypeError(
                    f"The attached material class {cls.Material} of {cls} "
                    "does not implement MaterialProtocol"
                )
            else:
                implements_material_protocol = True
                dofs = getattr(cls.Material, "displacement_variables", None)
                if dofs:
                    cls.Material.number_of_displacement_variables = len(dofs)

        if namespace.get("Geometry", None):
            if not isinstance(cls.Geometry, GeometryProtocol):
                raise TypeError(
                    f"The attached geometry class {cls.Geometry} of {cls} "
                    "does not implement GeometryProtocol"
                )
            else:
                if implements_material_protocol:
                    cls.Geometry.number_of_nodal_variables = (
                        cls.Material.number_of_displacement_variables
                    )

        return cls


class ABC_FemCell(metaclass=ABCMeta_FemCell):
    """Helper class that provides a standard way to create an ABC using
    inheritance.
    """

    __slots__ = ()
