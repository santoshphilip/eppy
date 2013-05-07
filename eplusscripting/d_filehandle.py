"""read the idf file using a file handle"""
# tested and works now

from idfreader import idfreader

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"

 
# bunchdt, data, commdct = idfreader(fname, iddfile)
# s = str(data)
# open("f.idf", 'w').write(s)



# reading idd
# -----------
# idfreader -> 
# readidf.readdatacommdct ->
# parse_idd.extractidddata ->
# DONE

# reading idf
# -----------
# idfreader -> 
# readidf.readdatacommdct ->
# eplusdata.eplusdata(theidd,idfname)

iddhandle = open(iddfile, 'r')
fhandle = open(fname, 'r')

bunchdt, data, commdct = idfreader(fname, iddhandle)
s = str(data)
open("fh.idf", 'w').write(s)

iddhandle.close()
fhandle.close()

iddhandle = open(iddfile, 'r')
fhandle = open(fname, 'r')

# bunchdt, data, commdct = idfreader(fhandle, iddhandle)
# s = str(data)
# open("fhfh.idf", 'w').write(s)

iddhandle.close()
fhandle.close()

from StringIO import StringIO
iddtxt = """Version,
      \\unique-object
      \\format singleLine
  A1 ; \\field Version Identifier
      \\required-field
      \\default 5.0

"""

idftxt = """Version,6.0;
"""
iddhandle = StringIO(iddtxt)
# iddhandle = open(iddfile, 'r')
fhandle = StringIO(idftxt)

bunchdt, data, commdct = idfreader(fhandle, iddhandle)
s = str(data)
open("fsfs.idf", 'w').write(s)

iddhandle.close()
fhandle.close()
