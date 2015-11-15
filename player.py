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

    def update(self, controls, dt):

        accel=self._get_accel_vector(controls)
        
        if accel is None:
            accel=self._get_decel_vector()

        if accel is not None:
            self.delta_velocity.set_magnitude(0.0)
            self.delta_velocity.add(accel)
            self.delta_velocity.multiply(dt)
            
            if (accel is self.decelerate and 
                self.velocity.length_squared() < self.delta_velocity.length_squared()):
                self.velocity.set_magnitude(0.0)
            else:
                self.velocity.add(self.delta_velocity)

        self.velocity.limit_length(self.max_speed)

        self.delta_position.set_magnitude(0.0)
        self.delta_position.add(self.velocity)
        self.delta_position.multiply(dt)

        self.delta_x_vector.x=self.delta_position.x
        self.delta_y_vector.y=self.delta_position.y

    def _get_accel_vector( self, controls ):
        if controls.up:
            if controls.left:
                return self.accelerate_upper_left
            elif controls.right:
                return self.accelerate_upper_right
            else:
                return self.accelerate_up
        elif controls.down:
            if controls.left:
                return self.accelerate_lower_left
            elif controls.right:
                return self.accelerate_lower_right
            else:
                return self.accelerate_down
        elif controls.left:
            return self.accelerate_left
        elif controls.right:
            return self.accelerate_right
        else:
            return None
            
    def _get_decel_vector( self ):
        if self.velocity.is_non_zero():
            self.decelerate.x=-self.velocity.x
            self.decelerate.y=-self.velocity.y
            self.decelerate.set_magnitude( self.deceleration )
            return self.decelerate
        else:
            return None
                
                

    
                                      
        
