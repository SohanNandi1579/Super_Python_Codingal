import pygame
import sys
import random
from collections import deque

# -------------------------
# CONFIG
# -------------------------
WIDTH, HEIGHT = 480, 720
FPS = 60
GRAVITY = 0.5
NUM_LEVELS = 100
LEVEL_SCORE_UP = 10
PIPE_WIDTH = 80

MAX_GAP = 200
MIN_GAP = 80
MIN_SPEED = 150
MAX_SPEED = 400
MAX_SPAWN = 1500
MIN_SPAWN = 900

ASSET_DIR = "assets"

def load_image(name):
    try:
        return pygame.image.load(f"{ASSET_DIR}/{name}").convert_alpha()
    except:
        return None

def load_sound(name):
    try:
        return pygame.mixer.Sound(f"{ASSET_DIR}/{name}")
    except:
        return None

# -------------------------
# ASSETS
# -------------------------
bird_sprite = load_image("bird.png")
pipe_img = load_image("pipe.png")
backgrounds = [load_image(f"bg{i}.png") for i in range(1, NUM_LEVELS+1)]
flap_sound = load_sound("flap.wav")
score_sound = load_sound("score.wav")
hit_sound = load_sound("hit.wav")

# -------------------------
# LEVELS
# -------------------------
levels = []
for i in range(NUM_LEVELS):
    gap = int(MAX_GAP - (MAX_GAP - MIN_GAP) * (i / (NUM_LEVELS-1)))
    speed = int(MIN_SPEED + (MAX_SPEED - MIN_SPEED) * (i / (NUM_LEVELS-1)))
    spawn_ms = int(MAX_SPAWN - (MAX_SPAWN - MIN_SPAWN) * (i / (NUM_LEVELS-1)))
    bg = backgrounds[i] if i < len(backgrounds) and backgrounds[i] else None
    wind = (i+1) % 10 == 0
    rain = (i+1) % 10 == 0
    layers = []
    if bg:
        layers = [
            {"image": bg, "speed": speed*0.2, "x":0},
            {"image": bg, "speed": speed*0.5, "x":0},
            {"image": bg, "speed": speed*0.8, "x":0},
        ]
    levels.append({"gap": gap, "speed": speed, "spawn_ms": spawn_ms, "bg": bg, "wind": wind, "rain": rain, "layers": layers})

# -------------------------
# PYGAME INIT
# -------------------------
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Ultimate Chaos")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)
large_font = pygame.font.Font(None, 48)

# -------------------------
# BIRD
# -------------------------
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.radius = 18

    def flap(self):
        self.vel_y = -10
        if flap_sound: flap_sound.play()

    def update(self, dt, wind_vector=(0,0)):
        self.vel_y += GRAVITY
        self.vel_y += wind_vector[1]*dt
        self.x += wind_vector[0]*dt
        self.y += self.vel_y

    def draw(self):
        if bird_sprite:
            rotated = pygame.transform.rotate(bird_sprite, -self.vel_y*3)
            rect = rotated.get_rect(center=(self.x,self.y))
            screen.blit(rotated, rect)
        else:
            pygame.draw.circle(screen,(255,200,60),(int(self.x),int(self.y)),self.radius)

    def get_rect(self):
        return pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)

# -------------------------
# PIPE
# -------------------------
class PipePair:
    def __init__(self, x, top_height, gap, speed):
        self.x = x
        self.top_height = top_height
        self.gap = gap
        self.speed = speed
        self.top_rect = pygame.Rect(self.x,0,PIPE_WIDTH,self.top_height)
        self.bottom_rect = pygame.Rect(self.x,self.top_height+self.gap,PIPE_WIDTH,HEIGHT-(self.top_height+self.gap))
        self.passed = False

    def update(self, dt):
        self.x -= self.speed*dt
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def draw(self):
        if pipe_img:
            top_img = pygame.transform.flip(pipe_img, False, True)
            screen.blit(top_img, (int(self.x), self.top_height - pipe_img.get_height()))
            screen.blit(pipe_img, (int(self.x), self.top_height+self.gap))
        else:
            pygame.draw.rect(screen, (30,140,40), self.top_rect)
            pygame.draw.rect(screen, (30,140,40), self.bottom_rect)

    def collides(self, rect):
        return rect.colliderect(self.top_rect) or rect.colliderect(self.bottom_rect)

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

# -------------------------
# RAIN
# -------------------------
class RainDrop:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT,0)
        self.speed = random.uniform(300,500)
    def update(self, dt):
        self.y += self.speed*dt
        if self.y>HEIGHT:
            self.y = random.randint(-HEIGHT,0)
            self.x = random.randint(0,WIDTH)
    def draw(self):
        pygame.draw.line(screen,(100,100,255),(self.x,self.y),(self.x,self.y+5),1)

