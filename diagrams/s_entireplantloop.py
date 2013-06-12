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

"""build the topology of the plant loop, and generate an idf for it."""
import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf

from EPlusCode.EPlusInterfaceFunctions import parse_idd
from EPlusCode.EPlusInterfaceFunctions import eplusdata

iddfile = "../iddfiles/Energy+V6_0.idd"
block,commlst,commdct=parse_idd.extractidddata(iddfile)
theidd=eplusdata.idd(block,2)


fname = "../idffiles/blank.idf"
data, commdct = readidf.readdatacommdct(fname, iddfile=theidd,
                            commdct=commdct)
import eplus_functions
import idd_fields



# TODO : unit testing for classes
class HalfLoop(object):
    """hold the data for the half loop (demand or supply)"""
    def __init__(self, txt, side="supply", loopname="ALoop"):
        self.txt = txt
        self.side = side
        self.loopname = loopname
        self.makevars(txt)
        # - init non-diagram vars (organizational)
        self.plantinlet = "%s_%s_inlet" % (loopname, side)
        self.plantoutlet = "%s_%s_outlet" % (loopname, side)
        self.branchlistN = "%s_%s_Blist" % (loopname, side)
        self.connectorlistN = "%s_%s_Clist" % (loopname, side)
        
        
    def makevars(self, txt):
        """make the input variables of the loop"""
        lines = txt.strip().splitlines()
        # -
        items = [item.strip() for item in lines[0].split('->')]
        self.firstbranch, self.thesplitter, outbranches = items
        self.outbranches = [item.strip() for item in outbranches.split(',')]
        # -
        items = [item.strip() for item in lines[1].split('->')]
        inbranches, self.themixer, self.lastbranch  = items
        self.inbranches = [item.strip() for item in inbranches.split(',')]
        


# This also has a plantloop
# Org -> shows the organization. Not needed to draw loop. E+ may need

# Below is org stuff (later comes the diagram stuff)
# plantloop: inlet, outlet, (branchlistN, connectorlistN -> Org)
# branchlist: branchN1, branchN2, branchN3 -> Org
# connectorlist: splitterN, mixerN -> Org
# code the org stuff first. 

def makeplantloop(data, commdct, sloop, dloop, loopname):
    """make the plantloop"""
    # - 
    def indx(objkey, fielddesc):
        return eplus_functions.getfieldindex(data, commdct, objkey, fielddesc)
    # -     
    objkey = "plantloop".upper()
    objname = loopname
    plantloop = eplus_functions.makeanobject(data, theidd, commdct, objkey,
                                                                objname)
    # add the fields.
    fields = idd_fields.PlantLoop()
    plantloop[indx(objkey, fields.plantinlet)] = sloop.plantinlet
    plantloop[indx(objkey, fields.plantoutlet)] = sloop.plantoutlet
    plantloop[indx(objkey, fields.demandinlet)] = dloop.plantinlet
    plantloop[indx(objkey, fields.demandoutlet)] = dloop.plantoutlet
    plantloop[indx(objkey, fields.plantbranchlist)] = sloop.branchlistN
    plantloop[indx(objkey, fields.plantconnectorlist)] = sloop.connectorlistN
    plantloop[indx(objkey, fields.demandbranchlist)] = dloop.branchlistN
    plantloop[indx(objkey, fields.demandconnectorlist)] = dloop.connectorlistN
    # append the object
    data.dt[objkey].append(plantloop)


def makebranchlist(data, commdct, aloop):
    """make the baranchlists"""
    # - 
    def indx(objkey, fielddesc):
        return eplus_functions.getfieldindex(data, commdct, objkey, fielddesc)
    # - 
    # branchlist
    objkey = "branchlist".upper()
    objname = aloop.branchlistN
    branchlist = eplus_functions.makeanobject(data, theidd, commdct, objkey,
                                                                objname)
    # add branches to branch list
    fields = idd_fields.BranchList()
    ix = eplus_functions.getextensibleposition(data, commdct, objkey)
    extlength = eplus_functions.getextensiblesize(data, commdct, objkey)
    for i in range(extlength):
        branchlist.pop(-1)
    zlist = zip(range(ix, ix + len(aloop.outbranches)), aloop.outbranches)
    for i, branch in zlist:
        branchlist.append(branch)
    # append the object
    data.dt[objkey].append(branchlist)
    


def makeconnectorlist(data, commdct, aloop):
    """docstring for makeconnectorlist"""
    # - 
    def indx(objkey, fielddesc):
        return eplus_functions.getfieldindex(data, commdct, objkey, fielddesc)
    # - 
    # connectorlist
    objkey = "ConnectorList".upper()
    objname = aloop.connectorlistN
    connectorlist = eplus_functions.makeanobject(data, theidd, commdct,
                                                            objkey, objname)
    # add connectors to connectorlist
    fields = idd_fields.ConnectorList()
    connectorlist[indx(objkey, fields.connectortype1)] = fields.splitter
    connectorlist[indx(objkey, fields.connector1)] = aloop.thesplitter
    connectorlist[indx(objkey, fields.connectortype2)] = fields.mixer
    connectorlist[indx(objkey, fields.connector2)] = aloop.themixer
    # append the object
    data.dt[objkey].append(connectorlist)
    

