# Copyright (c) 2012 Santosh Philip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Eppy.  If not, see <http://www.gnu.org/licenses/>.
"""I print the current version of eppy. Being polite, I also say hello !"""

import argparse
import sys


pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)

import eppy

if __name__    == '__main__':
    # do the argparse stuff
    parser = argparse.ArgumentParser(usage=None, description=__doc__)
    nspace = parser.parse_args()
    version = eppy.__version__
    print("Hello! I am  eppy version %s" % (version, ))