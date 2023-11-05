# Copyright (c) 2019 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"py.test for functions in __init__"

import os
import pytest

import eppy
from eppy.pytest_helpers import do_integration_tests
import eppy.idd_helpers as idd_helpers
from tests.pytest_helpers import safeIDDreset

try:
    VERSION = os.environ['ENERGYPLUS_VERSION']  # used in CI files
except KeyError:
    VERSION = "8.9.0"  # current default for integration tests on local system
IDDVERSION = VERSION

def teardown_module(module):
    """new IDD has been set in the module. Here you tear it down"""
    safeIDDreset()
    
def versiontuple(vers):
    """version tuple"""
    return tuple([int(num) for num in vers.split(".")])

@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set"
)
def test_newidf1():
    """py.test for newidf"""
    data = ((idd_helpers.latestidd(), idd_helpers.latestidd()),)  # ver, expected
    for ver, expected in data:
        idf = eppy.newidf(ver)
        result = idf.idfobjects["version".upper()][0]
        assert result.Version_Identifier == expected
        
@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set"
)
def test_newidf2():
    import eppy
    # Now test the following
    #
    # :Problem: eppy.newidf(version=None) does not work correctly
    # :Solution:
    #
    # There are starting conditions here:
    #
    # 1. IDD is already set
    #     - if IDD has been set, it should use that IDD
    #     - eppy.newidf(version=wrongIDD): throw exception
    # 2. IDD has not been set
    #     - if eppy.newidf(version=None), it should throw an exception
    #     - if eppy.newidf(version=some_version), it shoule use that some_version of IDD

    # 1. IDD is already set
    #     - if IDD has been set, it should use that IDD

    safeIDDreset()
    iddversion = IDDVERSION
    idf1 = eppy.newidf(version=iddversion) # this will set the IDD version
    idf2 = eppy.newidf(version=None)
    assert idf2.idd_version == versiontuple(iddversion)
    #     - eppy.newidf(version=wrongIDD): throw exception
    wrongiddversion = "8.9.9"
    with pytest.raises(eppy.easyopen.MissingIDDException):
        idf3 = eppy.newidf(version=wrongiddversion)
    # 2. IDD has not been set
    #     - if eppy.newidf(version=None), it should throw an exception
    safeIDDreset()
    with pytest.raises(eppy.modeleditor.IDDNotSetError):
        idf4 = eppy.newidf(version=None)
    #     - if eppy.newidf(version=some_version), it shoule use that some_version of IDD
    idf5 = eppy.newidf(version=iddversion)
    assert idf5.idd_version == versiontuple(iddversion)
