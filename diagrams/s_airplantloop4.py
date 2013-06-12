# Copyright (c) 2012 Santosh Philip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

"""draw plant and air loop
s_plantloop5.py + s_airloop2.py
- connects demand and supply side
has main with arguments

same as s_airplantloop1.py, but calls functions from diagram.py"""

import pydot
import sys
import os
import getopt
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf
import loops
import diagram

help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def transpose2d(mtx):
    """Transpose a 2d matrix
       [
            [1,2,3],
            [4,5,6]
            ]
        becomes
        [
            [1,4],
            [2,5],
            [3,6]
            ]
    """
    trmtx = [[] for i in mtx[0]]
    for i in range(len(mtx)):
        for j in range(len(mtx[i])):
            trmtx[j].append(mtx[i][j])
    return trmtx
##   -------------------------    
##    from python cookbook 2nd edition page 162
    # map(mtx, zip(*arr))

def makebranchcomponents(data, commdct, anode="epnode"):
    """return the edges jointing the components of a branch"""
    alledges = []

    objkey = 'BRANCH'
    cnamefield = "Component %s Name"
    inletfield = "Component %s Inlet Node Name"
    outletfield = "Component %s Outlet Node Name"

    numobjects = len(data.dt[objkey])
    cnamefields = loops.repeatingfields(data, commdct, objkey, cnamefield)
    inletfields = loops.repeatingfields(data, commdct, objkey, inletfield)
    outletfields = loops.repeatingfields(data, commdct, objkey, outletfield)

    inlts = loops.extractfields(data, commdct, 
        objkey, [inletfields] * numobjects)
    cmps = loops.extractfields(data, commdct, 
        objkey, [cnamefields] * numobjects)
    otlts = loops.extractfields(data, commdct, 
        objkey, [outletfields] * numobjects)

    zipped = zip(inlts, cmps, otlts)
    tzipped = [transpose2d(item) for item in zipped]
    for i in range(len(data.dt[objkey])):
        tt = tzipped[i]
        # branchname = data.dt[objkey][i][1]
        edges = []
        for t0 in tt:
            edges = edges + [((t0[0], anode), t0[1]), (t0[1], (t0[2], anode))]
        alledges = alledges + edges
    return alledges

