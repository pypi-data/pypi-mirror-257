from typing import Iterable, Union, Optional

import numpy as np
from numpy import ndarray, ascontiguousarray as ascont

from sigmaepsilon.mesh.cells import T3
from sigmaepsilon.math import atleast2d
from sigmaepsilon.mesh.utils.numint import Gauss_Legendre_Tri_1

from ..data import PlateFiniteElement
from ..material import KirchhoffPlateMaterial
from .utils.t3_p_KL_eoff import (
    basic_elastic_stiffness_matrix_bulk,
    higher_order_elastic_stiffness_matrix_bulk,
    strain_displacement_matrix_bulk,
    shape_function_matrix_bulk,
)
from ..utils.postproc import approx_element_solution_bulk

__all__ = ["T3_P_KL_EOFF"]


class T3_P_KL_EOFF(PlateFiniteElement):
    """
    A 3-node, 9-dof Kirchhoff-Love plate bending element by Felippa and Bergan,
    based on an energy-orthogonal free formulation :cite:p:`Bergan1980FEMEOF`.
    """

    label = "T3_P_KL_EOFF"

    class Geometry(T3.Geometry):
        ...

    class Material(KirchhoffPlateMaterial):
        quadrature = {
            "full": Gauss_Legendre_Tri_1,
            "geometry": "full",
            "stiffness": "full",
        }

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
            return shape_function_matrix_bulk(ec, x)

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
            return strain_displacement_matrix_bulk(ec, x)

    def _elastic_stiffness_matrix_(
        self, *_, transform: Optional[bool] = True, **__
    ) -> ndarray:
        ec = self.local_coordinates()
        D = self.Material.elastic_material_stiffness_matrix(self)
        nE = ec.shape[0]
        res = np.zeros((nE, 9, 9), dtype=float)
        basic_elastic_stiffness_matrix_bulk(ec, D, res)
        higher_order_elastic_stiffness_matrix_bulk(ec, D, res, 1.0)
        return self._transform_coeff_matrix_(res) if transform else res

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
        B = self.Material.strain_displacement_matrix(self, points)
        # (nE, nG, nSTRE, nEVAB)
        dofsol = ascont(np.swapaxes(dofsol, 1, 2))  # (nE, nRHS, nEVAB)
        strains = approx_element_solution_bulk(dofsol, B)  # (nE, nRHS, nP, nSTRE)
        strains = ascont(np.moveaxis(strains, 1, -1))
        # (nE, nP, nSTRE, nRHS)
        return strains

    def _strain_load_vector_(self, values: ndarray) -> ndarray:
        if not np.sum(values) < 1e-8:
            raise NotImplementedError("This is not implemented.")

        nE = len(self)
        nNE = self.Geometry.number_of_nodes
        nRHS = self.number_of_load_cases
        nDOFN = self.container.number_of_displacement_variables
        nTOTV = nNE * nDOFN
        return np.zeros((nE, nTOTV, nRHS), dtype=float)
