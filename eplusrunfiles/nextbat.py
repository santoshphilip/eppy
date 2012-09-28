"""read first line from runlist.tmp
make a batch file with it, 
delete that line and save runlist.tmp
-
if line is:
    dosomething abc | dosomethingelse xyz
the batch file is:
    dosomething abc
    dosomethingelse xyz"""
    
fname = "runlist.tmp"
batname = 'meplus_main.bat'
txt = open(fname, 'r').read()
lines = txt.splitlines()
try:
    first = lines.pop(0)
    open(fname, 'w').write('\n'.join(lines))

    firstlines = first.split('|')
    firstlines = [line.strip() for line in firstlines]
    open(batname, 'w').write('\n'.join(firstlines))
except IndexError, e:
    open(batname, 'w').write('REM ====== task complete ========')
