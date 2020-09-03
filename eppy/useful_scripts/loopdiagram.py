# Copyright (c) 2012 Santosh Philip
# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""Draw all the  loops in the IDF file.

There are two output files saved in the same location as the idf file:
- idf_file_location/idf_filename.dot
- idf_file_location/idf_filename.png

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)

import argparse
import eppy
import eppy.EPlusInterfaceFunctions
from eppy.EPlusInterfaceFunctions import readidf

# import pydot3k as pydot
import pydot

import eppy.loops as loops


pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)


def firstisnode(edge):
    if type(edge[0]) == tuple:
        return True
    else:
        return False


def secondisnode(edge):
    if type(edge[1]) == tuple:
        return True
    else:
        return False


def bothnodes(edge):
    if type(edge[0]) == tuple and type(edge[1]) == tuple:
        return True
    else:
        return False


def dropnodes(edges):
    """draw a graph without the nodes"""
    newedges = []
    added = False
    for edge in edges:
        if bothnodes(edge):
            newtup = (edge[0][0], edge[1][0])
            newedges.append(newtup)
            added = True
        elif firstisnode(edge):
            for edge1 in edges:
                if edge[0] == edge1[1]:
                    newtup = (edge1[0], edge[1])
                    try:
                        newedges.index(newtup)
                    except ValueError as e:
                        newedges.append(newtup)
                    added = True
        elif secondisnode(edge):
            for edge1 in edges:
                if edge[1] == edge1[0]:
                    newtup = (edge[0], edge1[1])
                    try:
                        newedges.index(newtup)
                    except ValueError as e:
                        newedges.append(newtup)
                    added = True
        # gets the hanging nodes - nodes with no connection
        if not added:
            if firstisnode(edge):
                newedges.append((edge[0][0], edge[1]))
            if secondisnode(edge):
                newedges.append((edge[0], edge[1][0]))
        added = False
    return newedges


def makeanode(name):
    return pydot.Node(name, shape="plaintext", label=name)


def makeabranch(name):
    return pydot.Node(name, shape="box3d", label=name)


def makeendnode(name):
    return pydot.Node(
        name, shape="doubleoctagon", label=name, style="filled", fillcolor="#e4e4e4"
    )


def istuple(x):
    return type(x) == tuple


def nodetype(anode):
    """return the type of node"""
    try:
        return anode[1]
    except IndexError as e:
        return None


def edges2nodes(edges):
    """gather the nodes from the edges"""
    nodes = []
    for e1, e2 in edges:
        nodes.append(e1)
        nodes.append(e2)
    nodedict = dict([(n, None) for n in nodes])
    justnodes = list(nodedict.keys())
    # justnodes.sort()
    justnodes = sorted(justnodes, key=lambda x: str(x[0]))
    return justnodes


def makediagram(edges):
    """make the diagram with the edges"""
    graph = pydot.Dot(graph_type="digraph")
    nodes = edges2nodes(edges)
    epnodes = [
        (node, makeanode(node[0])) for node in nodes if nodetype(node) == "epnode"
    ]
    endnodes = [
        (node, makeendnode(node[0])) for node in nodes if nodetype(node) == "EndNode"
    ]
    epbr = [(node, makeabranch(node)) for node in nodes if not istuple(node)]
    nodedict = dict(epnodes + epbr + endnodes)
    for value in list(nodedict.values()):
        graph.add_node(value)
    for e1, e2 in edges:
        graph.add_edge(pydot.Edge(nodedict[e1], nodedict[e2]))
    return graph


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
    return zip(*mtx)


