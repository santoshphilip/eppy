import ncommdct
from EPlusInterfaceFunctions import parse_idd

iddname = './Energy+.idd'
iddname = './a.idd'
txt = open(iddname, 'r').read()
commdct = ncommdct.getcommdct(txt)
commlst = ncommdct.getcommlst(txt)
(nocom,nocom1,block)=parse_idd.get_nocom_vars(txt)
block1,commlst1,commdct1=parse_idd.extractidddata(iddname)
print commlst[0][-4]
