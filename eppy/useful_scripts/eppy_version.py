# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

# along with Eppy.  If not, see <http://www.gnu.org/licenses/>.
"""I print the current version of eppy. Being polite, I also say hello !"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys


pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)

import eppy

if __name__ == "__main__":
    # do the argparse stuff
    parser = argparse.ArgumentParser(usage=None, description=__doc__)
    nspace = parser.parse_args()
    version = eppy.__version__
    print("Hello! I am  eppy version %s" % (version,))
