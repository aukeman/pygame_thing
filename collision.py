import pygame
import math
from line import Line
from point import Point
from object_pool import ObjectPool

rect_pool=ObjectPool(100,pygame.Rect,0,0,0,0)
line_pool=ObjectPool(100,Line,0,0,0,0)
point_pool=ObjectPool(100,Point,0,0)

def rectangles_overlap( a, b ):
    local_a=rect_pool(0,0,0,0)
    local_b=rect_pool(0,0,0,0)

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

def point_in_rect(point, rect):
    return (rect.x <= point.x <= rect.x+rect.width and
            rect.y <= point.y <= rect.y+rect.height)

def line_intersects_line(a, b, intersection=None):
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

def line_intersects_rectangle(line, rect, intersection=None):
    result=False

    line_bbox=rect_pool(line.x1,line.y1,line.x2-line.x1,line.y2-line.y1)

    _clear_point(intersection)
        
    if rectangles_overlap(rect, line_bbox):
        side_1=line_pool(rect.x+rect.width, rect.y, rect.x, rect.y)
        side_2=line_pool(rect.x+rect.width, rect.y, rect.x+rect.width, rect.y+rect.height)
        side_3=line_pool(rect.x, rect.y+rect.height, rect.x+rect.width, rect.y+rect.height)
        side_4=line_pool(rect.x, rect.y+rect.height, rect.x, rect.y)

        current_intersection=point_pool(0,0)
        _clear_point(current_intersection)

        v=point_pool(line.x2-line.x1, line.y2-line.y1)

        if _line_intersects_side(line, side_1, current_intersection):
            result=True
            _copy_point(current_intersection, intersection)

        if _line_intersects_side(line, side_2, current_intersection):
            result=True
            _copy_point(current_intersection, intersection)
            
        if _line_intersects_side(line, side_3, current_intersection):
            result=True
            _copy_point(current_intersection, intersection)
            
        if _line_intersects_side(line, side_4, current_intersection):
            result=True
            _copy_point(current_intersection, intersection)

        if not result:
            origin=point_pool(line.x1,line.y1)

            if point_in_rect(origin, rect):
                result=True
                _copy_point(origin, intersection)

    return result;
   
def _line_intersects_side(line, side, intersection=None):
    dot_product_line_with_side_normal=((line.x2-line.x1)*(side.y2-side.y1) + 
                                       (line.y2-line.y1)*(side.x2-side.x1))

    return ((dot_product_line_with_side_normal < 0) and
            line_intersects_line(line, side, intersection))
        
             
def distance_until_rectangles_intersect(a, a_motion, b):
    result=999999.9

    amx=a_motion.x
    amy=a_motion.y
    
    ax=a.x
    ay=a.y
    w=a.width
    h=a.height

    corner1=line_pool( ax,   ay,   ax+amx,   ay+amy )
    corner2=line_pool( ax+w, ay,   ax+w+amx, ay+amy )
    corner3=line_pool( ax,   ay+h, ax+amx,   ay+h+amy )
    corner4=line_pool( ax+w, ay+h, ax+w+amx, ay+h+amy )
    
    collision_point=point_pool(0,0)

    if line_intersects_rectangle(corner1,b,collision_point):
        origin=point_pool(corner1.x1, corner1.y1)
        d_sqrd=origin.distance_squared(collision_point)
        if d_sqrd < result:
            result=d_sqrd

    if line_intersects_rectangle(corner2,b,collision_point):
        origin=point_pool(corner2.x1, corner2.y1)
        d_sqrd=origin.distance_squared(collision_point)
        if d_sqrd < result:
            result=d_sqrd

    if line_intersects_rectangle(corner3,b,collision_point):
        origin=point_pool(corner3.x1, corner3.y1)
        d_sqrd=origin.distance_squared(collision_point)
        if d_sqrd < result:
            result=d_sqrd

    if line_intersects_rectangle(corner4,b,collision_point):
        origin=point_pool(corner4.x1, corner4.y1)
        d_sqrd=origin.distance_squared(collision_point)
        if d_sqrd < result:
            result=d_sqrd

    if result < 999999.9:
        return math.sqrt( float(result) )
    else:
        return None

def _parallel_line_collision(a, b, intersection=None):
    a1=point_pool(a.x1, a.y1)
  
    result = False

    if point_on_line( a1, b ):
        result = True
        _copy_point(a1, intersection)
    else:
        b1=point_pool(b.x1, b.y1)
        b2=point_pool(b.x2, b.y2)

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
    dest.x=src.x
    dest.y=src.y
    dest.width=src.width
    dest.height=src.height
    

def _copy_point(src, dest):
    if dest is not None:
        dest.x=src.x
        dest.y=src.y
                
def _clear_point(p):
    if p is not None:
        p.x=0
        p.y=0


