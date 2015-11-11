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
            y_intercept=line.y2 - slope*line.x2
            y_at_point_x = slope*point.x + y_intercept;

            result = (math.fabs(y_at_point_x - point.y) < 0.01);

    return result


def line_intersects_line(a, b, intersection):
    result=False

    _clear_point(intersection)

    slope_a=a.slope()
    slope_b=b.slope()

    if slope_a is None and slope_b is None:
        # a and b are both vertical
        result=_parallel_line_collision(a,b,intersection)
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

        if result and intersection is not None:
            intersection.x=b.x1
            intersection.y=y_at_intercept

    elif math.fabs(slope_a-slope_b) < 0.0001:
        result=_parallel_line_collision(a,b,intersection)
    else:
        x_at_intercept = ((a.y2-slope_a*a.x2)-(b.y2-slope_b*b.x2))/(slope_b-slope_a)

        x_on_line_a = ((a.x1 <= x_at_intercept and x_at_intercept <= a.x2) or
                       (a.x2 <= x_at_intercept and x_at_intercept <= a.x1))

        x_on_line_b = ((b.x1 <= x_at_intercept and x_at_intercept <= b.x2) or
                       (b.x2 <= x_at_intercept and x_at_intercept <= b.x1))

        result = ( x_on_line_a and x_on_line_b )

        if result and intersection is not None:
            y_at_intercept = slope_a * x_at_intercept + (a.y2-slope_a*a.x2)
	
            intersection.x = x_at_intercept;
            intersection.y = y_at_intercept;

    return result

def line_intersects_rectangle(line, rect, intersection):
    result=False

    line_bbox=rect_buffer[0]
    line_bbox.x=line.x1
    line_bbox.y=line.y1
    line_bbox.width=line.x2-line.x1
    line_bbox.height=line.y2-line.y1

    _clear_point(intersection)
        
    if rectangles_overlap(rect, line_bbox):
        side_1=line_buffer[0]
        side_1.x1=rect[0]+rect[2]
        side_1.y1=rect[1]
        side_1.x2=rect[0]
        side_1.y2=rect[1]

        side_2=line_buffer[1]
        side_2.x1=rect[0]+rect[2] 
        side_2.y1=rect[1]
        side_2.x2=rect[0]+rect[2]
        side_2.y2=rect[1]+rect[3]

        side_3=line_buffer[2]
        side_3.x1=rect[0]
        side_3.y1=rect[1]+rect[3]
        side_3.x2=rect[0]+rect[2]
        side_3.y2=rect[1]+rect[3]

        side_4=line_buffer[3]
        side_4.x1=rect[0]
        side_4.y1=rect[1]+rect[3]
        side_4.x2=rect[0]
        side_4.y2=rect[1]

        current_intersection=point_buffer[0]
        _clear_point(current_intersection)

        line_x=line.x2-line.x1
        line_y=line.y2-line.y1

        side_idx=0
        while side_idx<4:
            side=line_buffer[side_idx]

            dot_product_line_with_side_normal=(line_x*(side.y2-side.y1) + 
                                               line_y*(side.x2-side.x1))

            if ((dot_product_line_with_side_normal < 0) and
                line_intersects_line(line, side, current_intersection)):
                result=True
                _copy_point(current_intersection, intersection)

            side_idx+=1

        if not result:
            origin=point_buffer[1]
            origin.x=line.x1
            origin.y=line.y1

            if point_in_rect(origin, rect):
                result=True
                _copy_point(origin, intersection)

    return result;
                
def distance_until_rectangles_intersect(a, a_motion, b):
    result=999999.9

    amx=a_motion[0]
    amy=a_motion[1]
    
    ax=a[0]
    ay=a[1]
    w=a[2]
    h=a[3]

    line_buffer[0].set( ax,   ay,   ax+amx,   ay+amy )
    line_buffer[1].set( ax+w, ay,   ax+w+amx, ay+amy )
    line_buffer[2].set( ax,   ay+h, ax+amx,   ay+h+amy )
    line_buffer[3].set( ax+w, ay+h, ax+w+amx, ay+h+amy )
    
    collision_point=point_buffer[0]
    _clear_point(collision_point)

    idx=0
    while idx < 4:
        if line_intersects_rectangle(line_buffer[idx], b, collision_point):
            point_buffer[1].set(line_buffer[idx].x1, line_buffer[idx].y1)
            d_sqrd=point_buffer[1].distance_squared(collision_point)
            if d_sqrd < result:
                result = d_sqrd
        idx+=1

    if result < 999999.9:
        return math.sqrt(result)
    else:
        return None

def _parallel_line_collision(a, b, intersection):
    a1=point_buffer[0]
    a1.x = a.x1
    a1.y = a.y1
  
    result = False

    if point_on_line( a1, b ):
        result = True
        _copy_point(a1, intersection)
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
            if a1.distance_squared(b1) < a1.distance_squared(b2):
                _copy_point(b1, intersection)
            else:
                _copy_point(b2, intersection)

        elif b1_on_a:
            result=True
            _copy_point(b1, intersection)

        elif b2_on_a:
            result=True
            _copy_point(b2, intersection)

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
    

def _copy_point(src, dest):
    if dest is not None:
        dest[0]=src[0]
        dest[1]=src[1]
                
def _clear_point(p):
    if p is not None:
        p[0]=0
        p[1]=0


