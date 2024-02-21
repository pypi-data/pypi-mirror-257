from typing import Generic, TypeVar

from numpy import ndarray

from sigmaepsilon.core import classproperty
from sigmaepsilon.math import repeat
from sigmaepsilon.mesh.data import CellData

from ..typing import FemDataProtocol, PointDataProtocol

PD = TypeVar("PD", bound=PointDataProtocol)
FD = TypeVar("FD", bound=FemDataProtocol)


class CellData(Generic[FD, PD], CellData[FD, PD]):
    """
    A subclass of :class:`sigmaepsilon.mesh.celldata.CellData`to handle data related
    to the cells of a finite element mesh.
    """

    _attr_map_ = {
        "body-loads": "_body-loads_",
        "strain-loads": "_strain-loads_",
        "density": "_density_",
        "activity": "_activity_",
        "fixity": "_fixity_",
        "K": "_K_",  # elastic FEM stiffness matrix
        "C": "_C_",  # elastic material stiffness matrix
        "M": "_M_",  # mass matrix
        "B": "_B_",  # strain displacement matrix
        "f": "_f_",  # nodal load vector
    }

    @classproperty
    def _dbkey_stiffness_matrix_(cls) -> str:
        return cls._attr_map_["K"]

    @classproperty
    def _dbkey_material_stiffness_matrix_(cls) -> str:
        return cls._attr_map_["C"]

    @classproperty
    def _dbkey_nodal_load_vector_(cls) -> str:
        return cls._attr_map_["f"]

    @classproperty
    def _dbkey_strain_displacement_matrix_(cls) -> str:
        return cls._attr_map_["B"]

    @classproperty
    def _dbkey_mass_matrix_(cls) -> str:
        return cls._attr_map_["M"]

    @classproperty
    def _dbkey_fixity_(cls) -> str:
        return cls._attr_map_["fixity"]

    @classproperty
    def _dbkey_density_(cls) -> str:
        return cls._attr_map_["density"]

    @classproperty
    def _dbkey_activity_(cls) -> str:
        return cls._attr_map_["activity"]

    @classproperty
    def _dbkey_body_loads_(cls) -> str:
        return cls._attr_map_["body-loads"]

    @classproperty
    def _dbkey_strain_loads_(cls) -> str:
        return cls._attr_map_["strain-loads"]

    # methods to check if a field is available

    @property
    def has_fixity(self):
        return self._dbkey_fixity_ in self._wrapped.fields

    @property
    def has_body_loads(self):
        return self._dbkey_body_loads_ in self._wrapped.fields

    @property
    def has_strain_loads(self):
        return self._dbkey_strain_loads_ in self._wrapped.fields

    @property
    def has_nodal_load_vector(self):
        return self._dbkey_nodal_load_vector_ in self._wrapped.fields

    @property
    def has_material_stiffness(self):
        return self._dbkey_material_stiffness_matrix_ in self._wrapped.fields

    @property
    def has_elastic_stiffness_matrix(self):
        return self._dbkey_stiffness_matrix_ in self._wrapped.fields

    @property
    def has_strain_displacement_matrix(self):
        return self._dbkey_strain_displacement_matrix_ in self._wrapped.fields

    @property
    def has_mass_matrix(self) -> bool:
        return self._dbkey_mass_matrix_ in self._wrapped.fields

    # methods to access and set fields

    @property
    def nodes(self) -> ndarray:
        """Returns the topology of the cells."""
        return self._wrapped[self._dbkey_nodes_].to_numpy()

    @nodes.setter
    def nodes(self, value: ndarray):
        assert isinstance(value, ndarray)
        self._wrapped[self._dbkey_nodes_] = value

    @property
    def strain_loads(self) -> ndarray:
        """Returns strain loads."""
        return self._wrapped[self._dbkey_strain_loads_].to_numpy()

    @strain_loads.setter
    def strain_loads(self, value: ndarray):
        if value is None:
            if self.has_strain_loads:
                del self._wrapped[self._dbkey_strain_loads_]
        else:
            assert isinstance(value, ndarray)
            self._wrapped[self._dbkey_strain_loads_] = value

    @property
    def loads(self) -> ndarray:
        """Returns body loads."""
        return self._wrapped[self._dbkey_body_loads_].to_numpy()

    @loads.setter
    def loads(self, value: ndarray):
        assert isinstance(value, ndarray)
        self._wrapped[self._dbkey_body_loads_] = value

    @property
    def density(self) -> ndarray:
        """Returns densities."""
        return self._wrapped[self._dbkey_density_].to_numpy()

    @density.setter
    def density(self, value: ndarray):
        assert isinstance(value, ndarray)
        self._wrapped[self._dbkey_density_] = value

    @property
    def activity(self) -> ndarray:
        """Returns activity of the cells."""
        return self._wrapped[self._dbkey_activity_].to_numpy()

    @activity.setter
    def activity(self, value: ndarray):
        """Sets the activity of the cells."""
        assert isinstance(value, ndarray)
        self._wrapped[self._dbkey_activity_] = value

    @property
    def fixity(self) -> ndarray:
        """Returns the fixity of the cells."""
        return self._wrapped[self._dbkey_fixity_].to_numpy()

    @fixity.setter
    def fixity(self, value: ndarray):
        """
        Sets the fixity of the cells.
        """
        assert isinstance(value, ndarray)
        self._wrapped[self._dbkey_fixity_] = value

    @property
    def material_stiffness(self) -> ndarray:
        """Returns the material stiffness matrices of the cells."""
        return self._wrapped[self._dbkey_material_stiffness_matrix_].to_numpy()

    @material_stiffness.setter
    def material_stiffness(self, value: ndarray):
        assert isinstance(value, ndarray)
        dbkey = self._dbkey_material_stiffness_matrix_
        if len(value.shape) == 2:
            self._wrapped[dbkey] = repeat(value, len(self))
        else:
            assert len(value.shape) == 3
            self.db[dbkey] = value

    @property
    def elastic_stiffness_matrix(self) -> ndarray:
        """Returns the elastic stiffness matrices of the cells."""
        return self._wrapped[self._dbkey_stiffness_matrix_].to_numpy()

    @elastic_stiffness_matrix.setter
    def elastic_stiffness_matrix(self, value: ndarray) -> None:
        """Sets the elastic stiffness matrices of the cells."""
        assert isinstance(value, ndarray)
        self._wrapped[self._dbkey_stiffness_matrix_] = value

    @property
    def strain_displacement_matrix(self) -> ndarray:
        """Returns the strain-displacement matrices of the cells."""
        return self._wrapped[self._dbkey_strain_displacement_matrix_].to_numpy()

    @strain_displacement_matrix.setter
    def strain_displacement_matrix(self, value: ndarray) -> None:
        """Sets the strain-displacement matrices of the cells."""
        assert isinstance(value, ndarray)
        self._wrapped[self._dbkey_strain_displacement_matrix_] = value

    @property
    def mass_matrix(self) -> ndarray:
        """Returns the mass matrices of the cells."""
        return self._wrapped[self._dbkey_mass_matrix_].to_numpy()

    @mass_matrix.setter
    def mass_matrix(self, value: ndarray) -> None:
        """Sets the mass matrices of the cells."""
        assert isinstance(value, ndarray)
        self._wrapped[self._dbkey_mass_matrix_] = value

    @property
    def nodal_loads(self) -> ndarray:
        """Returns the nodal loads of the cells."""
        return self._wrapped[self._dbkey_nodal_load_vector_].to_numpy()

    @nodal_loads.setter
    def nodal_loads(self, value: ndarray) -> None:
        """Sets the nodal loads of the cells."""
        assert isinstance(value, ndarray)
        self._wrapped[self._dbkey_nodal_load_vector_] = value
