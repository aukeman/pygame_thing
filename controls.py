class Controls:

    def __init__(self):
        self.update()

    def update(self, **kwargs):
        self.left=kwargs.get('left', False)
        self.right=kwargs.get('right', False)
        self.up=kwargs.get('up', False)
        self.down=kwargs.get('down', False)
        self.jump=kwargs.get('jump', False)
        self.diagonal=(self.left or self.right) and (self.up or self.down)
        
