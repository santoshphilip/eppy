# Copyright (c) 2018 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================


"""home of easyopen - to easily open an idf file"""

# ideally this should be in idf_helper
# pytest kept failing since the other routines set the IDD file
# pytest works here in a seperate file, like eppy/runner.py

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
from io import IOBase
from io import StringIO
import eppy
import eppy.modeleditor
import eppy.EPlusInterfaceFunctions.parse_idd
import eppy.runner.run_functions


class MissingIDDException(Exception):
    pass


def cleanupversion(ver):
    """massage the version number so it matches the format of install folder"""
    lst = ver.split(".")
    if len(lst) == 1:
        lst.extend(["0", "0"])
    elif len(lst) == 2:
        lst.extend(["0"])
    elif len(lst) > 2:
        lst = lst[:3]
    lst[2] = "0"  # ensure the 3rd number is 0
    cleanver = ".".join(lst)
    return cleanver


def getiddfile(versionid):
    """find the IDD file of the E+ installation"""
    vlist = versionid.split(".")
    if len(vlist) == 1:
        vlist = vlist + ["0", "0"]
    elif len(vlist) == 2:
        vlist = vlist + ["0"]
    ver_str = "-".join(vlist)
    eplus_exe, _ = eppy.runner.run_functions.install_paths(ver_str)
    eplusfolder = os.path.dirname(eplus_exe)
    iddfile = "{}/Energy+.idd".format(eplusfolder)
    return iddfile


def getoldiddfile(versionid):
    """find the IDD file of the E+ installation
    E+ version 7 and earlier have the idd in /EnergyPlus-7-2-0/bin/Energy+.idd"""
    vlist = versionid.split(".")
    if len(vlist) == 1:
        vlist = vlist + ["0", "0"]
    elif len(vlist) == 2:
        vlist = vlist + ["0"]
    ver_str = "-".join(vlist)
    eplus_exe, _ = eppy.runner.run_functions.install_paths(ver_str)
    eplusfolder = os.path.dirname(eplus_exe)
    iddfile = "{}/bin/Energy+.idd".format(eplusfolder)
    return iddfile


def easyopen(fname, idd=None, epw=None):
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
    if idd:
        eppy.modeleditor.IDF.setiddname(idd)
        idf = eppy.modeleditor.IDF(fname, epw=epw)
        return idf
    # the rest of the code runs if idd=None
    if isinstance(fname, (IOBase, StringIO)):
        fhandle = fname
    else:
        fhandle = io.open(
            fname, "r", encoding="latin-1"
        )  # latin-1 seems to read most things

    # - get the version number from the idf file
    txt = fhandle.read()
    # try:
    #     txt = txt.decode('latin-1') # latin-1 seems to read most things
    # except AttributeError:
    #     pass
    ntxt = eppy.EPlusInterfaceFunctions.parse_idd.nocomment(txt, "!")
    blocks = ntxt.split(";")
    blocks = [block.strip() for block in blocks]
    bblocks = [block.split(",") for block in blocks]
    bblocks1 = [[item.strip() for item in block] for block in bblocks]
    ver_blocks = [block for block in bblocks1 if block[0].upper() == "VERSION"]
    ver_block = ver_blocks[0]
    versionid = ver_block[1]

    # - get the E+ folder based on version number
    iddfile = getiddfile(versionid)
    if os.path.exists(iddfile):
        pass
        # might be an old version of E+
    else:
        iddfile = getoldiddfile(versionid)
    if os.path.exists(iddfile):
        # if True:
        # - set IDD and open IDF.
        eppy.modeleditor.IDF.setiddname(iddfile)
        if isinstance(fname, (IOBase, StringIO)):
            fhandle.seek(0)
            idf = eppy.modeleditor.IDF(fhandle, epw=epw)
        else:
            idf = eppy.modeleditor.IDF(fname, epw=epw)
        return idf

    else:

        # - can't find IDD -> throw an exception
        astr = "input idf file says E+ version {}. easyopen() cannot find the corresponding idd file '{}'"
        astr = astr.format(versionid, iddfile)
        raise MissingIDDException(astr)
