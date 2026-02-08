import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dimension Shift")

clock = pygame.time.Clock()

# Colours
BG = (20, 20, 40)
CYAN = (0, 255, 255)
PINK = (255, 0, 150)
GREEN = (0, 255, 100)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("Arial", 30)

GROUND = HEIGHT - 60

# ---------------- PLAYER ----------------
class Player:
    def __init__(self):
        self.size = 40
        self.x = 150
        self.reset()

    def reset(self):
        self.y = GROUND - self.size
        self.vel = 0
        self.gravity = 0.8
        self.flip = False
        self.alive = True
        self.history = []

    def update(self):
        if not self.alive:
            return

        g = -self.gravity if self.flip else self.gravity
        self.vel += g
        self.y += self.vel

        floor = GROUND - self.size
        ceiling = 0

        if not self.flip:
            if self.y >= floor:
                self.y = floor
                self.vel = 0
        else:
            if self.y <= ceiling:
                self.y = ceiling
                self.vel = 0

        # Save history for rewind
        self.history.append((self.y, self.vel))
        if len(self.history) > 120:
            self.history.pop(0)

    def rewind(self):
        if len(self.history) > 5:
            for _ in range(5):
                if self.history:
                    self.y, self.vel = self.history.pop()

    def draw(self):
        pygame.draw.rect(screen, CYAN, (self.x, self.y, self.size, self.size))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


# ---------------- GAME ----------------
player = Player()
obstacles = []
speed = 6
score = 0
spawn_timer = 0
state = "menu"

def reset():
    global speed, score
    player.reset()
    obstacles.clear()
    speed = 6
    score = 0

while True:
    clock.tick(60)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if state == "menu":
                state = "game"
                reset()

            elif state == "game":
                if event.key == pygame.K_SPACE:
                    player.vel = -15 if not player.flip else 15
                if event.key == pygame.K_g:
                    player.flip = not player.flip
                if event.key == pygame.K_t:
                    player.rewind()
                if event.key == pygame.K_r:
                    reset()

    if state == "menu":
        title = font.render("DIMENSION SHIFT", True, CYAN)
        msg = font.render("Press any key to start", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 250))

    elif state == "game":

        spawn_timer += 1
        if spawn_timer > 80:
            height = random.choice([GROUND, GROUND-120])
            obstacles.append([WIDTH, height])
            spawn_timer = 0

        for obs in obstacles:
            obs[0] -= speed

        obstacles = [o for o in obstacles if o[0] > -50]

        player.update()

        # Draw ground
        pygame.draw.rect(screen, GREEN, (0, GROUND, WIDTH, HEIGHT-GROUND))

        # Draw obstacles
        for obs in obstacles:
            rect = pygame.Rect(obs[0], obs[1]-40, 40, 40)
            pygame.draw.rect(screen, PINK, rect)
            if player.rect().colliderect(rect):
                player.alive = False

        if not player.alive:
            death = font.render("You Died - Press R", True, WHITE)
            screen.blit(death, (WIDTH//2 - death.get_width()//2, 150))

        score += 1
        if score % 500 == 0:
            speed += 0.5

        score_text = font.render(f"Score: {score//10}", True, WHITE)
        screen.blit(score_text, (20, 20))

        player.draw()

    pygame.display.flip()
