import pygame

rect_buffer=[pygame.Rect(0,0,0,0) for i in range(0,10)]

def rectangles_overlap( a, b ):
    local_a=rect_buffer[0]
    local_b=rect_buffer[1]

    _copy_and_normalize_rect(a, local_a)
    _copy_and_normalize_rect(b, local_b)

    return (local_a.x <= (local_b.x + local_b.width) and
            local_b.x <= (local_a.x + local_a.width) and
            local_a.y <= (local_b.y + local_b.height) and
            local_b.y <= (local_a.y + local_a.height))


def _copy_and_normalize_rect( src, dest ):
    _copy_rect( src, dest )

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
    
    
