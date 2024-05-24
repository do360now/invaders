import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import random

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

class AsteroidDodgeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(AsteroidDodgeEnv, self).__init__()
        self.screen = None
        self.clock = pygame.time.Clock()
        self.action_space = spaces.Discrete(3)  # Actions: left, stay, right
        self.observation_space = spaces.Box(low=0, high=255, shape=(SCREEN_HEIGHT, SCREEN_WIDTH, 3), dtype=np.uint8)
        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        random.seed(seed)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.seed(seed)
        self.score = 0
        self.player = Player()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.asteroids = pygame.sprite.Group()
        self.last_asteroid_time = pygame.time.get_ticks()
        self.done = False
        return self._get_obs(), {}

    def step(self, action):
        if action == 0:
            self.player.move_left()
        elif action == 2:
            self.player.move_right()

        self.all_sprites.update()
        self._spawn_asteroids()

        reward = 1
        if pygame.sprite.spritecollideany(self.player, self.asteroids):
            reward = -100
            self.done = True

        self.score += reward
        obs = self._get_obs()
        truncated = False  # This game doesn't have truncation logic
        return obs, reward, self.done, truncated, {}

    def _get_obs(self):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        return np.transpose(np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2))

    def render(self, mode='human', close=False):
        if mode == 'human':
            if self.screen is None:
                pygame.init()
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def _spawn_asteroids(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_asteroid_time > NEW_ASTEROID_INTERVAL:
            x = random.randint(PADDING, SCREEN_WIDTH - PADDING - ASTEROID_WIDTH)
            y = -ASTEROID_HEIGHT
            speed = ASTEROID_MOVE_STEP + random.random() * 3
            asteroid = Asteroid(x, y, speed)
            self.all_sprites.add(asteroid)
            self.asteroids.add(asteroid)
            self.last_asteroid_time = current_time

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill((0, 204, 0))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        self.rect.y = PLAYER_Y

    def move_left(self):
        self.rect.x = max(self.rect.x - PLAYER_MOVE_STEP, PADDING)

    def move_right(self):
        self.rect.x = min(self.rect.x + PLAYER_MOVE_STEP, SCREEN_WIDTH - PADDING - PLAYER_WIDTH)

    def update(self):
        pass

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((ASTEROID_WIDTH, ASTEROID_HEIGHT))
        self.image.fill((204, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
