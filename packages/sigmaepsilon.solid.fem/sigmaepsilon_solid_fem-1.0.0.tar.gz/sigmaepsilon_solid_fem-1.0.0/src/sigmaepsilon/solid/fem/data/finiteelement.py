from typing import (
    Union,
    Iterable,
    ClassVar,
    Optional,
    TypeVar,
    Generic,
    Hashable,
    Callable,
    Tuple,
)
from functools import partial
from numbers import Number

from scipy.sparse import coo_matrix
import numpy as np
from numpy import ndarray
from awkward.errors import FieldNotFoundError
import xarray as xr

from sigmaepsilon.math.linalg import ReferenceFrame
from sigmaepsilon.math import atleastnd, ascont
from sigmaepsilon.math.linalg.sparse.jaggedarray import JaggedArray
from sigmaepsilon.math.logical import is1dfloatarray, isboolarray

from sigmaepsilon.mesh.data import PolyCell
from sigmaepsilon.mesh.geometry.geometry import PolyCellGeometry
from sigmaepsilon.mesh.cells import T3, Q4, Q9, T6, L2, L3

from sigmaepsilon.solid.material import CauchyStressTensor
from sigmaepsilon.solid.material import MaterialLike, StiffnessLike
from sigmaepsilon.solid.material.surface.surface import SurfaceSection
from sigmaepsilon.solid.material.utils.tr import _tr_stresses_3d_bulk_multi
from sigmaepsilon.solid.material.utils.imap import _map_6x1_to_3x3, _map_3x3_to_6x1

from .celldata import CellData
from ..typing import (
    ABC_FemCell,
    FemDataProtocol,
    PointDataProtocol,
    MaterialProtocol,
    CellDataProtocol,
)
from ..utils.preproc.preproc import (
    fem_coeff_matrix_coo,
    assert_min_diagonals_bulk,
    assemble_load_vector,
)
from ..utils.postproc import (
    approx_element_solution_bulk,
    calculate_external_forces_bulk,
    calculate_internal_forces_bulk,
    explode_kinetic_strains,
    element_dof_solution_bulk,
)
from ..utils.tr import (
    nodal_dcm,
    nodal_dcm_bulk,
    element_dcm,
    element_dcm_bulk,
    tr_element_vectors_bulk_multi as tr_vectors,
    tr_element_matrices_bulk as tr_matrices,
    _scatter_element_frames,
)
from ..utils.fem import (
    topo_to_gnum,
    expand_coeff_matrix_bulk,
    element_dofmap_bulk,
    topo_to_gnum_jagged,
    expand_load_vector_bulk,
)
from ..utils.cells import (
    stiffness_matrix_bulk2,
    strain_displacement_matrix_bulk2,
    unit_strain_load_vector_bulk,
    strain_load_vector_bulk,
    mass_matrix_bulk,
    body_load_vector_bulk_cm,
    body_load_vector_bulk_vm,
)
from ..utils.utils import expand_shape_function_matrix
from ..numint import Quadrature
from ..approximator import LagrangianCellGaussApproximator
from ..utils.preproc.condensate import condensate_bulk

FD = TypeVar("FD", bound=FemDataProtocol)
PD = TypeVar("PD", bound=PointDataProtocol)


