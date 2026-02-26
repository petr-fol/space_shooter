"""
Класс игрока
"""
import pygame
import math
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, 
    PLAYER_MAX_HEALTH, PLAYER_SHOOT_DELAY,
    WHITE, GREEN, RED, YELLOW, CYAN
)


class Player(pygame.sprite.Sprite):
    """Класс игрока"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.speed = PLAYER_SPEED
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.score = 0
        self.last_shot = 0
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 2000  # 2 секунды неуязвимости после получения урона
        
        # Создание изображения корабля
        self.image = self.create_ship_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        
        # Маска для коллизий
        self.mask = pygame.mask.from_surface(self.image)
        
        # Вектор движения
        self.vel_x = 0
        self.vel_y = 0
        self.friction = 0.92
        self.acceleration = 0.5
    
    def create_ship_image(self):
        """Создание изображения корабля игрока"""
        size = 40
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Основной корпус (треугольник)
        points = [
            (size // 2, 5),      # Нос
            (5, size - 5),       # Левый угол
            (size // 2, size - 10),  # Впадина сзади
            (size - 5, size - 5)  # Правый угол
        ]
        pygame.draw.polygon(surface, CYAN, points)
        
        # Двигатель (свечение)
        engine_points = [
            (size // 2 - 5, size - 8),
            (size // 2 + 5, size - 8),
            (size // 2, size - 2)
        ]
        pygame.draw.polygon(surface, YELLOW, engine_points)
        
        # Кокпит
        pygame.draw.circle(surface, WHITE, (size // 2, size // 2), 5)
        
        return surface
    
    def update(self):
        """Обновление состояния игрока"""
        # Применение ускорения
        self.vel_x += self.acceleration if self.game.keys[pygame.K_RIGHT] or self.game.keys[pygame.K_d] else 0
        self.vel_x -= self.acceleration if self.game.keys[pygame.K_LEFT] or self.game.keys[pygame.K_a] else 0
        self.vel_y += self.acceleration if self.game.keys[pygame.K_DOWN] or self.game.keys[pygame.K_s] else 0
        self.vel_y -= self.acceleration if self.game.keys[pygame.K_UP] or self.game.keys[pygame.K_w] else 0
        
        # Трение
        self.vel_x *= self.friction
        self.vel_y *= self.friction
        
        # Ограничение скорости
        max_vel = self.speed
        self.vel_x = max(-max_vel, min(max_vel, self.vel_x))
        self.vel_y = max(-max_vel, min(max_vel, self.vel_y))
        
        # Обновление позиции
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Выход за границы экрана (телепортация на другую сторону)
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
        
        # Обновление таймера неуязвимости
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_timer > self.invincible_duration:
                self.invincible = False
    
    def shoot(self):
        """Стрельба"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > PLAYER_SHOOT_DELAY:
            self.last_shot = current_time
            # Создаём пулю
            from bullets import Bullet
            bullet = Bullet(self.rect.centerx, self.rect.top, -1)
            self.game.all_sprites.add(bullet)
            self.game.player_bullets.add(bullet)
            return True
        return False
    
    def take_damage(self, damage):
        """Получение урона"""
        if not self.invincible:
            self.health -= damage
            self.invincible = True
            self.invincible_timer = pygame.time.get_ticks()

            # Создание эффекта взрыва
            from effects import Explosion
            explosion = Explosion(self.rect.centerx, self.rect.centery, color=RED, size=20)
            self.game.all_sprites.add(explosion)

            if self.health <= 0:
                self.health = 0
    
    def heal(self, amount):
        """Лечение"""
        self.health = min(self.max_health, self.health + amount)
    
    def draw(self, surface):
        """Отрисовка игрока с эффектом мигания при неуязвимости"""
        if self.invincible:
            # Мигание
            if pygame.time.get_ticks() % 100 < 50:
                surface.blit(self.image, self.rect)
        else:
            surface.blit(self.image, self.rect)
    
    def draw_health_bar(self, surface):
        """Отрисовка полоски здоровья"""
        bar_width = 200
        bar_height = 20
        fill = (self.health / self.max_health) * bar_width
        
        # Фон полоски
        border_rect = pygame.Rect(10, 10, bar_width, bar_height)
        pygame.draw.rect(surface, RED, border_rect)
        
        # Заполнение
        fill_rect = pygame.Rect(12, 12, fill - 2, bar_height - 4)
        pygame.draw.rect(surface, GREEN, fill_rect)
        
        # Рамка
        pygame.draw.rect(surface, WHITE, border_rect, 2)
        
        # Текст
        health_text = pygame.font.Font(None, 24).render(f"HP: {self.health}/{self.max_health}", True, WHITE)
        surface.blit(health_text, (15, 12))
