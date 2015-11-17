from vector import Vector
from rect import Rect
from point import Point

class Player:
    
    def __init__(self, **kwargs ):
        self.max_speed=kwargs.get('max_speed', 60.0)
        self.acceleration=kwargs.get('acceleration', 60.0)
        self.deceleration=kwargs.get('deceleration', 60.0)
        self.jump_velocity=kwargs.get('jump_velocity', 100.0)
        self.gravity=kwargs.get('gravity', 50.0)

        self.position=Vector(kwargs.get('x', 0.0),
                             kwargs.get('y', 0.0))

        self.bbox=Rect(self.position.x+kwargs.get('bbox_x',0.0),
                       self.position.y+kwargs.get('bbox_y',0.0),
                       kwargs.get('bbox_width',16.0),
                       kwargs.get('bbox_height',16.0))
        
                       

        self.velocity=Vector(0.0,0.0)

        self.delta_x_vector=Vector(0.0, 0.0)
        self.delta_y_vector=Vector(0.0, 0.0)

        self.delta_position=Vector(0.0, 0.0)
        self.delta_velocity=Vector(0.0, 0.0)

        self.decelerate=Vector(1.0, 1.0, magnitude=self.deceleration)

        self.accelerate_left=Vector(-1.0, 0.0, magnitude=self.acceleration)
        self.accelerate_right=Vector(1.0, 0.0, magnitude=self.acceleration)
        self.accelerate_up=Vector(0.0, -1.0, magnitude=self.acceleration)
        self.accelerate_down=Vector(0.0, 1.0, magnitude=self.acceleration)

        self.accelerate_lower_left=Vector(-1.0, 1.0, magnitude=self.acceleration)
        self.accelerate_lower_right=Vector(1.0, 1.0, magnitude=self.acceleration)
        self.accelerate_upper_left=Vector(-1.0, -1.0, magnitude=self.acceleration)
        self.accelerate_upper_right=Vector(1.0, -1.0, magnitude=self.acceleration)

        self.x_accel_vector=Vector(0,0)
        self.y_accel_vector=Vector(0,0)

    def update(self, controls, dt):

        x_accel=self._get_x_accel_vector(controls)
        y_accel=self._get_y_accel_vector(controls)

        self.delta_velocity.set_magnitude(0.0)
        self.delta_velocity.add(x_accel)
        self.delta_velocity.add(y_accel)
        self.delta_velocity.multiply(dt)
        
        if ((0 < self.velocity.x and self.velocity.x + self.delta_velocity.x < 0) or
            (self.velocity.x < 0 and 0 < self.velocity.x + self.delta_velocity.x)):
            self.delta_velocity.x = -self.velocity.x

        if ((0 < self.velocity.y and self.velocity.y + self.delta_velocity.y < 0) or
            (self.velocity.y < 0 and 0 < self.velocity.y + self.delta_velocity.y)):
            self.delta_velocity.y = -self.velocity.y

            
        self.velocity.add(self.delta_velocity)
        self.velocity.limit_length(self.max_speed)

        self.delta_position.set_magnitude(0.0)
        self.delta_position.add(self.velocity)
        self.delta_position.multiply(dt)

        self.delta_x_vector.x=self.delta_position.x
        self.delta_y_vector.y=self.delta_position.y

    def _get_x_accel_vector( self, controls ):

        self.x_accel_vector.set_magnitude(0)

        if controls.up: 
            if controls.left: 
                self.x_accel_vector.x = self.accelerate_upper_left.x 
            elif controls.right:
                self.x_accel_vector.x = self.accelerate_upper_right.x

        elif controls.down: 
            if controls.left: 
                self.x_accel_vector.x = self.accelerate_lower_left.x 
            elif controls.right:
                self.x_accel_vector.x = self.accelerate_lower_right.x

        elif controls.left:
            self.x_accel_vector.x=self.accelerate_left.x 
        elif controls.right:
            self.x_accel_vector.x=self.accelerate_right.x

        elif self.velocity.x < 0:
            self.x_accel_vector.x=self.deceleration
        elif 0 < self.velocity.x:
            self.x_accel_vector.x=-self.deceleration

        return self.x_accel_vector

    def _get_y_accel_vector( self, controls ):

        self.y_accel_vector.set_magnitude(0)

        if controls.left: 
            if controls.up: 
                self.y_accel_vector.y = self.accelerate_upper_left.y 
            elif controls.down:
                self.y_accel_vector.y = self.accelerate_lower_left.y

        elif controls.right: 
            if controls.up: 
                self.y_accel_vector.y = self.accelerate_upper_right.y 
            elif controls.down:
                self.y_accel_vector.y = self.accelerate_lower_right.y

        elif controls.up:
            self.y_accel_vector.y=self.accelerate_up.y 
        elif controls.down:
            self.y_accel_vector.y=self.accelerate_down.y

        elif self.velocity.y < 0:
            self.y_accel_vector.y=self.deceleration
        elif 0 < self.velocity.y:
            self.y_accel_vector.y=-self.deceleration

        return self.y_accel_vector
            
    def _get_decel_vector( self ):
        if self.velocity.is_non_zero():
            self.decelerate.x=-self.velocity.x
            self.decelerate.y=-self.velocity.y
            self.decelerate.set_magnitude( self.deceleration )
            return self.decelerate
        else:
            return None
                
                

    
                                      
        
