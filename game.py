"""
Основной класс игры
"""
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE,
    DARK_BLUE, TOTAL_LEVELS
)
from player import Player
from collision import CollisionSystem, Score
from effects import StarField, ScorePopup


class Game:
    """Основной класс игры"""

    def __init__(self, space_shooter, level=1):
        self.space_shooter = space_shooter
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        # Создание игрока
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # Система столкновений
        self.collision_system = CollisionSystem(self)

        # Счёт
        self.score = Score()

        # Звёздный фон
        self.star_field = StarField(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Уровень
        self.current_level_num = level
        self.level = None
        self.level_completed = False
        self.load_level()

        # Всплывающие очки
        self.score_popups = []

        # Таймер для вражеских выстрелов
        self.enemy_shoot_timer = 0

        # Клавиши
        self.keys = pygame.key.get_pressed()

    def load_level(self):
        """Загрузка уровня"""
        if self.current_level_num == 1:
            from levels.level_1 import Level1
            self.level = Level1(self)
        elif self.current_level_num == 2:
            from levels.level_2 import Level2
            self.level = Level2(self)
        elif self.current_level_num == 3:
            from levels.level_3 import Level3
            self.level = Level3(self)

    def handle_event(self, event):
        """Обработка событий"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.shoot()

    def update(self):
        """Обновление игры"""
        # Обновление клавиш
        self.keys = pygame.key.get_pressed()

        # Обновление звёздного фона
        self.star_field.update()

        # Обновление игрока
        self.player.update()

        # Обновление пуль
        self.player_bullets.update()
        self.enemy_bullets.update()

        # Обновление врагов
        self.enemies.update()

        # Обновление уровня
        if self.level:
            self.level.update()

            # Проверка завершения уровня
            if self.level.is_completed():
                self.level_completed = True
                if self.current_level_num < TOTAL_LEVELS:
                    self.current_level_num += 1
                    self.load_level()
                else:
                    # Все уровни пройдены
                    self.space_shooter.state = "victory"

        # Враги стреляют
        self.enemy_shoot_timer += 1
        if self.enemy_shoot_timer > 30:  # Каждые 30 кадров
            self.enemy_shoot_timer = 0
            for enemy in self.enemies:
                bullets = enemy.shoot()
                if bullets:
                    if isinstance(bullets, list):
                        for bullet in bullets:
                            self.all_sprites.add(bullet)
                            self.enemy_bullets.add(bullet)
                    else:
                        self.all_sprites.add(bullets)
                        self.enemy_bullets.add(bullets)

        # Проверка столкновений
        self.collision_system.check_collisions()

        # Обновление всех спрайтов
        self.all_sprites.update()

        # Обновление всплывающих очков
        self.score_popups = [p for p in self.score_popups if p.update() != False]

    def draw(self, surface):
        """Отрисовка игры"""
        # Фон
        surface.fill(DARK_BLUE)
        self.star_field.draw(surface)

        # Отрисовка всех спрайтов
        for sprite in self.all_sprites:
            if hasattr(sprite, 'draw'):
                sprite.draw(surface)
            else:
                surface.blit(sprite.image, sprite.rect)

        # Отрисовка всплывающих очков
        for popup in self.score_popups:
            popup.draw(surface)

        # Интерфейс
        self.draw_ui(surface)

    def draw_ui(self, surface):
        """Отрисовка интерфейса"""
        # Полоска здоровья
        self.player.draw_health_bar(surface)

        # Счёт
        self.score.draw(surface, SCREEN_WIDTH - 10, 10)

        # Информация об уровне
        level_font = pygame.font.Font(None, 28)
        level_text = level_font.render(f"Level {self.current_level_num}: {self.level.name}", True, WHITE)
        surface.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 10))

        # Прогресс уровня
        if self.level:
            progress = self.level.get_progress()
            bar_width = 200
            bar_height = 10
            fill = (progress / 100) * bar_width

            # Фон прогресс бара
            pygame.draw.rect(surface, (50, 50, 50), (SCREEN_WIDTH // 2 - bar_width // 2, 40, bar_width, bar_height))
            # Заполнение
            pygame.draw.rect(surface, GREEN := (0, 255, 0), (SCREEN_WIDTH // 2 - bar_width // 2, 40, fill, bar_height))
            # Рамка
            pygame.draw.rect(surface, WHITE, (SCREEN_WIDTH // 2 - bar_width // 2, 40, bar_width, bar_height), 1)

            # Счётчик убитых врагов
            if hasattr(self.level, 'enemies_killed') and hasattr(self.level, 'enemies_to_kill'):
                if not self.level.boss_spawned:
                    counter_text = level_font.render(
                        f"Killed: {self.level.enemies_killed}/{self.level.enemies_to_kill}",
                        True, WHITE
                    )
                    surface.blit(counter_text, (SCREEN_WIDTH // 2 - counter_text.get_width() // 2, 55))
                else:
                    boss_text = level_font.render("BOSS FIGHT!", True, RED := (255, 0, 0))
                    surface.blit(boss_text, (SCREEN_WIDTH // 2 - boss_text.get_width() // 2, 55))

        # Отладка - количество врагов на экране
        debug_text = pygame.font.Font(None, 24).render(f"Enemies on screen: {len(self.enemies)}", True, (150, 150, 150))
        surface.blit(debug_text, (10, SCREEN_HEIGHT - 30))
