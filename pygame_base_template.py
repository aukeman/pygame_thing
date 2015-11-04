"""
Pygame base template for opening a window
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
Explanation video: http://youtu.be/vRB_983kUMc
"""
import pygame
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
pygame.init()
# Set the width and height of the screen [width, height]
size = pygame.display.list_modes()[0] #(3200, 1800)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
#screen.set_alpha(None)
pygame.display.set_caption("My Game")
# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

coords = [0, 0, 199, 149]

 # Select the font to use, size, bold, italics
font = pygame.font.SysFont('', 25)

#tiles=pygame.image.load('tiles.png')

surf=pygame.Surface((200, 150))

# -------- Main Program Loop -----------
while not done:

    clock.tick()

    # --- Main event loop
    for event in pygame.event.get():
        if ((event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE) or
            event.type == pygame.QUIT):
            done = True

    # --- Game logic should go here
    # --- Drawing code should go here
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    surf.fill(RED)

    pygame.draw.rect(surf, WHITE, coords, 2)
    text = font.render('%.1f' % (clock.get_fps()), True, WHITE)
    surf.blit(text, [10, 10])

    pygame.transform.scale(surf, size, screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()



# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

print clock.get_fps()
