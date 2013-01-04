"""track down references"""

from idfreader import idfreader

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)

for i, key in enumerate(data.dtls):
    for fieldcomm in commdct[i]:
            # print comm
            if fieldcomm.has_key('reference'):
                if fieldcomm['field'] != ["Name"]:
                    print key
                    print fieldcomm['field']
                    print fieldcomm['reference']
                    print fieldcomm['type']
                    print fieldcomm.keys()
        # print key_comm
        # print
        # for comms in key_comm:
        #     print comms
        # for comm in comms:
        #     print comm
        #     if comm.has_key('reference'):
        #         print comm['field']
        #         print comm['reference']
    # if i > 3:
    #     break
    