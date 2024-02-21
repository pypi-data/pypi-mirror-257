from typing import Iterable, Union, Optional
from numbers import Number

from numpy import ndarray
import numpy as np

from sigmaepsilon.math import ascont
from sigmaepsilon.mesh.cells import Q4 as PolyCell, Q8
from sigmaepsilon.mesh.utils.numint import Gauss_Legendre_Quad_4
from sigmaepsilon.mesh.utils.topology.tr import Q4_to_Q8
from sigmaepsilon.mesh.utils import jacobian_matrix_bulk, points_of_cells

from ..data import DrillingMembraneFiniteElement
from ..material import DrillingMembraneMaterial, MembraneMaterial
from .utils.cook import tr_strain_displacement_matrices, tr_shape_function_matrices

__all__ = ["Q4_M_Cook"]


class Q4_M_Cook(DrillingMembraneFiniteElement):
    """
    Finite element class to handle 4-noded Cook quadrilaterals.
    """

    label = "Q4_M_Cook"

    Geometry = PolyCell.Geometry

    class Material(DrillingMembraneMaterial):
        quadrature = {
            "full": Gauss_Legendre_Quad_4,
            "stiffness": "full",
        }

        @classmethod
        def strain_displacement_matrix(
            cls,
            parent: "Q4_M_Cook",
            x: Iterable[float],
            *_,
            return_djac: Optional[bool] = False,
            **__,
        ) -> ndarray:  # B (nE, nG, nSTRE, nNODE * nDOF)
            dshp = Q8.Geometry.shape_function_derivatives(x)
            jac = parent.jacobian_matrix(pcoords=x, dshp=dshp)
            B = MembraneMaterial.strain_displacement_matrix(dshp=dshp, jac=jac)
            coords, topo = Q4_to_Q8(
                parent.source_coords(), parent.topology().to_numpy()
            )
            ec = points_of_cells(
                coords, topo, local_axes=parent.frames, centralize=True
            )
            B = tr_strain_displacement_matrices(B, ec)
            if return_djac:
                return B, np.linalg.det(jac)
            else:
                return B

        @classmethod
        def shape_function_matrix(
            cls,
            parent: "Q4_M_Cook",
            x: Union[float, Iterable[Number]],
            *,
            rng: Optional[Union[Iterable[Number], None]] = None,
            N: Optional[Union[int, None]] = None,
        ) -> ndarray:  # (nE, nP, nDOF, 12)
            if not N:
                N = cls.number_of_displacement_variables
            coords, topo = Q4_to_Q8(
                parent.source_coords(), parent.topology().to_numpy()
            )
            ec = points_of_cells(
                coords, topo, local_axes=parent.frames, centralize=True
            )
            shpm = Q8.Geometry.shape_function_matrix(x, rng=rng, N=2)
            return tr_shape_function_matrices(shpm, ec)

    def __strain_displacement_matrix__(
        self,
        x: Iterable[Number],
        _,
        return_djac: Optional[bool] = False,
    ) -> ndarray:  # B (nE, nG, nSTRE, nNODE * nDOF)
        return self.Material.strain_displacement_matrix(
            self, x, return_djac=return_djac
        )

    def jacobian_matrix(
        self, *, pcoords: Optional[Union[Iterable[Number], None]] = None, **__
    ) -> ndarray:
        """
        Returns the jacobian matrices of the cells in the block. The evaluation
        of the matrix is governed by the inputs in the following way:
        - if `dshp` is provided, it must be a matrix of shape function derivatives
          evaluated at the desired locations
        - the desired locations are specified through `pcoords`

        Parameters
        ----------
        pcoords: Iterable[float], Optional
            Locations of the evaluation points.

        Returns
        -------
        numpy.ndarray
            A 4d array of shape (nE, nP, nD=2, nD=2), where nE, nP and nD
            are the number of elements, evaluation points and spatial
            dimensions. The number of evaluation points in the output
            is governed by the parameter 'dshp' or 'pcoords'.
        """
        dshp = Q8.Geometry.shape_function_derivatives(pcoords)
        coords, topo = Q4_to_Q8(self.source_coords(), self.topology().to_numpy())
        ec = points_of_cells(coords, topo, local_axes=self.frames, centralize=True)
        ec = ascont(ec[:, :, :2])
        return jacobian_matrix_bulk(dshp, ec)
