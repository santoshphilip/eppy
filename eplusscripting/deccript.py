"""Do some experiments with descriptors"""

# a.b = 5
# then a.c will get 5 from a.b
# a.c = 8
# then a.c will set a.b to 8


# ordered_dict
# collection module

class RetriceClass(object):
    def __init__(self, retrive_from):
        super(RetriceClass, self).__init__()
        self.retrive_from = (retrive_from, )
    def __get__(self, obj, objtype):
        # return "gumby"
        return self.retrive_from[0]
    def __set__(self, obj, val):
        self.retrive_from[0] = val
        
    
class BigClass(object):
    c = RetriceClass(15)    
    def __init__(self):
        self.b = 5
        d= RetriceClass(15)
        
a = BigClass()
        