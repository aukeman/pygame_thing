"""
Pygame base template for opening a window
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
Explanation video: http://youtu.be/vRB_983kUMc
"""
import pygame,math
from animation import Animation
from controls import Controls
from image import Image
from collision import rectangles_overlap, distance_until_rectangles_intersect
from point import Point
from rect import Rect

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
pygame.init()
# Set the width and height of the screen [width, height]
#size = pygame.display.list_modes()[0] #(3200, 1800)
size=(2400, 1350)

screen = pygame.display.set_mode(size, 0, 32)  #pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
screen.set_alpha(None)
pygame.display.set_caption("My Game")
# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

 # Select the font to use, size, bold, italics
font = pygame.font.SysFont(None, 15)

tiles=Image('tiles.png')

mario=Image('mario.png', color_key=(0,0,0), flags=Image.FLIPPED_BOTH)

surf=pygame.Surface((200, 150))

ortho_speed_pps=60.0
angle_speed_pps=ortho_speed_pps/math.sqrt(2.0)

coords=[10.0,10.0]

w=16
h=16
walking=Animation( Animation.Frame(100, [1*w, 0*h, w, h]),
                   Animation.Frame(100, [2*w, 0*h, w, h]),
                   Animation.Frame(100, [3*w, 0*h, w, h]) )
walking.activate()

standing=Animation( Animation.Frame(100, [0*w, 0*h, w, h]) )
standing.activate()

controls=Controls()

current_anim=standing
facing_right=True
blit_flags=Image.NONE

pos_x=64
pos_y=64
pos_z=0
bbox=Rect(pos_x+4,pos_y+8+1,8,6)

x_vector_bbox=Rect(bbox.x, bbox.y, bbox.width, bbox.height)
y_vector_bbox=Rect(bbox.x, bbox.y, bbox.width, bbox.height)

x_vector=Point(0,0)
y_vector=Point(0,0)
z_vector=0

tile_bbox=Rect(0,0,0,0)

# -------- Main Program Loop -----------
while not done:

    dt=clock.tick()/1000.0

    # --- Main event loop
    for event in pygame.event.get():
        if ((event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE) or
            event.type == pygame.QUIT):
            done = True

    keys=pygame.key.get_pressed()

    controls.update( left=keys[pygame.K_LEFT],
                     right=keys[pygame.K_RIGHT],
                     up=keys[pygame.K_UP],
                     down=keys[pygame.K_DOWN],
                     jump=keys[pygame.K_SPACE])

    if controls.diagonal:
        speed_pps=angle_speed_pps
    else:
        speed_pps=ortho_speed_pps

    dx=dy=speed_pps * dt

    if current_anim==standing and (controls.left or 
                                   controls.right or 
                                   controls.up or 
                                   controls.down):
        current_anim=walking
        current_anim.activate()
    elif current_anim==walking and not (controls.left or 
                                        controls.right or 
                                        controls.up or 
                                        controls.down):
        current_anim=standing
        current_anim.activate()


    if facing_right and controls.left:
        facing_right=False
        blit_flags=Image.FLIPPED_H
    elif not facing_right and controls.right:
        facing_right=True
        blit_flags=Image.NONE

    if controls.jump and pos_z == 0:
        z_vector=-75.0
    elif pos_z < 0:
        z_vector += 100.0*dt
    else:
        z_vector=0
        pos_z=0
        
    if controls.left:
        x_vector.x = -dx
    elif controls.right:
        x_vector.x = dx
    else:
        x_vector.x = 0
    
    if controls.up:
        y_vector.y = -dy
    elif controls.down:
        y_vector.y = dy
    else:
        y_vector.y = 0

    bbox.x=pos_x+4
    bbox.y=pos_y+8+1

    if x_vector.x < 0:
        x_vector_bbox.x = bbox.x-1
        x_vector_bbox.width=bbox.width+1
    elif 0 < x_vector.x:
        x_vector_bbox.x = bbox.x
        x_vector_bbox.width = bbox.width+1
    else:
        x_vector_bbox.x = bbox.x
        x_vector_bbox.width=bbox.width

    if y_vector.y < 0:
        y_vector_bbox.y = bbox.y-1
        y_vector_bbox.height=bbox.height+1
    elif 0 < y_vector.y:
        y_vector_bbox.y = bbox.y
        y_vector_bbox.height=bbox.height+1
    else:
        y_vector_bbox.y = bbox.y
        y_vector_bbox.height=bbox.height

    # --- Game logic should go here
    # --- Drawing code should go here
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
#    surf.fill(RED)

    overlap=False
    
    for i in range(0, 13):
        for j in range(0,10):
            if i == 0 or i == 12 or j == 0 or j == 9:
                tiles.blit([0,0,16,16], i*16, j*16, surf)

                tile_bbox.__init__(i*16, j*16, 16, 16)

                distance_x=distance_until_rectangles_intersect(x_vector_bbox,x_vector,tile_bbox)
                if distance_x is not None:
                    if x_vector.x < 0:
                        x_vector.x = -distance_x
                    else:
                        x_vector.x=distance_x

                distance_y=distance_until_rectangles_intersect(y_vector_bbox,y_vector,tile_bbox)
                if distance_y is not None:
                    if y_vector.y < 0:
                        y_vector.y=-distance_y
                    else:
                        y_vector.y=distance_y

            else:
                tiles.blit([16,0,16,16], i*16, j*16, surf)

    pos_x += x_vector.x
    pos_y += y_vector.y
    pos_z += z_vector*dt

    mario.blit(current_anim.get_frame(), pos_x, pos_y+pos_z, surf, blit_flags)

    pygame.transform.scale(surf, size, screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()


