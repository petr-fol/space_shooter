"""
Уровень 3 - Сложный
Агрессивные враги, сложные паттерны атак
"""
import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from enemies import (
    BasicEnemy, SineEnemy, ZigZagEnemy,
    ShooterEnemy, TankEnemy, BossEnemy
)


class Level3:
    """Третий уровень - финальная битва"""

    def __init__(self, game):
        self.game = game
        self.level_number = 3
        self.name = "Final Battle"
        self.enemies_to_kill = 25
        self.enemies_killed = 0
        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.spawn_delay = 900
        self.boss_spawned = False
        self.boss_defeated = False
        self.max_enemies_on_screen = 6

    def update(self):
        """Обновление уровня"""
        current_time = pygame.time.get_ticks()

        if (not self.boss_spawned and
            self.enemies_killed < self.enemies_to_kill and
            len(self.game.enemies) < self.max_enemies_on_screen and
            current_time - self.spawn_timer > self.spawn_delay):
            self.spawn_timer = current_time
            self.spawn_enemy()

        if (not self.boss_spawned and
            self.enemies_killed >= self.enemies_to_kill and
            len(self.game.enemies) == 0):
            self.spawn_boss()

    def spawn_enemy(self):
        """Спавн врага"""
        x = random.randint(80, SCREEN_WIDTH - 80)
        y = -50

        # Более агрессивный спавн - больше сильных врагов
        rand = random.random()
        if rand < 0.20:
            enemy = BasicEnemy(x, y, level=3)
        elif rand < 0.40:
            enemy = SineEnemy(x, y, level=3)
        elif rand < 0.55:
            enemy = ZigZagEnemy(x, y, level=3)
        elif rand < 0.75:
            enemy = ShooterEnemy(x, y, level=3)
        else:
            enemy = TankEnemy(x, y, level=3)

        self.game.all_sprites.add(enemy)
        self.game.enemies.add(enemy)
        self.enemies_spawned += 1

    def spawn_boss(self):
        """Спавн главного босса"""
        self.boss_spawned = True
        boss = BossEnemy(SCREEN_WIDTH // 2, -100, level=3)
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
