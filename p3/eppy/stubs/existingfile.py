"""open an existing idf file in eppy"""
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

# you would normaly install eppy by doing
# python setup.py install
# or
# pip install eppy
# or
# easy_install eppy






# if you have not done so, uncomment the following three lines
import sys
# pathnameto_eppy = 'c:/eppy'
pathnameto_eppy = '../../'
sys.path.append(pathnameto_eppy)

from eppy import modeleditor
from eppy.modeleditor import IDF
iddfile = "../resources/iddfiles/Energy+V7_2_0.idd"
fname1 = "../resources/idffiles/V_7_2/smallfile.idf"

IDF.setiddname(iddfile)
idf1 = IDF(fname1)
idf1.printidf()
