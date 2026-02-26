"""
Настройки игры Space Shooter
"""
import pygame

# Экран
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Space Shooter"

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
DARK_BLUE = (10, 10, 40)
GRAY = (128, 128, 128)

# Игрок
PLAYER_SPEED = 5
PLAYER_MAX_HEALTH = 100
PLAYER_SHOOT_DELAY = 250  # мс

# Пули
BULLET_SPEED = 10
ENEMY_BULLET_SPEED = 6

# Враги
ENEMY_SPAWN_DELAY = 1500  # мс

# Звёзды (фон)
STAR_COUNT = 100
STAR_SPEED = 2

# Уровни
TOTAL_LEVELS = 3
