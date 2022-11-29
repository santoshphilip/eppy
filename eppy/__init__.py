# Copyright (c) 2019 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# -*- coding: utf-8 -*-

"""Top-level package for eppy."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = """Santosh Philip"""
__email__ = "santosh@noemail.com"
__version__ = "0.5.61"


from io import StringIO
import eppy


def newidf(version=None):
    """open a new idf file

    easy way to open a new idf file for particular version. Works only id Energyplus of that version is installed.

    Parameters
    ----------
    version: string
        version of the new file you want to create. Will work only if this version of Energyplus has been installed.

    Returns
    -------
    idf
       file of type eppy.modelmake.IDF
    """  # noqa: E501
    if not version:
        version = "8.9"
    import eppy.easyopen as easyopen

    idfstring = "  Version,{};".format(str(version))
    fhandle = StringIO(idfstring)
    return easyopen.easyopen(fhandle)


def openidf(fname, idd=None, epw=None):
    """automatically set idd and open idf file. Uses version from idf to set correct idd
    It will work under the following circumstances:

    - the IDF file should have the VERSION object.
    - Needs  the version of EnergyPlus installed that matches the IDF version.
    - Energyplus should be installed in the default location.

    Parameters
    ----------
    fname : str, StringIO or IOBase
        Filepath IDF file,
        File handle of IDF file open to read
        StringIO with IDF contents within
    idd : str, StringIO or IOBase
        This is an optional argument. easyopen will find the IDD without this arg
        Filepath IDD file,
        File handle of IDD file open to read
        StringIO with IDD contents within
    epw : str
        path name to the weather file. This arg is needed to run EneryPlus from eppy.
    """
    import eppy.easyopen as easyopen

    return easyopen.easyopen(fname, idd=idd, epw=epw)
