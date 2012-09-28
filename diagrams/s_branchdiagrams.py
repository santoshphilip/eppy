"""makes all the branch diagrams in a folder"""

"""make a diagram of the components in a branch"""

import os
import glob
import pydot
import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf
import loops

import getopt


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
        # ====================        
        iddfile = "../iddfiles/Energy+V6_0.idd"
        fname = args[0]
        makesavebranchdiagrams(fname, iddfile)
        # ====================        
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
