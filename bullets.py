"""
Классы пуль
"""
import pygame
import math
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_SPEED,
    ENEMY_BULLET_SPEED, WHITE, YELLOW, RED, ORANGE
)


class Bullet(pygame.sprite.Sprite):
    """Пуля игрока"""

    def __init__(self, x, y, direction=1):
        super().__init__()
        self.speed = BULLET_SPEED * direction
        self.direction = direction  # -1 вверх, 1 вниз

        # Создание изображения пули
        self.image = pygame.Surface((6, 15), pygame.SRCALPHA)

        # Градиентная пуля
        for i in range(15):
            alpha = 255 - i * 10
            color = (255, 255, 0, alpha) if direction == -1 else (255, 100, 0, alpha)
            pygame.draw.rect(self.image, color, (0, i, 6, 1))

        # Светящийся кончик
        pygame.draw.circle(self.image, WHITE, (3, 0 if direction == -1 else 14), 3)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Урон
        self.damage = 25

    def update(self):
        """Обновление позиции пули"""
        self.rect.y += self.speed

        # Удаление пули за пределами экрана
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    """Пуля врага"""

    def __init__(self, x, y, speed=None, angle=0):
        super().__init__()
        # Фиксированная скорость пули, не зависящая от врага
        self.speed = speed if speed else ENEMY_BULLET_SPEED
        self.angle = angle  # Угол в радианах
        self.vel_x = math.sin(angle) * self.speed if angle else 0
        self.vel_y = self.speed

        # Создание изображения пули
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (4, 4), 4)
        pygame.draw.circle(self.image, ORANGE, (4, 4), 2)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.damage = 10

    def update(self):
        """Обновление позиции пули"""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Удаление пули за пределами экрана
        if (self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
            self.rect.right < 0 or self.rect.left > SCREEN_WIDTH):
            self.kill()


class PowerUpBullet(pygame.sprite.Sprite):
    """Бонусная пуля (усиление)"""

    def __init__(self, x, y):
        super().__init__()
        self.speed = BULLET_SPEED * -1

        self.image = pygame.Surface((8, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 255, 255), (0, 0, 8, 20))
        pygame.draw.rect(self.image, WHITE, (2, 0, 4, 20))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.damage = 50

    def update(self):
        """Обновление позиции пули"""
        self.rect.y += self.speed

        if self.rect.bottom < 0:
            self.kill()
