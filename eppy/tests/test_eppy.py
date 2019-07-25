# Copyright (c) 2019 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"py.test for functions in __init__"

import pytest

import eppy
from eppy.pytest_helpers import do_integration_tests
import eppy.idd_helpers as idd_helpers


@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set"
)
def test_newidf():
    """py.test for newidf"""
    data = ((idd_helpers.latestidd(), idd_helpers.latestidd()),)  # ver, expected
    for ver, expected in data:
        idf = eppy.newidf(ver)
        result = idf.idfobjects["version".upper()][0]
        assert result.Version_Identifier == expected
