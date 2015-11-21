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
from player import Player

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
shadow=Image('shadow.png', color_key=(255,0,255))

surf=pygame.Surface((200, 150))


w=16
h=16

controls=Controls()

pos_z=0

tile_bbox=Rect(0,0,0,0)

player=Player(x=64, y=64, 
              sprite_sheet='mario.png',
              animations={
                  Player.WALKING: Animation( Animation.Frame(100, [1*w, 0*h, w, h]),
                                             Animation.Frame(100, [2*w, 0*h, w, h]),
                                             Animation.Frame(100, [3*w, 0*h, w, h]) ),
                  Player.STANDING: Animation( Animation.Frame(100, [0*w, 0*h, w, h]) ),
                  Player.JUMPING: Animation( Animation.Frame(100, [4*w, 0*h, w, h]) ) } )
            
bbox=Rect(player.position.x+4,player.position.y+8+1,8,6)

x_vector_bbox=Rect(bbox.x, bbox.y, bbox.width, bbox.height)
y_vector_bbox=Rect(bbox.x, bbox.y, bbox.width, bbox.height)

z_vector=0

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

    if controls.jump and pos_z == 0:
        z_vector=-75.0
    elif pos_z < 0:
        z_vector += 100.0*dt
    else:
        z_vector=0
        pos_z=0
        
    player.update( controls, dt )

    bbox.x=player.position.x+4
    bbox.y=player.position.y+8+1

    if player.delta_x_vector.x < 0:
        x_vector_bbox.x = bbox.x-1
        x_vector_bbox.width=bbox.width+1
    elif 0 < player.delta_x_vector.x:
        x_vector_bbox.x = bbox.x
        x_vector_bbox.width = bbox.width+1
    else:
        x_vector_bbox.x = bbox.x
        x_vector_bbox.width=bbox.width

    if player.delta_y_vector.y < 0:
        y_vector_bbox.y = bbox.y-1
        y_vector_bbox.height=bbox.height+1
    elif 0 < player.delta_y_vector.y:
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

    for i in range(0, 13):
        for j in range(0,10):
            if i == 0 or i == 12 or j == 0 or j == 9:
                tiles.blit([0,0,16,16], i*16, j*16, surf)

                tile_bbox.__init__(i*16, j*16, 16, 16)

                distance_x=distance_until_rectangles_intersect(x_vector_bbox,player.delta_x_vector,tile_bbox)
                if distance_x is not None:
                    if player.delta_x_vector.x < 0:
                        player.delta_position.x = -distance_x
                    else:
                        player.delta_position.x = distance_x

                distance_y=distance_until_rectangles_intersect(y_vector_bbox,player.delta_y_vector,tile_bbox)
                if distance_y is not None:
                    if player.delta_y_vector.y < 0:
                        player.delta_position.y=-distance_y
                    else:
                        player.delta_position.y=distance_y

            else:
                tiles.blit([16,0,16,16], i*16, j*16, surf)

    player.position.add(player.delta_position)

    pos_z += z_vector*dt

    shadow.blit((0,0,16,8), player.position.x, player.position.y+12, surf)

    player.draw(surf)

    # mario.blit(current_anim.get_frame(), player.position.x, player.position.y+pos_z, surf, blit_flags)

    pygame.transform.scale(surf, size, screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()


