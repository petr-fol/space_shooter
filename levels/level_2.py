"""
Уровень 2 - Средняя сложность
"""
import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from enemies import BasicEnemy, SineEnemy, ZigZagEnemy, ShooterEnemy, TankEnemy, BossEnemy


class Level2:
    """Второй уровень - эскалация"""

    def __init__(self, game):
        self.game = game
        self.level_number = 2
        self.name = "Escalation"
        self.enemies_to_kill = 18
        self.enemies_killed = 0
        self.spawn_timer = 0
        self.spawn_delay = 1200
        self.boss_spawned = False
        self.boss_defeated = False
        self.max_enemies_on_screen = 5

    def update(self):
        """Обновление уровня"""
        current_time = pygame.time.get_ticks()

        if not self.boss_spawned:
            if self.enemies_killed >= self.enemies_to_kill:
                self._kill_all_enemies()
                self.spawn_boss()
            else:
                if (len(self.game.enemies) < self.max_enemies_on_screen and
                    current_time - self.spawn_timer > self.spawn_delay):
                    self.spawn_timer = current_time
                    self.spawn_enemy()

        self._check_escaped_enemies()

    def _kill_all_enemies(self):
        """Убить всех обычных врагов"""
        for enemy in list(self.game.enemies):
            if not enemy.is_boss:
                enemy.kill()

    def _check_escaped_enemies(self):
        """Враги, улетевшие за экран, засчитываются как убитые"""
        for enemy in list(self.game.enemies):
            if enemy.rect.top > SCREEN_HEIGHT + 50:
                if not enemy.is_boss:
                    self.enemies_killed += 1
                enemy.kill()

    def spawn_enemy(self):
        """Спавн врага"""
        x = random.randint(80, SCREEN_WIDTH - 80)
        y = -50

        rand = random.random()
        if rand < 0.35:
            enemy = BasicEnemy(x, y, level=2)
        elif rand < 0.55:
            enemy = SineEnemy(x, y, level=2)
        elif rand < 0.70:
            enemy = ZigZagEnemy(x, y, level=2)
        elif rand < 0.85:
            enemy = ShooterEnemy(x, y, level=2)
        else:
            enemy = TankEnemy(x, y, level=2)

        self.game.all_sprites.add(enemy)
        self.game.enemies.add(enemy)

    def spawn_boss(self):
        """Спавн босса"""
        self.boss_spawned = True
        boss = BossEnemy(SCREEN_WIDTH // 2, 80, level=2)
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
        return min(100, int((self.enemies_killed / self.enemies_to_kill) * 100))
