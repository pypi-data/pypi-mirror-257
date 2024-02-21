"""
The ANDES template.
"""
from typing import Iterable, Optional, Union
from numbers import Number

import numpy as np
from numpy import ndarray

from sigmaepsilon.math.utils import repeat1d
from sigmaepsilon.mesh.cells import T3 as PolyCell

from ..typing import FiniteElementProtocol
from ..data import DrillingMembraneFiniteElement
from ..material import DrillingMembraneMaterial
from .utils.andes import (
    sig_ANDES,
    stiffness_matrix_ANDES,
    strain_displacement_matrix_ANDES,
)

__all__ = ["T3_ANDES", "T3_ALL88_3I", "T3_Opt_M"]


class T3_ANDES(DrillingMembraneFiniteElement):
    """
    The ANDES template of Carmelo Militello and Carlos A. Felippa.

    The template can be completed by inheriting from this class and providing
    a signature (an 1d iterable) to the new class as a class member. The class has
    a few built-in signatures, and they can be activated by specifying the 'version'
    class member.

    Example
    -------
    To reproduce the CST triangle, you would do this:

    >>> from sigmaepsilon.solid.fem.cells import T3_ANDES
    >>> class MyFiniteElement(T3_ANDES):
    >>>     signature = (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    The same by specifying the 'version' class member:

    >>> from sigmaepsilon.solid.fem.cells import T3_ANDES
    >>> class MyFiniteElement(T3_ANDES):
    >>>     version = "CST"

    References
    ----------
    .. [1] Carlos A. Felippa, A study of optimal membrane triangles with
       drilling freedoms, Computer Methods in Applied Mechanics and Engineering,
       Volume 192, Issues 16-18, 2003, Pages 2125-2168, ISSN 0045-7825,
       https://doi.org/10.1016/S0045-7825(03)00253-6.
    """

    label = "T3_ANDES"

    Geometry = PolyCell.Geometry

    version: Optional[Union[str, None]] = None
    signature: Optional[Union[Iterable[Number], None]] = None

    class Material(DrillingMembraneMaterial):
        qrule = "full"
        quadrature = {
            "full": (np.array([[1 / 3, 1 / 3]]), np.array([1 / 2])),
        }

        @classmethod
        def strain_displacement_matrix(
            cls,
            parent: FiniteElementProtocol,
            x: Iterable[float],
            *_,
            **__,
        ) -> ndarray:
            # FIXME : not tested, probably wrong
            ec = parent.local_coordinates()
            nE = ec.shape[0]

            sig = parent.__class__.signature
            if sig is None:
                sig = np.array(sig_ANDES(key=parent.version), dtype=float)
            sig = repeat1d(sig, nE).reshape(nE, 11)

            h = np.ones((nE), dtype=float)
            return strain_displacement_matrix_ANDES(x, ec, h, sig)

    def _elastic_stiffness_matrix_(
        self, *, transform: bool = True, **kwargs
    ) -> ndarray:
        ec = kwargs.get("_ec", self.local_coordinates())
        D = self.material_stiffness
        sig = np.array(sig_ANDES(key=self.version), dtype=float)
        sig = repeat1d(sig, D.shape[0]).reshape(D.shape[0], 11)
        h = np.ones((D.shape[0]), dtype=float)
        K = stiffness_matrix_ANDES(D, ec, h, sig)
        return self._transform_coeff_matrix_(K) if transform else K

    def _strain_load_vector_(self, values: ndarray) -> ndarray:
        # FIXME : returns a zero, but shape-correct array
        nE, _, nRHS = values.shape
        nNE = self.Geometry.number_of_nodes
        nDOF = self.Material.number_of_displacement_variables
        nodal_loads = np.zeros((nE, nNE * nDOF, nRHS))
        return nodal_loads  # (nE, nTOTV, nRHS)


class T3_ALL88_3I(T3_ANDES):
    """
    Allman 88 element integrated by 3-point interior rule, constructed
    using the ANDES template of Carmelo Militello and Carlos A. Felippa.

    References
    ----------
    .. [1] Carlos A. Felippa, A study of optimal membrane triangles with
       drilling freedoms, Computer Methods in Applied Mechanics and Engineering,
       Volume 192, Issues 16-18, 2003, Pages 2125-2168, ISSN 0045-7825,
       https://doi.org/10.1016/S0045-7825(03)00253-6.
    """

    label = "T3_ALL88_3I"
    Geometry = PolyCell.Geometry

    version = "ALL88-3I"


class T3_Opt_M(T3_ANDES):
    """
    The optimal 3-node bending triangle with corner rotations, constructed
    using the ANDES template of Carmelo Militello and Carlos A. Felippa.

    References
    ----------
    .. [1] Carlos A. Felippa, A study of optimal membrane triangles with
       drilling freedoms, Computer Methods in Applied Mechanics and Engineering,
       Volume 192, Issues 16-18, 2003, Pages 2125-2168, ISSN 0045-7825,
       https://doi.org/10.1016/S0045-7825(03)00253-6.
    """

    label = "T3_Opt_M"
    Geometry = PolyCell.Geometry

    version = "OPT"
