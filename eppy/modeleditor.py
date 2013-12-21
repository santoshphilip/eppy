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
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

"""functions to edit the E+ model"""

from idfreader import makebunches
from idfreader import idfreader, idfreader1
from idfreader import makeabunch
import function_helpers
import copy

class NoObjectError(Exception):
    pass

class NotSameObjectError(Exception):
    pass

class IDDNotSetError(Exception):
    pass

class IDDAlreadySetError(Exception):
    pass

def almostequal(first, second, places=7, printit=True):
    # taken from python's unit test
    # may be covered by Python's license 
    """docstring for almostequal"""
    if round(abs(second-first), places) != 0:
        if printit:
            print round(abs(second-first), places)
            print "notalmost: %s != %s" % (first, second)
        return False
    else:
        return True
        
def poptrailing(lst):
    """pop the trailing items in lst that are blank"""
    for i in range(len(lst)):
        if lst[-1] != '':
            break
        lst.pop(-1)
    return lst
    
def extendlist(lst, i, value=''):
    """extend the list so that you have i-th value"""
    if i < len(lst):
        pass
    else:
        lst.extend([value, ] * (i - len(lst) + 1))

    

def newrawobject(data, commdct, key):
    """make a new object for key"""
    dt = data.dt
    dtls = data.dtls
    key = key.upper()

    key_i = dtls.index(key)
    key_comm = commdct[key_i]
    #set default values
    obj = [comm.get('default', [''])[0] for comm in key_comm] 
    for i, comm in enumerate(key_comm):
        typ = comm.get('type', [''])[0]
        if typ in ('real', 'integer'):
            func_select = dict(real=float, integer=int)
            try:
                obj[i] = func_select[typ](obj[i])
            except IndexError, e:
                break
            except ValueError, e: # if value = autocalculate
                continue
    obj[0] = key
    obj = poptrailing(obj) # remove the blank items in a repeating field. 
    return obj
    
def addthisbunch(bunchdt, data, commdct, thisbunch):
    """add a bunch to model.
    abunch usually comes from another idf file
    or it can be used to copy within the idf file"""
    key = thisbunch.key.upper()
    obj = copy.copy(thisbunch.obj)
    data.dt[key].append(obj)
    abunch =  obj2bunch(data, commdct, obj)
    bunchdt[key].append(abunch)
    return abunch
    
def obj2bunch(data, commdct, obj):
    """make a new bunch object using the data object"""
    dt = data.dt
    dtls = data.dtls
    key = obj[0].upper()
    key_i = dtls.index(key)
    abunch = makeabunch(commdct, obj, key_i)
    return abunch
    
def namebunch(abunch, aname):
    """give the bunch object a name, if it has a Name field"""
    if abunch.Name == None:
        pass
    else:
        abunch.Name = aname
    return abunch
    
def renamebunch(bunchdt, commdct, oldname, newname):
    """rename this bunch and change name in all references"""
    pass
    
def addobject(bunchdt, data, commdct, key, aname=None, **kwargs):
    """add an object to the eplus model"""
    obj = newrawobject(data, commdct, key)
    abunch = obj2bunch(data, commdct, obj)
    if aname:
        namebunch(abunch, aname)
    data.dt[key].append(obj)
    bunchdt[key].append(abunch)
    for k, v in kwargs.items():
        abunch[k] = v
    return abunch

def getnamedargs(*args, **kwargs):
    """allows you to pass a dict and named args
    so you can pass ({'a':5, 'b':3}, c=8) and get
    dict(a=5, b=3, c=8)"""
    adict = {}
    for arg in args:
        if isinstance(arg, dict):
            adict.update(arg)
    adict.update(kwargs)
    return adict
    
def addobject1(bunchdt, data, commdct, key, **kwargs):
    """add an object to the eplus model"""
    obj = newrawobject(data, commdct, key)
    abunch = obj2bunch(data, commdct, obj)
    data.dt[key].append(obj)
    bunchdt[key].append(abunch)
    # adict = getnamedargs(*args, **kwargs)
    for kkey, value in kwargs.iteritems():
        abunch[kkey] = value
    return abunch
    
