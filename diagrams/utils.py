"""utility function"""

def getiddversion(iddtxt):
    """return the version number of the iddfile"""
    verstr = "IDD_Version"
    lines = iddtxt.splitlines()
    firstline = lines[0]
    if firstline.find(verstr) == -1:
        return "version not known"
    else:
        return firstline.split(verstr)[-1].strip()