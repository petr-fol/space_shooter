"""
Space Shooter - Главная точка входа
"""
import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, BLACK, DARK_BLUE
from menu import Menu
from game import Game


class SpaceShooter:
    """Основной класс игры"""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"  # menu, game, game_over, victory
        self.menu = Menu(self)
        self.game = None
        self.font = pygame.font.Font(None, 36)
        self.selected_level = 1

    def new_game(self, level=1):
        """Создать новую игру"""
        self.selected_level = level
        self.game = Game(self, level)
        self.state = "game"

    def start_level(self, level):
        """Запустить указанный уровень"""
        self.new_game(level)

    def run(self):
        """Главный цикл игры"""
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

    def events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "game":
                        self.state = "menu"
                        self.game = None
                    elif self.state in ["game_over", "victory"]:
                        self.state = "menu"
                        self.game = None

                # Быстрый рестарт в игре
                if event.key == pygame.K_r and self.state == "game":
                    self.new_game(self.selected_level)

            # Обработка событий в меню
            if self.state == "menu":
                self.menu.handle_event(event)

            # Обработка событий в игре
            elif self.state == "game" and self.game:
                self.game.handle_event(event)

    def update(self):
        """Обновление состояния игры"""
        if self.state == "game" and self.game:
            self.game.update()
            # Проверка окончания игры
            if self.game.player.health <= 0:
                self.state = "game_over"
            elif self.game.level_completed:
                self.state = "victory"
        elif self.state == "menu":
            self.menu.update()

    def draw(self):
        """Отрисовка"""
        self.screen.fill(DARK_BLUE)

        if self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "game" and self.game:
            self.game.draw(self.screen)
        elif self.state == "game_over":
            self.draw_game_over()
        elif self.state == "victory":
            self.draw_victory()

        pygame.display.flip()

    def draw_game_over(self):
        """Экран проигрыша"""
        self.draw_stars()

        text = self.font.render("GAME OVER", True, RED := (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)

        score_text = self.font.render(f"Score: {self.game.score if self.game else 0}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)

        restart_text = self.font.render("Press ENTER to restart or ESC for menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(restart_text, restart_rect)

        # Проверка нажатия ENTER
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.new_game(self.selected_level)

    def draw_victory(self):
        """Экран победы"""
        self.draw_stars()

        text = self.font.render("VICTORY!", True, GREEN := (0, 255, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)

        score_text = self.font.render(f"Final Score: {self.game.score if self.game else 0}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)

        restart_text = self.font.render("Press ENTER to play again or ESC for menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(restart_text, restart_rect)

        # Проверка нажатия ENTER
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.new_game(1)

    def draw_stars(self):
        """Рисование звёздного фона"""
        import random
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(self.screen, WHITE, (x, y), random.randint(1, 2))


if __name__ == "__main__":
    game = SpaceShooter()
    game.run()
