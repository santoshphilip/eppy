# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""pytest for idfreader. very few tests"""

import pytest
from six import StringIO

import eppy.idfreader as idfreader
from eppy.pytest_helpers import do_integration_tests


def test_iddversiontuple():
    """py.test for iddversiontuple"""
    iddtxt = """stuff 9.8.4
    other stuff"""
    fhandle = StringIO(iddtxt)
    result = idfreader.iddversiontuple(fhandle)
    assert result == (9, 8, 4)


def test_makeabunch():
    pass


def test_makebunches():
    pass


def test_makebunches_alter():
    pass


def test_convertfields():
    pass


def test_convertallfields():
    pass


def test_addfunctions():
    pass


def test_addfunctions2new():
    pass


@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set")
def test_idfreader():
    pass


@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set")
def test_idfreader1():
    pass
