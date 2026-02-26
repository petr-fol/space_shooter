"""
Уровень 3 - Сложный
Те же враги, но босс ещё сильнее и нужно убить ещё больше врагов
"""
import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from enemies import BasicEnemy, SineEnemy, BossEnemy


class Level3:
    """Третий уровень - финальная битва"""

    def __init__(self, game):
        self.game = game
        self.level_number = 3
        self.name = "Final Battle"
        self.enemies_to_kill = 25  # Ещё больше
        self.enemies_killed = 0
        self.spawn_timer = 0
        self.spawn_delay = 900  # Ещё быстрее спавн
        self.boss_spawned = False
        self.boss_defeated = False
        self.max_enemies_on_screen = 6

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
        """Спавн обычного врага"""
        x = random.randint(80, SCREEN_WIDTH - 80)
        y = -50

        # Те же враги что и в уровне 1
        if random.random() < 0.7:
            enemy = BasicEnemy(x, y, level=3)  # Но с параметрами уровня 3
        else:
            enemy = SineEnemy(x, y, level=3)

        self.game.all_sprites.add(enemy)
        self.game.enemies.add(enemy)

    def spawn_boss(self):
        """Спавн босса"""
        self.boss_spawned = True
        boss = BossEnemy(SCREEN_WIDTH // 2, 80, level=3)  # Босс уровня 3 (самый сильный)
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