def getobject(bunchdt, key, name):
    """get the object if you have the key and the name
    retunrs a list of objects, in case you have more than one
    You should not have more than one"""
    # TODO : throw exception if more than one object, or return more objects
    idfobjects = bunchdt[key]
    theobjs = [idfobj for idfobj in idfobjects if idfobj.Name.upper() == name.upper()]
    try:
        return theobjs[0]
    except IndexError, e:
        return None

def __objecthasfields(bunchdt, data, commdct, idfobject, places=7, **kwargs):
    """test if the idf object has the field values in kwargs"""
    key = idfobject.obj[0].upper()
    for k, v in kwargs.items():
        if not isfieldvalue(bunchdt, data, commdct, 
                idfobject, k, v, places=places):
            return False
    return True
        
def getobjects(bunchdt, data, commdct, key, places=7, **kwargs):
    """get all the objects of key that matches the fields in **kwargs"""
    idfobjects = bunchdt[key]
    allobjs = []
    for obj in idfobjects:
        if __objecthasfields(bunchdt, data, commdct, 
                obj, places=places, **kwargs):
            allobjs.append(obj)
    return allobjs
    
def iddofobject(data, commdct, key):
    """from commdct, return the idd of the object key"""
    dtls = data.dtls
    i = dtls.index(key)
    return commdct[i]
    
def getextensibleindex(bunchdt, data, commdct, key, objname):
    """get the index of the first extensible item"""
    theobject = getobject(bunchdt, key, objname)
    if theobject == None:
        return None
    theidd = iddofobject(data, commdct, key)
    extensible_i = [i for i in range(len(theidd)) if theidd[i].has_key('begin-extensible')]
    try:
        extensible_i = extensible_i[0]
    except IndexError, e:
        return theobject
        

def removeextensibles(bunchdt, data, commdct, key, objname):
    """remove the extensible items in the object"""
    theobject = getobject(bunchdt, key, objname)
    if theobject == None:
        return theobject
    theidd = iddofobject(data, commdct, key)
    extensible_i = [i for i in range(len(theidd)) if theidd[i].has_key('begin-extensible')]
    try:
        extensible_i = extensible_i[0]
    except IndexError, e:
        return theobject
    while True:
        try:
            p = theobject.obj.pop(extensible_i)
        except IndexError, e:
            break
    return theobject

def getfieldcomm(bunchdt, data, commdct, idfobject, fieldname):
    """get the idd comment for the field"""
    key = idfobject.obj[0].upper()
    keyi = data.dtls.index(key)
    fieldi = idfobject.objls.index(fieldname)
    thiscommdct = commdct[keyi][fieldi]
    return thiscommdct
    
def is_retaincase(bunchdt, data, commdct, idfobject, fieldname):
    """test if case has to be retained for that field"""
    thiscommdct = getfieldcomm(bunchdt, data, commdct, idfobject, fieldname)
    return thiscommdct.has_key('retaincase')
    
def isfieldvalue(bunchdt, data, commdct, idfobj, fieldname, value, places=7):
    """test if idfobj.field == value"""
    # do a quick type check
    # if type(idfobj[fieldname]) != type(value):
    #     return False # takes care of autocalculate and real
    # check float
    thiscommdct = getfieldcomm(bunchdt, data, commdct, idfobj, fieldname)
    if thiscommdct.has_key('type'):
        if thiscommdct['type'][0] in ('real', 'integer'):
            # test for autocalculate
            try:
                if idfobj[fieldname].upper() == 'AUTOCALCULATE':
                    if value.upper() == 'AUTOCALCULATE':
                        return True
            except AttributeError, e:
                pass
            return almostequal(float(idfobj[fieldname]), float(value), places, False)    
    # check retaincase
    if is_retaincase(bunchdt, data, commdct, idfobj, fieldname):
        return idfobj[fieldname] == value
    else:
        return idfobj[fieldname].upper() == value.upper()
    

