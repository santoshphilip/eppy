"""some helper files"""

from string import ascii_letters, digits

def onlylegalchar(name):
    """return only legal chars"""
    legalchar = ascii_letters + digits + ' '
    return ''.join([s for s in name[:] if s in legalchar])

def makefieldname(namefromidd):
    """made a field name that can be used by bunch"""
    newname = onlylegalchar(namefromidd)
    bunchname = newname.replace(' ', '_')
    return bunchname
    
def intinlist(lst):
    """test if int in list"""
    for item in lst:
        try:
            item = int(item)
            return True
        except ValueError, e:
            pass
    return False
    
def replaceint(fname, replacewith='%s'):
    """replace int in lst"""
    words = fname.split()
    for i, word in enumerate(words):
        try:
            word = int(word)
            words[i] = '%s'
        except ValueError, e:
            pass
    return ' '.join(words)

