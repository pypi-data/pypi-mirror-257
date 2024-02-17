"""
Affine subspaces.
"""

# Part of: q1ss
# Copyright (C) 2023 Hashberg Ltd and 20squares UG

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA

from __future__ import annotations
from collections.abc import Mapping, Sequence
from itertools import cycle, product
from typing import Any, Iterator, Literal, Protocol, final
from typing_extensions import Self
import numpy as np
import numpy.typing as npt
from typing_validation import validate
from .vectorized import (
    IntVec,
    BinVec,
    get_rref_args,
    matmul_r2l_partial,
    rref_pivot_cols,
    rref_residual_vec,
)
from .binvec import binvec
from .binmat import binmat

try:
    import networkx as nx  # type: ignore
except ModuleNotFoundError:
    nx = None

HypercubeAxes = npt.NDArray[np.number[Any]] | Sequence[Sequence[int | float]]
"""
Type alias for hypercube axes that can be passed to :meth:`AffineSubspace.draw`,
and :meth:`AffineSubspace.draw_many`.
"""


@final
class AffineSubspace:
    r"""
    A linear or affine subspace of a space over the field :math:`\mathbb{Z}_2`,
    represened by:

    - a matrix whose rows span the (underlying) linear subspace
    - a basepoint vector

    The subspace representation can be canonicalized: see :attr:`is_canonical`
    and :meth:`canonicalize` for details.

    .. warning ::

        For efficiency reasons, the internal representation of the affine
        subspace is not canonicalised at construction time. Many properties and
        methods automatically canonicalize the subspace as part of their inner
        workings, but the following properties and methods don't do so:

        - :attr:`ambient_dim`
        - :attr:`num_generators`
        - :attr:`generators`
        - :attr:`basepoint`
        - :attr:`linspace`
        - :meth:`__rmatmul__`
        - :meth:`__add__`
        - :meth:`__radd__`
        - :meth:`draw`

        The values returned by :attr:`num_generators`, :attr:`generators` and
        :attr:`basepoint` change when the space is canonicalized.
    """

    @staticmethod
    def draw_many(
        axes: HypercubeAxes,
        subspaces: Sequence[AffineSubspace],
        *,
        colors: Sequence[str] | None = None,
        label: BinvecLabelFun | None = None,
        subsp_kwargs: Sequence[Mapping[str, Any]] | None = None,
        **draw_networkx_kwargs: Any,
    ) -> None:
        """
        Draws the given affine subspaces using :func:`~networkx.draw_networkx`.
        """
        if nx is None:
            raise ModuleNotFoundError(
                "Hypercube drawing requires the 'networkx' library."
            )
        _axes: npt.NDArray[np.float64] = np.array(axes, dtype=np.float64)
        assert AffineSubspace.__validate_draw_data(
            _axes, subspaces, colors, subsp_kwargs
        )
        if colors is None:
            colors = ["#000" for _ in subspaces]
        draw_hypercube(_axes, label=label, **draw_networkx_kwargs)
        if subsp_kwargs is None:
            subsp_kwargs = [{}] * len(subspaces)
        for subsp, col, kwargs in zip(subspaces, colors, subsp_kwargs):
            basis = subsp.basis
            points = subsp.points
            _points = [tuple(u) for u in points]
            pos = dict(zip(_points, points.data @ _axes))
            subsp_g = nx.Graph()
            subsp_g.add_nodes_from(_points)
            subsp_g.add_edges_from(
                [(tuple(u), tuple(u + v)) for u in points for v in basis]
            )
            nx.draw_networkx(
                subsp_g,
                pos,
                labels=dict(zip(_points, cycle([""]))),
                node_size=[
                    40 if all(x == 0 for x in u) else 20 for u in _points
                ],
                node_color=col,
                edge_color=col,
                **kwargs,
            )

    @staticmethod
    def random(
        subsp_dim: int,
        ambient_dim: int,
        *,
        linear: bool = False,
        rng: np.random.Generator | int | None = None,
    ) -> AffineSubspace:
        """
        Samples a random affine subspace with given subspace dimension,
        within a vector space with given ambient dimension.
        If ``linear`` is :obj:`True`, only linear subspaces are sampled.

        .. warning::

            This method relies on :meth:`~q1ss.binalg.binmat.binmat.random_rref`
            to sample the underlying linear subspace: currently, it does not
            result in a uniform sampling across all subspaces.
            This will change in future releases.
        """
        assert AffineSubspace._validate_dimensions(subsp_dim, ambient_dim)
        if not isinstance(rng, np.random.Generator):
            rng = np.random.default_rng(rng)
        # n, m = ambient_dim, subsp_dim
        basis_mat = binmat.random_rref(subsp_dim, ambient_dim, rng=rng)
        basepoint = binvec.zeros(ambient_dim)
        if not linear:
            non_pivot_cols = [
                c
                for c in range(ambient_dim)
                if c not in set(rref_pivot_cols(basis_mat._data))
            ]
            params = binvec.random(len(non_pivot_cols), rng=rng)
            basepoint[non_pivot_cols] = params
        return AffineSubspace(basis_mat, basepoint)

    @staticmethod
    def std(
        subsp_dim: int, ambient_dim: int, basepoint: binvec | None = None
    ) -> AffineSubspace:
        """
        Returns the standard affine subspace of given dimension,
        using the first :math:`n` standard basis vectors of the ambient space
        where :math:`n` is the subspace dimension.
        """
        assert AffineSubspace._validate_dimensions(subsp_dim, ambient_dim)
        return AffineSubspace(
            binmat.trunc_eye(subsp_dim, ambient_dim), basepoint
        )

    _ambient_dim: int
    _generators: binmat
    _basepoint: binvec
    _is_canonical: bool

    __dim: int
    __pivot_cols: IntVec
    __params: BinVec
    __is_linear: bool

    __slots__ = (
        "__weakref__",
        "_ambient_dim",
        "_generators",
        "_basepoint",
        "_is_canonical",
        "__dim",
        "__pivot_cols",
        "__params",
        "__is_linear",
    )

    def __new__(
        cls,
        generators: binmat,
        basepoint: binvec | None = None,
        *,
        copy: bool = False,
    ) -> Self:
        """
        Constructs a linear/affine subspace of binary vectors from a basis and
        an optional basepoint.

        .. warning::

            The :class:`AffineSubspace` class logic presumes that the basis
            and basepoint will not be mutated after construction: both will
            be changed to readonly by the constructor.
            If you do not wish either one to be made readonly, pass
            ``copy=True`` at construction.
        """
        assert AffineSubspace.__validate_data(generators, basepoint)
        _, ambient_dim = generators.shape
        if copy:
            generators = generators.copy()
            basepoint = None if basepoint is None else basepoint.copy()
        if basepoint is None:
            basepoint = binvec.zeros(ambient_dim)
        generators.readonly = True
        basepoint.readonly = True
        instance = super().__new__(cls)
        instance._ambient_dim = ambient_dim
        instance._generators = generators
        instance._basepoint = basepoint
        instance._is_canonical = False
        return instance

    def __getnewargs__(self) -> tuple[binmat, binvec]:
        """
        Method for pickling.
        """
        return (self._generators, self._basepoint)

    @property
    def dim(self) -> int:
        """
        The dimension of the subspace.

        The subspace is automatically canonicalised.
        """
        if not self._is_canonical:
            self.canonicalize()
        return self.__dim

    @property
    def ambient_dim(self) -> int:
        """
        The dimension of the ambient space.
        """
        return self._ambient_dim

    @property
    def num_generators(self) -> int:
        """
        Returns the number of generators for the (underlying) linear subspace.
        """
        return self._generators.shape[1]

    @property
    def generators(self) -> binmat:
        """
        A matrix whose rows span the (underlying) linear subspace.

        The value returned by this property is only guaranteed to be constant
        if the subspace :attr:`is_canonical`, in which case it is the same
        as the subspace :attr:`basis`.
        """
        return self._generators

    @property
    def basis(self) -> binmat:
        """
        A RREF matrix whose rows form a basis for the linear subspace.

        The subspace is automatically canonicalised.
        """
        if not self._is_canonical:
            self.canonicalize()
        return self._generators

    @property
    def iter_basis(self) -> Iterator[binvec]:
        """
        Iterates over the basis vectors for the linear subspace.

        The subspace is automatically canonicalised.
        """
        if not self._is_canonical:
            self.canonicalize()
        yield from self._generators

    @property
    def basepoint(self) -> binvec:
        """
        The value returned by this property is only guaranteed to be constant
        if the subspace :attr:`is_canonical`, in which case:

        - it is guaranteed to be zero at the pivot cols for the :attr:`basis`
          matrix (which is in RREF when the subspace is canonical);
        - it is the zero vector if and only if the subspace is linear

        """
        return self._basepoint

    @property
    def is_canonical(self) -> bool:
        """
        Whether the subspace is in canonical form:

        - the basis matrix is in RREF
        - the basepoint vector has been reduced to canonical form

        A subspace can be put in canonical form by calling :meth:`canonicalize`,
        and it henceforth remains in canonical form.
        The subspace is automatically canonicalized the first time that
        an operation is executed which requires canonical data.
        """
        return self._is_canonical

    @property
    def is_linear(self) -> bool:
        """
        Whether the subspace is linear.

        The subspace is automatically canonicalised.
        """
        if not self._is_canonical:
            self.canonicalize()
        return self.__is_linear

    @property
    def linspace(self) -> AffineSubspace:
        """
        The linear subspace corresponding to this affine subspace.
        """
        return AffineSubspace(self._generators)

    @property
    def points(self) -> binmat:
        """
        Returns a matrix whose columns are all points of this affine subspace.
        """
        coeffs = binmat.from_rows(list(binvec.iter_all(self.dim)))
        return self.select(coeffs)

    @property
    def iter_points(self) -> Iterator[binvec]:
        """
        Iterates over all the points in the affine subspace.
        """
        basis = self.basis
        basepoint = self._basepoint
        n, _ = basis.shape
        for i in range(2**n):
            yield binvec.from_str(f"{i:0>{n}b}") @ basis + basepoint

    def copy(self, *, canonical: bool = False) -> AffineSubspace:
        """
        Returns a copy of this affine subspace.
        If ``canonical=True``, the copy is canonicalised.
        """

        subsp = AffineSubspace(self._generators, self._basepoint)
        if self._is_canonical:
            subsp._is_canonical = True
            subsp.__dim = self.__dim
            subsp.__pivot_cols = self.__pivot_cols
            subsp.__params = self.__params
            subsp.__is_linear = self.__is_linear
        elif canonical:
            subsp.canonicalize()
        return subsp

    def canonicalize(self) -> None:
        """
        Canonicalises the affine subspace's internal data:

        - the generators are brought to RCEF, zero columns are dropped and
          the subspace dimension is obtained as the number of non-zero columns.
        - the basepoint vector is reduced according to the new generators,
          and the subspace is linear when the reduced basepoint is zero.

        """

        if self._is_canonical:
            return
        basis = self._generators.rref
        basis = basis[: basis.rank]
        basepoint = binvec(
            rref_residual_vec(basis._data, self._basepoint._data)
        )
        dim, _, pivot_cols, params = get_rref_args(basis._data)
        basis.readonly = True
        basepoint.readonly = True
        self._generators = basis
        self._basepoint = basepoint
        self._is_canonical = True
        self.__dim = dim
        self.__pivot_cols = pivot_cols
        self.__params = params
        self.__is_linear = basepoint.is_zero

    def is_disjoint(self, other: AffineSubspace) -> bool:
        """
        Whether this affine subspace is disjoint from the other given subspace.
        """
        assert self.__same_ambient_dim(other)
        if not self._is_canonical:
            self.canonicalize()
        if not other._is_canonical:
            other.canonicalize()
        c = binmat.vstack([self.basis, other.basis]).rref
        r = c.rank
        if r == self.ambient_dim:
            return False
        d = binmat.vstack([c, other.basepoint - self.basepoint]).rref
        return d.rank > r

    def residual(self, vec: binvec) -> binvec:
        """
        Returns the canonical translation that must be applied to this affine
        subspace to obtain a coset which contains the given vector.
        """
        if not self._is_canonical:
            self.canonicalize()
        assert self.__same_ambient_dim(vec)
        u = vec - self.basepoint
        return binvec(rref_residual_vec(self._generators._data, u._data))

    def select(self, coeffs: binmat) -> binmat:
        """
        Returns a matrix whose columns are the affine subspace points obtained
        by linear combination of the basis vectors, using the columns of the
        input matrix as coefficient vectors.
        """
        assert self.__same_subsp_dim(coeffs)
        basis_mat = self.basis
        basepoint = self._basepoint
        return (coeffs @ basis_mat).rows + basepoint

    def random_points(
        self,
        num_samples: int,
        *,
        rng: np.random.Generator | int | None = None,
    ) -> binmat:
        """
        Returns a matrix with the given number of random subspace points
        as its rows.
        """
        assert validate(num_samples, int)
        if not isinstance(rng, np.random.Generator):
            rng = np.random.default_rng(rng)
        coeffs = binmat.random(num_samples, self.dim, rng=rng)
        return self.select(coeffs)

    def draw(
        self,
        axes: HypercubeAxes,
        *,
        color: str | None = None,
        label: BinvecLabelFun | None = None,
        **draw_networkx_kwargs: Any,
    ) -> None:
        """
        Draws this affine subspace using :func:`~networkx.draw_networkx`.
        """
        colors = None if color is None else [color]
        AffineSubspace.draw_many(
            axes, [self], colors=colors, label=label, **draw_networkx_kwargs
        )

    def transform(
        self, matrices: Sequence[binmat], *, partial: bool = False
    ) -> AffineSubspace:
        """
        Transforms the subspace by the given matrices, applied in order
        left-to-right.
        If ``partial=True``, matrices are allowed to have dimension/side ``k``
        smaller than the ambient dimension of the subspace, in which case
        they are applied to the subspace spanned by the first ``k`` standard
        ambient vectors.
        """
        assert validate(matrices, Sequence[binmat])
        if partial:
            assert all(self.__up_to_same_ambient_dim(mat) for mat in matrices)
        else:
            assert all(self.__same_ambient_dim(mat) for mat in matrices)
        matrix_data = [m.data for m in matrices]
        generators = binmat(
            matmul_r2l_partial(matrix_data, self._generators.data.T).T
        )
        if not self._basepoint.is_zero:
            basepoint = binvec(
                matmul_r2l_partial(matrix_data, self._basepoint.data)
            )
        else:
            basepoint = self._basepoint
        return AffineSubspace(generators, basepoint)

    def is_ortho(self, vec: binvec) -> bool:
        """
        Whether the given vector is orthogonal to the subspace.
        """
        assert self.__same_ambient_dim(vec)
        return (self._generators @ vec).is_zero

    def __rmatmul__(self, mat: binmat) -> AffineSubspace:
        """
        Transforms the affine subspace by the given matrix.

        :meta public:
        """
        assert validate(mat, binmat)
        assert self.__same_ambient_dim(mat)
        return AffineSubspace(self._generators @ mat.T, mat @ self._basepoint)

    def __add__(self, vec: binvec) -> AffineSubspace:
        """
        Translates the affine subspace by the given vector.

        :meta public:
        """
        assert validate(vec, binvec)
        assert self.__same_ambient_dim(vec)
        return AffineSubspace(self._generators, self._basepoint + vec)

    def __radd__(self, vec: binvec) -> AffineSubspace:
        """
        Translates the affine subspace by the given vector.

        :meta public:
        """
        return self + vec

    def __sub__(self, vec: binvec) -> AffineSubspace:
        """
        Same as :meth:`__add__`.

        :meta public:
        """
        return self + vec

    def __contains__(self, vec: binvec) -> bool:
        """
        Whether the given vector is contained in this affine subspace.

        :meta public:
        """
        return self.residual(vec).is_zero

    def __hash__(self) -> int:
        """
        Hashes the subspace.
        """
        if not self._is_canonical:
            self.canonicalize()
        if self.__is_linear:
            return hash((type(self), self._generators))
        return hash((type(self), self._generators, self._basepoint))

    def __eq__(self, other: Any) -> bool:
        """
        Checks whether this affine subspace is equal to another affine subspace.

        :meta public:
        """
        if not isinstance(other, AffineSubspace):
            return NotImplemented
        if not self._is_canonical:
            self.canonicalize()
        if not other._is_canonical:
            other.canonicalize()
        if self._generators != other._generators:
            return False
        if self.__is_linear and other.__is_linear:
            return True
        if self.__is_linear ^ other.__is_linear:
            return False
        return self._basepoint == other._basepoint

    def __repr__(self) -> str:
        gen = "\n".join(
            "  " + line for line in repr(self._generators).split("\n")
        )
        bp = "\n".join(
            "  " + line for line in repr(self._basepoint).split("\n")
        )
        return f"AffineSubspace(\n{gen},\n{bp}\n)"

    @staticmethod
    def _validate_dimensions(subsp_dim: int, ambient_dim: int) -> Literal[True]:
        validate(subsp_dim, int)
        validate(ambient_dim, int)
        if ambient_dim <= 0:
            raise ValueError("Ambient dimension must be positive.")
        if subsp_dim not in range(0, ambient_dim + 1):
            raise ValueError(
                f"Subspace dimension must be between 0 and {ambient_dim} incl."
            )
        return True

    @staticmethod
    def __validate_data(
        basis: binmat, basepoint: binvec | None
    ) -> Literal[True]:
        validate(basis, binmat)
        if basepoint is not None:
            validate(basepoint, binvec)
            if len(basepoint) != basis.shape[1]:
                raise ValueError(
                    f"Expected {basis.shape[1]}-dim basepoint, "
                    f"found {len(basepoint)}-dim."
                )
        return True

    def __same_ambient_dim(
        self, other: AffineSubspace | binvec | binmat
    ) -> Literal[True]:
        if isinstance(other, binvec):
            if len(other) != self.ambient_dim:
                raise ValueError(
                    "Vector dimension differs from ambient dimension of "
                    f"affine subspace: {len(other)} != {self.ambient_dim}."
                )
            return True
        if isinstance(other, binmat):
            _, m = other.shape
            if m != self.ambient_dim:
                raise ValueError(
                    "Matrix domain dimension differs from ambient dimension of "
                    f"affine subspace: {m} != {self.ambient_dim}."
                )
            return True
        validate(other, AffineSubspace)
        if self.ambient_dim != other.ambient_dim:
            raise ValueError(
                "Affine subspaces have different ambient dimensions: "
                f"{other.ambient_dim} != {self.ambient_dim}."
            )
        return True

    def __up_to_same_ambient_dim(self, other: binmat) -> Literal[True]:
        _, m = other.shape
        if m > self.ambient_dim:
            raise ValueError(
                "Matrix domain dimension is higher than ambient dimension of "
                f"affine subspace: {m} != {self.ambient_dim}."
            )
        return True

    def __same_subsp_dim(
        self, other: AffineSubspace | binvec | binmat
    ) -> Literal[True]:
        if isinstance(other, binvec):
            if len(other) != self.dim:
                raise ValueError(
                    "Vector dimension differs from ambient dimension of "
                    f"affine subspace: {len(other)} != {self.dim}."
                )
            return True
        if isinstance(other, binmat):
            _, m = other.shape
            if m != self.dim:
                raise ValueError(
                    "Matrix codomain dimension differs from ambient dimension "
                    f"of affine subspace: {m} != {self.dim}."
                )
            return True
        validate(other, AffineSubspace)
        if self.dim != other.dim:
            raise ValueError(
                "Affine subspaces have different subspace dimensions: "
                f"{other.dim} != {self.dim}."
            )
        return True

    @staticmethod
    def __validate_draw_data(
        axes: npt.NDArray[np.float64],
        subspaces: Sequence[AffineSubspace],
        colors: Sequence[str] | None,
        subsp_kwargs: Sequence[Mapping[str, Any]] | None,
    ) -> Literal[True]:
        assert validate(subspaces, Sequence[AffineSubspace])
        if colors is not None and len(colors) != len(subspaces):
            raise ValueError(
                f"Expected {len(subspaces)} colors, found {len(colors)}."
            )
        n = len(axes)
        for subsp in subspaces:
            if subsp.ambient_dim != n:
                raise ValueError(
                    f"All subspaces should have ambient dimension {n}, "
                    f"found ambient dimension {subsp.ambient_dim}."
                )
        if subsp_kwargs is not None:
            validate(subsp_kwargs, Sequence[Mapping[str, Any]])
            if len(subsp_kwargs) != len(subspaces):
                raise ValueError(
                    f"Expected {len(subspaces)} subspaces kwargs dictionaries, "
                    f"found {len(subsp_kwargs)}."
                )
        return True


