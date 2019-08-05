# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""script to test idf reads. Use this to test all the files
in the example folder when a new version is released"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse

import os
import sys
import eppy.simpleread as simpleread

# pathnameto_eppy = 'c:/eppy'
pathnameto_eppy = "../../"
sys.path.append(pathnameto_eppy)

from eppy.modeleditor import IDF

# iddfile = '/Applications/EnergyPlus-8-1-0/Energy+.idd'
# folder = '/Applications/EnergyPlus-8-1-0/ExampleFiles'
# python eppyreadtest_folder.py '/Applications/EnergyPlus-8-1-0/Energy+.idd'
# '/Applications/EnergyPlus-8-1-0/ExampleFiles'


def doreadtest(iddfile, folder, silent=False):
    """print out all the readtest results"""
    lst = os.listdir(folder)
    lst = [l for l in lst if l.endswith(".idf")]
    iddhandle = open(iddfile, "r")
    for i, fname in enumerate(lst[355:359]):  # lst[6:7]
        # if you want to test a specific file
        fname1 = "%s/%s" % (folder, fname)
        idfhandle1 = open(fname1, "rb")
        idfhandle2 = open(fname1, "rb")
        verbose = not silent
        result = simpleread.idfreadtest(
            iddhandle, idfhandle1, idfhandle2, verbose=verbose, save=False
        )
        print(i, result, fname)
        if result == False and (not silent):
            print("full filepath of file that failed the read test ->")
            print("    %s" % (fname1,))
            print()
        idfhandle1.close()
        idfhandle2.close()
    iddhandle.close()


if __name__ == "__main__":
    # do the argparse stuff
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "idd", action="store", help="location of idd file. ./somewhere/eplusv8-0-1.idd"
    )
    parser.add_argument(
        "folder",
        action="store",
        help="location of folder with idf files. ./somewhere/examples",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        default=False,
        help="don't print the first mismatching line",
    )
    nspace = parser.parse_args()
    folder = nspace.folder
    iddfile = nspace.idd
    silent = nspace.silent
    doreadtest(iddfile, folder, silent)
