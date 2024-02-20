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
Quantum tomography data for RB
"""

# Needed for functions
from functools import reduce
from re import match
from typing import Dict, Union, List


###########################################################################
# Data formats for converting from counts to fitter data
#
# TODO: These should be moved to a terra.tools module
###########################################################################


def marginal_counts(
    counts: Dict[str, int],
    meas_qubits: Union[bool, List[int]] = True,
    pad_zeros: bool = False,
) -> Dict[str, int]:
    """
    Compute marginal counts from a counts dictionary.

    Args:
        counts: a counts dictionary.
        meas_qubits: (default: True) the qubits to NOT be marinalized over
            if this is True meas_qubits will be all measured qubits.
        pad_zeros: (default: False) Include zero count outcomes in return dict.

    Returns:
        A counts dictionary for the specified qubits. The returned dictionary
        will have any whitespace trimmed from the input counts keys. Thus if
        meas_qubits=True the returned dictionary will have the same values as
        the input dictionary, but with whitespace trimmed from the keys.
    """

    # Extract total number of qubits from first count key
    # We trim the whitespace seperating classical registers
    # and count the number of digits
    num_qubits = len(next(iter(counts)).replace(" ", ""))

    # Check if we do not need to marginalize. In this case we just trim
    # whitespace from count keys
    if (meas_qubits is True) or (num_qubits == len(meas_qubits)):
        ret = {}
        for key, val in counts.items():
            key = key.replace(" ", "")
            ret[key] = val
        return ret

    # Sort the measured qubits into decending order
    # Since bitstrings have qubit-0 as least significant bit
    if meas_qubits is True:
        meas_qubits = range(num_qubits)  # All measured
    qubits = sorted(meas_qubits, reverse=True)

    # Generate bitstring keys for measured qubits
    meas_keys = count_keys(len(qubits))

    # Get regex match strings for summing outcomes of other qubits
    rgx = []
    for key in meas_keys:

        def helper(x, y):
            if y in qubits:
                return key[qubits.index(y)] + x
            return "\\d" + x

        rgx.append(reduce(helper, range(num_qubits), ""))

    # Build the return list
    meas_counts = []
    for m in rgx:
        c = 0
        for key, val in counts.items():
            if match(m, key.replace(" ", "")):
                c += val
        meas_counts.append(c)

    # Return as counts dict on measured qubits only
    if pad_zeros is True:
        return dict(zip(meas_keys, meas_counts))
    ret = {}
    for key, val in zip(meas_keys, meas_counts):
        if val != 0:
            ret[key] = val
    return ret


def count_keys(num_qubits: int) -> List[str]:
    """Return ordered count keys.

    Args:
        num_qubits: The number of qubits in the generated list.
    Returns:
        The strings of all 0/1 combinations of the given number of qubits
    Example:
        >>> count_keys(3)
        ['000', '001', '010', '011', '100', '101', '110', '111']
    """
    return [bin(j)[2:].zfill(num_qubits) for j in range(2**num_qubits)]
