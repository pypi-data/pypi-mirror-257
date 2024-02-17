"""
Options for the :mod:`q1ss` library.
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

from typing import Final
from optmanage import Option, OptionManager

try:
    import numba  # type: ignore
except ModuleNotFoundError:
    numba = None

try:
    import cupy as cp  # type: ignore
except ModuleNotFoundError:
    cp = None


def _validate_use_gpu(use_gpu: bool) -> None:
    if use_gpu:
        if numba is None:
            raise ValueError(
                "Cannot use GPU: 'numba' library must be installed."
            )
        if cp is None:
            raise ValueError(
                "Cannot use GPU: 'cupy' library must be installed."
            )


class Q1SSOptions(OptionManager):
    """
    Global options class for the :mod:`q1ss` library.
    """

    use_gpu: Option[bool] = Option(bool, cp is not None, _validate_use_gpu)
    """
    Whether to use GPU acceleration on matrix-matrix and matrix-vector
    multiplication.
    Can only be used if the `numba <https://numba.readthedocs.io/en/stable/>`_
    and `cupy <https://docs.cupy.dev/en/stable/>`_ libraries are installed.
    """


options: Final[Q1SSOptions] = Q1SSOptions()
"""
Global options for the :mod:`q1ss` library.
"""