# -------------------------
# GAME
# -------------------------
class Game:
    def __init__(self):
        self.bird = Bird(120, HEIGHT//2)
        self.pipes = deque()
        self.spawn_timer = 0
        self.score = 0
        self.level_index = 0
        self.total_time = 0
        self.game_over = False
        self.paused = False
        self.rain_drops = [RainDrop() for _ in range(100)]
        self.in_menu = True
        self.selected_level = 0
        self.menu_page = 0

    def spawn_pipe(self):
        gap = levels[self.level_index]["gap"]
        speed = levels[self.level_index]["speed"]
        x = WIDTH + 20
        top_height = random.randint(60, HEIGHT-gap-160)
        pair = PipePair(x, top_height, gap, speed)
        self.pipes.append(pair)

    def update(self, dt):
        if self.paused or self.game_over or self.in_menu: return

        self.total_time += dt
        level_data = levels[self.level_index]
        wind = level_data["wind"]
        rain = level_data["rain"]

        if wind:
            wind_strength = 400
            wind_vector = (
                random.uniform(-1,1)*wind_strength,
                random.uniform(-0.3,0.3)*wind_strength
            )
        else:
            wind_vector = (0,0)

        self.bird.update(dt, wind_vector)

        self.spawn_timer += dt*1000
        if self.spawn_timer >= level_data["spawn_ms"]:
            self.spawn_timer %= level_data["spawn_ms"]
            self.spawn_pipe()

        for p in list(self.pipes):
            p.update(dt)
            if not p.passed and p.x + PIPE_WIDTH < self.bird.x:
                p.passed = True
                self.score += 1
                if score_sound: score_sound.play()

        while self.pipes and self.pipes[0].off_screen():
            self.pipes.popleft()

        rect = self.bird.get_rect()
        hit = False
        for p in self.pipes:
            if p.collides(rect): hit=True
        if self.bird.y - self.bird.radius <=0 or self.bird.y + self.bird.radius >= HEIGHT:
            hit=True
        if self.bird.x - self.bird.radius <=0 or self.bird.x + self.bird.radius >= WIDTH:
            hit=True
        if hit:
            self.game_over = True
            if hit_sound: hit_sound.play()

        if self.score >= (self.level_index+1)*LEVEL_SCORE_UP and self.level_index < NUM_LEVELS-1:
            self.level_index += 1
            self.pipes.clear()
            self.spawn_timer=0
            self.bird.x = 120
            self.bird.y = HEIGHT//2
            self.bird.vel_y = 0

        if rain:
            for drop in self.rain_drops:
                drop.update(dt)

        # parallax
        for layer in level_data["layers"]:
            layer["x"] -= layer["speed"]*dt
            if layer["x"] <= -WIDTH: layer["x"] += WIDTH

    def draw(self):
        level_data = levels[self.level_index]
        if level_data["layers"]:
            for layer in level_data["layers"]:
                screen.blit(pygame.transform.scale(layer["image"],(WIDTH,HEIGHT)),(layer["x"],0))
                screen.blit(pygame.transform.scale(layer["image"],(WIDTH,HEIGHT)),(layer["x"]+WIDTH,0))
        else:
            screen.fill((135,206,235))

        for p in self.pipes: p.draw()
        self.bird.draw()

        if level_data["rain"]:
            for drop in self.rain_drops: drop.draw()

        score_text = font.render(f"Score: {self.score}  Level: {self.level_index+1}", True, (0,0,0))
        screen.blit(score_text, (10,10))

        if self.game_over:
            go = large_font.render("GAME OVER", True,(255,80,80))
            screen.blit(go,(WIDTH//2-go.get_width()//2,HEIGHT//2-40))
            info = font.render("Press R to Restart | SPACE to flap", True,(255,255,255))
            screen.blit(info,(WIDTH//2-info.get_width()//2, HEIGHT//2+20))

        if self.in_menu:
            screen.fill((50,50,100))
            title = large_font.render("Select Level", True,(255,255,0))
            screen.blit(title,(WIDTH//2-title.get_width()//2,50))
            start_y = 150
            cols = 5
            rows = 4
            per_page = cols*rows
            first_idx = self.menu_page*per_page
            for i in range(per_page):
                idx = first_idx + i
                if idx>=NUM_LEVELS: break
                row = i//cols
                col = i%cols
                x = 60 + col*80
                y = start_y + row*60
                color = (255,255,0) if idx==self.selected_level else (200,200,200)
                txt = font.render(f"{idx+1}", True,color)
                screen.blit(txt,(x,y))
            page_info = font.render(f"Page {self.menu_page+1}/{(NUM_LEVELS-1)//per_page+1}", True,(255,255,255))
            screen.blit(page_info,(WIDTH//2-page_info.get_width()//2, HEIGHT-50))
            instructions = font.render("Arrows: Move  Enter: Start", True,(255,255,255))
            screen.blit(instructions,(WIDTH//2-instructions.get_width()//2, HEIGHT-30))

        pygame.display.flip()

    def handle_event(self,e):
        if e.type==pygame.QUIT: pygame.quit(); sys.exit()
        elif e.type==pygame.KEYDOWN:
            if self.in_menu:
                cols = 5
                rows = 4
                per_page = cols*rows
                if e.key==pygame.K_RIGHT:
                    if self.selected_level%cols < cols-1: self.selected_level+=1
                if e.key==pygame.K_LEFT:
                    if self.selected_level%cols > 0: self.selected_level-=1
                if e.key==pygame.K_DOWN:
                    if self.selected_level + cols < NUM_LEVELS: self.selected_level+=cols
                if e.key==pygame.K_UP:
                    if self.selected_level - cols >=0: self.selected_level-=cols
                if e.key==pygame.K_RETURN:
                    self.level_index = self.selected_level
                    self.in_menu=False
                self.menu_page = self.selected_level//per_page
            else:
                if e.key==pygame.K_SPACE and not self.game_over: self.bird.flap()
                if e.key==pygame.K_r: self.__init__()
                if e.key==pygame.K_p: self.paused = not self.paused

# -------------------------
# MAIN LOOP
# -------------------------
game = Game()
while True:
    dt = clock.tick(FPS)/1000.0
    for e in pygame.event.get(): game.handle_event(e)
    game.update(dt)
    game.draw()
