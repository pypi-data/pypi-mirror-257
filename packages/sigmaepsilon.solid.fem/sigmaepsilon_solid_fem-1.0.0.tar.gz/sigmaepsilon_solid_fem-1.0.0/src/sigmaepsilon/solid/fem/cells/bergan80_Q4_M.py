from typing import Iterable, Union, Optional

import numpy as np
from numpy import ndarray, ascontiguousarray as ascont

from sigmaepsilon.math import atleast1d, atleast2d
from sigmaepsilon.mesh.cells import Q4
from sigmaepsilon.mesh.utils.numint import (
    Gauss_Legendre_Quad_1,
    Gauss_Legendre_Quad_4,
)

from ..data import MembraneFiniteElement
from ..data.finiteelement import Quadrature
from ..material import MembraneMaterial
from ..approximator import LagrangianCellGaussApproximator
from ..utils.postproc import approx_element_solution_bulk
from .utils.bergan80_Q4_M import (
    elastic_stiffness_matrix_bulk,
    nodal_displacement_pattern_vector_bulk,
    strain_displacement_matrix_bulk,
    shape_function_matrix_bulk,
)

__all__ = ["Q4_M_Bergan80"]


class Q4_M_Bergan80(MembraneFiniteElement):
    """
    Finite element class to handle 4-noded bilinear quadrilateral membranes,
    fabricated with the technique outlined in :cite:p:`Bergan1980FEMEOF`.

    The element comes in two flawours, according to the class attribute `mode`:
    * 0: standard isoparametric formulation
    * 1: incompatible rectangle suggested by Wilson et al. :cite:p:`Wilson1973IncompatibleDM`

    Note
    ----
    The element implicitly statisfies the patch test.
    """

    label = "Q4_M_Bergan80"
    mode = 0

    class Geometry(Q4.Geometry):
        ...

    class Material(MembraneMaterial):
        quadrature = {
            "full": Gauss_Legendre_Quad_4(),
            "selective": {(0, 1): "full", (2,): "reduced"},
            "reduced": Gauss_Legendre_Quad_1(),
            "stiffness": "full",
            "mass": "full",
        }

        @classmethod
        def shape_function_matrix(
            cls,
            parent: "Q4_M_Bergan80",
            x: Union[float, Iterable[float]],
            *_,
            **__,
        ) -> ndarray:  # (nE, nP, 3, 9)ű
            mode = parent.__class__.mode
            x = atleast2d(np.array(x), front=True)
            ec = parent.local_coordinates()
            Hrch = nodal_displacement_pattern_vector_bulk(ec, mode, invert=True)
            x_glob = parent.loc_to_glob(x, ec)
            return shape_function_matrix_bulk(Hrch, x_glob, mode)

        @classmethod
        def strain_displacement_matrix(
            cls,
            parent: "Q4_M_Bergan80",
            x: Iterable[float],
            *_,
            **__,
        ) -> ndarray:
            mode = parent.__class__.mode
            x = atleast2d(np.array(x), front=True)
            ec = parent.local_coordinates()
            Hrch = nodal_displacement_pattern_vector_bulk(ec, mode, invert=True)
            Hc = ascont(Hrch[:, 3:6, :])
            Hh = ascont(Hrch[:, 6:, :])
            del Hrch
            x_glob = parent.loc_to_glob(x, ec)
            return strain_displacement_matrix_bulk(ec, Hc, Hh, x_glob, mode)

    def __elastic_stiffness_matrix__(
        self: "Q4_M_Bergan80", q: Quadrature, ec: ndarray, D: ndarray
    ) -> ndarray:
        mode = self.__class__.mode
        qp, qw = atleast2d(q.pos), atleast1d(q.weight)
        Hrch = nodal_displacement_pattern_vector_bulk(ec, mode, invert=True)
        Hrc = ascont(Hrch[:, :6, :])
        Hh = ascont(Hrch[:, 6:, :])
        del Hrch
        dshp = self.Geometry.shape_function_derivatives(qp)
        jac = self.jacobian_matrix(dshp=dshp, ecoords=ec)
        djac = self.jacobian(jac=jac)
        x_glob = self.loc_to_glob(qp, ec)
        return elastic_stiffness_matrix_bulk(x_glob, D, Hrc, Hh, qw, djac, mode)

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
        quad = list(self._parse_gauss_data(self.Material.quadrature, "stiffness"))[0]
        B = self.Material.strain_displacement_matrix(self, quad.pos)
        # (nE, nG, nSTRE, nEVAB)
        dofsol = ascont(np.swapaxes(dofsol, 1, 2))  # (nE, nRHS, nEVAB)
        gauss_strains = approx_element_solution_bulk(dofsol, B)  # (nE, nRHS, nP, nSTRE)
        gauss_strains = ascont(np.moveaxis(gauss_strains, 1, -1))
        # (nE, nP, nSTRE, nRHS)
        # ------------------------ EXTRAPOLATE TO NODES ---------------------------
        nE, nP = len(dofsol), len(points)
        nSTRE = self.Material.number_of_material_variables
        nRHS = self.number_of_load_cases
        strains = np.zeros((nE, nP, nSTRE, nRHS), dtype=float)
        approximator = LagrangianCellGaussApproximator(Q4.Geometry)
        strains[:, :, quad.inds, :] += approximator(
            source=quad.pos, target=points, values=gauss_strains
        )[:, :, quad.inds, :]
        return strains