def makeairplantloop(data, commdct):
    """make the edges for the airloop and the plantloop"""
    anode = "epnode"
    endnode = "EndNode"

    # in plantloop get:
    #     demand inlet, outlet, branchlist
    #     supply inlet, outlet, branchlist
    plantloops = loops.plantloopfields(data, commdct)
    # splitters
    #     inlet
    #     outlet1
    #     outlet2
    splitters = loops.splitterfields(data, commdct)
    #     
    # mixer
    #     outlet
    #     inlet1
    #     inlet2

    mixers = loops.mixerfields(data, commdct)
    #     
    # supply barnchlist
    #     branch1 -> inlet, outlet
    #     branch2 -> inlet, outlet
    #     branch3 -> inlet, outlet
    #         
    # CONNET INLET OUTLETS
    edges = []

    # get all branches
    branchkey = "branch".upper()
    branches = data.dt[branchkey]
    branch_i_o = {}
    for br in branches:
        br_name = br[1]
        in_out = loops.branch_inlet_outlet(data, commdct, br_name)
        branch_i_o[br_name] = dict(zip(["inlet", "outlet"], in_out))
    # for br_name, in_out in branch_i_o.items():
    #     edges.append(((in_out["inlet"], anode), br_name))
    #     edges.append((br_name, (in_out["outlet"], anode)))

    # instead of doing the branch
    # do the content of the branch
    edges = makebranchcomponents(data, commdct)


    # connect splitter to nodes
    for splitter in splitters:
        # splitter_inlet = inletbranch.node
        splittername = splitter[0]
        inletbranchname = splitter[1] 
        splitter_inlet = branch_i_o[inletbranchname]["outlet"]
        # edges = splitter_inlet -> splittername
        edges.append(((splitter_inlet, anode), splittername))
        # splitter_outlets = ouletbranches.nodes
        outletbranchnames = [br for br in splitter[2:]]
        splitter_outlets = [branch_i_o[br]["inlet"] for br in outletbranchnames]
        # edges = [splittername -> outlet for outlet in splitter_outlets]
        moreedges = [(splittername, 
                            (outlet, anode)) for outlet in splitter_outlets]
        edges = edges + moreedges

    for mixer in mixers:
        # mixer_outlet = outletbranch.node
        mixername = mixer[0]
        outletbranchname = mixer[1] 
        mixer_outlet = branch_i_o[outletbranchname]["inlet"]
        # edges = mixername -> mixer_outlet
        edges.append((mixername, (mixer_outlet, anode)))
        # mixer_inlets = inletbranches.nodes
        inletbranchnames = [br for br in mixer[2:]]
        mixer_inlets = [branch_i_o[br]["outlet"] for br in inletbranchnames]
        # edges = [mixername -> inlet for inlet in mixer_inlets]
        moreedges = [((inlet, anode), mixername) for inlet in mixer_inlets]
        edges = edges + moreedges

    # connect demand and supply side
    for plantloop in plantloops:
        supplyinlet = plantloop[1]
        supplyoutlet = plantloop[2]
        demandinlet = plantloop[4]
        demandoutlet = plantloop[5]
        # edges = [supplyoutlet -> demandinlet, demandoutlet -> supplyinlet]
        moreedges = [((supplyoutlet, endnode), (demandinlet, endnode)), 
            ((demandoutlet, endnode), (supplyinlet, endnode))]
        edges = edges + moreedges
        
    # -----------air loop stuff----------------------
    # from s_airloop2.py
    # Get the demand and supply nodes from 'airloophvac'
    # in airloophvac get:
    #   get branch, supplyinlet, supplyoutlet, demandinlet, demandoutlet
    objkey = "airloophvac".upper()
    fieldlists = [["Branch List Name",
        "Supply Side Inlet Node Name",
        "Demand Side Outlet Node Name",
        "Demand Side Inlet Node Names",
        "Supply Side Outlet Node Names"]] * loops.objectcount(data, objkey)
    airloophvacs = loops.extractfields(data, commdct, objkey, fieldlists)
    # airloophvac = airloophvacs[0]

    # in AirLoopHVAC:ZoneSplitter:
    #   get Name, inlet, all outlets
    objkey = "AirLoopHVAC:ZoneSplitter".upper()
    singlefields = ["Name", "Inlet Node Name"]
    fld = "Outlet %s Node Name"
    repeatfields = loops.repeatingfields(data, commdct, objkey, fld)
    fieldlist = singlefields + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    zonesplitters = loops.extractfields(data, commdct, objkey, fieldlists)

    # in AirLoopHVAC:SupplyPlenum:
    #   get Name, Zone Name, Zone Node Name, inlet, all outlets
    objkey = "AirLoopHVAC:SupplyPlenum".upper()
    singlefields = ["Name", "Zone Name", "Zone Node Name", "Inlet Node Name"]
    fld = "Outlet %s Node Name"
    repeatfields = loops.repeatingfields(data, commdct, objkey, fld)
    fieldlist = singlefields + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    supplyplenums = loops.extractfields(data, commdct, objkey, fieldlists)

    # in AirLoopHVAC:ZoneMixer:
    #   get Name, outlet, all inlets
    objkey = "AirLoopHVAC:ZoneMixer".upper()
    singlefields = ["Name", "Outlet Node Name"]
    fld = "Inlet %s Node Name"
    repeatfields = loops.repeatingfields(data, commdct, objkey, fld)
    fieldlist = singlefields + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    zonemixers = loops.extractfields(data, commdct, objkey, fieldlists)

    # in AirLoopHVAC:ReturnPlenum:
    #   get Name, Zone Name, Zone Node Name, outlet, all inlets
    objkey = "AirLoopHVAC:ReturnPlenum".upper()
    singlefields = ["Name", "Zone Name", "Zone Node Name", "Outlet Node Name"]
    fld = "Inlet %s Node Name"
    repeatfields = loops.repeatingfields(data, commdct, objkey, fld)
    fieldlist = singlefields + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    returnplenums = loops.extractfields(data, commdct, objkey, fieldlists)


    # connect room to each equip in equiplist
    # in ZoneHVAC:EquipmentConnections:
    #   get Name, equiplist, zoneairnode, returnnode
    objkey = "ZoneHVAC:EquipmentConnections".upper()
    singlefields = ["Zone Name", "Zone Conditioning Equipment List Name", 
        "Zone Air Node Name", "Zone Return Air Node Name"]
    repeatfields = []
    fieldlist = singlefields + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    equipconnections = loops.extractfields(data, commdct, objkey, fieldlists)
    # in ZoneHVAC:EquipmentList:
    #   get Name, all equiptype, all equipnames
    objkey = "ZoneHVAC:EquipmentList".upper()
    singlefields = ["Name", ]
    fieldlist = singlefields
    flds = ["Zone Equipment %s Object Type", "Zone Equipment %s Name"]
    repeatfields = loops.repeatingfields(data, commdct, objkey, flds)
    fieldlist = fieldlist + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    equiplists = loops.extractfields(data, commdct, objkey, fieldlists)
    equiplistdct = dict([(ep[0], ep[1:])  for ep in equiplists])
    for key, equips in equiplistdct.items():
        enames = [equips[i] for i in range(1, len(equips), 2)]
        equiplistdct[key] = enames
    # adistuunit -> room    
    # adistuunit <- VAVreheat 
    # airinlet -> VAVreheat
    # in ZoneHVAC:AirDistributionUnit:
    #   get Name, equiplist, zoneairnode, returnnode
    objkey = "ZoneHVAC:AirDistributionUnit".upper()
    singlefields = ["Name", "Air Terminal Object Type", "Air Terminal Name"]
    repeatfields = []
    fieldlist = singlefields + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    adistuunits = loops.extractfields(data, commdct, objkey, fieldlists)
    # code only for AirTerminal:SingleDuct:VAV:Reheat
    # get airinletnodes for vavreheats
    # in AirTerminal:SingleDuct:VAV:Reheat:
    #   get Name, airinletnode
    adistuinlets = loops.makeadistu_inlets(data, commdct)
    alladistu_comps = []
    for key in adistuinlets.keys():
        objkey = key.upper()
        singlefields = ["Name"] + adistuinlets[key]
        repeatfields = []
        fieldlist = singlefields + repeatfields
        fieldlists = [fieldlist] * loops.objectcount(data, objkey)
        adistu_components = loops.extractfields(data, commdct, objkey, fieldlists)
        alladistu_comps.append(adistu_components)

    # in AirTerminal:SingleDuct:Uncontrolled:
    #   get Name, airinletnode
    objkey = "AirTerminal:SingleDuct:Uncontrolled".upper()
    singlefields = ["Name", "Zone Supply Air Node Name"]
    repeatfields = []
    fieldlist = singlefields + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    uncontrolleds = loops.extractfields(data, commdct, objkey, fieldlists)
    


    #---------

    anode = "epnode"
    endnode = "EndNode"

    # edges = []

    # connect demand and supply side
    for airloophvac in airloophvacs:
        supplyinlet = airloophvac[1]
        supplyoutlet = airloophvac[4]
        demandinlet = airloophvac[3]
        demandoutlet = airloophvac[2]
        # edges = [supplyoutlet -> demandinlet, demandoutlet -> supplyinlet]
        moreedges = [((supplyoutlet, endnode), (demandinlet, endnode)),
            ((demandoutlet, endnode), (supplyinlet, endnode))]
        edges = edges + moreedges

    # connect zonesplitter to nodes
    for zonesplitter in zonesplitters:
        name = zonesplitter[0]
        inlet = zonesplitter[1]
        outlets = zonesplitter[2:]
        edges.append(((inlet, anode), name))
        for outlet in outlets:
            edges.append((name, (outlet, anode)))

    # connect supplyplenum to nodes
    for supplyplenum in supplyplenums:
        name = supplyplenum[0]
        inlet = supplyplenum[3]
        outlets = supplyplenum[4:]
        edges.append(((inlet, anode), name))
        for outlet in outlets:
            edges.append((name, (outlet, anode)))

    # connect zonemixer to nodes
    for zonemixer in zonemixers:
        name = zonemixer[0]
        outlet = zonemixer[1]
        inlets = zonemixer[2:]
        edges.append((name, (outlet, anode)))
        for inlet in inlets:
            edges.append(((inlet, anode), name))

    # connect returnplenums to nodes
    for returnplenum in returnplenums:
        name = returnplenum[0]
        outlet = returnplenum[3]
        inlets = returnplenum[4:]
        edges.append((name, (outlet, anode)))
        for inlet in inlets:
            edges.append(((inlet, anode), name))

    # connect room to return node
    for equipconnection in equipconnections:
        zonename = equipconnection[0]
        returnnode = equipconnection[-1]
        edges.append((zonename, (returnnode, anode)))
    
    # connect equips to room
    for equipconnection in equipconnections:
        zonename = equipconnection[0]
        zequiplistname = equipconnection[1]
        for zequip in equiplistdct[zequiplistname]:
            edges.append((zequip, zonename))

    # adistuunit <- adistu_component 
    for adistuunit in adistuunits:
        unitname = adistuunit[0]
        compname = adistuunit[2]
        edges.append((compname, unitname))

    # airinlet -> adistu_component
    for adistu_comps in alladistu_comps:
        for adistu_comp in adistu_comps:
            name = adistu_comp[0]
            for airnode in adistu_comp[1:]:
                edges.append(((airnode, anode), name))

    # supplyairnode -> uncontrolled
    for uncontrolled in uncontrolleds:
        name = uncontrolled[0]
        airnode = uncontrolled[1]            
        edges.append(((airnode, anode), name))

                
    # edges = edges + moreedges    
    return edges






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
                
        iddfile = "../iddfiles/Energy+V6_0.idd"
        fname = args[0]
        iddfile = "../iddfiles/Energy+V6_0.idd"
        print "readingfile"
        data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)
        print "constructing the loops"
        edges = makeairplantloop(data, commdct)
        edges = diagram.cleanedges(edges)
        print "making the diagram"
        g = diagram.makediagram(edges)
        dotname = '%s_c.dot' % (os.path.splitext(fname)[0])
        pngname = '%s_c.png' % (os.path.splitext(fname)[0])
        g.write(dotname)
        g.write_png(pngname)
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
