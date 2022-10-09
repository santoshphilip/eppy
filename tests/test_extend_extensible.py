"""py.test to test extending extensible fields beyond what is in the IDD file"""

from io import StringIO

from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF


# idd is read only once in this test
# if it has already been read from some other test, it will continue with
# the old reading
iddfhandle = StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)

def test_read_overextended():
    """py.test when reading an IDD that has more fields than the IDD"""
    astr = """
    Version,
        9.6;                      !- Version Identifier

    WINDOWMATERIAL:GLAZINGGROUP:THERMOCHROMIC,
        Gumby,                    !- Name
        55,
        G1,"""
    
    # nn = 5000
    nn = 50
    extfields = ','.join([f"{i}, G{i}" for i in range(nn)])
    newstr = f"{astr} {extfields};"    

    fhandle = StringIO(newstr)
    idf = IDF(fhandle)
    wm = idf.idfobjects["WINDOWMATERIAL:GLAZINGGROUP:THERMOCHROMIC"]
    assert wm[0][f'Optical_Data_Temperature_{nn + 1}'] == nn - 1
    assert wm[0][f'Window_Material_Glazing_Name_{nn + 1}'] == f"G{nn - 1}"

def test_newidfobject_overextend():
    """py.test when idf.newidfobject creates an object with more fields than avaliable in the IDD"""
    idf = IDF(StringIO(""))
    n = 2000
    d1 = dict(Name="Gumby")
    d2 = {f"Optical_Data_Temperature_{i}":i for i in range(1, n+1)}
    d3 = {f"Window_Material_Glazing_Name_{i}":f"G{i}" for i in range(1, n+1)}
    kwargs = dict()
    kwargs.update(d1)
    kwargs.update(d2)
    kwargs.update(d3)
    wm = idf.newidfobject("WindowMaterial:GlazingGroup:Thermochromic", **kwargs)
    assert wm.Optical_Data_Temperature_2000 == 2000
    assert wm.Window_Material_Glazing_Name_2000 == "G2000"


