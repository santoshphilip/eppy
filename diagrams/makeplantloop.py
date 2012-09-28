"""make plant loop"""

# build the following
# supplyinlet -> branchname0
# branchname0 -> splitter -> [branchname1, branchname2, branchname3]
# [branchname1, branchname2, branchname3] -> mixer -> branchname4
# branchname4 -> supplyoutlet


# supplyinlet -> branchname0 
# need code to build a new object.
# it should be in orig EPlusInterface
# need to find it. Althoough I dont thik it deals with extensible
# orig does not have an add node.
def newobj(objkey, objname):
    """docstring for newnode"""
    pass

# branchname0 -> splitter -> [branchname1, branchname2, branchname3]
# [branchname1, branchname2, branchname3] -> mixer -> branchname4
# branchname4 -> supplyoutlet
