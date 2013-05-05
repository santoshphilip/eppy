"""make plant loop snippets"""
import sys
sys.path.append('../')


# from idfreader import idfreader

# iddfile = "../../iddfiles/Energy+V6_0.idd"
# fname = "../../idffiles/V_6_0/5ZoneSupRetPlenRAB.idf"
#  
# bunchdt, data, commdct = idfreader(fname, iddfile)
# 
# outfilename = "afile.idf"
# txt = str(data)
# open(outfilename, 'w').write(txt)

from modeleditor import IDF1
IDF = IDF1

iddfile = "../../iddfiles/Energy+V6_0.idd"
IDF.setiddname(iddfile)

fname = "../../idffiles/V_6_0/5ZoneSupRetPlenRAB.idf"
idf1 = IDF(fname)

# print idf1
# idf1.idfobjects["VERSION"]


loopname, theloop = "p_loop",  ['b0', ['b1', 'b2'], 'b3']

newplantloop = idf1.newidfobject("PLANTLOOP", loopname)

fields = ['Plant Side Inlet Node Name',
'Plant Side Outlet Node Name',
'Plant Side Branch List Name',
'Plant Side Connector List Name',
'Demand Side Inlet Node Name',
'Demand Side Outlet Node Name',
'Demand Side Branch List Name',
'Demand Side Connector List Name']

# for use in bunch
flnames = [field.replace(' ', '_') for field in fields]

# implify naming
fields1 = [field.replace('Plant Side', 'Supply') for field in fields]
fields1 = [field.replace('Demand Side', 'Demand') for field in fields1]
fields1 = [field[:field.find('Name') - 1] for field in fields1]
fields1 = [field.replace(' Node', '') for field in fields1]
fields1 = [field.replace(' List', 's') for field in fields1]
# changesnames to 
# ['Supply Inlet',
#  'Supply Outlet',
#  'Supply Branchs',
#  'Supply Connectors',
#  'Demand Inlet',
#  'Demand Outlet',
#  'Demand Branchs',
#  'Demand Connectors']

# make fieldnames in the plant loop
fieldnames = ['%s %s' % (loopname, field) for field in fields1]
for fieldname, thefield in zip(fieldnames, flnames):
    newplantloop[thefield] = fieldname
    
# make the branch lists for this plant loop    
supplybranchlist = idf1.newidfobject("BRANCHLIST",
                newplantloop.Plant_Side_Branch_List_Name)
demandbranchlist = idf1.newidfobject("BRANCHLIST",
                newplantloop.Demand_Side_Branch_List_Name)
                