def equalfield(bunchdt, data, commdct, idfobj1, idfobj2, fieldname, places=7):
    """returns true if the two fields are equal
    will test for retaincase
    places is used if the field is float/real"""
    # TODO test if both objects are of same type
    key1 = idfobj1.obj[0].upper()
    key2 = idfobj2.obj[0].upper()
    if key1 != key2:
        raise NotSameObjectError
    v2 = idfobj2[fieldname]
    return isfieldvalue(bunchdt, data, commdct, 
        idfobj1, fieldname, v2, places=places)
    
def getrefnames(idf, objname):
    """get the reference names for this object"""
    iddinfo = idf.idd_info
    dtls = idf.model.dtls
    index = dtls.index(objname)
    fieldidds = iddinfo[index]
    for fieldidd in fieldidds:
        if fieldidd.has_key('field'):
            if fieldidd['field'][0].endswith('Name'):
                if fieldidd.has_key('reference'):
                    return fieldidd['reference']
                else:
                    return []

def getallobjlists(idf, refname):
    """get all object-list fields for refname
    return a list:
    [('OBJKEY', refname, fieldindexlist), ...] where
    fieldindexlist = index of the field where the object-list = refname
    """
    dtls = idf.model.dtls
    objlists = []
    for i, fieldidds in enumerate(idf.idd_info):
        indexlist = []
        for j, fieldidd in enumerate(fieldidds):
            if fieldidd.has_key('object-list'):
                if fieldidd['object-list'][0].upper() == refname.upper():
                    indexlist.append(j)
        if indexlist != []:
            objkey = dtls[i]
            objlists.append((objkey, refname, indexlist))
    return objlists

def rename(idf, objkey, objname, newname):
    """rename all the refrences to this objname"""
    refnames = getrefnames(idf, objkey)
    for refname in refnames:
        objlists = getallobjlists(idf, refname) 
        # [('OBJKEY', refname, fieldindexlist), ...]
        for refname in refnames:
            for robjkey, refname, fieldindexlist in objlists:
                idfobjects = idf.idfobjects[robjkey]
                for idfobject in idfobjects:
                    for findex in fieldindexlist: # for each field
                        if idfobject[idfobject.objls[findex]] == objname:
                            idfobject[idfobject.objls[findex]] = newname
    theobject = idf.getobject(objkey, objname)
    fieldname = [item for item in theobject.objls if item.endswith('Name')][0]
    theobject[fieldname] = newname
    return theobject

def zonearea(idf, zonename, debug=False):
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == 'FLOOR']
    if debug:
        print len(floors)
        print [floor.area for floor in floors]
    # area = sum([floor.area for floor in floors])
    if floors != []:
        area = zonearea_floor(idf, zonename)
    else:
        area = zonearea_roofceiling(idf, zonename)
    return area
    
def zonearea_floor(idf, zonename, debug=False):
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == 'FLOOR']
    if debug:
        print len(floors)
        print [floor.area for floor in floors]
    area = sum([floor.area for floor in floors])
    return area

def zonearea_roofceiling(idf, zonename, debug=False):
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() in ['ROOF', 
                                                            'CEILING']]
    if debug:
        print len(floors)
        print [floor.area for floor in floors]
    area = sum([floor.area for floor in floors])
    return area
    
def zone_height_min2max(idf, zonename, debug=False):
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    surf_xyzs = [function_helpers.getcoords(s) for s in zone_surfs]
    import itertools # to flatten the list
    surf_xyzs = list(itertools.chain(*surf_xyzs))
    surf_zs = [z for x, y, z in surf_xyzs]
    topz =  max(surf_zs)
    botz = min(surf_zs)
    height = topz - botz    
    return height
    
def zoneheight(idf, zonename, debug=False):
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == 'FLOOR']
    roofs = [s for s in zone_surfs if s.Surface_Type.upper() == 'ROOF']
    if floors == [] or roofs == []:
        height = zone_height_min2max(idf, zonename)    
    else:
        height = zone_floor2roofheight(idf, zonename)    
    return height
    
