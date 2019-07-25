# Copyright (c) 2019 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""helper functions for idd"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import eppy.runner.run_functions as run_functions


def latestidd():
    """extract the latest idd installed"""
    pth, _ = run_functions.install_paths(
        version="8.8.0"
    )  # works with any value in version
    dirpth = os.path.dirname(pth)
    dirpth = os.path.dirname(dirpth)
    alldirs = os.listdir(dirpth)
    eplusdirs = [dir for dir in alldirs if dir.startswith("EnergyPlus")]
    maxapp = max(eplusdirs)
    ver = folder2ver(maxapp)
    return ver


def folder2ver(folder):
    """get the version number from the E+ install folder"""
    ver = folder.split("EnergyPlus")[-1]
    ver = ver[1:]
    splitapp = ver.split("-")
    ver = ".".join(splitapp)
    return ver
