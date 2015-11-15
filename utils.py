import math

def distance_squared(a, b):
    x_len=a.x-b.x
    y_len=a.y-b.y
    return x_len*x_len+y_len*y_len

def distance(a, b):
    return math.sqrt( distance_squared( a, b ) )