def zone_floor2roofheight(idf, zonename, debug=False):
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == 'FLOOR']
    roofs = [s for s in zone_surfs if s.Surface_Type.upper() == 'ROOF']
    ceilings = [s for s in zone_surfs if s.Surface_Type.upper() == 'CEILING']
    topsurfaces = roofs + ceilings

    topz = []
    for topsurface in topsurfaces:
        for coord in topsurface.coords:
            topz.append(coord[-1])
    topz = max(topz)
        
    botz = []
    for floor in floors:
        for coord in floor.coords:
            botz.append(coord[-1])
    botz = min(botz)
    height = topz - botz
    
    return height
    
    
    
def zonevolume(idf, zonename):
    area = zonearea(idf, zonename)
    height = zoneheight(idf, zonename)
    volume = area * height

    return volume


class IDF0(object):
    """
    document the following variables:
    
    - idfobjects
    - outputtype
    - iddname
    - idfname
    - idd_info
    - model
    
    
"""
    iddname = None
    idd_info = None
    block = None
    def __init__(self, idfname=None):
        if idfname != None:
            self.idfname = idfname
            self.read()
    @classmethod
    def setiddname(cls, arg, testing=False):
        if cls.iddname == None:
            cls.iddname = arg
            cls.idd_info = None
            cls.block = None
        else:
            if testing == False:
                errortxt = "IDD file is set to: %s"  % (cls.iddname, )
                raise IDDAlreadySetError(errortxt)
    @classmethod
    def getiddname(cls):
        return cls.iddname
    @classmethod
    def setidd(cls, iddinfo, block):
        cls.idd_info = iddinfo
        cls.block = block
    def read(self):
        """read the idf file"""
        # TODO unit test
        if self.getiddname() == None:
            errortxt = "IDD file needed to read the idf file. Set it using IDF.setiddname(iddfile)"
            raise IDDNotSetError(errortxt)
        readout = idfreader1(self.idfname, self.iddname,
                                commdct=self.idd_info, block=self.block)
        self.idfobjects, block, self.model, idd_info = readout
        self.__class__.setidd(idd_info, block)
    def save(self):
        # TODO unit test
        s = str(self.model)
        open(self.idfname, 'w').write(s)
    def saveas(self, filename):
        s = str(self.model)
        open(filename, 'w').write(s)

class IDF1(IDF0):
    """subclass of IDF0. Uses functions of IDF0 
    """
    def __init__(self, idfname=None):
        super(IDF1, self).__init__(idfname)
    def newidfobject(self, key, aname='', **kwargs):
    # def newidfobject(self, key, *args, **kwargs):
        """add a new idfobject to the model
        
        for example :: 
        
            newidfobject("CONSTRUCTION")
            newidfobject("CONSTRUCTION", 
                Name='Interior Ceiling_class', 
                Outside_Layer='LW Concrete', 
                Layer_2='soundmat')
        
        If you don't specify a value for a field, the default value will be set
        
        aname is not used. It is left there for backward compatibility"""
        # TODO unit test
        # return addobject1(self.idfobjects,
        #                     self.model,
        #                     self.idd_info,
        #                     key, **kwargs)  
        return addobject(self.idfobjects,
                            self.model,
                            self.idd_info,
                            key, aname=aname, **kwargs)
    def popidfobject(self, key, index):
        """pop this object"""
        popobject = self.idfobjects[key][index]
        self.removeidfobject(popobject)
    def removeidfobject(self, idfobject):
        """remove this idfobject"""
        # the object has to be removed from idfobjects and
        # form self.model.dt
        # since idfobjects is just a wrapper for model.dt
        key = idfobject.key
        theobjects = self.idfobjects[key.upper()]
        for i, theobject in enumerate(theobjects):
            if theobject is idfobject:
                theobjects.pop(i)
                # remove it from model too
                return self.model.dt[key.upper()].pop(i)
    def copyidfobject(self, idfobject):
        """add idfobject to this model
        
        idfobject usually comes from another idf file
        or it can be used to copy within this idf file"""
        # TODO unit test
        addthisbunch(self.idfobjects, 
                            self.model,
                            self.idd_info,
                            idfobject)
    def getobject(self, key, name):
        """return the object given key and name"""
        return getobject(self.idfobjects, key, name)
    def getextensibleindex(self, key, name):
        """get the index of the first extensible item
        
        only for internal use. # TODO : hide this"""
        return getextensibleindex(self.idfobjects, self.model, self.idd_info, 
                                key, name)
    def removeextensibles(self, key, name):
        """remove extensible items in the object of key and name
        
        only for internal use. # TODO : hide this"""
        return removeextensibles(self.idfobjects, self.model, self.idd_info, 
                                key, name)
      
