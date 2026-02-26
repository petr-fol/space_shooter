"""
Менеджер звуков для игры
"""
import pygame
import os


class SoundManager:
    """Класс для управления звуковыми эффектами"""

    def __init__(self):
        """Инициализация звуковой системы"""
        self.sounds = {}
        self.enabled = True
        
        # Путь к папке со звуками
        self.sounds_dir = os.path.join(os.path.dirname(__file__), "assets", "sounds")
        
        # Загрузка звуков
        self._load_sounds()

    def _load_sounds(self):
        """Загрузка всех звуковых файлов"""
        try:
            # Звук выстрела игрока
            self.sounds["shoot"] = pygame.mixer.Sound(
                os.path.join(self.sounds_dir, "jg-032316-sfx-8-bit-zap-sound-2.mp3")
            )
            self.sounds["shoot"].set_volume(0.3)
            
            # Звук взрыва врагов
            self.sounds["explosion"] = pygame.mixer.Sound(
                os.path.join(self.sounds_dir, "jg-032316-sfx-8-bit-crash-2.mp3")
            )
            self.sounds["explosion"].set_volume(0.4)
            
            # Звук выбора в меню
            self.sounds["select"] = pygame.mixer.Sound(
                os.path.join(self.sounds_dir, "jg-032316-sfx-8-bit-button-select.mp3")
            )
            self.sounds["select"].set_volume(0.3)
            
            # Звук попадания (опционально)
            self.sounds["hit"] = pygame.mixer.Sound(
                os.path.join(self.sounds_dir, "jg-032316-sfx-8-bit-hit-6.mp3")
            )
            self.sounds["hit"].set_volume(0.3)
            
            # Звук получения урона игроком
            self.sounds["player_hit"] = pygame.mixer.Sound(
                os.path.join(self.sounds_dir, "jg-032316-sfx-8-bit-punch.mp3")
            )
            self.sounds["player_hit"].set_volume(0.35)
            
        except pygame.error as e:
            print(f"Не удалось загрузить звуки: {e}")
            self.enabled = False

    def play(self, sound_name):
        """Воспроизведение звука по имени"""
        if not self.enabled:
            return
        
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def stop(self, sound_name):
        """Остановка конкретного звука"""
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()

    def stop_all(self):
        """Остановка всех звуков"""
        pygame.mixer.stop()

    def set_volume(self, sound_name, volume):
        """Установка громкости для конкретного звука"""
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(max(0.0, min(1.0, volume)))

    def mute(self):
        """Отключить все звуки"""
        self.enabled = False
        self.stop_all()

    def unmute(self):
        """Включить звуки"""
        self.enabled = True
