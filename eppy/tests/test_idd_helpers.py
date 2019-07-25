# Copyright (c) 2019 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for idd_helpers"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import eppy.idd_helpers as idd_helpers


def test_folder2ver():
    """py.test for folder2ver"""
    data = (
        ("EnergyPlus-8-8-0", "8.8.0"),  # folder, expected
        ("EnergyPlusV8-8-0", "8.8.0"),  # folder, expected
    )
    for folder, expected in data:
        result = idd_helpers.folder2ver(folder)
        assert result == expected
