"""
Pygame base template for opening a window
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
Explanation video: http://youtu.be/vRB_983kUMc
"""
import pygame
from animation import Animation
from controls import Controls
from image import Image

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

speed_pps=60.0

coords=[10.0,10.0]

w=16
h=16
anim=Animation( Animation.Frame(100, [1*w, 0*h, w, h]),
                Animation.Frame(100, [2*w, 0*h, w, h]),
                Animation.Frame(100, [3*w, 0*h, w, h]) )
anim.activate()


controls=Controls()

# -------- Main Program Loop -----------
while not done:

    dt=clock.tick()/1000.0

    # --- Main event loop
    for event in pygame.event.get():
        if ((event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE) or
            event.type == pygame.QUIT):
            done = True

    keys=pygame.key.get_pressed()

    dx=dy=speed_pps * dt

    controls.update( left=keys[pygame.K_LEFT],
                     right=keys[pygame.K_RIGHT],
                     up=keys[pygame.K_UP],
                     down=keys[pygame.K_DOWN] )

    if controls.left:
        coords[0] -= dx
    elif controls.right:
        coords[0] += dx
    
    if controls.up:
        coords[1] -= dy
    elif controls.down:
        coords[1] += dy


    # --- Game logic should go here
    # --- Drawing code should go here
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
#    surf.fill(RED)
    
    for i in range(0, 13):
        for j in range(0,10):
            tiles.blit([0,0,16,16], i*16, j*16, surf)

    mario.blit(anim.get_frame(), coords[0], coords[1], surf)

    text = font.render('%05.1f % 8.6f % 5.3f' % (clock.get_fps(), dt, dx), False, WHITE)
    surf.blit(text, [10, 10])

    pygame.transform.scale(surf, size, screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()


