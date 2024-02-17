"""
Binary vectors.
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
from collections.abc import Iterable, Iterator, Sequence
from itertools import product
from numbers import Integral
from typing import TYPE_CHECKING, Any, Literal, cast, final, overload
from typing_extensions import Self
import numpy as np
import numpy.typing as npt
from typing_validation import validate
from .vectorized import (
    BinVec,
    bits_from_bytes,
    bytes_from_bits,
)
from .base import bintensor

if TYPE_CHECKING:
    from .binmat import binmat

Bit = Literal[0, 1]
"""
Type alias for a bit value.
"""


@final
class binvec(bintensor):
    r"""
    A mutable vector over the field :math:`\mathbb{Z}_2`.
    """

    @staticmethod
    def validate_dim(dim: int, *, positive: bool = True) -> Literal[True]:
        """
        Validate a :class:`binvec` dimension.
        Raises :obj:`TypeError` or :obj:`ValueError` for invalid dimensions,
        returns :obj:`True` otherwise.
        """
        validate(dim, int)
        qual = "positive" if positive else "non-negative"
        if dim < 0 or (positive and dim == 0):
            raise ValueError(f"Dimension must be {qual}, found {dim}.")
        return True

    @staticmethod
    def validate_bitstr(bits: str) -> Literal[True]:
        """
        Validate a binary string.
        Raises :obj:`TypeError` or :obj:`ValueError` for invalid strings,
        returns :obj:`True` otherwise.
        """
        validate(bits, str)
        if not all(b in "01" for b in bits):
            raise ValueError("Characters in bitstring must be '0' or '1'.")
        return True

    @staticmethod
    def zeros(dim: int, *, readonly: bool = False) -> binvec:
        """
        Constructs a zero binary vector with given dimension.
        """
        assert binvec.validate_dim(dim, positive=False)
        return binvec(np.zeros(dim, dtype=np.uint8), readonly=readonly)

    @staticmethod
    def random(
        dim: int,
        *,
        rng: np.random.Generator | int | None = None,
        readonly: bool = False,
    ) -> binvec:
        """
        Random binary vector with given dimension.
        """
        assert validate(dim, int)
        if not isinstance(rng, np.random.Generator):
            rng = np.random.default_rng(rng)
        bits = rng.integers(0, 2, (dim,), dtype=np.uint8)
        return binvec(bits, readonly=readonly)

    @staticmethod
    def el(idx: int, dim: int, *, readonly: bool = False) -> binvec:
        """
        Returns the canonical basis vector with given index in given dimension.
        """
        assert validate(idx, int)
        assert binvec.validate_dim(dim)
        idx %= dim
        data = np.zeros(dim, dtype=np.uint8)
        data[idx] = 1
        return binvec(data, readonly=readonly)

    @staticmethod
    def iter_std_basis(dim: int, *, readonly: bool = False) -> Iterator[binvec]:
        """
        Iterates through all standard basis binary vectors with given dimension.
        """
        assert binvec.validate_dim(dim, positive=False)
        for idx in range(dim):
            data = np.zeros(dim, dtype=np.uint8)
            data[idx] = 1
            yield binvec(data, readonly=readonly)

    @staticmethod
    def iter_all(dim: int, *, readonly: bool = False) -> Iterator[binvec]:
        """
        Iterates through all binary vectors with given dimension.
        """
        assert binvec.validate_dim(dim, positive=False)
        if dim == 0:
            yield binvec.zeros(0)
            return
        for data in product([0, 1], repeat=dim):
            yield binvec(data, readonly=readonly)

    @staticmethod
    def from_bool(bits: Iterable[Any], *, readonly: bool = False) -> binvec:
        """
        Constructs a binary vector from an interable of boolean values.
        """
        data = np.fromiter((1 if b else 0 for b in bits), dtype=np.uint8)
        return binvec(data, readonly=readonly)

    @staticmethod
    def from_str(bits: str, *, readonly: bool = False) -> binvec:
        """
        Constructs a binary vector from a string with chars ``'0'`` and ``'1'``.
        """
        assert validate(bits, str)
        assert binvec.validate_bitstr(bits)
        data = np.array([int(b, 2) for b in bits], dtype=np.uint8)
        return binvec(data, readonly=readonly)

    @staticmethod
    def from_int(bits: int, n: int) -> binvec:
        """
        Constructs a binary vector from an integer.
        """
        assert validate(bits, int)
        assert validate(n, int)
        bits %= 2**n
        if n == 0:
            return binvec([])
        data = np.array(
            [int(b) for b in bin(bits)[2:].zfill(n)], dtype=np.uint8
        )
        return binvec(data)

    @staticmethod
    def hstack(vecs: Sequence[binvec], *, readonly: bool = False) -> binvec:
        """
        Stacks the given vectors horizontally.
        """
        assert validate(vecs, Sequence[binvec])
        return binvec(np.hstack([v._data for v in vecs]), readonly=readonly)

    @staticmethod
    def from_bytes(
        b: bytes, num_bits: int | None = None, *, readonly: bool = False
    ) -> binvec:
        """
        Converts bytes to a binary vector containing the corresponding bits.
        The binary vector has length ``8*len(b)`` by default, containing all
        bits, but length can be truncated by specifying a desired ``num_bits``
        between ``len(b)-7`` and ``len(b)`` (both inclusive).
        If a length is specified, the bits ignored at the end must all be zero.
        """
        if num_bits is None:
            num_bits = len(b) * 8
        if len(b) * 8 - num_bits not in range(8):
            raise ValueError(f"Expected n in range({len(b)*8-7}, {len(b)*8+1})")
        b_array = np.fromiter(b, dtype=np.uint8)
        if num_bits % 8 != 0 and b_array[-1] & (
            2 ** (k := 8 - num_bits % 8) - 1
        ):
            raise ValueError(
                f"Expected last {k} bits to be zero, "
                f"found {b_array[-1]&(2**k-1):0>{k}b}"
            )
        return binvec(bits_from_bytes(b_array, num_bits), readonly=readonly)

    @classmethod
    def _validate_data(cls, data: BinVec) -> Literal[True]:
        super()._validate_data(data)
        if len(data.shape) != 1:
            raise ValueError(
                f"Expected data to be 1D array, found shape {data.shape}."
            )
        return True

    def __new__(
        cls, data: npt.ArrayLike, *, readonly: bool = False, copy: bool = False
    ) -> Self:
        """
        Creates a new vector from binary data.

        If ``readonly=True``, the resulting tensor and its data are readonly.
        If ``copy=True``, a fresh copy of the given data is used.

        .. warning::

            The internal logic of :class:`binvec` presumes that the given data
            will not be mutated externally to the :class:`binvec` object after
            construction. If a fresh copy is needed, pass ``copy=True`` at
            construction.

        :meta public:
        """
        if not isinstance(data, np.ndarray) or data.dtype != np.uint8:
            data = np.array(data, dtype=np.uint8)
        return super().__new__(
            cls, cast(BinVec, data), readonly=readonly, copy=copy
        )

    @property
    def bin(self) -> str:
        """
        Binary string representation of this binary vector.
        """
        return "".join(str(b) for b in self)

    def __bytes__(self) -> bytes:
        """
        Converts this binary vector to bytes.

        :meta public:
        """
        return bytes(bytes_from_bits(self._data))

    @overload
    def __getitem__(self, idx: int) -> Bit: ...

    @overload
    def __getitem__(self, idx: slice | list[int]) -> binvec: ...

    def __getitem__(self, idx: int | slice | list[int]) -> Bit | binvec:
        """
        If the index is an integer, returns the corresponding entry of the vec.
        If the index is a slice or a list/array of integers, returns the
        vec containing the selected entries.

        :meta public:
        """
        if isinstance(idx, int):
            return cast(Bit, int(self._data[idx]))
        assert validate(idx, slice | list[int])
        return binvec(self._data[idx])

    @overload
    def __setitem__(self, idx: int, value: int) -> None: ...

    @overload
    def __setitem__(
        self, idx: slice | list[int], value: int | binvec
    ) -> None: ...

    def __setitem__(
        self, idx: int | slice | list[int], value: int | binvec
    ) -> None:
        """
        Sets a single value, or a slice/selection of values.

        :meta public:
        """
        if self._readonly:
            raise binvec.ReadonlyError("Tensor is read-only.")
        if isinstance(idx, int):
            assert validate(value, Integral)
            self._data[idx] = int(cast(Integral, value)) % 2
        else:
            assert validate(idx, slice | list[int])
            if isinstance(value, binvec):
                self._data[idx] = value._data
            else:
                self._data[idx] = int(value) % 2
        self._postprocess_mutation()

    def __or__(self, other: binvec) -> binvec:
        """
        Horizontal stacking of two vectors.

        :meta public:
        """
        if not isinstance(other, binvec):
            return NotImplemented
        return binvec.hstack([self, other])

    @overload
    def __matmul__(self, other: binvec) -> Bit: ...

    @overload
    def __matmul__(self, other: binmat) -> binvec: ...

    def __matmul__(self, other: binvec | binmat) -> Bit | binvec:
        r"""
        Vector-vector inner product or vector-matrix multiplication over the
        field :math:`\mathbb{Z}_2`.

        :raises ShapeError: if the intermediate dimensions don't match.

        :meta public:
        """

        from .binmat import binmat

        if not isinstance(other, (binvec, binmat)):
            return NotImplemented
        assert self.__has_compatible_matmul_shape(other)
        res = (self._data @ other._data) % 2
        if isinstance(other, binmat):
            return binvec(cast(BinVec, res))
        return cast(Bit, int(res))

    def __imatmul__(self, other: binmat) -> binvec:  # type: ignore[misc]
        r"""
        Inplace vector-matrix multiplication over the field :math:`\mathbb{Z}_2`

        :raises ShapeError: if the intermediate dimensions don't match.

        :meta public:
        """
        if self._readonly:
            raise bintensor.ReadonlyError("Tensor is read-only.")

        from .binmat import binmat

        if not isinstance(other, binmat):
            return NotImplemented
        assert self.__has_compatible_matmul_shape(other)
        self._data = (self._data @ other._data) % 2  # type: ignore
        self._postprocess_mutation()
        return self

    def __len__(self) -> int:
        """
        The dimension of this binary vector (i.e. the number of bits).

        :meta public:
        """
        return self._shape[0]

    def __iter__(self) -> Iterator[Bit]:
        """
        Iterates over the bits in this binary vector.

        :meta public:
        """
        for b in self._data:
            yield cast(Bit, int(b))

    def __int__(self) -> int:
        """
        Converts the binary vector to an integer.

        :meta public:
        """
        n = len(self)
        return int(
            np.sum(self._data * 2 ** (n - 1 - np.arange(n, dtype=np.uint64)))
        )

    def __has_compatible_matmul_shape(
        self, other: binvec | binmat
    ) -> Literal[True]:
        if self.shape[-1] != other._shape[0]:
            ss, os = self._shape, other._shape
            raise bintensor.ShapeError(
                f"unsupported operand shapes for @: {ss} and {os}"
            )
        return True
