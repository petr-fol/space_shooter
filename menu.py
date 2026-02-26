"""
Меню игры
"""
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, CYAN,
    YELLOW, RED, DARK_BLUE, GREEN
)
from sounds import SoundManager


class Menu:
    """Класс меню"""

    def __init__(self, game):
        self.game = game
        self.sound_manager = game.sound_manager
        self.selected_option = 0
        self.main_options = ["Start Game", "Select Level", "Controls", "Exit"]
        self.level_options = ["Level 1", "Level 2", "Level 3", "Back"]
        self.selected_level = 0
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.title_y = 100
        self.options_y = 280
        self.blink_timer = 0
        self.show_controls = False
        self.show_level_select = False
        self.star_field = None

        from effects import StarField
        self.star_field = StarField(SCREEN_WIDTH, SCREEN_HEIGHT, star_count=150, speed=1)

    def handle_event(self, event):
        """Обработка событий меню"""
        if event.type == pygame.KEYDOWN:
            if self.show_controls:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    if self.sound_manager:
                        self.sound_manager.play("select")
                    self.show_controls = False
                return

            if self.show_level_select:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_level = (self.selected_level - 1) % len(self.level_options)
                    if self.sound_manager:
                        self.sound_manager.play("select")
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_level = (self.selected_level + 1) % len(self.level_options)
                    if self.sound_manager:
                        self.sound_manager.play("select")
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.selected_level == 3:  # Back
                        if self.sound_manager:
                            self.sound_manager.play("select")
                        self.show_level_select = False
                        self.selected_option = 0
                    else:
                        # Выбор уровня
                        self.game.start_level(self.selected_level + 1)
                return

            # Главное меню
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.main_options)
                if self.sound_manager:
                    self.sound_manager.play("select")
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.main_options)
                if self.sound_manager:
                    self.sound_manager.play("select")
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.select_option()

    def select_option(self):
        """Выбор опции меню"""
        if self.selected_option == 0:
            self.game.start_level(1)
        elif self.selected_option == 1:
            self.show_level_select = True
            self.selected_level = 0
        elif self.selected_option == 2:
            self.show_controls = True
        elif self.selected_option == 3:
            self.game.running = False

    def update(self):
        """Обновление меню"""
        self.blink_timer += 1
        if self.star_field:
            self.star_field.update()

    def draw(self, surface):
        """Отрисовка меню"""
        if self.star_field:
            self.star_field.draw(surface)
        else:
            surface.fill(DARK_BLUE)

        if self.show_controls:
            self.draw_controls(surface)
        elif self.show_level_select:
            self.draw_level_select(surface)
        else:
            self.draw_main_menu(surface)

    def draw_main_menu(self, surface):
        """Отрисовка главного меню"""
        # Заголовок
        title = self.font_large.render("SPACE SHOOTER", True, CYAN)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=self.title_y)

        # Эффект свечения
        for i in range(3, 0, -1):
            glow_color = (0, 255 // i, 255 // i)
            glow_surface = self.font_large.render("SPACE SHOOTER", True, glow_color)
            glow_rect = glow_surface.get_rect(centerx=SCREEN_WIDTH // 2 + i, y=self.title_y + i)
            surface.blit(glow_surface, glow_rect)
            glow_rect = glow_surface.get_rect(centerx=SCREEN_WIDTH // 2 - i, y=self.title_y - i)
            surface.blit(glow_surface, glow_rect)

        surface.blit(title, title_rect)

        # Подзаголовок
        subtitle = self.font_small.render("The Final Battle", True, WHITE)
        subtitle_rect = subtitle.get_rect(centerx=SCREEN_WIDTH // 2, y=self.title_y + 70)
        surface.blit(subtitle, subtitle_rect)

        # Опции меню
        for i, option in enumerate(self.main_options):
            y = self.options_y + i * 60

            if i == self.selected_option:
                if self.blink_timer % 40 < 20:
                    cursor = self.font_medium.render("►", True, YELLOW)
                    cursor_rect = cursor.get_rect(x=SCREEN_WIDTH // 2 - 150, centery=y)
                    surface.blit(cursor, cursor_rect)

                text = self.font_medium.render(option, True, YELLOW)
            else:
                text = self.font_medium.render(option, True, WHITE)

            text_rect = text.get_rect(centerx=SCREEN_WIDTH // 2, centery=y)
            surface.blit(text, text_rect)

        # Управление внизу
        controls_hint = self.font_small.render("↑↓ to select | ENTER to confirm | ESC to quit", True, (150, 150, 150))
        controls_rect = controls_hint.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 50)
        surface.blit(controls_hint, controls_rect)

    def draw_level_select(self, surface):
        """Отрисовка выбора уровня"""
        # Заголовок
        title = self.font_medium.render("SELECT LEVEL", True, CYAN)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=100)
        surface.blit(title, title_rect)

        # Опции уровней
        for i, option in enumerate(self.level_options):
            y = self.options_y + i * 60

            if i == self.selected_level:
                if self.blink_timer % 40 < 20:
                    cursor = self.font_medium.render("►", True, YELLOW)
                    cursor_rect = cursor.get_rect(x=SCREEN_WIDTH // 2 - 150, centery=y)
                    surface.blit(cursor, cursor_rect)

                text = self.font_medium.render(option, True, YELLOW)
            else:
                text = self.font_medium.render(option, True, WHITE)

            text_rect = text.get_rect(centerx=SCREEN_WIDTH // 2, centery=y)
            surface.blit(text, text_rect)

        # Описание уровней
        level_descriptions = [
            "Level 1: Introduction - Easy enemies, slow pace",
            "Level 2: Escalation - Mixed enemies, medium pace",
            "Level 3: Final Battle - Hard enemies, fast pace"
        ]

        for i, desc in enumerate(level_descriptions):
            y = self.options_y + len(self.level_options) * 60 + i * 30
            text = self.font_small.render(desc, True, (150, 150, 150))
            text_rect = text.get_rect(centerx=SCREEN_WIDTH // 2, y=y)
            surface.blit(text, text_rect)

    def draw_controls(self, surface):
        """Отрисовка экрана управления"""
        # Заголовок
        title = self.font_medium.render("CONTROLS", True, CYAN)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=100)
        surface.blit(title, title_rect)

        # Список управления
        controls = [
            "Movement: WASD or Arrow Keys",
            "Shoot: SPACE",
            "Pause/Menu: ESC",
            "",
            "Destroy enemies to earn points",
            "Avoid enemy bullets and collisions",
            f"Kill {10} enemies to summon the boss",
            "",
            "Press ENTER or ESC to return"
        ]

        for i, line in enumerate(controls):
            if i == 8:
                color = YELLOW
            else:
                color = WHITE

            text = self.font_small.render(line, True, color)
            text_rect = text.get_rect(centerx=SCREEN_WIDTH // 2, y=180 + i * 35)
            surface.blit(text, text_rect)

        # Декоративные элементы
        pygame.draw.line(surface, CYAN, (SCREEN_WIDTH // 2 - 200, 150),
                        (SCREEN_WIDTH // 2 + 200, 150), 2)
        pygame.draw.line(surface, CYAN, (SCREEN_WIDTH // 2 - 150, 480),
                        (SCREEN_WIDTH // 2 + 150, 480), 2)
