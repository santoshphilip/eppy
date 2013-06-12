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

"""This will draw the plant loop for any file 
copy of s_plantloop.py
figure out how to remove the nodes

draws the contents of the branch here."""

import pydot
import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf
import loops

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
                    except ValueError, e:
                        newedges.append(newtup)
                    added = True
        elif secondisnode(edge):
            for edge1 in edges:
                if edge[1] == edge1[0]:
                    newtup = (edge[0], edge1[1])
                    try:
                        newedges.index(newtup)
                    except ValueError, e:
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
    
    
def test_dropnodes():
    """py.test for dropnodes"""
    # test 1
    node = "node"
    (a,b,c,d,e,f,g,h,i) = (('a', node),'b',('c', node),'d',
        ('e', node),'f',('g', node),'h',('i', node))
    edges = [(a, b),
    (b, c),
    (c, d),
    (d, e),
    (e, f),
    (f, g),
    (g, h),
    (h, i),]
    theresult = [('a', 'b'), ('b', 'd'), ('d', 'f'), ('f', 'h'), ('h', 'i')]
    result = dropnodes(edges)
    assert result == theresult
    # test 2
    (a,b,c,d,e,f,g,h,i,j) = (('a', node),'b',('c', node),
        ('d', node),'e','f',('g', node),('h', node),'i',('j', node))
    edges = [(a, b),
    (b, c),
    (c, e),
    (e, g),
    (g, i),
    (i, j),
    (b, d),
    (d, f),
    (f, h),
    (h, i),]
    theresult = [('a', 'b'), ('b', 'e'), ('e', 'i'), ('i', 'j'), 
            ('b', 'f'), ('f', 'i')]
    result = dropnodes(edges)
    assert result == theresult
    
def makeanode(name):
    return pydot.Node(name, shape="plaintext", label=name)
    
def makeabranch(name):
    return pydot.Node(name, shape="box3d", label=name)

def makeendnode(name):
    return pydot.Node(name, shape="circle", label=name, 
        style="filled", fillcolor="#e4e4e4")
    
def istuple(x):
    return type(x) == tuple

def nodetype(anode):
    """return the type of node"""
    try:
        return anode[1]
    except IndexError, e:
        return None


def edges2nodes(edges):
    """gather the nodes from the edges"""
    nodes = []
    for e1, e2 in edges:
        nodes.append(e1)
        nodes.append(e2)
    nodedict = dict([(n, None) for n in nodes])
    justnodes = nodedict.keys()
    justnodes.sort()
    return justnodes
    
def test_edges2nodes():
    """py.test for edges2nodes"""
    thedata = (([("a", "b"), ("b", "c"), ("c", "d")],
    ["a", "b", "c", "d"]), # edges, nodes
    )
    for edges, nodes in thedata:
        result = edges2nodes(edges)   
        assert result == nodes
        

def makediagram(edges):
    """make the diagram with the edges"""
    graph = pydot.Dot(graph_type='digraph')
    nodes = edges2nodes(edges)
    epnodes = [(node, 
        makeanode(node[0])) for node in nodes if nodetype(node)=="epnode"]
    endnodes = [(node, 
        makeendnode(node[0])) for node in nodes if nodetype(node)=="EndNode"]
    epbr = [(node, makeabranch(node)) for node in nodes if not istuple(node)]
    nodedict = dict(epnodes + epbr + endnodes)
    for value in nodedict.values():
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

iddfile = "../iddfiles/Energy+V6_0.idd"
# fname = "/Applications/EnergyPlus-6-0-0/Examples/DualDuctConstVolGasHC.idf"
# fname = "../idffiles/a.idf"
# fname = "/Volumes/Server/Active_Projects/stanttecE+Conssulting2/3_Simulation/2_Energy/EnergyPlus/fromMatt/Proposed110614exp.idf"
# fname = "/Volumes/Server/Active_Projects/stanttecE+Conssulting2/3_Simulation/2_Energy/EnergyPlus/workingfiles/5ZoneAirCooled.idf"
# fname = "/Volumes/Server/Active_Projects/LBNL_UHM/3_Simulation/2_Energy/Energyplus3/airflow/air6.expidf"
# fname = "/Volumes/Server/Staff/Santosh/transfer/asul/05_Baseline_06.idf"
fname = "/Applications/EnergyPlus-6-0-0/Examples/DualDuctConstVolGasHC.idf"
# fname = "../idffiles/HVACTemplate-5ZoneVAVFanPowered.idf"
# outname = "../idffiles/.idf"
fname = "../idffiles/CoolingTower.idf"
fname = "../idffiles/a.idf"
fname = "../idffiles/5ZoneSupRetPlenRAB.idf" # for supply plenum
# fname = "a.idf"
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)


# in plantloop get:
#     demand inlet, outlet, branchlist
#     supply inlet, outlet, branchlist
plantloops = loops.plantloopfields(data, commdct)
plantloop = plantloops[0]
anode = "epnode"
endnode = "EndNode"
#     
# supply barnchlist
#     branch1 -> inlet, outlet
#     branch2 -> inlet, outlet
#     branch3 -> inlet, outlet
sbranchlist = plantloop[3]
if sbranchlist.strip() != "":
    sbranches = loops.branchlist2branches(data, commdct, sbranchlist)
    s_in_out = [loops.branch_inlet_outlet(data, commdct, 
                                    sbranch) for sbranch in sbranches]
    sbranchinout = dict(zip(sbranches, (s_in_out, anode)))                            

dbranchlist = plantloop[6]
if dbranchlist.strip() != "":
    dbranches = loops.branchlist2branches(data, commdct, dbranchlist)
    d_in_out = [loops.branch_inlet_outlet(data, commdct, 
                                    dbranch) for dbranch in dbranches]
    dbranchinout = dict(zip(dbranches, (d_in_out, anode)))                            
#     
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
    
    
g = makediagram(edges)


g.write('a.dot')
g.write_png('a.png')