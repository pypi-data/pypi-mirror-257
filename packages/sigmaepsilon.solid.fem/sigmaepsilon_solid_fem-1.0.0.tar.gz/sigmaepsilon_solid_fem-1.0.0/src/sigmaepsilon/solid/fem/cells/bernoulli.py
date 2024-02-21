from typing import Union, Iterable

import numpy as np
from numpy import ndarray
from scipy import interpolate

from sigmaepsilon.math import atleastnd, ascont
from sigmaepsilon.mesh.geometry import PolyCellGeometry1d

from ..typing import (
    FemDataProtocol as FD,
    PointDataProtocol as PD,
)
from ..data import FiniteElement
from ..utils.cells.bernoulli import (
    body_load_vector_Bernoulli,
    lumped_mass_matrices_direct_Bernoulli as dlump,
)
from ..utils.postproc import (
    approx_element_solution_bulk,
    calculate_internal_forces_bulk,
)
from ..material.utils.bernoulli import (
    _postproc_bernoulli_internal_forces_H_,
    _postproc_bernoulli_internal_forces_L_,
)

__all__ = ["BernoulliBase"]


class BernoulliBase(FiniteElement[FD, PD]):
    """
    Base class for 1d finite elements, whose bending behaviour
    is governed by the Euler-Bernoulli theory.

    See Also
    --------
    :class:`~sigmaepsilon.solid.fem.cells.bernoulli2.Bernoulli2`
    :class:`~sigmaepsilon.solid.fem.cells.bernoulli3.Bernoulli3`
    """

    def integrate_body_loads(self, values: ndarray) -> ndarray:
        """
        Returns nodal representation of body loads.

        Parameters
        ----------
        values: numpy.ndarray
            2d or 3d numpy float array of material densities of shape
            (nE, nNE * nDOF, nRHS) or (nE, nNE * nDOF), where nE, nNE, nDOF and nRHS
            stand for the number of elements, nodes per element, number of degrees
            of freedom and number of load cases respectively.

        Returns
        -------
        numpy.ndarray
            An array of shape (nE, nNE * 6, nRHS).

        Notes
        -----
        The returned array is always 3 dimensional, even if there is only one
        load case.

        See Also
        --------
        :func:`~body_load_vector_bulk`
        """
        values = atleastnd(values, 3, back=True).astype(float)
        # (nE, nNE * nDOF, nRHS) -> (nE, nRHS, nNE * nDOF)
        values = np.swapaxes(values, 1, 2)
        values = ascont(values)
        qpos, qweights = self.Material.quadrature["full"]
        rng = np.array([-1.0, 1.0])
        shp = self.Material.shape_function_values(self, qpos, rng=rng)
        # (nP, nNE=2, nDOF=6)
        dshp = self.Material.shape_function_derivatives(self, qpos, rng=rng)
        # (nP, nNE=2, nDOF=6, 3)
        ecoords = self.local_coordinates()
        jac = self.jacobian_matrix(dshp=dshp, ecoords=ecoords)
        # (nE, nP, 1, 1)
        djac = self.jacobian(jac=jac)  # (nE, nG)
        gdshp = self.Material.shape_function_derivatives(self, jac=jac, dshp=dshp)
        # (nE, nP, nNE=2, nDOF=6, 3)
        return body_load_vector_Bernoulli(values, shp, gdshp, djac, qweights)

    def _internal_forces_H_(
        self,
        *_,
        cells: Union[int, Iterable[int]] = None,
        points: Union[float, Iterable] = None,  # [-1, 1]
    ) -> ndarray:
        shp = self.Material.shape_function_values(self, points, rng=[-1, 1])[cells]
        dshp = self.Material.shape_function_derivatives(self, points, rng=[-1, 1])[
            cells
        ]
        ecoords = self.local_coordinates()[cells]
        jac = self.jacobian_matrix(dshp=dshp, ecoords=ecoords)
        # jac -> (nE, nP, 1, 1)
        B = self.Material.strain_displacement_matrix(self, shp=shp, dshp=dshp, jac=jac)
        # B -> (nE, nP, nSTRE, nNODE * 6)

        dofsol = self.dof_solution(flatten=True, cells=cells)
        # dofsol -> (nE, nNE * nDOF, nRHS)
        dofsol = ascont(np.swapaxes(dofsol, 1, 2))
        # dofsol -> (nE, nRHS, nEVAB)
        strains = approx_element_solution_bulk(dofsol, B)
        # strains -> (nE, nRHS, nP, nSTRE)
        strains -= self.kinetic_strains(points=points)[cells]
        D = self.Material.elastic_material_stiffness_matrix(self)[cells]
        forces = calculate_internal_forces_bulk(strains, D)
        # forces -> (nE, nRHS, nP, nSTRE)
        forces = ascont(np.moveaxis(forces, 1, -1))
        dofsol = ascont(np.swapaxes(dofsol, 1, 2))
        # dofsol -> (nE, nEVAB, nRHS)
        # forces -> (nE, nP, nSTRE, nRHS)
        gdshp = self.Material.shape_function_derivatives(self, jac=jac, dshp=dshp)
        nE, _, nRHS = dofsol.shape
        nNE, nDOF = (
            self.Geometry.number_of_nodes,
            self.Material.number_of_displacement_variables,
        )
        dofsol = dofsol.reshape(nE, nNE, nDOF, nRHS)
        D = self.Material.elastic_material_stiffness_matrix(self)[cells]
        forces = _postproc_bernoulli_internal_forces_H_(dofsol, forces, D, gdshp)
        return forces  # (nE, nP, 6, nRHS)

    def _internal_forces_L_(
        self,
        *_,
        cells: Union[int, Iterable[int]] = None,
        points: Union[float, Iterable] = None,  # [-1, 1]
    ) -> ndarray:
        local_points = np.array(self.Geometry.master_coordinates()).flatten()

        shp = self.Material.shape_function_values(self, local_points, rng=[-1, 1])[
            cells
        ]
        dshp = self.Material.shape_function_derivatives(
            self, local_points, rng=[-1, 1]
        )[cells]
        ecoords = self.local_coordinates()[cells]
        jac = self.jacobian_matrix(dshp=dshp, ecoords=ecoords)
        # jac -> (nE, nNE, 1, 1)
        B = self.Material.strain_displacement_matrix(self, shp=shp, dshp=dshp, jac=jac)
        # B -> (nE, nNE, nSTRE, nNODE * 6)

        dofsol = self.dof_solution(flatten=True, cells=cells)
        # dofsol -> (nE, nNE * nDOF, nRHS)
        dofsol = ascont(np.swapaxes(dofsol, 1, 2))
        # dofsol -> (nE, nRHS, nEVAB)
        strains = approx_element_solution_bulk(dofsol, B)
        # strains -> (nE, nRHS, nNE, nSTRE)
        strains -= self.kinetic_strains(points=local_points)[cells]
        D = self.Material.elastic_material_stiffness_matrix(self)[cells]

        nE, nRHS, nP = strains.shape[:3]
        forces = np.zeros((nE, nRHS, nP, 6), dtype=float)
        inds = np.array([0, 3, 4, 5], dtype=int)
        calculate_internal_forces_bulk(strains, D, forces, inds)
        # forces -> (nE, nRHS, nNE, nSTRE)
        forces = np.moveaxis(forces, 1, -1)
        # forces -> (nE, nNE, nSTRE, nRHS)

        Geometry: PolyCellGeometry1d = self.Geometry
        *_, dshpf = Geometry.generate_class_functions(
            update=False, return_symbolic=False
        )
        dshp_geom = np.squeeze(dshpf([[i] for i in local_points]))
        # dshp_geom -> (nNE, nNE)
        _postproc_bernoulli_internal_forces_L_(forces, dshp_geom, jac)
        # forces -> (nE, nNE, nSTRE, nRHS)

        if isinstance(points, Iterable):
            approx = interpolate.interp1d(
                local_points, forces, axis=1, assume_sorted=True
            )
            forces = approx(points)

        return ascont(forces)

    def _internal_forces_(self, *args, **kwargs):
        return self._internal_forces_L_(self, *args, **kwargs)
        # return self._internal_forces_H_(self, *args, **kwargs)

    def lumped_mass_matrix(
        self,
        *_,
        lumping: str = "direct",
        alpha: float = 1 / 50,
        frmt: str = "full",
        **__,
    ) -> ndarray:
        """
        Returns the lumped mass matrix of the block.

        Parameters
        ----------
        alpha: float, Optional
            A nonnegative parameter, typically between 0 and 1/50 (see notes).
            Default is 1/20.
        lumping: str, Optional
            Controls lumping. Currently only direct lumping is available.
            Default is 'direct'.
        frmt: str, Optional
            Possible values are 'full' or 'diag'. If 'diag', only the diagonal
            entries are returned, if 'full' a full matrix is returned.
            Default is 'full'.
        """
        dbkey = self.__class__._attr_map_["M"]
        if lumping == "direct":
            dens = self.density
            try:
                areas = self.areas()
            except Exception:
                areas = np.ones_like(dens)
            lengths = self.lengths()
            topo = self.topology()
            ediags = dlump(dens, lengths, areas, topo, alpha)
            if frmt == "full":
                N = ediags.shape[-1]
                M = np.zeros((ediags.shape[0], N, N))
                inds = np.arange(N)
                M[:, inds, inds] = ediags
                self.db[dbkey] = M
                return M
            elif frmt == "diag":
                self.db[dbkey] = ediags
                return ediags
        raise RuntimeError("Lumping mode not recognized :(")
