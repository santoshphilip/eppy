"""core functions for E+"""


import idd_fields
from EPlusCode.EPlusInterfaceFunctions import mylib3
from EPlusCode.EPlusInterfaceFunctions import parse_idd

class NoSuchFieldError(Exception):
    pass
        

class Idd(object):
    """wrapper for oll idd data"""
    def __init__(self, commdct, commlst, theidd, block=None):
        super(Idd, self).__init__()
        self.commdct = commdct
        self.commlst = commlst
        self.theidd = theidd
        if block:
            self.block = block
            self.objlst_dct = parse_idd.getobjectref(block,commdct)

class IdfWrapper(object):
    """wraps the idf file and the idd data"""
    def __init__(self, idf, idd):
        super(IdfWrapper, self).__init__()
        self.idf = idf
        self.idd = idd
    def __repr__(self):
        #print dictionary
        dt=self.idf.dt
        dtls=self.idf.dtls
        commdct = self.idd.commdct
        dossep=mylib3.dossep
        st=''
        for ii, node in enumerate(dtls):
            nodedata=dt[node.upper()]
            for block in nodedata:
                for i in range(len(block)):
                    if i == 0:
                        thetab = ""
                        comm = ""
                        comment = ""
                    else:
                        thetab = "    "
                        comm = commdct[ii][i]['field'][0]
                        comment = "! %s" % (comm, )
                    if i == len(block) - 1:
                        endchar = ";"
                        sep = mylib3.dossep * 2
                    else:
                        endchar = ","
                        sep = mylib3.dossep
                    line = "%s%s%s" % (thetab, block[i], endchar)
                    line = line.ljust(30)
                    line = "%s%s%s" % (line, comment, sep)
                    st = st + line
        return st

def addfield2object(anobject, field, objname=""):
    """add a field to anobject"""
    try:
        if field['field'] == ['Name']:
            anobject.append(objname)
            return anobject
        anobject.append(field['default'][0])
    except KeyError, e:
        anobject.append('')
    return anobject

def makeanobject(data, theidd, commdct, objkey, objname=""):
    """make an object"""
    objs = data.dt[objkey]
    iobj = theidd.dtls.index(objkey)
    anobject = [objkey]
    # check for extensible objects
    field = commdct[iobj][0]
    ext = [key for key in field.keys() if key.startswith('extensible')]
    try:
        ext = ext[0]
        ext = ext.split(":")
        ext = int(ext[1])
        for i, field in enumerate(commdct[iobj]):
            if "begin-extensible" in field.keys():
                beginext = i
    except IndexError, e:
        ext = False
    if not ext:
        for field in commdct[iobj][1:]:
            anobject = addfield2object(anobject, field, objname)
    else:
        for field in commdct[iobj][1:beginext]:
            anobject = addfield2object(anobject, field, objname)
        for field in commdct[iobj][beginext:beginext + ext]:
            anobject = addfield2object(anobject, field, objname)
    return anobject

def getobjfieldnames(data, commdct, objkey):
    """get a list of fieldnames given objket"""
    objindex = data.dtls.index(objkey)
    objcomm = commdct[objindex]
    objfields = []
    # get the field names of that object
    for dct in objcomm:
        try:
            thefieldcomms = dct['field']
            objfields.append(thefieldcomms[0])
        except KeyError, e:
            objfields.append(None)
    return objfields

def getfieldindex(data, commdct, objkey, fielddescription):
    """get the index of the field in the object"""
    fields = getobjfieldnames(data, commdct, objkey)
    try:
        return fields.index(fielddescription)
    except ValueError, e:
        raise NoSuchFieldError, e
    
def getextensiblesize(data, commdct, objkey):
    """get the size of the extensible field in the object"""
    objindex = data.dtls.index(objkey)
    comment1 = commdct[objindex][0]
    keys = comment1.keys()
    extensions = [k for k in keys if k.startswith('extensible:')]
    try:
        extension = extensions[0]
    except IndexError, e:
        return None
    size = extension.split(':')[-1]
    return int(size)
        
    
def getextensibleposition(data, commdct, objkey):
    """get the index positon of the extensible field"""
    iobj = data.dtls.index(objkey)
    for i, field in enumerate(commdct[iobj]):
        if "begin-extensible" in field.keys():
            return i
    return None

