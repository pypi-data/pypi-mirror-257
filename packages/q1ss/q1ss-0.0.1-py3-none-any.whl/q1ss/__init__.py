"""
This library contains experimental implementations of quantum one-shot signatures by authors from the QSig Commission and other contributors, with special focus on blockchain technology.

Summary of contents:

- The :mod:`~q1ss.binalg` module contains binary linear algebra primitives used
  by the remainder of the library.
- The :mod:`~q1ss.ap` module contains implementations of affine partition functions.

"""

# Q1SS: Experimental development of Quantum 1-Shot Signatures.
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

__version__ = "0.0.1"

from .utils.options import options

__all__ = ("options",)
