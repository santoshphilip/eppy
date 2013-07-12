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


def idfdiffs_simple(idf1, idf2):
    """return the diffs between the two idfs
    is not aware of objects in onde idf not present in the other"""
    keys = idf1.model.dtls # undocumented variable

    for akey in keys:
        idfobjs1 = idf1.idfobjects[akey]
        idfobjs2 = idf2.idfobjects[akey]
        for idfobj1, idfobj2 in zip(idfobjs1, idfobjs2):
            for i, (f1, f2) in enumerate(zip(idfobj1.obj, idfobj2.obj)): # undocumented
                if f1 != f2:
                    print '%s, %s, %s, %s' % (akey, 
                        idfobj1.objidd[i]['field'][0], # uncodumented var
                        f1, f2, )


def idfdiffs(idf1, idf2):
    """return the diffs between the two idfs
    is not aware of objects in onde idf not present in the other"""
    keys = idf1.model.dtls # undocumented variable

    for akey in keys:
        idfobjs1 = idf1.idfobjects[akey]
        idfobjs2 = idf2.idfobjects[akey]
        # for idfobj1, idfobj2 in zip(idfobjs1, idfobjs2):
        #     for i, (f1, f2) in enumerate(zip(idfobj1.obj, idfobj2.obj)): # undocumented
        #         if f1 != f2:
        #             print '%s, %s, %s, %s' % (akey, 
        #                 idfobj1.objidd[i]['field'][0], # uncodumented var
        #                 f1, f2, )
        if len(idfobjs1) != len(idfobjs2):
            if len(idfobjs1) > len(idfobjs2):
                pass
            else:
                for item in idfobjs2[-(len(idfobjs2) - len(idfobjs1)):]:
                    print item.Name
                
                
