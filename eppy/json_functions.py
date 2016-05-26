"""functions to use json to modify an idf file"""


def key2elements(key):
    """split key to elements"""
    return key.split('.')
    
def updateidf(idf, dct):
    """update idf using dct"""
    for key in dct.keys():
        if key.startswith('idf.'):
            idftag, objkey, objname, field = key2elements(key)
            if objname == '':
                idfobj = idf.idfobjects[objkey.upper()][0]
            else:
                idfobj = idf.getobject(objkey.upper(), objname)
            idfobj[field] = dct[key]