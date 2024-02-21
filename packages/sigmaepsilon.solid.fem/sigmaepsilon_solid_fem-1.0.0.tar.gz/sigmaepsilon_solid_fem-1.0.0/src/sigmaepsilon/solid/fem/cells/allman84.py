from typing import Iterable, Union, Optional

import numpy as np
from numpy import ndarray

from sigmaepsilon.math import atleast2d
from sigmaepsilon.mesh.cells import T3, Q4, Q9
from sigmaepsilon.mesh.utils.numint import Gauss_Legendre_Tri_3a

from ..data.finiteelement import Quadrature
from ..data import DrillingMembraneFiniteElement
from ..material import DrillingMembraneMaterial
from .utils.all84 import (
    shape_function_matrix_bulk_multi_all84,
    strain_displacement_matrix_bulk_multi_all84,
)
from .utils.super import dofmap_of_subtriangles, sublocations_of_points
from ..utils.cells import (
    stiffness_matrix_bulk2,
    stiffness_matrix_bulk2_i,
    strain_displacement_matrix_bulk2,
)

__all__ = ["T3_ALL84_M", "Q4_ALL84_M", "Q9_ALL84_M"]


class T3_ALL84_M(DrillingMembraneFiniteElement):
    """
    Allman's drilling triangle from 1984. The class can be used to create new super
    classes hosting a certain number of All84 triangles. All you have to do is to
    implement the `master_topology` class function on the `Geometry` class member.
    """

    label = "T3_ALL84_M"

    class Geometry(T3.Geometry):
        @classmethod
        def master_topology(cls) -> Union[ndarray, None]:
            return None

    class Material(DrillingMembraneMaterial):
        quadrature = {
            "full": Gauss_Legendre_Tri_3a,
            "stiffness": "full",
            "mass": "full",
        }

        @classmethod
        def shape_function_matrix(
            cls,
            parent: "T3_ALL84_M",
            x: Iterable[float],
            *_,
            needs_transform: Optional[bool] = True,
            out: Optional[Union[ndarray, None]] = None,
            **kwargs,
        ) -> ndarray:
            """
            Evaluates the shape function matrix at one or more points.

            Parameters
            ----------
            parent: FiniteElementProtocol
                The parent celldata instance.
            x: Iterable[float]
                Locations of one or more evaluation points.
            needs_transform: bool, Optional
                Controls how the argument 'x' is understood. If it is 'True', it is assumed
                that the points 'x' are specified in the master cell (eg. Q9). Then for each
                point of interest, it is decided which is the hosting subelement and evaluation
                is carried out in the target subtriangle elements. When 'False', it is assumed
                that the points are provided in the domain of a master triangle and each triangle
                should be evaluated at every such point. Default is True.

            Returns
            -------
            numpy.ndarray
                4d float array of shape (nE, nP, nDOF=3, nNE*nDOF=12).
            """
            x = atleast2d(np.array(x), front=True)
            ec = kwargs.get("ec_", parent.local_coordinates())
            nE, nNE = ec.shape[:2]
            nP = x.shape[0]
            nDOF = parent.Material.number_of_displacement_variables
            inds = np.arange(nDOF * nNE)

            if out is None:
                out = np.zeros((nE, nP, nDOF, nDOF * nNE), dtype=x.dtype)

            # triangles -> maps the nodes of the subelements
            # to the nodes of the super element
            triangles = parent.Geometry.master_topology()

            if triangles is None:  # this is not a superelement
                return shape_function_matrix_bulk_multi_all84(x, ec, out, inds)

            # subdofmap -> maps dofs of the subelements
            # the dofs of the super element
            subdofmap = dofmap_of_subtriangles(triangles, nDOF)

            if not needs_transform:
                for iT in range(len(triangles)):
                    i_tri = triangles[iT]
                    inds = subdofmap[iT]
                    shape_function_matrix_bulk_multi_all84(x, ec[:, i_tri], out, inds)
            else:
                # submap -> maps the points of evaluation to
                # the subelements
                mc = parent.Geometry.master_coordinates()
                submap, subloc = sublocations_of_points(x, mc, triangles)

                for iP in range(nP):
                    iT = submap[iP]
                    i_tri = triangles[iT]
                    i_loc = subloc[iP]
                    i_x = atleast2d(i_loc)
                    inds = subdofmap[iT]
                    shape_function_matrix_bulk_multi_all84(i_x, ec[:, i_tri], out, inds)

            return out

        @classmethod
        def strain_displacement_matrix(
            cls,
            parent: "T3_ALL84_M",
            x: Iterable[float],
            *_,
            out: Optional[Union[ndarray, None]] = None,
            needs_transform: bool = True,
            **kwargs,
        ) -> ndarray:
            """
            Calculates the strain displacement matrix.

            Parameters
            ----------
            parent: FiniteElementProtocol
                The parent celldata instance.
            x: Iterable[float]
                Locations of one or more evaluation points.
            needs_transform: bool, Optional
                Controls how the argument 'x' is understood. If it is 'True', it is assumed
                that the points 'x' are specified in the master cell (eg. Q9). Then for each
                point of interest, it is decided which is the hosting subelement and evaluation
                is carried out in the target subtriangle elements. When 'False', it is assumed
                that the points are provided in the domain of a master triangle and each triangle
                should be evaluated at every such point. Default is True.

            Returns
            -------
            numpy.ndarray
                4d float array of shape (nE, nP, nSTRE=3, nNE*nDOF=9).
            """
            ec = kwargs.get("_ec", parent.local_coordinates())
            nE, nNE = ec.shape[:2]
            nP = x.shape[0]
            nDOF = parent.Material.number_of_displacement_variables
            nSTRE = parent.Material.number_of_material_variables
            inds = kwargs.get("_inds", np.arange(nDOF * nNE))

            if out is None:
                out = np.zeros((nE, nP, nSTRE, nDOF * nNE), dtype=x.dtype)

            # triangles -> maps the nodes of the subelements
            # to the nodes of the super element
            if "_triangles" in kwargs:
                triangles = kwargs.get("_triangles")
            else:
                triangles = parent.Geometry.master_topology()

            if triangles is None:  # this is not a superelement
                return strain_displacement_matrix_bulk_multi_all84(x, ec, out, inds)

            # subdofmap -> maps dofs of the subelements
            # the dofs of the super element
            subdofmap = dofmap_of_subtriangles(triangles, nDOF)

            if not needs_transform:
                for iT in range(len(triangles)):
                    i_tri = triangles[iT]
                    inds = subdofmap[iT]
                    strain_displacement_matrix_bulk_multi_all84(
                        x, ec[:, i_tri], out, inds
                    )
            else:
                # submap -> maps the points of evaluation to
                # the subelements
                mc = parent.Geometry.master_coordinates()
                submap, subloc = sublocations_of_points(x, mc, triangles)

                for iP in range(nP):
                    iT = submap[iP]
                    i_tri = triangles[iT]
                    i_loc = subloc[iP]
                    i_x = atleast2d(i_loc)
                    inds = subdofmap[iT]
                    strain_displacement_matrix_bulk_multi_all84(
                        i_x, ec[:, i_tri], out, inds
                    )

            return out

    def __strain_displacement_matrix__(self) -> ndarray:
        # this was used in the original implementation of
        # __elastic_stiffness_matrix__
        raise NotImplementedError

    def __elastic_stiffness_matrix__(
        self, q: Quadrature, ec: ndarray, D: ndarray
    ) -> ndarray:
        # the strain displacement matrix is zeroed when starting
        # to build the stiffness matrix

        x = q.pos  # the gauss locations
        
        # returnes the topology if this is a superelement or None if it isn't
        triangles = self.Geometry.master_topology()

        if triangles is None:  # not a super element
            B = T3_ALL84_M.Material.strain_displacement_matrix(
                self, x, _ec=ec, needs_transform=False
            )
            dshp = self.Geometry.shape_function_derivatives(q.pos)
            jac = self.jacobian_matrix(dshp=dshp, _ec=ec)
            djac = self.jacobian(jac=jac)

            if q.inds is not None:
                NSTRE = self.Material.number_of_material_variables
                # zero out unused indices, only for selective integration
                inds = np.where(~np.in1d(np.arange(NSTRE), q.inds))[0]
                B[:, :, inds, :] = 0.0

            dbkey = self._dbkey_strain_displacement_matrix_
            _B = self.db[dbkey].to_numpy()
            _B += strain_displacement_matrix_bulk2(B, djac, q.weight)
            self.db[dbkey] = _B

            return stiffness_matrix_bulk2(D, B, djac, q.weight)
        else:
            # this is a superelement -> assemble from subtriangles
            nDOF = self.Material.number_of_displacement_variables
            nE, nNE = ec.shape[:2]
            nDOF = self.Material.number_of_displacement_variables
            out = np.zeros((nE, nDOF * nNE, nDOF * nNE), dtype=x.dtype)
            dshp = T3_ALL84_M.Geometry.shape_function_derivatives(x)
            for tri in triangles:
                inds = np.array(
                    [i * nDOF + j for i in tri for j in range(nDOF)], dtype=int
                )
                _ec = ec[:, tri]
                B = T3_ALL84_M.Material.strain_displacement_matrix(
                    self, x, _ec=_ec, needs_transform=False, _triangles=None
                )
                jac = self.jacobian_matrix(dshp=dshp, _ec=_ec)
                djac = self.jacobian(jac=jac)
                stiffness_matrix_bulk2_i(D, B, djac, q.weight, inds, out)
            return out


class Q4_ALL84_M(T3_ALL84_M):
    """
    A 4-node superelement consisting of 2 triangle membranes of Allman from 1984.
    """

    label = "Q4_ALL84_M"
    standalone = True

    class Geometry(Q4.Geometry):
        @classmethod
        def master_topology(cls) -> Union[ndarray, None]:
            return np.array([[0, 1, 2], [0, 2, 3]], dtype=int)


class Q9_ALL84_M(T3_ALL84_M):
    """
    A 9-node superelement consisting of 8 triangle membranes of Allman from 1984.
    """

    label = "Q9_ALL84_M"
    standalone = True

    class Geometry(Q9.Geometry):
        @classmethod
        def master_topology(cls) -> Union[ndarray, None]:
            return np.array(
                [
                    [0, 4, 7],
                    [1, 5, 4],
                    [2, 6, 5],
                    [3, 7, 6],
                    [8, 4, 5],
                    [8, 5, 6],
                    [8, 6, 7],
                    [8, 7, 4],
                ],
                dtype=int,
            )
