# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""functions to use json to modify an idf file"""






def key2elements(key):
    """split key to elements"""
    return key.split('.')
    
def updateidf(idf, dct):
    """update idf using dct"""
    for key in list(dct.keys()):
        if key.startswith('idf.'):
            idftag, objkey, objname, field = key2elements(key)
            if objname == '':
                try:
                    idfobj = idf.idfobjects[objkey.upper()][0]
                except IndexError as e:
                    idfobj = idf.newidfobject(objkey.upper())
            else:
                idfobj = idf.getobject(objkey.upper(), objname)
                if idfobj == None:
                    idfobj = idf.newidfobject(objkey.upper(), Name=objname)
            idfobj[field] = dct[key]