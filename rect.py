class Rect:

    def __init__(self, x, y, width, height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height


    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.width
        elif index == 3:
            return self.height
        else:
            return None

    def set(self, x, y, width, height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height

    def normalize(self):
        if self.width < 0:
            self.width = -self.width
            self.x -= self.width

        if self.height < 0:
            self.height = -self.height
            self.y -= self.height


    
