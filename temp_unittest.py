"""script out a unit test for read an overshooting extensible field"""

# use WindowMaterial:GlazingGroup:Thermochromic

astr = """
Version,
    9.6;                      !- Version Identifier

WINDOWMATERIAL:GLAZINGGROUP:THERMOCHROMIC,
    Gumby,                    !- Name
    55,
    G1,"""
    
extfields = ','.join([f"{i}, G{i}" for i in range(5000)])
newstr = f"{astr} {extfields};"    

import eppy
from io import StringIO
fhandle = StringIO(newstr)
idf = eppy.openidf(fhandle)
idf.saveas("./temp/temp_unittest.idf")

