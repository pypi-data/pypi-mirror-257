from sigmaepsilon.mesh.config import __hasplotly__, __hasmatplotlib__

from .mesh import FemMesh

__all__ = ["SurfaceMesh"]


class SurfaceMesh(FemMesh):
    """
    A data class dedicated to 2d cells. It handles sections and other line
    related information, presets for plotting, etc.

    """

    def __init__(self, *args, section=None, **kwargs):
        if section is not None:
            pass
        self._section = section
        super().__init__(*args, **kwargs)

    @property
    def section(self):
        if self._section is not None:
            return self._section
        else:
            if self.is_root():
                return self._section
            else:
                return self.parent.section
