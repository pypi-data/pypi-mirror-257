from typing import Union, Iterable, Optional
from functools import partial

import numpy as np
from numpy import ndarray

from sigmaepsilon.math import atleast2d, atleastnd, ascont
from sigmaepsilon.math.linalg import ReferenceFrame

from ..data import FiniteElement
from ..utils.postproc import (
    approx_element_solution_bulk,
    calculate_internal_forces_bulk,
)
from ..utils.utils import expand_shape_function_matrix
from ..approximator import LagrangianCellGaussApproximator
from ..material.utils.mindlinplate import strain_displacement_matrix as sdm_mindlin

__all__ = ["KirchhoffPlateElement"]


class KirchhoffPlateElement(FiniteElement):
    """
    Finite element class to handle 4-noded bilinear quadrilateral
    Kirchhoff-Love plates.
    """

    standalone = True

    def _strains_(
        self,
        *_,
        cells: Optional[Union[int, Iterable[int], None]] = None,
        points: Optional[Union[float, Iterable, None]] = None,
        extrapolate: Optional[bool] = False,
        **__,
    ) -> ndarray:
        dofsol = self.dof_solution(flatten=True, cells=cells)
        # (nE, nEVAB, nRHS)
        # we swap axes so that vectorial axis is the last -> this makes
        # for fast matrix operations when transforming between frames,
        # see the gauss evaluator function `self.__internal_forces__`
        dofsol = ascont(np.swapaxes(dofsol, 1, 2))  # (nE, nRHS, nEVAB)

        postprod_mode = self.Material.switches["postproc-mode"]
        if postprod_mode == "KL":
            gauss_evaluator_fnc = self._gauss_strains_kirchhoff_
        elif postprod_mode == "UM":
            gauss_evaluator_fnc = self._gauss_strains_mindlin_
        else:
            raise NotImplementedError

        gauss_evaluator = partial(
            gauss_evaluator_fnc,
            cells=cells,
            dofsol=dofsol,
        )

        points = atleast2d(np.array(points), front=True)

        if not extrapolate:
            return gauss_evaluator(points=points)
        else:
            nE = len(dofsol)
            nP = len(points)
            nSTRE = self.Material.number_of_material_variables
            nRHS = self.number_of_load_cases

            # allocate result
            strains = np.zeros((nE, nP, nSTRE, nRHS), dtype=float)

            # calculate at Gauss points
            for q in self._parse_gauss_data(self.Material.quadrature, "stiffness"):
                approximator = LagrangianCellGaussApproximator(self.Geometry)
                strains[:, :, q.inds, :] += approximator(
                    source=q.pos, target=points, values=gauss_evaluator(points=q.pos)
                )[:, :, q.inds, :]

        return strains

    def _gauss_strains_kirchhoff_(
        self,
        *,
        dofsol: ndarray,  # (nE, nRHS, nNE * nDOF)
        points: Iterable[float],
        cells: Iterable[int],
    ) -> ndarray:  # (nE, nP, nSTRE, nRHS)
        B = self.Material.strain_displacement_matrix(self, points)[cells]
        # (nE, nP, nSTRE, nNODE * nDOFN)
        strains = approx_element_solution_bulk(dofsol, B)  # (nE, nRHS, nP, nSTRE)
        strains = ascont(np.moveaxis(strains, 1, -1))  # (nE, nP, nSTRE, nRHS)
        return strains

    def _gauss_strains_mindlin_(
        self,
        *,
        dofsol: ndarray,  # (nE, nRHS, nNE * nDOF)
        points: Iterable[float],
        cells: Iterable[int],
    ) -> ndarray:
        shp = self.Geometry.shape_function_values(points)[cells]
        dshp = self.Geometry.shape_function_derivatives(points)[cells]
        ecoords = self.local_coordinates()[cells]
        jac = self.jacobian_matrix(dshp=dshp, ecoords=ecoords)
        B = sdm_mindlin(shp, dshp, jac)
        # (nE, nP, nSTRE, nNODE * nDOFN)
        strains = approx_element_solution_bulk(dofsol, B)  # (nE, nRHS, nP, nSTRE)
        strains = ascont(np.moveaxis(strains, 1, -1)[:, :, :3, :])
        # (nE, nP, nSTRE, nRHS)
        return strains

    def _internal_forces_(self, *args, **kwargs) -> ndarray:
        # calculate shear forces
        postprod_mode = self.Material.switches["postproc-mode"]
        if postprod_mode == "KL":
            internal_force_evaluator = self._internal_forces_kirchhoff_
        elif postprod_mode == "UM":
            internal_force_evaluator = self._internal_forces_mindlin_
        else:
            raise NotImplementedError
        forces = internal_force_evaluator(*args, **kwargs)
        # forces -> (nE, nRHS, nP, nSTRE)
        forces = ascont(np.moveaxis(forces, 1, -1))
        # forces -> (nE, nP, nSTRE, nRHS)
        return forces

    def _internal_forces_kirchhoff_(
        self, *, points: ndarray, cells: Iterable[int], **kwargs
    ) -> ndarray:
        points = atleast2d(np.array(points), front=True)

        # calculate strains
        strains = self.strains(cells=cells, points=points, **kwargs)
        # (nE, nP, nSTRE, nRHS)
        strains = ascont(np.moveaxis(strains, -1, 1))  # (nE, nRHS, nP, nSTRE)
        strains -= self.kinetic_strains(points=points, cells=cells)

        # calculate moments
        D = self.Material.elastic_material_stiffness_matrix(self)[cells]
        nE, nRHS, nP, _ = strains.shape
        forces = np.zeros((nE, nRHS, nP, 5), dtype=float)
        inds = np.array([0, 1, 2], dtype=int)
        calculate_internal_forces_bulk(strains, D, forces, inds)
        # forces -> (nE, nRHS, nP, nSTRE)
        del strains

        # approximate body loads
        loads = self._get_body_loads(return_zeroes=True)
        loads = atleastnd(loads, 4, back=True)
        # (nE, nNE, nDOF, nRHS)
        nE, nNE, nDOF, nRHS = loads.shape
        loads = loads.reshape(nE, nNE * nDOF, nRHS)
        # (nE, nNE * nDOF, nRHS)
        loads = ascont(np.moveaxis(loads, 1, -1))
        # (nE, nRHS, nNE * nDOF)
        N = self.Geometry.shape_function_matrix(points, N=3)[cells]
        N = expand_shape_function_matrix(self, N)
        loads = approx_element_solution_bulk(loads, N)
        # (nE, nRHS, nP, nDOF)

        # calculate shear forces
        dofsol = self.dof_solution(flatten=True, cells=cells)
        # (nE, nEVAB, nRHS)
        dofsol = ascont(np.moveaxis(dofsol, 1, -1))
        # (nE, nRHS, nEVAB)
        ec = self.local_coordinates()[cells]
        points = self.loc_to_glob(points, ec)  # (nE, nP, nD)

        Material = self.__class__.Material
        Material.shear_force_calculator(loads, dofsol, D, points, ec, forces)

        return forces  # (nE, nRHS, nP, nSTRS=5)

    def _internal_forces_mindlin_(
        self, *, points: ndarray, cells: Iterable[int], **kwargs
    ) -> ndarray:
        points = atleast2d(np.array(points), front=True)

        # calculate internal forces at the nodes of the elements
        mc = self.Geometry.master_coordinates()
        forces = self._internal_forces_kirchhoff_(points=mc, cells=cells, **kwargs)
        # forces: (nE, nRHS, nP, nSTRE)

        # recalculate shear forces at the nodes
        shp = self.Geometry.shape_function_values(points)[cells]
        dshp = self.Geometry.shape_function_derivatives(points)[cells]
        ecoords = self.local_coordinates()[cells]
        jac = self.jacobian_matrix(dshp=dshp, ecoords=ecoords)
        loads = self._get_body_loads(return_zeroes=True)
        loads = atleastnd(loads, 4, back=True)
        # (nE, nNE, nDOF, nRHS)

        Material = self.__class__.Material
        Material.internal_force_calculator(loads, forces, shp, dshp, jac)

        return forces  # (nE, nRHS, nP, nSTRS=5)

    def _transform_internal_forces_(
        self,
        forces: ndarray,  # (nE, nP, nSTRE, nRHS)
        *,
        target: Union[str, ReferenceFrame] = "local",
        **_,
    ) -> ndarray:
        if target is not None:
            if isinstance(target, str) and target == "local":
                return forces
            else:
                raise NotImplementedError
        return forces