class IDF2(IDF1):
    """subclass of IDF1. Uses functions of IDF1 
    
    """
    def __init__(self, idfname=None):
        super(IDF2, self).__init__(idfname)
        self.outputtype = "standard" # standard, 
                                    # nocomment, 
                                    # nocomment1,
                                    # nocomment2,
                                    # compressed
    def idfstr(self):
        if self.outputtype != 'standard':
            st = self.model.__repr__()
            if self.outputtype == 'nocomment':
                return st
            elif self.outputtype == 'nocomment1':
                slist = st.split('\n')
                slist = [item.strip() for item in slist]
                return '\n'.join(slist)
            elif self.outputtype == 'nocomment2':
                slist = st.split('\n')
                slist = [item.strip() for item in slist]
                slist = [item for item in slist if item != '']
                return '\n'.join(slist)
            elif self.outputtype == 'compressed':
                slist = st.split('\n')
                slist = [item.strip() for item in slist]
                return ' '.join(slist)
        # else:
        st = ''
        dtls = self.model.dtls
        for objname in dtls:
            for obj in self.idfobjects[objname]:
                 st = st + obj.__repr__()
        return st
    def printidf(self):
        """print the idf"""
        print self.idfstr()
    def save(self):
        """save with comments"""
        s = self.idfstr()
        open(self.idfname, 'w').write(s)
    def saveas(self, filename):
        s = self.idfstr()
        open(filename, 'w').write(s)
    # def initread(self, idfname):
    #     """use the latest iddfile and read file fname"""
    #     from StringIO import StringIO
    #     from eppy.iddcurrent import iddcurrent
    #     iddfhandle = StringIO(iddcurrent.iddtxt)
    #     if self.getiddname() == None:
    #         self.setiddname(iddfhandle)
    #     self.idfname = idfname
    #     self.read()

class IDF3(IDF2):
    """subclass of IDF2. Uses functions of IDF1 and IDF2
    """
    def __init__(self, idfname=None):
        super(IDF3, self).__init__(idfname)
    def initread(self, idfname):
        """use the latest iddfile and read file fname
        idd is initialized only if it has not been done earlier"""
        from StringIO import StringIO
        from eppy.iddcurrent import iddcurrent
        iddfhandle = StringIO(iddcurrent.iddtxt)
        if self.getiddname() == None:
            self.setiddname(iddfhandle)
        self.idfname = idfname
        self.read()
    def initnew(self):
        """use the latest iddfile and opens a new file
        idd is initialized only if it has not been done earlier"""
        from StringIO import StringIO
        from eppy.iddcurrent import iddcurrent
        iddfhandle = StringIO(iddcurrent.iddtxt)
        if self.getiddname() == None:
            self.setiddname(iddfhandle)
        idfhandle = StringIO('')
        self.idfname = idfhandle
        self.read()
    def initreadtxt(self, idftxt):
        """use the latest iddfile and read txt
        idd is initialized only if it has not been done earlier"""
        from StringIO import StringIO
        from eppy.iddcurrent import iddcurrent
        iddfhandle = StringIO(iddcurrent.iddtxt)
        if self.getiddname() == None:
            self.setiddname(iddfhandle)
        idfhandle = StringIO(idftxt)
        self.idfname = idfhandle
        self.read()
        

IDF = IDF3
        
                                    
class something(IDF0):
    """docstring for something"""
    def __init__(self, arg):
        super(something, self).__init__()
        self.arg = arg
        
