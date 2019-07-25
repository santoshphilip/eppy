# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""
script to test idf reads in eppy.
Use to read test a single idf file
This may may be one of the files that failed when running eppyreadtest_folder.py
-
eppyreadtest_file.py will output two files:
1. simpleread.idf
2. eppyread.idf

The idf objects in both are sorted in ascending order. The files should be
identical. If there is a mismatch, eppy made a mistake in the read. Comparing
the two files will show you where the error occurred.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse

import sys

# pathnameto_eppy = 'c:/eppy'
pathnameto_eppy = "../../"
sys.path.append(pathnameto_eppy)

import os
from eppy.modeleditor import IDF
import eppy.simpleread as simpleread

# iddfile = '/Applications/EnergyPlus-8-1-0/Energy+.idd'
# folder = '/Applications/EnergyPlus-8-1-0/ExampleFiles'
# python eppyreadtest_file.py '/Applications/EnergyPlus-8-1-0/Energy+.idd'
# '/Applications/EnergyPlus-8-1-0/ExampleFiles/RetailPackagedTESCoil.idf'
# for non-failure -> SeriesActiveBranch.idf
# python eppyreadtest_file.py '/Applications/EnergyPlus-8-1-0/Energy+.idd'
# '/Applications/EnergyPlus-8-1-0/ExampleFiles/SeriesActiveBranch.idf'


def doreadtest(iddfile, folder, silent=False):
    """print out all the readtest results"""

    iddhandle = open(iddfile, "r")
    fname1 = thefile
    idfhandle1 = open(fname1, "rb")
    idfhandle2 = open(fname1, "rb")
    verbose = not silent
    result = simpleread.idfreadtest(
        iddhandle, idfhandle1, idfhandle2, verbose=verbose, save=False
    )
    # print result,   fname
    if result == False and (not silent):
        print("first mismatch at the above line numbers")
        print("full filepath of file that failed the read test ->")
        print("    %s" % (fname1,))
        print()
        print("compare files 'simpleread.idf' vs 'eppyread.idf'")
        print()
    else:
        print("file passed test")
    idfhandle1.close()
    idfhandle2.close()
    iddhandle.close()


if __name__ == "__main__":
    # do the argparse stuff
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument(
        "idd", action="store", help="location of idd file. ./somewhere/eplusv8-0-1.idd"
    )
    parser.add_argument(
        "thefile",
        action="store",
        help="location the idf file. ./somewhere/examples/thisfile.idf",
    )
    nspace = parser.parse_args()
    thefile = nspace.thefile
    iddfile = nspace.idd
    doreadtest(iddfile, thefile)
