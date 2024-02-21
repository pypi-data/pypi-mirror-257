from .mesh import FemMesh


__all__ = ["SolidMesh"]


class SolidMesh(FemMesh):
    """
    A data class dedicated to simple 3d solid cells with 3 degrees of
    freedom per node.
    """

    displacement_variables = ("UX", "UY", "UZ")
