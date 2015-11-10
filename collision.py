import pygame
import math
from line import Line
from point import Point

rect_buffer=[pygame.Rect(0,0,0,0) for i in range(0,10)]
line_buffer=[Line(0,0,0,0) for i in range(0,10)]
point_buffer=[Point(0,0) for i in range(0,10)]


def rectangles_overlap( a, b ):
    local_a=rect_buffer[0]
    local_b=rect_buffer[1]

    _copy_and_normalize_rect(a, local_a)
    _copy_and_normalize_rect(b, local_b)

    return (local_a.x <= (local_b.x + local_b.width) and
            local_b.x <= (local_a.x + local_a.width) and
            local_a.y <= (local_b.y + local_b.height) and
            local_b.y <= (local_a.y + local_a.height))

def point_on_line( point, line ):
    result = False

    if ((line.x1 <= point.x and point.x <= line.x2) or
        (line.x2 <= point.x and point.x <= line.x1)):

        if line.y1 == line.y2 and point.y == line.y1:
            result = True

        elif line.x1 == line.x2 and point.x == line.x1:
            result = (( line.y1 <= point.y and point.y <= line.y2 ) or
                      ( line.y2 <= point.y and point.y <= line.y1 ))

        else:
            slope = line.slope()
            y_intercept=line.y - slope*line.x2
            y_at_point_x = slope*point.x + y_intercept;

            result = (math.fabs(y_at_point_x - point.y) < 0.01);

    return result


def line_intersects_line(a, b, intersection):
    result=False

    if intersection is not None:
        intersection[0]=0
        intersection[1]=0

    slope_a=a.slope()
    slope_b=b.slope()

    if slope_a is None and slope_b is None:
        # a and b are both vertical
        result=_parallel_line_collision(a,b)
    elif slope_a is None:
        # a is vertical
        result=line_intersects_line(b, a, intersection)
    elif slope_b is None:
        # b is vertical
        y_at_intercept = slope_a * b.x1 + (a.y2 - slope_a*a.x2)

        x_on_line_a = ((a.x1 <= b.x1 and b.x1 <= a.x2) or
                       (a.x2 <= b.x1 and b.x1 <= a.x1))
        
        y_on_line_b = ((b.y1 <= y_at_intercept and y_at_intercept <= b.y2) or
                       (b.y2 <= y_at_intercept and y_at_intercept <= b.y1))

        result = (x_on_line_a and y_on_line_b)

    elif math.fabs(slope_a, slope_b) < 0.0001:
        result=_parallel_line_collision(a,b)
    else:
        x_at_intercept = ((a.y2-slope_a*a.x2)-(b.y2-slope_b*b.x2))/(slope_b-slope_a)

        x_on_line_a = ((a.x1 <= x_at_intercept and x_at_intercept <= a.x2) or
                       (a.x2 <= x_at_intercept and x_at_intercept <= a.x1))

        x_on_line_b = ((b.x1 <= x_at_intercept and x_at_intercept <= b.x2) or
                       (b.x2 <= x_at_intercept and x_at_intercept <= b.x1))

        result = ( x_on_line_a and x_on_line_b )

        if intersection is not None:
            y_at_intercept = slope_a * x_at_intercept + (a.y2-slope_a*a.x2)
	
            intersection.x = x_at_intercept;
            intersection.y = y_at_intercept;

    return result

def _parallel_line_collision(a, b, intersection):
    a1=point_buffer[0]
    a1.x = a.x1
    a1.y = a.y1
  
    result = False

    if point_on_line( a1, b ):
        if intersection is not None:
            intersection.x=a1.x
            intersection.y=a1.y

        result = True
    else:
        b1=point_buffer[1]
        b2=point_buffer[2]

        b1.x=b.x1
        b1.y=b.y1

        b2.x=b.x2
        b2.y=b.y2

        b1_on_a = point_on_line(b1, a);
        b2_on_a = point_on_line(b2, a);

        if b1_on_a and b2_on_a:
            result=True

            if intersection is not None:
                distance_to_b1 = a1.distance_squared(b1)
                distance_to_b2 = a1.distance_squared(b2)

                if distance_to_b1 < distance_to_b2:
                    intersection.x=b1.x
                    intersection.y=b1.y
                else:
                    intersection.x=b2.x
                    intersection.y=b2.y

        elif b1_on_a:
            result=True
            
            if intersection is not None:
                intersection.x=b1.x
                intersection.y=b1.y

        elif b2_on_a:
            result=True

            if intersection is not None:
                intersection.x=b1.x
                intersection.y=b1.y

    return result

def _copy_and_normalize_rect( src, dest ):
    _copy_rect( src, dest )

    dest.normalize()

    if dest.width < 0:
        dest.x += dest.width
        dest.width = -dest.width
    
    if dest.height < 0:
        dest.y += dest.height
        dest.height = -dest.height


def _copy_rect( src, dest ):
    dest[0]=src[0]
    dest[1]=src[1]
    dest[2]=src[2]
    dest[3]=src[3]
    
    
