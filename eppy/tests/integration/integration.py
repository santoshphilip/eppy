# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""integration tests for eppy"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
pathnameto_eppy = './'
sys.path.append(pathnameto_eppy)

from eppy import modeleditor
from eppy.modeleditor import IDF

def getversion(idf):
    """return the version number"""
    versions = idf.idfobjects['VERSION']
    return versions[0].Version_Identifier
    
def setversion(idf, newversion):
    """set the version number"""
    versions = idf.idfobjects['VERSION']
    versions[0].Version_Identifier = newversion

def test_modeleditor():
    """test reading a idf file"""
    # TODO : organize this differently .. as multiple tests
    # TODO : add cleanup code
    iddfile = "./eppy/resources/iddfiles/Energy+V7_2_0.idd"
    startfolder = "./eppy/tests/integration/data2test"
    origfile = "%s/%s" % (startfolder, "origfile.idf")

    # make a copy of test file
    startfile = "%s/%s" % (startfolder, "startfile.idf")
    import shutil
    shutil.copy(origfile, startfile)
    
    # pytest open the file
    # check the version number
    IDF.setiddname(iddfile)
    idf = IDF(startfile)
    result = getversion(idf)
    assert result == '7.3'

    # pytest save
    # change version number and save
    # open again and check version number
    idf = IDF(startfile)
    setversion(idf, '7.4')
    idf.save()
    idf2 = IDF(startfile)
    result = getversion(idf2)
    assert result == '7.4'


    # pytest saveas
    # saveas changes the filename. The next save should save with new name
    saveasfile = "%s/%s" %  (startfolder, "saveas.idf")
    idf = IDF(startfile)
    idf.saveas(saveasfile)
    setversion(idf, '7.4')
    idf.save()
    idf2 = IDF(saveasfile)
    result = getversion(idf2)
    assert result == '7.4'

    # pytest savecopy
    # test that it saves a copy. If a following save is done, the copy is unchanged
    copyfile = "%s/%s" %  (startfolder, "savecopy.idf")
    idf = IDF(startfile)
    idf.savecopy(copyfile)
    setversion(idf, '7.5')
    idf.save()
    idf2 = IDF(copyfile)
    result = getversion(idf2)
    assert result == '7.4'
    idf3 = IDF(startfile)
    result = getversion(idf3)
    assert result == '7.5'
    
    # test lineendings 
    idf = IDF(startfile)
    idf.save(lineendings='windows')
    txt = open(startfile, 'r').read()
    print(txt.count('\r\n'))
    lines = txt.splitlines()
    numlines = len(lines)
    assert numlines == txt.count('\r\n') + 1 # no CR on last line
    idf.save(lineendings='unix')
    txt = open(origfile, 'r').read()
    lines = txt.splitlines()
    numlines = len(lines)
    assert numlines == txt.count('\n') + 1 # no CR on last line
    
    
    
