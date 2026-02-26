"""
Система столкновений и система очков
"""
import pygame
from settings import WHITE, YELLOW, GREEN


class CollisionSystem:
    """Система обработки столкновений"""

    def __init__(self, game):
        self.game = game

    def check_collisions(self):
        """Проверка всех столкновений"""
        self.check_player_bullets_hit_enemies()
        self.check_enemy_bullets_hit_player()
        self.check_enemies_collide_player()

    def check_player_bullets_hit_enemies(self):
        """Проверка попадания пуль игрока во врагов"""
        hits = pygame.sprite.groupcollide(
            self.game.enemies,
            self.game.player_bullets,
            False,
            True
        )

        # Используем list() для безопасной итерации
        for enemy in list(hits.keys()):
            if enemy not in self.game.enemies:
                continue
            bullets = hits[enemy]
            for bullet in bullets:
                damaged = enemy.take_damage(bullet.damage)
                if damaged:
                    # Враг уничтожен
                    self.game.score.add_score(enemy.score_value)
                    if self.game.level:
                        self.game.level.on_enemy_defeated(enemy)

                    # Эффект взрыва
                    from effects import Explosion
                    explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                    self.game.all_sprites.add(explosion)

                    # Звук взрыва
                    if self.game.sound_manager:
                        self.game.sound_manager.play("explosion")

                    # Всплывающие очки
                    from effects import ScorePopup
                    popup = ScorePopup(enemy.rect.centerx, enemy.rect.centery,
                                      f"+{enemy.score_value}", YELLOW)
                    self.game.score_popups.append(popup)
                    break

    def check_enemy_bullets_hit_player(self):
        """Проверка попадания пуль врагов в игрока"""
        hits = pygame.sprite.spritecollide(
            self.game.player,
            self.game.enemy_bullets,
            True
        )

        for bullet in hits:
            self.game.player.take_damage(bullet.damage)
            # Звук получения урона
            if self.game.sound_manager:
                self.game.sound_manager.play("player_hit")

    def check_enemies_collide_player(self):
        """Проверка столкновения врагов с игроком"""
        hits = pygame.sprite.spritecollide(
            self.game.player,
            self.game.enemies,
            False
        )

        for enemy in hits:
            damaged = enemy.take_damage(50)
            if damaged:
                self.game.score.add_score(enemy.score_value)
                if self.game.level:
                    self.game.level.on_enemy_defeated(enemy)

                from effects import Explosion
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                self.game.all_sprites.add(explosion)
                
                # Звук взрыва
                if self.game.sound_manager:
                    self.game.sound_manager.play("explosion")

            self.game.player.take_damage(enemy.damage)


class Score:
    """Система подсчёта очков"""

    def __init__(self):
        self.score = 0
        self.high_score = self.load_high_score()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def add_score(self, points):
        """Добавление очков"""
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def reset(self):
        """Сброс очков"""
        self.score = 0

    def load_high_score(self):
        """Загрузка рекорда"""
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        """Сохранение рекорда"""
        try:
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))
        except IOError:
            pass

    def draw(self, surface, x, y):
        """Отрисовка счёта"""
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(topright=(x, y))
        surface.blit(score_text, score_rect)

        highscore_text = self.small_font.render(f"Best: {self.high_score}", True, YELLOW)
        highscore_rect = highscore_text.get_rect(topright=(x, y + 30))
        surface.blit(highscore_text, highscore_rect)

    def draw_centered(self, surface, y, color=WHITE):
        """Отрисовка счёта по центру"""
        score_text = self.font.render(f"Score: {self.score}", True, color)
        score_rect = score_text.get_rect(centerx=surface.get_width() // 2, top=y)
        surface.blit(score_text, score_rect)