def getobject(data, commdct, objkey, objname):
    """get the object matching objkey and objname"""
    theobjects = data.dt[objkey]
    namefield = idd_fields.ObjectName.name
    for theobject in theobjects:
        indx = getfieldindex(data, commdct, objkey, namefield)
        if theobject[indx] == objname:
            return theobject
    return None

def getobjlistOfField(idfw, objkey, objid, fieldid):
    """if the field is 'object-list', get the list of objects"""
    ikey = idfw.idf.dtls.index(objkey)
    try:
        object_list = idfw.idd.commdct[ikey][fieldid]['object-list'][0]
    except KeyError, e:
        return []
    objlst_dct = idfw.idd.objlst_dct
    dt = idfw.idf.dt
    objlist = []
    for obj, index in objlst_dct[object_list]:
        alist = [n[index] for n in dt[obj.upper()]]
        objlist = objlist + alist
    return objlist 

def getchoiceOFField(idfw, objkey, objid, fieldid):
    """if the filed is 'choice', get the key values in the choice"""
    ikey = idfw.idf.dtls.index(objkey)
    try:
        return idfw.idd.commdct[ikey][fieldid]['key']
    except KeyError, e:
        return []

def getreferences(idfw, key, fieldid):
    """get the references for this field. reference is defined in idd"""
    data = idfw.idf
    commdct = idfw.idd.commdct
    ikey = data.dtls.index(key)
    name = commdct[ikey][fieldid]['field'][0]
    if name == 'Name':
        try:
            refs = commdct[ikey][fieldid]['reference']
        except KeyError, e:
            refs = []
    else:
        refs = []
    return refs

def getReferenceObjectList(idfw, refs):
    """get the object-list of the references.
    object-list and reference definded in idd
    returns a list of tuples.
    tuple is (objkey, fieldid). fieldid is the filed that is refering to the ref."""
    data = idfw.idf
    commdct = idfw.idd.commdct
    keys = [key  for key in data.dt.keys() if len(data.dt[key]) > 0]
    ikeys = [(data.dtls.index(key), key) for key in keys]
    reflist = []
    for ref in refs:
        for i, key in ikeys:
            for j, comms in enumerate(commdct[i]):
                try:
                    if ref == comms['object-list'][0]:
                        reflist.append((key, j))
                except KeyError, e:
                    continue
    return reflist                

def newname2references_inner(idfw, reflist, oldname, newname):
    """put the new names to all fields that refer to it."""
    data = idfw.idf
    if not reflist:
        return None
    for key, fieldid in reflist:
        for obj in data.dt[key]:
            print obj
            if obj[fieldid] == oldname:
                obj[fieldid] = newname

def newname2references(idfw, key, fieldid, oldname, newname):
    """docstring for newname2references"""
    refs = getreferences(idfw, key, fieldid)
    reflist = getReferenceObjectList(idfw, refs)
    newname2references_inner(idfw, reflist, oldname, newname)
    
def rename_name(idfw, objkey, oldname, newname, fieldid=1):
    """change the (objkey, oldname) to newname and all it's references"""
    refs = getreferences(idfw, objkey, fieldid)
    reflist = getReferenceObjectList(idfw, refs)
    newname2references(idfw, objkey, fieldid, oldname, newname)
    # change the object's name. 
    objs = idfw.idf.dt[objkey]
    for obj in objs:
        if obj[fieldid] == oldname:
            obj[fieldid] = newname

def createobject(idfw, objkey, objname=None):
    """create an empty object. 
    if objname=None, no name is given. (some objects do not have names)"""
    objkey = objkey.upper()
    data = idfw.idf
    commdct = idfw.idd.commdct
    index = data.dtls.index(objkey)
    comm = commdct[index]
    lst = ["", ] * len(comm)
    lst[0] = objkey
    if objname:
        lst[1] = objname
    data.dt[objkey].append(lst)
    
def fieldvalue(idfw, objkey, objname, field, value):
    """insert the value into field.
    for objects that have only one object, objname=None"""
    # this is not very robust. There are many objects without name. 
    # it uses the first field
    objkey = objkey.upper()
    data = idfw.idf
    commdct = idfw.idd.commdct
    index = getfieldindex(data, commdct, objkey, field)
    objs = data.dt[objkey]
    if objname:
        objs = [obj for obj in objs if obj[1].upper() == objname.upper()]
        obj = objs[0]
    else:
        obj = objs[0] 
    obj[index] = value
