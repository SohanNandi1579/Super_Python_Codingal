import pygame
import random
import sys

# -------------------
# Setup
# -------------------
pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 28)

# -------------------
# Player
# -------------------
player_width = 50
player_height = 30
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 60
player_speed = 6

# -------------------
# Bullet
# -------------------
bullet_width = 5
bullet_height = 15
bullet_speed = 7
bullets = []

# -------------------
# Enemies
# -------------------
enemy_width = 40
enemy_height = 30
enemy_rows = 4
enemy_cols = 8
enemy_padding = 20
enemy_offset_x = 80
enemy_offset_y = 60
enemy_speed = 1

enemies = []

for row in range(enemy_rows):
    for col in range(enemy_cols):
        x = enemy_offset_x + col * (enemy_width + enemy_padding)
        y = enemy_offset_y + row * (enemy_height + enemy_padding)
        enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))

enemy_direction = 1

score = 0
game_over = False

# -------------------
# Game Loop
# -------------------
while True:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullet = pygame.Rect(player_x + player_width//2 - 2,
                                     player_y,
                                     bullet_width,
                                     bullet_height)
                bullets.append(bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Move bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Move enemies
    move_down = False
    for enemy in enemies:
        enemy.x += enemy_speed * enemy_direction
        if enemy.right >= WIDTH or enemy.left <= 0:
            move_down = True

    if move_down:
        enemy_direction *= -1
        for enemy in enemies:
            enemy.y += 20

    # Collision
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    # Check game over
    for enemy in enemies:
        if enemy.bottom >= player_y:
            game_over = True

    # Draw player
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(over_text, (WIDTH//2 - 100, HEIGHT//2))

    pygame.display.flip()
