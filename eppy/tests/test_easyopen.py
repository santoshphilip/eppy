# Copyright (c) 2018 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for idf_helpers.easyopen"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import pytest

from eppy import modeleditor
import eppy.easyopen as easyopen
from eppy.pytest_helpers import do_integration_tests
import eppy.runner.run_functions as run_functions

from six import StringIO
from six.moves import reload_module as reload

def _latestidd():
    """extract the latest idd installed"""
    pth, _ = run_functions.install_paths('8.8.0')
    dirpth = os.path.dirname(pth)
    dirpth = os.path.dirname(dirpth)
    alldirs = os.listdir(dirpth)
    eplusdirs = [dir for dir in alldirs if dir.startswith('EnergyPlus')]
    maxapp = max(eplusdirs)
    splitapp = maxapp.split('-')
    ver = '.'.join(splitapp[1:])
    return ver
    
def test_cleanupversion():
    """py.test for cleanupversion"""
    data = (
        ('8.8.0', '8.8.0'), # ver, expected
        ('8.8.1', '8.8.0'), # ver, expected
        ('8.8', '8.8.0'), # ver, expected
        ('8', '8.0.0'), # ver, expected
        ('', '.0.0'), # ver, expected
    )    
    for ver, expected in data:
        result = easyopen.cleanupversion(ver)
        assert result == expected
    
@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set")
def test_easyopen():
    """py.test for easyopen"""
    ver = _latestidd()
    txt, result = ("  Version,{};".format(ver), '{}'.format(ver))
    fhandle = StringIO(txt)
    reload(modeleditor)
    reload(easyopen)
    idf = easyopen.easyopen(fhandle)
    versions = idf.idfobjects['version'.upper()]
    version = versions[0]
    ver = version.Version_Identifier
    assert result == ver
    