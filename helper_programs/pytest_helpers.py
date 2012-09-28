"""helpers for pytest"""
def almostequal(first, second, places=7, printit=True):
    """docstring for almostequal"""
    if round(abs(second-first), places) != 0:
        if printit:
            print "notalmost: %s != %s" % (first, second)
        return False
    else:
        return True