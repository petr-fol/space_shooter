"""
Классы врагов
"""
import pygame
import random
import math
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, GREEN,
    PURPLE, ORANGE, CYAN, GRAY
)


class Enemy(pygame.sprite.Sprite):
    """Базовый класс врага"""

    def __init__(self, x, y, health=50, speed=2, damage=10, score_value=100, color=RED):
        super().__init__()
        self.health = health
        self.max_health = health
        self.speed = speed
        self.damage = damage
        self.score_value = score_value
        self.color = color
        self.shoot_timer = 0
        self.shoot_delay = 2000  # мс между выстрелами
        self.start_x = x
        self.start_y = y
        self.move_pattern = "straight"
        self.move_timer = 0
        self.is_boss = False

        self.image = self.create_enemy_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def create_enemy_image(self):
        """Создание изображения врага"""
        size = 35
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        points = [
            (size // 2, size - 5),
            (5, 5),
            (size // 2, 10),
            (size - 5, 5)
        ]
        pygame.draw.polygon(surface, self.color, points)
        pygame.draw.circle(surface, WHITE, (size // 2, size // 2), 4)
        pygame.draw.circle(surface, GRAY, (10, 15), 3)
        pygame.draw.circle(surface, GRAY, (size - 10, 15), 3)

        return surface

    def update(self):
        """Обновление позиции врага"""
        self.move_timer += 1

        if self.move_pattern == "straight":
            self.rect.y += self.speed
        elif self.move_pattern == "sine":
            self.rect.y += self.speed
            self.rect.x = self.start_x + math.sin(self.move_timer * 0.03) * 50
        elif self.move_pattern == "zigzag":
            self.rect.y += self.speed
            if self.move_timer % 60 < 30:
                self.rect.x += 1
            else:
                self.rect.x -= 1
        elif self.move_pattern == "circle":
            self.rect.y += self.speed * 0.7
            self.rect.x = self.start_x + math.cos(self.move_timer * 0.02) * 30

        # Телепортация по X
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
            self.start_x = SCREEN_WIDTH + self.rect.width // 2
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
            self.start_x = -self.rect.width // 2

        # Удаление если ушёл слишком далеко вниз - ВРАГ УБИРАЕТСЯ БЕЗ ОЧКОВ
        if self.rect.top > SCREEN_HEIGHT + 50:
            self.kill()

    def shoot(self):
        """Выстрел врага"""
        from bullets import EnemyBullet
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = current_time
            # Пуля с фиксированной скоростью 5
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, speed=5)
            return bullet
        return None

    def take_damage(self, damage):
        """Получение урона"""
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False

    def draw_health_bar(self, surface):
        """Отрисовка полоски здоровья"""
        if self.health < self.max_health:
            bar_width = 30
            bar_height = 4
            fill = (self.health / self.max_health) * bar_width

            pygame.draw.rect(surface, RED, (self.rect.centerx - bar_width//2, self.rect.top - 8, bar_width, bar_height))
            pygame.draw.rect(surface, GREEN, (self.rect.centerx - bar_width//2, self.rect.top - 8, fill, bar_height))


class BasicEnemy(Enemy):
    """Простой враг"""

    def __init__(self, x, y, level=1):
        # Настройки для разных уровней
        health = 30 + (level - 1) * 15
        speed = 1.5 + (level - 1) * 0.3
        damage = 10 + (level - 1) * 5
        score = 100 * level

        super().__init__(x, y, health=health, speed=speed, damage=damage, score_value=score, color=RED)
        self.move_pattern = "straight"
        self.shoot_delay = 2500
        self.level = level


class SineEnemy(Enemy):
    """Враг, движущийся по синусоиде"""

    def __init__(self, x, y, level=1):
        health = 50 + (level - 1) * 20
        speed = 1.2 + (level - 1) * 0.3
        damage = 15 + (level - 1) * 5
        score = 150 * level

        super().__init__(x, y, health=health, speed=speed, damage=damage, score_value=score, color=ORANGE)
        self.move_pattern = "sine"
        self.shoot_delay = 2000
        self.level = level


class ZigZagEnemy(Enemy):
    """Враг, движущийся зигзагом"""

    def __init__(self, x, y, level=1):
        health = 40 + (level - 1) * 15
        speed = 1.8 + (level - 1) * 0.3
        damage = 12 + (level - 1) * 4
        score = 120 * level

        super().__init__(x, y, health=health, speed=speed, damage=damage, score_value=score, color=PURPLE)
        self.move_pattern = "zigzag"
        self.shoot_delay = 1800
        self.level = level


class TankEnemy(Enemy):
    """Танк - медленный, но живой"""

    def __init__(self, x, y, level=1):
        health = 120 + (level - 1) * 50
        speed = 0.6 + (level - 1) * 0.15
        damage = 25 + (level - 1) * 8
        score = 300 * level

        super().__init__(x, y, health=health, speed=speed, damage=damage, score_value=score, color=GRAY)
        self.move_pattern = "straight"
        self.shoot_delay = 1500
        self.level = level

        self.image = self.create_tank_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def create_tank_image(self):
        """Создание изображения танка"""
        size = 50
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        pygame.draw.rect(surface, GRAY, (10, 10, 30, 35))
        pygame.draw.polygon(surface, (80, 80, 80),
                          [(5, 45), (size-5, 45), (size//2, 25)])
        pygame.draw.rect(surface, (80, 80, 80), (22, 35, 6, 15))
        pygame.draw.circle(surface, RED, (25, 25), 5)
        pygame.draw.circle(surface, WHITE, (15, 20), 3)
        pygame.draw.circle(surface, WHITE, (35, 20), 3)

        return surface


class ShooterEnemy(Enemy):
    """Враг, который часто стреляет"""

    def __init__(self, x, y, level=1):
        health = 35 + (level - 1) * 15
        speed = 1.0 + (level - 1) * 0.2
        damage = 10 + (level - 1) * 4
        score = 180 * level

        super().__init__(x, y, health=health, speed=speed, damage=damage, score_value=score, color=CYN)
        self.move_pattern = "circle"
        self.shoot_delay = 1000
        self.level = level

    def shoot(self):
        """Стреляет тремя пулями"""
        from bullets import EnemyBullet
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = current_time
            bullets = []
            # Пули с фиксированной скоростью
            bullets.append(EnemyBullet(self.rect.centerx, self.rect.bottom, speed=5))
            bullets.append(EnemyBullet(self.rect.centerx, self.rect.bottom, speed=5, angle=math.pi/6))
            bullets.append(EnemyBullet(self.rect.centerx, self.rect.bottom, speed=5, angle=-math.pi/6))
            return bullets
        return None


class BossEnemy(Enemy):
    """Босс уровня"""

    def __init__(self, x, y, level=1):
        self.level = level
        health = 400 + (level - 1) * 250  # Босс не умирает с 1 выстрела
        speed = 1.0 + (level - 1) * 0.2
        damage = 25 + (level - 1) * 10
        score = 1000 * level

        super().__init__(x, y, health=health, speed=speed, damage=damage, score_value=score, color=(139, 0, 0))
        self.is_boss = True
        self.move_pattern = "boss_horizontal"  # Новый паттерн для босса
        self.shoot_delay = 800
        self.attack_pattern = 0
        self.attack_timer = 0
        self.move_direction = 1  # 1 вправо, -1 влево
        self.move_range = 200  # Диапазон движения по горизонтали
        self.base_x = SCREEN_WIDTH // 2
        self.base_y = 100  # Фиксированная позиция по Y

        self.image = self.create_boss_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def create_boss_image(self):
        """Создание изображения босса"""
        size = 80
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        pygame.draw.polygon(surface, (139, 0, 0),
                          [(size//2, size-10), (10, 20), (size//2, 5), (size-10, 20)])
        pygame.draw.polygon(surface, (100, 0, 0),
                          [(0, 30), (15, 25), (15, 55), (5, 50)])
        pygame.draw.polygon(surface, (100, 0, 0),
                          [(size, 30), (size-15, 25), (size-15, 55), (size-5, 50)])
        pygame.draw.circle(surface, (200, 50, 50), (20, 40), 8)
        pygame.draw.circle(surface, (200, 50, 50), (size-20, 40), 8)
        pygame.draw.circle(surface, (255, 100, 100), (size//2, size//2), 12)
        pygame.draw.circle(surface, WHITE, (size//2, size//2), 6)

        return surface

    def update(self):
        """Обновление босса - движение по горизонтали"""
        self.move_timer += 1

        # Движение по горизонтали в пределах диапазона
        self.rect.x += self.speed * self.move_direction

        # Фиксируем Y позицию - босс не двигается вниз!
        self.rect.centery = self.base_y

        # Разворот у границ диапазона
        if self.rect.centerx > self.base_x + self.move_range:
            self.move_direction = -1
        elif self.rect.centerx < self.base_x - self.move_range:
            self.move_direction = 1

        # Убедимся, что босс не уходит за экран
        if self.rect.left < 0:
            self.rect.left = 0
            self.move_direction = 1
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.move_direction = -1

        # Изменение паттерна атаки
        self.attack_timer += 1
        if self.attack_timer > 300:
            self.attack_timer = 0
            self.attack_pattern = (self.attack_pattern + 1) % 3

    def draw(self, surface):
        """Отрисовка босса с полоской здоровья"""
        surface.blit(self.image, self.rect)
        # Полоска здоровья босса
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        """Отрисовка полоски здоровья босса"""
        bar_width = 100
        bar_height = 8
        fill = (self.health / self.max_health) * bar_width

        # Фон
        pygame.draw.rect(surface, (100, 0, 0), (self.rect.centerx - bar_width//2, self.rect.top - 15, bar_width, bar_height))
        # Заполнение
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.centerx - bar_width//2, self.rect.top - 15, fill, bar_height))
        # Рамка
        pygame.draw.rect(surface, WHITE, (self.rect.centerx - bar_width//2, self.rect.top - 15, bar_width, bar_height), 2)

    def shoot(self):
        """Особая атака босса"""
        from bullets import EnemyBullet
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = current_time
            bullets = []

            if self.attack_pattern == 0:
                # Круговой выстрел
                for i in range(8):
                    angle = (2 * math.pi / 8) * i
                    bullet = EnemyBullet(self.rect.centerx, self.rect.centery,
                                        speed=4, angle=angle + math.pi/2)
                    bullets.append(bullet)
            elif self.attack_pattern == 1:
                # Тройной выстрел вниз
                bullets.append(EnemyBullet(self.rect.centerx - 20, self.rect.bottom, speed=5))
                bullets.append(EnemyBullet(self.rect.centerx, self.rect.bottom, speed=5))
                bullets.append(EnemyBullet(self.rect.centerx + 20, self.rect.bottom, speed=5))
            else:
                # Спиральный выстрел
                angle = current_time * 0.01
                for i in range(4):
                    bullet = EnemyBullet(self.rect.centerx, self.rect.centery,
                                        speed=4, angle=angle + (math.pi/2) * i)
                    bullets.append(bullet)

            return bullets
        return None
