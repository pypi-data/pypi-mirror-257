"""
Abstract base class for binary tensors.
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
from numbers import Integral
from typing import Any, Literal, TypeVar, overload
from typing_extensions import Self
import numpy as np
import numpy.typing as npt
from typing_validation import validate

from .vectorized import BinTensor

Shape = tuple[int, ...]
""" Type alias for tensor shapes. """

_ScalarType = TypeVar("_ScalarType", bound=np.generic)


class bintensor:
    r"""
    Abstract base class for mutable tensors over the field :math:`\mathbb{Z}_2`.
    """

    class ShapeError(ValueError):
        """
        Specialised :obj:`ValueError` subclass for shape errors.
        """

    class ReadonlyError(ValueError):
        """
        Specialised :obj:`ValueError` subclass for when attempting to mutate
        a readonly tensor.
        """

    @classmethod
    def make_readonly(cls, *tensors: bintensor) -> None:
        """
        Makes all given tensors readonly.
        """
        for t in tensors:
            t.readonly = True

    @classmethod
    def _validate_data(cls, data: BinTensor) -> Literal[True]:
        """
        Class method enforcing data validity.
        Can be overridden by subclasses to include additional checks.
        """
        if not np.all((data == 0) | (data == 1)):
            raise ValueError("Bin array data value must be all 0 or 1.")
        return True

    _shape: tuple[int, ...]
    _data: BinTensor
    _readonly: bool
    __hash: int
    __is_zero: bool

    __slots__ = (
        "__weakref__",
        "_shape",
        "_data",
        "_readonly",
        "__hash",
        "__is_zero",
    )

    def __new__(
        cls, data: npt.ArrayLike, *, readonly: bool = False, copy: bool = False
    ) -> Self:
        """
        Creates a new tensor with given shape from the given binary data.
        The class :class:`BinTensor` cannot be instantiated directly.

        If ``readonly=True``, the resulting tensor and its data are readonly.
        If ``copy=True``, a fresh copy of the given data is used.

        .. warning::

            The internal logic of the :class:`BinTensor` class and its
            subclasses presumes that the given data will not be mutated
            externally to the :class:`BinTensor` object after construction.
            If a fresh copy is needed, pass ``copy=True`` at construction.

        :meta public:
        """
        assert cls is not bintensor, "Can't instantiate class 'bintensor'."
        if not isinstance(data, np.ndarray) or data.dtype != np.uint8:
            data = np.array(data, dtype=np.uint8)
            copy = False
        assert cls._validate_data(data)
        if copy:
            data = data.copy()
        if readonly:
            data.flags.writeable = False
            data = data.view()
        instance = super().__new__(cls)
        instance._shape = data.shape
        instance._data = data
        instance._readonly = readonly
        return instance

    def __getnewargs_ex__(self) -> tuple[tuple[BinTensor], dict[str, Any]]:
        """
        Method for pickling.
        """
        return (self._data,), {"readonly": self._readonly}

    # TODO: data compression on pickling
    # TODO: data decompression on unpickling
    # Move the __bytes__ and from_bytes logic from binvec to here,
    # reshape/linearise tensor data and include shape information in the bytes
    # as a header: shape length (uint8), shape (tuple of varints), data (bytes)
    # https://github.com/multiformats/unsigned-varint

    @property
    def shape(self) -> Shape:
        """
        The shape of this bit tensor.
        """
        return self._shape

    @property
    def data(self) -> BinTensor:
        """
        The underlying binary data.
        """
        return self._data

    @property
    def readonly(self) -> bool:
        """
        Whether the tensor is readonly.
        """
        return self._readonly

    @readonly.setter
    def readonly(self, value: Literal[True]) -> None:
        """
        Makes the tensor readonly.
        """
        assert validate(value, Literal[True])
        if self._readonly:
            return
        data = self._data
        data.flags.writeable = False
        self._data = data.view()
        self._readonly = True

    @property
    def is_zero(self) -> bool:
        """
        Whether the tensor is the constant zero tensor.
        """
        try:
            return self.__is_zero
        except AttributeError:
            self.__is_zero = (is_zero := bool(np.all(self._data == 0)))
            return is_zero

    def copy(self, *, readonly: bool = False) -> Self:
        """
        Returns a copy of this tensor.
        If ``readonly=True``, the resulting copy is readonly.
        """
        return type(self)(self._data.copy(), readonly=readonly)

    def _postprocess_mutation(self) -> None:
        """
        Method called when tensor data is potentially mutated.
        Can be overridden by subclasses to avoid stale cache values.
        """
        assert (
            not self._readonly
        ), "You have mutated a readonly tensor, data integrity not guaranteed."
        self._shape = self._data.shape

    def _same_shape(self, other: bintensor, op: str) -> Literal[True]:
        """
        Enforces that this and the other given tensor have the same shape.
        The ``op`` argument refers to the operation being performed,
        and is used by the error message.
        """
        if self._shape != other._shape:
            ss, os = self._shape, other._shape
            raise bintensor.ShapeError(
                f"unsupported operand shapes for {op}: {ss} and {os}"
            )
        return True

    def _same_type(self, other: bintensor, op: str) -> Literal[True]:
        """
        Enforces that the other tensor is an instance of this tensor's class.
        The ``op`` argument refers to the operation being performed,
        and is used by the error message.
        """
        cls = type(self)
        if not isinstance(other, cls):
            st_str = cls.__name__
            ot_str = type(other).__name__
            raise TypeError(
                f"unsupported operand types for {op}: {st_str} and {ot_str!r}"
            )
        return True

    def __pos__(self) -> Self:
        """
        Returns the tensor unchanged.

        :meta public:
        """
        return self

    def __neg__(self) -> Self:
        """
        Componentwise mod 2 negation: returns the tensor unchanged.

        :meta public:
        """
        return self

    def __add__(self, other: Self | Integral) -> Self:
        """
        Componentwise mod 2 addition (bitwise XOR).
        :raises ShapeError: if the tensors have different shapes.

        :meta public:
        """
        cls = type(self)
        if isinstance(other, Integral):
            return cls(self._data ^ (int(other) % 2))
        if not isinstance(other, cls):
            return NotImplemented
        assert self._same_shape(other, "+")
        return cls(self._data ^ other._data)

    def __sub__(self, other: Self | Integral) -> Self:
        """
        Alias for :meth:`__add__`.

        :meta public:
        """
        return self + other

    def __mul__(self, other: Self | Integral) -> Self:
        """
        Componentwise mod 2 multiplication (bitwise AND).
        :raises ShapeError: if the tensors have different shapes.

        :meta public:
        """
        cls = type(self)
        if isinstance(other, Integral):
            return cls(self._data * (int(other) % 2))
        if not isinstance(other, cls):
            return NotImplemented
        assert self._same_shape(other, "*")
        return cls(self._data * other._data)

    def __iadd__(self, other: Self | Integral) -> Self:
        """
        Inplace componentwise mod 2 addition (bitwise XOR).
        :raises ShapeError: if the tensors have different shapes.

        :meta public:
        """
        if self._readonly:
            raise bintensor.ReadonlyError("Tensor is read-only.")
        if isinstance(other, Integral):
            self._data ^= int(other) % 2
        else:
            assert self._same_type(other, "+=")
            assert self._same_shape(other, "+=")
            self._data ^= other._data
        self._postprocess_mutation()
        return self

    def __isub__(self, other: Self | Integral) -> Self:
        """
        Alias for :meth:`__iadd__`.

        :meta public:
        """
        return self.__iadd__(other)

    def __imul__(self, other: Self | Integral) -> Self:
        """
        Inplace componentwise mod 2 multiplication (bitwise AND).
        :raises ShapeError: if the tensors have different shapes.

        :meta public:
        """
        if self._readonly:
            raise bintensor.ReadonlyError("Tensor is read-only.")
        if isinstance(other, Integral):
            self._data *= int(other) % 2
        else:
            assert self._same_type(other, "*=")
            assert self._same_shape(other, "*=")
            self._data *= other._data
        self._postprocess_mutation()
        return self

    def __eq__(self, other: Any) -> bool:
        # if other in (0, 1):
        #     return bool(np.all(self._data == other))
        if type(self) != type(other):
            return NotImplemented
        return self._shape == other._shape and bool(
            np.all(self._data == other._data)
        )

    def __repr__(self) -> str:
        s = repr(self._data)
        assert s.startswith("array"), s
        if s.endswith(", dtype=uint8)"):
            end = -14
        else:
            assert s.endswith("dtype=uint8)"), s
            end = -12
        cls = type(self)
        cls_name = cls.__name__
        indent = " " * (len(cls_name) + len(self.shape))
        s = cls_name + s[5:end] + ")"
        return "\n".join(
            indent + line.strip() if idx > 0 else line
            for idx, line in enumerate(s.split("\n"))
        )

    def __hash__(self) -> int:
        try:
            return self.__hash
        except AttributeError:
            if not self._readonly:
                raise TypeError(
                    "Only readonly tensors can be hashed."
                ) from None
            h = hash((type(self), self._shape, bytes(self._data)))
            self.__hash = h
            return h

    @overload
    def __array__(self, dtype: None = None, /) -> npt.NDArray[np.uint8]: ...

    @overload
    def __array__(self, dtype: _ScalarType, /) -> npt.NDArray[_ScalarType]: ...

    def __array__(self, dtype: _ScalarType | None = None) -> Any:
        return self._data.__array__(dtype)
