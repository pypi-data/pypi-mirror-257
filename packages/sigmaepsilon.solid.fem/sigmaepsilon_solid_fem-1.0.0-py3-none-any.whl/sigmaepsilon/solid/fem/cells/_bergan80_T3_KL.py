from typing import Iterable, Union, Optional

import numpy as np
from numpy import ndarray, ascontiguousarray as ascont

from sigmaepsilon.mesh.cells import T3, T6
from sigmaepsilon.math import atleast1d, atleast2d

from ..data import PlateFiniteElement
from ..data.finiteelement import Quadrature
from ..material import KirchhoffPlateMaterial
from .utils import (
    elastic_stiffness_matrix_bulk,
    nodal_displacement_pattern_vector_bulk,
    strain_displacement_matrix_bulk,
    shape_function_matrix_bulk,
)
from ..utils.postproc import approx_element_solution_bulk
from ..approximator import LagrangianCellGaussApproximator

__all__ = ["T3_P_KL_Bergan80"]


class T3_P_KL_Bergan80(PlateFiniteElement):
    """
    A 3-node, 9-dof Kirchhoff-Love plate bending element by Bergan, fabricated
    with the free formulation technique :cite:p:`Bergan1980FEMEOF`.

    Notes
    -----
    1) Concerns were raised in the past about the reliability of this element, but as
    it's pointed out by Bergan :cite:p:`Bergan1980FEMEOF`, the issues were caused by the
    origin of the coordinate system not being in the centers of the elements.
    2) The element implicitly statisfies the patch test.
    """

    label = "T3_P_KL_Bergan80"

    class Geometry(T3.Geometry):
        ...

    class Material(KirchhoffPlateMaterial):
        qrule = "full"
        quadrature = T6.Geometry.quadrature

        @classmethod
        def shape_function_matrix(
            cls,
            parent: PlateFiniteElement,
            x: Union[float, Iterable[float]],
            *_,
            **__,
        ) -> ndarray:  # (nE, nP, 3, 9)
            x = atleast2d(np.array(x), front=True)
            ec = parent.local_coordinates()
            Hrch = nodal_displacement_pattern_vector_bulk(ec, invert=True)
            return shape_function_matrix_bulk(ec, Hrch, x)

        @classmethod
        def strain_displacement_matrix(
            cls,
            parent: PlateFiniteElement,
            x: Iterable[float],
            *_,
            **__,
        ) -> ndarray:
            x = atleast2d(np.array(x), front=True)
            ec = parent.local_coordinates()
            Hrch = nodal_displacement_pattern_vector_bulk(ec, invert=True)
            Hc = ascont(Hrch[:, 3:6, :])
            Hh = ascont(Hrch[:, 6:, :])
            del Hrch
            return strain_displacement_matrix_bulk(ec, Hc, Hh, x)

    def __elastic_stiffness_matrix__(
        self, q: Quadrature, ec: ndarray, D: ndarray
    ) -> ndarray:
        qp, qw = atleast2d(q.pos), atleast1d(q.weight)
        Hrch = nodal_displacement_pattern_vector_bulk(ec, invert=True)
        Hrc = ascont(Hrch[:, :6, :])
        Hh = ascont(Hrch[:, 6:, :])
        del Hrch
        dshp = self.Geometry.shape_function_derivatives(q.pos)
        jac = self.jacobian_matrix(dshp=dshp, ecoords=ec)
        djac = self.jacobian(jac=jac)
        return elastic_stiffness_matrix_bulk(ec, D, Hrc, Hh, qp, qw, djac)

    def _strains_(
        self,
        *_,
        cells: Optional[Union[int, Iterable[int], None]] = None,
        points: Optional[Union[float, Iterable, None]] = None,
        **__,
    ) -> ndarray:
        # ---------------------- CALCULATE AT GAUSS POINTS ------------------------
        dofsol = self.dof_solution(flatten=True, cells=cells)
        # (nE, nEVAB, nRHS)
        quad = list(self._parse_gauss_data(self.Material.quadrature, "full"))[0]
        B = self.Material.strain_displacement_matrix(self, quad.pos)
        # (nE, nG, nSTRE, nEVAB)
        dofsol = ascont(np.swapaxes(dofsol, 1, 2))  # (nE, nRHS, nEVAB)
        gauss_strains = approx_element_solution_bulk(dofsol, B)  # (nE, nRHS, nP, nSTRE)
        gauss_strains = ascont(np.moveaxis(gauss_strains, 1, -1))
        # (nE, nP, nSTRE, nRHS)
        # ------------------------ EXTRAPOLATE TO NODES ---------------------------
        nE, nP = len(dofsol), len(points)
        nSTRE = self.Material.number_of_material_variables
        if len(self.pointdata.loads.shape) == 2:
            nRHS = 1
        else:
            nRHS = self.pointdata.loads.shape[-1]
        strains = np.zeros((nE, nP, nSTRE, nRHS), dtype=float)
        approximator = LagrangianCellGaussApproximator(T6.Geometry)
        strains[:, :, quad.inds, :] += approximator(
            source=quad.pos, target=points, values=gauss_strains
        )[:, :, quad.inds, :]
        return strains

    """def _internal_forces_(
        self,
        *_,
        cells: Union[int, Iterable[int]] = None,
        points: Union[float, Iterable] = None,
    ) -> ndarray:
        pass"""
