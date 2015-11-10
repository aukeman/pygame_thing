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

    def set(self,x,y):
        self.x=x
        self.y=y

    def distance_squared(self, other):
        x_len=self.x-other.x
        y_len=self.y-other.y
        return x_len*x_len+y_len*y_len
