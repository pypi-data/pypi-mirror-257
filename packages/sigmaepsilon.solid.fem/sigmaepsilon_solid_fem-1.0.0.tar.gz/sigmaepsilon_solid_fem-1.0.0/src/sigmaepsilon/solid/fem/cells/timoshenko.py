from typing import Iterable, Union, Optional
from functools import partial

import numpy as np
from numpy import ndarray, ascontiguousarray as ascont

from sigmaepsilon.mesh.geometry import PolyCellGeometry1d
from sigmaepsilon.mesh.cells import L2, L3

from ..typing import (
    FemDataProtocol as FD,
    PointDataProtocol as PD,
)
from ..data import FiniteElement
from ..numint import Quadrature
from ..utils.postproc import (
    approx_element_solution_bulk,
    calculate_internal_forces_bulk,
)
from ..approximator import LagrangianCellGaussApproximator


__all__ = ["TimoshenkoBase"]


class TimoshenkoBase(FiniteElement[FD, PD]):
    """
    Base class for 1d finite elements, whose bending behaviour
    is governed by the Timoshenko-Ehrenfest beam theory. The implementations
    covered by this class are independent of the number of nodes of the cells.
    Specification of an actual finite element consists of specifying class
    level attributes only.

    See also
    --------
    :class:`~sigmaepsilon.solid.fem.cells.T2`
    :class:`~sigmaepsilon.solid.fem.cells.T3`
    """

    def _internal_forces_(
        self,
        *,
        cells: Optional[Union[int, Iterable[int], None]] = None,
        points: Optional[Union[float, Iterable, None]] = None,
    ) -> ndarray:
        strains = self._strains_(cells=cells, points=points)  # (nE, nP, nSTRE, nRHS)
        strains = ascont(np.moveaxis(strains, -1, 1))  # (nE, nRHS, nP, nSTRE)
        strains -= self.kinetic_strains(points=points)[cells]

        material = self.Material.elastic_material_stiffness_matrix(self)[cells]

        forces = np.zeros_like(strains)
        inds = np.arange(forces.shape[-1])
        calculate_internal_forces_bulk(
            strains, material, forces, inds
        )  # (nE, nRHS, nP, nSTRE)
        forces = ascont(np.moveaxis(forces, 1, -1))  # (nE, nP, nSTRE, nRHS)

        return forces

    def _strains_(
        self,
        *,
        cells: Optional[Union[int, Iterable[int], None]] = None,
        points: Optional[Union[float, Iterable, None]] = None,
        **_,
    ) -> ndarray:
        dofsol = self.dof_solution(flatten=True, cells=cells)  # (nE, nNE * nDOF, nRHS)
        # we swap axes so that vectorial axis is the last -> this makes
        # for fast matrix operations when transforming between frames,
        # see the gauss evaluator function `self.__internal_forces__`
        dofsol = ascont(np.swapaxes(dofsol, 1, 2))  # (nE, nRHS, nEVAB)

        ecoords = self.local_coordinates()[cells]

        nE = len(dofsol)
        nP = len(points)
        nSTRE = self.Material.number_of_material_variables
        nRHS = self.number_of_load_cases

        # allocate result
        strains = np.zeros((nE, nP, nSTRE, nRHS), dtype=float)

        # calculate at Gauss points
        gauss_evaluator = partial(
            self._gauss_strains_,
            ecoords=ecoords,
            dofsol=dofsol,
            cells=cells,
        )

        for q in self._parse_gauss_data(self.Material.quadrature, "stiffness"):
            nQ = len(q.weight)

            if nQ == 1:
                approximator_cls = None
            elif nQ == 2:
                approximator_cls = L2.Geometry
            elif nQ == 3:
                approximator_cls = L3.Geometry
            else:
                approximator_cls = PolyCellGeometry1d.generate_class(number_of_nodes=nQ)

            if approximator_cls:
                approximator = LagrangianCellGaussApproximator(approximator_cls)
                strains[:, :, q.inds, :] += approximator(
                    source=q.pos, target=points, values=gauss_evaluator(quad=q)
                )[:, :, q.inds, :]
            else:
                strains[:, :, q.inds, :] += gauss_evaluator(quad=q)[:, :, q.inds, :]

        return strains  # (nE, nP, nSTRE, nRHS)

    def _gauss_strains_(
        self,
        *,
        ecoords: ndarray,  # (nE, nNE, nD)
        dofsol: ndarray,  # (nE, nRHS, nNE * nDOF)
        quad: Quadrature,
        cells: Iterable[int],
    ) -> ndarray:  # (nE, nP, nSTRE, nRHS)
        points: Iterable[float] = quad.pos

        shp = self.Geometry.shape_function_values(points)
        dshp = self.Geometry.shape_function_derivatives(points)
        jac = self.jacobian_matrix(dshp=dshp, ecoords=ecoords)  # (nE, nP, nD, nD)
        B = self.Material.strain_displacement_matrix(
            self, points, shp=shp, dshp=dshp, jac=jac
        )[
            cells
        ]  # (nE, nP, nSTRE, nNODE * nDOFN)

        strains = approx_element_solution_bulk(dofsol, B)  # (nE, nRHS, nP, nSTRE)
        strains = ascont(np.moveaxis(strains, 1, -1))  # (nE, nP, nSTRE, nRHS)

        return strains
