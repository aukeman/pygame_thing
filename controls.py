class Controls:

    def __init__(self):
        self.left=False
        self.right=False
        self.up=False
        self.down=False
        self.jump=False

        self.update()

    def update(self, **kwargs):
        self._previous_left=self.left
        self._previous_right=self.right
        self._previous_up=self.up
        self._previous_down=self.down
        self._previous_jump=self.jump

        self.left=kwargs.get('left', False)
        self.right=kwargs.get('right', False)
        self.up=kwargs.get('up', False)
        self.down=kwargs.get('down', False)
        self.jump=kwargs.get('jump', False)

        self.left_pressed=(self.left and not self._previous_left)
        self.right_pressed=(self.right and not self._previous_right)
        self.up_pressed=(self.up and not self._previous_up)
        self.right_pressed=(self.right and not self._previous_right)
        self.jump_pressed=(self.jump and not self._previous_jump)

        self.left_released=(not self.left and self._previous_left)
        self.right_released=(not self.right and self._previous_right)
        self.up_released=(not self.up and self._previous_up)
        self.right_released=(not self.right and self._previous_right)
        self.jump_released=(not self.jump and self._previous_jump)

        self.diagonal=(self.left or self.right) and (self.up or self.down)
        self.moving=(self.left or self.right or self.up or self.down)
        
