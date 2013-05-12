"""build a new reader that will read idd only once"""
import datetime
import idfreader
from idfreader import IIDF

d0 = datetime.datetime.now()
iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"


 
bunchdt, data, commdct = idfreader.idfreader(fname, iddfile)

# reading idd
# -----------
# idf = IIDF(fname)
# idfreader1(fname, iddfile) -> 
# readidf.readdatacommdct1(fname, iddfile) ->
# parse_idd.extractidddata(idfname, iddfile) 
# and eplusdata.eplusdata(theidd,)


IIDF.setiddname(iddfile)
idf = IIDF(fname)

d1 = datetime.datetime.now()
print d1 -d0
# idf.printidf()

d0 = d1
idf1 = IIDF(fname)
d1 = datetime.datetime.now()
print d1 -d0

d0 = d1
idf1 = IIDF(fname)
d1 = datetime.datetime.now()
print d1 -d0

d0 = d1
idf1 = IIDF(fname)
d1 = datetime.datetime.now()
print d1 -d0

d0 = d1
idf1 = IIDF(fname)
d1 = datetime.datetime.now()
print d1 -d0

d0 = d1
idf1 = IIDF(fname)
d1 = datetime.datetime.now()
print d1 -d0