# Non Org stuff -> necessary for diagram
# ------
# make branches
def pipebranch(branchname):
    """make a pipebranch"""
    # - 
    def indx(objkey, fielddesc):
        return eplus_functions.getfieldindex(data, commdct, objkey, fielddesc)
    # - 
    objkey = "branch".upper()
    objname = branchname
    branch = eplus_functions.makeanobject(data, theidd, commdct, objkey,
                                                                objname)
    # put a pipe object
    fields = idd_fields.Branch()
    branch[indx(objkey, fields.componenttype1)] = "Pipe:Adiabatic"
    pipename = "%s_%s" % (objname, "pipe")
    branch[indx(objkey, fields.component1)] = pipename
    branch[indx(objkey, fields.inlet1)] = "%s_%s" % (pipename, "inlet")
    branch[indx(objkey, fields.outlet1)] = "%s_%s" % (pipename, "outlet")
    branch[indx(objkey, fields.controltype1)] = fields.bypass
    return branch
    
def makebranches(data, commdct, aloop):
    """make the branches for the loop"""
    # - 
    def indx(objkey, fielddesc):
        return eplus_functions.getfieldindex(data, commdct, objkey, fielddesc)
    # - 
    objkey = "branch".upper()
    branch = pipebranch(aloop.firstbranch)
    data.dt[objkey].append(branch)
    for branchname in aloop.outbranches:
        branch = pipebranch(branchname)
        data.dt[objkey].append(branch)
    branch = pipebranch(aloop.lastbranch)
    data.dt[objkey].append(branch)
    


def makesplitter(data, commdct, aloop):
    """make a splitter for the loop"""
    # - 
    def indx(objkey, fielddesc):
        return eplus_functions.getfieldindex(data, commdct, objkey, fielddesc)
    # - 
    # make splitter
    objkey = "Connector:Splitter".upper()
    objname = aloop.thesplitter
    splitter = eplus_functions.makeanobject(data, theidd, commdct, objkey,
                                                                objname)
    # add nodes to splitter
    fields = idd_fields.Connector_Splitter()
    splitter[indx(objkey, fields.inlet)] = aloop.firstbranch
    splitter[indx(objkey, fields.firstoutlet)] = aloop.outbranches[0]
    for branchname in aloop.outbranches[1:]:
        splitter.append(branchname)
    # append the object
    data.dt[objkey].append(splitter)
    

def makemixer(data, commdct, aloop):
    """make the mixer for the loop"""
    # - 
    def indx(objkey, fielddesc):
        return eplus_functions.getfieldindex(data, commdct, objkey, fielddesc)
    # - 
    # make mixer
    objkey = "Connector:Mixer".upper()
    objname = aloop.themixer
    mixer = eplus_functions.makeanobject(data, theidd, commdct, objkey,
                                                                objname)
    # add nodes to mixer
    fields = idd_fields.Connector_Mixer()
    mixer[indx(objkey, fields.outlet)] = aloop.lastbranch
    mixer[indx(objkey, fields.firstinlet)] = aloop.inbranches[0]
    for branchname in aloop.inbranches[1:]:
        mixer.append(branchname)
    # append the object
    data.dt[objkey].append(mixer)
    
def rename_endnodes(data, commdct, aloop):
    """rename firstbranch inlet to plantinlet
    rename lastbranch outlet to plantoutlet"""
    # - 
    def indx(objkey, fielddesc):
        return eplus_functions.getfieldindex(data, commdct, objkey, fielddesc)
    # - 
    # rename firstbranch inlet to plantinlet
    objkey = "branch".upper()
    objname = aloop.firstbranch
    namefield = idd_fields.ObjectName.name
    firstbranchobj = eplus_functions.getobject(data, commdct, objkey,
                                                                    objname)
    fields = idd_fields.Branch()
    firstbranchobj[indx(objkey, fields.inlet1)] = aloop.plantinlet
    # rename lastbranch outlet to plantoutlet
    objkey = "branch".upper()
    objname = aloop.lastbranch
    namefield = idd_fields.ObjectName.name
    lastbranchobj = eplus_functions.getobject(data, commdct, objkey,
                                                                    objname)
    fields = idd_fields.Branch()
    outlet1_index = indx(objkey, fields.outlet1)
    extsize = eplus_functions.getextensiblesize(data, commdct, objkey)
    extbegin = eplus_functions.getextensibleposition(data, commdct, objkey)
    lastoutletpos = outlet1_index - extbegin - extsize # index in reverse
    lastbranchobj[lastoutletpos] = aloop.plantoutlet
    
def makeentireplantloop(data, commdct, sloop, dloop, loopname=None):
    """make the entire plantloop"""
    if not loopname:
        loopname = sloop.loopname
    makeplantloop(data, commdct, sloop, dloop, loopname)
    makebranchlist(data, commdct, sloop)    
    makebranchlist(data, commdct, dloop)    
    makeconnectorlist(data, commdct, sloop)    
    makeconnectorlist(data, commdct, dloop)    
    makebranches(data, commdct, sloop)
    makebranches(data, commdct, dloop)
    makesplitter(data, commdct, sloop)    
    makesplitter(data, commdct, dloop)    
    makemixer(data, commdct, sloop)    
    makemixer(data, commdct, dloop)
    rename_endnodes(data, commdct, sloop)
    rename_endnodes(data, commdct, dloop)

loopsupplystr = """
branchname0 -> splitter -> branchname1, branchname2, branchname3
branchname1, branchname2, branchname3 -> mixer -> branchname4
"""

loopdemandstr = """
dbranchname0 -> dsplitter -> dbranchname1, dbranchname2, dbranchname3
dbranchname1, dbranchname2, dbranchname3 -> dmixer -> dbranchname4
"""
sloop = HalfLoop(loopsupplystr, "supply", loopname="plantloop")
dloop = HalfLoop(loopdemandstr, "demand", loopname='plantloop')
makeentireplantloop(data, commdct, sloop, dloop, loopname='plantloop')

txt = `data`
idd = eplus_functions.Idd(commdct, commlst, theidd)
idfw = eplus_functions.IdfWrapper(data, idd)
txt = `idfw`
print txt,


