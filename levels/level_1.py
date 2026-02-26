"""
Уровень 1 - Обучение
Простые враги, медленное движение
"""
import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from enemies import BasicEnemy, SineEnemy, BossEnemy


class Level1:
    """Первый уровень - введение"""

    def __init__(self, game):
        self.game = game
        self.level_number = 1
        self.name = "Introduction"
        self.enemies_to_kill = 10  # Нужно убить врагов перед боссом
        self.enemies_killed = 0
        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.spawn_delay = 1500
        self.boss_spawned = False
        self.boss_defeated = False
        self.max_enemies_on_screen = 4

    def update(self):
        """Обновление уровня"""
        current_time = pygame.time.get_ticks()

        # Спавн врагов пока не убили нужное количество
        if (not self.boss_spawned and
            self.enemies_killed < self.enemies_to_kill and
            len(self.game.enemies) < self.max_enemies_on_screen and
            current_time - self.spawn_timer > self.spawn_delay):
            self.spawn_timer = current_time
            self.spawn_enemy()

        # Спавн босса после убийства нужного количества врагов
        if (not self.boss_spawned and
            self.enemies_killed >= self.enemies_to_kill and
            len(self.game.enemies) == 0):
            self.spawn_boss()

    def spawn_enemy(self):
        """Спавн обычного врага"""
        x = random.randint(80, SCREEN_WIDTH - 80)
        y = -50

        # 70% BasicEnemy, 30% SineEnemy
        if random.random() < 0.7:
            enemy = BasicEnemy(x, y, level=1)
        else:
            enemy = SineEnemy(x, y, level=1)

        self.game.all_sprites.add(enemy)
        self.game.enemies.add(enemy)
        self.enemies_spawned += 1

    def spawn_boss(self):
        """Спавн босса"""
        self.boss_spawned = True
        boss = BossEnemy(SCREEN_WIDTH // 2, -100, level=1)
        self.game.all_sprites.add(boss)
        self.game.enemies.add(boss)

    def on_enemy_defeated(self, enemy):
        """Вызывается при уничтожении врага"""
        if not enemy.is_boss:
            self.enemies_killed += 1
        else:
            self.boss_defeated = True

    def is_completed(self):
        """Проверка завершения уровня"""
        return self.boss_defeated

    def get_progress(self):
        """Получение прогресса уровня"""
        if self.boss_spawned:
            return 100
        return int((self.enemies_killed / self.enemies_to_kill) * 100)
