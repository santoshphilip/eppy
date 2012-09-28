"""Given a list of files, the script will track all the autosized values across files
It will put together a single file containing all the autosized values. The autosized values are
tagged as AUTO. If a field is autosized in one file and not autosized in other files, it's 
value is still pulled up. 
The results are output in a csv file.
The input data is hardcoded at the moment"""

from BeautifulSoup import BeautifulSoup
import autosized
import ncommdct
import mycsv
import table


iddname = './EPlusInterfaceFunctions/Energy+.idd'
path = '../../../30pctCD/PROPOSED/10_mech9_experiments/'
names = ['builtCAV_mech9prop_nomult', "builtCAV_mech9prop_nomult_1"]
outputcsv = 'b.csv'

txt = open(iddname, 'r').read()
commdct = ncommdct.getcommdct(txt)



# puts all the autosized key:values in autos as a list of auto
# puts all key:values in flattables as a list of flattable
autos = []
flattables = []
for i, name in enumerate(names):
    print name
    fname = '%s/%s.idf' % (path, name, )
    tablename = '%s/%sTable.html' % (path, name, )
    auto = autosized.getautosizeddcts(fname, tablename, commdct)
    autos.append(auto)
    #------
    txt = open(tablename, 'r').read()
    soup = BeautifulSoup(txt)
    head, body = table.getheadbody(soup)
    btabledct = table.gettitletabledct(body)
    flatbtable = table.flattenkey(btabledct)
    flattables.append(flatbtable)
    
    
# make master key list of autosized values from all files
allautos = {}    
for auto in autos:
    for key in auto.keys():
        allautos[key] = []
        

for key in allautos:
    for auto, flattable in zip(autos, flattables):
        if auto.has_key(key):
            allautos[key].append("AUTO")
        else:
            allautos[key].append('')
        if flattable.has_key(key):
            allautos[key].append(flattable[key])
        else:
            allautos[key].append('')
        
                
            

keys = allautos.keys()
keys.sort()

grid = []
for key in keys:
    row = []
    row = list(key) + allautos[key]
    grid.append(row)

dubnames = []
for name in names:
    dubnames.append('')
    dubnames.append(name)
header = ['','',''] + dubnames
grid  = [header] + grid
    
mycsv.writecsv(grid, outputcsv)    