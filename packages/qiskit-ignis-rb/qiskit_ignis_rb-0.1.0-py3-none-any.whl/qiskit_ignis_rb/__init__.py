# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


"""
Randomized Benchmarking module
"""

import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "qiskit-ignis-rb"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


# Randomized Benchmarking functions
# flake8: noqa: F401
from .circuits import randomized_benchmarking_seq
from .fitters import RBFitter, InterleavedRBFitter, PurityRBFitter, CNOTDihedralRBFitter
from .rb_utils import (
    count_gates,
    gates_per_clifford,
    coherence_limit,
    twoQ_clifford_error,
    calculate_1q_epg,
    calculate_2q_epg,
    calculate_1q_epc,
    calculate_2q_epc,
)
from .rb_groups import RBgroup