class FiniteElement(Generic[FD, PD], PolyCell[FD, PD], ABC_FemCell):
    """
    A subclass of :class:`~sigmaepsilon.mesh.data.PolyCell` as a base class
    for all finite elements.

    Parameters
    ----------
    activity: numpy.ndarray, Optional
        1d boolean array describing the activity of the elements.
    density: numpy.ndarray, Optional
        1d float array describing the density as mass per unit volume if areas
        (or thickness) are provided, mass per unit length (or area) othervise.
        See the Notes. Default is None.
    loads: numpy.ndarray, Optional
        3d (for a single load case) or 4d (for multiple load cases) float
        array of body loads for each load component of each node of each cell.
        Default is None.
    strain_loads: numpy.ndarray, Optional
        2d float array of body strain loads for each cell and strain
        component. Default is None.
    t or thickness: numpy.ndarray, Optional
        1d float array of thicknesses. Only for 2d cells.
        Default is None.
    fixity: numpy.ndarray, Optional
        3d boolean array of element fixity. Default is None.
    areas: numpy.ndarray, Optional
        1d float array of cross sectional areas. Only for 1d cells.
        Default is None.
    fields: dict, Optional
        Every value of this dictionary is added to the dataset.
        Default is `None`.
    material: Union[MaterialLike, StiffnessLike, ndarray], Optional
        The material of the cells either as an object which is an instance of
        :class:`~sigmaepsilon.solid.core.material.MaterialLike`, or NumPy arrays
        for every cell in the block. In the latter case, the matrices must have
        a matching shape to the model. Default is None.
    **kwargs: dict, Optional
        For every key and value pair where the value is a numpy array
        with a matching shape (has entries for all points), the key
        is considered as a field and the value is added to the database.
    """

    Material: ClassVar[MaterialProtocol]
    standalone: Optional[bool] = False

    data_class: ClassVar[type] = CellData[FD, PD]

    def __init__(
        self,
        *args,
        material: Optional[Union[MaterialLike, StiffnessLike, ndarray, None]] = None,
        loads: Optional[Union[ndarray, None]] = None,
        strain_loads: Optional[Union[ndarray, None]] = None,
        activity: Optional[Union[ndarray, None]] = None,
        density: Optional[Union[ndarray, None]] = None,
        fields: Optional[Union[dict, None]] = None,
        t: Optional[Union[ndarray, None]] = None,
        thickness: Optional[Union[ndarray, None]] = None,
        fixity: Optional[Union[ndarray, None]] = None,
        **kwargs,
    ):
        super().__init__(*args, fields=fields, **kwargs)

        t = t if thickness is None else thickness

        if self.db is not None:
            topo = self.topology().to_numpy()
            nE, nNE = topo.shape
            NDOFN = self.Material.number_of_displacement_variables

            if activity is not None:
                assert isinstance(activity, ndarray)
                assert activity.shape[0] == nE
                self.db.activity = activity

            if isinstance(fixity, ndarray):
                assert isboolarray(fixity), "Fixity must be a boolean array."
                assert fixity.shape[0] == nE
                self.db.fixity = fixity

            if isinstance(density, ndarray):
                assert (
                    len(density.shape) == 1
                ), "'densities' must be a 1d float or integer numpy array!"
                self.db.density = density
            else:
                if density is not None and "density" not in fields:
                    raise TypeError(
                        "'density' must be a 1d float" + " or integer numpy array!"
                    )

            # body loads
            if loads is not None:
                assert isinstance(loads, ndarray)
                if loads.shape[0] == nE and loads.shape[1] == nNE:
                    self.db.loads = loads
                elif loads.shape[0] == nE and loads.shape[1] == nNE * NDOFN:
                    loads = atleastnd(loads, 3, back=True)
                    self.db.loads = loads.reshape(nE, nNE, NDOFN, loads.shape[-1])

            # strain loads
            if strain_loads is not None:
                assert isinstance(strain_loads, ndarray)
                assert strain_loads.shape[0] == nE
                self.db.strain_loads = strain_loads

            if self.Geometry.number_of_spatial_dimensions == 2:
                nE = len(self.db)
                if t is None:
                    t = np.ones(nE, dtype=float)
                else:
                    if isinstance(t, float):
                        t = np.full(nE, t)
                    else:
                        assert is1dfloatarray(
                            t
                        ), "'t' must be a 1d numpy array or a float!"
                self.db.t = t

        self._material = None
        if isinstance(material, (StiffnessLike, SurfaceSection)):
            self._material = material
            self.db.material_stiffness = material.elastic_stiffness_matrix()
        elif isinstance(material, MaterialLike):
            self._material = material
            self.db.material_stiffness = material.stiffness.elastic_stiffness_matrix()
        elif isinstance(material, ndarray):
            self.db.material_stiffness = material

    @property
    def db(self) -> CellDataProtocol[FemDataProtocol, PointDataProtocol]:
        """
        Returns the database of the block.
        """
        return self._db

    @db.setter
    def db(self, value: CellDataProtocol[FemDataProtocol, PointDataProtocol]) -> None:
        """
        Sets the database of the block.
        """
        self._db = value

    @property
    def number_of_load_cases(self) -> int:
        """
        Returns the number of load cases in the model.
        """
        if len(self.pointdata.loads.shape) == 2:
            nRHS = 1
        else:
            nRHS = self.pointdata.loads.shape[-1]
        return nRHS

    @property
    def material(self) -> Union[MaterialLike, None]:
        """
        Returns the attached material, or `None` if there is none.
        """
        return self._material

    @material.setter
    def material(self, value: MaterialLike) -> None:
        """
        Sets the attached material.
        """
        self._material = value

    def _approximator_class(
        self, N: Optional[Union[int, None]] = None
    ) -> PolyCellGeometry:
        nNE = self.Geometry.number_of_nodes
        nD = self.Geometry.number_of_spatial_dimensions

        nP = nNE
        if N is not None:
            nP = N

        if nP == 1:
            return None

        if nD == 1:
            if nP == 2:
                return L2.Geometry
            elif nP == 3:
                return L3.Geometry
        elif nD == 2:
            if nP == 3:
                return T3.Geometry
            elif nP == 4:
                return Q4.Geometry
            elif nP == 6:
                return T6.Geometry
            elif nP == 9:
                return Q9.Geometry

        return self.__class__.Geometry

    def _parse_gauss_data(self, quad_dict: dict, key: Hashable) -> Iterable[Quadrature]:
        value: Union[Callable, str, dict] = quad_dict[key]

        if isinstance(value, dict):
            for qinds, qvalue in value.items():
                if isinstance(qvalue, str):
                    qdata = quad_dict[qvalue]
                    if isinstance(qdata, Callable):
                        qpos, qweight = qdata()
                    else:
                        qpos, qweight = qdata
                else:
                    qpos, qweight = qvalue
                quad = Quadrature(qpos, qweight, inds=qinds)
                yield quad
        elif isinstance(value, Callable):
            qpos, qweight = value()
            nSTRE = self.Material.number_of_material_variables
            inds = tuple(range(nSTRE))
            quad = Quadrature(qpos, qweight, inds=inds)
            yield quad
        elif isinstance(value, str):
            for v in self._parse_gauss_data(quad_dict, value):
                yield v
        else:
            qpos, qweight = value
            nSTRE = self.Material.number_of_material_variables
            inds = tuple(range(nSTRE))
            quad = Quadrature(qpos, qweight, inds=inds)
            yield quad

    def elastic_material_stiffness_matrix(self, *args, **kwargs) -> ndarray:
        """
        Returns the elastic stiffness matrix as a 2d NumPy array.
        """
        return self.Material.elastic_material_stiffness_matrix(self, *args, **kwargs)

    def direction_cosine_matrix(
        self,
        *_,
        source: Optional[Union[ndarray, str, ReferenceFrame, None]] = None,
        target: Optional[Union[ndarray, str, ReferenceFrame, None]] = None,
        N: Optional[Union[int, None]] = None,
        **kwargs,
    ) -> ndarray:
        """
        Returns the DCM matrix for all elements in the block.

        Parameters
        ----------
        source: Union[ndarray, str, ReferenceFrame], Optional
            A source frame. The string 'global' refers to the global
            frame of the mesh. Default is None.
        target: Union[ndarray, str, ReferenceFrame], Optional
            A target frame. The string 'global' refers to the global
            frame of the mesh. Default is None.
        N: int, Optional
            Number of points. If not specified, the number of nodes is inferred from
            the class of the instance the function is called upon. Default is None.

        Returns
        -------
        numpy.ndarray
            The dcm matrix for linear transformations from source to target.
        """
        nNE = self.Geometry.number_of_nodes if N is None else N
        nDOF = kwargs.get("_ndof", self.container.number_of_displacement_variables)

        div, mod = divmod(nDOF, 3)
        if not mod == 0:
            raise ValueError(
                "The default mechanism assumes that the number of "
                + "deegrees of freedom per node is a multiple of 3."
            )

        mesh_source = self.container.source()
        ndcm = nodal_dcm_bulk(self.frames, div)
        dcm = element_dcm_bulk(ndcm, nNE, nDOF)  # (nE, nEVAB, nEVAB)

        if source is None and target is None:
            target = "global"

        if isinstance(target, str) and target == "global":
            target = ReferenceFrame(mesh_source.frame)

        if isinstance(source, str) and source == "global":
            source = ReferenceFrame(mesh_source.frame)

        if source is not None:
            if isinstance(source, ReferenceFrame):
                if len(source) == 3:
                    s_ndcm = nodal_dcm(source.dcm(), div)
                    s_dcm = element_dcm(s_ndcm, nNE, nDOF)  # (nEVAB, nEVAB)
                    source = ReferenceFrame(s_dcm)
                return ReferenceFrame(dcm).dcm(source=source)
            else:
                raise NotImplementedError
        elif target is not None:
            if isinstance(target, ReferenceFrame):
                if len(target) == 3:
                    t_ndcm = nodal_dcm(target.dcm(), div)
                    t_dcm = element_dcm(t_ndcm, nNE, nDOF)  # (nEVAB, nEVAB)
                    target = ReferenceFrame(t_dcm)
                return ReferenceFrame(dcm).dcm(target=target)
            else:
                raise NotImplementedError

        raise NotImplementedError

    def dof_solution(
        self,
        *_,
        target: Optional[Union[str, ReferenceFrame]] = "local",
        cells: Optional[Union[int, Iterable[int], None]] = None,
        points: Optional[Union[float, Iterable, None]] = None,
        rng: Optional[Union[Iterable, None]] = None,
        flatten: Optional[bool] = True,
        **__,
    ) -> ndarray:
        """
        Returns nodal displacements for the cells, wrt. their local frames.

        Parameters
        ----------
        points: float or Iterable, Optional
                Points of evaluation. If provided, it is assumed that the given values
                are wrt. the range [0, 1], unless specified otherwise with the 'rng'
                parameter. If not provided, results are returned for the nodes of the
                selected elements. Default is None.
        rng: Iterable, Optional
            Range where the points of evauation are understood. Only for 1d cells.
            Default is [0, 1].
        cells: int or Iterable[int], Optional
            Indices of cells. If not provided, results are returned for all cells.
            If cells are provided, the function returns a dictionary, with the cell
            indices being the keys. Default is None.
        target: str or ReferenceFrame, Optional
            Reference frame for the output. A value of None or 'local' refers to the
            local system of the cells. Default is 'local'.

        Returns
        -------
        numpy.ndarray
            An array of shape (nE, nEVAB, nRHS) if 'flatten' is True
            else (nE, nNE, nDOF, nRHS).
        """
        cells = self._get_cell_slicer(cells)
        points, rng = self._get_points_and_range(points, rng)

        nDIM = self.Geometry.number_of_spatial_dimensions

        dofsol = self.pointdata.dofsol
        dofsol = atleastnd(dofsol, 3, back=True)
        nP, nDOF, nRHS = dofsol.shape
        dofsol = dofsol.reshape(nP * nDOF, nRHS)
        gnum = self.global_dof_numbering().to_numpy()[cells]

        # transform values to cell-local frames
        dcm = self.direction_cosine_matrix(source="global")[cells]
        values = element_dof_solution_bulk(dofsol, gnum)  # (nE, nEVAB, nRHS)
        values = ascont(np.swapaxes(values, 1, 2))  # (nE, nRHS, nEVAB)
        values = tr_vectors(values, dcm)
        values = ascont(np.swapaxes(values, 1, 2))  # (nE, nEVAB, nRHS)

        # approximate at points
        # values -> (nE, nEVAB, nRHS)
        if nDIM == 1:
            N = self.Material.shape_function_matrix(self, points, rng=rng)[cells]
        else:
            N = self.Material.shape_function_matrix(self, points)
            N = expand_shape_function_matrix(self, N)
            if len(N.shape) > 3:
                N = N[cells]
        # N -> (nP, nDOF, nDOF * nNODE) for constant metric
        # N -> (nE, nP, nDOF, nDOF * nNODE) for variable metric
        values = ascont(np.swapaxes(values, 1, 2))  # (nE, nRHS, nEVAB)
        values = approx_element_solution_bulk(values, N)
        # values -> (nE, nRHS, nP, nDOF)

        if target is not None:
            # transform values to a destination frame, otherwise return
            # the results in the local frames of the cells
            if isinstance(target, str) and target == "local":
                pass
            else:
                nE, nRHS, nP, nDOF = values.shape
                values = values.reshape(nE, nRHS, nP * nDOF)
                dcm = self.direction_cosine_matrix(N=nP, target=target)[cells]
                values = tr_vectors(values, dcm)
                values = values.reshape(nE, nRHS, nP, nDOF)

        values = np.moveaxis(values, 1, -1)  # (nE, nP, nDOF, nRHS)

        if flatten:
            nE, nP, nDOF, nRHS = values.shape
            values = values.reshape(nE, nP * nDOF, nRHS)

        # values -> (nE, nP, nDOF, nRHS) or (nE, nP * nDOF, nRHS)
        return values

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

        nE, nP = len(dofsol), len(points)
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

            approximator_cls: PolyCellGeometry = self._approximator_class(N=nQ)

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

        if self.Geometry.number_of_spatial_dimensions == 1:
            shp = self.Material.shape_function_values(self, points, rng=[-1, 1])
            dshp = self.Geometry.shape_function_derivatives(points, rng=[-1, 1])
        else:
            shp = self.Material.shape_function_values(self, points)
            dshp = self.Geometry.shape_function_derivatives(points)

        jac = self.jacobian_matrix(dshp=dshp, ecoords=ecoords)[
            cells
        ]  # (nE, nP, nD, nD)
        B = self.Material.strain_displacement_matrix(
            self, points, shp=shp, dshp=dshp, jac=jac
        )  # (nE, nP, nSTRE, nNODE * nDOFN)

        strains = approx_element_solution_bulk(dofsol, B)  # (nE, nRHS, nP, nSTRE)
        strains = ascont(np.moveaxis(strains, 1, -1))  # (nE, nP, nSTRE, nRHS)

        return strains

    def strains(
        self,
        *_,
        cells: Optional[Union[int, Iterable[int], None]] = None,
        rng: Optional[Union[Iterable, None]] = None,
        points: Optional[Union[float, Iterable, None]] = None,
        **__,
    ) -> ndarray:
        """
        Returns strains for one or more cells.

        Parameters
        ----------
        points: float or Iterable[float], Optional
                Points of evaluation. If provided, it is assumed that the given values
                are wrt. the range [0, 1], unless specified otherwise with the 'rng'
                parameter. If not provided, results are returned for the nodes of the
                selected elements. Default is None.
        rng: Iterable, Optional
            Range where the points of evauation are understood. Only for 1d cells.
            Default is [0, 1].
        cells: int or Iterable[int], Optional
            Indices of cells. If not provided, results are returned for all cells.
            Default is None.

        Returns
        -------
        numpy.ndarray
            An array of shape (nE, nP, nSTRE, nRHS).
        """
        cells = self._get_cell_slicer(cells)
        points, _ = self._get_points_and_range(points, rng)
        return self._strains_(cells=cells, points=points)

    def kinetic_strains(
        self,
        *_,
        cells: Union[int, Iterable[int]] = None,
        points: Union[float, Iterable] = None,
        **__,
    ) -> ndarray:
        """
        Returns kinetic strains for one or more cells.

        Parameters
        ----------
        points: float or Iterable, Optional
                 Points of evaluation. If provided, it is assumed that the given values
                 are wrt. the range [0, 1], unless specified otherwise with the 'rng'
                 parameter. If not provided, results are returned for the nodes of the
                 selected elements. Default is None.
        rng: Iterable, Optional
            Range where the points of evauation are understood. Default is [0, 1].
        cells: int or Iterable[int], Optional
            Indices of cells. If not provided, results are returned for all cells.
            Default is None.

        Returns
        -------
        numpy.ndarray
            An array of shape (nE, nSTRE, nRHS), where nE is the number of cells,
            nSTRE is the number of strain components and nRHS is the number of
            load cases. If points of evaluation are specified, the shape of the
            returned array is (nE, nRHS, nP, nSTRE), with an additional axis
            spanning the points.
        """
        key = self.db._dbkey_strain_loads_
        try:
            sloads = self.db._wrapped[key].to_numpy()
        except Exception as e:
            if key not in self.db._wrapped.fields:
                nE = len(self)
                nRHS = self.number_of_load_cases
                nSTRE = self.Material.number_of_material_variables
                sloads = np.zeros((nE, nSTRE, nRHS))
            else:
                raise e
        finally:
            sloads = atleastnd(sloads, 3, back=True)  # (nE, nSTRE=4, nRHS)

        cells = self._get_cell_slicer(cells)

        if isinstance(points, Iterable):
            nP = len(points)
            return explode_kinetic_strains(sloads[cells], nP)
        else:
            return sloads[cells]

    def external_forces(
        self,
        *_,
        cells: Union[int, Iterable[int]] = None,
        target: Union[str, ReferenceFrame] = "local",
        flatten: bool = True,
        **__,
    ) -> ndarray:
        """
        Evaluates :math:`\mathbf{f}_e = \mathbf{K}_e @ \mathbf{u}_e` for one
        or several cells and load cases.

        Parameters
        ----------
        cells: int or Iterable[int], Optional
            Indices of cells. If not provided, results are returned for all cells.
            Default is None.
        target: Union[str, ReferenceFrame], Optional
            The target frame. Default is 'local', which means that the returned
            forces should be understood as coordinates of generalized vectors in
            the local frames of the cells.
        flatten: bool, Optional
            Determines the shape of the resulting array. Default is True.

        Returns
        -------
        numpy.ndarray
            An array of shape (nE, nP * nDOF, nRHS) if 'flatten' is True else
            (nE, nP, nDOF, nRHS).
        """
        dofsol = self.dof_solution(flatten=True, cells=cells)
        # (nE, nNE * nDOF, nRHS)

        cells = self._get_cell_slicer(cells)

        # approximation matrix
        # values -> (nE, nEVAB, nRHS)
        points = np.array(self.Geometry.master_coordinates()).flatten()
        N = self.Material.shape_function_matrix(self, points, rng=[-1, 1])[cells]
        # N -> (nE, nNE, nDOF, nDOF * nNODE)

        # calculate external forces
        K = self.db.elastic_stiffness_matrix
        dofsol = ascont(np.swapaxes(dofsol, 1, 2))  # (nE, nRHS, nEVAB)
        forces = calculate_external_forces_bulk(K, dofsol)
        # forces -> (nE, nRHS, nEVAB)
        forces = approx_element_solution_bulk(forces, N)
        # forces -> (nE, nRHS, nNE, nDOF)
        dofsol = ascont(np.swapaxes(dofsol, 1, 2))  # (nE, nEVAB, nRHS)
        forces = ascont(np.moveaxis(forces, 1, -1))
        # forces ->  (nE, nNE, nDOF, nRHS)

        if target is not None:
            if isinstance(target, str) and target == "local":
                values = forces
            else:
                # transform values to a destination frame, otherwise return
                # the forces are in the local frames of the cells
                values = np.moveaxis(forces, -1, 1)
                nE, nRHS, nP, nDOF = values.shape
                values = values.reshape(nE, nRHS, nP * nDOF)
                dcm = self.direction_cosine_matrix(N=nP, target=target)[cells]
                values = tr_vectors(values, dcm)
                values = values.reshape(nE, nRHS, nP, nDOF)
                values = np.moveaxis(forces, 1, -1)
        else:
            values = forces

        if flatten:
            nE, nP, nX, nRHS = values.shape
            values = values.reshape(nE, nP * nX, nRHS)

        # forces : (nE, nP, nDOF, nRHS)
        return values

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

    def _transform_internal_forces_(
        self,
        forces: ndarray,  # (nE, nP, nSTRE, nRHS)
        *,
        target: Union[str, ReferenceFrame] = "local",
        cells: Union[int, Iterable[int]] = None,
    ) -> ndarray:
        # The implementation here should apply to solidsm and dedicated mechanisms
        # should be implemented at the corresponding base classes
        nDIM = self.Geometry.number_of_spatial_dimensions

        if target is not None:
            if isinstance(target, str) and target == "local":
                values = forces
            else:
                if isinstance(target, str):
                    assert target == "global"
                    target = self.container.source().frame
                else:
                    if not isinstance(target, ReferenceFrame):
                        raise TypeError(
                            "'target' should be an instance of ReferenceFrame"
                        )

                if nDIM == 3:
                    # FIXME use CauchyStressTensor here
                    values = np.moveaxis(forces, -1, -2)
                    nE, nP, nRHS, nSTRE = values.shape
                    dcm = ReferenceFrame(self.frames[cells]).dcm(target=target)
                    dcm = _scatter_element_frames(dcm, nP)
                    values = _map_6x1_to_3x3(values)
                    values = _tr_stresses_3d_bulk_multi(ascont(values), dcm)
                    values = _map_3x3_to_6x1(values)
                    values = np.moveaxis(values, -1, -2)
                else:
                    # FIXME Move this to the dedicated base class
                    values = np.moveaxis(forces, -1, 1)
                    nE, nRHS, nP, nSTRE = values.shape
                    values = values.reshape(nE, nRHS, nP * nSTRE)
                    dcm = self.direction_cosine_matrix(N=nP, target=target)[cells]
                    values = tr_vectors(values, dcm)
                    values = values.reshape(nE, nRHS, nP, nSTRE)
                    values = np.moveaxis(values, 1, -1)
        else:
            values = forces
        return values

    def internal_forces(
        self,
        *_,
        cells: Union[int, Iterable[int]] = None,
        rng: Iterable = None,
        points: Union[float, Iterable] = None,
        flatten: bool = True,
        target: Union[str, ReferenceFrame] = "local",
        **__,
    ) -> ndarray:
        """
        Returns internal forces for many cells and evaluation points.

        Parameters
        ----------
        points: float or Iterable[float], Optional
                Points of evaluation. If provided, it is assumed that the given values
                are wrt. the range [0, 1], unless specified otherwise with the 'rng'
                parameter. If not provided, results are returned for the nodes of the
                selected elements. Default is None.
        rng: Iterable[float], Optional
            Range where the points of evauation are understood. Only for 1d cells.
            Default is [0, 1].
        cells: int or Iterable[int], Optional
            Indices of cells. If not provided, results are returned for all cells.
            Default is None.
        target: Union[str, ReferenceFrame], Optional
            The target frame. Default is 'local', which means that the returned forces
            should be understood as coordinates of generalized vectors in the local
            frames of the cells.
        flatten: bool, Optional
            Determines the shape of the resulting array. Default is True.

        Returns
        -------
        numpy.ndarray
            An array of shape (nE, nP * nSTRE, nRHS) if 'flatten' is True else
            (nE, nP, nSTRE, nRHS).
        """
        cells = self._get_cell_slicer(cells)
        points, _ = self._get_points_and_range(points, rng)

        forces = self._internal_forces_(cells=cells, points=points)
        forces = self._transform_internal_forces_(forces, cells=cells, target=target)
        # forces -> (nE, nP, nSTRE, nRHS)

        if flatten:
            nE, nP, nSTRE, nRHS = forces.shape
            forces = forces.reshape(nE, nP * nSTRE, nRHS)

        return forces

    def global_dof_numbering(self, *_, **kwargs) -> Union[JaggedArray, ndarray]:
        """
        Returns global numbering of the degrees of freedom of the cells.
        """
        topo = kwargs.get("topo", None)
        topo = self.topology().to_numpy() if topo is None else topo
        nDOFN = self.container.number_of_displacement_variables
        try:
            if topo.is_jagged():
                cuts = topo.widths() * nDOFN
                data1d = np.zeros(np.sum(cuts), dtype=int)
                gnum = JaggedArray(data1d, cuts=cuts)
                topo_to_gnum_jagged(topo, gnum, nDOFN)
                return gnum
            else:
                data = topo_to_gnum(topo.to_numpy(), nDOFN)
                return JaggedArray(data)
        except Exception:
            data = topo_to_gnum(topo, nDOFN)
            return JaggedArray(data)

    def elastic_stiffness_matrix(
        self,
        *,
        transform: Optional[bool] = True,
        minval: Optional[float] = 1e-12,
        sparse: Optional[bool] = False,
        recalculate: Optional[bool] = True,
        **kwargs,
    ) -> Union[ndarray, coo_matrix]:
        """
        Returns the elastic stiffness matrix of the cells.

        Parameters
        ----------
        transform: bool, Optional
            If `True`, local matrices are transformed to the global frame.
            Default is `True`.
        minval: float, Optional
            A minimal value for the entries in the main diagonal. Set it to a negative
            value to disable its effect. Default is 1e-12.
        sparse: bool, Optional
            If `True`, the returned object is a sparse COO matrix. Default is False.
        recalculate: bool, Optional
            If `False`, the stiffness matrix is returned from the last calculation if
            possible. Default is `True`, in which case the stiffness matrix is calculated
            from cell data even if it is available from a previous calculation.

        Returns
        -------
        numpy.ndarray or scipy.sparse.coo_matrix
            A sparse SciPy matrix if 'sparse' is `True`, or a 3d numpy array, where the
            elements run along the first axis.
        """
        if (not self.db.has_elastic_stiffness_matrix) or recalculate:
            K = self._elastic_stiffness_matrix_(transform=False, **kwargs)
            assert_min_diagonals_bulk(K, minval)
            self.db.elastic_stiffness_matrix = K
        else:
            K = self.db.elastic_stiffness_matrix

        # if the model has more dofs than the element
        nDOFN = self.container.number_of_displacement_variables
        dofmap = self.Material.dofmap

        if len(dofmap) < nDOFN:
            NNODE = self.Geometry.number_of_nodes
            nE = K.shape[0]
            nX = nDOFN * NNODE
            K_ = np.zeros((nE, nX, nX), dtype=float)
            dofmap = element_dofmap_bulk(dofmap, nDOFN, NNODE)
            K = expand_coeff_matrix_bulk(K, K_, dofmap)
            assert_min_diagonals_bulk(K, minval)

        if transform:
            K = self._transform_coeff_matrix_(K)

        if sparse:
            assert transform, "Must be transformed for a sparse result."
            nP = len(self.pointdata)
            N = nP * self.Material.number_of_displacement_variables
            topo = self.topology().to_numpy()
            gnum = self.global_dof_numbering(topo=topo).to_numpy()
            K = fem_coeff_matrix_coo(K, inds=gnum, N=N, **kwargs)

        return K

    def _elastic_stiffness_matrix_(
        self,
        *,
        transform: Optional[bool] = True,
        quadrature: Optional[Union[Quadrature, None]] = None,
        **kwargs,
    ) -> ndarray:
        if quadrature is None:
            nSTRE = self.Material.number_of_material_variables
            nDOF = self.Material.number_of_displacement_variables
            nNE = self.Geometry.number_of_nodes
            nE = len(self)
            nK = nDOF * nNE

            ec = self.local_coordinates()

            try:
                D = self.Material.elastic_material_stiffness_matrix(self)
            except FieldNotFoundError:
                raise FieldNotFoundError(
                    "The block is missing a valid material definition."
                )

            # the strain displacement matrix is incremented in __elastic_stiffness_matrix__
            K = np.zeros((len(self), nK, nK), dtype=float)
            self.db.strain_displacement_matrix = np.zeros((nE, nSTRE, nDOF * nNE))

            func = partial(
                self._elastic_stiffness_matrix_, transform=False, _D=D, _ec=ec
            )
            for quadrature in self._parse_gauss_data(
                self.Material.quadrature, "stiffness"
            ):
                K += func(quadrature=quadrature)
            self.db.elastic_stiffness_matrix = K

            return self._transform_coeff_matrix_(K) if transform else K

        # in side loop
        ec = kwargs.get("_ec", self.local_coordinates())
        D = kwargs.get("_D", self.Material.elastic_material_stiffness_matrix(self))
        return self.__elastic_stiffness_matrix__(quadrature, ec, D)

    def __elastic_stiffness_matrix__(
        self, q: Quadrature, ec: ndarray, D: ndarray
    ) -> ndarray:
        # the strain displacement matrix is zeroed when starting
        # to build the stiffness matrix
        B, djac = self.__strain_displacement_matrix__(q.pos, ec, True)

        if q.inds is not None:
            # zero out unused indices, only for selective integration
            NSTRE = self.Material.number_of_material_variables
            inds = np.where(~np.in1d(np.arange(NSTRE), q.inds))[0]
            B[:, :, inds, :] = 0.0

        # increment the strain displacement matrix
        _B = self.db.strain_displacement_matrix
        _B += strain_displacement_matrix_bulk2(B, djac, q.weight)
        self.db.strain_displacement_matrix = _B

        return stiffness_matrix_bulk2(D, B, djac, q.weight)

    def __strain_displacement_matrix__(
        self,
        x: Iterable[Number],
        ec: ndarray,
        return_djac: Optional[bool] = False,
    ) -> ndarray:
        shp = self.Material.shape_function_values(self, x)
        dshp = self.Geometry.shape_function_derivatives(x)
        jac = self.jacobian_matrix(dshp=dshp, ecoords=ec)
        djac = self.jacobian(jac=jac)
        dshp = self.Material.shape_function_derivatives(self, x)
        B = self.Material.strain_displacement_matrix(
            self, x, shp=shp, dshp=dshp, jac=jac
        )
        # B (nE, nG, nSTRE, nNODE * nDOF)
        return (B, djac) if return_djac else B

    def consistent_mass_matrix(
        self,
        *args,
        sparse: Optional[bool] = False,
        transform: Optional[bool] = True,
        minval: Optional[float] = 1e-12,
        recalculate: Optional[bool] = True,
        **kwargs,
    ) -> Union[ndarray, coo_matrix]:
        """
        Returns the stiffness-consistent mass matrix of the cells.

        Parameters
        ----------
        transform: bool, Optional
            If True, local matrices are transformed to the global frame.
            Default is True.
        minval: float, Optional
            A minimal value for the entries in the main diagonal. Set it to a
            negative value to diable its effect. Default is 1e-12.
        sparse: bool, Optional
            If True, the returned object is a sparse COO matrix.
            Default is False.
        recalculate: bool, Optional
            If `False`, the mass matrix is returned from the last calculation if
            possible. Default is `True`, in which case the mass matrix is calculated
            from cell data even if it is available from a previous calculation.

        Returns
        -------
        numpy.ndarray or scipy.sparse.coo_matrix
            A sparse SciPy matrix if 'sparse' is True, or a 3d numpy array,
            where the elements run along the first axis.
        """
        if (not self.db.has_mass_matrix) or recalculate:
            M = self._consistent_mass_matrix_(transform=False, **kwargs)
            assert_min_diagonals_bulk(M, minval)
            self.db.mass_matrix = M
        else:
            M = self.db.mass_matrix

        nDOFN = self.container.number_of_displacement_variables
        dofmap = self.Material.dofmap

        # if the model has more dofs than the element
        if len(dofmap) < nDOFN:
            NNODE = self.Geometry.number_of_nodes
            nE = M.shape[0]
            nX = nDOFN * self.Geometry.number_of_nodes
            M_ = np.zeros((nE, nX, nX), dtype=float)
            dofmap = element_dofmap_bulk(dofmap, nDOFN, NNODE)
            M = expand_coeff_matrix_bulk(M, M_, dofmap)
            assert_min_diagonals_bulk(M, minval)

        if transform:
            M = self._transform_coeff_matrix_(M)

        if sparse:
            nP = len(self.pointdata)
            N = nP * self.Material.number_of_displacement_variables
            topo = self.topology().to_numpy()
            gnum = self.global_dof_numbering(topo=topo).to_numpy()
            M = fem_coeff_matrix_coo(M, *args, inds=gnum, N=N, **kwargs)

        return M

    def _consistent_mass_matrix_(
        self,
        *,
        values: Optional[Union[ndarray, None]] = None,
        transform: Optional[bool] = True,
        quadrature: Optional[Union[Quadrature, None]] = None,
        **kwargs,
    ) -> ndarray:
        if quadrature is None:
            nDOF = self.Material.number_of_displacement_variables
            nNE = self.Geometry.number_of_nodes
            nE = len(self)
            nM = nDOF * nNE

            ec = self.local_coordinates()

            if isinstance(values, ndarray):
                dens = values
            else:
                dens = kwargs.get("_dens", self.db.density)

            try:
                areas = self.areas()
            except Exception:
                areas = np.ones((len(self),), dtype=float)

            res = np.zeros((nE, nM, nM), dtype=float)
            func = partial(
                self._consistent_mass_matrix_, _ec=ec, _areas=areas, values=dens
            )
            for quadrature in self._parse_gauss_data(self.Material.quadrature, "mass"):
                res += func(quadrature=quadrature)
            self.db.mass_matrix = res

            return self._transform_coeff_matrix_(res) if transform else res

        ec = kwargs.get("_ec", self.local_coordinates())
        areas = kwargs.get("_areas", np.ones((len(self),), dtype=float))
        rng = np.array([-1.0, 1.0])
        dshp = self.Geometry.shape_function_derivatives(quadrature.pos)
        jac = self.jacobian_matrix(dshp=dshp, ecoords=ec)
        djac = self.jacobian(jac=jac)
        N = self.Material.shape_function_matrix(self, quadrature.pos, rng=rng)
        return mass_matrix_bulk(N, values, areas, djac, quadrature.weight)

    def load_vector(
        self,
        transform: Optional[bool] = True,
        assemble: Optional[bool] = False,
        recalculate: Optional[bool] = True,
        **__,
    ) -> ndarray:
        """
        Builds the equivalent nodal load vector from all sources
        and returns it in either the global frame or cell-local frames.

        Parameters
        ----------
        assemble: bool, Optional
            If True, the values are returned with a matching shape to the total
            system. Default is False.
        transform: bool, Optional
            If True, local matrices are transformed to the global frame.
            Default is True.

        See Also
        --------
        :func:`body_load_vector`
        :func:`strain_load_vector`

        Returns
        -------
        numpy.ndarray
            The nodal load vector for all load cases as a 2d numpy array
            of shape (nX, nRHS), where nX and nRHS are the total number of
            unknowns of the structure and the number of load cases.
        """
        if (not self.db.has_nodal_load_vector) or recalculate:
            options = dict(transform=False, assemble=False, return_zeroes=True)
            f = self.body_load_vector(**options)
            f += self.strain_load_vector(**options)
            self.db.nodal_loads = f
        else:
            f = self.db.nodal_loads

        if transform:
            f = self._transform_nodal_loads_(f)
            # (nE, nRHS, nNE * nDOF) -> (nE, nNE * nDOF, nRHS)

        if assemble:
            assert transform, "Must transform before assembly."
            f = self._assemble_nodal_loads_(f)
            # (nX, nRHS)

        return f

    def strain_load_vector(
        self,
        values: Optional[Union[ndarray, None]] = None,
        *,
        return_zeroes: Optional[bool] = False,
        transform: Optional[bool] = True,
        assemble: Optional[bool] = False,
        **__,
    ) -> ndarray:
        """
        Generates a load vector from strain loads specified for all cells.

        Parameters
        ----------
        values: numpy.ndarray, Optional
            Strain loads as a 3d numpy array of shape (nE, nS, nRHS).
            The array must contain values for all cells (nE), strain
            components (nS) and load cases (nL).
        return_zeroes: bool, Optional
            Controls what happends if there are no strain loads provided.
            If True, a zero array is retured with correct shape, otherwise None.
            Default is False.
        transform: bool, Optional
            If True, local matrices are transformed to the global frame.
            Default is True.
        assemble: bool, Optional
            If True, the values are returned with a matching shape to the total
            system. Default is False.

        See Also
        --------
        :func:`load_vector`
        :func:`body_load_vector`

        Returns
        -------
        numpy.ndarray
            The equivalent load vector.
        """
        dbkey = self.db._dbkey_strain_loads_
        try:
            if values is None:
                values = self.db._wrapped[dbkey].to_numpy()
        except Exception as e:
            if dbkey not in self.db._wrapped.fields:
                if not return_zeroes:
                    return None
                nRHS = self.number_of_load_cases
                nE = len(self)
                nSTRE = self.Material.number_of_material_variables
                values = np.zeros((nE, nSTRE, nRHS))
            else:
                raise e
        finally:
            values = atleastnd(values, 3, back=True)  # (nE, nSTRE, nRHS)

        nodal_loads = self._strain_load_vector_(values)
        # (nE, nTOTV, nRHS)

        # if the model has more dofs than the element
        nDOFN = self.container.number_of_displacement_variables
        dofmap = self.Material.dofmap
        if len(dofmap) < nDOFN:
            nNODE = self.Geometry.number_of_nodes
            nE, _, nRHS = nodal_loads.shape
            nX = nDOFN * nNODE
            f_ = np.zeros((nE, nX, nRHS), dtype=float)
            dofmap = element_dofmap_bulk(dofmap, nDOFN, nNODE)
            nodal_loads = expand_load_vector_bulk(nodal_loads, f_, dofmap)

        if transform:
            nodal_loads = self._transform_nodal_loads_(nodal_loads)
            # (nE, nRHS, nNE * nDOF) -> (nE, nNE * nDOF, nRHS)

        if assemble:
            assert transform, "Must transform before assembly."
            nodal_loads = self._assemble_nodal_loads_(nodal_loads)
            # (nX, nRHS)

        return nodal_loads

    def _strain_load_vector_(self, values: ndarray) -> ndarray:
        if not self.db.has_strain_displacement_matrix:
            self.elastic_stiffness_matrix(transform=False)
        B = self.db.strain_displacement_matrix  # (nE, nSTRE, nNODE * nDOF)
        D = self.Material.elastic_material_stiffness_matrix(self)  # (nE, nSTRE, nSTRE)
        BTD = unit_strain_load_vector_bulk(D, B)  # (nE, nTOTV, nSTRE)
        # values : # (nE, nSTRE, nRHS)
        values = np.swapaxes(values, 1, 2)  # (nE, nRHS, nSTRE)
        nodal_loads = strain_load_vector_bulk(BTD, ascont(values))
        return nodal_loads  # (nE, nTOTV, nRHS)

    def _get_body_loads(self, return_zeroes: bool = True) -> ndarray:
        nNE = self.Geometry.number_of_nodes
        dbkey = self.db._dbkey_body_loads_
        try:
            values = self.db._wrapped[dbkey].to_numpy()
        except Exception as e:
            if dbkey not in self.db._wrapped.fields:
                if not return_zeroes:
                    return None
                nRHS = self.number_of_load_cases
                nE = len(self)
                nDOF = self.Material.number_of_displacement_variables
                values = np.zeros((nE, nNE, nDOF, nRHS))
            else:
                raise e
        finally:
            values = atleastnd(values, 4, back=True)
        return values  # (nE, nNE, nDOF, nRHS)

    def body_load_vector(
        self,
        values: ndarray = None,
        *,
        constant: bool = False,
        return_zeroes: bool = False,
        transform: bool = True,
        assemble: bool = False,
        **__,
    ) -> ndarray:
        """
        Builds the equivalent discrete representation of body loads
        and returns it in either the global frame or cell-local frames.

        Parameters
        ----------
        values: numpy.ndarray, Optional
            Body load values for all cells. Default is None.
        constant: bool, Optional
            Set this True if the input represents a constant load.
            Default is False.
        assemble: bool, Optional
            If True, the values are returned with a matching shape to the total
            system. Default is False.
        return_zeroes: bool, Optional
            Controls what happends if there are no strain loads provided.
            If True, a zero array is retured with correct shape, otherwise None.
            Default is False.
        transform: bool, Optional
            If True, local matrices are transformed to the global frame.
            Default is True.

        See Also
        --------
        :func:`load_vector`
        :func:`strain_load_vector`

        Returns
        -------
        numpy.ndarray
            The nodal load vector for all load cases as a 2d numpy array
            of shape (nX, nRHS), where nX and nRHS are the total number of
            unknowns of the structure and the number of load cases.
        """
        nNE = self.Geometry.number_of_nodes
        if values is None:
            values = self._get_body_loads(return_zeroes=return_zeroes)
        values = atleastnd(values, 4, back=True)
        # (nE, nNE, nDOF, nRHS)

        # prepare data to shape (nE, nNE * nDOF, nRHS)
        if constant:
            values = atleastnd(values, 3, back=True)  # (nE, nDOF, nRHS)
            # np.insert(values, 1, values, axis=1)
            nE, nDOF, nRHS = values.shape
            values_ = np.zeros((nE, nNE, nDOF, nRHS), dtype=values.dtype)
            for i in range(nNE):
                values_[:, i, :, :] = values
            values = values_
        values = atleastnd(values, 4, back=True)  # (nE, nNE, nDOF, nRHS)
        nE, _, nDOF, nRHS = values.shape
        # (nE, nNE, nDOF, nRHS) -> (nE, nNE * nDOF, nRHS)
        values = values.reshape(nE, nNE * nDOF, nRHS)
        values = ascont(values)
        nodal_loads = self.integrate_body_loads(values)
        # (nE, nNE * nDOF, nRHS)

        # if the model has more dofs than the element
        nDOFN = self.container.number_of_displacement_variables
        dofmap = self.Material.dofmap
        if len(dofmap) < nDOFN:
            nNODE = self.Geometry.number_of_nodes
            nE, _, nRHS = nodal_loads.shape
            nX = nDOFN * nNODE
            f_ = np.zeros((nE, nX, nRHS), dtype=float)
            dofmap = element_dofmap_bulk(dofmap, nDOFN, nNODE)
            nodal_loads = expand_load_vector_bulk(nodal_loads, f_, dofmap)

        if transform:
            nodal_loads = self._transform_nodal_loads_(nodal_loads)
            # (nE, nRHS, nNE * nDOF) -> (nE, nNE * nDOF, nRHS)

        if assemble:
            assert transform, "Must transform before assembly."
            nodal_loads = self._assemble_nodal_loads_(nodal_loads)
            # (nX, nRHS)

        return nodal_loads

    def integrate_body_loads(self, values: ndarray) -> ndarray:
        """
        Returns nodal representation of body loads.

        Parameters
        ----------
        values: numpy.ndarray
            2d or 3d numpy float array of material densities of shape
            (nE, nNE * nDOF, nRHS) or (nE, nNE * nDOF), where nE, nNE,
            nDOF and nRHS stand for the number of elements, nodes per
            element, number of degrees of freedom and number of load cases
            respectively.

        Returns
        -------
        numpy.ndarray
            An array of shape (nE, nNE * 6, nRHS).

        Notes
        -----
        1) The returned array is always 3 dimensional, even if there is only one
        load case.
        2) Reimplemented for elements with Hermite basis functions.

        See Also
        --------
        :func:`~body_load_vector_bulk`
        """
        values = atleastnd(values, 3, back=True)
        # (nE, nNE * nDOF, nRHS) -> (nE, nRHS, nNE * nDOF)
        values = np.swapaxes(values, 1, 2)
        values = ascont(values)

        quadrature: Quadrature = next(
            self._parse_gauss_data(self.Material.quadrature, "full")
        )

        N = self.Material.shape_function_matrix(self, quadrature.pos)
        # (nP, nDOF, nDOF * nNE) for constant metric elements
        # (nE, nP, nDOF, nDOF * nNE) for variable metric elements
        dshp = self.Geometry.shape_function_derivatives(quadrature.pos)
        # (nP, nNE==nSHP, nD)
        ecoords = self.local_coordinates()
        # (nE, nNE, nD)
        jac = self.jacobian_matrix(dshp=dshp, ecoords=ecoords)
        # (nE, nP, nD, nD)
        djac = self.jacobian(jac=jac)
        # (nE, nG)

        if len(N.shape) == 3:  # constant metric elements
            f = body_load_vector_bulk_cm(values, N, djac, quadrature.weight)
        elif len(N.shape) == 4:  # variable metric elements
            f = body_load_vector_bulk_vm(values, N, djac, quadrature.weight)
        # (nE, nEVAB, nRHS)

        return f

    def condensate(
        self,
        K: Optional[Union[ndarray, None]] = None,
        f: Optional[Union[ndarray, None]] = None,
        M: Optional[Union[ndarray, None]] = None,
        fixity: Optional[Union[ndarray, None]] = None,
        assertmin: bool = True,
    ) -> Tuple[ndarray, ndarray, Union[ndarray, None]]:
        """
        Applies static condensation to account for cell fixity.

        References
        ----------
        .. [1] Duan Jin, Li-Yun-gui "About the Finite Element
           Analysis for Beam-Hinged Frame," Advances in Engineering
           Research, vol. 143, pp. 231-235, 2017.
        """
        if fixity is None:
            if not self.db.has_fixity:
                return
            else:
                fixity = self.db.fixity

        assert isinstance(fixity, ndarray)
        nE, nNE, nDOF = fixity.shape
        fixity = fixity.reshape(nE, nNE * nDOF)

        inplace = K is None and f is None and M is None

        if inplace:
            K = self.db.elastic_stiffness_matrix
            f = self.db.nodal_loads

            if self.db.has_mass_matrix:
                M = self.db.mass_matrix
            else:
                M = None

        K, f, M = condensate_bulk(fixity, K, f, M, assertmin)

        if inplace:
            self.db.elastic_stiffness_matrix = K
            self.db.nodal_loads = f

            if self.db.has_mass_matrix:
                self.db.mass_matrix = M

        return K, f, M

    def _transform_coeff_matrix_(
        self, A: ndarray, *args, invert: bool = False, **kwargs
    ) -> ndarray:
        """
        Transforms element coefficient matrices (eg. the stiffness or the
        mass matrix) from local to global.

        Parameters
        ----------
        *args
            Forwarded to :func:`direction_cosine_matrix`
        **kwargs
            Forwarded to :func:`direction_cosine_matrix`
        A: numpy.ndarray
            The coefficient matrix in the source frame.
        invert: bool, Optional
            If True, the DCM matrices are transposed before transformation.
            This makes this function usable in both directions.
            Default is False.

        Returns
        -------
        numpy.ndarray
            The coefficient matrix in the target frame.
        """
        # DCM from local to global
        dcm = self.direction_cosine_matrix(*args, **kwargs)
        return A if dcm is None else tr_matrices(A, dcm, invert)

    def _transform_nodal_loads_(self, nodal_loads: ndarray) -> ndarray:
        """
        Transforms discrete nodal loads to the global frame.

        Parameters
        ----------
        nodal_loads: numpy.ndarray
            A 3d array of shape (nE, nEVAB, nRHS).

        Returns
        -------
        numpy.ndarray
            A numpy array of shape (nE, nEVAB, nRHS).
        """
        dcm = self.direction_cosine_matrix(target="global")
        # (nE, nNE * nDOF, nRHS) -> (nE, nRHS, nNE * nDOF)
        nodal_loads = np.swapaxes(nodal_loads, 1, 2)
        nodal_loads = ascont(nodal_loads)
        nodal_loads = tr_vectors(nodal_loads, dcm)
        nodal_loads = np.swapaxes(nodal_loads, 1, 2)
        # (nE, nRHS, nNE * nDOF) -> (nE, nNE * nDOF, nRHS)
        return nodal_loads

    def _assemble_nodal_loads_(self, nodal_loads: ndarray) -> ndarray:
        """
        Assembles the nodal load vector for multiple load cases.

        Parameters
        ----------
        nodal_loads: numpy.ndarray
            A 3d array of shape (nE, nEVAB, nRHS).

        Returns
        -------
        numpy.ndarray
            A numpy array of shape (nX, nRHS), where nX is the total
            number of unknowns in the total structure.
        """
        topo = self.topology().to_numpy()
        gnum = self.global_dof_numbering(topo=topo).to_numpy()
        nX = len(self.pointdata) * self.container.number_of_displacement_variables
        return assemble_load_vector(nodal_loads, gnum, nX)  # (nX, nRHS)

    def masses(self, *_, density: ndarray = None, **__) -> ndarray:
        """
        Returns the masses of the cells in the block.
        """
        if isinstance(density, ndarray):
            dens = density
        else:
            dens = self.db.density
        measures = self.measures()
        return dens * measures

    def mass(self, *args, **kwargs) -> float:
        """
        Returns the total mass of the block. All parameters are forwarded
        to :func:`masses`.
        """
        return np.sum(self.masses(*args, **kwargs))

    def utilization(self, *args, **kwargs) -> Union[xr.DataArray, ndarray]:
        raise NotImplementedError

    def maximum_utilization(self, *args, **kwargs) -> Union[xr.DataArray, ndarray]:
        """
        Retruns the maximum utilization of the block for every load case. The parameters
        are the same as for `utilization`.
        """
        utils = self.utilization(*args, dtype=xr.DataArray, **kwargs)
        dims = filter(lambda d: d not in ["case"], utils.dims)
        return utils.max(dim=dims)

    def maximum_utilizations(self, *args, **kwargs) -> Union[xr.DataArray, ndarray]:
        """
        Retruns the maximum utilization of the block for every cell and load case.
        The parameters are the same as for `utilization`.
        """
        utils = self.utilization(*args, dtype=xr.DataArray, **kwargs)
        dims = filter(lambda d: d not in ["index", "case"], utils.dims)
        return utils.max(dim=dims)
