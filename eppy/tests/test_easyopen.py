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

def latestidd():
    """extract the latest idd installed"""
    pth, _ = run_functions.install_paths(version='8.8.0') # works with any value in version
    dirpth = os.path.dirname(pth)
    dirpth = os.path.dirname(dirpth)
    alldirs = os.listdir(dirpth)
    eplusdirs = [dir for dir in alldirs if dir.startswith('EnergyPlus')]
    maxapp = max(eplusdirs)
    ver = folder2ver(maxapp)
    return ver
    
def folder2ver(folder):
    """get the version number from the E+ install folder"""
    ver = folder.split('EnergyPlus')[-1]
    ver = ver[1:]
    splitapp = ver.split('-')
    ver = '.'.join(splitapp)
    return ver
    
def test_folder2ver():
    """py.test for folder2ver"""
    data = (
    ('EnergyPlus-8-8-0', '8.8.0'), # folder, expected
    ('EnergyPlusV8-8-0', '8.8.0'), # folder, expected
    )   
    for folder, expected in data:
        result = folder2ver(folder) 
        assert result == expected
    
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
    ver = latestidd()
    txt, result = ("  Version,{};".format(ver), '{}'.format(ver))
    fhandle = StringIO(txt)
    reload(modeleditor)
    reload(easyopen)
    idf = easyopen.easyopen(fhandle)
    versions = idf.idfobjects['version'.upper()]
    version = versions[0]
    ver = version.Version_Identifier
    assert result == ver
    # test with epw=weatherfile
    fhandle = StringIO(txt)
    epwname = 'weatherfile.epw'
    idf = easyopen.easyopen(fhandle, epw=epwname)
    assert idf.epw == epwname

@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set")
def test_easyopen_withidd():
    """py.test for easyopen"""
    ver = latestidd()
    iddfile = easyopen.getiddfile(ver)
    txt, result = ("  Version,{};".format(ver), '{}'.format(ver))
    fhandle = StringIO(txt)
    reload(modeleditor)
    reload(easyopen)
    idf = easyopen.easyopen(fhandle, idd=iddfile)
    versions = idf.idfobjects['version'.upper()]
    version = versions[0]
    ver = version.Version_Identifier
    assert result == ver
    # test with epw=weatherfile
    fhandle = StringIO(txt)
    epwname = 'weatherfile.epw'
    idf = easyopen.easyopen(fhandle, idd=iddfile, epw=epwname)
    assert idf.epw == epwname
    