# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""sample script - autosize all autosizable fields"""
# email to jason
# Jason,
#   Try out the attached script.
# (you might have to change file pathnames)
#
# I don't think you could have written it on your own :-(
# It became apparent to me that eppy needs functions that allows it to look
# into the idd structure for any object and field
# I'll put some thought into this and see how best to write this.
# If that functionality is done well, hopefully anyone should be able to write
# the equivalent code to what I wrote in the attached file.
#
#
# Santosh
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)

from eppy import modeleditor
from eppy.modeleditor import IDF
from eppy import bunch_subclass


def autosize_fieldname(idfobject):
    """return autsizeable field names in idfobject"""
    # undocumented stuff in this code
    return [
        fname
        for (fname, dct) in zip(idfobject.objls, idfobject["objidd"])
        if "autosizable" in dct
    ]


def main():
    iddfile = "../resources/iddfiles/Energy+V8_0_0.idd"
    fname1 = "../resources/idffiles/V8_0_0/5ZoneWaterLoopHeatPump.idf"

    IDF.setiddname(iddfile)
    idf = IDF(fname1)
    idf.saveas("./a.idf")

    allidfobjects = idf.idfobjects
    for objname in list(allidfobjects.keys()):
        idfobjects = allidfobjects[objname]
        for idfobject in idfobjects:
            autofields = autosize_fieldname(idfobject)
            for autofield in autofields:
                idfobject[autofield] = "autosize"

    idf.saveas("./b.idf")


if __name__ == "__main__":
    main()
