"""try to import from another file"""

from idfreader import idfreader
import modeleditor

class IDF0(object):
    iddname = None
    def __init__(self, idfname):
        # TODO use file handle instead of file name
        self.idfname = idfname
        self.read()
    @classmethod
    def setiddname(cls, arg):
        # TODO use file handle instead of filename
        if cls.iddname == None:
            cls.iddname = arg
    def read(self):
        """read the idf file"""
        # TODO unit test
        # TODO : thow an exception if iddname = None
        readout = idfreader(self.idfname, self.iddname)
        self.idfobjects, self.model, self.idd_info = readout
    def __repr__(self):
        return self.model.__repr__()
    def save(self):
        # TODO unit test
        s = str(self.model)
        open(self.idfname, 'w').write(s)
    def saveas(self, filename):
        s = str(self.model)
        open(filename, 'w').write(s)

class IDF1(IDF0):
    def __init__(self, idfname):
        super(IDF, self).__init__(idfname)
    def newidfobject(self, key, aname=''):
        # TODO unit test
        modeleditor.addobject(self.idfobjects,
                            self.model,
                            self.idd_info,
                            key, aname=aname)  
    def addidfobject(self, idfobject):
        # TODO unit test
        modeleditor.addthisbunch(self.model,
                            self.idd_info,
                            idfobject)  
            
def test_IDF():
    """py.test for class IDF"""
    assert IDF.iddname == None
    IDF.setiddname("gumby")
    assert IDF.iddname == "gumby"
    IDF.setiddname("karamba")
    assert IDF.iddname != "karamba"
    assert IDF.iddname == "gumby"
    idf = IDF("zoumba")
    assert idf.idfname == "zoumba"
    assert idf.iddname == "gumby"
    
# from idfreader import idfreader
# 
IDF = IDF1

iddfile = "../iddfiles/Energy+V7_2_0.idd"
IDF.setiddname(iddfile)

fname1 = "../idffiles/V_7_2/smallfile.idf"
idf1 = IDF(fname1)

print idf1



# fname2 = "../idffiles/V_7_2/constructions.idf"
# idf2 = IDF(fname2)
# # print idf1
# idfobject = idf1.idfobjects["version".upper()][0]

# print idf2.idfobjects["construction".upper()][0]
# idf1.addobject("ZONE")
# idf1.saveas('a.idf')

# # test addidfobject
# constr = idf2.idfobjects["construction".upper()][0]
# idf1.addidfobject(constr)
# print idf1

# # test newidfobject
# idf1.newidfobject("zone".upper())
# idf1.newidfobject("zone".upper(), "gumby")
# print idf1
 
# bunchdt1, data1, commdct = idfreader(fname1, iddfile)
# bunchdt2, data2, commdct = idfreader(fname2, iddfile)
# 
# cons1 = bunchdt1["Construction".upper()]
# cons2 = bunchdt2["Construction".upper()]
