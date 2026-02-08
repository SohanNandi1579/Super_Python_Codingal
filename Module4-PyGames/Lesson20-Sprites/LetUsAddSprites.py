# Let Us Add Sprites
import pygame
import random

pygame.init()
sprite_colour_changing_colourful_bright_event_here = pygame.USEREVENT+1
background_colour_changing_colourful_bright_event_here = pygame.USEREVENT+2

#background colours:
red = pygame.Color('red')
orange = pygame.color('orange')
yellow = pygame.color(255, 118, 0)
royalblue = pygame.color("royalblue")
fluroscentgreen = pygame.color("fluroscentgreen")
peach = pygame.color("peach")

#sprite colours:
black = pygame.color("black")
lightblack = pygame.color("lightblack")
gray = pygame.color("grey")
darkwhite = pygame.color("darkwhite")
white = pygame.color("white")



import pygame
import random

pygame.init()

sprite_color_change_event=pygame.USEREVENT+1
background_color_change_event=pygame.USEREVENT+2


#background colors
blue=pygame.color('blue')
lightblue=pygame.color('lightblue')
darkblue=pygame.color('darkblue')
cyan=pygame.color('cyan')
scarlet=pygame.color('scarlet')

#sprite colors
fluorescentyellow=pygame.color('fluorescentyellow')
magenta=pygame.color('magenta')
red=pygame.color('red')
green=pygame.color('green')
orange=pygame.color('orange')

class Sprite(pygame.sprite.Sprite):
    def  __init__(self,color,width,height):
        super(). __init__()
        self.image=pygame.Surface([width,height])
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.velocity=[random.choice([-1,1]),random.choice([-1,1])]

    def update(self):
        self.rect.move_ip(self.velocity)
        boundary_hit=False
        if self.rect.left <=0 or self.rect.right >= 500:
            self.velocity[0]=-self.velocity[0]
            boundary_hit=True
        if self.rect.top <=0 or self.rect.bottom >= 400:
            self.velocity[1]=-self.velocity[1]
            boundary_hit=True

        if boundary_hit:
            pygame.event.post(pygame.event.Event(sprite_color_change_event))
            pygame.event.post(pygame.event.Event(background_color_change_event))

    def change_color(self,color):
        self.image.fill(random.choice([fluorescentyellow,magenta,red,green,orange]))
        #