# Copyright (c) 2012 Santosh Phillip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

"""get data for autosized fields
see comments at bottom of page for usage
"""
from EPlusInterfaceFunctions import readidf
from BeautifulSoup import BeautifulSoup
import table


def getautosized(theobj, data, commdct):
    """get all the sutosized field named for the object"""
    theobj_i = data.dtls.index(theobj)
    pl = data.dtls[theobj_i]
    objfields = []
    for obj in data.dt[pl]:
        objname = obj[1]
        iautosize = [i for i, field in enumerate(obj) if field.lower() == 'autosize']
        fieldnames = [commdct[theobj_i][i]['field'][0] for i in iautosize]
        fieldnames = []
        for i in iautosize:
            fieldtitle = commdct[theobj_i][i]['field'][0]
            try:
                #add the unit to the end of the field title - if it exists
                fieldtitle = '%s [%s]' % (fieldtitle, commdct[theobj_i][i]['units'][0], )
            except KeyError, e:
                pass
            fieldnames.append(fieldtitle)
        objfields.append((objname, fieldnames))
    objfields = [obj for obj in objfields if obj[1] != []]
    return objfields

def getautosizeds(data, commdct):
    """get all the autosized"""
    autosizeds = []
    for theobj in data.dtls:
        autosizeds.append((theobj, getautosized(theobj, data,  commdct)))
    autosizeds = [auto for auto in autosizeds if auto[1] != []]
    return autosizeds


def getautosizeddcts(idfname, tablename, commdct):
    """get values of autosized as a dictionary"""
    data = readidf.readidf(idfname)
    keys = []
    autosizeds = getautosizeds(data, commdct)
    for obj, autos in autosizeds:
        for vert, horiz in autos:
            for header in horiz:
                akey = [unicode(obj.upper()), unicode(vert.upper()), unicode(header.upper())]
                # all keys are caps in above line
                keys.append(tuple(akey))

    txt = open(tablename, 'r').read()
    soup = BeautifulSoup(txt)
    head, body = table.getheadbody(soup)

    btabledct = table.gettitletabledct(body)
    flatbtable = table.flattenkey(btabledct)
    nflatbtable = flatbtable
    autos = {}
    for key in keys:
        try:
            # pass
            autos[key] = nflatbtable[key]
        except KeyError, e:
            pass
    return autos
    
# usage below

# fname = "5ZoneDD.idf"
# data, commdct = readidf.readdatacommdct(fname)
# 
# autosizeds = getautosizeds(data, commdct)
# 
# print autosizeds
