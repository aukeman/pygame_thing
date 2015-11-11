class Line:
    
    def __init__(self, x1,y1, x2, y2):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2

    def __getitem__(self, index):
        if index == 0:
            return self.x1
        elif index == 1:
            return self.y1
        elif index == 2:
            return self.x2
        elif index == 3:
            return self.y2
        else:
            return None
            
    def set(self, x1, y1, x2, y2):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2

    def slope(self):
        if self.x2 == self.x1:
            return None
        else:
            return float(self.y2 - self.y1) / float(self.x2 - self.x1);