class BinvecLabelFun(Protocol):
    """
    Structural type for a labelling function which can be passed to the
    ``label`` argument of various drawing methods for affine subspaces.
    """

    def __call__(self, label: binvec) -> str: ...


def draw_hypercube(
    axes: HypercubeAxes,
    *,
    label: BinvecLabelFun | None = None,
    **draw_networkx_kwargs: Any,
) -> None:
    """
    Draws a hypercube using :func:`~networkx.draw_networkx`,
    plotting the generating directions along the given 2D axes.
    """
    if nx is None:
        raise ModuleNotFoundError(
            "Hypercube drawing requires the 'networkx' library."
        )
    _axes = np.array(axes, dtype=np.float64)
    if len(_axes.shape) != 2:
        raise ValueError(
            "Axes should be a sequence of vectors, found a tensor of "
            f"shape {_axes.shape} instead."
        )
    n, _m = _axes.shape
    if _m != 2:
        raise ValueError(
            f"Axes values should be 2-dim vectors, found {_m}-dim."
        )
    nodes = list(product([0, 1], repeat=n))
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(
        [
            (u, tuple(1 - x if i == j else x for i, x in enumerate(u)))
            for u in nodes
            for j in range(n)
        ]
    )
    pos = dict(zip(nodes, np.array(nodes) @ _axes))
    if label is None:
        labels = dict(zip(nodes, cycle([""])))
    else:
        labels = dict(zip(nodes, [label(binvec(node)) for node in nodes]))
    nx.draw_networkx(
        g,
        pos,
        labels=labels,
        node_size=[40 if all(x == 0 for x in u) else 20 for u in nodes],
        node_color="#ddd",
        edge_color="#ddd",
        **draw_networkx_kwargs,
    )
