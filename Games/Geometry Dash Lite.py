import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Dash X")

clock = pygame.time.Clock()

# Colours
BG = (15, 15, 30)
CYAN = (0, 255, 255)
PINK = (255, 0, 255)
GREEN = (57, 255, 20)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

font_big = pygame.font.SysFont("Arial", 60)
font = pygame.font.SysFont("Arial", 30)

GROUND = 80

# ---------------- PLAYER ----------------
class Player:
    def __init__(self):
        self.x = 200
        self.size = 40
        self.reset()

    def reset(self):
        self.y = HEIGHT - GROUND - self.size
        self.vel = 0
        self.gravity = 0.9
        self.jump_power = -18
        self.rotation = 0
        self.mini = False
        self.gravity_flip = False
        self.alive = True

    def get_size(self):
        return 25 if self.mini else 40

    def rect(self):
        size = self.get_size()
        return pygame.Rect(self.x - size//2, self.y, size, size)

    def update(self):
        if not self.alive:
            return

        g = -self.gravity if self.gravity_flip else self.gravity
        self.vel += g
        self.y += self.vel

        floor = HEIGHT - GROUND - self.get_size()
        ceiling = 0

        if not self.gravity_flip:
            if self.y >= floor:
                self.y = floor
                self.vel = 0
        else:
            if self.y <= ceiling:
                self.y = ceiling
                self.vel = 0

        if abs(self.vel) > 1:
            self.rotation += 8

    def jump(self):
        if self.alive:
            self.vel = self.jump_power if not self.gravity_flip else -self.jump_power

    def draw(self):
        size = self.get_size()
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(surf, CYAN, (0, 0, size, size))
        rot = pygame.transform.rotate(surf, self.rotation)
        rect = rot.get_rect(center=(self.x, self.y + size//2))
        screen.blit(rot, rect.topleft)


# ---------------- PARTICLES ----------------
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-5, 5)
        self.dy = random.uniform(-5, 5)
        self.life = 30

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self):
        pygame.draw.circle(screen, PINK, (int(self.x), int(self.y)), 3)


# ---------------- GAME ----------------
player = Player()
obstacles = []
orbs = []
pads = []
portals = []
particles = []

speed = 7
score = 0
state = "menu"
spawn_timer = 0


def spawn():
    r = random.random()
    if r < 0.5:
        obstacles.append([WIDTH, HEIGHT - GROUND])
    elif r < 0.7:
        orbs.append([WIDTH, HEIGHT - GROUND - 120])
    elif r < 0.85:
        pads.append([WIDTH, HEIGHT - GROUND - 10])
    else:
        portals.append([WIDTH, random.choice(["gravity", "mini"])])


def reset():
    global speed, score
    player.reset()
    obstacles.clear()
    orbs.clear()
    pads.clear()
    portals.clear()
    particles.clear()
    speed = 7
    score = 0


# ---------------- MAIN LOOP ----------------
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
                    player.jump()
                if event.key == pygame.K_r:
                    reset()

    if state == "menu":
        title = font_big.render("NEON DASH X", True, CYAN)
        msg = font.render("Press any key to start", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 180))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 300))

    elif state == "game":

        spawn_timer += 1
        if spawn_timer > 90:
            spawn()
            spawn_timer = 0

        # Move objects
        for group in [obstacles, orbs, pads]:
            for obj in group:
                obj[0] -= speed

        for portal in portals:
            portal[0] -= speed

        player.update()

        pygame.draw.rect(screen, GREEN, (0, HEIGHT-GROUND, WIDTH, GROUND))

        # Obstacles
        for obs in obstacles:
            points = [(obs[0], obs[1]),
                      (obs[0]+40, obs[1]),
                      (obs[0]+20, obs[1]-40)]
            pygame.draw.polygon(screen, PINK, points)

            if player.rect().colliderect(pygame.Rect(obs[0], obs[1]-40, 40, 40)):
                player.alive = False
                for _ in range(25):
                    particles.append(Particle(player.x, player.y))

        # Orbs
        for orb in orbs:
            pygame.draw.circle(screen, YELLOW, (int(orb[0]), int(orb[1])), 12)
            if player.rect().colliderect(pygame.Rect(orb[0]-12, orb[1]-12, 24, 24)):
                player.vel = -20 if not player.gravity_flip else 20

        # Pads
        for pad in pads:
            pygame.draw.rect(screen, CYAN, (pad[0], pad[1], 40, 10))
            if player.rect().colliderect(pygame.Rect(pad[0], pad[1], 40, 10)):
                player.vel = -25 if not player.gravity_flip else 25

        # Portals
        for portal in portals:
            color = GREEN if portal[1]=="gravity" else PINK
            pygame.draw.rect(screen, color, (portal[0], 200, 20, 100))
            if player.rect().colliderect(pygame.Rect(portal[0], 200, 20, 100)):
                if portal[1] == "gravity":
                    player.gravity_flip = not player.gravity_flip
                else:
                    player.mini = not player.mini

        # Particles
        for p in particles[:]:
            p.update()
            p.draw()
            if p.life <= 0:
                particles.remove(p)

        score += 1
        if score % 600 == 0:
            speed += 0.5

        score_text = font.render(f"Score: {score//10}", True, WHITE)
        screen.blit(score_text, (20, 20))

        player.draw()

    pygame.display.flip()
