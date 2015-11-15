import utils
import math
from point import Point

class Vector:

    _ORIGIN=Point(0,0)

    def __init__(self, x, y, **kwargs):
        self.x=x
        self.y=y
        
        if kwargs.get('magnitude') is not None:
            self.set_magnitude( kwargs['magnitude'] )

    def add(self, other):
        self.x += other.x
        self.y += other.y

    def subtract(self, other):
        self.x += other.x
        self.y += other.y

    def multiply(self, factor):
        self.x *= factor
        self.y *= factor

    def divide(self, divisor):
        self.x /= divisor
        self.y /= divisor

    def to_unit(self):
        if self.is_non_zero():
            self.divide( self.length() )

    def limit_length(self, limit):
        length_squared=self.length_squared()
        if limit*limit < length_squared:
            limit_factor=(limit/math.sqrt(length_squared))
            self.multiply(limit_factor)

    def set_magnitude(self, magnitude):
        if magnitude == 0.0:
            self.x=0.0
            self.y=0.0
        else:
            self.to_unit()
            self.multiply(magnitude)
            
    def is_zero(self):
        return (self.x == 0 and self.y == 0)

    def is_non_zero(self):
        return not self.is_zero()

    def length_squared(self):
        return utils.distance_squared(Vector._ORIGIN, self)

    def length(self):
        return utils.distance(Vector._ORIGIN, self)
        
