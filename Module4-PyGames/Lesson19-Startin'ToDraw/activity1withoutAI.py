import pygame


print(pygame.__file__)

#initialising pygame
pygame.init()

screen = pygame.display.set_mode((500,500))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill((0,0,255))
    pygame.draw.rect(screen, (123, 123, 123), (30, 40, 50, 60))

    pygame.display.flip()