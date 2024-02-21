from .mesh import FemMesh

__all__ = ["MembraneMesh", "DrillingMembraneMesh"]


class MembraneMesh(FemMesh):
    """
    A data class dedicated to membranes with 2 degrees of
    freedom per node.
    """

    displacement_variables = ("UX", "UY")


class DrillingMembraneMesh(FemMesh):
    """
    A data class dedicated to drilling membranes with 3 degrees of
    freedom per node.
    """

    displacement_variables = ("UX", "UY", "ROTZ")
