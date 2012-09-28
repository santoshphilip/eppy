"""Remove air distribution unit and replace it with an uncontrolled unit
usage:
python s_adu2uncondr1.py infile zonename aduname unctr_name outfile
"""
import sys
import sys
import getopt




sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf

from EPlusCode.EPlusInterfaceFunctions import parse_idd
from EPlusCode.EPlusInterfaceFunctions import eplusdata
import loops
import eplus_functions


help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg



def adu2unctr(idfw, zonename, aduname, uunitname):
    """replace the airdistribution unit with an uncontrolled terminal"""
    # from ADU grab objtype  and objname
    # remove ADU
    # - 
    # in ZoneHVAC:AirDistributionUnit:
    #   get name, objtype, objname
    data = idfw.idf
    commdct = idfw.idd.commdct
    objkey = "ZoneHVAC:AirDistributionUnit".upper()
    singlefields = ["Name", "Air Terminal Object Type", "Air Terminal Name"]
    repeatfields = []
    fieldlist = singlefields + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    adus = loops.extractfields(data, commdct, objkey, fieldlists)
    adu = [adu for adu in adus if adu[0].upper() == aduname.upper()]
    adu = adu[0]
    objtype = adu[1]
    objname = adu[2]
    # remove adu
    adus = data.dt[objkey]
    adu = [adu for adu in adus if adu[1] == aduname]
    adus.remove(adu[0])

    # get the avaliability, airinletnode of the object reffered to by the ADU
    # in objkey:
    #   get name, avaliability, airinletnode
    objtype = objtype.upper()
    singlefields = ["Name", "Availability Schedule Name", 
        "Air Inlet Node Name"]
    repeatfields = []
    fieldlist = singlefields + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objtype)
    objs = loops.extractfields(data, commdct, objtype, fieldlists)
    obj = [obj for obj in objs if obj[0].upper() == objname.upper()]
    obj = obj[0]
    avaliability = obj[1]
    airinlet = obj[2]
    # find and remove the object refered to by the ADU
    objkey = objtype.upper()
    objs = data.dt[objkey]
    obj = [obj for obj in objs if obj[1].upper() == objname.upper()]
    objs.remove(obj[0])

    # remove ADU from equiplist
    #
    # # in ZoneHVAC:EquipmentList:
    # #   get Name, all equiptype, all equipnames
    # objkey = "ZoneHVAC:EquipmentList".upper()
    # singlefields = ["Name", ]
    # fieldlist = singlefields
    # flds = ["Zone Equipment %s Object Type", "Zone Equipment %s Name"]
    # repeatfields = loops.repeatingfields(data, commdct, objkey, flds)
    # fieldlist = fieldlist + repeatfields
    # fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    # equiplists = loops.extractfields(data, commdct, objkey, fieldlists)
    # equiplistdct = dict([(ep[0], ep[1:])  for ep in equiplists])
    # for key, equips in equiplistdct.items():
    #     enames = [equips[i] for i in range(1, len(equips), 2)]
    #     equiplistdct[key] = enames
    # - 
    objkey = "ZoneHVAC:EquipmentList".upper()
    objs = data.dt[objkey]
    obj = [obj for obj in objs if obj.count(aduname) > 0]
    obj =obj[0]
    index = obj.index(aduname)
    for i in range(4):
        obj.pop(index-1)
    # ------
    # put the uncontrolled unit in
    # in ZoneHVAC:EquipmentConnections:
    #   get Name, equiplist
    objkey = "ZoneHVAC:EquipmentConnections".upper()
    singlefields = ["Zone Name", "Zone Conditioning Equipment List Name"]
    fieldlist = singlefields
    repeatfields = []
    fieldlist = fieldlist + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    econnects = loops.extractfields(data, commdct, objkey, fieldlists)
    econnect = [cn for cn in econnects if cn[0].upper() == zonename.upper()]
    econnect = econnect[0]
    equipconnname = econnect[0]
    theequiplist = econnect[1]
    # add airinletnode to equipconnections
    objkey = "ZoneHVAC:EquipmentConnections".upper()
    field = "Zone Air Inlet Node or NodeList Name"
    eplus_functions.fieldvalue(idfw, objkey, equipconnname, field, airinlet)
    # make uncontrolled unit - and fill some fields
    objkey = "AirTerminal:SingleDuct:Uncontrolled".upper()
    eplus_functions.createobject(idfw, objkey, uunitname)
    field = "Zone Supply Air Node Name"
    eplus_functions.fieldvalue(idfw, objkey, uunitname, field, airinlet)
    field = "Maximum Air Flow Rate"
    eplus_functions.fieldvalue(idfw, objkey, uunitname, field, "autosize")
    field = "Availability Schedule Name"
    eplus_functions.fieldvalue(idfw, objkey, uunitname, field, avaliability)
    # add uncontrolled to equipment list
    objkey = "ZoneHVAC:EquipmentList".upper()
    objs = data.dt[objkey]
    obj = [obj for obj in objs if obj[1].upper() == theequiplist.upper()]
    obj =obj[0]
    obj.extend(["AirTerminal:SingleDuct:Uncontrolled", uunitname, 1, 1])
    # ------


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value

        infile, zonename, aduname, uunitname, outfile = args
        iddfile = "../iddfiles/Energy+V6_0.idd"
        block,commlst,commdct=parse_idd.extractidddata(iddfile)
        theidd=eplusdata.idd(block,2)
        data, commdct = readidf.readdatacommdct(infile, iddfile=theidd,
                                    commdct=commdct)
        idd = eplus_functions.Idd(commdct, commlst, theidd, block)
        idfw = eplus_functions.IdfWrapper(data, idd)
        print "%s | %s | %s" % (zonename, aduname, uunitname)
        adu2unctr(idfw, zonename, aduname, uunitname)
        data = idfw.idf
        txt = `data`
        open(outfile, 'w').write(txt)
        # #--------------------------
        # fname = "../idffiles/doas2.idf"
        # zonename = "ZN_1_FLR_2_SEC_1"
        # aduname = "ZN_1_FLR_2_SEC_1 ATU"
        # uunitname = "ZN_1_FLR_2_SEC_1 uncontrolled"
        # outname = "../idffiles/doas2_1.idf"
        # #--------------------------

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
# python s_adu2uncontr1.py ../idffiles/doas2.idf ZN_1_FLR_2_SEC_1 "ZN_1_FLR_2_SEC_1 ATU" "ZN_1_FLR_2_SEC_1 uncontrolled" ../idffiles/doas2_3.idf
# python s_adu2uncontr1.py ../idffiles/doas2_3.idf ZN_1_FLR_2_SEC_2 "ZN_1_FLR_2_SEC_2 ATU" "ZN_1_FLR_2_SEC_2 uncontrolled" ../idffiles/doas2_4.idf
