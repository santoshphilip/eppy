"""open a blank idf file in eppy and print it"""
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
IDF.setiddname(iddfile)

idftxt = "" # empty string
from io import StringIO
fhandle = StringIO(idftxt) # we can make a file handle of a string
new_idf = IDF(fhandle) # initialize the IDF object with the file handle

# add an object to the idf file
objtype = "BUILDING"
new_idf.newidfobject(objtype, Name="Taj Mahal")

buildings = new_idf.idfobjects["BUILDING"]
building = buildings[0]
# print building
new_idf.newidfobject("LIGHTS", Name="light one")

lights = new_idf.idfobjects["LIGHTS"]
light = lights[0]
print(light)

new_idf.printidf()
