import pygame
import sys # System Y S

# Initialize pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rectangle Example")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Define rectangle properties
rect_x, rect_y = 200, 150
rect_width, rect_height = 400, 300

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    screen.fill(WHITE)

    # Draw rectangle
    pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
