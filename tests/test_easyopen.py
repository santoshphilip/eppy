# Copyright (c) 2018 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for easyopen"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import pytest

import eppy
from eppy import modeleditor
import eppy.easyopen as easyopen
from eppy.pytest_helpers import do_integration_tests
import eppy.idd_helpers as idd_helpers


from six import StringIO
from importlib import reload


def test_cleanupversion():
    """py.test for cleanupversion"""
    data = (
        ("8.8.0", "8.8.0"),  # ver, expected
        ("8.8.1", "8.8.0"),  # ver, expected
        ("8.8", "8.8.0"),  # ver, expected
        ("8", "8.0.0"),  # ver, expected
        ("", ".0.0"),  # ver, expected
    )
    for ver, expected in data:
        result = easyopen.cleanupversion(ver)
        assert result == expected


@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set"
)
def test_easyopen_idfopen():
    """py.test for easyopen"""
    ver = idd_helpers.latestidd()
    txt, result = ("  Version,{};".format(ver), "{}".format(ver))
    fhandle1 = StringIO(txt)
    fhandle2 = StringIO(txt)
    reload(eppy)
    reload(modeleditor)
    reload(easyopen)
    idf1, idf2 = easyopen.easyopen(fhandle1), eppy.openidf(fhandle2)
    for idf in [idf1, idf2]:
        versions = idf.idfobjects["version"]
        version = versions[0]
        ver = version.Version_Identifier
        assert result == ver
    # test with epw=weatherfile
    fhandle1 = StringIO(txt)
    fhandle2 = StringIO(txt)
    epwname = "weatherfile.epw"
    idf1, idf2 = (
        easyopen.easyopen(fhandle1, epw=epwname),
        eppy.openidf(fhandle2, epw=epwname),
    )
    for idf in [idf1, idf2]:
        assert idf.epw == epwname


@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set"
)
def test_easyopen_withidd():
    """py.test for easyopen"""
    ver = idd_helpers.latestidd()
    iddfile = easyopen.getiddfile(ver)
    txt, result = ("  Version,{};".format(ver), "{}".format(ver))
    fhandle1 = StringIO(txt)
    fhandle2 = StringIO(txt)
    reload(eppy)
    reload(modeleditor)
    reload(easyopen)
    idf1, idf2 = (
        easyopen.easyopen(fhandle1, idd=iddfile),
        eppy.openidf(fhandle2, idd=iddfile),
    )
    for idf in [idf1, idf2]:
        versions = idf.idfobjects["version"]
        version = versions[0]
        ver = version.Version_Identifier
        assert result == ver
    # test with epw=weatherfile
    fhandle1 = StringIO(txt)
    fhandle2 = StringIO(txt)
    epwname = "weatherfile.epw"
    idf1, idf2 = (
        easyopen.easyopen(fhandle1, idd=iddfile, epw=epwname),
        eppy.openidf(fhandle2, idd=iddfile, epw=epwname),
    )
    for idf in [idf1, idf2]:
        assert idf.epw == epwname
