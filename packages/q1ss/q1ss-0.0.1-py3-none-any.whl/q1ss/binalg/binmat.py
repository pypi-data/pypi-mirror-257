"""
Binary matrices.
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
from collections.abc import Iterator, Sequence
from typing import Literal, Union, cast, final, overload
from typing_extensions import Self
import numpy as np
import numpy.typing as npt
from typing_validation import validate
from .vectorized import (
    BinMat,
    BinVec,
    BinVecOrMat,
    IntVec,
    make_rcef,
    make_rref,
    matmul2,
    num_rcef_params,
    num_rref_params,
    rcef,
    rref,
)
from .base import bintensor
from .binvec import binvec, Bit


MatBitIdx = tuple[int, int]
"""
Type alias for the union of index types which result in a single bit
being selected when passed to :meth:`binmat.__getitem__`.
"""

MatSubvecIdx = (
    int
    | tuple[int, slice | list[int]]
    | tuple[slice | list[int], int]
    | tuple[list[int], list[int]]
)
"""
Type alias for the union of index types which result in a sub-vector
being selected when passed to :meth:`binmat.__getitem__`.
"""

MatSubmatIdx = (
    slice
    | list[int]
    | tuple[slice, slice | list[int]]
    | tuple[slice | list[int], slice]
)
"""
Type alias for the union of index types which result in a sub-matrix
being selected when passed to :meth:`binmat.__getitem__`.
"""


@final
class binmat(bintensor):
    r"""
    A mutable matrix over the field :math:`\mathbb{Z}_2`.
    """

    class NotInvertibleError(ZeroDivisionError):
        """
        Subclass of :obj:`ZeroDivisionError` use when attempting to invert a
        matrix which is not invertible.
        """

    @final
    class Rows:
        """
        View of a binary matrix as a sequence of rows.
        """

        _mat: binmat

        __slots__ = ("__weakref__", "_mat")

        def __new__(cls, mat: binmat) -> Self:
            instance = super().__new__(cls)
            instance._mat = mat
            return instance

        @overload
        def __getitem__(self, idx: int) -> binvec: ...

        @overload
        def __getitem__(self, idx: slice | list[int]) -> binmat: ...

        def __getitem__(self, idx: int | slice | list[int]) -> binvec | binmat:
            """
            Selects a row vector in a matrix, or creates a new matrix
            by slicing/selecting rows.

            :meta public:
            """
            mat = self._mat
            if isinstance(idx, int):
                return mat[idx]
            validate(idx, slice | list[int])
            return mat[idx]

        def __iter__(self) -> Iterator[binvec]:
            """
            Iterates over the rows of the matrix.

            :meta public:
            """
            data = self._mat._data
            n, _ = data.shape
            for r in range(n):
                yield binvec(data[r, :])

        def __len__(self) -> int:
            """
            The number of rows in the matrix.

            :meta public:
            """
            return self._mat.shape[0]

        def __add__(self, vec: binvec) -> binmat:
            """
            Returns the matrix obtained by adding the given vector
            to all rows of the matrix.

            :meta public:
            """
            assert self.__has_compatible_shape(vec)
            return binmat(self._mat._data ^ vec._data)

        def __sub__(self, vec: binvec) -> binmat:
            """
            Same as :meth:`__add__`.

            :meta public:
            """
            return self + vec

        def __mul__(self, vec: binvec) -> binmat:
            """
            Returns the matrix obtained by pointwise multiplication of the given
            vector with all rows of the matrix.

            :meta public:
            """
            assert self.__has_compatible_shape(vec)
            return binmat(self._mat._data * vec._data)

        def __has_compatible_shape(self, vec: binvec) -> Literal[True]:
            validate(vec, binvec)
            if len(vec) != self._mat.shape[1]:
                raise binmat.ShapeError(
                    f"Cannot add {len(vec)}-dim vector to the rows "
                    f"of a matrix of shape {self._mat.shape}"
                )
            return True

    @final
    class Cols:
        """
        View of a binary matrix as a sequence of columns.
        """

        _mat: binmat

        __slots__ = ("__weakref__", "_mat")

        def __new__(cls, mat: binmat) -> Self:
            instance = super().__new__(cls)
            instance._mat = mat
            return instance

        @overload
        def __getitem__(self, idx: int) -> binvec: ...

        @overload
        def __getitem__(self, idx: slice | list[int]) -> binmat: ...

        def __getitem__(self, idx: int | slice | list[int]) -> binvec | binmat:
            """
            Selects a column vector in a matrix, or creates a new matrix
            by slicing/selecting columns.

            :meta public:
            """
            mat = self._mat
            if isinstance(idx, int):
                return mat[:, idx]
            validate(idx, slice | list[int])
            return mat[:, idx]

        def __iter__(self) -> Iterator[binvec]:
            """
            Iterates over the columns of the matrix.

            :meta public:
            """
            data = self._mat._data
            _, m = data.shape
            for c in range(m):
                yield binvec(data[:, c])

        def __len__(self) -> int:
            """
            The number of columns in the matrix.

            :meta public:
            """
            return self._mat.shape[1]

        def __add__(self, vec: binvec) -> binmat:
            """
            Returns the matrix obtained by adding the given vector
            to all columns of the matrix.

            :meta public:
            """
            assert self.__has_compatible_shape(vec)
            return binmat(self._mat._data ^ vec._data[:, np.newaxis])

        def __sub__(self, vec: binvec) -> binmat:
            """
            Same as :meth:`__add__`.

            :meta public:
            """
            return self + vec

        def __mul__(self, vec: binvec) -> binmat:
            """
            Returns the matrix obtained by pointwise multiplication of the given
            vector with all columns of the matrix.

            :meta public:
            """
            assert self.__has_compatible_shape(vec)
            return binmat(self._mat._data * vec._data[:, np.newaxis])

        def __has_compatible_shape(self, vec: binvec) -> Literal[True]:
            validate(vec, binvec)
            if len(vec) != self._mat.shape[0]:
                raise binmat.ShapeError(
                    f"Cannot add {len(vec)}-dim vector to the cols "
                    f"of a matrix of shape {self._mat.shape}"
                )
            return True

    @staticmethod
    def zeros(n: int, m: int, *, readonly: bool = False) -> binmat:
        """
        Constructs a zero binary matrix with given shape.
        """
        assert binmat.__validate_shape(n, m, positive=False)
        return binmat(np.zeros((n, m), dtype=np.uint8), readonly=readonly)

    @staticmethod
    def random(
        n: int,
        m: int,
        *,
        rng: np.random.Generator | int | None = None,
        readonly: bool = False,
    ) -> binmat:
        """
        Random binary matrix with given shape.
        """
        assert binmat.__validate_shape(n, m)
        if not isinstance(rng, np.random.Generator):
            rng = np.random.default_rng(rng)
        bits = rng.integers(0, 2, (n, m), dtype=np.uint8)
        return binmat(bits, readonly=readonly)

    @staticmethod
    def eye(dim: int, *, readonly: bool = False) -> binmat:
        """
        The identity matrix in the given dimension.
        """

        assert binmat.__validate_dim(dim, positive=False)
        mat = binmat(np.eye(dim, dtype=np.uint8), readonly=readonly)
        mat.__in_rref = True
        mat.__in_rcef = True
        mat.__rank = dim
        return mat

    @staticmethod
    def trunc_eye(n: int, m: int, *, readonly: bool = False) -> binmat:
        """
        The truncated identity matrix with the given shape
        """

        assert binmat.__validate_shape(n, m, positive=False)
        dim = max(n, m)
        mat = binmat(np.eye(dim, dtype=np.uint8), readonly=readonly)
        if n < dim:
            mat = mat[:n, :]
            mat.__rank = n
        elif m < dim:
            mat = mat[:, :m]
            mat.__rank = m
        else:
            mat.__rank = dim
        mat.__in_rref = True
        mat.__in_rcef = True
        return mat

    @staticmethod
    def from_rows(rows: Sequence[binvec], *, readonly: bool = False) -> binmat:
        """
        Creates a matrix with the given row vectors.
        """
        assert validate(rows, Sequence[binvec])
        return binmat(np.vstack([r._data for r in rows]), readonly=readonly)

    @staticmethod
    def from_cols(cols: Sequence[binvec], *, readonly: bool = False) -> binmat:
        """
        Creates a matrix with the given column vectors.
        """
        assert validate(cols, Sequence[binvec])
        return binmat(np.vstack([c._data for c in cols]).T, readonly=readonly)

    @staticmethod
    def hstack(
        matrices: Sequence[Union[binmat, binvec]], *, readonly: bool = False
    ) -> binmat:
        """
        Stacks the given matrices (or column vectors) horizontally.
        """
        assert validate(matrices, Sequence[Union[binmat, binvec]])
        return binmat(
            np.hstack(
                [
                    (
                        m._data.reshape(len(m._data), 1)
                        if isinstance(m, binvec)
                        else m._data
                    )
                    for m in matrices
                ]
            ),
            readonly=readonly,
        )

    @staticmethod
    def vstack(
        matrices: Sequence[Union[binmat, binvec]], *, readonly: bool = False
    ) -> binmat:
        """
        Stacks the given matrices (or row vectors) vertically.
        """
        assert validate(matrices, Sequence[Union[binmat, binvec]])
        return binmat(np.vstack([m._data for m in matrices]), readonly=readonly)

    @staticmethod
    def block(
        blocks: Sequence[Sequence[binmat]], *, readonly: bool = False
    ) -> binmat:
        """
        Creates a block matrix from given submatrices (or vectors).
        """
        assert validate(blocks, Sequence[Sequence[binmat]])
        return binmat(
            np.block([[block._data for block in row] for row in blocks]),
            readonly=readonly,
        )

    @staticmethod
    def block_diag(
        blocks: Sequence[binmat], *, readonly: bool = False
    ) -> binmat:
        """
        Creates a block-diagonal matrix from given submatrices (or vectors).
        """
        assert validate(blocks, Sequence[binmat])
        n = sum(block.shape[0] for block in blocks)
        m = sum(block.shape[1] for block in blocks)
        data = np.zeros((n, m), dtype=np.uint8)
        i, j = 0, 0
        for block in blocks:
            a, b = block.shape
            data[i : i + a, j : j + b] = block._data
            i += a
            j += b
        return binmat(data, readonly=readonly)

    @staticmethod
    def __pivot_array(pivot_rows: npt.ArrayLike) -> IntVec:
        if not isinstance(pivot_rows, np.ndarray):
            return np.array(pivot_rows, dtype=np.int64)
        if not np.issubdtype(pivot_rows.dtype, np.integer):
            return np.array(pivot_rows, dtype=np.int64)
        return cast(IntVec, pivot_rows)

    @staticmethod
    def __rxef_params_array(
        num_params: int, params: npt.ArrayLike | None
    ) -> BinVec:
        if params is None:
            return np.zeros(num_params, dtype=np.uint8)
        if not isinstance(params, np.ndarray) or params.dtype != np.uint8:
            return np.array(params, dtype=np.uint8)
        return cast(BinVec, params)

    @staticmethod
    def __validate_rank(n: int, rank: int) -> Literal[True]:
        if rank not in range(n + 1):
            raise ValueError(f"Rank must be between 0 and {n} inclusive.")
        return True

    @staticmethod
    def _rxef_matrix(
        n: int,
        m: int,
        pivots: npt.ArrayLike,
        params: npt.ArrayLike | None = None,
        *,
        readonly: bool = False,
        mode: Literal["rref", "rcef"],
    ) -> binmat:
        """
        Returns a ``n``-by-``m`` matrix in RREF or RCEF with the given pivot
        cols/rows. The available degrees of freedom are filled with the given
        ``params`` vector entries, or set to zero if ``params`` is not given.

        :raises ValueError: if the pivot rows are not in range,
                            not strictly ascending, or not the same number.
        :raises ValueError: if ``params`` is given and it is not a 1D array
                            with the number of parameters specified by
                            :meth:`num_rcef_params`.
        """
        pivots = binmat.__pivot_array(pivots)
        num_params = binmat._validate_rxef_args(n, m, pivots, mode=mode)
        params = binmat.__rxef_params_array(num_params, params)
        assert binmat.__validate_params(params, num_params)
        make_rxef = make_rref if mode == "rref" else make_rcef
        return binmat(make_rxef(n, m, pivots, params), readonly=readonly)

    @staticmethod
    def rcef_matrix(
        n: int,
        m: int,
        pivot_rows: npt.ArrayLike,
        params: npt.ArrayLike | None = None,
        *,
        readonly: bool = False,
    ) -> binmat:
        """
        Returns a ``n``-by-``m`` matrix in RCEF with the given pivot rows.
        The available degrees of freedom are filled with the given
        ``params`` vector entries, or set to zero if ``params`` is not given.

        :raises ValueError: if the pivot rows are not in range,
                            not strictly ascending, or not the same number.
        :raises ValueError: if ``params`` is given and it is not a 1D array
                            with the number of parameters specified by
                            :meth:`num_rcef_params`.
        """
        return binmat._rxef_matrix(
            n, m, pivot_rows, params, readonly=readonly, mode="rcef"
        )

    @staticmethod
    def rref_matrix(
        n: int,
        m: int,
        pivot_cols: npt.ArrayLike,
        params: npt.ArrayLike | None = None,
        *,
        readonly: bool = False,
    ) -> binmat:
        """
        Returns a ``n``-by-``m`` matrix in RCEF with the given pivot rows.
        The available degrees of freedom are filled with the given
        ``params`` vector entries, or set to zero if ``params`` is not given.

        :raises ValueError: if the pivot rows are not in range,
                            not strictly ascending, or not the same number.
        :raises ValueError: if ``params`` is given and it is not a 1D array
                            with the number of parameters specified by
                            :meth:`num_rref_params`.
        """
        return binmat._rxef_matrix(
            n, m, pivot_cols, params, readonly=readonly, mode="rref"
        )

    @staticmethod
    def _num_rxef_params(
        n: int, m: int, pivots: npt.ArrayLike, *, mode: Literal["rref", "rcef"]
    ) -> int:
        """
        The number of parameters for a RREF or RCEF matrix with given data.
        See :meth:`rcef_matrix`.
        """
        pivots = binmat.__pivot_array(pivots)
        assert binmat.__validate_shape(n, m)
        assert binmat.__validate_pivots(n, m, pivots, mode)
        num_rxef_params = num_rref_params if mode == "rref" else num_rcef_params
        return num_rxef_params(n, m, pivots)

    @staticmethod
    def num_rcef_params(n: int, m: int, pivots: npt.ArrayLike) -> int:
        """
        The number of parameters for a RCEF matrix with given data.
        See :meth:`rcef_matrix`.
        """
        return binmat._num_rxef_params(n, m, pivots, mode="rcef")

    @staticmethod
    def num_rref_params(n: int, m: int, pivots: npt.ArrayLike) -> int:
        """
        The number of parameters for a RREF matrix with given data.
        See :meth:`rref_matrix`.
        """
        return binmat._num_rxef_params(n, m, pivots, mode="rref")

    @staticmethod
    def _validate_rxef_args(
        n: int,
        m: int,
        pivots: npt.ArrayLike,
        params: npt.ArrayLike | None = None,
        *,
        mode: Literal["rref", "rcef"],
    ) -> int:
        """
        Validates the arguments for a RCEF matrix with given data.
        See :meth:`rcef_matrix`. Returns the number of parameters expected
        (the length of ``params``, if given).
        """
        pivots = binmat.__pivot_array(pivots)
        num_params = binmat._num_rxef_params(n, m, pivots, mode=mode)
        params = binmat.__rxef_params_array(num_params, params)
        assert binmat.__validate_params(params, num_params)
        return num_params

    @staticmethod
    def validate_rcef_args(
        n: int,
        m: int,
        pivots: npt.ArrayLike,
        params: npt.ArrayLike | None = None,
    ) -> int:
        """
        Validates the arguments for a RCEF matrix with given data.
        See :meth:`rcef_matrix`. Returns the number of parameters expected
        (the length of ``params``, if given).
        """
        return binmat._validate_rxef_args(n, m, pivots, params, mode="rcef")

    @staticmethod
    def validate_rref_args(
        n: int,
        m: int,
        pivots: npt.ArrayLike,
        params: npt.ArrayLike | None = None,
    ) -> int:
        """
        Validates the arguments for a RREF matrix with given data.
        See :meth:`rref_matrix`. Returns the number of parameters expected
        (the length of ``params``, if given).
        """
        return binmat._validate_rxef_args(n, m, pivots, params, mode="rref")

    @staticmethod
    def _random_rxef(
        n: int,
        m: int,
        rank: int | None = None,
        *,
        rng: np.random.Generator | int | None = None,
        readonly: bool = False,
        mode: Literal["rref", "rcef"],
    ) -> binmat:
        """
        Returns a random RREF or RCEF matrix with given shape.
        The rank of the matrix can be optionally specified (by default,
        the sampled RREF/RCEF matrix is full rank).
        """
        k = n if mode == "rcef" else m
        assert binmat.__validate_shape(n, m)
        assert rank is None or binmat.__validate_rank(k, rank)
        assert validate(mode, Literal["rref", "rcef"])
        if rank is None:
            rank = min(n, m)
        if not isinstance(rng, np.random.Generator):
            rng = np.random.default_rng(rng)
        pivots = rng.choice(k, rank, replace=False)
        pivots.sort()
        num_rxef_params = num_rref_params if mode == "rref" else num_rcef_params
        num_params = num_rxef_params(n, m, pivots)
        params = rng.integers(0, 2, num_params, dtype=np.uint8)
        make_rxef = make_rref if mode == "rref" else make_rcef
        return binmat(make_rxef(n, m, pivots, params), readonly=readonly)

    @staticmethod
    def random_rcef(
        n: int,
        m: int,
        rank: int | None = None,
        *,
        rng: np.random.Generator | int | None = None,
        readonly: bool = False,
    ) -> binmat:
        r"""
        Returns a random RCEF matrix with given shape.
        The rank of the matrix can be optionally specified (by default,
        the sampled RCEF matrix is full rank, i.e. ``rank=min(n,m)``).

        .. warning::

            The current sampling method does not result in a uniform
            distribution in the Grasmannian :math:`\mathbf{Gr}(r,n)`,
            where :math:`r` is the ``rank`` and :math:`n` the number of rows.
            This will change in future releases.
        """
        return binmat._random_rxef(
            n, m, rank=rank, rng=rng, readonly=readonly, mode="rcef"
        )

    @staticmethod
    def random_rref(
        n: int,
        m: int,
        rank: int | None = None,
        *,
        rng: np.random.Generator | int | None = None,
        readonly: bool = False,
    ) -> binmat:
        r"""
        Returns a random RREF matrix with given shape.
        The rank of the matrix can be optionally specified (by default,
        the sampled RREF matrix is full rank, i.e. ``rank=min(n,m)``).

        .. warning::

            The current sampling method does not result in a uniform
            distribution in the Grasmannian :math:`\mathbf{Gr}(r,m)`,
            where :math:`r` is the ``rank`` and :math:`m` the number of cols.
            This will change in future releases.
        """
        return binmat._random_rxef(
            n, m, rank=rank, rng=rng, readonly=readonly, mode="rref"
        )

    @staticmethod
    def random_inv(
        n: int,
        *,
        rng: np.random.Generator | int | None = None,
        max_attempts: int | None = None,
        readonly: bool = False,
    ) -> tuple[binmat, binmat]:
        """
        Returns a random invertible matrix with given shape.
        This is done by rejection sampling, and a ``max_attempts`` can be set
        to limit the number of sampling attempts.
        """
        assert binmat.__validate_dim(n)
        assert max_attempts is None or validate(max_attempts, int)
        if not isinstance(rng, np.random.Generator):
            rng = np.random.default_rng(rng)
        shape = (n, n)
        num_attempts = 0
        while True:
            try:
                mat = binmat.random(*shape, rng=rng, readonly=readonly)
                mat_inv = ~mat
                return mat, mat_inv
            except binmat.NotInvertibleError:
                pass
            num_attempts += 1
            if max_attempts is not None and num_attempts >= max_attempts:
                raise binmat.NotInvertibleError(
                    "Failed to sample an invertible matrix "
                    f"within {max_attempts} attempts."
                )

    # TODO: restore matmul and matapp, but no need for matrices to be square...

    # @staticmethod
    # def matmul(matrices: Sequence[binmat], *, readonly: bool = False) -> binmat:
    #     """
    #     Performs matrix multiplication of a non-empty sequence of matrices.
    #     """
    #     validate(matrices, Sequence[binmat])
    #     assert binmat.__validate_square_matrices(matrices)
    #     return binmat(matmul_l2r([m._data for m in matrices]), readonly=readonly)

    # @overload
    # @staticmethod
    # def matapp(
    #     __vec: binvec,
    #     __matrices: Sequence[binmat],
    #     /,
    #     *,
    #     readonly: bool = False,
    # ) -> binvec:
    #     ...

    # @overload
    # @staticmethod
    # def matapp(
    #     __matrices: Sequence[binmat],
    #     __vec: binvec,
    #     /,
    #     *,
    #     readonly: bool = False,
    # ) -> binvec:
    #     ...

    # @staticmethod
    # def matapp(
    #     fst: Sequence[binmat] | binvec,
    #     snd: Sequence[binmat] | binvec,
    #     /,
    #     *,
    #     readonly: bool = False,
    # ) -> binvec:
    #     """
    #     Applies a sequence of matrices to a column vector (right-to-left),
    #     or a row-vector (left-to-right), depending on whether :class:`binvec`
    #     argument is passed as second argument or first argument, respectively.
    #     """
    #     assert validate(
    #         (fst, snd),
    #         tuple[binvec, Sequence[binmat]] | tuple[Sequence[binmat], binvec],
    #     )
    #     if isinstance(fst, binvec):
    #         vec, matrices = fst, cast(Sequence[binmat], snd)
    #         assert binmat.__validate_square_matrices(matrices, dim=len(vec))
    #         mat_data = [m._data for m in matrices]
    #         return binvec(matapp_rowvec(vec._data, mat_data))
    #     matrices, vec = fst, cast(binvec, snd)
    #     assert binmat.__validate_square_matrices(matrices, dim=len(vec))
    #     mat_data = [m._data for m in matrices]
    #     return binvec(matapp_colvec(mat_data, vec._data), readonly=readonly)

    @classmethod
    def _validate_data(cls, data: BinMat) -> Literal[True]:
        super()._validate_data(data)
        if len(data.shape) != 2:
            raise ValueError(
                f"Expected data to be 2D array, found shape {data.shape}."
            )
        return True

    __rank: int | None
    """
    A cached value for the matrix rank, or :obj:`None` if no value is cached.
    """

    __in_rcef: bool
    """
    An indicator of whether the matrix is known to be in RCEF.
    """

    __in_rref: bool
    """
    An indicator of whether the matrix is known to be in RREF.
    """

    __slots__ = ("__rank", "__in_rcef", "__in_rref")

    def __new__(
        cls, data: npt.ArrayLike, *, readonly: bool = False, copy: bool = False
    ) -> Self:
        """
        Creates a new matrix from binary data.

        If ``readonly=True``, the resulting tensor and its data are readonly.
        If ``copy=True``, a fresh copy of the given data is used.

        .. warning::

            The internal logic of :class:`binvec` presumes that the given data
            will not be mutated externally to the :class:`binvec` object after
            construction. If a fresh copy is needed, pass ``copy=True`` at
            construction.

        :meta public:
        """
        instance = super().__new__(cls, data, readonly=readonly, copy=copy)
        instance.__rank = None
        instance.__in_rcef = False
        instance.__in_rref = False
        return instance

    def _postprocess_mutation(self) -> None:
        """
        Invalidates cached information about rank and RCEF/RREF upon mutation.
        """
        super()._postprocess_mutation()
        self.__rank = None
        self.__in_rcef = False
        self.__in_rref = False

    @property
    def rows(self) -> binmat.Rows:
        """
        Returns a view of the matrix as a sequence of row vectors.
        """
        return binmat.Rows(self)

    @property
    def cols(self) -> binmat.Cols:
        """
        Returns a view of the matrix as a sequence of column vectors.
        """
        return binmat.Cols(self)

    @property
    def T(self) -> binmat:
        """
        Returns the transpose of the matrix.
        """

        mat = binmat(self._data.T)
        if (rank := self.__rank) is not None:
            mat.__rank = rank
            if self.__in_rcef:
                mat.__in_rref = True
            if self.__in_rref:
                mat.__in_rcef = True
        return mat

    @property
    def is_eye(self) -> bool:
        """
        Whether this is the identity matrix.
        """
        n, m = self._shape
        if n != m:
            return False
        return bool(np.all(self._data == np.eye(n)))

    @property
    def inverse(self) -> binmat:
        r"""
        The left inverse of this matrix over the field :math:`\mathbb{Z}_2`,
        or :obj:`None` if the matrix is not invertible.
        """
        n, m = self.shape
        if n != m:
            raise binmat.NotInvertibleError(
                f"Matrix to be inverted is not square, shape is {self.shape}."
            )
        if (rank := self.__rank) is not None and rank < n:
            raise binmat.NotInvertibleError(
                f"Matrix to be inverted is not full-rank, rank is {rank}."
            )
        rcef, inv = self.ext_rcef
        if rcef.rank < n:
            raise binmat.NotInvertibleError(
                f"Matrix to be inverted is not full-rank, rank is {rcef.rank}."
            )
        return inv

    @property
    def rcef(self) -> binmat:
        r"""
        Returns the reduced column echelon form (RCEF) of this matrix,
        computed over the field :math:`\mathbb{Z}_2`.
        """

        if self.__in_rcef:
            return self.copy()
        data, rank = rcef(self._data, ext=False)
        mat = binmat(data)
        mat.__rank = rank
        mat.__in_rcef = True
        return mat

    @property
    def rref(self) -> binmat:
        r"""
        Returns the reduced row echelon form (RREF) of this matrix,
        computed over the field :math:`\mathbb{Z}_2`.
        """

        if self.__in_rref:
            return self.copy()
        data, rank = rref(self._data, ext=False)
        mat = binmat(data)
        mat.__rank = rank
        mat.__in_rref = True
        return mat

    @property
    def ext_rcef(self) -> tuple[binmat, binmat]:
        r"""
        Returns the reduced column echelon form (RCEF) ``r`` of this matrix,
        computed over the field :math:`\mathbb{Z}_2`, together with the matrix
        ``m`` such that ``m@self == r``.

        If the matrix is invertible, ``r`` is the identity and ``m`` is its
        inverse.
        """

        n, m = self.shape
        ext_data, rank = rcef(self._data, ext=True)
        mat_rcef = binmat(ext_data[:n, :])
        mat_inv = binmat(ext_data[n:, :])
        mat_rcef.__rank = rank
        mat_rcef.__in_rcef = True
        mat_inv.__rank = m
        if self.__rank is None:
            self.__rank = rank
        return mat_rcef, mat_inv

    @property
    def ext_rref(self) -> tuple[binmat, binmat]:
        r"""
        Returns the reduced row echelon form (RREF) ``r`` of this matrix,
        computed over the field :math:`\mathbb{Z}_2`, together with the matrix
        ``m`` such that ``m@self == r``.

        If the matrix is invertible, ``r`` is the identity and ``m`` is its
        inverse.
        """

        n, m = self.shape
        ext_data, rank = rref(self._data, ext=True)
        mat_rref = binmat(ext_data[:, :m])
        mat_inv = binmat(ext_data[:, m:])
        mat_rref.__rank = rank
        mat_rref.__in_rref = True
        mat_inv.__rank = n
        if self.__rank is None:
            self.__rank = rank
        return mat_rref, mat_inv

    @property
    def rank(self) -> int:
        """
        Computes and returns the matrix rank.
        """
        if (rank := self.__rank) is None:
            _, rank = rcef(self._data, ext=False)
            self.__rank = rank
        return rank

    @property
    def is_fullrank(self) -> bool:
        """
        Whether the matrix is full rank.
        """
        return self.rank == min(self.shape)

    def copy(self, *, readonly: bool = False) -> Self:
        # pylint: disable=unused-private-member, assigning-non-slot
        mat = super().copy(readonly=readonly)
        if (rank := self.__rank) is not None:
            mat.__rank = rank
            mat.__in_rcef = self.__in_rcef
            mat.__in_rref = self.__in_rref
        return mat

    def __or__(self, other: binmat) -> binmat:
        """
        Horizontal stacking of two matrices.

        :meta public:
        """
        if not isinstance(other, binmat):
            return NotImplemented
        return binmat.hstack([self, other])

    def __invert__(self) -> binmat:
        """
        Same as :attr:`inverse`.

        :meta public:
        """
        return self.inverse

    @overload
    def __matmul__(self, other: binvec) -> binvec: ...

    @overload
    def __matmul__(self, other: binmat) -> binmat: ...

    def __matmul__(self, other: binvec | binmat) -> binvec | binmat:
        r"""
        Performs matrix-vector or matrix-matrix multiplication over the
        field :math:`\mathbb{Z}_2`, depending on the type of ``other``.

        :raises ShapeError: if the intermediate dimensions don't match.

        :meta public:
        """
        if not isinstance(other, (binvec, binmat)):
            return NotImplemented
        assert self.__has_compatible_matmul_shape(other)
        res = cast(BinVecOrMat, matmul2(self._data, other._data))
        if isinstance(other, binvec):
            return binvec(res)
        return binmat(res)

    def __imatmul__(self, other: binmat) -> binmat:  # type: ignore[misc]
        r"""
        Performs inplace matrix-matrix multiplication over the
        field :math:`\mathbb{Z}_2`.

        :raises ShapeError: if the intermediate dimensions don't match.

        :meta public:
        """
        if self._readonly:
            raise bintensor.ReadonlyError("Tensor is read-only.")
        if not isinstance(other, binmat):
            return NotImplemented
        assert self.__has_compatible_matmul_shape(other)
        self._data = cast(BinMat, matmul2(self._data, other._data))
        self._postprocess_mutation()
        return self

    @overload
    def __getitem__(self, idx: MatBitIdx) -> Bit: ...

    @overload
    def __getitem__(self, idx: MatSubvecIdx) -> binvec: ...

    @overload
    def __getitem__(self, idx: MatSubmatIdx) -> binmat: ...

    def __getitem__(
        self, idx: MatBitIdx | MatSubvecIdx | MatSubmatIdx
    ) -> Bit | binvec | binmat:
        """
        If the index is an integer, returns the corresponding row of the matrix.
        If the index is a slice or a list/array of integers, returns the
        binary matrix containing the selected rows.

        :meta public:
        """
        # pylint: disable=unused-private-member
        assert validate(idx, MatBitIdx | MatSubvecIdx | MatSubmatIdx)
        sliced_data = self._data[idx]
        if not isinstance(sliced_data, np.ndarray):
            return cast(Bit, int(sliced_data))
        if len(sliced_data.shape) == 1:
            return binvec(sliced_data)
        assert len(sliced_data.shape) == 2
        return binmat(sliced_data)

    # TODO: implement __setitem__ for binmat
    #       remember to check for readonly and call _postprocess_mutation

    def __iter__(self) -> Iterator[binvec]:
        """
        Iterates over the rows of the matrix.

        :meta public:
        """
        data = self._data
        n, _ = data.shape
        for r in range(n):
            yield binvec(data[r, :])

    def __len__(self) -> int:
        """
        The number of rows in the matrix.

        :meta public:
        """
        return self.shape[0]

    @staticmethod
    def __validate_dim(dim: int, *, positive: bool = True) -> Literal[True]:
        validate(dim, int)
        qual = "positive" if positive else "non-negative"
        if dim < 0 or (positive and dim == 0):
            raise ValueError(f"Dimension must be {qual}, found {dim}.")
        return True

    @staticmethod
    def __validate_shape(
        n: int, m: int, *, positive: bool = True
    ) -> Literal[True]:
        binmat.__validate_dim(n, positive=positive)
        binmat.__validate_dim(m, positive=positive)
        return True

    @staticmethod
    def __validate_pivots(
        n: int, m: int, pivots: IntVec, mode: Literal["rref", "rcef"]
    ) -> Literal[True]:
        validate(pivots, IntVec)
        validate(mode, Literal["rref", "rcef"])
        k = n if mode == "rcef" else m
        if not np.all(pivots[1:] > pivots[:-1]):
            raise ValueError("Pivots must be strictly increasing.")
        if pivots[0] < 0 or pivots[-1] >= k:
            raise ValueError(f"Pivots must be in range({k}).")
        return True

    @staticmethod
    def __validate_params(
        params: BinVec | None, num_params: int
    ) -> Literal[True]:
        if params is None:
            return True
        validate(params, BinVec)
        if not np.all((params == 0) | (params == 1)):
            raise ValueError("RCEF param values must be all 0 or 1.")
        if params.shape != (num_params,):
            raise ValueError(
                f"Expected param shape to be {(num_params,)} "
                f"found shape {params.shape}."
            )
        return True

    # @staticmethod
    # def __validate_square_matrices(
    #     matrices: Sequence[binmat], dim: int | None = None
    # ) -> Literal[True]:
    #     if dim is None:
    #         if not matrices:
    #             raise ValueError("Expected at least one matrix.")
    #         dim = matrices[0].shape[0]
    #     for idx, m in enumerate(matrices):
    #         if m.shape != (dim, dim):
    #             raise BinTensor.ShapeError(
    #                 f"Expected matrices of square shape ({dim}, {dim}), "
    #                 f"matrix at idx {idx} has shape {m.shape} instead."
    #             )
    #     return True

    def __has_compatible_matmul_shape(
        self, other: binvec | binmat
    ) -> Literal[True]:
        if self.shape[-1] != other._shape[0]:
            ss, os = self._shape, other._shape
            raise bintensor.ShapeError(
                f"unsupported operand shapes for @: {ss} and {os}"
            )
        return True
