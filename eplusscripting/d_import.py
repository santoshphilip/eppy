"""try to import from another file"""

from idfreader import idfreader

class IDF0(object):
    iddname = None
    def __init__(self, idfname):
        self.idfname = idfname
        self.read()
    @classmethod
    def setiddname(cls, arg):
        if cls.iddname == None:
            cls.iddname = arg
    def read(self):
        """read the idf file"""
        # TODO : thow an exception if iddname = None
        self.objects, model, idd_info = idfreader(self.idfname, self.iddname)

class IDF1(IDF0):
    def __init__(self, idfname):
        super(IDF, self).__init__(idfname)
        
            
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
fname2 = "../idffiles/V_7_2/constructions.idf"
idf1 = IDF(fname1)
idf2 = IDF(fname2)
print idf1.objects["version".upper()][0]
print idf2.objects["construction".upper()][0]
# 
 
# bunchdt1, data1, commdct = idfreader(fname1, iddfile)
# bunchdt2, data2, commdct = idfreader(fname2, iddfile)
# 
# cons1 = bunchdt1["Construction".upper()]
# cons2 = bunchdt2["Construction".upper()]
