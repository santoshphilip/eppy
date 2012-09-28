"""This will draw the plant loop for any file 
Also makes a folder with the branch diagrams"""

import getopt
import os
import pydot
import sys
import glob
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf
import loops


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


# make graphs
def makebranchgrapsh(data, commdct):
    """return the pydot graphs for the all branches"""
    allgraphs = []

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
            edges = edges + [(t0[0], t0[1]), (t0[1], t0[2])]
        g=pydot.graph_from_edges(edges, directed=True)
        allgraphs.append(g)
    return allgraphs


# make folder
def makefolder(fname):
    """make a folder for the branch diagrams. Return it's path"""
    newfolder = "%s_branches" % (os.path.splitext(fname)[0], )
    if os.path.exists(newfolder) == False:
        os.makedirs(newfolder)
    else:
        for thext in ('png', 'dot'):
            dotfiles = glob.glob('%s/*.%s' % (newfolder, thext))
            [os.remove(afile) for afile in dotfiles]
    return newfolder


# save files
def makesavebranchdiagrams(fname, iddfile):
    """make and save branch diagrams"""
    data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)
    allgraphs = makebranchgrapsh(data, commdct)
    newfolder = makefolder(fname)
    objkey = "BRANCH"
    branchnames = [br[1] for br in data.dt[objkey]]
    for branchname, gr in zip(branchnames, allgraphs):
        gr.write('%s/%s.dot' % (newfolder, branchname, ))
        gr.write_png('%s/%s.png' % (newfolder, branchname, ))

def makeplantloop(iddfile, fname):
    """make the plant loop"""
    data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)


    # in plantloop get:
    #     demand inlet, outlet, branchlist
    #     supply inlet, outlet, branchlist
    plantloops = loops.plantloopfields(data, commdct)
    plantloop = plantloops[0]
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
        sbranchinout = dict(zip(sbranches, s_in_out))                            

    dbranchlist = plantloop[6]
    if dbranchlist.strip() != "":
        dbranches = loops.branchlist2branches(data, commdct, dbranchlist)
        d_in_out = [loops.branch_inlet_outlet(data, commdct, 
                                        dbranch) for dbranch in dbranches]
        dbranchinout = dict(zip(dbranches, d_in_out))                            
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
    for br_name, in_out in branch_i_o.items():
        edges.append((in_out["inlet"], br_name))
        edges.append((br_name, in_out["outlet"]))



    # connect splitter to nodes
    for splitter in splitters:
        # splitter_inlet = inletbranch.node
        splittername = splitter[0]
        inletbranchname = splitter[1] 
        splitter_inlet = branch_i_o[inletbranchname]["outlet"]
        # edges = splitter_inlet -> splittername
        edges.append((splitter_inlet, splittername))
        # splitter_outlets = ouletbranches.nodes
        outletbranchnames = [br for br in splitter[2:]]
        splitter_outlets = [branch_i_o[br]["inlet"] for br in outletbranchnames]
        # edges = [splittername -> outlet for outlet in splitter_outlets]
        moreedges = [(splittername, outlet) for outlet in splitter_outlets]
        edges = edges + moreedges

    for mixer in mixers:
        # mixer_outlet = outletbranch.node
        mixername = mixer[0]
        outletbranchname = mixer[1] 
        mixer_outlet = branch_i_o[outletbranchname]["inlet"]
        # edges = mixername -> mixer_outlet
        edges.append((mixername, mixer_outlet))
        # mixer_inlets = inletbranches.nodes
        inletbranchnames = [br for br in mixer[2:]]
        mixer_inlets = [branch_i_o[br]["outlet"] for br in inletbranchnames]
        # edges = [mixername -> inlet for inlet in mixer_inlets]
        moreedges = [(inlet, mixername) for inlet in mixer_inlets]
        edges = edges + moreedges

    # connect demand and supply side
    for plantloop in plantloops:
        supplyinlet = plantloop[1]
        supplyoutlet = plantloop[2]
        demandinlet = plantloop[4]
        demandoutlet = plantloop[5]
        # edges = [supplyoutlet -> demandinlet, demandoutlet -> supplyinlet]
        moreedges = [(supplyoutlet, demandinlet), (demandoutlet, supplyinlet)]
        edges = edges + moreedges
    
    g=pydot.graph_from_edges(edges, directed=True) 
    return g



# iddfile = "../iddfiles/Energy+V6_0.idd"
# fname = "../idffiles/Suite_RADIANT_AIR.idf"
# g = makeplantloop(iddfile, fname)
# g.write('Suite_RADIANT_AIR.dot')
# g.write_png('Suite_RADIANT_AIR.png')


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
        print "make main loop"
        g = makeplantloop(iddfile, fname)
        g.write('%s.dot' % (os.path.splitext(fname)[0]))
        g.write_png('%s.png' % (os.path.splitext(fname)[0]))
        print "diagram each branch. "
        makesavebranchdiagrams(fname, iddfile)
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
