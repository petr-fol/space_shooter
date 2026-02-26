"""
Визуальные эффекты
"""
import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, RED, ORANGE


class Explosion(pygame.sprite.Sprite):
    """Эффект взрыва"""
    
    def __init__(self, x, y, color=YELLOW, size=30, duration=500):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.max_radius = size
        self.particles = []
        
        # Создание частиц
        for _ in range(20):
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-5, 5),
                'life': random.randint(20, 40),
                'color': random.choice([color, YELLOW, ORANGE, RED]),
                'size': random.randint(2, 5)
            })
        
        self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        """Обновление эффекта"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        
        # Очистка поверхности
        self.image.fill((0, 0, 0, 0))
        
        # Обновление и отрисовка частиц
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['size'] = max(0, particle['size'] - 0.1)
            
            if particle['life'] <= 0 or particle['size'] <= 0:
                self.particles.remove(particle)
                continue
            
            # Отрисовка частицы
            alpha = int(255 * (particle['life'] / 40))
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(self.image, color, 
                             (int(particle['x'] - self.rect.x), int(particle['y'] - self.rect.y)), 
                             int(particle['size']))
        
        # Удаление эффекта, когда все частицы исчезли
        if not self.particles or elapsed > self.duration:
            self.kill()


class StarField:
    """Звёздное поле (фон)"""
    
    def __init__(self, width, height, star_count=100, speed=2):
        self.width = width
        self.height = height
        self.speed = speed
        self.stars = []
        
        # Создание звёзд
        for _ in range(star_count):
            self.stars.append({
                'x': random.randint(0, width),
                'y': random.randint(0, height),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.5, speed),
                'brightness': random.randint(100, 255)
            })
    
    def update(self):
        """Обновление звёздного поля"""
        for star in self.stars:
            star['y'] += star['speed']
            # Если звезда ушла за экран, перемещаем её наверх
            if star['y'] > self.height:
                star['y'] = 0
                star['x'] = random.randint(0, self.width)
    
    def draw(self, surface):
        """Отрисовка звёздного поля"""
        for star in self.stars:
            # Мерцание звёзд
            brightness = star['brightness'] + random.randint(-20, 20)
            brightness = max(100, min(255, brightness))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(surface, color, (star['x'], int(star['y'])), star['size'])


class Thruster:
    """Эффект двигателя"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particles = []
        self.max_particles = 10
    
    def update(self):
        """Обновление эффекта"""
        # Добавление новой частицы
        if len(self.particles) < self.max_particles:
            self.particles.append({
                'x': self.x + random.uniform(-3, 3),
                'y': self.y,
                'vy': random.uniform(2, 5),
                'life': random.randint(10, 20),
                'size': random.randint(3, 6)
            })
        
        # Обновление частиц
        for particle in self.particles[:]:
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['size'] = max(0, particle['size'] - 0.2)
            
            if particle['life'] <= 0 or particle['size'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, surface):
        """Отрисовка эффекта"""
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 20))
            color = (255, random.randint(100, 255), 0, alpha)
            pygame.draw.circle(surface, color, 
                             (int(particle['x']), int(particle['y'])), 
                             int(particle['size']))


class ScorePopup:
    """Всплывающие очки"""
    
    def __init__(self, x, y, text, color=WHITE):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.start_time = pygame.time.get_ticks()
        self.duration = 1000
        self.font = pygame.font.Font(None, 28)
    
    def update(self):
        """Обновление"""
        pass
    
    def draw(self, surface):
        """Отрисовка"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        
        if elapsed > self.duration:
            return False
        
        # Смещение вверх
        offset = (elapsed / self.duration) * 30
        alpha = max(0, 255 - int(255 * (elapsed / self.duration)))
        
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.x, self.y - offset))
        surface.blit(text_surface, text_rect)
        
        return True