def makebranchcomponents(data, commdct, anode="epnode"):
    """return the edges jointing the components of a branch"""
    alledges = []

    objkey = "BRANCH"
    cnamefield = "Component %s Name"
    inletfield = "Component %s Inlet Node Name"
    outletfield = "Component %s Outlet Node Name"

    numobjects = len(data.dt[objkey])
    cnamefields = loops.repeatingfields(data, commdct, objkey, cnamefield)
    inletfields = loops.repeatingfields(data, commdct, objkey, inletfield)
    outletfields = loops.repeatingfields(data, commdct, objkey, outletfield)

    inlts = loops.extractfields(data, commdct, objkey, [inletfields] * numobjects)
    cmps = loops.extractfields(data, commdct, objkey, [cnamefields] * numobjects)
    otlts = loops.extractfields(data, commdct, objkey, [outletfields] * numobjects)

    zipped = list(zip(inlts, cmps, otlts))
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
        branch_i_o[br_name] = dict(list(zip(["inlet", "outlet"], in_out)))
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
        moreedges = [(splittername, (outlet, anode)) for outlet in splitter_outlets]
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
    # for plantloop in plantloops:
    #     supplyinlet = plantloop[1]
    #     supplyoutlet = plantloop[2]
    #     demandinlet = plantloop[4]
    #     demandoutlet = plantloop[5]
    #     # edges = [supplyoutlet -> demandinlet, demandoutlet -> supplyinlet]
    #     moreedges = [((supplyoutlet, endnode), (demandinlet, endnode)),
    #         ((demandoutlet, endnode), (supplyinlet, endnode))]
    #     edges = edges + moreedges
    #
    # -----------air loop stuff----------------------
    # from s_airloop2.py
    # Get the demand and supply nodes from 'airloophvac'
    # in airloophvac get:
    #   get branch, supplyinlet, supplyoutlet, demandinlet, demandoutlet
    objkey = "airloophvac".upper()
    fieldlists = [
        [
            "Branch List Name",
            "Supply Side Inlet Node Name",
            "Demand Side Outlet Node Name",
            "Demand Side Inlet Node Names",
            "Supply Side Outlet Node Names",
        ]
    ] * loops.objectcount(data, objkey)
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
    singlefields = [
        "Zone Name",
        "Zone Conditioning Equipment List Name",
        "Zone Air Node Name",
        "Zone Return Air Node Name",
    ]
    repeatfields = []
    fieldlist = singlefields + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    equipconnections = loops.extractfields(data, commdct, objkey, fieldlists)
    # in ZoneHVAC:EquipmentList:
    #   get Name, all equiptype, all equipnames
    objkey = "ZoneHVAC:EquipmentList".upper()
    singlefields = ["Name"]
    fieldlist = singlefields
    flds = ["Zone Equipment %s Object Type", "Zone Equipment %s Name"]
    repeatfields = loops.repeatingfields(data, commdct, objkey, flds)
    fieldlist = fieldlist + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    equiplists = loops.extractfields(data, commdct, objkey, fieldlists)
    equiplistdct = dict([(ep[0], ep[1:]) for ep in equiplists])
    for key, equips in list(equiplistdct.items()):
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
    for key in list(adistuinlets.keys()):
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

    anode = "epnode"
    endnode = "EndNode"

    # edges = []

    # connect demand and supply side
    # for airloophvac in airloophvacs:
    #     supplyinlet = airloophvac[1]
    #     supplyoutlet = airloophvac[4]
    #     demandinlet = airloophvac[3]
    #     demandoutlet = airloophvac[2]
    #     # edges = [supplyoutlet -> demandinlet, demandoutlet -> supplyinlet]
    #     moreedges = [((supplyoutlet, endnode), (demandinlet, endnode)),
    #         ((demandoutlet, endnode), (supplyinlet, endnode))]
    #     edges = edges + moreedges

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


def getedges(fname, iddfile):
    """return the edges of the idf file fname"""
    data, commdct, _idd_index = readidf.readdatacommdct(fname, iddfile=iddfile)
    edges = makeairplantloop(data, commdct)
    return edges


def replace_colon(s, replacewith="__"):
    """replace the colon with something"""
    return s.replace(":", replacewith)


def clean_edges(arg):
    if isinstance(arg, str):
        return replace_colon(arg)
    try:
        return tuple(clean_edges(x) for x in arg)
    except TypeError:  # catch when for loop fails
        return replace_colon(arg)  # not a sequence so just return repr


def make_and_save_diagram(fname, iddfile):
    g = process_idf(fname, iddfile)
    save_diagram(fname, g)


def process_idf(fname, iddfile):
    data, commdct, _iddindex = readidf.readdatacommdct(fname, iddfile=iddfile)
    print("constructing the loops")
    edges = makeairplantloop(data, commdct)
    print("cleaning edges")
    edges = clean_edges(edges)
    print("making the diagram")

    return makediagram(edges)


def save_diagram(fname, g, silent=False):
    dotname = "%s.dot" % (os.path.splitext(fname)[0])
    pngname = "%s.png" % (os.path.splitext(fname)[0])
    g.write(dotname)
    if not silent:
        print("saved file: %s" % (dotname))
    g.write_png(pngname)
    if not silent:
        print("saved file: %s" % (pngname))


def main():
    parser = argparse.ArgumentParser(
        usage=None, description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    # need the formatter to print newline from __doc__
    parser.add_argument(
        "idd",
        type=str,
        action="store",
        help="location of idd file = ./somewhere/eplusv8-0-1.idd",
    )
    parser.add_argument(
        "file",
        type=str,
        action="store",
        help="location of idf file = ./somewhere/f1.idf",
    )
    args = parser.parse_args()
    make_and_save_diagram(args.file, args.idd)


if __name__ == "__main__":
    sys.exit(main())
