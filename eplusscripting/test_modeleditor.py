"""py.test for modeleditor"""

import bunch
import idfreader
import modeleditor
import snippet

iddsnippet = snippet.iddsnippet
idfsnippet = snippet.idfsnippet

from StringIO import StringIO
idffhandle = StringIO(idfsnippet)
iddfhandle = StringIO(iddsnippet)
bunchdt, data, commdct = idfreader.idfreader(idffhandle, iddfhandle)


def test_newrawobject():
    """py.test for newrawobject"""
    thedata = (('zone'.upper(), 
        ['ZONE', '', '0', '0', '0', '0', '1', '1', 'autocalculate', 
            'autocalculate', 'autocalculate', '', '', 'Yes']), # key, obj
    )
    for key, obj in thedata:
        result = modeleditor.newrawobject(data, commdct, key)
        assert result == obj
        
def test_obj2bunch():
    """py.test for obj2bunch"""
    thedata = ((['ZONE', '', '0', '0', '0', '0', '1', '1', 'autocalculate', 
        'autocalculate', 'autocalculate', '', '', 'Yes']), # obj
    )
    for obj in thedata:
        key_i = data.dtls.index(obj[0].upper())
        abunch = idfreader.makeabunch(commdct, obj, key_i)
        result = modeleditor.obj2bunch(data, commdct, obj)
        assert result == abunch
    
def test_namebunch():
    """py.test for namebunch"""
    thedata = ((bunch.Bunch(dict(Name="", a=5)), 
        "yay", "yay"), # abunch, aname, thename
        (bunch.Bunch(dict(Name=None, a=5)), 
            "yay", None), # abunch, aname, thename
    )
    for abunch, aname, thename in thedata:
        result = modeleditor.namebunch(abunch, aname)
        assert result.Name == thename
        
def test_addobject():
    """py.test for addobject"""
    thedata = (('ZONE', 'karamba'), # key, aname
    )
    for key, aname in thedata:
        result = modeleditor.addobject(bunchdt, data, commdct, key, aname)
        assert data.dt[key][-1][1] == aname
        assert bunchdt[key][-1].Name == aname