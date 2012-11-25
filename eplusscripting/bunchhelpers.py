"""some helper files"""

from string import ascii_letters, digits

def makefieldname(namefromidd):
    """made a field name that can be used by bunch"""
    legalchar = ascii_letters + digits + ' '
    newname = ''.join([s for s in namefromidd[:] if s in legalchar])
    bunchname = newname.replace(' ', '_')
    return bunchname
    
