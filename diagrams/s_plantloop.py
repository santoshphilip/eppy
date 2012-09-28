"""This will draw the plant loop for any file """
import pydot
import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf
import loops


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
# fname = "../idffiles/a.idf"
fname = "../idffiles/HVACTemplate-5ZonePackagedVAV_exp.idf" # for supply mixer 
fname = "a.idf"
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

# for edge in edges:
#     print edge    
g=pydot.graph_from_edges(edges, directed=True) 


g.write('a.dot')
g.write_png('a.png')