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
        self.retrive_from = retrive_from
    def __get__(self, instance, owner):
        return instance.__getattribute__(self.retrive_from)
    def __set__(self, instance, value):
        instance.__setattr__(self.retrive_from, value)
        
    
class BigClass(object):
    c = RetriceClass('b')    
    def __init__(self):
        self.b = 5
        
class Thing(object):
    def __init__(self):
        self.b = 5
        self.c = RetriceClass('b')


a = BigClass()
# a = Thing()
print a.__dict__['b']

class Fred(object):
    hair_color = 'brown'
                
                
                
class Rectangle:
    def __init__(self):
        self.width = 0
        self.height = 0
    def __setattr__(self, name, value):
        if name == 'size':
            self.width, self.height = value
        else:
            self.__dict__[name] = value
    def __getattr__(self, name):
        if name == 'size':
            return self.width, self.height
        else:
            raise AttributeError                
            
r = Rectangle()
print r.size
r.size = (5, 7)
print r.size
            