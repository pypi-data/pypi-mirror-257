from typing import (
    Union,
    List,
    Iterable,
    Collection,
    Generic,
    TypeVar,
    Hashable,
    ClassVar,
)
import logging

from scipy.sparse import coo_matrix
import numpy as np
from numpy import ndarray

from sigmaepsilon.math import atleast3d
from sigmaepsilon.math.linalg.sparse import JaggedArray
from sigmaepsilon.mesh import PolyData

from .pointdata import PointData
from .finiteelement import FiniteElement
from ..dofmap import DOF
from ..typing import (
    ABC_FemMesh,
    PointDataProtocol,
    FiniteElementProtocol,
)
from ..utils.preproc.preproc import (
    nodal_load_vector,
    essential_penalty_matrix,
    nodal_mass_matrix,
)
from ..constants import DEFAULT_DIRICHLET_PENALTY


T = TypeVar("T", bound="FemMesh")
PD = TypeVar("PD", bound=PointDataProtocol)
CD = TypeVar("CD", bound=FiniteElementProtocol)


class FemMesh(PolyData[PD, CD], ABC_FemMesh):
    """
    A descendant of :class:`~sigmaepsilon.mesh.PolyData` to handle polygonal meshes for
    the **Finite Element Method**.

    Parameters
    ----------
    pd: PointDataProtocol or CellDataProtocol, Optional
        A PolyData or a CellData instance. Default is None.
    cd: PointDataProtocol or CellDataProtocol, Optional
        A PolyData or a CellData instance. Default is None.

    Note
    ----
    The suggested way of usage is to create the pointdata and celldata
    objects in advance, and provide them as the first argument when building
    the model.

    Examples
    --------
    >>> from sigmaepsilon.solid import FemMesh
    >>> from sigmaepsilon.mesh.grid import grid
    >>> size = Lx, Ly, Lz = 100, 100, 100
    >>> shape = nx, ny, nz = 10, 10, 10
    >>> coords, topo = grid(size=size, shape=shape, eshape='H27')
    >>> pd = FemMesh(coords=coords)
    >>> pd['A']['Part1'] = FemMesh(topo=topo[:10])
    >>> pd['B']['Part2'] = FemMesh(topo=topo[10:-10])
    >>> pd['C']['Part3'] = FemMesh(topo=topo[-10:])

    See also
    --------
    :class:`~sigmaepsilon.mesh.PolyData`
    :class:`~sigmaepsilon.mesh.CellData`
    """

    displacement_variables = ("UX", "UY", "UZ", "ROTX", "ROTY", "ROTZ")
    number_of_displacement_variables: ClassVar[Union[int, None]] = None

    _point_class_ = PointData  # used in sigmaepsilon.mesh

    def __init__(
        self, *args, cell_fields: dict = None, point_fields: dict = None, **kwargs
    ):
        point_fields = {} if point_fields is None else point_fields
        cell_fields = {} if cell_fields is None else cell_fields
        super().__init__(
            *args, point_fields=point_fields, cell_fields=cell_fields, **kwargs
        )
        self._create_dofmap()

    def __getitem__(self, key) -> "FemMesh":
        return super().__getitem__(key)

    @property
    def pd(self) -> PD:
        """
        Returns the attached pointdata.

        See Also
        --------
        class:`sigmaepsilon.solid.fem.pointdata.PointData`
        """
        return self.pointdata

    @property
    def cd(self) -> CD:
        """
        Returns the attached celldata.

        See Also
        --------
        class:`~sigmaepsilon.solid.fem.cells.elem.FiniteElement`
        class:`~sigmaepsilon.solid.fem.cells.celldata.CellData`
        """
        return self.celldata

    @property
    def number_of_load_cases(self) -> int:
        """
        Returns the number of load cases in the model.
        """
        try:
            if len(self.pointdata.loads.shape) == 2:
                nRHS = 1
            else:
                nRHS = self.pointdata.loads.shape[-1]
            return nRHS
        except Exception:
            raise Exception(
                "No loads are defined. Check for a failed definition or refer to the documentation."
            )

    def cellblocks(self, *args, **kwargs) -> Collection["FemMesh"]:
        """
        Returns an iterable over blocks with cell data.
        """
        return filter(lambda i: i.celldata is not None, self.blocks(*args, **kwargs))

    def is_jagged(self) -> bool:
        """
        Returns True if the mesh is jagged, i.e. if it consists of blocks with
        inconsistent matrix shapes, thus prohibiting bulk calculations.
        """
        cell_class_id = map(
            lambda b: id(b.cd.__class__), self.cellblocks(inclusive=True)
        )
        return len(set(cell_class_id)) > 1

    def is_regular(self, **kwargs) -> bool:
        """
        Returns true if the numbering of the nodes in the mesh (hence the numbering
        of the dofs) is regular, according to the following criteria:
            * the smallest index is 0
            * the largest index equals the number of nodes in the mesh - 1
            * the number of unique indices equals the number of nodes in the mesh
        """
        coords = kwargs.get("_coords", self.root.coords())
        topo = kwargs.get("_topo", self.topology())
        imin, imax = np.min(topo), np.max(topo)
        nP = len(coords)
        c0 = imin == 0
        c1 = imax == (nP - 1)
        c2 = len(np.unique(topo)) == nP
        return all([c0, c1, c2])

    def cells_coords(
        self, *args, points: Iterable = None, cells: Iterable = None, **kwargs
    ) -> Union[ndarray, List[ndarray]]:
        """
        Returns the coordinates of the cells as a 3d numpy array if the
        subblocks form a regular mesh, or a list of such arrays.
        """
        if points is None and cells is None:
            return super().cells_coords(*args, **kwargs)
        else:
            blocks = self.cellblocks(inclusive=True)
            kwargs.update(points=points)
            if cells is not None:
                kwargs.update(cells=cells)
                res = {}

                def foo(b: FemMesh[PointData, FiniteElement]):
                    return b.cd.coords(*args, **kwargs)

                [res.update(d) for d in map(foo, blocks)]
                return res
            else:

                def foo(b: FemMesh[PointData, FiniteElement]):
                    return b.cd.coords(*args, **kwargs)

                return np.vstack(list(map(foo, blocks)))

    def element_dof_numbering(
        self, *args, return_inds: bool = False, jagged: bool = None, **kwargs
    ) -> Union[ndarray, JaggedArray]:
        """
        Returns global ids of the local degrees of freedoms for each cell
        as either a `NumPy` or an `Awkward` array.

        Parameters
        ----------
        return_inds: bool, Optional
            Returns the indices of the points. Default is False.
        jagged: bool, Optional
            If True, returns the topology as a :class:`TopologyArray`
            instance, even if the mesh is regular. Default is False.

        Returns
        -------
        Union[numpy.ndarray, JaggedArray]
            A 2d integer array.
        """
        blocks = list(self.cellblocks(*args, inclusive=True, **kwargs))
        gnum = list(map(lambda i: i.cd.global_dof_numbering(), blocks))
        widths = np.concatenate(list(map(lambda arr: arr.widths(), gnum)))
        jagged = False if not isinstance(jagged, bool) else jagged
        needs_jagged = not np.all(widths == widths[0])
        if jagged or needs_jagged:
            gnum = np.vstack(gnum)
            if return_inds:
                inds = list(map(lambda i: i.celldata.id, blocks))
                return gnum, np.concatenate(inds)
            else:
                return gnum
        else:
            gnum = np.vstack([arr.to_numpy() for arr in gnum])
            if return_inds:
                inds = list(map(lambda i: i.celldata.id, blocks))
                return gnum, np.concatenate(inds)
            else:
                return gnum

    def element_fixity(self) -> ndarray:
        """
        Returns element fixity data.
        """
        fixity = []
        for b in self.cellblocks(inclusive=True):
            if b.has_fixity:
                fixity.append(b.cd.fixity.astype(float))
            else:
                nE, nNE, nDOF = (
                    len(b.cd),
                    b.cd.Geometry.number_of_nodes,
                    self.number_of_displacement_variables,
                )
                fixity.append(np.ones(nE, nNE, nDOF))
        return np.vstack(fixity)

    def direction_cosine_matrix(self, target: str = "global") -> ndarray:
        """
        Returns the DCM matrix for all elements in the block.

        Parameters
        ----------
        target: Union[ndarray, str, ReferenceFrame], Optional
            A target frame. The string 'global' refers to the global
            frame of the mesh. Default is None.
        """
        blocks = self.cellblocks(inclusive=True)

        def foo(b: FemMesh[PointData, FiniteElement]):
            return b.cd.direction_cosine_matrix(target=target)

        return np.vstack(list(map(foo, blocks)))

    def elastic_stiffness_matrix(
        self,
        *,
        eliminate_zeros: bool = True,
        sum_duplicates: bool = True,
        sparse: bool = False,
        transform: bool = True,
        recalculate: bool = True,
        **kwargs,
    ) -> Union[ndarray, coo_matrix]:
        """
        Returns the elastic stiffness matrix in dense or sparse format.

        Parameters
        ----------
        sparse: bool, Optional
            If True, the result is a sparse matrix. Default is False.
        eliminate_zeros : bool, Optional
            Eliminates zero entries. Only if 'sparse' is True. Default is True.
        sum_duplicates : bool, Optional
            Sums duplicate entries. Only if 'sparse' is True. Default is True.
        transform : bool, Optional
            If True, local matrices are transformed to the global frame.
            Default is True.
        recalculate: bool, Optional
            Whether to recalculate the values when they are available from a previous
            evaluation. Default is True.

        Returns
        -------
        numpy.ndarray or scipy.sparse.coo_matrix
        """
        blocks = self.cellblocks(inclusive=True)
        if sparse:
            assert transform, "Must transform for sparse output."

            def foo(b: FemMesh[PointData, FiniteElement]):
                return b.cd.elastic_stiffness_matrix(
                    sparse=True, transform=True, recalculate=recalculate
                )

            K = np.sum(list(map(foo, blocks))).tocoo()
            if eliminate_zeros:
                K.eliminate_zeros()
            if sum_duplicates:
                K.sum_duplicates()
            return K
        else:

            def foo(b: FemMesh[PointData, FiniteElement]):
                return b.cd.elastic_stiffness_matrix(
                    transform=transform, recalculate=recalculate
                )

            if kwargs.get("_jagged", self.is_jagged()):
                shaper = map(
                    lambda x: x.reshape(x.shape[0], x.shape[1] * x.shape[1]),
                    map(foo, blocks),
                )
                mapper = map(lambda x: JaggedArray(x, force_numpy=False), shaper)
            else:
                mapper = map(foo, blocks)
            return np.vstack(list(mapper))

    def masses(self, *args, **kwargs) -> ndarray:
        """
        Returns masses of the cells as a 1d numpy array.
        """
        blocks = self.cellblocks(*args, inclusive=True, **kwargs)

        def foo(b: FemMesh[PointData, FiniteElement]):
            return b.cd.masses()

        vmap = map(foo, blocks)
        return np.concatenate(list(vmap))

    def mass(self, *args, **kwargs) -> float:
        """
        Returns the total mass of the structure.
        """
        return np.sum(self.masses(*args, **kwargs))

    def consistent_mass_matrix(
        self,
        *,
        eliminate_zeros: bool = True,
        sum_duplicates: bool = True,
        sparse: bool = False,
        transform: bool = True,
        recalculate: bool = True,
        **kwargs,
    ) -> Union[ndarray, coo_matrix]:
        """
        Returns the stiffness-consistent mass matrix as a dense or a sparse
        matrix.

        Parameters
        ----------
        sparse : bool, Optional
            If True, the result is a sparse matrix. Default is False.
        eliminate_zeros : bool, Optional
            Eliminates zero entries. Only if 'sparse' is True. Default is True.
        sum_duplicates : bool, Optional
            Sums duplicate entries. Only if 'sparse' is True. Default is True.
        transform : bool, Optional
            If True, local matrices are transformed to the global frame.
            Default is True.
        recalculate: bool, Optional
            Whether to recalculate the values when they are available from a previous
            evaluation. Default is True.

        Returns
        -------
        numpy.ndarray or scipy.sparse.coo_matrix
            The mass matrix as a 3d dense or a 2d sparse array.
        """
        blocks = self.cellblocks(inclusive=True)
        if sparse:
            assert transform, "Must transform for sparse output."

            def foo(b: FemMesh[PointData, FiniteElement]):
                return b.cd.consistent_mass_matrix(
                    sparse=True, transform=True, recalculate=recalculate, **kwargs
                )

            M = np.sum(list(map(foo, blocks))).tocoo()
            if eliminate_zeros:
                M.eliminate_zeros()
            if sum_duplicates:
                M.sum_duplicates()
            return M
        else:

            def foo(b: FemMesh[PointData, FiniteElement]):
                return b.cd.consistent_mass_matrix(
                    transform=transform, recalculate=recalculate, **kwargs
                )

            if kwargs.get("_jagged", self.is_jagged()):
                shaper = map(
                    lambda x: x.reshape(x.shape[0], x.shape[1] * x.shape[1]),
                    map(foo, blocks),
                )
                mapper = map(lambda x: JaggedArray(x, force_numpy=False), shaper)
            else:
                mapper = map(foo, blocks)
            return np.vstack(list(mapper))

    def mass_matrix(
        self,
        *,
        eliminate_zeros: bool = True,
        sum_duplicates: bool = True,
        recalculate: bool = True,
    ) -> coo_matrix:
        """
        Returns the mass matrix in coo format.The resulting matrix is the
        sum of the consistent mass matrix and the nodal mass matrix.

        Parameters
        ----------
        eliminate_zeros : bool, Optional
            Eliminates zero entries. Default is True.
        sum_duplicates : bool, Optional
            Sums duplicate entries. Default is True.
        recalculate: bool, Optional
            Whether to recalculate the values when they are available from a previous
            evaluation. Default is True.

        Returns
        -------
        scipy.sparse.coo_matrix
            The mass matrix in sparse COO format.
        """
        # distributed masses (cells)
        M = self.consistent_mass_matrix(
            sparse=True,
            transform=True,
            eliminate_zeros=False,
            sum_duplicates=False,
            recalculate=recalculate,
        )
        # nodal masses
        M += self.nodal_mass_matrix(eliminate_zeros=False, sum_duplicates=False)
        if eliminate_zeros:
            M.eliminate_zeros()
        if sum_duplicates:
            M.sum_duplicates()
        return M.tocoo()

    def nodal_mass_matrix(
        self, *, eliminate_zeros: bool = False, sum_duplicates: bool = False, **kw
    ):
        """
        Returns the mass matrix from nodal masses only, in coo format.

        Parameters
        ----------
        eliminate_zeros : bool, Optional
            Eliminates zero entries. Default is True.
        sum_duplicates : bool, Optional
            Sums duplicate entries. Default is True.

        Returns
        -------
        scipy.sparse.coo_matrix
            The nodal mass matrix in sparse COO format.
        """
        pd = self.root.pointdata
        nN = len(pd)
        nDOF = self.number_of_displacement_variables
        try:
            m = pd.mass
            M = nodal_mass_matrix(
                values=m,
                eliminate_zeros=eliminate_zeros,
                sum_duplicates=sum_duplicates,
                ndof=nDOF,
            )
            return M
        except Exception:
            nX = nN * nDOF
            return coo_matrix(shape=(nX, nX))

    def essential_penalty_matrix(
        self,
        fixity: ndarray = None,
        *,
        eliminate_zeros: bool = True,
        sum_duplicates: bool = True,
        penalty: float = DEFAULT_DIRICHLET_PENALTY,
    ) -> coo_matrix:
        """
        A penalty matrix that enforces Dirichlet boundary conditions.
        Returns a scipy sparse matrix in coo format.

        Parameters
        ----------
        fixity: numpy.ndarray, Optional
            The fixity values as a 2d array. The length of the first axis must
            equal the number of nodes, the second the number of DOFs of the model.
            If not specified, the data is assumed to be stored in the attached
            pointdata with the same key. Default is None.
        penalty: float, Optional
            The Courant-type penalty value.
            Default is `sigmaepsilon.solid.fem.constants.DEFAULT_DIRICHLET_PENALTY`.
        eliminate_zeros: bool, Optional
            Eliminates zeros from the matrix. Default is True.
        eliminate_zeros: bool, Optional
            Summs duplicate entries in the matrix. Default is True.

        Returns
        -------
        scipy.sparse.coo_matrix
        """
        root = self.root
        pd = root.pointdata
        N = len(pd) * root.number_of_displacement_variables
        K_coo = coo_matrix(([0.0], ([0], [0])), shape=(N, N))
        try:
            fixity = pd.fixity
            K_coo += essential_penalty_matrix(
                fixity=fixity,
                pfix=penalty,
                eliminate_zeros=eliminate_zeros,
                sum_duplicates=sum_duplicates,
            )
        except AttributeError:
            logging.info("No FIXITY information in pointdata.")
        except Exception as e:
            logging.error(f"Exception {e} occured", exc_info=True)
        return K_coo.tocoo()

    def nodal_load_vector(self, *args, **kwargs) -> ndarray:
        """
        Returns the nodal load vector.

        Returns
        -------
        numpy.ndarray
        """
        # concentrated nodal loads
        nodal_data = self.root.pointdata.loads
        nodal_data = atleast3d(nodal_data, back=True)
        # (nP, nDOF, nRHS)
        res = nodal_load_vector(nodal_data)
        return res

    def cell_load_vector(
        self,
        *,
        transform: bool = True,
        assemble: bool = False,
        recalculate: bool = True,
        **kwargs,
    ) -> ndarray:
        """
        Returns the nodal load vector from body and strain loads.

        Parameters
        ----------
        assemble: bool, Optional
            If True, the values are returned with a matching shape to
            the total system. Default is False.
        transform: bool, Optional
            If True, local matrices are transformed to the global frame.
            Default is False.

        Returns
        -------
        numpy.ndarray
            The shape depends on the arguments.
        """
        if assemble:
            assert transform, "Must transform before assembly."

        blocks = list(self.cellblocks(inclusive=True))
        params = dict(transform=transform, assemble=assemble, recalculate=recalculate)
        params.update(**kwargs)

        def foo(b: FemMesh[PointData, FiniteElement]):
            return b.cd.load_vector(**params)

        if assemble:
            return sum(map(foo, blocks))
        else:
            return np.vstack(list(map(foo, blocks)))

    def prostproc_dof_solution(self, *args, **kwargs) -> None:
        """
        Calculates approximate solution of the primary variables as a list
        of arrays for each block in the mesh.
        """
        blocks = self.cellblocks(inclusive=True)
        dofsol = self.root.pointdata.dofsol

        def foo(b: FemMesh[PointData, FiniteElement]):
            return b.cd.prostproc_dof_solution(dofsol=dofsol)

        list(map(foo, blocks))

    def condensate_cell_fixity(self) -> "FemMesh":
        """
        Performs static condensation of the system equations to account for
        cell fixity. Returns the mesh object for continuation.
        """
        [b.cd.condensate() for b in self.cellblocks(inclusive=True)]
        return self

    def nodal_dof_solution(self, *, flatten: bool = False, **kw) -> ndarray:
        """
        Returns nodal degree of freedom solution.

        Parameters
        ----------
        flatten: bool, Optional
            If True, nodal results are flattened. Default is False.

        Returns
        -------
        numpy.ndarray
        """
        dofsol = self.root.pointdata.dofsol
        if flatten:
            if len(dofsol.shape) == 2:
                return dofsol.flatten()
            else:
                nN, nDOFN, nRHS = dofsol.shape
                return dofsol.reshape((nN * nDOFN, nRHS))
        else:
            return dofsol

    def cell_dof_solution(
        self, *args, cells: Iterable = None, flatten: bool = True, **kwargs
    ) -> ndarray:
        """
        Returns degree of freedom solution for each cell or just some.

        Parameters
        ----------
        cells: Iterable, Optional
            Indices of cells for which data is requested.
            If specified, the result is a dictionary with the indices
            being the keys. Default is None.
        flatten: bool, Optional
            If True, nodal results are flattened. Default is True.

        Returns
        -------
        numpy.ndarray or dict
            A dictionary if cell indices are specified, or a NumPy array.
        """
        kwargs.update(flatten=flatten)
        if cells is not None:

            def f(b: FemMesh[PointData, FiniteElement], cid: int):
                return b.cd.dof_solution(*args, cells=[cid], **kwargs)[0]

            boc = self.blocks_of_cells(i=cells)
            return {cid: f(boc[cid], cid) for cid in cells}
        else:
            blocks = self.cellblocks(inclusive=True)

            def foo(b: FemMesh[PointData, FiniteElement]):
                return b.cd.dof_solution(*args, **kwargs)

            return np.vstack(list(map(foo, blocks)))

    def strains(self, *args, cells: Iterable = None, **kwargs) -> ndarray:
        """
        Returns strains for each cell or just some.

        Parameters
        ----------
        cells: Iterable, Optional
            Indices of cells for which data is requested.
            If specified, the result is a dictionary with the indices
            being the keys. Default is None.
        flatten: bool, Optional
            If True, nodal results are flattened. Default is True.

        Returns
        -------
        numpy.ndarray or dict
            A dictionary if cell indices are specified, or a NumPy array.
        """
        kwargs.update()
        if cells is not None:

            def f(b: FemMesh[PointData, FiniteElement], cid: int):
                return b.cd.strains(*args, cells=[cid], **kwargs)[0]

            boc = self.blocks_of_cells(i=cells)
            return {cid: f(boc[cid], cid) for cid in cells}
        else:
            blocks = self.cellblocks(inclusive=True)

            def foo(b: FemMesh[PointData, FiniteElement]):
                return b.cd.strains(*args, **kwargs)

            return np.vstack(list(map(foo, blocks)))

    def external_forces(
        self, *args, cells: Iterable = None, flatten: bool = True, **kwargs
    ) -> ndarray:
        """
        Returns external forces for each cell or just some.

        Parameters
        ----------
        cells: Iterable, Optional
            Indices of cells for which external forces are requested.
            If specified, the result is a dictionary with the indices
            being the keys. Default is None.
        flatten: bool, Optional
            If True, nodal results are flattened. Default is True.

        Returns
        -------
        numpy.ndarray or dict
            A dictionary if cell indices are specified, or a NumPy array.
        """
        kwargs.update(flatten=flatten)
        if cells is not None:

            def f(b: FemMesh[PointData, FiniteElement], cid: int):
                return b.cd.external_forces(*args, cells=[cid], **kwargs)[0]

            boc = self.blocks_of_cells(i=cells)
            return {cid: f(boc[cid], cid) for cid in cells}
        else:
            blocks = self.cellblocks(inclusive=True)

            def foo(b: FemMesh[PointData, FiniteElement]):
                return b.cd.external_forces(*args, **kwargs)

            return np.vstack(list(map(foo, blocks)))

    def internal_forces(
        self, *args, cells: Iterable = None, flatten: bool = True, **kwargs
    ) -> ndarray:
        """
        Returns internal forces for each cell or a selection.

        Parameters
        ----------
        cells: Iterable, Optional
            Indices of cells for which internal forces are requested.
            If specified, the result is a dictionary with the indices
            being the keys. Default is None.
        flatten: bool, Optional
            If True, nodal results are flattened. Default is True.

        Returns
        -------
        numpy.ndarray or dict
            A dictionary if cell indices are specified, or a NumPy array.
        """
        kwargs.update(flatten=flatten)
        if cells is not None:

            def f(b: FemMesh[PointData, FiniteElement], cid: int):
                return b.cd.internal_forces(*args, cells=[cid], **kwargs)[0]

            boc = self.blocks_of_cells(i=cells)
            return {cid: f(boc[cid], cid) for cid in cells}
        else:
            blocks = self.cellblocks(inclusive=True)

            def foo(b: FemMesh[PointData, FiniteElement]):
                return b.cd.internal_forces(*args, **kwargs)

            return np.vstack(list(map(foo, blocks)))

    def internal_forces_at_centers(self, *args, **kwargs) -> ndarray:
        """
        Returns internal forces at the centers of all cells.

        Returns
        -------
        numpy.ndarray
        """
        blocks = self.cellblocks(inclusive=True)

        def foo(b: FemMesh[PointData, FiniteElement]):
            return b.cd.stresses_at_centers(*args, **kwargs)

        return np.vstack(list(map(foo, blocks)))

    def maximum_utilization(self) -> float:
        """
        Returns the maximum utilization in the mesh.
        """
        blocks = self.cellblocks(inclusive=True)

        def foo(b: FemMesh[PointData, FiniteElement]) -> float:
            return b.cd.maximum_utilization()

        return float(max(list(map(foo, blocks))))

    def postprocess(self, *_, **__):
        """
        General postprocessing. This may be reimplemented in subclasses,
        currently nothing happens here.
        """
        ...

    def _create_dofmap(self, parent: T = None) -> None:
        # rewire variable mapping
        root = self.root if parent is None else parent.root
        root_dofs = root.displacement_variables
        for cb in self.cellblocks(inclusive=True):
            dofs = cb.cd.Material.displacement_variables
            cb.cd.__class__.Material.dofmap = np.array(
                DOF.dofmap(dofs, root_dofs), dtype=int
            )

    def __join_parent__(self, parent: T, key: Hashable = None) -> None:
        super().__join_parent__(parent, key)
        self._create_dofmap(parent)  # rewire variable mapping

    def __leave_parent__(self) -> None:
        # rewire variable mapping to standalone mode
        root = self
        root_dofs = root.displacement_variables
        for cb in self.cellblocks(inclusive=True):
            dofs = cb.cd.Material.displacement_variables
            cb.cd.__class__.Material.dofmap = np.array(
                DOF.dofmap(dofs, root_dofs), dtype=int
            )
        super().__leave_parent__()
