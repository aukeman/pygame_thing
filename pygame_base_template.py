"""
Pygame base template for opening a window
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
Explanation video: http://youtu.be/vRB_983kUMc
"""
import pygame
import time
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
pygame.init()
# Set the width and height of the screen [width, height]
#size = pygame.display.list_modes()[0] #(3200, 1800)
size=(1600, 900)

screen = pygame.display.set_mode(size) #, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
#screen.set_alpha(None)
pygame.display.set_caption("My Game")
# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

 # Select the font to use, size, bold, italics
font = pygame.font.SysFont('', 15)

tiles=pygame.image.load('tiles.png')
tiles=tiles.convert()
blur=tiles.copy()
blur.set_alpha(127)

surf=pygame.Surface((200, 150))

speed_pps=60.0

fcoords=[10.0, 10.0]
coords=[10,10]

t1=0
t2=0

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

    if keys[pygame.K_LEFT]:
        fcoords[0] -= dx
    elif keys[pygame.K_RIGHT]:
        fcoords[0] += dx
    
    if keys[pygame.K_UP]:
        fcoords[1] -= dy
    elif keys[pygame.K_DOWN]:
        fcoords[1] += dy


    # --- Game logic should go here
    # --- Drawing code should go here
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
#    surf.fill(RED)
    
    for i in range(0, 13):
        for j in range(0,10):
            surf.blit(tiles, [i*16,j*16], [0,0,16,16])

    surf.blit(blur, coords, [0,16,16,16])

    coords[0]=int(fcoords[0])
    coords[1]=int(fcoords[1])

    surf.blit(tiles, coords, [0,16,16,16])

    text = font.render('%5.1f %8.6f %5.3f' % (clock.get_fps(), dt, dx), False, WHITE)
    surf.blit(text, [10, 10])

    pygame.transform.scale(surf, size, screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()


