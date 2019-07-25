# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for EPlusInterfaceFunctions.parse_idd.py"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import eppy.EPlusInterfaceFunctions.parse_idd as parse_idd


def test_extractidddata():
    """py.test for extractidddata"""
    assert 1 == 1


def test_removeblanklines():
    """py.test for removeblanklines"""
    tdata = (
        # unix line endings
        ("1\n2", "1\n2"),  # astr, nstr
        ("1\n\n2", "1\n2"),  # astr, nstr
        ("1\n   \n2", "1\n2"),  # astr, nstr
        # dos line endings
        ("1\r\n2", "1\n2"),  # astr, nstr
        ("1\r\n\r\n2", "1\n2"),  # astr, nstr
        ("1\r\n   \r\n2", "1\n2"),  # astr, nstr
        # mac line endings
        ("1\r2", "1\n2"),  # astr, nstr
        ("1\r\r2", "1\n2"),  # astr, nstr
        ("1\r   \r2", "1\n2"),  # astr, nstr
        # mixed unix and dos line endings
        ("1\r\n2\n3", "1\n2\n3"),  # astr, nstr
    )
    for astr, nstr in tdata:
        result = parse_idd.removeblanklines(astr)
        # print(astr.__repr__(), nstr.__repr__(), result.__repr__())
        assert result == nstr
