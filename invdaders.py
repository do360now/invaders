import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
PADDING = 10
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
ASTEROID_WIDTH = 40
ASTEROID_HEIGHT = 40
PLAYER_Y = SCREEN_HEIGHT - PADDING - PLAYER_HEIGHT
PLAYER_MOVE_STEP = 5
ASTEROID_MOVE_STEP = 5
ASTEROID_FALL_SPEED_INCREMENT = 0.1
NEW_ASTEROID_INTERVAL = 1000  # milliseconds

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 204, 0)
ASTEROID_COLOR = (204, 0, 0)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroid Dodge")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        self.rect.y = PLAYER_Y

    def move_left(self):
        self.rect.x = max(self.rect.x - PLAYER_MOVE_STEP, PADDING)

    def move_right(self):
        self.rect.x = min(self.rect.x + PLAYER_MOVE_STEP, SCREEN_WIDTH - PADDING - PLAYER_WIDTH)

# Asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((ASTEROID_WIDTH, ASTEROID_HEIGHT))
        self.image.fill(ASTEROID_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()

# Game setup
player = Player()
all_sprites = pygame.sprite.Group(player)
asteroids = pygame.sprite.Group()

def create_asteroid():
    x = random.randint(PADDING, SCREEN_WIDTH - PADDING - ASTEROID_WIDTH)
    y = -ASTEROID_HEIGHT
    speed = ASTEROID_MOVE_STEP + random.random() * 3
    asteroid = Asteroid(x, y, speed)
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

# Game loop
running = True
clock = pygame.time.Clock()
keys = pygame.key.get_pressed()
score = 0
last_asteroid_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    # Update sprites
    all_sprites.update()

    # Check collisions
    if pygame.sprite.spritecollideany(player, asteroids):
        running = False

    # Create new asteroids
    current_time = pygame.time.get_ticks()
    if current_time - last_asteroid_time > NEW_ASTEROID_INTERVAL:
        create_asteroid()
        last_asteroid_time = current_time

    # Update score
    score += 1

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)
    score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (PADDING, PADDING))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
