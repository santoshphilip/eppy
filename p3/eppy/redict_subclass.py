
from eppy.bunch_subclass import EpBunch_5 as epb5
import re


# http://flo.nigsch.com/?p=82
# http://stackoverflow.com/questions/260056/hashtable-dictionary-map-lookup-with-regular-expressions/816047#816047
class redict(epb5):
    def __init__(self, d):
        dict.__init__(self, d)

    def __getitem__(self, regex):
        r = re.compile(regex)
        mkeys = list(filter(r.match, list(self.keys())))
        for i in mkeys:
                yield dict.__getitem__(self, i)
