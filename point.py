import utils

class Point:
    
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        else:
            return None

    def __setitem__(self, idx, value):
        if idx == 0:
            self.x=value
            return value
        elif idx == 1:
            self.y=value
            return value
        else:
            return None

    def set(self,x,y):
        self.x=x
        self.y=y

    def distance_squared(self, other):
        return utils.distance_squared(self, other)

    def distance(self,other):
        return utils.distance(self, other)

