import glob
import os

from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from eppy.pytest_helpers import IDD_FILES
from io import StringIO

import eppy.snippet as snippet


iddsnippet = iddcurrent.iddtxt
idfsnippet = snippet.idfsnippet

iddfhandle = StringIO(iddcurrent.iddtxt)
IDF.setiddname(iddfhandle)

idd = os.path.join(IDD_FILES, "Energy+V8_1_0.idd")
OUTPUT_DIR = "C:\EnergyPlusV8-5-0\ExampleFiles\loopdiagrams"

idfs = glob.glob(OUTPUT_DIR + "\*.idf")
dots = glob.glob(OUTPUT_DIR + "\*.dot")
for idf in idfs:
    os.remove(idf)
for dot in dots:
    os.remove(dot)
