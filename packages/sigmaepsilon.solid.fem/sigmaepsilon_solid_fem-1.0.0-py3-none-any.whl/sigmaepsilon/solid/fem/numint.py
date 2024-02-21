from typing import Iterable, Optional, Union

from numpy.lib.index_tricks import IndexExpression

from sigmaepsilon.mesh.utils.numint import Quadrature as Q


class Quadrature(Q):
    def __init__(
        self,
        *args,
        inds: Optional[Union[Iterable[int], IndexExpression, None]] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._inds = inds

    @property
    def inds(self) -> Union[Iterable[int], IndexExpression, None]:
        return self._inds

    @inds.setter
    def inds(self, value: Union[Iterable[int], IndexExpression]) -> None:
        self._inds = value
