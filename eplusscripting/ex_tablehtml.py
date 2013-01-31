"""read the table html files"""

import readhtml
fname = "../outputfiles/V_7_2/5ZoneCAVtoVAVWarmestTempFlowTable_ABUPS.html"
txt = open(fname, 'r').read()
htables = readhtml.titletable(txt)
fname = "../outputfiles/V_7_2/5ZoneCAVtoVAVWarmestTempFlowTable.html"
txt = open(fname, 'r').read()
htables = readhtml.titletable(txt)
